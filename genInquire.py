from datetime import date
import re
import xml.etree.ElementTree as ET

defult_url = 'http://www-01.ibm.com/support/knowledgecenter/api/content/nl/ko/SSGMCP_4.2.0/com.ibm.cics.ts.systemprogramming.doc/commands/dfha8_{}.html'

output_syntax_full = 'spi/output_syntax/{}_full.txt'
output_syntax = 'spi/output_syntax/{}.txt'
input_xml = 'spi/input_xml/{}.xml'

output_source = 'spi/output_code/{}/osc_spi_{}_{}.c'
output_source_rtsd = 'spi/output_code/{}/osc_spi_{}_{}_rtsd_temp.c'
output_header = 'spi/output_code/{}/osc_spi_{}_{}.h'
output_local_header = 'spi/output_code/{}/osc_spi_{}_{}_local.h'
output_rtsddump = 'spi/output_code/{}/oscrtsddump_dump_{}.c'
output_oscossvr = 'spi/output_code/{}/oscossvr_get_{}.c'
output_oscossvr_f = 'spi/output_code/{}/oscossvr_{}.f'
output_inquire_c = 'spi/output_code/cics_spi/cics_inquire_{}_temp.c'
output_inquire_h = 'spi/output_code/{}/cics_inquire_{}.h'
output_arg_h = 'spi/output_code/{}/cics_arg_inquire_{}.h'
output_cmmd_h = 'spi/output_code/{}/cics_cmmd_inquire_{}.h'
output_ecpi_c = 'spi/output_code/{}/cics_ecpi_inquire_{}.c'

