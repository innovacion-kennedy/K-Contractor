# Generated by Django 5.1.7 on 2025-03-26 18:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_contrato', models.CharField(max_length=50, unique=True)),
                ('numero_proyecto', models.CharField(max_length=50)),
                ('nombre_proyecto', models.CharField(max_length=200)),
                ('fecha_suscripcion', models.DateField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_terminacion', models.DateField()),
                ('valor_inicial_contrato', models.DecimalField(decimal_places=2, max_digits=12)),
                ('valor_total_con_adiciones', models.DecimalField(decimal_places=2, max_digits=12)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado'), ('Finalizado', 'Finalizado')], default='Pendiente', max_length=20)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Convocatoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('documento', models.FileField(blank=True, null=True, upload_to='convocatorias/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('Abierta', 'Abierta'), ('Cerrada', 'Cerrada'), ('En evaluación', 'En evaluación')], default='Abierta', max_length=20)),
                ('creada_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_documento', models.CharField(choices=[('Hoja de Vida', 'Hoja de Vida'), ('Cédula', 'Cédula'), ('Certificación Mínima', 'Certificación Mínima')], max_length=50)),
                ('archivo', models.FileField(upload_to='contratos/documentos/')),
                ('estado', models.CharField(default='Pendiente', max_length=20)),
                ('fecha_carga', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('contratista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='login.persona')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentosContrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_documento', models.CharField(max_length=100)),
                ('archivo', models.FileField(upload_to='contratos/documentos/')),
                ('estado', models.CharField(default='Pendiente', max_length=20)),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('ultima_actualizacion', models.DateTimeField(auto_now=True)),
                ('contratista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.persona')),
                ('contrato', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contratacion.contrato')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluacionHV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje', models.IntegerField(default=0)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado')], default='Pendiente', max_length=10)),
                ('fecha_evaluacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_asociacion', models.DateTimeField(blank=True, null=True)),
                ('contratista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='login.persona')),
                ('convocatoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='contratacion.convocatoria')),
                ('evaluador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SeguimientoContrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seguimientos', to='contratacion.contrato')),
            ],
        ),
    ]
