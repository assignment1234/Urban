# Generated by Django 2.0.8 on 2019-05-16 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urban', '0003_auto_20190515_0445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskstate',
            options={'ordering': ('-created',)},
        ),
    ]