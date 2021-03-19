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
    title = soup.find('h1')
    tom = soup.findAll('td')


#universal_product_code = soup.find("upc")
#product_page_url = soup.find


    print(title.text)
    print(tom)


