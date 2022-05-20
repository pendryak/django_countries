from django.shortcuts import render
import json
from pathlib import Path
from DjangoCountries.settings import BASE_DIR, STATICFILES_DIRS
from django.http import Http404
import string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import operator
from countries.models import Country, Language


person = {'First_name': 'Ольга', 'Last_name': 'Пендрикова',
          'Second_name': 'Николаевна', 'Tel': '8-923-600-01-02',
          'email': 'pendryak@mail.ru', }


def get_countries():
    path = Path(STATICFILES_DIRS[0] / 'country_by_languages.json')
    with open(path) as json_file:
        data = json.load(json_file)
    return data


def index(request):
    result = f'{person["Last_name"]} {person["First_name"][0]}.{person["Second_name"][0]}.'
    context = {'result': result}
    return render(request, 'countries/index.html', context)


def countries_list(request):
    countries = Country.objects.all()
    per_page = 10
    paginator = Paginator(countries, per_page)
    page = request.GET.get('page')
    try:
        countries = paginator.page(page)
    except PageNotAnInteger:
        countries = paginator.page(1)
    except EmptyPage:
        countries = paginator.page(paginator.num_pages)
    context = {'countries': countries, 'page': page, 'alphabet': list(string.ascii_uppercase)}
    return render(request, 'countries/countries_list.html', context)


def country_view(request, c_name):
    country = Country.objects.get(name=c_name)
    context = {'country': country}

    if context:
        return render(request, 'countries/country.html', context)
    else:
        raise Http404(f'Country {c_name} does not exist')


def countries_alpha(request, alpha):
    countries = Country.objects.filter(name__startswith=alpha)
    context = {'countries': countries, 'alpha': alpha}
    return render(request, 'countries/countries_list_alpha.html', context)


def languages_list(request):
    languages = Language.objects.all()
    per_page = 10
    paginator = Paginator(languages, per_page)
    page = request.GET.get('page')
    try:
        languages = paginator.page(page)
    except PageNotAnInteger:
        languages = paginator.page(1)
    except EmptyPage:
        languages = paginator.page(paginator.num_pages)
    context = {'languages': languages, 'page': page}
    return render(request, 'countries/languages_list.html', context)


def countries_lang(request, lang):
    countries = Country.objects.filter(languages__name==lang)
    context = {'countries': countries, 'lang': lang}
    return render(request, 'countries/countries_list_lang.html', context)