class genInquire(object):
    def __init__(self, command, resource):
        self.prefix = 'osc_spi'
        self.command = command
        self.resource = resource
        self.systemcommand = self.command + self.resource
        self.outputsource = output_source.format(self.resource, self.command, self.resource)
        self.outputsource_rtsd = output_source_rtsd.format(self.resource, self.command, self.resource)
        self.outputheader = output_header.format(self.resource, self.command, self.resource)
        self.outputlocalheader = output_local_header.format(self.resource, self.command, self.resource)

        self.oscrtsddump = output_rtsddump.format('rtsddump', self.resource)

        self.oscossvr = output_oscossvr.format(self.resource, self.resource)
        self.oscossvr_f = output_oscossvr_f.format(self.resource, self.resource)
        self.inquire_c = output_inquire_c.format(self.resource)
        self.inquire_h = output_inquire_h.format(self.resource, self.resource)
        self.arg_h = output_arg_h.format(self.resource, self.resource)
        self.cmmd_h = output_cmmd_h.format(self.resource, self.resource)
        self.ecpi_c = output_ecpi_c.format(self.resource, self.resource)

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

    def printecpi_c(self):
        f = open(self.ecpi_c, mode = 'w', encoding='utf-8')

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        f.write(
            'cics_' + self.command + '_' + self.resource.lower() + '(eib, valflag, '
        )

        size = len(root.findall('argument'))

        count = 0
        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if value == 'data-value':
                f.write(
                    'arg[' + str(count) + '].dv_alphanumeric, '
                )
            elif value == 'data-area':
                type = argument.find('type').text

                if type == 'Character':
                    f.write(
                    'arg[' + str(count) + '].da_alphanumeric, '
                )
                elif type == 'Halfword binary':
                    f.write(
                    'arg[' + str(count) + '].da_int16, '
                )
                elif type == 'Fullword binary':
                    f.write(
                    'arg[' + str(count) + '].da_int32, '
                )
                elif type == 'ABSTIME':
                    f.write(
                    'arg[' + str(count) + '].da_char, '
                )
                else:
                    f.write(
                    'arg[' + str(count) + '].da_int32, '
                )
            elif value == 'ptr-ref':
                f.write(
                    'arg[' + str(count) + '].ptrref, '
                )
            elif value == 'ptr-val':
                f.write(
                    'arg[' + str(count) + '].ptrval, '
                )
            elif value == 'cvda':
                f.write(
                    'arg[' + str(count) + '].cvda, '
                )
            count = count + 1
        f.write(
            'flag);'
        )

        return

    def printcmmd_h(self):
        f = open(self.cmmd_h, mode = 'w', encoding='utf-8')

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        count = 0
        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text
            f.write(
                '{:30s}'.format('\tINQUIRE_' + self.resource.upper() + '_CMMD, ')
                + '{:20s}'.format('"'+ str(name).upper() +'",')
            )

            if value == 'data-value':
                type = argument.find('type').text
                if type == 'Character':
                    f.write(
                    '{:30s}'.format('ARGCLASS_DATA_VALUE,')
                    )
                    length = argument.find('length').text
                    f.write(
                    '{:25s}'.format('ALPHANUMERIC' + str(length) + ',')
                    )
                    f.write(
                    '"", ' + '/* (' + str(count) + ') char ' + str(name).lower() + '[' + str(length) + ']' + ' */'
                    )
                elif type == 'Halfword binary':
                    f.write(
                    '{:30s}'.format('ARGCLASS_DATA_VALUE,')
                    )
                    f.write(
                        '{:25s}'.format('HALFWORD_BINARY,')
                    )
                    f.write(
                    '"", ' + '/* (' + str(count) + ') int16_t *' +  str(name).lower() + ' */'
                    )
                elif type == 'Fullword binary':
                    f.write(
                    '{:30s}'.format('ARGCLASS_DATA_VALUE,')
                    )
                    f.write(
                        '{:25s}'.format('FULLWORD_BINARY,')
                    )
                    f.write(
                    '"", ' + '/* (' + str(count) + ') int32_t *' +  str(name).lower() + ' */'
                    )
                elif type == 'ABSTIME':
                    f.write(
                    '{:30s}'.format('ARGCLASS_DATA_VALUE,')
                    )
                    f.write(
                        '{:25s}'.format('PACKED_DECIMAL8,')
                    )
                    f.write(
                    '"", ' + '/* (' + str(count) + ') char *' +  str(name).lower() + '[8] */'
                    )
                elif type == 'digit':
                    f.write(
                    '{:30s}'.format('ARGCLASS_DATA_VALUE,')
                    )
                    f.write(
                        '{:25s}'.format('FULLWORD_BINARY,')
                    )
                    f.write(
                    '"", ' + '/* (' + str(count) + ') int32_t *' +  str(name).lower() + ' */'
                    )
            elif value == 'data-area':
                type = argument.find('type').text

                if type == 'Character':
                    f.write(
                    '{:30s}'.format('ARGCLASS_DATA_AREA,')
                    )
                    length = argument.find('length').text
                    f.write(
                    '{:25s}'.format('ALPHANUMERIC' + str(length) + ',')
                    )
                    f.write(
                    '"", ' + '/* (' + str(count) + ') char ' + str(name).lower() + '[' + str(length) + ']' + ' */'
                    )
                elif type == 'Halfword binary':
                    f.write(
                    '{:30s}'.format('ARGCLASS_DATA_AREA,')
                    )
                    f.write(
                        '{:25s}'.format('HALFWORD_BINARY,')
                    )
                    f.write(
                    '"", ' + '/* (' + str(count) + ') int16_t *' +  str(name).lower() + ' */'
                    )
                elif type == 'Fullword binary':
                    f.write(
                    '{:30s}'.format('ARGCLASS_DATA_AREA,')
                    )
                    f.write(
                        '{:25s}'.format('FULLWORD_BINARY,')
                    )
                    f.write(
                    '"", ' + '/* (' + str(count) + ') int32_t *' +  str(name).lower() + ' */'
                    )
                elif type == 'ABSTIME':
                    f.write(
                    '{:30s}'.format('ARGCLASS_DATA_AREA,')
                    )
                    f.write(
                        '{:25s}'.format('PACKED_DECIMAL8,')
                    )
                    f.write(
                    '"", ' + '/* (' + str(count) + ') char *' +  str(name).lower() + '[8] */'
                    )
                elif type == 'digit':
                    f.write(
                    '{:30s}'.format('ARGCLASS_DATA_AREA,')
                    )
                    f.write(
                        '{:25s}'.format('FULLWORD_BINARY,')
                    )
                    f.write(
                    '"", ' + '/* (' + str(count) + ') int32_t *' +  str(name).lower() + ' */'
                    )
            elif value == 'ptr-ref':
                f.write(
                    '{:30s}'.format('ARGCLASS_PTR_REF,')
                )
                f.write(
                    '{:25s}'.format('VOID_ARG,')
                )
                f.write(
                    '"", ' + '/* (' + str(count) + ') void *' +  str(name).lower() + ' */'
                )
            elif value == 'cvda':
                f.write(
                    '{:30s}'.format('ARGCLASS_CVDA,')
                )
                f.write(
                    '{:25s}'.format('FULLWORD_BINARY,')
                )
                f.write(
                    '"", ' + '/* (' + str(count) + ') int32_t *' +  str(name).lower() + ' */'
                )

            f.write(
                '\n')
            count = count + 1

        f.write(
            '{:30s}'.format('\tINQUIRE_' + self.resource.upper() + '_CMMD, ') + '{:20s}'.format('"START",')
            + '{:30s}'.format('ARGCLASS_NOARG,') + '{:25s}'.format('NO_ARG,') + '"", \n'
            '{:30s}'.format('\tINQUIRE_' + self.resource.upper() + '_CMMD, ') + '{:20s}'.format('"NEXT",')
            + '{:30s}'.format('ARGCLASS_NOARG,') + '{:25s}'.format('NO_ARG,') + '"", \n'
            '{:30s}'.format('\tINQUIRE_' + self.resource.upper() + '_CMMD, ') + '{:20s}'.format('"END",')
            + '{:30s}'.format('ARGCLASS_NOARG,') + '{:25s}'.format('NO_ARG,') + '"", \n'
            '{:30s}'.format('\tINQUIRE_' + self.resource.upper() + '_CMMD, ') + '{:20s}'.format('"NOHANDLE",')
            + '{:30s}'.format('ARGCLASS_NOARG,') + '{:25s}'.format('NO_ARG,') + '"", \n'
            '{:30s}'.format('\tINQUIRE_' + self.resource.upper() + '_CMMD, ') + '{:20s}'.format('"RESP",')
            + '{:30s}'.format('ARGCLASS_EIB,') + '{:25s}'.format('FULLWORD_BINARY,') + '"", /* int eibresp */\n'
            '{:30s}'.format('\tINQUIRE_' + self.resource.upper() + '_CMMD, ') + '{:20s}'.format('"RESP2",')
            + '{:30s}'.format('ARGCLASS_EIB,') + '{:25s}'.format('FULLWORD_BINARY,') + '"", /* int eibresp2 */\n'
        )

        f.close()
        return

    def printarg_h(self):
        f = open(self.arg_h, mode = 'w', encoding='utf-8')

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        count = 0
        for argument in root.findall('argument'):
            name = argument.get('name')
            f.write(
                '{:54}'.format('#define CICS_ARG_INQUIRE_' + self.resource.upper() + '_' + str(name).upper())
                + '(1L<<' + str(count) +')\n'
            )
            count = count + 1
        f.close()
        return

    def printinquire_h(self):
        f = open(self.inquire_h, mode = 'w', encoding='utf-8')

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        f.write(
            'extern void cics_' + self.command + '_' + self.resource + '(void *eiblk, uint64_t val_flag, '
        )

        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if value == 'cvda' :
                f.write(
                    'int32_t *' + str(name).lower() + ','
                )
            elif value == 'data-area':
                type = argument.find('type').text
                if type == 'Character':
                    f.write(
                        'char ' + str(name).lower() + '[CICS_' + str(name).upper() + '_SIZE],'
                    )
                elif type == 'Halfword binary':
                    f.write(
                        'int16_t *' + str(name).lower() + ','
                    )
                elif type == 'Fullword binary':
                    f.write(
                        'int32_t *' + str(name).lower() + ','
                    )
                elif type == 'ABSTIME': # ABSTIME = char[8] = PACKED_DECIMAL8
                    f.write(
                        'char ' + str(name).lower() + '[8],'
                    )
                else:
                    f.write(
                        'int32_t *' + str(name).lower() + ','
                    )
            elif value == 'data-value':
                type = argument.find('type').text
                if type == 'Character':
                    f.write(
                        'char ' + str(name).lower() + '[CICS_' + str(name).upper() + '_SIZE],'
                    )
            elif value == 'ptr-ref':
                f.write(
                        'void *' + str(name).lower() + ','
                )

        f.write(
            'int flag);\n'
        )
        f.close()
        return

    def printinquire_c(self):
        today = date.today()
        f = open(self.inquire_c, mode = 'w', encoding='utf-8')

        f.write('/**\n'
                ' * @file cics_' + self.command + '_' + self.resource + '.c\n'
                ' * @brief Retrieve information about a '+ self.resource +'.\n'
                ' * \n'
                ' * @date ' + today.strftime('%Y. %m. %d') + '\n'
                ' * @author Yeongseon Choe <yeongseon_choe@tmax.co.kr>\n'
                '*/\n'
                '\n'
                )

        f.write('#include "osc/cicsinc/cics_spi_extern.h"\n'
                '\n'
                '#include <stdio.h>\n'
                '#include <stdlib.h>\n'
                '#include <string.h>\n'
                '\n'
                '#include "osc/cicsinc/cics_svr.h"\n'
                '#include "osc/cicsinc/cics_size.h"\n'
                '#include "osc/cicsinc/cics_type.h"\n'
                '\n'
                '#include "osc/errcode/errcode_osc.h" /* for osc errcode */\n'
                '\n'
                '#include "osc/include/osc_spi.h" /* for osc spi */\n'
                '\n\n'
                )

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        '''

        '''
        f.write(
            'void cics_' + self.command + '_' + self.resource + '(void *eiblk, uint64_t val_flag, '
        )

        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if value == 'cvda' :
                f.write(
                    'int32_t *' + str(name).lower() + ','
                )
            elif value == 'data-area':
                type = argument.find('type').text
                if type == 'Character':
                    f.write(
                        'char ' + str(name).lower() + '[CICS_' + str(name).upper() + '_SIZE],'
                    )
                elif type == 'Halfword binary':
                    f.write(
                        'int16_t *' + str(name).lower() + ','
                    )
                elif type == 'Fullword binary':
                    f.write(
                        'int32_t *' + str(name).lower() + ','
                    )
                elif type == 'ABSTIME': # ABSTIME = char[8] = PACKED_DECIMAL8
                    f.write(
                        'char ' + str(name).lower() + '[8],'
                    )
                else:
                    f.write(
                        'int32_t *' + str(name).lower() + ','
                    )
            elif value == 'data-value':
                type = argument.find('type').text
                if type == 'Character':
                    f.write(
                        'char ' + str(name).lower() + '[CICS_' + str(name).upper() + '_SIZE],'
                    )
                elif type == 'Halfword binary':
                    f.write(
                        'int16_t ' + str(name).lower() + ','
                    )
                elif type == 'Fullword binary':
                    f.write(
                        'int32_t ' + str(name).lower() + ','
                    )
                elif type == 'Doubleword binary':
                    f.write(
                        'int64_t ' + str(name).lower() + ','
                    )
                elif type == 'ABSTIME': # ABSTIME = char[8] = PACKED_DECIMAL8
                    f.write(
                        'char ' + str(name).lower() + '[8],'
                    )
                else:
                    f.write(
                        'int32_t *' + str(name).lower() + ','
                    )
            elif value == 'ptr-ref':
                f.write(
                        'void *' + str(name).lower() + ','
                )
            elif value == 'ptr-val':
                f.write(
                        'void **' + str(name).lower() + ','
                )
        f.write(
            'int flag) {\n'
        )

        '''

        '''

        f.write(
            '\tint rc = 0;\n'
            '\tint resp1 = 0;\n'
            '\tint resp2 = 0;\n'
            '\tint temp = 0;\n'
            '\tcics_eib_t *eib;\n'
            '\tcics_ctx_t *cics_ctxp;\n\n'
            '\t/* for osc_spi_' + self.command + '_' + self.resource + '*/\n'
        )

        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if value == 'cvda':
                f.write(
                    '\tint32_t spi_' + str(name).lower() + ' = 0; /* CVDA */\n'
                )
            elif value == 'data-value':
                type = argument.find('type').text
                if type == 'Character':
                    f.write(
                        '\tchar spi_' + str(name).lower()
                        + '[CICS_' + str(name).upper() + '_SIZE] = "\\0"; /* Character */\n'
                    )
                elif type == 'Halfword binary':
                    f.write(
                        '\tint16_t spi_' + str(name).lower() + ' = 0; /* Halfword binary */\n'
                    )
                elif type == 'Fullword binary':
                    f.write(
                        '\tint32_t spi_' + str(name).lower() + ' = 0; /* Fullword binary */\n'
                    )
                elif type == 'ABSTIME':
                    f.write(
                        '\tchar spi_' + str(name).lower() + '[8] = "\\0"; /* ABSTIME */\n'
                    )
                else:
                    f.write(
                        '\tint32_t spi_' + str(name).lower() + ' = 0; /* ' + type + '*/\n'
                    )
            elif value == 'data-area':
                type = argument.find('type').text
                if type == 'Character':
                    f.write(
                        '\tchar spi_' + str(name).lower()
                        + '[CICS_' + str(name).upper() + '_SIZE] = "\\0"; /* Character */\n'
                    )
                elif type == 'Halfword binary':
                    f.write(
                        '\tint16_t spi_' + str(name).lower() + ' = 0; /* Halfword binary */\n'
                    )
                elif type == 'Fullword binary':
                    f.write(
                        '\tint32_t spi_' + str(name).lower() + ' = 0; /* Fullword binary */\n'
                    )
                elif type == 'ABSTIME':
                    f.write(
                        '\tchar spi_' + str(name).lower() + '[8] = "\\0"; /* ABSTIME */\n'
                    )
                else:
                    f.write(
                        '\tint32_t spi_' + str(name).lower() + ' = 0; /* ' + type + '*/\n'
                    )
            elif value == 'ptr-ref':
                f.write(
                    '\tvoid *spi_' + str(name).lower() + '= NULL; /* Ptr-ref */\n'
                )

        f.write(
            '\n'
            '\tcics_cmd_entry(CICS_EIBFN_' + str(self.command).upper() + '_' + str(self.resource).upper() + ', '
            + '"' + str(self.command).upper() + ' ' + str(self.resource).upper() + '", val_flag, flag,'
            + '"' + str(self.command).upper() + ' ' + str(self.resource).upper() + '(\'%.8s\')", spi_'
            + self.resource + ');\n'
            '\tcics_ctxp = CICS_ADDRESS_CTX;\n'
            '\teib = CICS_ADDRESS_EIB;\n'
            '\n'
            '\trc = osc_spi_' + self.command + '_' + self.resource + '_init();\n'
            '\tif (rc < 0) {\n'
            '\t\tCICS_LOG_EPRINTF3("CICS", OSC_MSG_FUNCTION_ERROR, "' + str(self.command).upper()
            + ' ' + str(self.resource) + '", "osc_spi_' + self.command + '_' + self.resource
            + '_init()", rc);\n'
            '\t\tresp1 = CICS_ERR_ERROR;\n'
            '\t\tresp2 = 0;\n'
            '\t\tgoto CATCH;\n'
            '\t}\n'
            '\n'
            '\tif (CICS_CHECK_ARG(CICS_ARG_' + str(self.command).upper() + '_' + str(self.resource).upper()
            + '_' + str(self.resource).upper() + ')) {\n'
            '\t\t_cics_name2str(' + self.resource + ', spi_' + self.resource + ', CICS_' + self.resource.upper()
            + '_SIZE);\n'
            '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_set_option("' + self.resource
            + '", spi_' + self.resource + ', &resp1, &resp2);\n'
            '\t\tif (rc < 0) {\n'
            '\t\t\tCICS_LOG_EPRINTF3("CICS", OSC_MSG_FUNCTION_ERROR, "' + str(self.command).upper()
            + ' ' + str(self.resource).upper() + '", "osc_spi_' + self.command + '_' + self.resource
            + '_set_option(' + self.resource + ')", rc);\n'
            '\t\t\tgoto CATCH;\n'
            '\t\t}\n'
            '\t}\n'
            '\n'
            '\tif (spi_' + self.resource + '[0] == ' + "'\\0'" + ' &&\n'
            '\t!CICS_CHECK_FLAG(CICS_FLAG_START) &&\n'
            '\t!CICS_CHECK_FLAG(CICS_FLAG_NEXT) && \n'
            '\t!CICS_CHECK_FLAG(CICS_FLAG_END)) {\n'
            '\t\tCICS_LOG_EPRINTF1("CICS", OSC_MSG_INVALID_REQUEST, "' + self.resource
            + ' is mandatory");\n'
            '\t\tresp1 = CICS_ERR_ERROR;\n'
            '\t\tresp2 = 0;\n'
            '\t\tgoto CATCH;\n'
            '\t}\n'
            '\n'
            '\tif (CICS_CHECK_FLAG(CICS_FLAG_START)) {\n'
            '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_set_option("start", "", &resp1, &resp2);\n'
            '\t\tif (rc < 0) {\n'
            '\t\t\tCICS_LOG_EPRINTF3("CICS", OSC_MSG_FUNCTION_ERROR, "' + str(self.command).upper() + ' '
            + str(self.resource).upper() + '", "osc_spi_' + self.command + '_' + self.resource
            + '_set_option(start)", rc);\n'
            '\t\t\tgoto CATCH;\n'
            '\t\t}\n'
            '\t} else if (CICS_CHECK_FLAG(CICS_FLAG_NEXT)) {\n'
            '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_set_option("next", "", &resp1, &resp2);\n'
            '\t\tif (rc < 0) {\n'
            '\t\t\tCICS_LOG_EPRINTF3("CICS", OSC_MSG_FUNCTION_ERROR, "' + str(self.command).upper() + ' '
            + str(self.resource).upper() + '", "osc_spi_' + self.command + '_' + self.resource
            + '_set_option(next)", rc);\n'
            '\t\t\tgoto CATCH;\n'
            '\t\t}\n'
            '\t} else if (CICS_CHECK_FLAG(CICS_FLAG_END)) {\n'
            '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_set_option("end", "", &resp1, &resp2);\n'
            '\t\tif (rc < 0) {\n'
            '\t\t\tCICS_LOG_EPRINTF3("CICS", OSC_MSG_FUNCTION_ERROR, "' + str(self.command).upper() + ' '
            + str(self.resource).upper() + '", "osc_spi_' + self.command + '_' + self.resource
            + '_set_option(end)", rc);\n'
            '\t\t\tgoto CATCH;\n'
            '\t\t}\n'
            '\t}\n'
            '\n'

            '\trc = osc_spi_' + self.command + '_' + self.resource + '(&resp1, &resp2);\n'
            '\tif (rc == OSC_ERR_SPI_END) {\n'
            '\t\tgoto CATCH;\n'
            '\t} else if (rc < 0) {\n'
            '\t\tCICS_LOG_EPRINTF3("CICS", OSC_MSG_FUNCTION_ERROR, "' + str(self.command).upper() +
            ' ' + str(self.resource).upper() + '", "osc_spi_' + self.command + '_' + self.resource
            + '()", rc);\n'
            '\t\tgoto CATCH;\n'
            '\t}'
            '\n'
        )

        for argument in root.findall('argument'):
            name = argument.get('name')
            support = argument.get('support')
            value = argument.find('value').text

            f.write(
                '\tif (CICS_CHECK_ARG(CICS_ARG_' + str(self.command).upper() + '_' + str(self.resource).upper() + '_' + str(name).upper() + ')) {\n'
            )

            if value == 'cvda':
                if str(support) == 'no':
                    f.write(
                        '\t\tCICS_LOG_EPRINTF1("CICSSPI", OSC_MSG_UNSUPPORTED_ERROR, "INQUIRE ' + self.resource.upper() + ' '
                        + str(name) + '");\n'
                        '\t\tresp1 = CICS_ERR_ERROR;\n'
                        '\t\tresp2 = 0;\n'
                    )
                    f.write('\t\t/*\n')

                f.write(
                        '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_get_option("' + str(name).lower() + '", &spi_'
                        + str(name).lower() + ');\n'
                    )
            elif value == 'data-value':
                pass
            elif value == 'data-area':
                type = argument.find('type').text
                if str(support) == 'no':
                    f.write(
                        '\t\tCICS_LOG_EPRINTF1("CICSSPI", OSC_MSG_UNSUPPORTED_ERROR, "INQUIRE ' + self.resource.upper() + ' '
                        + str(name) + '");\n'
                        '\t\tresp1 = CICS_ERR_ERROR;\n'
                        '\t\tresp2 = 0;\n'
                    )
                    f.write('\t\t/*\n')

                if type == 'Character':
                    f.write(
                        '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_get_option("' + str(name).lower() + '", spi_'
                        + str(name).lower() + ');\n'
                    )
                elif type == 'ABSTIME':
                    f.write(
                        '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_get_option("' + str(name).lower() + '", spi_'
                        + str(name).lower() + ');\n'
                    )
                elif type == 'Halfword binary':
                    f.write(
                        '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_get_option("' + str(name).lower() + '", &spi_'
                        + str(name).lower() + ');\n'
                    )
                elif type == 'Fullword binary':
                    f.write(
                        '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_get_option("' + str(name).lower() + '", &spi_'
                        + str(name).lower() + ');\n'
                    )
                else:
                    f.write(
                        '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_get_option("' + str(name).lower() + '", &spi_'
                        + str(name).lower() + ');\n'
                    )
            elif value == 'ptr-ref':
                if str(support) == 'no':
                    f.write(
                        '\t\tCICS_LOG_EPRINTF1("CICSSPI", OSC_MSG_UNSUPPORTED_ERROR, "INQUIRE ' + self.resource.upper() + ' '
                        + str(name) + '");\n'
                        '\t\tresp1 = CICS_ERR_ERROR;\n'
                        '\t\tresp2 = 0;\n'
                    )
                    f.write('\t\t/*\n')

            f.write(
                '\t\tif (rc < 0) {\n'
                '\t\t\tCICS_LOG_EPRINTF3("CICSSPI", OSC_MSG_FUNCTION_ERROR, "INQUIRE ' + self.resource.upper() + ' '
                + str(name) + '", \n'
                '\t\t\t\t\t"osc_spi_inquire_' + self.resource +'_get_option('+ str(name).lower() +')", rc);\n'
                '\t\t\tgoto CATCH;\n'
                '\t\t} else { \n'
            )


            if value == 'cvda':
                f.write(
                    # '\t\t\tmemcpy(' + str(name).lower() + ', &htonl(spi_' + str(name).lower() + ') , sizeof(int32_t));\n'
                    '\t\t\t*' + str(name).lower() + ' = htonl(spi_' + str(name).lower() + ');\n'
                )
            elif value == 'data-value':
                pass
            elif value == 'data-area':
                type = argument.find('type').text
                if type == 'Character':
                    f.write(
                        '\t\t\t_cics_str2name(spi_' + str(name).lower() + ', ' + str(name).lower() + ', '
                        + 'CICS_' + str(name) + '_SIZE);\n'
                    )
                elif type == 'ABSTIME':
                    f.write(
                        '\t\t\t_cics_str2name(spi_' + str(name).lower() + ', ' + str(name).lower() + ', '
                        + 'CICS_' + str(name) + '_SIZE);\n'
                    )
                elif type == 'Halfword binary':
                    f.write(
                        '\t\t\t*' + str(name).lower() + ' = htons(spi_' + str(name).lower() + ');\n'
                    )
                elif type == 'Fullword binary':
                    f.write(
                        '\t\t\t*' + str(name).lower() + ' = htonl(spi_' + str(name).lower() + ');\n'
                    )
                else:
                    f.write(
                        '\t\t\t*' + str(name).lower() + ' = htonl(spi_' + str(name).lower() + ');\n'
                    )

            f.write(
                '\t\t}\n'
            )

            if str(support) == 'no':
                f.write('\t\t*/\n')

            f.write(
                '\t}\n'
            )

        f.write(
            '\n'
            'END:\n'
            '\tcics_cmd_exit(CICS_EIBFN_' + str(self.command).upper() + '_' + str(self.resource).upper()
            + ', "' + str(self.command).upper() + ' ' + str(self.resource).upper() + '", val_flag, flag, '
            + '(int32_t) ntohl(eib->eibresp), (int32_t) ntohl(eib->eibresp2), 0);\n'
            '\treturn;\n'
            '\n'
            'CATCH:\n'
            '\tcics_cmd_exit(CICS_EIBFN_' + str(self.command).upper() + '_' + str(self.resource).upper()
            + ', "' + str(self.command).upper() + ' ' + str(self.resource).upper() + '", val_flag, flag, '
            + 'resp1, resp2, 1);\n'
            '\treturn;\n'
            '\n'
            '}\n'
        )
        f.close()
        return

    def printoscossvr_f(self):
        f = open(self.oscossvr_f, mode = 'w', encoding='utf-8')

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        i = 1
        line = ''
        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text
            if value == 'cvda' :
                line = '{:40s}{:8s}{:10s}{:5s}{:5s}\n'.format('FB_CICS_RTSD_' + self.resource.upper() + '_' + str(name).upper(), str(i), 'int','-','-')
            elif value == 'data-value':
                line = '{:40s}{:8s}{:10s}{:5s}{:5s}\n'.format('FB_CICS_RTSD_' + self.resource.upper() + '_' + str(name).upper(), str(i), 'string','-','-')
            elif value == 'data-area':
                type = argument.find('type').text
                if type == 'Character':
                    line = '{:40s}{:8s}{:10s}{:5s}{:5s}\n'.format('FB_CICS_RTSD_' + self.resource.upper() + '_' + str(name).upper(), str(i), 'string','-','-')
                elif type == 'ABSTIME':
                    line = '{:40s}{:8s}{:10s}{:5s}{:5s}\n'.format('FB_CICS_RTSD_' + self.resource.upper() + '_' + str(name).upper(), str(i), 'string','-','-')
                else:
                    line = '{:40s}{:8s}{:10s}{:5s}{:5s}\n'.format('FB_CICS_RTSD_' + self.resource.upper() + '_' + str(name).upper(), str(i), 'int','-','-')

            f.write(line)
            i = i + 1

        f.close()
        return

    def printoscossvr(self):
        today = date.today()
        f = open(self.oscossvr, mode = 'w', encoding='utf-8')
        f.write(
            '/**\n'
            ' * @file oscossvr_get_' + self.resource + '.c\n'
            ' * @brief\n'
            ' * \n'
            ' * @date ' + today.strftime('%Y. %m. %d') + '\n'
            ' * @author Yeongseon Choe <yeongseon_choe@tmax.co.kr>\n'
            '*/\n'
            '\n'
        )

        f.write(
            '#include "osc/svr/oscossvr/oscossvr.h"\n'
            '\n'
            '#include <stdio.h>\n'
            '#include <stdlib.h>\n'
            '#include <string.h>\n'
            '\n'
            '#include "osc/cicsinc/cics_cvda.h" /* for cvda value */\n'
            '#include "osc/cicsinc/cics_size.h" /* for cics size */\n'
            '\n'
            '#include "osc/include/cics_log.h"\n'
            '#include "osc/include/osc_spi.h" /* for osc spi library */\n'
            '\n'
            '#include "osc/msgcode/msgcode_osc.h" \n'
            '\n'
            '#include "osc/svr/oscossvr/oscossvr_fdl.h" \n\n'
        )

        f.write(
            'int oscossvr_get_' + self.resource + '(char resource_name[8], FBUF *rbuf, FBUF **sendbuf) {\n'
            '\trc = 0;\n'
            '\tretval = 0;\n'
            '\tretmsg[128] = "\\0"\n\n'
            '\tFBUF *sbuf = *sendbuf;\n'
            '\tFLDLEN rlen;\n\n'
        )

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        f.write('\tchar ' + self.resource.lower() + '[CICS_' + self.resource.upper() + '_SIZE] = "\\0";\n')
        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if str(name).upper() != self.resource.upper():
                if value == 'cvda' :
                    f.write('\tint32_t ' + str(name).lower() + ' = 0; /* CVDA */\n')
                elif value == 'data-value' :
                    type = argument.find('type').text
                    if type == 'Character':
                        f.write('\tchar ' + str(name).lower() + '[CICS_' + str(name).upper() + '_SIZE] = "\\0"; /* ' + type + ' */\n')
                    elif type == 'Halfword binary':
                        f.write('\tint32_t ' + str(name).lower() + ' = 0; /* ' + type + ' */\n')
                    elif type == 'Fullword binary':
                        f.write('\tint32_t ' + str(name).lower() + ' = 0; /* ' + type + ' */\n')
                    elif type == 'ABSTIME':
                        f.write('\tchar ' + str(name).lower() + '[8] = "\\0"; /* ' + type + ' */\n')
                    else:
                        f.write('\tint32_t ' + str(name).lower() + ' = 0; /* ' + type + ' */\n')
                elif value == 'data-area' :
                    type = argument.find('type').text
                    if type == 'Character':
                        f.write('\tchar ' + str(name).lower() + '[CICS_' + str(name).upper() + '_SIZE] = "\\0"; /* ' + type + ' */\n')
                    elif type == 'Halfword binary':
                        f.write('\tint32_t ' + str(name).lower() + ' = 0; /* ' + type + ' */\n')
                    elif type == 'Fullword binary':
                        f.write('\tint32_t ' + str(name).lower() + ' = 0; /* ' + type + ' */\n')
                    elif type == 'ABSTIME':
                        f.write('\tchar ' + str(name).lower() + '[8] = "\\0"; /* ' + type + ' */\n')
                    else:
                        f.write('\tint32_t ' + str(name).lower() + ' = 0; /* ' + type + ' */\n')
                else :
                    f.write('\tint32_t ' + str(name).lower() + ' = 0; /* ' + value + ' */\n')
        f.write('\n')

        f.write(
            '\tsprintf(retmsg, "Success");\n\n'
        )

        f.write(
            '\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'init();\n'
            '\tif (rc < 0) {\n'
            '\t\tCICS_LOG_EPRINTF3("OSCOSSVR", OSC_MSG_FUNCTION_ERROR, '
            '"oscossvr_get_' + self.resource + '", "osc_spi_' + self.command + '_' + self.resource + '_' + 'init()", rc);\n'
            '\treturn rc;\n'
            '\t}\n'
                )

        f.write(
            '\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'set_option("' + self.resource + '", resource_name, &resp1, &resp2);\n'
            '\trc = osc_spi_' + self.command + '_' + self.resource + '(&resp1, &resp2);\n\n'
        )


        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            f.write(
                '\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", &' + str(name).lower() + ');\n'
                '\tif (rc == OSC_ERR_SUCCESS) {\n'
                '\t\trc = fbput(sbuf, FB_CICSRTSD_' + self.resource.upper() + '_' + str(name).upper() + ', (char *) ' +
                str(name).lower() + ', 0);\n'
                '\t\tif (rc < 0) {\n'
                '\t\t\tsprintf(retmsg, "Field buffer error(%s)", fbstrerror(fberror));\n'
                '\t\t\tretval = rc;\n'
                '\t\t\tgoto CATCH;\n'
                '\t\t}\n'
                '\t}\n'
            )

        f.write(
            '\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'done();\n'
            '\tif (rc < 0) {\n'
            '\t\tCICS_LOG_EPRINTF3("OSCOSSVR", OSC_MSG_FUNCTION_ERROR, '
            '"oscossvr_get_' + self.resource + '", "osc_spi_' + self.command + '_' + self.resource + '_' + 'done()", rc);\n'
            '\t\treturn rc;\n'
            '\t}\n'
        )

        f.write(
            '\nCATCH:\n\n'
            '\trc = fbput(sbuf, FB_CICS_RCODE, (char *) &retval, 0);\n'
            '\tif (rc < 0) {\n'
            '\t\tretval = rc;\n'
            '\t\tsprintf(retmsg, "Field buffer error(%s)", fbstrerror(fberror));\n'
            '\t\tCICS_LOG_EPRINTF3("OSCOSSVR", OSC_MSG_FUNCTION_ERROR, "oscossvr_get_' + self.resource + '", "fbput", fbsterror(fberror));\n'
            '\t}\n\n'
            '\trc = fbput(sbuf, FB_CICS_RMSG, (char *) retmsg, strlen(retmsg));\n'
            '\tif (rc < 0) {\n'
            '\t\tretval = rc;\n'
            '\t\tsprintf(retmsg, "Field buffer error(%s)", fbstrerror(fberror));\n'
            '\t\tCICS_LOG_EPRINTF3("OSCOSSVR", OSC_MSG_FUNCTION_ERROR, "oscossvr_get_' + self.resource + '", "fbput", fbsterror(fberror));\n'
            '\t}\n\n'
        )

        f.write(
            '\treturn retval;\n'
            '}\n'
        )
        f.close()
        return

    def printrtsddump(self):
        today = date.today()
        f = open(self.oscrtsddump, mode = 'w', encoding='utf-8')
        f.write('/**\n'
                ' * @file oscrtsdupdate_update_' + self.resource + '.c\n'
                ' * @brief\n'
                ' * \n'
                ' * @date ' + today.strftime('%Y. %m. %d') + '\n'
                ' * @author Yeongseon Choe <yeongseon_choe@tmax.co.kr>\n'
                '*/\n'
                '\n'
                )

        f.write('#include "osc/tool/oscrtsddump/oscrtsddump.h"\n'
                '\n'
                '#include <stdio.h>\n'
                '#include <stdlib.h>\n'
                '#include <string.h>\n'
                '\n'
                '#include "osc/cicsinc/cics_cvda.h" /* for cvda value */\n'
                '#include "osc/cicsinc/cics_size.h" /* for cics size */\n'
                '#include "osc/include/osc_spi.h" /* for osc spi */\n\n'
                '#include "osc/errcode/errcode_osc.h" /* for osc errcode */\n'
                '\n'
                )

        f.write('extern int oscrtsddump_dump_' + self.resource + '(FILE *_fout, int *_success_count) {\n'
        '\tint rc = 0;\n'
        '\tchar str[1024] = "\\0";\n'
        '\tint i = 0;\n'
        '\n'
        '\t/* for osc_spi_set_' + self.resource + ' */\n'
        '\tint resp1 = 0, resp2 = 0;\n'
        )

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        f.write('\tchar ' + self.resource.lower() + '[CICS_' + self.resource.upper() + '_SIZE] = "\\0";\n')
        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if str(name).upper() != self.resource.upper():
                if value == 'cvda' :
                    f.write('\tint32_t ' + str(name).lower() + ' = 0; /* CVDA */\n')

                elif value == 'data-value' :
                    type = argument.find('type').text

                    if type == 'Character':
                        f.write('\tchar ' + str(name).lower() + '[CICS_' + str(name).upper() + '_SIZE]; /* ' + type + ' */\n')
                    elif type == 'Halfword binary':
                        f.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')
                    elif type == 'Fullword binary':
                        f.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')
                    elif type == 'ABSTIME':
                        f.write('\tchar ' + str(name).lower() + '[8] = "\\0"; /* ' + type + ' */\n')
                    else:
                        f.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')
                elif value == 'data-area' :
                    type = argument.find('type').text

                    if type == 'Character':
                        f.write('\tchar ' + str(name).lower() + '[CICS_' + str(name).upper() + '_SIZE]; /* ' + type + ' */\n')
                    elif type == 'Halfword binary':
                        f.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')
                    elif type == 'Fullword binary':
                        f.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')
                    elif type == 'ABSTIME':
                        f.write('\tchar ' + str(name).lower() + '[8] = "\\0"; /* ' + type + ' */\n')
                    else:
                        f.write('\tint32_t ' + str(name).lower() + '; /* ' + type + ' */\n')

                elif value == 'ptr-ref':
                        f.write('\tvoid *' + str(name).lower() + '; /* Ptr-ref */\n')

                else:
                    f.write('\tint32_t ' + str(name).lower() + '; /* ' + value + ' */\n')

        f.write('\n')

        f.write(
            '\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'init();\n'
            '\tif (rc < 0) {\n'
            '\t\tprintf("OSCRTSDDUMP : osc_spi_' + self.command + '_' + self.resource + '_' + 'init() fail, rc(%d)\\n", rc);\n'
            '\t\treturn rc;\n\n'
            '\t}\n'
         )

        f.write(
            '\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'set_option("start", "", &resp1, &resp2);\n'
            '\trc = osc_spi_' + self.command + '_' + self.resource + '(&resp1, &resp2);\n'
            '\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'set_option("next", "", &resp1, &resp2);\n'
            '\trc = osc_spi_' + self.command + '_' + self.resource + '(&resp1, &resp2);\n'
        )

        f.write('\n')

        f.write(
            '\twhile (rc > 0){\n'
            '\t\tstrcpy(str, "DEFINE ");\n'
            '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + self.resource + '", &' + self.resource + ');\n'
            '\t\tif (' + self.resource + '[0]) {\n'
            '\t\t\tstrcat(str, "' + self.resource.upper() + '(");\n'
            '\t\t\tstrncat(str, ' + self.resource + ', CICS_' + self.resource.upper() +'_SIZE);\n'
            '\t\t\tstrcat(str, ")");\n'
            '\t\t} else\n'
            '\t\t\tcontinue;\n\n'
        )

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if str(name).upper() != self.resource.upper():

                if value == 'cvda':
                    f.write(
                        '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", &' + str(name).lower() + ');\n'
                        '\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                    )
                    i = 0

                    for cvda in argument.findall('cvda'):
                        if i == 0:
                            f.write(
                                '\t\t\tif (' + str(name).lower() + '== CVDA_' + cvda.text + ')\n'
                                '\t\t\t\tstrcat(str, "' + str(name).upper() + '(' + cvda.text + ')");\n'
                            )
                            i = i+1
                        else:
                            f.write(
                                '\t\t\telse if (' + str(name).lower() + '== CVDA_' + cvda.text + ')\n'
                                '\t\t\t\tstrcat(str, "' + str(name).upper() + '(' + cvda.text + ')");\n'
                            )

                elif value == 'data-value':
                    type = argument.find('type').text

                    if type == 'Character':
                        f.write(
                            '\t\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", ' + str(name).lower() + ');\n'
                            '\t\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                        )

                        f.write(
                                '\t\t\t\tstrcat(str, "' + str(name).upper() + '(");\n'
                                '\t\t\t\tstrcat(str, '+ str(name).lower() + ');\n'
                                '\t\t\t\tstrcat(str, ")");\n'
                        )
                    elif type == 'Halfword binary':
                        f.write(
                            '\t\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", &' + str(name).lower() + ');\n'
                            '\t\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                        )
                        f.write(
                        '\t\t\t\tstrcat(str, "' + str(name).upper() + '(");\n'
                        '\t\t\t\tstrcat(str, (char *) osc_itoa(' + str(name).lower() + '));\n'
                        '\t\t\t\tstrcat(str, ")");\n'
                    )
                    elif type == 'Fullword binary':
                        f.write(
                            '\t\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", &' + str(name).lower() + ');\n'
                            '\t\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                        )
                        f.write(
                        '\t\t\t\tstrcat(str, "' + str(name).upper() + '(");\n'
                        '\t\t\t\tstrcat(str, (char *) osc_itoa(' + str(name).lower() + '));\n'
                        '\t\t\t\tstrcat(str, ")");\n'
                    )
                    elif type == 'ABSTIME':
                        f.write(
                            '\t\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", ' + str(name).lower() + ');\n'
                            '\t\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                        )
                        f.write(
                            '\t\t\t\tstrcat(str, "' + str(name).upper() + '(");\n'
                            '\t\t\t\tstrcat(str, '+ str(name).lower() + ');\n'
                            '\t\t\t\tstrcat(str, ")");\n'
                        )
                    elif type == 'digit':
                        f.write(
                            '\t\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", &' + str(name).lower() + ');\n'
                            '\t\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                        )
                        f.write(
                        '\t\t\t\tstrcat(str, "' + str(name).upper() + '(");\n'
                        '\t\t\t\tstrcat(str, (char *) osc_itoa(' + str(name).lower() + '));\n'
                        '\t\t\t\tstrcat(str, ")");\n'
                        )
                    else :
                        '\t\t\t\t/* TODO ' + str(name) + ' */\n'

                elif value == 'data-area':
                    type = argument.find('type').text

                    if type == 'Character':
                        f.write(
                            '\t\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", ' + str(name).lower() + ');\n'
                            '\t\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                        )
                        f.write(
                            '\t\t\t\tstrcat(str, "' + str(name).upper() + '(");\n'
                            '\t\t\t\tstrncat(str, '+ str(name).lower() + ', CICS_'+ str(name).upper() +'_SIZE);\n'
                            '\t\t\t\tstrcat(str, ")");\n'
                        )
                    elif type == 'Halfword binary':
                        f.write(
                            '\t\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", &' + str(name).lower() + ');\n'
                            '\t\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                        )
                        f.write(
                        '\t\t\t\tstrcat(str, "' + str(name).upper() + '(");\n'
                        '\t\t\t\tstrcat(str, (char *) osc_itoa(' + str(name).lower() + '));\n'
                        '\t\t\t\tstrcat(str, ")");\n'
                    )
                    elif type == 'Fullword binary':
                        f.write(
                            '\t\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", &' + str(name).lower() + ');\n'
                            '\t\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                        )
                        f.write(
                        '\t\t\t\tstrcat(str, "' + str(name).upper() + '(");\n'
                        '\t\t\t\tstrcat(str, (char *) osc_itoa(' + str(name).lower() + '));\n'
                        '\t\t\t\tstrcat(str, ")");\n'
                        )
                    elif type == 'ABSTIME':
                        f.write(
                            '\t\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", ' + str(name).lower() + ');\n'
                            '\t\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                        )
                        f.write(
                            '\t\t\t\tstrcat(str, "' + str(name).upper() + '(");\n'
                            '\t\t\t\tstrcat(str, '+ str(name).lower() + ');\n'
                            '\t\t\t\tstrcat(str, ")");\n'
                        )
                    elif type == 'digit':
                        f.write(
                            '\t\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", &' + str(name).lower() + ');\n'
                            '\t\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                        )
                        f.write(
                        '\t\t\t\tstrcat(str, "' + str(name).upper() + '(");\n'
                        '\t\t\t\tstrcat(str, (char *) osc_itoa(' + str(name).lower() + '));\n'
                        '\t\t\t\tstrcat(str, ")");\n'
                        )

                    else :
                        f.write(
                        '\t\t\t\t/* TODO ' + str(name) + ' */\n'
                    )

                elif value == 'ptr-ref':
                    f.write(
                        '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'get_option("' + str(name).lower() + '", ' + str(name).lower() + ');\n'
                        '\t\tif (rc == OSC_ERR_SUCCESS) {\n'
                    )

                else:
                    '\t\t\t\t/* TODO ' + str(name) + ' */\n'

                f.write('\t\t\t}\n\n')

        f.write(
            '\t\tfprintf(_fout, "%s\\n", str);\n'
            '\t\tmemset(str, 0x00, sizeof(str));\n'
            '\t\t(*_success_count)++;\n\n'
        )

        f.write(
            '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'set_option("next", "", &resp1, &resp2);\n'
            '\t\trc = osc_spi_' + self.command + '_' + self.resource + '(&resp1, &resp2);\n'
            '\t}\n'
        )

        f.write(
            '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'set_option("end", "", &resp1, &resp2);\n'
            '\t\trc = osc_spi_' + self.command + '_' + self.resource + '(&resp1, &resp2);\n\n'
            '\t\trc = osc_spi_' + self.command + '_' + self.resource + '_' + 'done();\n'
            '\t\tif (rc < 0) {\n'
            '\t\t\tprintf("OSCRTSDDUMP : osc_spi_' + self.command + '_' + self.resource + '_' + 'done() fail, rc(%d)\\n", rc);\n'
            '\t\t}\n'
            '\treturn rc;\n'
            '}'
        )

        f.close()
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
                           'extern int ' + self.prefix + '_' + self.command + '_' + self.resource + '_set_option' +
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
                           ' * @brief Get the '+ self.command + ' ' + self.resource + ' command.\n'
                           ' * @param[in] _option\n'
                           ' * @param[out] _argument\n'
                           ' * @param[out] _resp1 RESP1\n'
                           ' * @param[out] _resp2 RESP2\n'
                           ' */\n'
                           'extern int ' + self.prefix + '_' + self.command + '_' + self.resource + '_get_option' +
                           '(char *_option, void *_argument);\n\n'
                           )
        self.oheader.write('/**\n'
                           ' * @brief Finalize the ' + self.command + ' ' + self.resource + ' command.\n'
                           ' * @return zero on success\n'
                           ' */\n'
                           'extern int ' + self.prefix + '_' + self.command + '_' + self.resource + '_' + 'done();\n\n'
                           )

        self.oheader.close()

    def printStruct(self):
        self.olhearder = open(self.outputlocalheader, mode = 'w', encoding='utf-8')
        self.olhearder.write('enum ' + self.command + '_' + self.resource + '_flag_type {\n'
                             '\t' + self.command.upper() + '_' + self.resource.upper() + '_FLAG_' +  self.resource.upper() +' = 0,\n'
                             '\t' + self.command.upper() + '_' + self.resource.upper() + '_FLAG_AT,\n'
                             '\t' + self.command.upper() + '_' + self.resource.upper() + '_FLAG_START,\n'
                             '\t' + self.command.upper() + '_' + self.resource.upper() + '_FLAG_NEXT,\n'
                             '\t' + self.command.upper() + '_' + self.resource.upper() + '_FLAG_END,\n'
                             '};\n'
                             '\n'
                             )
        self.olhearder.write('typedef struct osc_spi_' + self.command + '_' + self.resource + '_options_s {\n'
                             '\tchar ' + self.resource + '[CICS_' + self.resource.upper() + '_SIZE];\n'
                             '\tchar at[CICS_' + self.resource.upper() + '_SIZE];\n'
                             '\tint32_t start;\n'
                             '\tint32_t next;\n'
                             '\tint32_t end;\n'
                             '\tint32_t flag[10];\n'
                             '} osc_spi_' + self.command + '_' + self.resource + '_options_t;\n'
                             )
        self.olhearder.close()

    def printComment(self):
        today = date.today()

        inputfile = open(self.inputsyntaxfile, mode = 'r', encoding='utf-8')

        self.osource.write('/**\n'
                           ' * @file ' + self.prefix + '_' + self.command + '_' + self.resource + '.c\n'
                           ' * @brief \n')

        for line in inputfile.readlines():
            self.osource.write(' * ' + line)

        self.osource.write(' * Reference: \n'
                           ' * ' + defult_url.format(self.systemcommand) + '\n'
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

    def printGlobalVariable(self):

        self.osource.write(self.prefix + '_' + self.command + '_' + self.resource + '_' + 'options_t ' +
                           self.command + '_' + self.resource + '_' + 'options;\n'
                           )
        self.osource.write('cics_rtsd_' + self.resource + '_t ' + self.command + '_rtsd_' + self.resource + ';\n')
        self.osource.write('\n')
        return

    def printInitFunction(self):
        functionname = self.prefix + '_' + self.command + '_' + self.resource + '_init()'
        self.osource.write('int\t' + functionname + ' {\n')
        self.osource.write('\tint\trc = 0;\n')
        self.osource.write('\tif (' + self.command + '_' + self.resource + '_options.flag[' + \
                           self.command.upper() + '_' + self.resource.upper() + '_' + 'FLAG_START] == \n'
                           '\tOSC_SPI_FALSE) {\n'
                           '\t\tmemset(&' + self.command + '_' + self.resource + '_options, 0x00,\n'
                           '\t\t\tsizeof(' + self.command + '_' + self.resource + '_options));\n'
                           '\t\tmemset(&' + self.command + '_rtsd_' + self.resource + ', 0x00, sizeof(' + self.command + '_rtsd_' + self.resource + '));\n'
                           '\t}\n'
                           )
        self.osource.write('\treturn rc;\n'
                           '}\n'
                           '\n'
                           )
        return

    def printSetFunction(self):
        functionname = self.prefix + '_' + self.command + '_' + self.resource + \
                       '_set_option(char *_option, void *_argument, int *_resp1, int *_resp2)'
        self.osource.write('int\t' + functionname + ' {\n')
        self.osource.write('\tint\trc = 0;\n')
        self.osource.write('\n')
        self.osource.write('\tif (strcmp(_option, "' + self.resource + '") == 0) {\n'
                           '\t\tmemcpy(' + self.command + '_' + self.resource + '_options.' + self.resource + ', (char *)_argument,\n'
                           '\t\tCICS_' + self.resource.upper() + '_SIZE);\n'
                           '\t\t' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_' +
                           self.resource.upper() + '] = OSC_SPI_TRUE;\n'

                           '\t} else if (strcmp(_option, "start") == 0) {\n'
                           '\t\t/* Exception condition for browsing */\n'
                           '\t\tif (' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_START]) {\n'
                           '\t\t\t*_resp1 = CICS_ERR_ILLOGIC;\n'
                           '\t\t\t*_resp2 = 1;\n'
                           '\t\t\treturn OSC_ERR_SPI_ILLOGIC;\n'
                           '\t\t}\n'
                           '\t\t' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_START] = OSC_SPI_TRUE;\n'

                           '\t} else if (strcmp(_option, "at") == 0) {\n'
                           '\t\t/* Not supported. */\n'
                           '\t\treturn OSC_ERR_SPI_NOT_SUPPORTED;\n'

                           '\t} else if (strcmp(_option, "next") == 0) {\n'
                           '\t\t/* Exception condition for browsing */\n'
                           '\t\tif (' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_START] == OSC_SPI_FALSE) {\n'
                           '\t\t\t*_resp1 = CICS_ERR_ILLOGIC;\n'
                           '\t\t\t*_resp2 = 1;\n'
                           '\t\t\treturn OSC_ERR_SPI_ILLOGIC;\n'
                           '\t\t}\n'
                           '\t\t' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_NEXT] = OSC_SPI_TRUE;\n'

                           '\t} else if (strcmp(_option, "end") == 0) {\n'
                           '\t\t/* Exception condition for browsing */\n'
                           '\t\tif (' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_START] == OSC_SPI_FALSE) {\n'
                           '\t\t\t*_resp1 = CICS_ERR_ILLOGIC;\n'
                           '\t\t\t*_resp2 = 1;\n'
                           '\t\t\treturn OSC_ERR_SPI_ILLOGIC;\n'
                           '\t\t}\n'
                           '\t\t' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_END] = OSC_SPI_TRUE;\n'

                           '\t} else {\n'
                           '\t\t*_resp1 = CICS_ERR_ERROR;\n'
                           '\t\t*_resp2 = 0;\n'
                           '\t\treturn OSC_ERR_SPI_ERROR;\n'
                           '\t}\n'
                           '\n'
                           )
        self.osource.write('\treturn rc;\n'
                           '}\n'
                           '\n'
                           )
        return

    def printExecuteFunction(self):
        functionname = self.prefix + '_' + self.command + '_' + self.resource + '(int *_resp1, int *_resp2)'
        self.osource.write('int\t' + functionname + ' {\n')
        self.osource.write('\tint\trc = 0;\n')
        self.osource.write('\n')

        self.osource.write('\tif (' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_END]) {\n'
                           '\t\trc = cics_rtsd_endbr(CICS_RTSD_' + self.resource.upper() + ');\n'
                           '\t\tif (rc < 0) {\n'
                           '\t\t\t*_resp1 = CICS_ERR_ERROR;\n'
                           '\t\t\t*_resp2 = 0;\n'
                           '\t\t\treturn OSC_ERR_SPI_ERROR;\n'
                           '\t\t}\n'

                           '\t} else if (' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_START]) {\n'
                           '\t\tif (' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_NEXT]) {\n'
                           '\t\t\trc = cics_rtsd_readnext(CICS_RTSD_' + self.resource.upper() + ', &' + self.command +'_rtsd_' + self.resource + ', 0);\n'
                           '\t\t\tif (rc == OSC_ERR_RTSD_NOT_FOUND) {\n'
                           '\t\t\t\t/* no more resource definition */\n'
                           '\t\t\t\t*_resp1 = CICS_ERR_END;\n'
                           '\t\t\t\t*_resp2 = 2;\n'
                           '\t\t\t\treturn OSC_ERR_SPI_END;\n'
                           '\t\t\t} else if (rc < 0) {\n'
                           '\t\t\t\t*_resp1 = CICS_ERR_ERROR;\n'
                           '\t\t\t\t*_resp2 = 0;\n'
                           '\t\t\t\treturn OSC_ERR_SPI_ERROR;\n'
                           '\t\t\t}\n'

                           '\t\t} else {\n'
                           '\t\t\trc = cics_rtsd_startbr(CICS_RTSD_' + self.resource.upper() + ', ' +
                           self.command + '_' + self.resource + '_' + 'options.' + self.resource + ');\n'
                           '\t\t\tif (rc == OSC_ERR_RTSD_NOT_FOUND) {\n'
                           '\t\t\t\t/* no more resource definition */\n'
                           '\t\t\t\t*_resp1 = CICS_ERR_END;\n'
                           '\t\t\t\t*_resp2 = 2;\n'
                           '\t\t\t\treturn OSC_ERR_SPI_END;\n'
                           '\t\t\t} else if (rc < 0) {\n'
                           '\t\t\t\t*_resp1 = CICS_ERR_ERROR;\n'
                           '\t\t\t\t*_resp2 = 0;\n'
                           '\t\t\t\treturn OSC_ERR_SPI_ERROR;\n'
                           '\t\t\t}\n'
                           '\t\t}\n'

                           '\t} else {\n'
                           '\t\trc = cics_rtsd_read(CICS_RTSD_' + self.resource.upper() + ', ' +
                           self.command + '_' + self.resource + '_options.' + self.resource + ', ' +
                           '&' + self.command + '_rtsd_' + self.resource + ', 0);\n'
                           '\t\tif (rc == OSC_ERR_RTSD_NOT_FOUND) {\n'
                           '\t\t\t/* no more resource definition */\n'
                           '\t\t\t*_resp1 = CICS_ERR_END;\n'
                           '\t\t\t*_resp2 = 2;\n'
                           '\t\t\treturn OSC_ERR_SPI_END;\n'
                           '\t\t} else if (rc < 0) {\n'
                           '\t\t\t*_resp1 = CICS_ERR_ERROR;\n'
                           '\t\t\t*_resp2 = 0;\n'
                           '\t\t\treturn OSC_ERR_SPI_ERROR;\n'
                           '\t\t}\n'
                           '\t}\n'
                           '\n'
                           )

        self.osource.write('\treturn rc;\n'
                           '}\n'
                           '\n'
                           )
        return

    def printGetFunction(self):
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
            'extern cics_rtsd_' + self.resource + '_t ' + self.command + '_rtsd_' + self.resource + ';\n'
        )

        inputfile = open(self.inputsyntaxfile, mode = 'r', encoding='utf-8')
        functionname = self.prefix + '_' + self.command + '_' + self.resource + \
                       '_get_option(char *_option, void *_argument)'
        self.osource_rtsd.write('int\t' + functionname + ' {\n'
                                '\tint\trc = 0;\n'
                                '\tint32_t\tcvda = 0;\n'
                                '\n'
                                )

        self.osource_rtsd.write('\tif(strcmp(_option, "' + self.resource + '") == 0) {\n'
                           '\t\t/* Not supported. */\n'
                           '\t\treturn OSC_ERR_SPI_NOT_SUPPORTED;\n'
                           )

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if str(name).upper() != str(self.resource).upper() :
                self.osource_rtsd.write(
                    '\t} else if (strcmp(_option, "' + str(name).lower() + '") == 0) { \n'
                    '\t\t/* Not supported. */\n'
                    '\t\treturn OSC_ERR_SPI_NOT_SUPPORTED;\n'
                )
                if value == 'cvda':
                    for cvda in argument.findall('cvda'):
                        self.osource_rtsd.write(
                            '\t\t/* cvda = CVDA_' + cvda.text + ';*/\n'
                        )


        self.osource_rtsd.write(
            '\t} else {\n'
            '\t\treturn OSC_ERR_SPI_ERROR;\n'
            '\t}\n'
            '\n'
        )

        self.osource_rtsd.write(
            '\treturn rc;\n'
            '}\n\n'
        )

    def printDoneFunction(self):
        functionname = self.prefix + '_' + self.command + '_' + self.resource + '_done()'
        self.osource.write('int\t' + functionname + ' {\n'
                           '\tint\trc = 0;\n'
                           '\n'
                           )
        self.osource.write('\tif (' + self.command + '_' + self.resource + '_options.flag[' +
                           self.command.upper() + '_' + self.resource.upper() + '_FLAG_END]) {\n'
                           '\t\tmemset(&' + self.command + '_' + self.resource + '_options, 0x00, sizeof(' +
                           self.command + '_' + self.resource + '_options));\n'
                           '\t\tmemset(&' + self.command + '_rtsd_' + self.resource + ', 0x00, sizeof(' + self.command + '_rtsd_' + self.resource + '));\n'
                           '\t}\n'
                           )

        self.osource.write('\treturn rc;\n'
                           '}\n'
                           '\n'
                           )

        return