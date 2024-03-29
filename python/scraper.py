import sys
import requests
import time
import csv
import re
from bs4 import BeautifulSoup

# get data from a web menu
def scrape_menu(soup, base_url='', language=''):
    # categories
    categories = soup.select("a[class^='menu_']")

    # file namess
    csv_menu_file = 'data_menu' + '_' + base_url + '_' + language
    csv_url_file = 'data_url' + '_' + base_url + '_' + language

    for cat in categories:
        url = cat['href']
        catnum = cat['id']
        catid = cat['data-catid']

        write_to_csv([catid,catnum,url], csv_menu_file)
        # write_to_csv([url], csv_url_file)
    print('Generated tree categories csv: ', csv_menu_file)

# get data from a card
def scrape_tarjeta(soup, base_url='', language=''):
    # categories
    categories = soup.select("a[class^='menu_']")

    # file namess
    csv_menu_file = 'data_menu' + '_' + base_url + '_' + language
    csv_url_file = 'data_url' + '_' + base_url + '_' + language

    for cat in categories:
        url = cat['href']
        catnum = cat['id']
        catid = cat['data-catid']

        write_to_csv([catid,catnum,url], csv_menu_file)
        # write_to_csv([url], csv_url_file)
    print('Generated tree categories csv: ', csv_menu_file)

# this is an example to scrape a book
def scrape(source_url, soup):  # Takes the driver and the subdomain for concats as params
    # Find the elements of the article tag
    books = soup.find_all("article", class_="product_pod")

    # Iterate over each book article tag
    for each_book in books:
        info_url = source_url+"/"+each_book.h2.find("a")["href"]
        cover_url = source_url+"/catalogue" + each_book.a.img["src"].replace("..", "")

        title = each_book.h2.find("a")["title"]
        rating = each_book.find("p", class_="star-rating")["class"][1]
        # can also be written as : each_book.h2.find("a").get("title")
        price = each_book.find("p", class_="price_color").text.strip().encode(
            "ascii", "ignore").decode("ascii")
        availability = each_book.find(
            "p", class_="instock availability").text.strip()

        # Invoke the write_to_csv function
        write_to_csv([info_url, cover_url, title, rating, price, availability])

# write data to csv
def write_to_csv(list_input, file_name='data'):
    # The scraped info will be written to a CSV here.
    try:
        with open(f'{file_name}.csv', "a", encoding='UTF8', newline='') as fopen:  # Open the csv file.
            csv_writer = csv.writer(fopen)
            # head row
            csv_writer.writerow(['file1','file2','file3'])
            # content row
            csv_writer.writerows(list_input)
    except:
        return False

# Auxiliary method to print data in a formatted way
def log(data, value):
    print(data)
    print(f'\t{value}')
    print("")

# get head metadata
def get_head_metadata(soup):

    # get title
    metatitle = (soup.find('title')).get_text()
    log("metatile: ", metatitle)

    # get metadescription
    metadescription = soup.find('meta',attrs={'name':'description'})["content"]
    log("metadescription: ", metadescription)

    # get metarobots
    if soup.find('meta',attrs={'name':'robots'}) != None:
        robots_directives = soup.find('meta',attrs={'name':'robots'})["content"].split(",")
        log('Directivas robot',robots_directives)
        write_to_csv(robots_directives)
    else:
        log("Directivas robot", "not found")

    # get viewport
    viewport = soup.find('meta',attrs={'name':'viewport'})["content"]
    log('Vieport:', viewport)

    # get charset
    # charset = soup.find('meta',attrs={'charset':True})["charset"]
    # log('Charset: ', charset)

# get canonical and hreflang
def get_canonical(soup):

    # canonical
    if soup.find('link',attrs={'rel':'canonical'}) != None:
        canonical = soup.find('link',attrs={'rel':'canonical'})["href"]
        log('Canonical: ', canonical)
    else:
        log('Canonical: ', 'not found')

# get canonical and hreflang
def get_hreflang(soup):
    # hreflang
    list_hreflangs = [[a['href'], a["hreflang"]] for a in soup.find_all('link', href=True, hreflang=True)]
    # log('Hreflangs: ', list_hreflangs)
    return list_hreflangs

# get language
def get_lang(soup):
    html_language = soup.find('html')["lang"]
    log('Html language: ', html_language)

# get media
def get_media(soup):
    if soup.find('link',attrs={'media':'only screen and (max-width: 640px)'}) != None:
        mobile_alternate = soup.find('link',attrs={'media':'only screen and (max-width: 640px)'})["href"]
        log('Mobile alternate: ', mobile_alternate)
    else:
        log('Mobile alternate: ', 'not found')

# alter cookies
def alter_cookie(session, node):
    # get de cookies
    mi_cookies = session.cookies
    cookies_dic = mi_cookies.get_dict()
    # log('cookies: ',cookies_dic)

    # get searched cookie
    jsession = mi_cookies.get('JSESSIONID')
    # log('jsession: ', jsession)

    jsession_arr = jsession.split(':')

    # for i in range(len(nodes_arr)):
    jsession_alt = jsession.replace(':' + jsession_arr[1], ':' + node)
    print('jsession_new: ', jsession_alt)

    session.cookies.set('JSESSIONID', jsession_alt, domain='www.one-url.com')

    # Example google cookies
    # a_session = requests.Session()
    # a_session.get('https://google.com/')
    # session_cookies = a_session.cookies
    # cookies_dictionary = session_cookies.get_dict()
    # print('Google cookies: ',cookies_dictionary)

# test if it have an url format
def is_url(formatted_url):

    is_url = False

    # Fetch the URL - We will be using this to append to images and info routes
    url_pat = re.compile(r"(https://*.*.*)")
    # print(url_pat)
    # print(formatted_url)
    source_url = url_pat.search(formatted_url)
    # print(source_url)
    if source_url != None:
        is_url = True
    return is_url

