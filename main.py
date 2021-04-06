import requests
from bs4 import BeautifulSoup
import pandas
from urllib.request import urlretrieve
import os

# extraction des urls des différentes catégories sur la page principale
list_categories = []
url = 'http://books.toscrape.com/index.html'
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.content, features='html.parser')
    containers = soup.find(class_='nav nav-list').find_all('a')[1:]
    for container in containers:
        list_categories.append('https://books.toscrape.com/' + container['href'])

# extraction des urls pour les livres d'1 catégorie sur la première page
all_books = []
for url in list_categories:
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, features='html.parser')
        containers = soup.find_all('article', class_='product_pod')
        for container in containers:
            all_books.append('https://books.toscrape.com/catalogue/' + container.find('a', href=True)['href'][9:])

        # extraction en itérant sur l'ensemble des pages de la catégorie
        next_page = soup.find('li', class_='next')
        while next_page:
            if 'index.html' in url:
                url = url.replace('index.html', next_page.find('a')['href'])
            elif 'page-' in url:
                url = url[:-6].replace('page', next_page.find('a')['href'])
            if url[-1] == "-":
                url = url[:len(url) - 1]
            else:
                pass

            response = requests.get(url)
            soup = BeautifulSoup(response.content, features='html.parser')
            next_pages = ['https://books.toscrape.com/catalogue/' + book.find('a', href=True)['href'][9:] for book in
                          soup.find_all('div', class_='image_container')]
            for pages in next_pages:
                all_books.append(pages)
                next_page = soup.find('li', class_='next')

# extraction des éléments de chacun des livres de la catégorie et alimentation du dictionnaire afin de créer la base
# de données pour export csv
product_page_urls = []
upcs = []
titles = []
prices_excluding_tax = []
prices_including_tax = []
numbers_available = []
product_descriptions = []
categories = []
reviews_rating = []
images = []

for url in all_books:
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, features='html.parser')
        product_page_urls.append(url)
        upcs.append(soup.tr.td.text)
        titles.append(soup.find('h1').text)
        infos = soup.findAll('td')
        prices_excluding_tax.append(infos[2].text)
        prices_including_tax.append(infos[3].text)
        numbers_available.append(infos[5].text)
        product_descriptions.append(soup.find_all('p')[3].text)
        category = soup.ul.find_all('li')
        category = category[2].text.strip()
        categories.append(category)
        reviews_rating.append(soup.find('p', class_='star-rating')['class'][1])
        images.append('https://books.toscrape.com/' + soup.img['src'].replace('..', ''))

data_to_extract = {'Category': categories, 'Universal Product Code': upcs, 'Title': titles,
                   'Product Page Url': product_page_urls, 'Product Description': product_descriptions,
                   'Price Excluding Tax': prices_excluding_tax, 'Price Including Tax': prices_including_tax,
                   'Review Rating': reviews_rating, 'Number Available': numbers_available, 'Image Url': images}

# création de la DataFrame et export des données splittées par catégorie
os.mkdir('./Données extraites/')
path = './Données extraites/'
df = pandas.DataFrame(data=data_to_extract)
df_by_cat = df.groupby('Category')
for (category, category_df) in df_by_cat:
    filename = category + ".csv"
    category_df.to_csv(path + filename, index=False,  sep=';', encoding='utf-8-sig')

# téléchargement des images dans un dossier
os.mkdir('./Couvertures/')
for url in images:
    urlretrieve(url, './Couvertures/' + os.path.basename(url))
