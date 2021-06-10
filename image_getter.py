import requests
from bs4 import BeautifulSoup

attr = {
    'class': 'fixed_wrap2'
}

response = requests.get('https://vz.ru/world/2020/9/1/1057826.html')
bs = BeautifulSoup(response.text, 'html.parser')
content = bs.find('div', attrs=attr)

all_images = content.find_all(['img'])[0]['src']
print(all_images)

with open('clone/static/media/article/' + all_images[-12:], 'wb') as image:
    res_image = requests.get(all_images)
    image.write(res_image.content)
