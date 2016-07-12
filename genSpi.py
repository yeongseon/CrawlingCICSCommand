from urllib.request import urlopen
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from datetime import date
import re
from bs4 import NavigableString
import xml.etree.ElementTree as ET

#default_url = 'http://www-01.ibm.com/support/knowledgecenter/api/content/nl/ko/SSGMCP_4.2.0/com.ibm.cics.ts.systemprogramming.doc/commands/dfha8_{}.html'
#default_url = 'https://www.ibm.com/support/knowledgecenter/en/SSGMCP_4.2.0/com.ibm.cics.ts.systemprogramming.doc/commands/dfha8_{}.html?view=embed'
default_url = 'https://www.ibm.com/support/knowledgecenter/en/SSGMCP_4.2.0/com.ibm.cics.ts.systemprogramming.doc/commands/dfha8_{}.html'
default_url1 = 'https://www-01.ibm.com/support/knowledgecenter/api/content/nl/ko/SSGMCP_4.2.0/com.ibm.cics.ts.resourcedefinition.doc/resources/{}/dfha4_attributes.html'
output_syntax_full = 'spi/output_syntax/{}_full.txt'
output_syntax = 'spi/output_syntax/{}.txt'
output_syntax_html = 'spi/output_syntax/{}.html'
output_syntax_resource_html = 'spi/output_syntax/{}_resource.html'
output_syntax_resource = 'spi/output_syntax/{}_resource.txt'
output_xml = 'spi/output_xml/{}.xml'
output_options = 'spi/output_syntax/{}_options.txt'

class spisyntax(object):
    def __init__(self, command, resource):

        self.command, self.resource = str(command).lower(), str(resource).lower()
        self.systemcommand = self.command + self.resource
        self.systemcommandurl = default_url.format(self.systemcommand)

    def extract(self):

        page = urlopen(self.systemcommandurl).read()

        if page == None:
            print('urlopen error : ' + self.systemcommand)
            pass

        self.soup = BeautifulSoup(page)

        fname = output_syntax_html.format(self.systemcommand)
        f = open(fname, mode='w', encoding='utf-8')
        f.write(self.soup.prettify())
        f.close()

        fname = output_syntax_full.format(self.systemcommand)
        f = open(fname, mode='w', encoding='utf-8')
        f.write(self.soup.find_all('div')[1].text)
        f.close()

        fname = output_syntax.format(self.systemcommand)
        f = open(fname, mode='w', encoding='utf-8')
        f.write(self.soup.find_all('div')[2].text)
        f.close()

        if (self.command == 'create'):
            url = default_url1.format(self.resource)
            page = urlopen(url).read()
            self.soup = BeautifulSoup(page)

            fname = output_syntax_resource_html.format(self.systemcommand)
            f = open(fname, mode='w', encoding='utf-8')
            f.write(self.soup.prettify())
            f.close()

            div = self.soup.find_all("div", class_="section")

            fname = output_syntax_resource.format(self.systemcommand)
            f = open(fname, mode='w', encoding='utf-8')
            f.write(div[-1].text)
            f.close()


        return


