# Generated by Django 2.1.1 on 2018-10-09 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0012_auto_20181009_0417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumcomment',
            name='question_target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.AskPost'),
        ),
    ]