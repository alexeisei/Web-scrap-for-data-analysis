import requests
from bs4 import BeautifulSoup
import pandas
from urllib.request import urlretrieve
import os

#Extraction des urls des différentes catégories sur la page principale
url = 'http://books.toscrape.com/index.html'
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), features='html.parser')
    list_categories = []
    containers = soup.find(class_='nav nav-list').find_all('a')[1:]
    for container in containers:
        link_to_extract = container['href'][0:51]
        cat_link = 'https://books.toscrape.com/' + link_to_extract
        list_categories.append(cat_link)
    print(len(list_categories))
    print(list_categories)

#extraction des urls pour les livres d'1 catégorie sur première page

url = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")
    list_books = []
    containers = soup.find_all('article', class_='product_pod')
    for container in containers:
        list_books.append('https://books.toscrape.com/catalogue/' + container.find('a', href=True)['href'][9:])

#extraction en itérant sur l'ensemble des pages de la catégorie
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
        soup = BeautifulSoup(response.content.decode("utf-8", 'ignore'), features='html.parser')
        next_pages = ['https://books.toscrape.com/catalogue/' + book.find('a', href=True)['href'][9:] for book in
                      soup.find_all('div', class_='image_container')]
        for pages in next_pages:
            list_books.append(pages)
            next_page = soup.find('li', class_='next')

#contrôle des urls récupérées
print(len(list_books))
print(list_books)


#extraction des éléments de chacun des livres de la catégorie et alimentation des listes afin de créer la base de données pour export csv

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

for url in list_books:
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), features='html.parser')

        product_page_url = str(url)
        product_page_urls.append(product_page_url)
        print(product_page_url)

        upc = soup.tr.td.text
        upcs.append(upc)

        title = soup.find('h1').text
        titles.append(title)

        infos = soup.findAll('td')

        price_excluding_tax = infos[2].text[1:]
        prices_excluding_tax.append(price_excluding_tax)

        price_including_tax = infos[3].text[1:]
        prices_including_tax.append(price_including_tax)

        number_available = infos[5].text
        numbers_available.append(number_available)

        product_description = soup.find_all('p')
        product_description = product_description[3].text
        product_descriptions.append(product_description)

        category = soup.ul.find_all('li')
        category = category[2].text.strip()
        categories.append(category)

        review_rating = soup.find('p', class_='star-rating')['class'][1]
        reviews_rating.append(review_rating)

        image_url = 'https://books.toscrape.com/' + soup.img['src'].replace('..', (''))
        images.append(image_url)

        data_to_extract = {
            'Category': categories,
            'Universal Product Code': upcs,
            'Title': titles,
            'Product Page Url': product_page_urls,
            'Product Description': product_descriptions,
            'Price Excluding Tax': prices_excluding_tax,
            'Price Including Tax': prices_including_tax,
            'Review Rating': reviews_rating,
            'Number Available': numbers_available,
            'Image Url': images
        }
        
#Création de la DataFrame Pandas et export du fichier avec les résultats

df = pandas.DataFrame(data=data_to_extract)
df.to_csv('Résultats.csv', index=False, sep=';')


#téléchargement des images dans un dossier

os.mkdir('./Couvertures/')

for url in images:
    urlretrieve(url, './Couvertures/' + os.path.basename(url))

