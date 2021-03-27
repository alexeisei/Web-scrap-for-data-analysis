import requests
from bs4 import BeautifulSoup
import pandas

#extraction des urls pour les livres d'1 catégorie sur première page

url = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")

    list_books = []

    containers = soup.find_all('article', class_='product_pod')
    for container in containers:
        list_books.append('https://books.toscrape.com/catalogue/' + container.find('a', href=True)['href'][9:])

#extraction des urls en itérant sur l'ensemble des pages de la catégorie

    i = 2
    next_page = url.replace('index', 'page-2')
    while requests.get(next_page).ok:

        response = requests.get(next_page)
        soup = BeautifulSoup(response.content, features="html.parser")

        for product_pod in soup.find_all('article', class_='product_pod'):
            list_books.append('https://books.toscrape.com/catalogue/' + container.find('a', href=True)['href'][9:])

        i += 1
        page = "page-" + str(i)
        next_page = url.replace('index', page)

print(len(list_books))


"""
#extraction des éléments d'un livre

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), features="html.parser")

    upc = soup.tr.td.text
    #upc2 = soup.th.next_sibling.text
    title = soup.find('h1').text
    infos = soup.findAll('td')
    price_excluding_tax = infos[2].text[1:]
    price_including_tax = infos[3].text[1:]
    number_available = infos[5].text
    product_description = soup.find('meta', {'name': 'description'})['content'].strip()
    cat = soup.ul.findAll('li')
    category = cat[2].text.strip()
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = 'https://books.toscrape.com/' + soup.img['src'].replace('..', (''))

    info_list = [upc, title, price_excluding_tax, price_including_tax, number_available, product_description, category, review_rating, image_url]

    df = pandas.DataFrame([info_list], columns=['upc', 'title', 'price_excluding_tax', 'price_including_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

    df.to_csv('résultats.csv', index=False, sep=';')
"""
