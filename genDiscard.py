from datetime import date
import re

output_syntax = 'spi/output_syntax/{}.txt'

output_source = 'spi/output_code/{}/osc_spi_{}_{}.c'
output_header = 'spi/output_code/{}/osc_spi_{}_{}.h'
output_local_header = 'spi/output_code/{}/osc_spi_{}_{}_local.h'
output_oscossvr = 'spi/output_code/{}/oscossvr_remove_{}.c'

class genDiscard(object):
    def __init__(self, command, resource):
        self.prefix = 'osc_spi'
        self.command = command
        self.resource = resource
        self.outputsource = output_source.format(self.resource, self.command, self.resource)
        self.outputheader = output_header.format(self.resource, self.command, self.resource)

    def fopen(self):
        self.osource = open(self.outputsource, mode = 'w', encoding='utf-8')
        return

    def fclose(self):
        self.osource.close()
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

    def printComment(self):
        today = date.today()
        inputfilename = output_syntax.format(self.command + self.resource)
        # inputfilename = 'discard/' + self.command + self.resource + '.txt'
        inputfile = open(inputfilename, mode = 'r', encoding='utf-8')

        self.osource.write('/**\n'
                           ' * @file ' + self.prefix + '_' + self.command + '_' + self.resource + '.c\n'
                           ' * @brief \n')

        for line in inputfile.readlines():
            self.osource.write(' * ' + line)

        self.osource.write(' * Reference: \n'
                           ' * TS Server 4.2 System Programming Reference p.\n'
                           ' *\n'
                           ' * @date ' + today.strftime('%Y. %m. %d') + '\n'
                           ' * @author Yeongseon Choe <yeongseon_choe@tmax.co.kr>\n'
                           '*/\n'
                           '\n'
                           )
        return

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
        var = 'char\t' + self.resource + '[CICS_' + self.resource.upper() + '_SIZE];'
        self.osource.write(var + '\n')
        self.osource.write('\n')
        return

    def printInitFunction(self):
        functionname = self.prefix + '_' + self.command + '_' + self.resource + '_init()'
        self.osource.write('int\t' + functionname + ' {\n'
                           '\tint\trc = 0;\n'
                           '\tmemset(&' + self.resource + ', 0x00, sizeof(' + self.resource + '));\n'
                           '\treturn rc;\n'
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
                           '\tif(strcmp(_option, "' + self.resource + '") == 0 ) {\n'
                           '\t\tmemcpy(' + self.resource + ', (char *) _argument, CICS_' + self.resource.upper() + '_SIZE);\n'
                           '\t} else {\n'
                           '\t\t*_resp1 = CICS_ERR_ERROR;\n'
                           '\t\t*_resp2 = 0;\n'
                           '\t\treturn OSC_ERR_SPI_ERROR;\n'
                           '\t}\n'
                           '\treturn rc;\n'
                           '}\n'
                           '\n'
                           )
        return

    def printExecuteFunction(self):
        functionname = self.prefix + '_' + self.command + '_' + self.resource + '(int *_resp1, int *_resp2)'
        self.osource.write('int\t' + functionname + ' {\n'
                           '\tint\trc = 0;\n'
                           '\n'
                           '\t/* TODO : INVREQ condition */\n'
                           '\t/* TODO : NOTAUTH condition */\n'
                           '\n'
                           '\trc = cics_rtsd_delete(' + 'CICS_RTSD_' + self.resource.upper() + ', ' + self.resource + ');\n'
                           '\tif (rc == OSC_ERR_RTSD_NOT_FOUND) {\n'
                           '\t\t/* TODO : */\n'
                           '\t}else if (rc < 0) {\n'
                           '\t\t*_resp1 = CICS_ERR_ERROR;\n'
                           '\t\t*_resp2 = 0;\n'
                           '\t\treturn OSC_ERR_SPI_ERROR;\n'
                           '\t}\n'
                           '\treturn rc;\n'
                           '}\n'
                           '\n'
                           )
        return

    def printDoneFunction(self):
        functionname = self.prefix + '_' + self.command + '_' + self.resource + '_done()'
        self.osource.write('int\t' + functionname + ' {\n'
                           '\tint\trc = 0;\n'
                           '\tmemset(&' + self.resource + ', 0x00, sizeof(' + self.resource + '));\n'
                           '\treturn rc;\n'
                           '}\n'
                           '\n'
                           )
        return
