# Generated by Django 4.2.3 on 2023-07-23 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentApp', '0008_alter_arrendatario_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='planta',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='plantas/'),
        ),
    ]
