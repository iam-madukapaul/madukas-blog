# Generated by Django 4.2.2 on 2023-06-25 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_alter_contact_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.IntegerField(),
        ),
    ]