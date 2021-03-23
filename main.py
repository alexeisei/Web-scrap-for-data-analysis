import requests
from bs4 import BeautifulSoup
import csv
import pandas

#extraction des urls pour les livres d'1 catégorie

url_cat = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
response = requests.get(url_cat)
if response.ok:
    soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")

    books_links = []
    containers = soup.find_all('div', class_='image_container')
    for container in containers:
        links = container.find('a', href=True)['href'][9:]
        books_links.append('https://books.toscrape.com/catalogue/' + links)
        print(books_links)



#extraction des éléments d'un livre

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.text, features="html.parser")

    upc = soup.tr.td.text
    #upc2 = soup.th.next_sibling.text
    title = soup.find('h1').text
    infos = soup.findAll('td')
    price_excluding_tax = infos[2].text
    price_including_tax = infos[3].text
    number_available = infos[5].text
    product_description = soup.find('meta', {'name': 'description'})['content'].strip()
    cat = soup.ul.findAll('li')
    category = cat[2].text.strip()
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = 'https://books.toscrape.com/' + soup.img['src'].replace('..', (''))

    info_list = [upc, title, price_excluding_tax, price_including_tax, number_available, product_description, category, review_rating, image_url]

    df = pandas.DataFrame([info_list], columns=['upc', 'title', 'price_excluding_tax', 'price_including_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

    df.to_csv('résultats.csv', index=False, sep=';')



""""  
    print(upc)
    print(title.text)
    print(price_excluding_tax)
    print(price_including_tax)
    print(number_available)
    print(product_description)
    print(category)
    print(review_rating)
    print(image_url)
"""
