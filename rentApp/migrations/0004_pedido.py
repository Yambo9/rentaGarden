# Generated by Django 4.2.2 on 2023-07-18 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentApp', '0003_admin_caracteristica_arrendatario_ultimo_login_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=200)),
                ('numero', models.IntegerField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_termino', models.DateField()),
                ('hora_inicio', models.TimeField(blank=True, null=True)),
                ('hora_termino', models.TimeField(blank=True, null=True)),
                ('instrucciones', models.TextField(blank=True, null=True)),
                ('peso', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('valorFlete', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('arrendatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentApp.arrendatario')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentApp.comuna')),
            ],
        ),
    ]
