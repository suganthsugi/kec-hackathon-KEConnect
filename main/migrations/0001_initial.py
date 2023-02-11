# Generated by Django 4.1.2 on 2023-02-04 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, max_length=35, null=True)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('draft', 'draft'), ('published', 'published')], default='draft', max_length=60, null=True)),
                ('visibility', models.CharField(blank=True, choices=[('public', 'public'), ('private', 'private'), ('deleted', 'deleted')], default='public', max_length=70, null=True)),
                ('dt_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('dt_updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('dt_published', models.DateTimeField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(blank=True, choices=[('Sexual content', 'Sexual content'), ('Violent or repulsive content', 'Violent or repulsive content'), ('Hateful or abusive content', 'Hateful or abusive content'), ('Harassment or bullying', 'Harassment or bullying'), ('Harmful or dangerous acts', 'Harmful or dangerous acts'), ('Misinformation', 'Misinformation'), ('Child abuse', 'Child abuse'), ('Promotes terrorism', 'Promotes terrorism'), ('Spam or misleading', 'Spam or misleading'), ('Infringes my rights', 'Infringes my rights'), ('Captions issue', 'Captions issue')], max_length=70, null=True)),
                ('dt_reported', models.DateTimeField(auto_now_add=True, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_linked', models.DateTimeField(auto_now_add=True, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
