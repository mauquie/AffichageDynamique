# Generated by Django 3.2.3 on 2021-09-28 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiServer', '0002_auto_20210829_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='modification_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
