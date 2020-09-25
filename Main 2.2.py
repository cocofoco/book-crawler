from bs4 import BeautifulSoup
import requests
# import sys
import re
import time
import csv

# todo crawl also for adebooks
# todo context manager for file

# todo create csv file from the results
# todo create html description from csv file

# todo da aggiungere scraping for prezzo

# file = open('Example', 'a')

search_terms = input("Che cosa cerchi? ")


# search_terms = 'le mille una notte nugoli'


def make_soup(self):
    page_link = requests.get(self)
    src = page_link.content
    soup_page = BeautifulSoup(src, 'lxml')
    return soup_page


def silence_error(self):
    try:
        return self
    except (AttributeError, NameError):
        pass


def remove_error(self, fun_soup):
    try:
        self(fun_soup)
        pass
    except (AttributeError, NameError):
        return self


# def create_soup_file(self):
#     soup_text = make_soup(self)

class Book:
    def __init__(self, title, author, publisher, publishing_year, luogo_pubblicazione, edizione, dimensions, weight,
                 legatura, collana, soggetti, num_pagine, volumi, description, website):
        self.title = title
        self.author = author
        self.publishing_year = publishing_year
        self.publisher = publisher
        self.luogo_pubblicazione = luogo_pubblicazione
        self.soggetti = soggetti
        self.weight = weight
        self.dimensions = dimensions
        self.legatura = legatura
        self.collana = collana
        self.edizione = edizione
        self.volumi = volumi
        self.num_pagine = num_pagine
        self.description = description
        self.website = website

    @classmethod
    def create_book_list(cls, selected_list, website):
        book_list = []
        for i in selected_list:
            created_book = cls(
                title=i.get('title'),
                author=i.get('author'),
                publishing_year=i.get('year'),
                publisher=i.get('publisher'),
                soggetti=i.get('soggetti'),
                weight=i.get('peso'),
                dimensions=i.get('dimensioni'),
                legatura=i.get('legatura'),
                collana=i.get('collana'),
                luogo_pubblicazione=i.get('luogo_pubblicazione'),
                description=i.get('note_bibliografiche'),
                edizione=i.get('edizione'),
                volumi=i.get('volumi'),
                num_pagine=i.get('num_pagine'),
                website=website
            )
            book_list.append(created_book)
        return book_list

# class BookMaremagnum(Book):
#     def __init__(self, title, author, publisher, publishing_year, luogo_pubblicazione,
#                  edizione, dimensions, weight,
#                  legatura, collana, soggetti, num_pagine, volumi, description, website):
#         Book.__init__(self, title, author, publisher, publishing_year, luogo_pubblicazione,
#                       edizione, dimensions, weight, legatura,
#                       collana, soggetti, num_pagine, volumi, description)


