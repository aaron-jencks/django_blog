# Generated by Django 2.1.1 on 2018-10-03 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_auto_20181003_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='posttopic',
            name='articles',
            field=models.ManyToManyField(to='blogapp.BlogPost'),
        ),
    ]