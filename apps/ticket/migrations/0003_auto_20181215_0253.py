# Generated by Django 2.1.3 on 2018-12-15 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_ticket_booked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='flight',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