def search_maremagnum(self):
    # given some search parameters, these functions will:
    # . create the appropiate link
    # . find the relative search page in maremagnum
    # . limit the scraping to x elements

    search_limit = 35

    def create_link_maremagnum(self):
        maremagnum_link_first_part = 'https://www.maremagnum.com/ricerca' \
                                     '/risultati?search%5Bkeyword%5D='
        search_terms_maremagnum = self.strip().lower().replace(' ', '+')
        search_link_maremagnum = maremagnum_link_first_part + search_terms_maremagnum
        return search_link_maremagnum

    def try_find_results(self):
        try:
            soup_maremagnum_search = make_soup(self)
            return soup_maremagnum_search
        except AttributeError as e:
            print(e)
            print('No results.')
            return

    def check_limit(self):
        number_of_results = int(self.find('section', id='inside-search').label.span.text)
        if number_of_results < search_limit:
            pass
        else:
            print(f'>{search_limit} results found. Limited scraping to first {search_limit} elements.')
            pass

    # here we find the link to the page of each book present in the search result

    link_maremagnum = create_link_maremagnum(self)
    soup_mare = try_find_results(link_maremagnum)
    check_limit(soup_mare)

    # within the search page there will be multiple results. Within each there's an
    # embedded link to the relative book page.
    # This function extracts each book of these links

    def extract_links(self):
        website_maremagnum = 'https://maremagnum.com'
        list_finalpart_bookpage = []
        list_links_bookpages = []
        for book in self.findAll('li', class_='note', limit=search_limit):
            finalpart_link_bookpage = book.find('a')
            list_finalpart_bookpage.append(finalpart_link_bookpage.attrs['href'])

            link_book_complete = website_maremagnum + finalpart_link_bookpage.attrs['href']
            list_links_bookpages.append(link_book_complete)

        return list_links_bookpages

        # print(list_links_bookpage)
        # print(type(list_links_bookpage))

    # There are multiple attributes for each book:
    # 1.year 2.publisher 3.dimensions 4.peso 5.legatura
    # 6. collana 7.luogo di pubblicazione 8.note 9.soggetti 10. numero pagine
    # 11. volumi 12.edizione 13. author 14. title
    # Here we define a function to search for each of these parameters we want to extract

    # most of these search functions will search within a 'details' list.
    # This function searches for that part of the html.

    def search_details(self):
        list_details = self.find('div', class_='details')
        return list_details

    def search_general(self, tag, attribute, src_str):
        global location
        if attribute == 'string':
            location = self.find(f'{tag}', string=re.compile(f'{src_str}'))
        elif attribute == 'itemprop':
            location = self.find(f'{tag}', itemprop=f'{src_str}')

        need_sibling = ('Anno', 'Sogge', 'Dimen', 'Peso', 'Collana', 'Luogo di pubblicazione', 'Volumi')

        if src_str in need_sibling:
            info = location.next_sibling.next_sibling.text
        else:
            info = location.text

        return info

    def search_author(self):
        book_author = search_general(self, 'h2', 'itemprop', 'author')
        return book_author

    def search_title(self):
        book_title = search_general(self, 'h1', 'itemprop', 'name')
        return book_title

    def search_year(self):
        book_year = search_general(self, 'b', 'string', 'Anno')
        return book_year

    def search_publisher(self):
        book_publisher = search_general(self, 'span', 'itemprop', 'publisher')
        return book_publisher

    def search_soggetti(self):
        book_soggetti = search_general(self, 'b', 'string', 'Sogge')
        return book_soggetti

    def search_peso(self):
        book_peso = search_general(self, 'b', 'string', 'Peso')
        return book_peso

    def search_dimensioni(self):
        book_dimensioni = search_general(self, 'b', 'string', 'Dimen')
        return book_dimensioni

    def search_legatura(self):
        book_legatura = search_general(self, 'span', 'itemprop', 'bookFormat')
        return book_legatura

    def search_collana(self):
        book_collana = search_general(self, 'b', 'string', 'Collana')
        return book_collana

    def search_luogo_pubblicazione(self):
        book_lg_pub = search_general(self, 'b', 'string', 'Luogo di pubblicazione')
        return book_lg_pub

    def search_note_bibliografiche(self):
        book_note = search_general(self, 'p', 'itemprop', 'description')
        return book_note

    def search_volumi(self):
        book_vol = search_general(self, 'b', 'string', 'Volumi')
        return book_vol

    def search_edizione(self):
        book_ediz = search_general(self, 'span', 'itemprop', 'bookEdition')
        return book_ediz

    def search_num_pagine(self):
        book_num_pag = search_general(self, 'span', 'itemprop', 'numberOfPages')
        return book_num_pag

    functions_to_try_details = [search_year, search_publisher, search_soggetti, search_peso,
                                search_dimensioni, search_legatura,
                                search_collana, search_luogo_pubblicazione,
                                search_note_bibliografiche,
                                search_volumi, search_edizione, search_num_pagine]
    functions_to_try_soup = [search_author, search_title]

    list_links_book = extract_links(soup_mare)
    book_list = []

    def extract_info(self, list_to_try):
        funcs_removanda = []

        for z in list_to_try:
            defective_funcs = remove_error(z, self)
            funcs_removanda.append(defective_funcs)

        working_funcs = [i for i in list_to_try if i not in funcs_removanda]

        var_name_list = []
        info_list = []

        for i in working_funcs:
            func_name = i.__name__
            var_name = func_name.lower().replace('search_', '')
            info = i(self)

            var_name_list.append(var_name)
            info_list.append(info)

        book_info = dict(zip(var_name_list, info_list))

        return book_info

    for i in list_links_book:
        soup_page = make_soup(i)
        details = search_details(soup_page)

        details_dic = extract_info(details, functions_to_try_details)
        page_dic = extract_info(soup_page, functions_to_try_soup)

        book_dic = {
            **details_dic,
            **page_dic
        }

        book_list.append(book_dic)

        time.sleep(0.03)

    return book_list


list_books_info = search_maremagnum(search_terms)
list_books = Book.create_book_list(list_books_info, 'maremagnum')

file_title = search_terms
directory = 'D:\\Website searcher files\\csv files'

with open(f'{directory}\\{file_title}.csv', 'w') as new_file:
    fieldnames = ['Title', 'Author', 'Publishing Year', 'Publisher', 'Luogo di Pubblicazione',
                  'Soggetti', 'Peso', 'Dimensioni', 'Legatura',
                  'Collana', 'Edizione', 'Volumi', 'Numero di pagine',
                  'Note Bibliografiche']

    csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')

    csv_writer.writeheader()
    for book in list_books:
        csv_writer.writerow(
            {'Title': book.title,
            'Author': book.author,
            'Publishing Year': book.publishing_year,
            'Publisher': book.publisher,
            'Luogo di Pubblicazione': book.luogo_pubblicazione,
            'Soggetti': book.soggetti,
            'Peso': book.weight,
            'Dimensioni': book.dimensions,
            'Legatura': book.legatura,
            'Collana': book.collana,
            'Edizione': book.edizione,
            'Volumi': book.volumi,
            'Numero di pagine': book.num_pagine,
            'Note Bibliografiche': book.description}
        )
