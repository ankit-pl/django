# Generated by Django 3.2.8 on 2021-10-15 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='metadata',
            field=models.JSONField(default=list),
        ),
    ]
