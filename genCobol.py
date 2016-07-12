from datetime import date
import xml.etree.ElementTree as ET

input_xml = 'spi/input_xml/{}.xml'

output_cob = 'spi/output_cobol/{}.cob'

space = ' '
tab = ' ' * 7
tab3 = ' ' * 3
tab4 = ' ' * 4
tab5 = ' ' * 5
tab7 = ' ' * 7

tab01 = ' ' * 7
tab05 = ' ' * 10
tab88 = ' ' * 10
tab10 = ' ' * 13

#        7     33
ws_01 = '{}{:26s}{:16s}{}\n'
ws_05 = '{}{:21s}{:18s}{}\n'
ws_88 = '{}{:23s}{:16s}{}\n'
ws_10 = '{}{:20s}{:16s}{}\n'

move_to = 'MOVE {:20} TO {:20}\n'

ws_tdq_name = 'OSTQ'

class genCobol(object):
    def __init__(self, command, resource):
        self.prefix = 'cics_spi'
        self.command = command
        self.resource = resource
        self.systemcommand = self.command + self.resource
        self.cobfile = str(self.command).upper()[0:3] + str(self.resource).upper()[0:4]
        self.fopen()
        return

    def __del__(self):
        self.fclose()

    def fopen(self):
        cobol_file = output_cob.format(self.cobfile)
        self.f = open(cobol_file, mode = 'w', encoding = 'utf-8')
        return

    def fclose(self):
        self.f.close()
        return


    def print_identification_division(self):
        today = date.today()
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(space * 6 + '* Author  : yeongseon_choe@tmax.co.kr\n')
        self.f.write(space * 6 + '* Data    : ' + today.strftime('%Y. %m. %d') + '\n')
        self.f.write(space * 6 + '* Purpose : ' + str(self.command).upper() + ' ' + str(self.resource).upper() + ' TEST\n')
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + "IDENTIFICATION DIVISION.\n")
        self.f.write(tab + "PROGRAM-ID. " + self.cobfile + ".\n")
        self.f.write(tab + "AUTHOR.     " + "YEONGSEON CHOE.\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write('\n')
        return

    def print_configuration_section(self):
        self.f.write(tab + "CONFIGURATION SECTION.\n")
        return

    def print_input_ouput_section(self):
        self.f.write(tab + "INPUT-OUTPUT SECTION.\n")
        return

    def print_environment_divition(self):
        self.f.write(tab + "ENVIRONMENT DIVISION.\n")
        return

    def print_data_divition(self):
        self.f.write(tab + "DATA DIVISION.\n")
        self.f.write(tab + "WORKING-STORAGE SECTION.\n")

        self.f.write(ws_01.format(tab01, "01 WS-TRANS-ID"               ,"PIC X(4)."            ,""))
        self.f.write(ws_01.format(tab01, '01 WS-MAPSET-NAME'            ,"PIC X(8)."            ,''))
        self.f.write(ws_01.format(tab01, '01 WS-MAP-NAME'               ,"PIC X(8)."            ,''))

        self.f.write('\n')
        self.f.write(ws_01.format(tab01, "01 WS-FIRST-TIME-FLAG"        ,"PIC S9(4) COMP."      ,""))
        self.f.write(ws_88.format(tab88, "88 FIRST-TIME"                ,""                     ,"VALUE 0."))

        self.f.write('\n')
        self.f.write(ws_01.format(tab01, "01 PIC X(1)"                  ,""                     ,"VALUE 'N'."))
        self.f.write(ws_88.format(tab88, "88 NO-FIELD-ERRORS"           ,""                     ,"VALUE 'N'."))
        self.f.write(ws_88.format(tab88, "88 FIELD-ERRORS"              ,""                     ,"VALUE 'F'."))

        self.f.write('\n')
        self.f.write(ws_01.format(tab01, "01 PIC X(1)."                 ,""                    ,""))
        self.f.write(ws_88.format(tab88, "88 THIS-FIELD-GOOD"           ,""                     ,"VALUE 'G'."))
        self.f.write(ws_88.format(tab88, "88 THIS-FILED-BAS"            ,""                     ,"VALUE 'B'."))

        self.f.write('\n')
        self.f.write(ws_01.format(tab01, "01 WS-RESPONSE-CODE"          ,"PIC S9(8) BINARY."    ,""))
        self.f.write(ws_01.format(tab01, "01 WS-RESPONSE-CODE2 "        ,"PIC S9(8) BINARY."    ,""))

        self.f.write(ws_01.format(tab01, "01 WS-COMMUNICATION-AREA"     ,"PIC X(1)."            ,""))
        self.f.write(ws_01.format(tab01, "01 WS-END-MESSAGE"            ,"PIC X(60)."           ,""))

        self.f.write('\n')
        self.f.write(space * 6 + '*' + '-' * 64 + '\n')
        self.f.write(space * 6 + '*' + '  TODO : MOVE COPYBOOK' + '\n')
        self.f.write(space * 6 + '*' + '  ERRMSGS' + '\n')
        self.f.write(space * 6 + '*' + '  STANDARD OSC ERROR MESSAGES' + '\n')
        self.f.write(space * 6 + '*' + '  MATCHES ABRTCODE COPYBOOK MEMBER' + '\n')
        self.f.write(space * 6 + '*' + '-' * 64 + '\n')

        #self.f.write(ws_01.format(tab01, "01 WS-ERROR-MESSAGE."           ,""           ,""))
        self.f.write(tab01 + "01 WS-ERROR-MESSAGES.\n")
        self.f.write('\n')
        self.f.write(tab05 + "05 PIC X(35) VALUE '**  OSC ERROR -- CONTACT HELP DESK'.\n")
        self.f.write(tab05 + "05 PIC X(35) VALUE '-- REPORT THIS INFORMATION **     '.\n")
        self.f.write(tab05 + "05 PIC X(9)  VALUE SPACES.\n")
        self.f.write('\n')
        self.f.write(ws_05.format(tab05, "05 WS-ERROR-LINE1.", "", ""))
        self.f.write(ws_10.format(tab10, "10", "PIC X(14)", "VALUE '   EIBTRNID = '."))
        self.f.write(ws_10.format(tab10, "10 WS-EIBTRNID", "PIC X(4).", ""))
        self.f.write(ws_10.format(tab10, "10", "PIC X(61)", "VALUE SPACES."))
        self.f.write('\n')
        self.f.write(ws_05.format(tab05, "05 WS-ERROR-LINE2.", "", ""))
        self.f.write(ws_10.format(tab10, "10", "PIC X(14)", "VALUE '   EIBSRCE  = '."))
        self.f.write(ws_10.format(tab10, "10 WS-EIBRSRCE", "PIC X(8).", ""))
        self.f.write(ws_10.format(tab10, "10", "PIC X(57)", "VALUE SPACES."))
        self.f.write('\n')
        self.f.write(ws_05.format(tab05, "05 WS-ERROR-LINE3.", "", ""))
        self.f.write(ws_10.format(tab10, "10", "PIC X(14)", "VALUE '   EIBRESP  = '."))
        self.f.write(ws_10.format(tab10, "10 WS-EIBRESP", "PIC ZZZZZZZ9.", ""))
        self.f.write(ws_10.format(tab10, "10", "PIC X(57)", "VALUE SPACES."))
        self.f.write('\n')
        self.f.write(ws_05.format(tab05, "05 WS-ERROR-LINE4.", "", ""))
        self.f.write(ws_10.format(tab10, "10", "PIC X(14)", "VALUE '   EIBRESP2 = '."))
        self.f.write(ws_10.format(tab10, "10 WS-EIBRESP2", "PIC ZZZZZZZ9.", ""))
        self.f.write(ws_10.format(tab10, "10", "PIC X(57)", "VALUE SPACES."))
        self.f.write('\n')
        self.f.write(ws_05.format(tab05, "05 WS-ERROR-LINE5", "PIC X(79)", "VALUE SPACES."))
        self.f.write('\n')
        self.f.write(ws_05.format(tab05, "05 PIC X(79) VALUE ALL '*'.", "", ""))

        self.f.write('\n')
        self.f.write(ws_01.format(tab01, "01 WS-TDQ-NAME "              ,"PIC X(8)"             ,"VALUE '" + ws_tdq_name + "'."))
        self.f.write(ws_01.format(tab01, "01 WS-MESSAGE "               ,"PIC X(40)."           ,""))
        self.f.write(ws_01.format(tab01, "01 WS-MESSAGE-LENGTH"         ,"PIC S9(8) COMP"       ,"VALUE 40."))

        self.f.write('\n')
        self.f.write(space * 6 + '*' + '-' * 64 + '\n')
        self.f.write(space * 6 + '*' + '  TODO : MOVE COPYBOOK' + '\n')
        self.f.write(space * 6 + '*' + '  KEYDEFS' + '\n')
        self.f.write(space * 6 + '*' + '  88-LEVEL CONDITION NAME FOR AID KEYS' + '\n')
        self.f.write(space * 6 + '*' + '-' * 64 + '\n')
        self.f.write(ws_01.format(tab01, "01 EIBAID-TEST-FIELD"          ,"PIC X(1)."    ,""))
        self.f.write(ws_88.format(tab88, "88 NULL-BYTE"                  ,""                     ,"VALUE X'00'."))
        self.f.write(ws_88.format(tab88, "88 ENTER-KEY"                  ,""                     ,"VALUE ''''."))
        self.f.write(ws_88.format(tab88, "88 CLEAR-KEY"                  ,""                     ,"VALUE '_'."))
        self.f.write(ws_88.format(tab88, "88 PF1-KEY"                    ,""                     ,"VALUE '1'."))
        self.f.write(ws_88.format(tab88, "88 PF2-KEY"                    ,""                     ,"VALUE '2'."))
        self.f.write(ws_88.format(tab88, "88 PF3-KEY"                    ,""                     ,"VALUE '3'."))
        self.f.write(ws_88.format(tab88, "88 PF4-KEY"                    ,""                     ,"VALUE '4'."))
        self.f.write(ws_88.format(tab88, "88 PF5-KEY"                    ,""                     ,"VALUE '5'."))
        self.f.write(ws_88.format(tab88, "88 PF6-KEY"                    ,""                     ,"VALUE '6'."))
        self.f.write(ws_88.format(tab88, "88 PF7-KEY"                    ,""                     ,"VALUE '7'."))
        self.f.write(ws_88.format(tab88, "88 PF8-KEY"                    ,""                     ,"VALUE '8'."))
        self.f.write(ws_88.format(tab88, "88 PF9-KEY"                    ,""                     ,"VALUE '9'."))
        self.f.write(ws_88.format(tab88, "88 PF10-KEY"                   ,""                     ,"VALUE ':'."))
        self.f.write(ws_88.format(tab88, "88 PF11-KEY"                   ,""                     ,"VALUE '#'."))
        self.f.write(ws_88.format(tab88, "88 PF12-KEY"                   ,""                     ,"VALUE '@'."))

        self.f.write('\n')
        '''
        self.f.write(space * 6 + '*' + '-' * 64 + '\n')
        self.f.write(space * 6 + '*' + '  TODO : MOVE COPYBOOK' + '\n')
        self.f.write(space * 6 + '*' + '  ATTDEFS' + '\n')
        self.f.write(space * 6 + '*' + '  ATTRIBUTE CONTROL VALUES TO MOVE TO SYMBOLIC MAP' + '\n')
        self.f.write(space * 6 + '*' + '-' * 64 + '\n')
        self.f.write(ws_01.format(tab01, "01 ATTRIBUTE-VALUES-TO-SET."          ,""    ,""))
        self.f.write(ws_05.format(tab05, "05 UNPROT-NORM"                , "PIC X(1)"            ,"VALUE SPACE."))
        self.f.write(ws_05.format(tab05, "05 UNPROT-NORM-MDT"            , "PIC X(1)"            ,"'A'."))
        self.f.write(ws_05.format(tab05, "05 UNPROT-BRT"                 , "PIC X(1)"            ,"'H'."))
        self.f.write(ws_05.format(tab05, "05 UNPROT-BRT-MDT"             , "PIC X(1)"            ,"'I'."))
        self.f.write(ws_05.format(tab05, "05 UNPROT-DARK"                , "PIC X(1)"            ,"'<'."))
        self.f.write(ws_05.format(tab05, "05 UNPROT-DARK-MDT"            , "PIC X(1)"            ,"'('."))
        self.f.write(ws_05.format(tab05, "05 UNPROT-NUM"                 , "PIC X(1)"            ,"'&'."))
        self.f.write(ws_05.format(tab05, "05 UNPROT-NUM-MDT"             , "PIC X(1)"            ,"'J'."))
        self.f.write(ws_05.format(tab05, "05 UNPROT-NUM-BRT"             , "PIC X(1)"            ,"'Q'."))
        self.f.write(ws_05.format(tab05, "05 UNPROT-NUM-BRT-MDT"         , "PIC X(1)"            ,"'R'."))
        self.f.write(ws_05.format(tab05, "05 UNPROT-NUM-DARK"            , "PIC X(1)"            ,"'*'."))
        self.f.write(ws_05.format(tab05, "05 UNPROT-NUM-DARK-MDT"        , "PIC X(1)"            ,"')'."))
        self.f.write(ws_05.format(tab05, "05 PROT-NORM"                  , "PIC X(1)"            ,"'-'."))

        self.f.write('\n')
        '''
        self.print_working_storage_resource()
        self.f.write('\n')
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(space * 6 + '*' * 65 + '\n')
        return

    def print_working_storage_resource(self):

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        self.f.write('\n')
        self.f.write(ws_01.format(tab01, "01 WS-STRUCT-" + str(self.command).upper() + "-" + str(self.resource).upper() + ".",""    ,""))
        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if value == 'data-value':
                type = argument.find('type').text
                if type == "Character":
                    length = argument.find('length').text
                    self.f.write(ws_05.format(tab05, "05 WS-" + str(name).upper(),"PIC X(" + str(length) + ")","VALUE SPACE."))
            if value == 'data-area':
                type = argument.find('type').text
                if type == "Character":
                    length = argument.find('length').text
                    self.f.write(ws_05.format(tab05, "05 WS-" + str(name).upper(),"PIC X(" + str(length) + ")","VALUE SPACE."))
                elif type == "Fullword binary":
                    self.f.write(ws_05.format(tab05, "05 WS-" + str(name).upper(),"PIC S9(8) COMP","VALUE 0."))
                elif type == "Halfword binary":
                    self.f.write(ws_05.format(tab05, "05 WS-" + str(name).upper(),"PIC S9(4) COMP","VALUE 0."))
                elif type == "ABSTIME":
                    self.f.write(ws_05.format(tab05, "05 WS-" + str(name).upper(),"PIC S9(15) COMP-3","VALUE 0."))
                elif type == "digit":
                    self.f.write(ws_05.format(tab05, "05 WS-" + str(name).upper(),"PIC S9(8) COMP","VALUE 0."))

            elif value == 'cvda':
                self.f.write(ws_05.format(tab05, "05 WS-" + str(name).upper(), "PIC S9(8) COMP", "VALUE 0."))


        return

    def print_linkage_section(self):
        self.f.write('\n')
        self.f.write(tab + "LINKAGE SECTION.\n")
        self.f.write(ws_01.format(tab01, "01 DFHCOMMAREA"                 ,"PIC X(1)."                    ,""))
        return

    def print_procedure_divition(self):
        self.f.write('\n')
        self.f.write(tab + "PROCEDURE DIVISION.\n")
        self.f.write('\n')
        self.print_procedure_division_0000_mainline()
        self.f.write('\n')
        self.print_procedure_division_0100_inquire()
        self.f.write('\n')
        self.print_procedure_division_0200_move_data2map()
        self.f.write('\n')
        self.print_procedure_division_0500_normal_processing()
        self.f.write('\n')
        self.print_procedure_division_1000_receive_map()
        self.f.write('\n')
        self.print_procedure_division_1200_send_map_dataonly()
        self.f.write('\n')
        self.print_procedure_division_1300_send_map()
        self.f.write('\n')
        self.print_procedure_division_3333_always_test()
        self.f.write('\n')
        self.print_procedure_division_8000_return_with_trans_id()
        self.f.write('\n')
        self.print_procedure_division_8900_quit()
        self.f.write('\n')
        self.print_procedure_division_9000_first_time()
        self.f.write('\n')
        self.print_procedure_division_9100_clean_the_screen()
        self.f.write('\n')
        self.print_procedure_division_9200_invalid_key_message()
        self.f.write('\n')
        self.print_procedure_division_9999_abort()
        self.f.write('\n')
        return

    def print_procedure_division_0000_mainline(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "0000-MAINLINE.\n")
        self.f.write(tab + tab4 + "PERFORM 3333-ALWAYS-TEST.\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + "EVALUATE" + tab3 + "TRUE\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + tab3 + "WHEN" + tab3 + "FIRST-TIME\n")
        self.f.write(tab + tab4 + tab3 + tab3 + "PERFORM 9000-FIRST-TIME\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + tab3 + "WHEN" + tab3 + "PF3-KEY\n")
        self.f.write(tab + tab4 + tab3 + tab3 + "PERFORM 9100-CLEAN-THE-SCREEN\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + tab3 + "WHEN" + tab3 + "ENTER-KEY\n")
        self.f.write(tab + tab4 + tab3 + tab3 + "PERFORM 0500-NORMAL-PROCESSING\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + tab3 + "WHEN" + tab3 + "OTHER\n")
        self.f.write(tab + tab4 + tab3 + tab3 + "PERFORM 9200-INVALID-KEY-MESSAGE\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + "END-EVALUATE\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + "PERFORM 8000-RETURN-WITH-TRANS-ID.\n")
        return

    def print_procedure_division_0100_inquire(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "0100-INQUIRE-" + str(self.resource).upper() + ".\n")
        self.f.write(tab + tab4 + "DISPLAY \"0100-INQUIRE-" + str(self.resource).upper() + "\".\n")

        self.f.write(tab + tab4 + "EXEC CICS\n")
        self.f.write(tab + tab4 + "     INQUIRE\n")
        '''
        self.f.write(tab + tab4 + "     " +  str(self.resource).upper() + "(WS-" + str(self.resource).upper() + ")\n")
        '''
        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()
        for argument in root.findall('argument'):
            name = argument.get('name')
            self.f.write(tab + tab4 + "     " +  str(name).upper() + "(WS-" + str(name).upper() + ")\n")
        self.f.write(tab + tab4 + "END-EXEC.\n")

        self.f.write('\n')

        for argument in root.findall('argument'):
            name = argument.get('name')
            self.f.write(tab + tab4 + "DISPLAY \"WS-" +  str(name).upper() + "[\"WS-" + str(name).upper() + "\"].\"\n")

        return

    def print_procedure_division_0200_move_data2map(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "0200-MOVE-DATA2MAP.\n")
        self.f.write('\n')

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if value == 'cvda':
                for cvda in argument.findall('cvda'):
                    self.f.write(tab + tab4 + "IF WS-" + name + " = DFHVALUE(" + cvda.text + ")\n")
                    self.f.write(tab + tab4 + tab4 + "MOVE \'" + str(cvda.text).title() + "\' TO " + name + "O.\n");
                self.f.write('\n')
        return

    def print_procedure_division_0500_normal_processing(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "0500-NORMAL-PROCESSING.\n")
        self.f.write(tab + tab4 + "PERFORM 1000-RECEIVE-MAP.\n")

        return

    def print_procedure_division_1000_receive_map(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "1000-RECEIVE-MAP.\n")
        self.f.write(tab + tab4 + "EXEC CICS\n")
        self.f.write(tab + tab4 + "     RECEIVE\n")
        self.f.write(tab + tab4 + "     MAP           (WS-MAP-NAME)\n")
        self.f.write(tab + tab4 + "     MAPSET        (WS-MAPSET-NAME)\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + "     INTO          ()\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + "     RESP          (WS-RESPONSE-CODE)\n")
        self.f.write(tab + tab4 + "END-EXEC.\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + "EVALUATE WS-RESPONSE-CODE\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + "WHEN     DFHRESP   (NORMAL)\n")
        self.f.write(tab + tab4 + tab4 + "CONTINUE\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + "WHEN     DFHRESP   (MAPFAIL)\n")
        self.f.write(tab + tab4 + tab4 + 'MOVE \'NO CODE OR ID ENTERED\' TO MSGO\n')
        self.f.write(tab + tab4 + tab4 + "PERFORM 1200-SEND-MAP-DATAONLY\n")
        self.f.write(tab + tab4 + tab4 + "PERFORM 8000-RETURN-WITH-TRANS-ID\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + "WHEN     OTHER\n")
        self.f.write(tab + tab4 + tab4 + "PERFORM 9999-ABORT\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + "END-EVALUATE.\n")
        return

    def print_procedure_division_1200_send_map_dataonly(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "1200-SEND-MAP-DATAONLY.\n")
        self.f.write(tab + tab4 + "EXEC CICS\n")
        self.f.write(tab + tab4 + "     SEND\n")
        self.f.write(tab + tab4 + "     MAP           (WS-MAP-NAME)\n")
        self.f.write(tab + tab4 + "     MAPSET        (WS-MAPSET-NAME)\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + "     FROM          ()\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + "     DATAONLY\n")
        self.f.write(tab + tab4 + "END-EXEC.\n")
        return

    def print_procedure_division_1300_send_map(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "1300-SEND-MAP.\n")
        self.f.write(tab + tab4 + "EXEC CICS\n")
        self.f.write(tab + tab4 + "     SEND\n")
        self.f.write(tab + tab4 + "     MAP           (WS-MAP-NAME)\n")
        self.f.write(tab + tab4 + "     MAPSET        (WS-MAPSET-NAME)\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + "     FROM          ()\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + "     ERASE\n")
        self.f.write(tab + tab4 + "END-EXEC.\n")
        return

    def print_procedure_division_3333_always_test(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "3333-ALWAYS-TEST.\n")
        self.f.write(tab + tab4 + move_to.format('EIBAID', 'EIBAID-TEST-FIELD.'))
        self.f.write('\n')
        self.f.write(tab + tab4 + "IF  CLEAR-KEY\n")
        self.f.write(tab + tab4 + tab3 + "PERFORM 8900-QUIT.\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + move_to.format('EIBCALEN', 'WS-FIRST-TIME-FLAG.'))
        return


    def print_procedure_division_8000_return_with_trans_id(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "8000-RETURN-WITH-TRANS-ID.\n")
        self.f.write(tab + tab4 + "EXEC CICS\n")
        self.f.write(tab + tab4 + "     RETURN\n")
        self.f.write(tab + tab4 + "     TRANSID       (WS-TRANS-ID)\n")
        self.f.write(tab + tab4 + "     COMMAREA      (WS-COMMUNICATION-AREA)\n")
        self.f.write(tab + tab4 + "     LENGTH        (LENGTH OF WS-COMMUNICATION-AREA)\n")
        self.f.write(tab + tab4 + "END-EXEC.\n")
        return

    def print_procedure_division_8900_quit(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "8900-QUIT.\n")
        self.f.write(tab + tab4 + "EXEC CICS\n")
        self.f.write(tab + tab4 + "     SEND TEXT \n")
        self.f.write(tab + tab4 + "     FROM          (WS-END-MESSAGE)\n")
        self.f.write(tab + tab4 + "     ERASE\n")
        self.f.write(tab + tab4 + "     FREEKB\n")
        self.f.write(tab + tab4 + "END-EXEC.\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + "EXEC CICS\n")
        self.f.write(tab + tab4 + "     RETURN\n")
        self.f.write(tab + tab4 + "END-EXEC.\n")
        return

    def print_procedure_division_9000_first_time(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "9000-FIRST-TIME.\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + move_to.format('LOW-VALUES', 'XXXXXXX.'))
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + tab4 + "PERFORM 0100-INQUIRE-" + str(self.resource).upper() + ".\n")
        self.f.write(tab + tab4 + "PERFORM 0200-MOVE-DATA2MAP.\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + "EXEC CICS\n")
        self.f.write(tab + tab4 + "     SEND MAP      (WS-MAP-NAME)\n")
        self.f.write(tab + tab4 + "     MAPSET        (WS-MAPSET-NAME)\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + "     FROM          (XXXXXXX)\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + "     ERASEAUP\n")
        self.f.write(tab + tab4 + "     CURSOR\n")
        self.f.write(tab + tab4 + "END-EXEC.\n")
        return

    def print_procedure_division_9100_clean_the_screen(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "9100-CLEAN-THE-SCREEN.\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + move_to.format('LOW-VALUES', 'XXXXXXX.'))
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + 'MOVE \'ENTER VALUE, PRESS <ENTER>, <CLEAR> TO QUIT\'\n')
        self.f.write(tab + tab4 + tab4 + 'TO MSGO.\n')
        self.f.write(tab + tab4 + "EXEC CICS\n")
        self.f.write(tab + tab4 + "     SEND MAP      (WS-MAP-NAME)\n")
        self.f.write(tab + tab4 + "     MAPSET        (WS-MAPSET-NAME)\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + "     FROM          (XXXXXXX)\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + "     DATAONLY\n")
        self.f.write(tab + tab4 + "     ERASEAUP\n")
        self.f.write(tab + tab4 + "     CURSOR\n")
        self.f.write(tab + tab4 + "END-EXEC.\n")
        return

    def print_procedure_division_9200_invalid_key_message(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "9200-INVALID-KEY-MESSAGE.\n")
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + move_to.format('LOW-VALUES', 'XXXXXXX.'))
        self.f.write(space * 6 + '*' * 65 + '\n')
        self.f.write(tab + tab4 + 'MOVE \'YOU PRESSED WRONG KEY! PRESS <ENTER>, <CLEAR> TO QUIT\'\n')
        self.f.write(tab + tab4 + tab4 + 'TO MSGO.\n')
        self.f.write(tab + tab4 + "PERFORM 1200-SEND-MAP-DATAONLY.\n")
        return

    def print_procedure_division_9999_abort(self):
        self.f.write(space * 6 + '*' + '-' * 65 + '\n')
        self.f.write('\n')
        self.f.write(tab + "9999-ABORT.\n")
        self.f.write(tab + tab4 + move_to.format('EIBTRNID', 'WS-EIBTR`NID.'))
        self.f.write(tab + tab4 + move_to.format('EIBRSRCE', 'WS-EIBRSRCE.'))
        self.f.write(tab + tab4 + move_to.format('EIBRESP', 'WS-EIBRESP.'))
        self.f.write(tab + tab4 + move_to.format('EIBRESP2', 'WS-EIBRESP2.'))
        self.f.write('\n')
        self.f.write(tab + tab4 + "EXEC CICS\n")
        self.f.write(tab + tab4 + "     SEND TEXT\n")
        self.f.write(tab + tab4 + "     FROM          (WS-ERROR-MESSAGES)\n")
        self.f.write(tab + tab4 + "     ERASE\n")
        self.f.write(tab + tab4 + "     ALARM\n")
        self.f.write(tab + tab4 + "     FREEKB\n")
        self.f.write(tab + tab4 + "END-EXEC.\n")
        self.f.write('\n')
        self.f.write(tab + tab4 + "EXEC CICS\n")
        self.f.write(tab + tab4 + "     RETURN\n")
        self.f.write(tab + tab4 + "END-EXEC.\n")
        return
