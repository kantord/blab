# Generated by Django 3.0.4 on 2020-03-26 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0026_dictionaryitem_reverse'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dictionaryitem',
            unique_together={('course', 'word', 'reverse')},
        ),
    ]
