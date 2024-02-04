import requests
import codecs
from bs4 import BeautifulSoup as BS


# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
#            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

__all__ = ('superjob', 'rabota')


def superjob(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.superjob.ru'
    if url:
        response = requests.get(url=url)
        if response.status_code == 200:
            soup = BS(response.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': '_3VMkc _3JfmZ UnlTV _3jfFx _3nFmX'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': '_1MxfQ _2ZP2D'})
                for div in div_list:
                    title = div.find('span', attrs={'class': '_1gB-h _39bKX _1MEwQ _3t5Je _3TptJ _2C8nO _2KJeO _2L4SY'})
                    href = title.a['href']
                    content = div.find('span', attrs={'class': '_10jsR _2C8nO _2KJeO _3B9u2 _3nGEP'})
                    company = div.find('span', attrs={
                        'class': '_3nMqD f-test-text-vacancy-item-company-name _1trBE _2C8nO _2KJeO _3B9u2 _3nGEP'})
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content.text, 'company': company.text,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page not response'})
        return jobs, errors


def rabota(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://spb.rabota.ru'
    if url:
        response = requests.get(url=url)
        if response.status_code == 200:
            soup = BS(response.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'r-serp'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'r-serp__item r-serp__item_vacancy'})
                for div in div_list:
                    title = div.find('h3', attrs={'vacancy-preview-card__title'})
                    href = title.a['href']
                    description = div.find('div', attrs={'class': 'vacancy-preview-card__short-description'})
                    company = div.find('span', attrs={'class': 'vacancy-preview-card__company-name'})
                    jobs.append({'title': title.text.replace('  ', ''), 'url': domain + href,
                                 'description': description.text, 'company': company.text.replace('  ', ''),
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page not response'})
        return jobs, errors


if __name__ == '__main__':
    url = 'https://spb.superjob.ru/vacancy/search/?keywords=python'
    jobs, errors = superjob(url)
    h = codecs.open('work2.json', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
