from urllib.request import urlopen
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from datetime import date
import re
from bs4 import NavigableString
import xml.etree.ElementTree as ET
from collections import Counter

default_url = 'https://www-01.ibm.com/support/knowledgecenter/api/content/nl/en-us/SSGMCP_4.2.0/com.ibm.cics.ts.applicationprogramming.doc/commands/dfhp4_{}.html'
output_syntax_html = 'api/output_syntax/{}.html'
output_syntax_full = 'api/output_syntax/{}_full.txt'
output_syntax = 'api/output_syntax/{}.txt'
output_syntax_html = 'api/output_syntax/{}.html'
output_xml = 'api/output_xml/{}.xml'

class genAPIXml(object):
    def __init__(self, apicommand=None):
        self.systemcommand = apicommand
        self.systemcommandurl = default_url.format(self.systemcommand)
        return

    def gen_xml1(self):
        fname = output_syntax.format(self.systemcommand)
        f = open(fname, mode='r', encoding='utf-8')
        text = f.read()
        f.close()

        pattern = re.compile(r"[A-Z]*[-]*\([-]*[a-z]+\-?[a-z]+[-]*\)")

        root = ET.Element('data')

        option_list = []
        for option in pattern.findall(text):
            temp_option = option.replace('-','')
            if temp_option in option_list:
                continue
            else:
                option_list.append(temp_option)

        for option in option_list:
            if str(option).find('('):
                argument_name, argument_value = option.split('(')[0], option.split('(')[1].split(')')[0]
                argument = ET.SubElement(root, 'argument', name=argument_name)

            '''
            Argument values : data-area, data-value, ptr-ref, ptr-value, cvda
            '''
            if argument_value == 'dataarea':
                value = ET.SubElement(argument, 'value').text = 'data-area'
            elif argument_value == 'datavalue':
                value = ET.SubElement(argument, 'value').text = 'data-value'
            elif argument_value == 'ptrref':
                value = ET.SubElement(argument, 'value').text = 'ptr-ref'
            elif argument_value == 'ptrvalue':
                value = ET.SubElement(argument, 'value').text = 'ptr-value'
            elif argument_value == 'cvda':
                value = ET.SubElement(argument, 'value').text = 'cvda'

        self.indent(root)
        tree = ET.ElementTree(root)
        xml_file = output_xml.format(self.systemcommand)
        tree.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")

    def gen_xml2(self):
        page = urlopen(self.systemcommandurl).read()
        self.soup = BeautifulSoup(page)

        for div in self.soup.find_all('div', {'class' : 'section'}):
            if (div.h2):    # 값이 있는 경우
                if div.h2.text == 'Options':
                    option_div = div


        # print((option_div.dl.dt.text)) # 맨처음 resource(type) 출력

        if str(option_div.dl.dt.text).find('(') :
            argument_name, argument_value = str(option_div.dl.dt.text).split('(')[0], \
                          str(option_div.dl.dt.text).split('(')[1].split(')')[0]


        for i in option_div.dt.next_siblings:
            if(i.name == 'dt') :
                # print(i.text)   # resource(type) 출력

                if str(i.text).find('(') > 0:
                    argument_name, argument_value = str(i.text).split('(')[0], \
                                                str(i.text).split('(')[1].split(')')[0]
                else:
                    argument_name = str(i.text)

            if(i.name == 'dd') :
                #print (type(dt), dt.string) # cvda 제외하고는 구분
                # print(type(dt))
                if (i.dt):     # 리소스 이름
                    # 여기서부터 cvda 시작
                    #print(i.dl.dt.text) # cvda
                    self.add_cvda(argument_name, i.dl.dt.text)
                    for j in i.dl.dt.next_siblings:
                        if(j.name == 'dt'):
                            #print(j.text)  # cvda value
                            self.add_cvda(argument_name, j.text)

    def indent(self, elem, level=0):
          i = "\n" + level*"  "
          if len(elem):
            if not elem.text or not elem.text.strip():
              elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
              elem.tail = i
            for elem in elem:
              self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
              elem.tail = i
          else:
            if level and (not elem.tail or not elem.tail.strip()):
              elem.tail = i