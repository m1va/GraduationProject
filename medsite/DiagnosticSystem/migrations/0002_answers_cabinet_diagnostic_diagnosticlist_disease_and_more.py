# Generated by Django 4.0.1 on 2022-01-22 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DiagnosticSystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Ответ')),
            ],
        ),
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(verbose_name='Номер кабинета')),
            ],
        ),
        migrations.CreateModel(
            name='Diagnostic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DiagnosticList',
            fields=[
                ('result', models.TextField(verbose_name='Список диагностик пациента')),
                ('diagnostic_date', models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False)),
                ('diagnostic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.diagnostic')),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название заболевания')),
            ],
        ),
        migrations.CreateModel(
            name='DiseaseDiagnostics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnostic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.diagnostic')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.disease')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=50, verbose_name='Отчество')),
                ('cabinet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.cabinet')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('patronymic', models.CharField(max_length=50)),
                ('birthday_date', models.DateField(verbose_name='Дата рождения')),
            ],
        ),
        migrations.CreateModel(
            name='PatientAnswers',
            fields=[
                ('answer_date', models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False, verbose_name='Дата ответа')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.answers')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('diagnostic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.diagnostic')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Вопрос')),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название специальности')),
            ],
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AddField(
            model_name='patientanswers',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.questions'),
        ),
        migrations.AddField(
            model_name='employee',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.speciality'),
        ),
        migrations.AddField(
            model_name='diagnosticlist',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.employee'),
        ),
        migrations.AddField(
            model_name='diagnosticlist',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.patient'),
        ),
        migrations.AddField(
            model_name='answers',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DiagnosticSystem.questions'),
        ),
    ]