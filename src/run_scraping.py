# import codecs
import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraping_service.settings')

from django.contrib.auth import get_user_model
from django.db import DatabaseError
import django
django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()

parsers = (
    (superjob, 'superjob'),
    (rabota, 'rabota'),
)


def get_settings():
    qs = User.objects.filter(is_send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dict[pair]
        urls.append(tmp)
    return urls


settings = get_settings()
url_list = get_urls(settings)


# city = City.objects.filter(slug='spb').first()
# language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for data in url_list:
    for func, key in parsers:
        url = data['url_data'][key]
        job, error = func(url, city=data['city'], language=data['language'])
        jobs += job
        errors += error

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()

# h = codecs.open('work.json', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()

