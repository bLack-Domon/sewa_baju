# Generated by Django 4.2.7 on 2024-07-14 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_detailsewa_jangkasewa'),
    ]

    operations = [
        migrations.AddField(
            model_name='sewa',
            name='status_batalpesanan',
            field=models.CharField(choices=[('Tidak', 'Tidak'), ('Batal', 'Batal')], default='Tidak', max_length=20),
        ),
    ]
