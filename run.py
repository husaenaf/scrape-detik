import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template

app = Flask(__name__)   # pembuatan objek Flask untuk membuat aplikasi web

@app.route('/')     # Ini adalah decorator yang menentukan rute untuk fungsi home().
def home():         # Ketika mengakses rute utama (/), maka fungsi home()  dijalankan & merender template 'base.html'.
    return render_template('base.html')

@app.route('/detik-populer')
def detik_populer():
    html_doc = requests.get('https://www.detik.com/terpopuler')     # Fungsi ini dan setelahnya melakukan scraping data
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    populer_area = soup.find('div', 'grid-row list-content')
    titles = populer_area.findAll('h3', 'media__title')
    images = populer_area.findAll('div', 'media__image')

    # kemudian kode ini untuk merender template 'detik-scraper.html' dengan mengirimkan data gambar dari hasil scraper.
    return render_template('detik-scraper.html', images=images)


@app.route('/idr-rates')
def idr_rates():
    source = requests.get('https://www.floatrates.com/daily/idr.json')      # Fungsi ini mengambil data kurs mata web dalam format JSON
    json_data = source.json()
    return render_template('idr-rates.html', datas=json_data.values())  # kemudian merender template 'idr-rates.html' dengan mengirimkan data JSON tersebut.


# Ini adalah bagian yang menjalankan aplikasi Flask jika file ini dijalankan sebagai program utama.
# Debug mode diaktifkan untuk memudahkan debugging saat pengembangan.
# Jadi, jika Anda menjalankan file ini, aplikasi Flask akan mulai berjalan dan dapat diakses melalui browser Anda.
if __name__ =='__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True, port=5555)