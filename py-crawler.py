#!/bin/python3
import requests
from bs4 import BeautifulSoup
import argparse


urls = []


def add_url(url):
    url = url.rstrip('/').rstrip('#')

    if url not in urls:
        urls.append(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="py-crawler",
        description="Crawler a web page",
    )

    parser.add_argument("-u", "--url", required=True, help="Store the URL to crawler")

    args = parser.parse_args()

    url = args.url

    resp = requests.get(url)
    
    if resp.status_code == 200:
        add_url(url)
        soup = BeautifulSoup(resp.text, 'lxml')

        for a in soup.find_all('a'):
            href = a['href']
            add_url(href)

    for u in urls:
        if u.startswith('http://') or u.startswith('https://') or u.startswith('mailto:'):
            print(f"[+] {u}")
        else:
            print(f"[+] {url}/{u}")
