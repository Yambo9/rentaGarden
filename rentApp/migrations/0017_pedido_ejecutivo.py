# Generated by Django 4.2.3 on 2023-07-29 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentApp', '0016_ejecutivo_telefono'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='ejecutivo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rentApp.ejecutivo'),
            preserve_default=False,
        ),
    ]
