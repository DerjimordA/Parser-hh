from django import forms
import requests

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Запрос для поиска', max_length=100)
    response = requests.get('https://api.hh.ru/areas')
    regions = [(i['id'], i['name']) for i in response.json()]

    region = forms.ChoiceField(choices=regions, label='Регион')

    min_salary = forms.IntegerField(label='Минимальная зарплата', required=False)

    EMPLOYMENT_TYPES = [
        ('full', 'Полная занятость'),
        ('part', 'Частичная занятость'),
        ('project', 'Проектная работа'),
        ('volunteer', 'Волонтерство'),
        ('probation', 'Стажировка'),
    ]

    employment_type = forms.ChoiceField(choices=EMPLOYMENT_TYPES, label='Вид занятости', required=False)

    EXPERIENCE_TYPES = [
        ('noExperience', 'Нет опыта'),
        ('between1And3', 'От 1 до 3 лет'),
        ('between3And6', 'От 3 до 6 лет'),
        ('moreThan6', 'Больше 6 лет'),
    ]

    experience = forms.ChoiceField(choices=EXPERIENCE_TYPES, label='Опыт работы', required=False)

class CollectVacanciesForm(forms.Form):
    search_query = forms.CharField(label='Поисковый запрос', max_length=100)
    page = forms.IntegerField(label='Номер страницы', min_value=1)
    min_salary = forms.IntegerField(label='Минимальная зарплата', required=False)

    EMPLOYMENT_TYPES = [
        ('full', 'Полная занятость'),
        ('part', 'Частичная занятость'),
        ('project', 'Проектная работа'),
        ('volunteer', 'Волонтерство'),
        ('probation', 'Стажировка'),
    ]

    employment_type = forms.ChoiceField(choices=EMPLOYMENT_TYPES, label='Вид занятости', required=False)

    EXPERIENCE_TYPES = [
        ('noExperience', 'Нет опыта'),
        ('between1And3', 'От 1 до 3 лет'),
        ('between3And6', 'От 3 до 6 лет'),
        ('moreThan6', 'Больше 6 лет'),
    ]

    experience = forms.ChoiceField(choices=EXPERIENCE_TYPES, label='Опыт работы', required=False)
    WORK_SCHEDULES = [
        ('fullDay', 'Полный день'),
        ('shift', 'Сменный график'),
        ('flexible', 'Гибкий график'),
        ('remote', 'Удаленная работа'),
        ('flyInFlyOut', 'Вахтовый метод'),
        ('shiftMethod', 'Метод сменности'),
        ('freeDay', 'График с выходными днями'),
        ('other', 'Другой график'),
    ]

    work_schedule = forms.ChoiceField(choices=WORK_SCHEDULES, label='График работы', required=False)

class VacancyFilterForm(forms.Form):
    search_query = forms.CharField(max_length=200, required=False, label="Название")
    min_salary = forms.IntegerField(required=False, label="Минимальная зарплата")
    EMPLOYMENT_TYPES = [
        ('', '---------'),
        ('Полная занятость', 'Полная занятость'),
        ('Частичная занятость', 'Частичная занятость'),
        ('Проектная работа', 'Проектная работа'),
        ('Волонтерство', 'Волонтерство'),
        ('Стажировка', 'Стажировка'),
    ]

    employment_type = forms.ChoiceField(choices=EMPLOYMENT_TYPES, label='Вид занятости', required=False)
    EXPERIENCE_TYPES = [
        ('', '---------'),
        ('Нет опыта', 'Нет опыта'),
        ('От 1 года до 3 лет', 'От 1 года до 3 лет'),
        ('От 3 до 6 лет', 'От 3 до 6 лет'),
        ('Больше 6 лет', 'Больше 6 лет'),
    ]

    experience = forms.ChoiceField(choices=EXPERIENCE_TYPES, label='Опыт работы', required=False)
    WORK_SCHEDULES = [
        ('', '---------'),
        ('Полный день', 'Полный день'),
        ('Сменный график', 'Сменный график'),
        ('Гибкий график', 'Гибкий график'),
        ('Удаленная работа', 'Удаленная работа'),
        ('Вахтовый метод', 'Вахтовый метод'),
        ('Метод сменности', 'Метод сменности'),
        ('График с выходными днями', 'График с выходными днями'),
        ('Другой график', 'Другой график'),
    ]

    work_schedule = forms.ChoiceField(choices=WORK_SCHEDULES, label='График работы', required=False)
    skills = forms.CharField(max_length=200, required=False, label="Навыки")

    SALARY_CHOICES = [
        ('from', 'Минимальная зарплата'),
        ('to', 'Максимальная зарплата'),
    ]
    salary_choice = forms.ChoiceField(choices=SALARY_CHOICES, label='Анализ зарплаты по:', required=False)





