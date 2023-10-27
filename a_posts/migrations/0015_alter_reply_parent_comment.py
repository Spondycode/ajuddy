# Generated by Django 4.2.6 on 2023-10-24 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0014_rename_parent_post_reply_parent_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='parent_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='a_posts.comment'),
        ),
    ]
