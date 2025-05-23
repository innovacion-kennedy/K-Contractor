# Generated by Django 5.1.7 on 2025-05-07 14:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('nombre', models.CharField(db_column='nombre', default='Área General', max_length=255)),
            ],
            options={
                'db_table': 'area',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('proyecto', models.CharField(db_column='proyecto', default='Proyecto X', max_length=255)),
                ('actividad', models.TextField(blank=True, db_column='actividad', null=True)),
                ('arl', models.CharField(db_column='arl', default='Positiva', max_length=100)),
                ('eps', models.CharField(db_column='eps', default='Nueva EPS', max_length=100)),
                ('fondo_pensiones', models.CharField(db_column='fondo_pensiones', default='Colpensiones', max_length=100)),
                ('sipse', models.CharField(blank=True, db_column='sipse', max_length=100, null=True)),
                ('cdp', models.CharField(blank=True, db_column='cdp', max_length=100, null=True)),
                ('objeto_contrato', models.TextField(db_column='objeto_contrato', default='Por definir')),
                ('honorarios', models.DecimalField(db_column='honorarios', decimal_places=2, default=0.0, max_digits=14)),
                ('duracion_meses', models.IntegerField(db_column='duracion_meses', default=1)),
                ('modalidad_pago', models.CharField(db_column='modalidad_pago', default='Mensual', max_length=100)),
                ('fuente_recurso', models.CharField(db_column='fuente_recurso', default='Recursos propios', max_length=100)),
                ('estado_contrato', models.CharField(db_column='estado_contrato', default='Pendiente', max_length=100)),
                ('fecha_inicio', models.DateField(db_column='fecha_inicio', default=django.utils.timezone.now)),
                ('fecha_fin', models.DateField(db_column='fecha_fin', default=django.utils.timezone.now)),
                ('fecha_firma_contrato', models.DateField(db_column='fecha_firma_contrato', default=django.utils.timezone.now)),
                ('numero_contrato', models.CharField(db_column='numero_contrato', default='TEMP-0001', max_length=100)),
                ('supervisor_nombre', models.CharField(db_column='supervisor_nombre', default='Supervisor X', max_length=255)),
                ('supervisor_cargo', models.CharField(db_column='supervisor_cargo', default='Cargo X', max_length=255)),
                ('supervisor_correo', models.EmailField(db_column='supervisor_correo', default='correo@example.com', max_length=254)),
                ('supervisor_telefono', models.CharField(db_column='supervisor_telefono', default='123456789', max_length=100)),
                ('documento_rut', models.CharField(db_column='documento_rut', default='rut.pdf', max_length=255)),
                ('documento_cert_bancaria', models.CharField(db_column='documento_cert_bancaria', default='cert_bancaria.pdf', max_length=255)),
                ('documento_seguridad_social', models.CharField(db_column='documento_seguridad_social', default='seg_social.pdf', max_length=255)),
                ('documento_antecedentes', models.CharField(db_column='documento_antecedentes', default='antecedentes.pdf', max_length=255)),
                ('documento_poliza', models.CharField(db_column='documento_poliza', default='poliza.pdf', max_length=255)),
                ('observaciones', models.TextField(blank=True, db_column='observaciones', null=True)),
                ('ultima_actualizacion', models.DateTimeField(auto_now=True, db_column='ultima_actualizacion')),
            ],
            options={
                'db_table': 'contrato',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Convocatoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(db_column='titulo', max_length=255)),
                ('descripcion', models.TextField(db_column='descripcion')),
                ('documento', models.FileField(blank=True, db_column='documento', null=True, upload_to='convocatorias/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')),
                ('estado', models.CharField(choices=[('Abierta', 'Abierta'), ('Cerrada', 'Cerrada'), ('En evaluación', 'En evaluación')], db_column='estado', default='Abierta', max_length=20)),
            ],
            options={
                'db_table': 'convocatoria',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('tipo_documento', models.CharField(db_column='tipo', max_length=100)),
                ('archivo', models.TextField(db_column='archivo')),
                ('estado', models.CharField(db_column='estado', max_length=50)),
                ('fecha_carga', models.DateTimeField(auto_now_add=True, db_column='fecha_carga')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, db_column='fecha_modificacion')),
            ],
            options={
                'db_table': 'documento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EvaluacionHV',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('puntaje', models.IntegerField(db_column='puntaje')),
                ('observaciones', models.TextField(blank=True, db_column='observaciones', null=True)),
                ('estado', models.CharField(db_column='estado', max_length=50)),
                ('fecha_evaluacion', models.DateTimeField(auto_now_add=True, db_column='fecha')),
                ('fecha_asociacion', models.DateTimeField(blank=True, db_column='fecha_asociacion', null=True)),
            ],
            options={
                'db_table': 'evaluacionhv',
                'managed': True,
            },
        ),
    ]
