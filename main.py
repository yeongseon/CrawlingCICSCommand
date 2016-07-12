import argparse
from genSpi import spisyntax
from genApi import apisyntax
from genAPIXml import genAPIXml
from genMap import genMap
from genXml import genXml
from genCreate import genCreate
from genDiscard import genDiscard
from genInquire import genInquire
from genSet import genSet
from genCobol import genCobol

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--command type', dest = 'command', type = str)
parser.add_argument('-r', '--resource type', dest = 'resource', type = str)
parser.add_argument('-o', '--output type', dest = 'output', type = str)
parser.add_argument('-t', '--type', dest = 'type', type = str)

if __name__ == "__main__":
    args = parser.parse_args()

    if str(args.type) == 'api':
        if str(args.output) == 'xml':
            apisyntax = apisyntax(args.command)
            apisyntax.extract()
            apiXML = genAPIXml(args.command)
            apiXML.gen_xml1()
            apiXML.gen_xml2()

    if args.command and args.resource:
        if str(args.command) == 'create':
            if str(args.output) == 'xml':
                spisyntax = spisyntax(args.command, args.resource)
                spisyntax.extract()
                createXml = genXml(args.command, args.resource)
                createXml.gen_xml4()
                createXml.gen_xml5()
                #createXml.gen_xml6()
            elif str(args.output) == 'code':
                code = genCreate(args.command, args.resource)
                code.printDefine()
                code.printStruct()
                code.fopen()
                code.printComment()
                code.printHeader()
                code.printGlobalVariable()
                code.printInitFunction()
                code.printSetFunction()
                code.printExecuteFunction() # rtsd
                code.printDoneFunction()
            elif str(args.output) == 'cob':
                cob =genCobol(args.command, args.resource)
                cob.print_identification_division()
                cob.print_environment_divition()
                cob.print_data_divition()
            elif str(args.output) == 'map':
                map = genMap(args.command, args.resource)
                map.print_inquire_map()

        elif str(args.command) == 'discard':
            if str(args.output) == 'xml':
                spisyntax = spisyntax(args.command, args.resource)
                spisyntax.extract()
                discardXml = genXml(args.command, args.resource)
                discardXml.gen_xml_discard()
            elif str(args.output) == 'code':
                code = genDiscard(args.command, args.resource)
                code.printDefine()
                code.fopen()
                code.printComment()
                code.printHeader()
                code.printGlobalVariable()
                code.printInitFunction()
                code.printSetFunction()
                code.printExecuteFunction()
                code.printDoneFunction()

        elif str(args.command) == 'inquire':
            if str(args.output) == 'xml':
                spisyntax = spisyntax(args.command, args.resource)
                spisyntax.extract()
                inquireXml = genXml(args.command, args.resource)
                inquireXml.gen_xml1()
                inquireXml.gen_xml2()
                inquireXml.gen_xml3()
            elif str(args.output) == 'map':
                map = genMap(args.command, args.resource)
                map.print_inquire_map()
            elif str(args.output) == 'code':
                code = genInquire(args.command, args.resource)
                code.printecpi_c()
                code.printcmmd_h()
                code.printarg_h()
                code.printinquire_h()
                code.printinquire_c()
                code.printoscossvr_f()
                code.printoscossvr()
                code.printrtsddump()
                code.printDefine()
                code.printStruct()
                code.fopen()
                code.printComment()
                code.printHeader()
                code.printGlobalVariable()
                code.printInitFunction()
                code.printSetFunction()
                code.printExecuteFunction()
                code.printGetFunction() # rtsd
                code.printDoneFunction()
                code.fclose()
            elif str(args.output) == 'cob':
                cob = genCobol(args.command, args.resource)
                cob.print_identification_division()
                cob.print_environment_divition()
                cob.print_data_divition()
                cob.print_linkage_section()
                cob.print_procedure_divition()

        elif str(args.command) == 'set':
            if str(args.output) == 'xml':
                setXml = genXml(args.command, args.resource)
                setXml.gen_xml1()
                setXml.gen_xml2()
                setXml.gen_xml3()
                setXml.gen_xml_resp()
            elif str(args.output) == 'map':
                map = genMap(args.command, args.resource)
                map.print_set_map()
            elif str(args.output) == 'code':
                code = genSet(str(args.command), str(args.resource))
                code.printecpi_c()
                code.printcmmd_h()
                code.printarg_h()
                code.printset_h()
                code.printset_c()
                code.printoscossvr()
                code.printrtsdupdate()
                code.printDefine()
                code.printStruct()
                code.fopen()
                code.printComment()
                code.printHeader()
                code.printGlobalVariable()
                code.printInitFunction()
                code.printSetFunction()
                code.printExecuteFunction() #rtsd
                code.printDoneFunction()
                code.fclose()
            elif str(args.output) == 'cob':
                cob = genCobol(args.command, args.resource)
                cob.print_identification_division()
                cob.print_environment_divition()
                cob.print_data_divition()
                cob.print_linkage_section()
                cob.print_procedure_divition()

