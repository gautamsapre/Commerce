# Generated by Django 3.0.8 on 2020-08-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='category',
            field=models.CharField(choices=[('FAS', 'Fashion'), ('ELC', 'Electronics'), ('TYS', 'Toys'), ('HME', 'Home'), ('ATO', 'Auto')], default='Auto', max_length=3),
        ),
    ]