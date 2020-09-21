from bs4 import BeautifulSoup
import requests
import sys
import re
import time
import csv

# todo crawl also for adebooks
# todo context manage for file

# todo da aggiungere scraping for prezzo

file = open('Example', 'a')

def make_soup(self):
    page_link = requests.get(self)
    src = page_link.content
    soup_page = BeautifulSoup(src, 'lxml')
    return soup_page

# def create_soup_file(self):
#     soup_text = make_soup(self)

def search_maremagnum():

    # create link from which to extract individual book pages

    search_terms = input("Che cosa cerchi? ")
    search_terms_maremagnum = search_terms.strip().lower().replace(' ', '+')
    search_link_maremagnum = 'https://www.maremagnum.com/ricerca' \
                             '/risultati?search%5Bkeyword%5D=' + search_terms_maremagnum
    response_maremagnum = requests.get(search_link_maremagnum).text
    soup_maremagnum = BeautifulSoup(response_maremagnum, 'lxml')

    # check if there are too many pages

    number_of_results = int(soup_maremagnum.find('section', id='inside-search').label.span.text)

    if number_of_results < 26:
        pass
    else:
        print('>25 results found. No scraping done. Be more specific.')
        sys.exit()

    # here we find the link to the page of each book present in the search result

    website_maremagnum = 'https://maremagnum.com'
    list_finalpart_bookpage = []
    list_links_bookpage = []

    for book in soup_maremagnum.findAll('li', class_='note', limit=25):
        finalpart_link_bookpage = book.find('a')
        list_finalpart_bookpage.append(finalpart_link_bookpage.attrs['href'])

        link_book_complete = website_maremagnum + finalpart_link_bookpage.attrs['href']
        list_links_bookpage.append(link_book_complete)

    # print(list_links_bookpage)
    # print(type(list_links_bookpage))

    # search 1.year 2.publisher 3.dimensions 4.peso
    # 5.legatura 6. collana 7.luogo di pubblicazione 8.note 9.soggetti 10. numero pagine 11. volumi 12.edizione
    # 13. author 14. title
    # Here we define a function for each of these parameters we want to extract
    # Once we have all the functions, we make a for loop and call each function once for each link, i.e. book

    def search_details(self):
        soup_book_page = make_soup(self)
        list_details = soup_book_page.find('div', class_='details')
        return list_details

    def search_author(self):
        author_location = self.find('h2', itemprop='author')
        book_author = author_location.text
        return book_author

    def search_title(self):
        title_location = self.find('h1', itemprop='name')
        book_title = title_location.text
        return book_title

    def search_year(self):
        book_year_location = self.find('b', string=re.compile('Anno'))
        book_year = book_year_location.next_sibling.next_sibling.text
        return book_year

    def search_publisher(self):
        publisher_location = self.find('span', itemprop='publisher')
        book_publisher = publisher_location.text
        return book_publisher

    def search_soggetti(self):
        soggetti_location = self.find('b', string=re.compile('Sogge'))
        book_soggetti = soggetti_location.next_sibling.next_sibling.text
        return book_soggetti

    def search_dimensioni(self):
        dimensioni_location = self.find('b', string=re.compile('Dimen'))
        book_dimensioni = dimensioni_location.next_sibling.next_sibling.text
        return book_dimensioni

    def search_peso(self):
        peso_location = self.find('b', string=re.compile('Peso'))
        book_peso = peso_location.next_sibling.next_sibling.text
        return book_peso

    def search_legatura(self):
        publisher_location = self.find('span', itemprop='bookFormat')
        book_legatura = publisher_location.text
        return book_legatura

    def search_collana(self):
        collana_location = self.find('b', string=re.compile('Collana'))
        book_collana = collana_location.next_sibling.next_sibling.text
        return book_collana

    def search_luogo_pubblicazione(self):
        luogo_pubblicazione_location = self.find('b', string=re.compile('Luogo di pubblicazione'))
        book_luogo_pubblicazione = luogo_pubblicazione_location.next_sibling.next_sibling.text
        return book_luogo_pubblicazione

    def search_note_bibliografiche(self):
        note_bibliografiche_location = self.find('p', itemprop='description')
        book_note_bibliografiche = note_bibliografiche_location.text
        return book_note_bibliografiche

    def search_volumi(self):
        volumi_location = self.find('b', string=re.compile('Volumi'))
        book_volumi = volumi_location.next_sibling.next_sibling.text
        return book_volumi

    def search_edizione(self):
        edizione_location = self.find('span', itemprop='bookEdition')
        book_edizione = edizione_location.text
        return book_edizione

    def search_num_pagine(self):
        num_pagine_location = self.find('span', itemprop='numberOfPages')
        book_num_pagine = num_pagine_location.text
        return book_num_pagine

    # todo as of now, this loop will request the page twice,
    #  which can cause too much load on the server.
    #  I should create a txt file with the html source and then use that file for scraping.

    for i in list_links_bookpage:
        soup_whole_book_page = make_soup(i)
        details = search_details(i)

        try:
            book_year = search_year(details)
            return book_year
        except (AttributeError, NameError):
            book_year = None
            pass

        try:
            book_publisher = search_publisher(details)
            return book_publisher
        except (AttributeError, NameError):
            book_publisher = None
            pass

        try:
            book_soggetti = search_soggetti(details)
            return book_soggetti
        except (AttributeError, NameError):
            book_soggetti = None
            pass

        try:
            book_dimensioni = search_dimensioni(details)
            return book_dimensioni
        except (AttributeError, NameError):
            book_dimensioni = None
            pass

        try:
            book_peso = search_peso(details)
            return book_peso
        except (AttributeError, NameError):
            book_peso = None
            pass

        try:
            book_legatura = search_legatura(details)
            return book_legatura
        except (AttributeError, NameError):
            book_legatura = None
            pass

        try:
            book_collana = search_collana(details)
            return book_collana
        except (AttributeError, NameError):
            book_collana = None
            pass

        try:
            book_luogo_pubblicazione = search_luogo_pubblicazione(details)
            return book_luogo_pubblicazione
        except (AttributeError, NameError):
            book_luogo_pubblicazione = None
            pass

        try:
            book_note_bibliografiche = search_note_bibliografiche(details)
            return  book_note_bibliografiche
        except (AttributeError, NameError):
            book_note_bibliografiche = None
            pass

        try:
            book_volumi = search_volumi(details)
            return book_volumi
        except (AttributeError, NameError):
            book_volumi = None
            pass

        try:
            book_edizione = search_edizione(details)
            return  book_edizione
        except (AttributeError, NameError):
            book_edizione = None
            pass

        try:
            book_num_pagine = search_num_pagine(details)
            return book_num_pagine
        except (AttributeError, NameError):
            book_num_pagine = None
            pass

        #     le altre funzioni cercano nella lista "details" -
        #     funzione: search_details(), mentre queste vanno a cercare
        #     nella pagina completa, perche si trovano
        #     sotto un parent diverso (div class header > div class links > h2,h1)

        try:
            book_author = search_author(soup_whole_book_page)
            return book_author
        except (AttributeError, NameError):
            book_author = None
            pass

        try:
            book_title = search_title(soup_whole_book_page)
            return book_title
        except (AttributeError, NameError):
            book_title = None
            pass

        book_information = {
            "Title": book_title,
            "Author": book_author,
            "Publisher": book_publisher,
            "Publishing Year": book_year,
            "Luogo di pubblicazione": book_luogo_pubblicazione,
            "Edizione": book_edizione,
            "Dimensions": book_dimensioni,
            "Weight": book_peso,
            "Legatura": book_legatura,
            "Collana": book_collana,
            "Soggetti": book_soggetti,
            "Numero pagine": book_num_pagine,
            "Volumi": book_volumi,
            "Description": book_note_bibliografiche
        }

        # file.write(book_information)

        return book_information

        time.sleep(0.3)


try:
    books = search_maremagnum()
    print(books)
    print(type(books))
except AttributeError:
    print('no results in maremagnum')
    sys.exit()
finally:
    file.close()