# Generated by Django 3.0.5 on 2020-05-08 12:06

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tcas', '0013_auto_20200503_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=versatileimagefield.fields.VersatileImageField(blank=True, upload_to='avatars'),
        ),
    ]
