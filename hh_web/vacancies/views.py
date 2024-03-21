from .forms import SearchForm
from .models import Vacancy, Region
import requests
from collections import Counter
from django.shortcuts import render, redirect
from .forms import CollectVacanciesForm, VacancyFilterForm
from plotly.offline import plot
import plotly.graph_objs as go


def analyze_skills(vacancies):
    all_skills = []
    for vacancy in vacancies:
        all_skills.extend(vacancy['skills'])

    skill_counts = Counter(all_skills)
    skill_counts_sorted = dict(sorted(skill_counts.items(), key=lambda item: item[1], reverse=True))
    return skill_counts_sorted

def skills_analysis_view(request):
    vacancies = Vacancy.objects.all()
    all_skills = [skill for vacancy in vacancies for skill in vacancy.skills]
    skill_counts = Counter(all_skills)
    skill_counts_sorted = dict(sorted(skill_counts.items(), key=lambda item: item[1], reverse=True))

    skills_analysis = skill_counts_sorted
    return render(request, 'vacancies/database.html', {'skills_analysis': skills_analysis})

def parse_vacancy_skills(vacancy_url):
    response = requests.get(vacancy_url)
    data = response.json()

    if 'errors' in data:
        for error in data['errors']:
            if error['value'] == 'captcha_required':
                return redirect(error['captcha_url'+ '&backurl=' + 'http://127.0.0.1:8000/'])  # redirect to captcha page

    vacancy_skills = []

    if 'key_skills' in data:
        for skill in data['key_skills']:
            vacancy_skills.append(skill['name'])

    return vacancy_skills

def parse_vacancy_work_schedule(vacancy_url):
    response = requests.get(vacancy_url)
    data = response.json()

    if 'errors' in data:
        for error in data['errors']:
            if error['value'] == 'captcha_required':
                return redirect(error['captcha_url'+ '&backurl=' + 'http://127.0.0.1:8000/'])  # redirect to captcha page

    if 'schedule' in data:
        return data['schedule']['name']
    else:
        return None


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            region = form.cleaned_data['region']
            min_salary = form.cleaned_data['min_salary']
            employment_type = form.cleaned_data['employment_type']
            experience = form.cleaned_data['experience']

            api_url = 'https://api.hh.ru/vacancies'
            params = {
                'text': search_query,
                'per_page': 100,
                'area': region,
                'salary': min_salary,
                'employment': employment_type,
                'experience': experience,
            }

            response = requests.get(api_url, params=params)
            data = response.json()

            vacancies = []
            for item in data['items']:
                vacancy_id = item['id']
                vacancy_name = item['name']
                vacancy_salary = item['salary']
                vacancy_url = item['url']
                vacancy_skills = parse_vacancy_skills(vacancy_url)
                print(vacancy_url)
                vacancy_experience = item['experience'][
                    'name'] if 'experience' in item else 'Not specified'  # added line

                vacancy_url = item['url'].replace('api.hh.ru/vacancies', 'hh.ru/vacancy')

                vacancies.append({
                    'id': vacancy_id,
                    'name': vacancy_name,
                    'salary': vacancy_salary,
                    'url': vacancy_url,
                    'skills': vacancy_skills,
                    'experience': vacancy_experience,
                })
            skill_counts = analyze_skills(vacancies)

            return render(request, 'vacancies/results.html', {'vacancies': vacancies, 'skill_counts': skill_counts})
    else:
        form = SearchForm()

    return render(request, 'vacancies/search.html', {'form': form})

def home(request):
    return render(request, 'vacancies/home.html')

def collect_regions():
    api_url = 'https://api.hh.ru/areas'  # Предполагаемый URL для получения регионов

    response = requests.get(api_url)
    data = response.json()

    def save_region(region_data, parent=None):
        region_id = region_data['id']
        region_name = region_data['name']
        region, created = Region.objects.update_or_create(
            id=region_id,
            defaults={
                'name': region_name,
                'parent': parent,
            }
        )

        for subregion_data in region_data['areas']:
            save_region(subregion_data, parent=region)

    for country_data in data:
        save_region(country_data)



def database_view(request):
    form = CollectVacanciesForm()
    filter_form = VacancyFilterForm()
    vacancies = Vacancy.objects.all()

    skills_list = [skill for vacancy in vacancies for skill in vacancy.skills]
    skills_counter = Counter(skills_list)
    most_common_skills = skills_counter.most_common()

    salaries = [vacancy.salary['from'] for vacancy in Vacancy.objects.all() if
                vacancy.salary and 'from' in vacancy.salary and vacancy.salary['from'] is not None]
    salaries.sort()
    salary_counts = Counter(salaries)

    data = go.Histogram(
        x=salaries,
        nbinsx=20,
        xbins=dict(start=0, end=500000, size=25000),
    )

    layout = go.Layout(
        bargap=0.1,  # зазор между барами
    )

    fig = go.Figure(data=data, layout=layout)

    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    context = {
        'form': form,
        'filter_form': filter_form,
        'vacancies': vacancies,
        'most_common_skills': most_common_skills,
        'plot_div': plot_div,
    }
    return render(request, 'vacancies/database.html', context, )

