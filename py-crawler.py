#!/bin/python3
import requests
from bs4 import BeautifulSoup
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        prog="py-crawler",
        description="Crawler a web page",
    )

    parser.add_argument("-u", "--url", help="Store the URL to crawler")
    parser.add_argument('-uw', '--url-wordlist', help="A list of urls, separated by new line")
    parser.add_argument('--all-href', action='store_true', help="Download all the href in a targer URL", )
    parser.add_argument('-t', '--tags', type=str, help="The tags to search, an example: tag1, tag2, tag....")
    parser.add_argument('-a', '--attributes', type=str, help="The attributes to search, an example: attr1, attr2, attr...")
    parser.add_argument('-i', '--id', type=str, help="The id to search.")

    return parser.parse_args()


def get_the_soup(url):
    resp = requests.get(url)
    
    if resp.status_code == 200:
        return BeautifulSoup(resp.text, 'lxml')
    
    resp.raise_for_status()


def get_value_by_attrs(soup, tag, attrs: list):
    """
        Parse a soup and search a specific tag and their attributes 
    """
    vals = []
    for tag in soup.find_all(tag):
        for attr in attrs:
            val = tag[attr]
            
            if val not in vals:
                vals.append(val)
    return vals


def get_value_by_attr(soup, tag: str, attr: str):
    """
        Parse a soup and search a specific tag and their attribute 
    """
    vals = []
    for tag in soup.find_all(tag):
        val = tag[attr]
        
        if val not in vals:
            vals.append(val)
    return vals


def get_from_tags(soup, tags: list):
    elements = []
    for tag in tags:
        for element in soup.find_all(tag):
            if element not in elements:
                elements.append(element)
    return elements


def search_id(soup, id: str):
    elements = []
    for element in soup.find_all(id=id):
        if element not in elements:
            elements.append(element)
    return elements

if __name__ == '__main__':
    args = get_args()

    if args.url:
        url = args.url
        print(f'[+] Url: {url}')
        soup = get_the_soup(url)
        print('[+] Souped!\n')

        if args.all_href:
            print('[+] Searching for all the urls...')
            urls = get_value_by_attr(soup, 'a', 'href')
        
            for u in urls:
                if u.startswith('http://') or u.startswith('https://') or u.startswith('mailto:'):
                    print(f"[+] {u}")
                else:
                    print(f"[+] {url}/{u}")
        elif args.tags:
            print('[+] Searching for all the tags...')
            elements = get_from_tags(soup, args.tags.split(','))
            for e in elements:
                print(f'[+] {e}')
        elif args.id:
            print(f'[+] Searching id: {args.id}...')
            elements = search_id(soup, args.id)
            for e in elements:
                print(f'[+] Tag: {e.name}; content: {e.text}')
    elif args.url_wordlist:
        print(f'[+] Wordlist: {args.url_wordlist}')
        with open(args.url_worlist, 'r') as f:
            print(f.readlines())


