import re

import requests
from bs4 import BeautifulSoup
file_url = r'C:\Users\483\Desktop\Русик файлы\Реализм , мистика детективы last'
page=2
num=0
for_reit=''
post_link='https://fantlab.ru/login'
data = {
    'login': 'sidbarret',
    'password': '****'
}

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36}"
}

sess = requests.Session()
req = sess.post(post_link, headers=headers , data=data)
for ggg in range(1, 469):
    page = ggg
    url = f'https://fantlab.ru/bygenre?form=&lang=rus&logicalor=on&sort=marks&wg160=on&wg225=on&wg30=on&wg31=on&wg34=on&wg35=on&wg37=on'
    reg = sess.get(url)

    with open(f"{file_url}\{page}.html", "w", encoding='utf-8') as file:
        file.write(reg.text)
        file.close()

    with open(f"{file_url}\{page}.html", encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    numbooks = 0
    # bl=['Дж. Р. Р. Толкин','Дж. К. Роулинг' , 'Анджей Сапковский','Дэн Симмонс']
    num = 0
    links = []

    # try:
    #     book_titles_hrefs = soup.find('tbody').find_all('a')
    #     print(book_titles_hrefs)
    # except:
    book_titles_hrefs = soup.find_all('a', href=re.compile("/work"))

    for i in book_titles_hrefs:  # все теги html
        # for ii in bl:
        #     if ii in i.text:
        #         break
        # else:
        if i.text[0] == '«':
            link_href = i.get("href")

            if link_href[0] == '/':
                link_href = 'https://fantlab.ru/' + link_href

            links.append(link_href)

    for i in links:  # обращение к каждой конкретной странице
        for aaa in i:
            if aaa.isdigit():
                for_reit += aaa
        response = requests.get(i, headers=headers)
        # print(response.status_code)
        soup2 = BeautifulSoup(response.text, "lxml")
        try:
            genre = soup2.find('div', id='workclassif').find('li').find('a')
        except:
            for_reit = ''
            continue
        num += 1
        print(f'{num}. {genre.text}')
        # if genre=='None':
        # except:
        #     genre = soup2.find('a', title='Показать все книги с такой меткой')
        if genre.text =='Фантастика' or genre.text == 'Фэнтези' or genre.text[:6] == 'Сказка' or genre=='None' or genre=='':
            for_reit = ''
            continue
        else:

            author = soup2.find('a', itemprop='author')
            title = soup2.find('span', itemprop='name')
            rating = soup2.find('span', id=f'm_m_{for_reit}')
            if rating.text=='?':
                for_reit=''
                continue
            rating = float(rating.text)
            readers = soup2.find('span', id=f'm_c_{for_reit}')
            for_reit = ''
            if author.text == 'фантЛабораторная работа' or author.text == 'Макс Фрай' or author.text == 'Мария Семёнова' or rating < 7.49 or author.text == 'Борис Акунин':
                continue
            else:
                numbooks += 1
                endname = f'{author.text} - {title.text}.  {rating} ({readers.text})'
                print(endname)
                my_file = open(f'{file_url}\_realistic_russian', 'a', encoding='utf-8')
                my_file.write(endname + '\n')
                my_file.close()




