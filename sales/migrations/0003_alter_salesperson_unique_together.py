# Generated by Django 5.0.1 on 2024-07-26 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_alter_salesperson_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='salesperson',
            unique_together=set(),
        ),
    ]
