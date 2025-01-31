# Generated by Django 5.1.4 on 2025-01-30 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="address_line_1",
            new_name="address",
        ),
        migrations.RenameField(
            model_name="order",
            old_name="first_name",
            new_name="name",
        ),
        migrations.RemoveField(
            model_name="order",
            name="ip",
        ),
        migrations.RemoveField(
            model_name="order",
            name="last_name",
        ),
        migrations.RemoveField(
            model_name="order",
            name="tax",
        ),
    ]
