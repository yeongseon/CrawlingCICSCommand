from urllib.request import urlopen
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from datetime import date
import re
from bs4 import NavigableString
import xml.etree.ElementTree as ET

defult_url = 'https://www-01.ibm.com/support/knowledgecenter/api/content/nl/en-us/SSGMCP_4.2.0/com.ibm.cics.ts.applicationprogramming.doc/commands/dfhp4_{}.html'
output_syntax_html = 'api/output_syntax/{}.html'
output_syntax_full = 'api/output_syntax/{}_full.txt'
output_syntax = 'api/output_syntax/{}.txt'
output_syntax_html = 'api/output_syntax/{}.html'

class apisyntax(object):
    def __init__(self, command):
        self.applicationcommand = command
        self.applicationcommand_url = defult_url.format(self.applicationcommand)
        return

    def extract(self):
        page = urlopen(self.applicationcommand_url).read()

        if page == None:
            print('urlopen error : ' + self.applicationcommand)
            pass

        self.soup = BeautifulSoup(page)

        fname = output_syntax_html.format(self.applicationcommand)
        f = open(fname, mode='w', encoding='utf-8')
        f.write(self.soup.prettify())
        f.close()

        fname = output_syntax_full.format(self.applicationcommand)
        f = open(fname, mode='w', encoding='utf-8')
        f.write(self.soup.find_all('div')[1].text)
        f.close()

        fname = output_syntax.format(self.applicationcommand)
        f = open(fname, mode='w', encoding='utf-8')
        f.write(self.soup.find_all('div')[2].text)
        f.close()

        return