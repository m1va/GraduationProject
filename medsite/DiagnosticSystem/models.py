from django.db import models
from django.contrib.auth.models import User


class Disease(models.Model):
    name = models.CharField(max_length=50, verbose_name='Заболевание')
    membership_chart = models.ForeignKey('MembershipChart', on_delete=models.PROTECT,
                                         verbose_name='График принадлежности', blank=True, null=True)

    def __str__(self):
        return self.name


class Diagnostic(models.Model):
    name = models.CharField(max_length=128, verbose_name='Диагностика')

    def __str__(self):
        return self.name


class DiseaseDiagnostics(models.Model):
    disease = models.ForeignKey('Disease', on_delete=models.PROTECT, verbose_name='Заболевание')
    diagnostic = models.ForeignKey('Diagnostic', on_delete=models.PROTECT, verbose_name='Диагностика')


class Cabinet(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name='Номер кабинета')

    def __str__(self):
        return str(self.number)


class Speciality(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название специальности')

    def __str__(self):
        return self.title


class Employee(models.Model):
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество')
    cabinet = models.ForeignKey('Cabinet', on_delete=models.PROTECT, verbose_name='Кабинет')
    speciality = models.ForeignKey('Speciality', on_delete=models.PROTECT, verbose_name='Специальность')

    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic


class Price(models.Model):
    price = models.FloatField()
    diagnostic = models.ForeignKey('Diagnostic', on_delete=models.PROTECT, verbose_name='Диагностика')
    employee = models.ForeignKey('Employee', on_delete=models.PROTECT, verbose_name='Сотрудник')


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=50, verbose_name='Отчество')
    birthday_date = models.DateField(verbose_name='Дата рождения')

    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class Questions(models.Model):
    title = models.CharField(max_length=30, verbose_name='Вопрос')

    def __str__(self):
        return self.title


class Answers(models.Model):
    title = models.CharField(max_length=30, verbose_name='Ответ')
    question = models.ForeignKey('Questions', on_delete=models.PROTECT, verbose_name='Вопрос')
    disease = models.ForeignKey('Disease', on_delete=models.PROTECT, verbose_name='Заболевание')
    number_of_points = models.PositiveSmallIntegerField(verbose_name='Количество баллов', blank=True, null=True)

    def __str__(self):
        return self.title


class PatientAnswers(models.Model):
    answer = models.ForeignKey('Answers', on_delete=models.PROTECT, verbose_name='Ответ')
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, verbose_name='Пациент')
    question = models.ForeignKey('Questions', on_delete=models.PROTECT, verbose_name='Вопрос')
    answer_date = models.DateTimeField(auto_now_add=True, primary_key=True, verbose_name='Дата ответа')


class DiagnosticList(models.Model):
    result = models.TextField(blank=False, verbose_name='Список диагностик пациента')
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT, verbose_name='Пациент')
    diagnostic = models.ForeignKey('Diagnostic', on_delete=models.PROTECT, verbose_name='Диагностика')
    employee = models.ForeignKey('Employee', on_delete=models.PROTECT, verbose_name='Сотрудник')
    diagnostic_date = models.DateTimeField(auto_now_add=True, primary_key=True, verbose_name='Дата диагностирования')


class MembershipChart(models.Model):
    membership_id = models.BigIntegerField(primary_key=True, verbose_name='График принадлежности №')


class MembershipFunction(models.Model):
    membership_chart = models.ForeignKey('MembershipChart', on_delete=models.PROTECT,
                                         verbose_name='График принадлежности')
    function_name = models.CharField(max_length=50, verbose_name='Название функции')
    a = models.PositiveSmallIntegerField()
    b = models.PositiveSmallIntegerField()
    c = models.PositiveSmallIntegerField()
    d = models.PositiveSmallIntegerField()
