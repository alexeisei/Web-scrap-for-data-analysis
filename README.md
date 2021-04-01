# Web Scraper

P02

Ce projet a pour objectif de créer un programme (web scraper) codé en Python, qui va extraire des données de l'ensemble des livres de chaque catégorie depuis le site http://books.toscrape.com/

Les données extraites pour chacun des livres sont les suivantes :
- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

Les données extraites seront enregistrées dans un fichier .CSV pour chaque catégorie de livres, dans un dossier "Données extraites". Egalement, l'ensemble des images des livres seront extraites dans un dossier "Couvertures".

## Prérequis pour lancer le programme

Quelques étapes sont nécessaires afin de faire fonctionner le scraper :

1) télécharger l'ensemble des fichiers du programme au format ZIP depuis la page principale de ce projet et les extraires sur votre ordinateur (par exemple sur votre Desktop)
2) télécharger la dernière version de Python 3 sur la page https://www.python.org/downloads/
3) se rendre dans le dossier où se trouvent les fichiers du projet et ouvrir le terminal de commande correspondant à votre système d'exploitation
4) créer un environnement virtuel en y tappant les commandes suivante :
```
pip install venv
```
puis :
```
python -m venv env
```
5) activer l'environnement virtuel en tappant :
```
-env\Scripts\activate.bat
```
ou pour Windows :
```
env\Scripts\activate
```
6) importer les modules et paquets nécessaires dans l'environnement virtuel depuis le documents "requirements.txt" en tappant :
```
pip install -r requirements.txt
```

## Pour lancer le programme

Voilà ! Votre environnement virtuel est configuré et prêt à lancer le scraper. 

Pour cela, tapper la commande suivante :
```
python main.py
```

## Les résultats

- patienter un peu, il y a beaucoup de données à récupérer ;)
- un dossier "Données extraites" contenant un fichier CSV par catégorie de livres sera créé dans le dossier du projet (50 fichiers CSV au total)
- un dossier "Couvertures" contenant l'ensemble des images des livres sera créé également (1000 images au total)

## Conclusion

Mon premier programme :)
Merci à mon mentor Mariot pour ses conseils !
