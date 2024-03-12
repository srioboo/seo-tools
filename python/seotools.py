import sys
import requests
import time
import csv
import re
from bs4 import BeautifulSoup

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
            csv_writer.writerow(list_input)
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
    print("-s -> get seo data")
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