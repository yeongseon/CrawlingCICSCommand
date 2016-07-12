from datetime import date
import re
import xml.etree.ElementTree as ET

default_url = 'http://www-01.ibm.com/support/knowledgecenter/api/content/nl/ko/SSGMCP_4.2.0/com.ibm.cics.ts.systemprogramming.doc/commands/dfha8_{}.html'

output_syntax_full = 'spi/output_syntax/{}_full.txt'
output_syntax = 'spi/output_syntax/{}.txt'
input_xml = 'spi/input_xml/{}.xml'

output_source = 'spi/output_code/osc_spi_create/osc_spi_{}_{}.c'
output_source_rtsd = 'spi/output_code/osc_spi_create/osc_spi_{}_{}_rtsd_temp.c'
output_header = 'spi/output_code/osc_spi_create/osc_spi_{}_{}.h'
output_local_header = 'spi/output_code/osc_spi_create/osc_spi_{}_{}_local.h'

class genCreate(object):
    def __init__(self, command, resource):
        self.prefix = 'osc_spi'
        self.command = command
        self.resource = resource
        self.systemcommand = self.command + self.resource

        self.outputsource = output_source.format(self.command, self.resource)
        self.outputsource_rtsd = output_source_rtsd.format(self.command, self.resource)
        self.outputheader = output_header.format(self.command, self.resource)
        self.outputlocalheader = output_local_header.format(self.command, self.resource)

        self.inputsyntaxfile = output_syntax.format(self.command + self.resource)
        self.inputsyntaxfullfile = output_syntax_full.format(self.command + self.resource)


    def fopen(self):
        self.osource = open(self.outputsource, mode = 'w', encoding='utf-8')
        self.osource_rtsd = open(self.outputsource_rtsd, mode = 'w', encoding='utf-8')
        return

    def fclose(self):
        self.osource.close()
        self.osource_rtsd.close()
        return

    def printDefine(self):
        self.oheader = open(self.outputheader, mode = 'w', encoding='utf-8')
        self.oheader.write('/**\n'
                           ' * @brief Initialize the ' + self.command + ' ' + self.resource + ' command.\n'
                           ' * @return zero on success\n'
                           ' */\n'
                           'extern int ' + self.prefix + '_' + self.command + '_' + self.resource + '_' + 'init();\n\n'
                           )

        self.oheader.write('/**\n'
                           ' * @brief Set the options to the ' + self.command + ' ' + self.resource + ' command.\n'
                           ' * @param[in] _option\n'
                           ' * @param[in] _argument\n'
                           ' * @param[out] _resp1 RESP1\n'
                           ' * @param[out] _resp2 RESP2\n'
                           ' * @return zero on success\n'
                           ' */\n'
                           'extern int ' + self.prefix + '_' + self.command + '_' + self.resource + '_' + 'set_option' +
                           '(char *_option, void *_argument, int *_resp1, int *_resp2);\n\n'
                           )

        self.oheader.write('/**\n'
                           ' * @brief Execute the ' + self.command + ' ' + self.resource + ' command.\n'
                           ' * @param[out] _resp1 RESP1\n'
                           ' * @param[out] _resp2 RESP2\n'
                           ' * @return zero on success\n'
                           ' */\n'
                           'extern int ' + self.prefix + '_' + self.command + '_' + self.resource +
                           '(int *_resp1, int *_resp2);\n\n'
                           )

        self.oheader.write('/**\n'
                           ' * @brief Finalize the ' + self.command + ' ' + self.resource + ' command.\n'
                           ' * @return zero on success\n'
                           ' */\n'
                           'extern int ' + self.prefix + '_' + self.command + '_' + self.resource + '_' + 'done();\n\n'
                           )

        self.oheader.close()
        return

    def printComment(self):
        today = date.today()

        inputfile = open(self.inputsyntaxfile, mode = 'r', encoding='utf-8')

        self.osource.write('/**\n'
                           ' * @file ' + self.prefix + '_' + self.command + '_' + self.resource + '.c\n'
                           ' * @brief \n')

        for line in inputfile.readlines():
            self.osource.write(' * ' + line)

        self.osource.write(' * Reference: \n'
                           ' * ' + default_url.format(self.systemcommand) + '\n'
                           ' *\n'
                           ' * @date ' + today.strftime('%Y. %m. %d') + '\n'
                           ' * @author Yeongseon Choe <yeongseon_choe@tmax.co.kr>\n'
                           '*/\n'
                           '\n'
                           )

    def printHeader(self):
        self.osource.write('#include "osc/include/osc_spi.h"\n'
                           '\n'
                           '#include <stdio.h>\n'
                           '#include <stdlib.h>\n'
                           '#include <string.h>\n'
                           '\n'
                           '#include "osc/cicsinc/cics_cvda.h" /* for cvda value */\n'
                           '#include "osc/cicsinc/cics_err.h" /* for cics errcode */\n'
                           '#include "osc/cicsinc/cics_size.h" /* for cics size */\n'
                           '#include "osc/include/cics_rtsd.h" /* for cics_rtsd */\n'
                           '#include "osc/errcode/errcode_osc.h" /* for osc errcode */\n'
                           '\n'
                           '#include "osc/lib/oscspi/osc_spi_local.h" /* for internal function */\n'
                           '\n'
                           )
        return

    def printStruct(self):
        self.olhearder = open(self.outputlocalheader, mode = 'w', encoding='utf-8')

        self.olhearder.write('enum ' + self.command + '_' + self.resource + '_flag_type {\n'
                             '\t' + self.command.upper() + '_' + self.resource.upper() + '_FLAG_' +  self.resource.upper() +' = 0,\n'
                             )

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text
            if str(name).upper() != str(self.resource).upper() :
                    self.olhearder.write('\t' + self.command.upper() + '_' + self.resource.upper() + '_FLAG_' + str(name).upper() +',\n')


        self.olhearder.write('};\n'
                             '\n'
                             )

        self.olhearder.write('typedef struct osc_spi_' + self.command + '_' + self.resource + '_options_s {\n'
                             '\tchar ' + self.resource + '[CICS_' + self.resource.upper() + '_SIZE];\n'
                             )

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()


        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if str(name).upper() != str(self.resource).upper():
                if value == 'cvda' :
                    self.olhearder.write('\tint32_t ' + name.lower() + '; /* CVDA */\n')
                elif value == 'Character':
                    self.olhearder.write('\tchar ' + name.lower() + '[CICS_' + name.upper() + '_SIZE]; /* Character */\n')
                elif value == 'data-area' :
                    type = argument.find('type').text
                    if type == 'Character':
                        self.olhearder.write('\tchar ' + name.lower() + '[CICS_' + name.upper() + '_SIZE]; /* Character */\n')
                    elif type == 'Halfword binary':
                        self.olhearder.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')
                    elif type == 'Fullword binary':
                        self.olhearder.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')
                    else:
                        self.olhearder.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')
                elif value == 'data-value':
                    type = argument.find('type').text
                    if type == 'Character':
                        self.olhearder.write('\tchar ' + name.lower() + '[CICS_' + name.upper() + '_SIZE]; /* Character */\n')
                    elif type == 'Halfword binary':
                        self.olhearder.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')
                    elif type == 'Fullword binary':
                        self.olhearder.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')
                    else:
                        self.olhearder.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')
                else:
                    self.olhearder.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')

        self.olhearder.write('\tint32_t flag[' + str(len(root.findall('argument')) + 1) + '];\n'
                             '} osc_spi_' + self.command + '_' + self.resource + '_options_t;\n'
                             )
        self.olhearder.close()

    def printGlobalVariable(self):
        var = 'char\t' + self.resource + '[CICS_' + self.resource.upper() + '_SIZE];'
        self.osource.write(self.prefix + '_' + self.command + '_' + self.resource + '_options_t ' +
                           self.command + '_' + self.resource+ '_options;\n'
                           )
        self.osource.write('\n')
        return

    def printInitFunction(self):
        functionname = self.prefix + '_' + self.command + '_' + self.resource + '_init()'
        self.osource.write('int\t' + functionname + ' {\n'
                           '\tint\trc = 0;\n'
                           )
        self.osource.write('\tmemset(&' + self.command + '_' + self.resource + '_options, ' +
                           '0x00, sizeof(' + self.command + '_' + self.resource + '_options));\n')
        self.osource.write('\treturn rc;\n'
                           '}\n'
                           '\n'
                           )
        return

    def printSetFunction(self):
        functionname = self.prefix + '_' + self.command + '_' + self.resource + \
                       '_set_option(char *_option, void *_argument, int *_resp1, int *_resp2)'
        self.osource.write('int\t' + functionname + ' {\n'
                           '\tint\trc = 0;\n'
                           '\n'
                           )

        self.osource.write('\tif(strcmp(_option, "' + self.resource + '") == 0 ) {\n'
                           '\t\tmemcpy(' + self.command + '_' + self.resource + '_options.' + self.resource +
                           ', (char *) _argument, CICS_' + self.resource.upper() + '_SIZE);\n'
                           '\t\t' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_' + self.resource.upper() + '] = OSC_SPI_TRUE;\n'
                           )

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if str(name).upper() != str(self.resource).upper() :
                self.osource.write('\t} else if (strcmp(_option, "' + str(name).lower() + '") == 0) {\n'
                #                   '\t\t/* Not supported. */\n'
                #                   '\t\t' + self.command + '_' + self.resource + '_options.flag[' +
                #                    self.command.upper() + '_' + self.resource.upper() + '_FLAG_' + str(name).upper() + '] = OSC_SPI_FALSE;\n'
                #                    '\t\treturn OSC_ERR_SPI_NOT_SUPPORTED;\n'
                                   )

                self.osource.write('\t\t' + self.command + '_' + self.resource + '_options.flag[' +
                                       self.command.upper() + '_' + self.resource.upper() + '_FLAG_' + str(name).upper() + '] = OSC_SPI_TRUE;\n'
                                   )
                if str(value) == 'cvda':
                    i = 0
                    self.osource.write('\n\t\tint32_t cvda = *(int32_t *)_argument;\n')
                    for cvda in argument.findall('cvda'):
                        cvda_value = cvda.text
                        if i == 0 :
                            self.osource.write('\t\tif (cvda == CVDA_' + str(cvda_value).upper() + ') {\n')
                            i = i+1
                        else :
                            self.osource.write('\t\t} else if (cvda == CVDA_' + str(cvda_value).upper() + ') {\n')
                            i = i+1

                    self.osource.write('\t\t} else {\n'
                                       '\t\t\t*_resp1 = CICS_ERR_ERROR;\n'
                                       '\t\t\t*_resp2 = 0;\n'
                                       '\t\t\treturn OSC_ERR_SPI_ERROR;\n'
                                       '\t\t}\n'
                                       )
                elif str(value) == 'data-value':
                    type = argument.find('type').text
                    if type == 'Character':
                        self.osource.write('\t\tmemcpy(' + self.command + '_' + self.resource + '_options.' + str(name).lower() +
                                       ', (char *) _argument, CICS_' + str(name).upper() + '_SIZE);\n')

                    elif type == 'Fullword binary':
                        self.osource.write('\n\t\tint32_t ' + str(name).lower() + '= *(int32_t *)_argument;\n')

                        if argument.find('start'):
                            start = argument.find('start').text
                            continue
                        if argument.find('end'):
                            end = argument.find('end').text
                            continue
                        self.osource.write('\t\tif(' +  str(name).lower() + ' < ' + str(start) + ' && ' +
                                           str(name).lower() + ' > ' + str(end) + ') {\n' +
                                           '\t\t\t\t*_resp1 = CICS_ERR_INVREQ;\n' +
                                           '\t\t\t\t*_resp2 = 0;\n' +
                                           '\t\t\t\treturn OSC_ERR_SPI_INVREQ;\n' +
                                           '\t\t}\n')

                    elif type == 'Halfword binary':
                        self.osource.write('\n\t\tint32_t ' + str(name).lower() + '= *(int32_t *)_argument;\n')
                        #if argument.find('start'):
                        start = argument.find('start').text
                        #    continue
                        #if argument.find('end'):
                        end = argument.find('end').text
                        #    continue
                        self.osource.write('\t\tif(' +  str(name).lower() + ' < ' + str(start) + ' && ' +
                                           str(name).lower() + ' > ' + str(end) + ') {\n' +
                                           '\t\t\t\t*_resp1 = CICS_ERR_INVREQ;\n' +
                                           '\t\t\t\t*_resp2 = 0;\n' +
                                           '\t\t\t\treturn OSC_ERR_SPI_INVREQ;\n' +
                                           '\t\t}\n')

                else:
                    self.osource.write('\t\tmemcpy(&' + self.command + '_' + self.resource + '_options.' + str(name).lower() +
                                       ', (int32_t *) _argument, sizeof(int32_t));\n')



        self.osource.write('\t} else {\n')
        self.osource.write('\t\t*_resp1 = CICS_ERR_ERROR;\n')
        self.osource.write('\t\t*_resp2 = 0;\n')
        self.osource.write('\t\treturn OSC_ERR_SPI_ERROR;\n')
        self.osource.write('\t}\n')

        self.osource.write('\treturn rc;\n'
                           '}\n'
                           '\n'
                           )
        return

    def printExecuteFunction(self):
        self.osource_rtsd.write('#include "osc/include/osc_spi.h"\n'
                               '\n'
                               '#include <stdio.h>\n'
                               '#include <stdlib.h>\n'
                               '#include <string.h>\n'
                               '\n'
                               '#include "osc/cicsinc/cics_cvda.h" /* for cvda value */\n'
                               '#include "osc/cicsinc/cics_err.h" /* for cics errcode */\n'
                               '#include "osc/cicsinc/cics_size.h" /* for cics size */\n'
                               '#include "osc/include/cics_rtsd.h" /* for cics_rtsd */\n'
                               '#include "osc/errcode/errcode_osc.h" /* for osc errcode */\n'
                               '\n'
                               '#include "osc/lib/oscspi/osc_spi_local.h" /* for internal function */\n'
                               '\n'
                               )

        self.osource_rtsd.write(
                    'extern ' + self.prefix + '_' + self.command + '_' + self.resource + '_options_t ' +
                   self.command + '_' + self.resource+ '_options;\n\n'
                   )
        functionname = self.prefix + '_' + self.command + '_' + self.resource + '(int *_resp1, int *_resp2)'
        self.osource_rtsd.write('int\t' + functionname + ' {\n'
                           '\tint\trc = 0;\n'
                           '\tint\tis_rtsd = 0;\n'
                           '\tcics_rtsd_' + self.resource + '_t rtsd_' + self.resource + ';\n'
                           '\n'
                           )

        self.osource_rtsd.write('\trc = cics_rtsd_read(' + 'CICS_RTSD_' + self.resource.upper() + ', ' +
                           self.command + '_' + self.resource + '_options.' + self.resource + ', &rtsd_' + self.resource + ', 0);\n'
                           '\tif (rc == OSC_ERR_RTSD_NOT_FOUND) {\n'
                           '\t\tis_rtsd = 0;\n'
                           '\t} else if (rc > 0) {\n'
                           '\t\tis_rtsd = 1;\n'
                           '\t} else if (rc < 0) {\n'
                           '\t\t*_resp1 = CICS_ERR_ERROR;\n'
                           '\t\t*_resp2 = 0;\n'
                           '\t\treturn OSC_ERR_SPI_ERROR;\n'
                           '\t}\n'
                           '\n'
                                )

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        for argument in root.findall('argument'):
            name = argument.get('name')
            support = argument.get('support')

            value = argument.find('value').text

            if str(name).upper() != str(self.resource).upper() :
                    if str(support) == 'no':
                        self.osource_rtsd.write('\tif (' + self.command + '_' + self.resource + '_options.flag[' +
                                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_' + str(name).upper() + ']) {\n'
                                           '\t\t/* Not supported. */\n'
                                           '\t}\n'
                                           )
                    if str(support) == 'yes':
                        self.osource_rtsd.write('\tif (' + self.command + '_' + self.resource + '_options.flag[' +
                                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_' + str(name).upper() + ']) {\n'
                                            '\t\t/* TODO. */\n'
                                           '\t}\n'
                                            )

        self.osource_rtsd.write('\n')


        self.osource_rtsd.write(
                           '\tif (is_rtsd == 0) {\n'
                           '\t\trc = cics_rtsd_write(' + 'CICS_RTSD_' + self.resource.upper() + ', ' +
                           self.command + '_' + self.resource + '_options.' + self.resource + ', &rtsd_' + self.resource + ');\n'
                           '\t\tif (rc < 0) {\n'
                           '\t\t\t*_resp1 = CICS_ERR_ERROR;\n'
                           '\t\t\t*_resp2 = 0;\n'
                           '\t\t\treturn OSC_ERR_SPI_ERROR;\n'
                           '\t\t}\n'
                           '\t} else {\n'
                           '\t\trc = cics_rtsd_rewrite(' + 'CICS_RTSD_' + self.resource.upper() + ', ' +
                           self.command + '_' + self.resource + '_options.' + self.resource + ', &rtsd_' + self.resource + ');\n'
                           '\t\tif (rc < 0) {\n'
                           '\t\t\t*_resp1 = CICS_ERR_ERROR;\n'
                           '\t\t\t*_resp2 = 0;\n'
                           '\t\t\treturn OSC_ERR_SPI_ERROR;\n'
                           '\t\t}\n'
                           '\t}\n'
                            )

        self.osource_rtsd.write('\treturn rc;\n'
                           '}\n'
                           '\n'
                           )

        return

    def printDoneFunction(self):
        functionname = self.prefix + '_' + self.command + '_' + self.resource + '_done()'
        self.osource.write('int\t' + functionname + ' {\n'
                           '\tint\trc = 0;\n'
                           )
        self.osource.write('\tmemset(&' + self.command + '_' + self.resource + '_options, ' +
                           '0x00, sizeof(' + self.command + '_' + self.resource + '_options));\n')
        self.osource.write('\treturn rc;\n'
                           '}\n'
                           '\n'
                           )
        return