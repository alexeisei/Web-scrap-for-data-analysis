# importation des modules et des paquets
import requests
from bs4 import BeautifulSoup

#envoyer une requête à l'URL choisie via requests
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

 #création de la variable "response"
response = requests.get(url)

 #si la requête = ok (200), création de "soup" et recherche de title dedans, puis afficher le résultat en .txt
if response.ok:
    soup = BeautifulSoup(response.text, features="html.parser")


    upc = soup.tr.td.text
    #upc2 = soup.th.next_sibling.text
    title = soup.find('h1')
    infos = soup.findAll('td')
    price_excluding_tax = infos[2].text
    price_including_tax = infos[3].text
    number_available = infos[5].text
    # product_description = soup.find(id="content_inner")
    cat = soup.ul.findAll('li')
    category = cat[2].text.strip()
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = soup.img['src'].replace('..', '')



    print(upc)
    print(title.text)
    print(price_excluding_tax)
    print(price_including_tax)
    print(number_available)
    #print(product_description)
    print(category)
    print(review_rating)
    print(image_url)
