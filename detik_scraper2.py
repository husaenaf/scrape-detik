import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
import mysql.connector

def fetch_detik_populer():
    html_doc = requests.get('https://www.detik.com/terpopuler')
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    populer_area = soup.find('div', 'grid-row list-content')
    content = populer_area.findAll('div', 'media media--left media--image-radius block-link')
    return content      # artinya semua nilai di fetch_detik_populer disimpan di variable content

def save_to_csv(data):
    total_data = 0
    file = open('csvresult2.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(file)
    headers = ['title', 'category', 'link', 'link image']
    writer.writerow(headers)

    for item in data:
        title = item.find('span').find('img')['title']
        category = item.find('div', 'media__date').text
        clean_category = category.split('|')[0]
        link = item.find('a')['href']
        link_image = item.find('span').find('img')['src']

        item_data = {
            'title': title,
            'clean_category': clean_category,
            'link': link,
            'link_image': link_image
        }

        total_data += 1

        writer.writerow([title, clean_category, link, link_image])

        # print item in terminal
        print('\n' + title)
        print(clean_category)
        print(link)
        print(link_image)
        print("================")

    file.close()
    return total_data  # Mengembalikan total_data

def save_to_mysql(data):
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='detik')
    cursor = cnx.cursor()

    for item in data:
        title = item.find('span').find('img')['title']
        category = item.find('div', 'media__date').text
        clean_category = category.split('|')[0]
        link = item.find('a')['href']
        link_image = item.find('span').find('img')['src']

        item_data = {
            'title': title,
            'clean_category': clean_category,
            'link': link,
            'link_image': link_image
        }

        add_data = ("INSERT INTO popular (title, clean_category, link, link_image) VALUES (%(title)s, %(clean_category)s, %(link)s, %(link_image)s )")
        cursor.execute(add_data, item_data)
        cnx.commit()

    cursor.close()
    cnx.close()

def save_images(data):
    for item in data:
        title = item.find('span').find('img')['title']
        link_image = item.find('span').find('img')['src']

        title = title.replace(':', '=').replace('/', '_').replace('?', '')
        with open('gallery/' + title + '.jpg', 'wb') as f:
            img = requests.get(link_image)
            f.write(img.content)

def dataframe():
    df = pd.read_csv('csvresult2.csv')
    print(df)

def main():
    content = fetch_detik_populer()
    total_data = save_to_csv(content)  # Mengambil nilai total_data dari save_to_csv
    save_to_mysql(content)
    save_images(content)
    dataframe()
    print(f'\nTotal data yang di-generate : {total_data}')

if __name__ == "__main__":
    main()
