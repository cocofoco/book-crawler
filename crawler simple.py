from bs4 import BeautifulSoup
import requests
import sys
import re
import time
import csv

# todo crawl also for adebooks
# todo context manage for file

# todo da aggiungere scraping for prezzo

# file = open('Example', 'a')


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

    def search_author(self):
        author_location = self.find('h2', itemprop='author')
        book_author = author_location.text
        return book_author

    def search_title(self):
        title_location = self.find('h1', itemprop='name')
        book_title = title_location.text
        return book_title

    for i in list_links_bookpage:
        soup_page = make_soup(i)

        title = search_title(soup_page)
        author = search_author(soup_page)

        book_info = {
            'title': title,
            'author': author
        }

        print(book_info)

    print(list_links_bookpage)
    print(type(list_links_bookpage))

search_maremagnum()