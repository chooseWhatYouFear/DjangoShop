# Generated by Django 2.1.8 on 2019-07-25 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='connect_address',
            field=models.TextField(blank=True, null=True, verbose_name='联系地址'),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='phone',
            field=models.IntegerField(blank=True, null=True, verbose_name='联系电话'),
        ),
    ]
