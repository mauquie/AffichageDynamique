# Generated by Django 3.2.3 on 2021-11-25 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiServer', '0002_delete_survey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sondage',
            name='est_affiche',
            field=models.BooleanField(default=False),
        ),
    ]
