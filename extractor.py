#!/usr/bin/python

__author__ = "Devharsh Trivedi"
__copyright__ = "Copyright 2018, Devharsh Trivedi"
__license__ = "GPL"
__version__ = "1.4"
__maintainer__ = "Devharsh Trivedi"
__email__ = "devharsh@live.in"
__status__ = "Production"

import sys, random
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# https://stackoverflow.com/a/73385650/16161618
user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/104.0.5112.99 Mobile/15E148 Safari/604.1"
        ]
reffer_list=[
    'https://stackoverflow.com/',
    'https://twitter.com/',
    'https://www.google.co.in/',
    'https://gem.gov.in/'
]


try:
    for link in sys.argv[1:]:
        headers = {'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(user_agent_list),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'referer': random.choice(reffer_list)}

        page = requests.get(link, headers=headers)
        soup = BeautifulSoup(page.text, "lxml")
        extlist = set()
        intlist = set()

        for a in soup.findAll("a", attrs={"href": True}):
            if (
                len(a["href"].strip()) > 1
                and a["href"][0] != "#"
                and "javascript:" not in a["href"].strip()
                and "mailto:" not in a["href"].strip()
                and "tel:" not in a["href"].strip()
            ):
                if "http" in a["href"].strip() or "https" in a["href"].strip():
                    if (
                        urlparse(link).netloc.lower()
                        in urlparse(a["href"].strip()).netloc.lower()
                    ):
                        intlist.add(a["href"])
                    else:
                        extlist.add(a["href"])
                else:
                    intlist.add(a["href"])

        print("\n")
        print(link)
        print("---------------------")
        print("\n")
        print(str(len(intlist)) + " internal links found:")
        print("\n")
        for il in intlist:
            print(il)
        print("\n")
        print(str(len(extlist)) + " external links found:")
        print("\n")
        for el in extlist:
            print(el)
        print("\n")

except Exception as e:
    print(e)
