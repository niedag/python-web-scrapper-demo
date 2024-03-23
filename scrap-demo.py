import requests
from bs4 import BeautifulSoup

def req_demo():
    r = requests.get("https://www.geeksforgeeks.org/python-programming-language/")
    print(r)

    print(r.content)

def bsoup_demo():
    r = requests.get("https://www.geeksforgeeks.org/python-programming-language/")
    print(r)

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup.prettify())


bsoup_demo()
