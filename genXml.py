from urllib.request import urlopen
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from datetime import date
import re
from bs4 import NavigableString
import xml.etree.ElementTree as ET
from collections import Counter
import pattern

#default_url = 'https://www.ibm.com/support/knowledgecenter/en/SSGMCP_4.2.0/com.ibm.cics.ts.systemprogramming.doc/commands/dfha8_{}.html?view=embed'
default_url = 'https://www.ibm.com/support/knowledgecenter/en/SSGMCP_4.2.0/com.ibm.cics.ts.systemprogramming.doc/commands/dfha8_{}.html'
#default_url = 'http://www-01.ibm.com/support/knowledgecenter/api/content/nl/ko/SSGMCP_4.2.0/com.ibm.cics.ts.systemprogramming.doc/commands/dfha8_{}.html'
default_url1 = 'https://www-01.ibm.com/support/knowledgecenter/api/content/nl/ko/SSGMCP_4.2.0/com.ibm.cics.ts.resourcedefinition.doc/resources/{}/dfha4_attributes.html'
output_syntax_full = 'spi/output_syntax/{}_full.txt'
output_syntax_full = 'spi/output_syntax/{}_full.txt'
output_syntax = 'spi/output_syntax/{}.txt'
output_syntax_resource = 'spi/output_syntax/{}_resource.txt'
output_options = 'spi/output_syntax/{}_options.txt'
output_resps = 'spi/output_syntax/{}_resps.txt'
output_syntax_html = 'spi/output_syntax/{}.html'
output_xml = 'spi/output_xml/{}.xml'

pattern_hexadecimal8 = r'(8 hexadecimal digits)'
pattern_byte1 = r'1-byte'
pattern_byte1_1 = r'1 byte character'
pattern_byte2 = r'2-byte'
pattern_byte4 = r'4-byte'
pattern_byte4_1 = r'4 byte character'
pattern_byte8 = r'8-byte'
pattern_byte8_1 = r'8 byte character'
pattern_byte16 = r'16-byte'
pattern_byte16_1 = r'16 byte character'
pattern_byte28 = r'28-byte'
pattern_byte28_1 = r'28 byte character'
pattern_byte32 = r'32-byte'
pattern_byte32_1 = r'32 byte character'
pattern_byte64 = r'64-byte'
pattern_byte64_1 = r'64 byte character'

pattern_character1 = r'(1 character)'
pattern_character1_1 = r'(single character)'
pattern_character3 = r'(3 character)'
pattern_character3_1 = r'(3-character)'
pattern_character5 = r'(5 character)'
pattern_character5_1 = r'(5-character)'
pattern_character5_2 = r'(five character)'
pattern_character4 = r'(4 character)'
pattern_character4_1 = r'(4-character)'
pattern_character4_2 = r'(four character)'
pattern_character7 = r'(7 characters)'
pattern_character7_1 = r'(7-character)'
pattern_character8 = r'(8 characters)'
pattern_character8_1 = r'(8-character)'
pattern_character8_2 = r'(eight character)'
pattern_character16 = r'(16 character)'
pattern_character16_1 = r'(16-character)'
pattern_character26 = r'(26 character)'
pattern_character26_1 = r'(26-character)'
pattern_character32 = r'(32 character)'
pattern_character32_1 = r'(32-character)'
pattern_character44 = r'(44 character)'
pattern_character44_1 = r'(44-character)'
pattern_character58 = r'(58 character)'
pattern_character255 = r'(255 character)'
pattern_character255_1 = r'(255-character)'

pattern_cvda = r'(CVDA value)'
pattern_doubleword = r'doubleword binary'
pattern_fullword = r'fullword binary'
pattern_fullword1 = r'fullword data'
pattern_number1 = r'number of buffers'
pattern_length1 = r'length of the'
pattern_halfword = r'halfword binary'
pattern_character = r'\d(-character)'
pattern_digit = r'\d(-digit number)'
pattern_abstime = r'ABSTIME value'
pattern_obsolete = r'obsolete'

pattern_range = r'the range'

invalid_cvda1 = 'has an invalid CVDA value.'
invalid_cvda2 = 'An invalid CVDA is specified for the '
invalid_option = ' option is invalid' # The TABLE option is invalid for a file defined with the REUSE option.
invalid_name = ' name is specified.' # An invalid CFDTPOOL name is specified.
invalid_range1 = ' value is not in the range ' # STRINGS value is not in the range 1 - 255, or this is not a VSAM file.
invalid_range2 = ' is not in the range' # LSRPOOLNUM is not in the range 1 - 255, or the corresponding buffer is not defined.
invalid_range3 = 'An invalid ' # An invalid RECORDSIZE is specified. RECORDSIZE must be in the range 0 - 32 767 bytes.
invaild_range4 = ' value is out of range.' # MAXNUMRECS value is out of range.
invaild_range5 = ' value not in range'  # TERMPRIORITY value not in range 0–255.
invlaid_specified1 = ' is not specified'  # CFDTPOOL is not specified for a file that refers to a coupling facility data table.
invlaid_specified2 = ' has been specified' # DELETE has been specified for a non-VSAM file.

