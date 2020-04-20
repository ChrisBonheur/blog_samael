from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from random import choice

from .models import Article, Category, Comment, ResponseComment, Utilisateur


def articles_comment_count(request, article_by_page, filter_name=""):
    """This function create a list with articles by page"""
    #verifictaion if filter exist to return articles with filter or no
    if filter_name == "":
        all_articles_list = Article.objects.all()
    else:
        all_articles_list = Article.objects.filter(title__icontains=filter_name)
        if not all_articles_list.exists():
            categories = Category.objects.filter(name__icontains=filter_name)
            all_articles_list = Article.objects.filter(category=categories)
            if not all_articles_list.exists():
                return False
                     
    #cretaing paginator with all_articles
    paginator = Paginator(all_articles_list, article_by_page)
    page = request.GET.get('page')
    try:
        all_articles = paginator.page(page)
    except PageNotAnInteger:
        all_articles = paginator.page(1)
    except EmptyPage:
        all_articles = paginator.page(paginator.num_pages)

    #creating of dictionnary (article and their comment count)    
    articles_comments = {} #this for all article and their comment count
    for article in all_articles:
        #this loop add to dict article_comment the key and value(article and comment count)
        comment_count = Comment.objects.filter(article__title=article.title).count()
        articles_comments[article] = comment_count
    
    return all_articles, articles_comments

def categories_articles_count():
    """This function return table of categories and dict(categories with their 
    count articles)"""
    categories = Category.objects.all()
    #creating of dictionnary for categories with their articles count
    categories_articles_count = {}
    for category in  categories:
        #This loop add to dict categories_articles_count categories and their count article
        article_count = Article.objects.filter(category__name=category.name).count()
        categories_articles_count[category] = article_count
    
    return categories, categories_articles_count

def get_articles_limit(limit_number):
    """this function get articles with limited_number"""
    last_article = Article.objects.last()
    all_articles_limit = Article.objects.exclude(pk=last_article.id)[:limit_number]
    #creating of dictionnary (article and their comment count)
    articles_comments_limit = {} # this for article limit  and their comment count
    for article in all_articles_limit:
        #this loop add to dict article_comment the key and value(article and comment count)
        comment_count = Comment.objects.filter(article__title=article.title).count()
        articles_comments_limit[article] = comment_count   
    
    return articles_comments_limit    

def index(request):
    last_article = Article.objects.last()          
    articles_comments_limit = get_articles_limit(3)#getting limited articles by 3 artilces
    #getting of table categories and dict of categories with their count articles
    categories, categories_articles = categories_articles_count()
    #getting of table articles and dict of articles with their count comments
    all_articles, articles_comment = articles_comment_count(request, 2)
    
    # get total comment for last article
    last_article_count_comment = Comment.objects.filter(article__id=last_article.id)
    last_article_count_comment = last_article_count_comment.count()
   
    # random posts for bloc other posts
    random_post_comment = {}
    for i in range(3):
        article = choice(all_articles)
        comment_count = Comment.objects.filter(article__title=article).count()
        random_post_comment[article] = comment_count
        
    context = {
        "articles_comments_limit": articles_comments_limit,
        "articles_comments": articles_comment,
        "all_articles": all_articles,
        "last_article": last_article,
        "last_article_count_comment": last_article_count_comment,
        "categories_articles_count": categories_articles,
        "categories": categories,
        "random_posts": random_post_comment
    }
    
    return render(request, 'blog/index.html', context)

def single_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    context = {
        "article_date": article.date_create,
        "article_title": article.title,
        "article_content": article.content,
        "article_category": article.category
    }
    return render(request, 'blog/blog-single.html', context)

def about(request):
    """This function customise the about.html page"""
    #getting of categories and categories with articles count
    categories, categories_articles = categories_articles_count()
    #getting all articles and all articles with their comment count
    all_articles, articles_comment = articles_comment_count(request, 3)
    
    
    context = {
        "articles_comment": articles_comment,
        "all_articles": all_articles,
        "categories": categories,
        "categories_articles_count": categories_articles,
        "articles_comments_limit": get_articles_limit(3)
    }
    return render(request, 'blog/about.html', context)

def contact(request):
    context = {
        
    }
    return render(request, 'blog/contact.html', context)

def search(request):
    query = request.GET.get('query')
    query = str(query)
    title = "Résultat pour la recherche {}".format(query)
    if not query:
        articles_comments = articles_comment_count(request, 2)
    else:
        articles_comments = articles_comment_count(request, 2, query)
        
        if not articles_comments == False:
            title = "Aucun résultat pour la recherche {}".format(query)
    
    context = {
        "articles_comment": articles_comments,
        "title": title
    }
    
    return render(request, 'blog/search.html', context)