# get seo data
def get_full_seo_data(soup):
    # get head metadata
    get_head_metadata(soup)

    # get canonical
    get_canonical(soup)

    # get canonical and hreflang
    list_hreflangs = get_hreflang(soup)
    # hreflang loop
    for x in list_hreflangs:
        print(str(x))

    # get language
    get_lang(soup)

    # get media
    # get_media(soup)

# get data to parse
def get_soup(session, formatted_url):
    # after alter session get data and get text
    response = session.get(formatted_url)
    # get de text
    html_text = response.text

    # Prepare the soup
    soup = BeautifulSoup(html_text, "html.parser")
    
    # retur soup
    return soup

# this get the data
def browse_and_scrape(formatted_url, choice=1):

    # nodes
    nodes_arr = ['c1pro01','c1pro02','c1pro03','c1pro04','c2pro01','c2pro02','c2pro03','c2pro04']

    try:
        # get session
        session = requests.Session()
        # first get to cookie
        response = session.get(formatted_url)
        
        if choice == 1:
            # get data
            soup = get_soup(session, formatted_url)
            get_full_seo_data(soup)

        elif choice == 2:
            # rows
            rows = []
            # alter cookies
            for i in range(len(nodes_arr)):
                alter_cookie(session, nodes_arr[i])

                # get the soup for each cookie alteration
                soup = get_soup(session, formatted_url)

                # Be a responsible citizen by waiting before you hit again
                time.sleep(3)

                # categories
                categories = soup.select("a[class^='menu_']")
                print('Categories tree size: ', len(categories))

                # construct row and add to rows
                rows.append([len(categories),'test'])

            # print csv
            write_to_csv(rows, 'menu_simple')

        elif choice == 3:
            # get the soup
            soup = get_soup(session, formatted_url)

            # get canonical and hreflang
            list_hreflangs = get_hreflang(soup)
            # log('Hreflangs: ', list_hreflangs) 

            # hreflang loop
            for x in list_hreflangs:
                # print(str(x))
                new_url = x[0]
                new_lang = x[1]
                
                if "-" in new_lang:
                    # go to all hreflang and search empty url
                    # get data
                    soup = get_soup(session, new_url)
                    # scrape menu data
                    scrape_menu(soup, '', new_lang)
            print("grep 'Category_' *.csv")

        elif choice == 4:
            # alter cookies
            for i in range(len(nodes_arr)):
                alter_cookie(session, nodes_arr[i])

                # get the soup for each cookie alteration
                soup = get_soup(session, formatted_url)

                # Be a responsible citizen by waiting before you hit again
                time.sleep(3)

                # cards
                cards = soup.select("button[class='btn btn-block btn-default dropdown-toggle']")
                texto = ''
                is_correct = 'wrong'
                if len(cards) != 0 and cards[0] != None:
                    texto = cards[0].text
                else:
                    texto = 'price selector not found'
                    is_correct = ''

                if 'importe' in texto:
                    is_correct = 'correct!!'
                print(f'Card {is_correct}: ', texto)

        elif choice == 5:
            print('working -- test if menus in nodes are correct in all countries')
            # get the soup
            soup = get_soup(session, formatted_url)

            # get canonical and hreflang
            list_hreflangs = get_hreflang(soup)

            # hreflang loop
            print(list_hreflangs)
            for x in list_hreflangs:
                # print(str(x))
                new_url = x[0]
                new_lang = x[1]
                # print(new_url)
                # print(new_lang)

                if "-" in new_lang and "ru" not in new_lang:
                    print(new_url)
                    # go to all hreflang and search empty url
                    # get data
                    # soup = get_soup(session, new_url)

                    # alter cookies
                    #for i in range(len(nodes_arr)):
                    #alter_cookie(session, nodes_arr[i])

                    # get the soup for each cookie alteration
                    soup = get_soup(session, new_url)

                    # Be a responsible citizen by waiting before you hit again
                    time.sleep(2)

                    # categories
                    categories = soup.select("a[class^='menu_']")
                    print('Categories tree size: ', len(categories))
                    write_to_csv([new_url, len(categories)], 'menu_status')

        else:
            help_message()        

        return True
    except Exception as e:
        print(e)
        return e

# Print help message
def help_message():
    print("Help message:")
    print("acepted parameters")
    print("-h -> help menu")
    print("-s -> get seo data")
    print("-m -> test if menus in nodes are correct")
    print("-a -> test if menus in nodes are correct in all countries")
    print("-u -> list not SEO compilant urls")
    print("-t -> verify is 'Tarjeta regalo' has diferents amounts")
    print("only one is allowed")
    print("Do you need a valid url")

# main method
if __name__ == "__main__":
    # test if there are args
    # if len(sys.argv) == 2:
    #    seed_url = sys.argv[1]
    # else:
    #    seed_url = 'https://salrion.netlify.app'

    # base seed url
    seed_url = 'https://salrion.netlify.app'
    choice = 0

    for argument in sys.argv:
        # get and show arguments
        if is_url(argument):
            seed_url = argument
        elif argument == '-s':
            choice = 1
        elif argument == '-m':
            choice = 2
        elif argument == '-u':
            choice = 3
        elif argument == '-t':
            choice = 4
        elif argument == '-a':
            choice = 5
        elif argument == '-h':
            choice = 0

        # print(is_url(argument))
        # print(argument)

    print(seed_url)

    print(f"Web {seed_url} scraping has begun")
    print("----------------------------------")
    result = browse_and_scrape(seed_url, choice)
    if result == True:
        print("----------------------------------")
        print("Web scraping is now complete!")
    else:
        print(f"Oops, That doesn't seem right!!! - {result}")                        