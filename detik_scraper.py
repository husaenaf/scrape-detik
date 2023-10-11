import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
import mysql.connector

html_doc = requests.get('https://www.detik.com/terpopuler')
soup = BeautifulSoup(html_doc.text, 'html.parser')
populer_area = soup.find('div', 'grid-row list-content')
content = populer_area.findAll('div', 'media media--left media--image-radius block-link')

total_data = 0

# saving data to csv part 1
file = open('csvresult.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)
headers = ['title', 'category', 'link', 'link image', 'date_news', 'author_clean']
writer.writerow(headers)

# saving data to mysql part 1
cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='detik')
cursor = cnx.cursor()
output_list = []

for item in content:
    title = item.find('span').find('img')['title']
    category = item.find('div', 'media__date').text
    clean_category = category.split('|')[0]
    link = item.find('a')['href']
    link_image = item.find('span').find('img')['src']

    # Mulai Mengakses tautan artikel di setiap link / deep tautan
    enter_html_doc = requests.get(link)
    enter_soup = BeautifulSoup(enter_html_doc.text, 'html.parser')
    # mengapa tidak cukup dengan kode samping ini saja? date_news = enter_soup.find('div', 'detail__date').text
    # karena akan menghasilkan output == Rabu, 11 Okt 2023 08:20 WIB, tetapi juga ada error setelah output ini yaitu
    # AttributeError: 'NoneType' object has no attribute 'text'....... maka harus diberi if else seperti dibawah ini
    # ini karena di tampilan web memang tidak mencantumkan sehingga output error dan ditangani dengan if else
    date_element = enter_soup.find('div', 'detail__date')
    if date_element:
        date_news = date_element.text
    else:
        date_news = "no date"

    author = enter_soup.find('div', class_='detail__author')
    if author:
        author_clean = author.text.split('-')[0].strip()
    else:
        author_clean = "no author"


    # change data to type data list / json
    item_data = {
        'title': title,
        'clean_category': clean_category,
        'link': link,
        'link_image': link_image,
        'date_news': date_news,
        'author_clean': author_clean
    }
    output_list.append(item_data)

    # saving data to mysql part 2
    add_data = (
        "INSERT INTO popular (title, clean_category, link, link_image, date_news, author_clean) VALUES (%(title)s, %(clean_category)s, %(link)s, %(link_image)s, %(date_news)s, %(author_clean)s )")
    cursor.execute(add_data, item_data)
    cnx.commit()

    # cont total data scraping part 1
    total_data += 1

    # saving image to gallery with replace some title
    title = title.replace(':', '=').replace('/', '_').replace('?', '')
    with open('gallery/' + title + '.jpg', 'wb') as f:
        img = requests.get(link_image)
        f.write(img.content)

    # saving data to csv part 2
    writer.writerow([title, clean_category, link, link_image, date_news, author_clean])

    # print item in terminal
    print('\n'+title)
    print(clean_category)
    print(link)
    print(link_image)
    print(date_news)
    print(author_clean)
    print("================")

file.close()


# dataframe view from file csv with pandas
# pd.set_option('display.max_columns', None)  # hanya untuk menampilkan semua kolom (opsional)
df = pd.read_csv('csvresult.csv')
print(df)


# cont total data scraping part 2
print(f'\nTotal data yang di-generate : {total_data}')