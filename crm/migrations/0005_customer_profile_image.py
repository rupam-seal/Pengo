# Generated by Django 4.1.1 on 2022-09-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_image',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to=''),
        ),
    ]