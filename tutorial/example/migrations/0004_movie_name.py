# Generated by Django 2.2 on 2020-01-11 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0003_auto_20200111_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='name',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
