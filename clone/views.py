import requests
import re
from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime
from bs4 import BeautifulSoup
from .models import News




def search_news(request, all_news):
    search_text = request.GET['q']
    result_news = []
    for news in all_news:
        if re.search(search_text, news.article) is not None:
            result_news.append(news)
    return result_news


def show_all_news(request):
    all_news = News.objects.all().order_by('-created')
    if request.GET:
        if request.GET['q'] != '':
            if search_news(request, all_news):
                all_news = search_news(request, all_news)

    context = {
        "all_news": all_news,
    }
    return render(request, 'clone/home.html', context=context)


def show_news(request, link_id):
    target_news = News.objects.filter(link=link_id).get()
    news_text = target_news.text_news.split('\n')
    context = {
        "news": target_news,
        'news_text': news_text,
    }

    return render(request, "clone/single_news.html", context=context)


def update(request):

    START_URL = 'https://vz.ru'
    attr = {
        'class': 'fixed_wrap2'
    }
    content_tags = ['p']

    def search_content_block(response):
        soup_news = BeautifulSoup(response, 'html.parser')
        content = soup_news.find('div', attrs=attr)
        return content

    def get_text(url):
            response = requests.get(url).text
            content_soup = search_content_block(response)
            image_url = content_soup.find_all(['img'])[0]['src']
            content = content_soup.find_all(content_tags)
            wrapper_text = ''
            for p in content:
                if p.text != '':
                    wrapper_text += ''.join(p.text) + "\n\n"


            return wrapper_text, image_url

    response = requests.get(START_URL).text
    content = search_content_block(response)
    news = content.find_all(['h1', 'h4'])
    for new in news:
        try:
            new_url = new.find('a')['href']
            new_url_mod = re.search('\/\w+[\/\d]+\.html', new_url)

            if not News.objects.filter(link=new_url_mod.group(0)[-12:-5]).exists():
                wrapper_text, image_url = get_text(START_URL + new_url_mod.group(0))
                with open('clone/static/media/article/' + image_url[-12:], 'wb') as image:
                    res_image = requests.get(image_url)
                    image.write(res_image.content)
                News.objects.update_or_create(article=new.text.strip(),
                                    text_news=wrapper_text,
                                    descriptions=wrapper_text[:200] + '...',
                                    link=new_url_mod.group(0)[-12:-5],
                                    image=image_url[-12:],
                                    created=datetime.now())
        except:
            pass

    return redirect("Home")
