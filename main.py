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

#extraction en itérant sur l'ensemble des pages de la catégorie

    next_page = soup.find('li', class_='next')
    while next_page:
        if 'index.html' in url:
            url = url.replace('index.html', next_page.find('a')['href'])
        elif 'page-' in url:
            url = url[:-6].replace('page', next_page.find('a')['href'])
        if url[-1] == "-":
            url = url[:len(url) - 1]

        response = requests.get(url)
        soup = BeautifulSoup(response.content.decode("utf-8", 'ignore'), features='html.parser')
        next_pages = ['https://books.toscrape.com/catalogue/' + book.find('a', href=True)['href'][9:] for book in
                      soup.find_all('div', class_='image_container')]
        for pages in next_pages:
            list_books.append(pages)
            next_page = soup.find('li', class_='next')

            print(list_books)


#extraction des éléments d'un livre

for url in list_books:
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), features='html.parser')

        upc = soup.tr.td.text
        title = soup.find('h1').text
        infos = soup.findAll('td')
        price_excluding_tax = infos[2].text[1:]
        price_including_tax = infos[3].text[1:]
        number_available = infos[5].text
        product_description = soup.find_all('p')
        product_description = product_description[3].text
        category = soup.ul.find_all('li')
        category = category[2].text.strip()
        review_rating = soup.find('p', class_='star-rating')['class'][1]
        image_url = 'https://books.toscrape.com/' + soup.img['src'].replace('..', (''))

        info_list = [image_url, category, title, upc, price_excluding_tax, price_including_tax, number_available,
                     product_description, review_rating]

        print(info_list)


df = pandas.DataFrame([info_list], columns=['image_url', 'category', 'title', 'upc', 'price_excluding_tax', 'price_including_tax', 'number_available', 'product_description', 'review_rating'])

df.to_csv('résultats.csv', index=False, sep=';')


