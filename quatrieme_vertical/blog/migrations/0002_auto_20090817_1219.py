# Generated by Django 2.2.11 on 2009-08-17 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Article'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(),
        ),
    ]