class genXml(object):
    def __init__(self, command=None, resource=None):
        self.command = command
        self.resource = resource
        self.systemcommand = self.command + self.resource
        self.systemcommandurl = default_url.format(self.systemcommand)
        self.resourcedefintionurl = default_url1.format(self.resource)
        return

    def gen_xml_discard(self):
        root = ET.Element('data')

        argument = ET.SubElement(root, 'argument', name=str(self.resource).upper())
        value = ET.SubElement(argument, 'value').text = 'data-value'
        type = ET.SubElement(argument, 'type').text = 'Character'
        length = ET.SubElement(argument, 'length').text = str(self.get_resource_len(self.resource.upper()))

        self.indent(root)
        tree = ET.ElementTree(root)
        xml_file = output_xml.format(self.systemcommand)
        tree.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")

        return

    def get_resource_len(self, resource):
        if resource == 'CONNECTION':
            return 4
        elif resource == 'FILE':
            return 8
        elif resource == 'JOURNALMODEL':
            return 8
        elif resource == 'PROGRAM':
            return 8
        elif resource == 'TDQUEUE':
            return 4
        elif resource == 'TERMINAL':
            return 4
        elif resource == 'TRANCLASS':
            return 8
        elif resource == 'TRANSACTION':
            return 8
        elif resource == 'TSMODEL':
            return 8
        elif resource == 'TSQUEUE':
            return 8
        elif resource == 'TYPETERM':
            return 8
        elif resource == 'WEBSERVICE':
            return 32


    def gen_xml4(self):
        fname = output_syntax.format(self.systemcommand)
        f = open(fname, mode='r', encoding='utf-8')
        text = f.read()

        root = ET.Element('data')

        argument = ET.SubElement(root, 'argument', name=str(self.resource).upper())
        value = ET.SubElement(argument, 'value').text = 'data-value'
        type = ET.SubElement(argument, 'type').text = 'Character'
        length = ET.SubElement(argument, 'length').text = str(self.get_resource_len(self.resource.upper()))

        #argument = ET.SubElement(root, 'argument', name='ATTRIBUTE')
        #value = ET.SubElement(argument, 'value').text = 'data-area'

        argument = ET.SubElement(root, 'argument', name='ATTRLEN')
        value = ET.SubElement(argument, 'value').text = 'data-value'
        type = ET.SubElement(argument, 'type').text = 'Halfword binary'
        start = ET.SubElement(argument, 'start').text = "0"
        end = ET.SubElement(argument, 'end').text = "32767"

        argument = ET.SubElement(root, 'argument', name='LOGMESSAGE')
        value = ET.SubElement(argument, 'value').text = 'cvda'
        cvda = ET.SubElement(argument, 'cvda', default='YES').text = 'LOG'
        cvda = ET.SubElement(argument, 'cvda').text = 'NOLOG'


        pattern = re.compile(r"[A-Z]*[-]*\([-]*[a-z0-9]+\-?[a-z0-9]+[-]*\)")
        option_list = []
        for option in pattern.findall(text):
            temp_option = option
            if temp_option in option_list:
                continue
            else:
                option_list.append(temp_option)

        if str(self.resource).upper()+'(data-value)' in option_list:
            option_list.remove(str(self.resource).upper()+'(data-value)')
        if 'ATTRLEN(data-value)' in option_list:
            option_list.remove('ATTRLEN(data-value)')
        if 'ATTRIBUTES(data-area)' in option_list:
            option_list.remove('ATTRIBUTES(data-area)')
        if 'ATTRIBUTES(data-value)' in option_list:
            option_list.remove('ATTRIBUTES(data-value)')
        if 'LOGMESSAGE(cvda)' in option_list:
            option_list.remove('LOGMESSAGE(cvda)')
        #print(option_list, len(option_list))
        '''
        for option in option_list:
            option_name = (option.split('(')[0])
            option_value = option.split('(')[1].split(')')[0]
            #print(option_name, option_value)
            if 'char' in option_value:
                length = str(option_value).split('char')[1]
                #print(option_name, length)
                argument = ET.SubElement(root, 'argument', name=option_name)
                value = ET.SubElement(argument, 'value').text = 'data-value'
                type = ET.SubElement(argument, 'type').text = 'Character'
                length = ET.SubElement(argument, 'length').text = str(length)
            elif '-' in option_value:
                start = str(option_value).split('-')[0]
                end = str(option_value).split('-')[1]
                #print(option_name, start, end)
                argument = ET.SubElement(root, 'argument', name=option_name)
                value = ET.SubElement(argument, 'value').text = 'data-value'
                type = ET.SubElement(argument, 'type').text = 'Fullword binary'
                ET.SubElement(argument, 'start').text = str(start)
                ET.SubElement(argument, 'end').text = str(end)
            else:
                pass
            '''

        self.indent(root)
        tree = ET.ElementTree(root)
        xml_file = output_xml.format(self.systemcommand)
        tree.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")
        return

    def get_resource_size(self, resource):
        if 'tranclass':
            return 8
        if 'profile':
            return 8
        if 'partitionset':
            return 8
        if 'stream_name_template': # p.Resource Definition Guide 147
            return 26
        if 'jvmprofile': # p.Resource Definition Guide 204
            return 8
        if 'pipelinename':
            return 8

    def is_resource_in_list(self, list):
        if 'tranclass' in list:
            return 8
        if 'profile' in list:
            return 8
        if 'partitionset' in list:
            return 8

        return False

    def is_ddmmss_in_list(self, list):
        if 'dd,hh,mm' in list:
        #if (str(list[-1]) == 'dd,hh,mm'):
            return True
        return False

    def is_hhmmss_in_list(self, list):
        if 'hhmmss' in list:
        #if str(list[1]) == 'hhmmss':
            return True
        return False

    def is_mmss_in_list(self, list):
        if 'mmss' in list:
        #if str(list[1]) == 'mmss':
            return True
        return False

    def is_digit_in_list(self, list):
        if str(list[0]).isdigit():
            return True
        return False

    def is_length_in_list(self, list):
        if 'length' in list:
            return True
        return False

    def is_dsname_in_list(self, list):
        if 'dsname' in list:
            return True
        return False

    def is_seconds_in_list(self, list):
        if 'seconds' in list:
            return True
        return False

    def get_option_list(self, list):
        option_list = []

        for element in list:
            if re.search(r'\(', element):
                option_list.append(element)

        return  option_list

    def gen_xml5(self):
        fname = output_syntax_resource.format(self.systemcommand)
        f = open(fname, mode='r', encoding='utf-8')
        text = f.read()

        page = urlopen(self.resourcedefintionurl).read()
        self.soup = BeautifulSoup(page)

        option_list = []
        for span in self.soup.find_all("span", class_="ph synph") :
            if span.find_all("span", class_='keyword kwd'):
                option_list.append(span.text)

        option_list = self.get_option_list(option_list)
        description_list = self.get_description_list(text, option_list)

        #print(option_list, len(option_list))
        fname = output_syntax.format(self.systemcommand)
        f = open(fname, mode='r', encoding='utf-8')
        text = f.read()
        pattern = re.compile(r"[A-Z]*[-]*\([-]*[a-z0-9]+\-?[a-z0-9]+[-]*\)")
        temp_option_list1 = [] #
        temp_option_list2 = [] #
        for option in pattern.findall(text):
            temp_option = option
            if temp_option in temp_option_list1:
                continue
            else:
                temp_option_list1.append(temp_option)
                temp_option_list2.append(temp_option.split('(')[0])
        ###

        xml_file = output_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        for (option, description) in zip(option_list, description_list):

            if Counter(option)['(']:
                #print('Counter : ', option)
                argument_name, argument_value = option.split('(')[0], option.split('(')[1].split(')')[0]
            else:
                #print('error : ', option)
                continue

            if argument_name in temp_option_list2:
                index = temp_option_list2.index(argument_name)
                option = temp_option_list1[index]
                option_name = (option.split('(')[0])
                option_value = option.split('(')[1].split(')')[0]
                #print(option_name, option_value)
                if option_name == str(self.resource).upper():
                    continue

                if 'char' in option_value:
                    length = str(option_value).split('char')[1]
                    #print(option_name, length)
                    argument = ET.SubElement(root, 'argument', name=option_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'
                    type = ET.SubElement(argument, 'type').text = 'Character'
                    length = ET.SubElement(argument, 'length').text = str(length)
                    continue
                elif 'hex' in option_value:
                    length = str(option_value).split('hex')[1]
                    #print(option_name, length)
                    argument = ET.SubElement(root, 'argument', name=option_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'
                    type = ET.SubElement(argument, 'type').text = 'Character'
                    length = ET.SubElement(argument, 'length').text = str(length)
                    continue
                elif '-' in option_value:
                    start = str(option_value).split('-')[0]
                    end = str(option_value).split('-')[1]
                    #print(option_name, start, end)
                    argument = ET.SubElement(root, 'argument', name=option_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'
                    type = ET.SubElement(argument, 'type').text = 'Fullword binary'
                    ET.SubElement(argument, 'start').text = str(start)
                    ET.SubElement(argument, 'end').text = str(end)
                    ET.SubElement(argument, 'default').text = str(start)
                    continue
                else:
                    pass

            if Counter(argument_value)['{']:
                keyword = argument_value.split('{')[1].split('}')[0].split('|')
                # print(keyword)
                if Counter(keyword)['number']:
                    argument = ET.SubElement(root, 'argument', name=argument_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'

                    for i, word in zip(range(0, len(keyword)), keyword):
                        if i == 0:
                            type = ET.SubElement(argument, 'type').text = 'Fullword binary'
                            default = ET.SubElement(argument, 'default').text = word

                elif self.is_digit_in_list(keyword): #halfword
                    #print(argument_name, keyword)
                    argument = ET.SubElement(root, 'argument', name=argument_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'

                    for i, word in zip(range(0, len(keyword)), keyword):
                        if i == 0:
                            type = ET.SubElement(argument, 'type').text = 'Fullword binary'
                            default = ET.SubElement(argument, 'default').text = word

                elif self.is_resource_in_list(keyword):
                    argument = ET.SubElement(root, 'argument', name=argument_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'
                    type = ET.SubElement(argument, 'type').text = 'Character'
                    length = ET.SubElement(argument, 'length').text = str(self.get_resource_size(keyword))


                elif self.is_hhmmss_in_list(keyword): # ['NO', 'hhmmss']
                    argument = ET.SubElement(root, 'argument', name=argument_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'
                    type = ET.SubElement(argument, 'type').text = 'Character'
                    length = ET.SubElement(argument, 'length').text = '8'
                    default = ET.SubElement(argument, 'default').text  = 'NO'

                elif self.is_mmss_in_list(keyword): # ['NO', 'mmss']
                    argument = ET.SubElement(root, 'argument', name=argument_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'
                    type = ET.SubElement(argument, 'type').text = 'Character'
                    length = ET.SubElement(argument, 'length').text = '4'
                    default = ET.SubElement(argument, 'default').text = 'NO'

                elif self.is_ddmmss_in_list(keyword): # ['00,00,00', '00,00,10', 'dd,hh,mm']
                    argument = ET.SubElement(root, 'argument', name=argument_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'
                    type = ET.SubElement(argument, 'type').text = 'Character'
                    length = ET.SubElement(argument, 'length').text = '10'

                elif self.is_seconds_in_list(keyword): # ['NO', 'seconds']
                    argument = ET.SubElement(root, 'argument', name=argument_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'
                    type = ET.SubElement(argument, 'type').text = 'Fullword binary'

                elif self.is_length_in_list(keyword): # {length}
                    argument = ET.SubElement(root, 'argument', name=argument_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'
                    type = ET.SubElement(argument, 'type').text = 'Fullword binary'
                    if re.search('the range', description):
                        start = (str(description).split(pattern_range)[1].split())
                        end = str(start[2]).replace(".", "")
                        ET.SubElement(argument, 'start').text = str(start[0])
                        ET.SubElement(argument, 'end').text = str(end)

                elif self.is_dsname_in_list(keyword):
                    argument = ET.SubElement(root, 'argument', name=argument_name)
                    value = ET.SubElement(argument, 'value').text = 'data-value'
                    type = ET.SubElement(argument, 'type').text = 'Character'
                    length = ET.SubElement(argument, 'length').text = '44'

                else: #cvda
                    argument = ET.SubElement(root, 'argument', name=argument_name)
                    value = ET.SubElement(argument, 'value').text = 'cvda'

                    for i, word in zip(range(0, len(keyword)), keyword):
                        if i == 0:
                            cvda = ET.SubElement(argument, 'cvda', default='YES').text = word
                        else:
                            cvda = ET.SubElement(argument, 'cvda').text = word

            else:
                if argument_name.lower() == str(self.resource).lower(): # 리소스는 제외
                    '''
                    if re.search(pattern_character255, description):
                        length = ET.SubElement(argument, 'length').text = '255'
                    elif re.search(pattern_character255_1, description):
                        length = ET.SubElement(argument, 'length').text = '255'
                    elif re.search(pattern_character58, description):
                        length = ET.SubElement(argument, 'length').text = '58'
                    elif re.search(pattern_character44, description):
                        length = ET.SubElement(argument, 'length').text = '44'
                    elif re.search(pattern_character32_1, description):
                        length = ET.SubElement(argument, 'length').text = '32'
                    elif re.search(pattern_character32, description):
                        length = ET.SubElement(argument, 'length').text = '32'
                    elif re.search(pattern_character16_1, description):
                        length = ET.SubElement(argument, 'length').text = '16'
                    elif re.search(pattern_character16, description):
                        length = ET.SubElement(argument, 'length').text = '16'
                    elif re.search(pattern_character8_2, description):
                        length = ET.SubElement(argument, 'length').text = '8'
                    elif re.search(pattern_character8_1, description):
                        length = ET.SubElement(argument, 'length').text = '8'
                    elif re.search(pattern_character8, description):
                        length = ET.SubElement(argument, 'length').text = '8'
                    elif re.search(pattern_character4, description):
                        length = ET.SubElement(argument, 'length').text = '4'
                    elif re.search(pattern_character4_1, description):
                        length = ET.SubElement(argument, 'length').text = '4'
                    elif re.search(pattern_character4_2, description):
                        length = ET.SubElement(argument, 'length').text = '4'
                    else:
                        print('error : ', argument_name, argument_value)
                    '''

                else:
                    if argument_value == 'number':
                        argument = ET.SubElement(root, 'argument', name=argument_name)
                        value = ET.SubElement(argument, 'value').text = 'data-value'
                        type = ET.SubElement(argument, 'type').text = 'Fullword binary'
                        if re.search('the range', description):
                            start = (str(description).split(pattern_range)[1].split())
                            end = str(start[2]).replace(".", "")
                            ET.SubElement(argument, 'start').text = str(start[0])
                            ET.SubElement(argument, 'end').text = str(end)
                            #self.add_data_type(option.split('(')[0], 'Fullword binary', start=temp[0], end=temp_end)

                    elif argument_name == 'SOLICITED':
                        argument = ET.SubElement(root, 'argument', name=argument_name)
                        value = ET.SubElement(argument, 'value').text = 'cvda'
                        cvda = ET.SubElement(argument, 'cvda', default='YES').text = 'NO'
                        cvda = ET.SubElement(argument, 'cvda').text = 'YES'

                    elif argument_name == 'VALIDATION':
                        argument = ET.SubElement(root, 'argument', name=argument_name)
                        value = ET.SubElement(argument, 'value').text = 'cvda'
                        cvda = ET.SubElement(argument, 'cvda', default='YES').text = 'NO'
                        cvda = ET.SubElement(argument, 'cvda').text = 'YES'

                    else:
                        argument = ET.SubElement(root, 'argument', name=argument_name)

                        value = ET.SubElement(argument, 'value').text = 'data-value'
                        type = ET.SubElement(argument, 'type').text = 'Character'

                        if re.search(pattern_character255, description):
                            length = ET.SubElement(argument, 'length').text = '255'
                        elif re.search(pattern_character255_1, description):
                            length = ET.SubElement(argument, 'length').text = '255'
                        elif re.search(pattern_character58, description):
                            length = ET.SubElement(argument, 'length').text = '58'
                        elif re.search(pattern_character44, description):
                            length = ET.SubElement(argument, 'length').text = '44'
                        elif re.search(pattern_character32_1, description):
                            length = ET.SubElement(argument, 'length').text = '32'
                        elif re.search(pattern_character32, description):
                            length = ET.SubElement(argument, 'length').text = '32'
                        elif re.search(pattern_character16_1, description):
                            length = ET.SubElement(argument, 'length').text = '16'
                        elif re.search(pattern_character16, description):
                            length = ET.SubElement(argument, 'length').text = '16'
                        elif re.search(pattern_character8_2, description):
                            length = ET.SubElement(argument, 'length').text = '8'
                        elif re.search(pattern_character8_1, description):
                            length = ET.SubElement(argument, 'length').text = '8'
                        elif re.search(pattern_character8, description):
                            length = ET.SubElement(argument, 'length').text = '8'
                        elif re.search(pattern_character4, description):
                            length = ET.SubElement(argument, 'length').text = '4'
                        elif re.search(pattern_character4_1, description):
                            length = ET.SubElement(argument, 'length').text = '4'
                        elif re.search(pattern_character4_2, description):
                            length = ET.SubElement(argument, 'length').text = '4'
                        else:
                            '''
                            예외처리하기
                            '''
                            if argument_name == 'CFDTPOOL':
                                length = ET.SubElement(argument, 'length').text = '8'
                            elif argument_name == 'SECURITYNAME':
                                length = ET.SubElement(argument, 'length').text = '8'
                            elif argument_name == 'JVMCLASS':
                                length = ET.SubElement(argument, 'length').text = '255'
                            elif argument_name == 'REMOTENAME':
                                length = ET.SubElement(argument, 'length').text = '8'
                            elif argument_name == 'REMOTESYSTEM':
                                length = ET.SubElement(argument, 'length').text = '8'
                            elif argument_name == 'TRANSID':
                                length = ET.SubElement(argument, 'length').text = '4'
                            elif argument_name == 'INDIRECTNAME':
                                length = ET.SubElement(argument, 'length').text = '4'
                            elif argument_name == 'NATLANG':
                                length = ET.SubElement(argument, 'length').text = '1'
                            elif argument_name == 'SECURITYNAME':
                                length = ET.SubElement(argument, 'length').text = '8'
                            elif argument_name == 'DEVICE':
                                length = ET.SubElement(argument, 'length').text = '8'
                            elif argument_name == 'SESSIONTYPE':
                                length = ET.SubElement(argument, 'length').text = '8'
                            elif argument_name == 'PIPELINE':
                                length = ET.SubElement(argument, 'length').text = '8'
                            else:
                                print('error : ', argument_name, argument_value)

        self.indent(root)
        tree = ET.ElementTree(root)
        xml_file = output_xml.format(self.systemcommand)
        tree.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")
        return

    def sortchildrenby(self, parent, attr):
        parent[:] = sorted(parent, key=lambda child: child.get(attr))

    def gen_xml6(self):
        # sort
        xml_file = output_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        self.sortchildrenby(root, 'name')
        for child in root:
            self.sortchildrenby(child, 'name')

        self.indent(root)
        tree = ET.ElementTree(root)
        xml_file = output_xml.format(self.systemcommand)
        tree.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")
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

        #print(option_list)

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
                '''
                예외처리해주기
                '''
                if argument_name == 'DATASET':
                    type =  ET.SubElement(argument, 'type').text = 'Character'
                    length = ET.SubElement(argument, 'length').text = '44'
                if argument_name == 'CFDTPOOL':
                    type =  ET.SubElement(argument, 'type').text = 'Character'
                    length = ET.SubElement(argument, 'length').text = '44'
                if argument_name == 'OBJECTNAME':
                    type =  ET.SubElement(argument, 'type').text = 'Character'
                    length = ET.SubElement(argument, 'length').text = '44'
            elif argument_value == 'ptrref':
                value = ET.SubElement(argument, 'value').text = 'ptr-ref'
            elif argument_value == 'ptrvalue':
                value = ET.SubElement(argument, 'value').text = 'ptr-value'
            elif argument_value == 'cvda':
                value = ET.SubElement(argument, 'value').text = 'cvda'

            '''
            Data types : Doubleword binary(8), Fullword binary(4), Halfword binary(2)
                         Packed decimal(), Charcter string
            '''
            # ET.SubElement(argument, 'type')

            '''
            Character
            '''
            #ET.SubElement(argument, 'length')

            '''
            '''

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


    def add_cvda(self, argument_name, cvda_value):
        xml_file = output_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)

        root = xml.getroot()

        for argument in root.findall('argument'):
            if (argument.attrib["name"] == argument_name) :
                cvda = ET.SubElement(argument, "cvda")
                cvda.text = cvda_value

        self.indent(root)
        xml.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")

    def add_resp(self, argument_name, resp_item):
        xml_file = output_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)

        root = xml.getroot()

        flag = 0
        for argument in root.findall('argument'):
            if (argument.attrib["name"] == argument_name) :

                for resp in argument.findall('resp1'):
                    if resp:
                        if (resp.text == resp_item[0]):
                            resp2 = ET.SubElement(resp, "resp2")
                            resp2.text = str(resp_item[1])
                            resp2.attrib["description"] = str(resp_item[2]).replace('\n', ' ')
                            flag = 1
                        else:
                            pass
                    else: # resp가 없으면
                        pass
                if (flag == 0):
                    resp1 = ET.SubElement(argument, "resp1")
                    resp1.text = resp_item[0]
                    resp2 = ET.SubElement(resp1, "resp2")
                    resp2.text = str(resp_item[1])
                    resp2.attrib["description"] = str(resp_item[2]).replace('\n', ' ')

        self.indent(root)
        xml.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")

    def add_data_type(self, argument_name, data_type, length = 0, start = 0, end = 0):
        xml_file = output_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)

        root = xml.getroot()

        for argument in root.findall('argument'):
            if (argument.attrib['name'] == argument_name) :
                ET.SubElement(argument, 'type').text = data_type
                if(data_type == 'Character'):
                    ET.SubElement(argument, 'length').text = str(length)
                elif(data_type == 'digit'):
                    if (length != 0):
                        ET.SubElement(argument, 'length').text = str(length)
                elif(data_type == 'Fullword binary'):
                    if (start != 0):
                        ET.SubElement(argument, 'start').text = str(start)
                    if (end != 0):
                        ET.SubElement(argument, 'end').text = str(end)

        self.indent(root)
        xml.write(xml_file, xml_declaration=True, encoding='utf-8', method="xml")

    '''
    copy and paste from http://effbot.org/zone/element-lib.htm#prettyprint
    it basically walks your tree and adds spaces and newlines so the tree is
    printed in a nice way
    '''
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

    def gen_xml3(self):
        try:
            fname = output_syntax_full.format(self.systemcommand)
            f = open(fname , mode='r', encoding='utf-8')
            data = str(f.read()).split('Description')[1].split('Conditions')[0]
            f.close()
        except:
            print('Error: ' + self.resource + 'gen_xml3')
            return

        pattern = re.compile(r"[A-Z]+\([a-z]+\-?[a-z]+\)")
        option_list = pattern.findall(data)     # APIST(cvda) 형태로
        description_list = self.get_description_list(data, option_list)

        for (option, description) in zip(option_list, description_list):
            # print(option, description)
            if re.search('cvda', option):
                pass
            elif re.search(pattern_doubleword, description) :
                if re.search(pattern_range, description) :
                    temp = (str(description).split(pattern_range)[1].split())
                    temp_end = str(temp[2]).replace(".", "")
                    self.add_data_type(option.split('(')[0], 'Doubleword binary', start=temp[0], end=temp_end)
                else:
                    self.add_data_type(option.split('(')[0], 'Doubleword binary')
            elif re.search(pattern_fullword, description) :
                if re.search(pattern_range, description) :

                    #print(description.split(pattern_range)[1])
                    temp = (str(description).split(pattern_range)[1].split())

                    #print(temp, type(temp))
                    if len(temp) > 1:
                        print(temp)
                        temp_end = str(temp[2])
                        if re.search(r'.', temp_end):
                            temp_end = str(temp[2]).replace(".", "")

                        if temp_end.isdigit():
                            pass
                        else:
                            if re.search(chr(8211), temp[0]):
                                temp = str(temp[0]).replace(".", "").split(chr(8211))
                                print(temp)
                                temp_end = (temp)[-1]

                                if temp_end.isdigit():
                                    pass
                                else:
                                    temp_end = str(temp)[-2]
                            else:
                                temp = str(temp[0]).replace(".", "").split('-')
                                print(temp)
                                temp_end = (temp)[-1]

                                if temp_end.isdigit():
                                    pass
                                else:
                                    temp_end = str(temp)[-2]

                    else: # 0 -255 로 된경우. 병신같은 경우임.
                        temp = str(temp[0]).replace(".", "").split(chr(8211))
                        # print(chr(8211), temp, type(temp))
                        temp_end = (temp)[-1]
                        if temp_end.isdigit():
                            pass
                        else:
                            temp_end = str(temp)[-2]


                    self.add_data_type(option.split('(')[0], 'Fullword binary', start=temp[0], end=temp_end)
                else:
                    self.add_data_type(option.split('(')[0], 'Fullword binary')
            elif re.search(pattern_fullword1, description) :
                if re.search(pattern_range, description) :
                    print(description)
                    temp = (str(description).split(pattern_range)[1].split())
                    #print(temp)
                    temp_end = str(temp[2]).replace(".", "")
                    self.add_data_type(option.split('(')[0], 'Fullword binary', start=temp[0], end=temp_end)
                else:
                    self.add_data_type(option.split('(')[0], 'Fullword binary')
            elif re.search(pattern_number1, description) :
                if re.search(pattern_range, description) :
                    temp = (str(description).split(pattern_range)[1].split())
                    temp_end = str(temp[2]).replace(".", "")
                    self.add_data_type(option.split('(')[0], 'Fullword binary', start=temp[0], end=temp_end)
                else:
                    self.add_data_type(option.split('(')[0], 'Fullword binary')
            elif re.search(pattern_length1, description) :
                if re.search(pattern_range, description) :
                    temp = (str(description).split(pattern_range)[1].split())
                    temp_end = str(temp[2]).replace(".", "")
                    self.add_data_type(option.split('(')[0], 'Fullword binary', start=temp[0], end=temp_end)
                else:
                    self.add_data_type(option.split('(')[0], 'Fullword binary')

            elif re.search(pattern_halfword, description) :
                self.add_data_type(option.split('(')[0], 'Halfword binary')

            elif re.search(pattern_character, description) :
                temp = (str(description).split('-character')[0].split())
                self.add_data_type(option.split('(')[0], 'Character', length=temp[-1])
            elif re.search(pattern_character255_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 255)
            elif re.search(pattern_character255, description) :
                self.add_data_type(option.split('(')[0], 'Character', 255)
            elif re.search(pattern_character58, description) :
                self.add_data_type(option.split('(')[0], 'Character', 58)
            elif re.search(pattern_character44_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 44)
            elif re.search(pattern_character44, description) :
                self.add_data_type(option.split('(')[0], 'Character', 44)
            elif re.search(pattern_character32_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 32)
            elif re.search(pattern_character32, description) :
                self.add_data_type(option.split('(')[0], 'Character', 32)
            elif re.search(pattern_character26_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 26)
            elif re.search(pattern_character26, description) :
                self.add_data_type(option.split('(')[0], 'Character', 26)
            elif re.search(pattern_character16_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 16)
            elif re.search(pattern_character16, description) :
                self.add_data_type(option.split('(')[0], 'Character', 16)
            elif re.search(pattern_character8_2, description) :
                self.add_data_type(option.split('(')[0], 'Character', 8)
            elif re.search(pattern_character8_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 8)
            elif re.search(pattern_character8, description) :
                self.add_data_type(option.split('(')[0], 'Character', 8)
            elif re.search(pattern_character5_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 5)
            elif re.search(pattern_character5, description) :
                self.add_data_type(option.split('(')[0], 'Character', 5)
            elif re.search(pattern_character4_2, description) :
                self.add_data_type(option.split('(')[0], 'Character', 4)
            elif re.search(pattern_character4_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 4)
            elif re.search(pattern_character4, description) :
                self.add_data_type(option.split('(')[0], 'Character', 4)
            elif re.search(pattern_character1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 1)
            elif re.search(pattern_character1_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 1)

            elif re.search(pattern_byte64, description) :
                self.add_data_type(option.split('(')[0], 'Character', 64)
            elif re.search(pattern_byte64_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 64)
            elif re.search(pattern_byte32, description) :
                self.add_data_type(option.split('(')[0], 'Character', 32)
            elif re.search(pattern_byte32_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 32)
            elif re.search(pattern_byte28, description) :
                self.add_data_type(option.split('(')[0], 'Character', 28)
            elif re.search(pattern_byte16, description) :
                self.add_data_type(option.split('(')[0], 'Character', 16)
            elif re.search(pattern_byte16_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 16)
            elif re.search(pattern_byte8, description) :
                self.add_data_type(option.split('(')[0], 'Character', 8)
            elif re.search(pattern_byte8_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 8)
            elif re.search(pattern_byte4, description) :
                self.add_data_type(option.split('(')[0], 'Character', 4)
            elif re.search(pattern_byte4_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 4)
            elif re.search(pattern_character3, description) :
                self.add_data_type(option.split('(')[0], 'Character', 3)
            elif re.search(pattern_character3_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 3)
            elif re.search(pattern_byte2, description) :
                self.add_data_type(option.split('(')[0], 'Character', 2)
            elif re.search(pattern_byte1_1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 1)
            elif re.search(pattern_byte1, description) :
                self.add_data_type(option.split('(')[0], 'Character', 1)
            elif re.search(pattern_digit, description) :
                temp = (str(description).split('-digit number')[0].split())
                self.add_data_type(option.split('(')[0], 'digit', length=temp[-1])
            elif re.search(pattern_abstime, description) :
                self.add_data_type(option.split('(')[0], 'ABSTIME')
            elif re.search(pattern_obsolete, description) :
                self.add_data_type(option.split('(')[0], 'obsolete')

            else :
                if option.split('(')[0] == 'POOLNAME':
                    self.add_data_type(option.split('(')[0], 'Character', 8)
                elif option.split('(')[0] == 'SYSID':
                    self.add_data_type(option.split('(')[0], 'Character', 8)
                elif option.split('(')[0] == 'TRANSID':
                    self.add_data_type(option.split('(')[0], 'Character', 4)
                elif option.split('(')[0] == 'CCSID':
                    self.add_data_type(option.split('(')[0], 'Character', 8)
                elif option.split('(')[0] == 'LASTUSEDINT':
                    self.add_data_type(option.split('(')[0], 'Fullword binary')
                else :
                    print("gen xml3 error " , option)

    def gen_xml_resp(self):
        page = urlopen(self.systemcommandurl).read()
        self.soup = BeautifulSoup(page)

        for div in self.soup.find_all('div', {'class' : 'section'}):
            if (div.h2):    # 값이 있는 경우
                if div.h2.text == 'Conditions':
                    conditions_div = div

        resp_list = []

        resp_item = []
        resp_item.append(conditions_div.dt.text)    # RESP1

        resp_item.append(conditions_div.dd.dt.text) # RESP2
        resp_item.append(conditions_div.dd.dd.text) # RESP description
        resp_list.append(resp_item)

        resp_item = []
        resp_item.append(conditions_div.dt.text)

        for resp2 in conditions_div.dd.dd.next_siblings:
            if(resp2.name == 'dd'):
                resp_item.append(resp2.text)
                resp_list.append(resp_item)
                resp_item = []
                resp_item.append(conditions_div.dt.text)
            if(resp2.name == 'dt'):
                resp_item.append(resp2.text)

        if (len(resp_item) == 3):
            resp_list.append(resp_item)

        resp1_list = []
        for resp1 in conditions_div.dt.next_siblings:
            if (resp1.name == 'dt'):
                resp1_list.append(resp1.text)

        i = 0
        for resp2 in conditions_div.dd.next_siblings:
            if(resp2.name == 'dd'):
                resp_item = []
                resp_item.append(resp1_list[i])

                resp_item.append(resp2.dt.text)
                resp_item.append(resp2.dd.text)

                resp_list.append(resp_item)

                resp_item = []
                for resp2val in resp2.dd.next_siblings:
                    if (resp2val.name == 'dd'):
                        resp_item.append(resp2val.text)
                        resp_list.append(resp_item)
                        resp_item = []
                    elif (resp2val.name == 'dt'):
                        resp_item.append(resp1_list[i])
                        resp_item.append(resp2val.text)
                i = i+1

        fname = output_resps.format(self.systemcommand)
        f = open(fname , mode='w', encoding='utf-8')
        for resp in resp_list:
            f.write(str(resp))
            f.write('\n')
        f.close()

        for resp in resp_list:
            if re.search(invalid_cvda1, resp[2]):
                arugument_name = str(resp[2]).split(invalid_cvda1)[0]
                self.add_resp(arugument_name, resp)
                pass
            elif re.search(invalid_cvda2, resp[2]):
                arugument_name = str(resp[2]).split(invalid_cvda2)[1].split(' option.')[0]
                self.add_resp(arugument_name, resp)
                pass
            elif re.search(invalid_option, resp[2]):
                arugument_name = str(resp[2]).split(invalid_option)[0].split('The ')[1]
                self.add_resp(arugument_name, resp)
                pass
            elif re.search(invalid_name, resp[2]):
                arugument_name = str(resp[2]).split(invalid_name)[0].split('An invalid ')[1]
                self.add_resp(arugument_name, resp)
                pass
            elif re.search(invalid_range1, resp[2]):
                arugument_name = str(resp[2]).split(invalid_range1)[0]
                self.add_resp(arugument_name, resp)
                pass
            elif re.search(invalid_range2, resp[2]):
                arugument_name = str(resp[2]).split(invalid_range2)[0]
                self.add_resp(arugument_name, resp)
                pass
            elif re.search(invalid_range3, resp[2]):
                arugument_name = str(resp[2]).split(invalid_range3)[1].split()[0]
                self.add_resp(arugument_name, resp)
                pass
            elif re.search(invaild_range4, resp[2]):
                arugument_name = str(resp[2]).split(invaild_range4)[0]
                self.add_resp(arugument_name, resp)
                pass
            elif re.search(invaild_range5, resp[2]):
                arugument_name = str(resp[2]).split(invaild_range5)[0]
                self.add_resp(arugument_name, resp)
                pass
            elif re.search(invlaid_specified1, resp[2]):
                arugument_name = str(resp[2]).split(invlaid_specified1)[0]
                self.add_resp(arugument_name, resp)
                pass
            elif re.search(invlaid_specified2, resp[2]):
                arugument_name = str(resp[2]).split(invlaid_specified2)[0]
                self.add_resp(arugument_name, resp)
                pass
            else:
                #print(resp[2])
                pass
            #print(resp)


    def get_description_list(self, data, option_list):

        description_list = []
        for i in range(0, len(option_list)):
            if i == 0 :
                description     = data.split(option_list[i])[1].split(option_list[i+1])[0]
                description_list.append(description.replace('\n', ' '))
                data            = data.split(option_list[i+1], 1)[1]
            elif i == (len(option_list) - 1) :
                description     = data
                description_list.append(description.replace('\n', ' '))
            else :
                description     = data.split(option_list[i+1], 1)[0]
                description_list.append(description.replace('\n', ' '))
                data            = data.split(option_list[i+1], 1)[1]
        return description_list