def collect_vacancies(request):
    if request.method == 'POST':
        form = CollectVacanciesForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            page = form.cleaned_data['page']
            min_salary = form.cleaned_data['min_salary']
            employment_type = form.cleaned_data['employment_type']
            experience = form.cleaned_data['experience']
            work_schedule = form.cleaned_data['work_schedule']

            api_url = 'https://api.hh.ru/vacancies'
            params = {
                'text': search_query,  # Текстовый запрос
                'page': page,  # Номер страницы
                'per_page': 50,  # Количество вакансий на странице
                'area': 1,
                'salary': min_salary,
                'employment': employment_type,
                'experience': experience,
                'schedule': work_schedule,
            }

            response = requests.get(api_url, params=params)
            data = response.json()

            for item in data['items']:
                vacancy_id = item['id']
                vacancy_name = item['name']
                vacancy_salary = item['salary']
                vacancy_url = item['url']
                vacancy_skills = parse_vacancy_skills(vacancy_url)
                vacancy_experience = item['experience']['name'] if 'experience' in item else 'Not specified'
                vacancy_employment_type = item['employment']['name'] if 'employment' in item else 'Not specified'
                vacancy_work_schedule = parse_vacancy_work_schedule(vacancy_url)
                vacancy_url = item['url'].replace('api.hh.ru/vacancies', 'hh.ru/vacancy')

                # Обновление или создание вакансии
                Vacancy.objects.update_or_create(
                    id=vacancy_id,
                    defaults={
                        'name': vacancy_name,
                        'salary': vacancy_salary,
                        'url': vacancy_url,
                        'skills': vacancy_skills,
                        'experience': vacancy_experience,
                        'employment_type': vacancy_employment_type,
                        'work_schedule': vacancy_work_schedule,
                    }
                )

        return redirect('database')  # перенаправление на страницу базы данных после заполнения
    else:
        form = CollectVacanciesForm()

    return render(request, 'vacancies/database.html', {'form': form})

def filter_vacancies(request):
    if request.method == 'POST':
        filter_form = VacancyFilterForm(request.POST)
        if filter_form.is_valid():
            search_query = filter_form.cleaned_data.get('search_query')
            min_salary = filter_form.cleaned_data.get('min_salary')
            employment_type = filter_form.cleaned_data.get('employment_type')
            experience = filter_form.cleaned_data.get('experience')
            work_schedule = filter_form.cleaned_data.get('work_schedule')
            skills = filter_form.cleaned_data.get('skills')
            salary_choice = filter_form.cleaned_data.get('salary_choice')

            vacancies = Vacancy.objects.all()

            if search_query:
                vacancies = vacancies.filter(name__icontains=search_query)

            if min_salary:
                vacancies = vacancies.filter(salary__from__gte=min_salary)

            if employment_type:
                vacancies = vacancies.filter(employment_type=employment_type)

            if experience:
                vacancies = vacancies.filter(experience=experience)

            if work_schedule:
                vacancies = vacancies.filter(work_schedule=work_schedule)

            if skills:
                for skill in skills.split(','):
                    skill = skill.strip()
                    vacancies = vacancies.filter(skills__icontains=skill)

            skills_list = [skill for vacancy in vacancies for skill in vacancy.skills]
            skills_counter = Counter(skills_list)
            most_common_skills = skills_counter.most_common()


            salaries = [vacancy.salary[salary_choice] for vacancy in vacancies if
                        vacancy.salary and salary_choice in vacancy.salary and vacancy.salary[salary_choice] is not None]
            salaries.sort()
            salary_counts = Counter(salaries)

            data = go.Histogram(
                x=salaries,
                nbinsx=20,
                xbins=dict(start=0, end=500000, size=25000),
            )

            layout = go.Layout(
                bargap=0.1,
            )

            fig = go.Figure(data=data, layout=layout)

            plot_div = plot(fig, output_type='div', include_plotlyjs=False)

            return render(request, 'vacancies/database.html', {'vacancies': vacancies, 'filter_form': filter_form, 'most_common_skills': most_common_skills,
                                                               'plot_div': plot_div,})

    else:
        filter_form = VacancyFilterForm()
        vacancies = Vacancy.objects.all()
        return render(request, 'vacancies/database.html', {'vacancies': vacancies, 'filter_form': filter_form})

















