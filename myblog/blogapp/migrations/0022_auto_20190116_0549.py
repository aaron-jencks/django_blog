# Generated by Django 2.1.5 on 2019-01-16 05:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0021_auto_20190116_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitenews',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 16, 5, 49, 49, 458396, tzinfo=utc), verbose_name='date published'),
        ),
    ]