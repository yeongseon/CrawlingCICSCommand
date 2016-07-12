from datetime import date
import re
import xml.etree.ElementTree as ET

defult_url = 'http://www-01.ibm.com/support/knowledgecenter/api/content/nl/ko/SSGMCP_4.2.0/com.ibm.cics.ts.systemprogramming.doc/commands/dfha8_{}.html'
output_syntax_full = 'output_syntax/{}_full.txt'
output_syntax = 'output_syntax/{}.txt'
output_syntax_html = 'output_syntax/{}.html'
input_xml = 'output_xml/{}.xml'
output_mapset = 'TESTSPI'
output_map = 'output_map/{}'

max_cloumn = 72

mapset_define_type                  = "{:8s} DFHMSD TYPE={}"
mapset_define_lang                  = "LANG={}"
mapset_define_mode                  = "MODE={}"
mapset_define_ctrl                  = "CTRL={}"
mapset_define_storage               = "STORAGE={}"
mapset_define_tioapfx               = "TIOAPFX={}"

map_define_size                     = "{:8s} DFHMDI SIZE=(24, 80)"
map_define_line                     = "LINE={}"
map_define_column                   = "COLUMN={}"

field_fmt                           = "{:8s} DFHMDF POS=({:2d},{:2d})"
long_field_fmt                      = "{:29s} DFHMDF POS=({:2d},{:2d})"

#lenth_fmt                           = "               LENGTH={:2d},"
lenth_fmt                           = "LENGTH={:2d}"
screen_label_attrb_fmt              = "ATTRB=(BRT,PROT)"
enterable_numeric_field_fmt         = "ATTRB=(BRT,UNPROT,NUM)"
enterable_alphanumeric_field_fmt    = "ATTRB=(BRT,UNPROT)"
sttoper_field_fmt                   = "ATTRB=(DRK,PROT)"
blue_color_field_fmt                = "COLOR=BLUE"
green_color_field_fmt               = "COLOR=GREEN"
white_color_field_fmt               = "COLOR=WHITE"
red_color_field_fmt                 = "COLOR=RED"
yellow_color_field_fmt              = "COLOR=YELLOW"
initial_field_fmt_14                = "INITIAL='{:14s}:'"
initial_field_fmt                   = "INITIAL='{}'"

color_field_fmt                     = "COLOR={}"
initial_field_fmt                   = "INITIAL='{}'"
outline_field_fmt                   = "OUTLINE={}"
attrb_field_fmt                     = "ATTRB=({})"


class genMap(object):
    def __init__(self, command, resource):
        self.command = command
        self.resource = resource
        self.systemcommand = self.command + self.resource
        return

    def __del__(self):        
        return

    def print_separate_line(self, file):
        for i in range(0, max_cloumn - 1):  # 71번까지 출 체크
            file.write('*')
        file.write('\n')

    def print_filed(self, file, x, y, field_name, field_value, field_type, field_length, field_initail):
        pos_x = x
        pos_y = y
        temp = field_fmt.format('        ', pos_x, pos_y) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(15) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        label_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(label_field)

        temp = ' '.rjust(15) + blue_color_field_fmt + ','
        color_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(color_field)

        temp = ' '.rjust(15) + initial_field_fmt_14.format(field_name.upper())
        initial_field = temp + '\n'
        file.write(initial_field)

        pos_y = pos_y + 16
        if len(field_name) > 8 :
            temp = long_field_fmt.format(field_name.upper(), pos_x, pos_y) + ','
            pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
            file.write(pos_filed)
        else :
            temp = field_fmt.format(field_name.upper(), pos_x, pos_y) + ','
            pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
            file.write(pos_filed)

        if field_value == 'cvda' :
            pos_y = pos_y + 15 + 1
            temp = ' '.rjust(15) + lenth_fmt.format(15) + ','
        elif field_value == 'data-area' :
            pos_y = pos_y + field_length + 1
            temp = ' '.rjust(15) + lenth_fmt.format(field_length) + ','
        elif field_value == 'data-value' :
            pos_y = pos_y + field_length + 1
            temp = ' '.rjust(15) + lenth_fmt.format(field_length) + ','

        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        label_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(label_field)

        temp = ' '.rjust(15) + blue_color_field_fmt
        color_field = temp + '\n'
        file.write(color_field)

        # stopper field
        temp = field_fmt.format('        ', pos_x, pos_y) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(1) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + sttoper_field_fmt
        label_field = temp + '\n'
        file.write(label_field)

        if field_initail:
            temp = field_fmt.format('        ', pos_x, 40) + ','
            pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
            file.write(pos_filed)

            temp = ' '.rjust(15) + lenth_fmt.format(len(field_initail)) + ','
            len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
            file.write(len_field)

            temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
            label_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
            file.write(label_field)

            temp = ' '.rjust(15) + blue_color_field_fmt + ','
            color_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
            file.write(color_field)

            temp = ' '.rjust(15) + initial_field_fmt.format(field_initail)
            initial_field = temp + '\n'
            file.write(initial_field)


        return

    def print_dfhmdf(self, file, pos_x, pos_y, field_name, field_value, field_type, field_length, field_initial=""):
        x = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        y = [5, 40]
        self.print_filed(file, int(x[pos_x]), int(y[pos_y]), field_name=field_name, field_value=field_value,
                         field_type = field_type, field_length=field_length, field_initail=field_initial)
        self.print_separate_line(file)
        return


    def print_mapset_define(self, file):
        temp = mapset_define_type.format(output_mapset, '&SYSPARAM') + ','
        label_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(label_field)

        temp = ' '.rjust(15) + mapset_define_lang.format('COBOL') + ','
        label_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(label_field)

        temp = ' '.rjust(15) + mapset_define_mode.format('INOUT') + ','
        label_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(label_field)

        temp = ' '.rjust(15) + mapset_define_ctrl.format('FREEKB') + ','
        label_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(label_field)

        temp = ' '.rjust(15) + mapset_define_storage.format('AUTO') + ','
        label_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(label_field)

        temp = ' '.rjust(15) + mapset_define_tioapfx.format('YES')
        label_field = temp + '\n'
        file.write(label_field)

        self.print_separate_line(file)
        return

    def print_mapset_final(self, file):
        temp = mapset_define_type.format(output_mapset, 'FINAL')
        label_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(label_field)

        file.write("         END")

        return

    def print_map_define(self, file, filename):
        temp = map_define_size.format(filename) + ','
        label_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(label_field)

        temp = ' '.rjust(15) + map_define_line.format('1') + ','
        label_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(label_field)

        temp = ' '.rjust(15) + map_define_column.format('1')
        label_field = temp + '\n'
        file.write(label_field)

        self.print_separate_line(file)
        return

    def print_subject(self, file):
        text = '** System Programming Command Test **'
        temp = field_fmt.format('        ', 1, 22) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + color_field_fmt.format("WHITE") + ','
        color_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(color_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        temp = field_fmt.format('        ', 3, 2) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(77) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + blue_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + outline_field_fmt.format('OVER')
        len_field = temp + '\n'
        file.write(len_field)

        temp = field_fmt.format('        ', 3, 80) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(1) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + sttoper_field_fmt
        len_field = temp + '\n'
        file.write(len_field)

        self.print_separate_line(file)
        return

    def print_copyright(self, file):

        temp = field_fmt.format('        ', 23, 2) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(77) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + blue_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + outline_field_fmt.format('OVER')
        len_field = temp + '\n'
        file.write(len_field)

        temp = field_fmt.format('        ', 23, 80) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(1) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + sttoper_field_fmt
        len_field = temp + '\n'
        file.write(len_field)

        text = 'CopyRight(c) 2015, Tmaxsoft, All Rights Reserved.'
        temp = field_fmt.format('        ', 24, 29) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + color_field_fmt.format("BLUE") + ','
        color_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(color_field)

        file.write("               INITIAL='CopyRight(c) 2015, Tmaxsoft, All Rights ReserveX\n")
        file.write("               d.'\n")

        self.print_separate_line(file)
        return

    def print_msg(self, file):
        temp = field_fmt.format('        ', 21, 2) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(76) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + yellow_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        file.write("               INITIAL='***< MESSAGE >*********************************X\n")
        file.write("               ********************************'\n")

        self.print_separate_line(file)
        return

    def print_menu(self, file):
        text = 'ENTER'
        temp = field_fmt.format('        ', 22, 2) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + red_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'F1'
        temp = field_fmt.format('        ', 22, 10) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + blue_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'Help'
        temp = field_fmt.format('        ', 22, 13) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + red_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'F3'
        temp = field_fmt.format('        ', 22, 20) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + blue_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'Exit'
        temp = field_fmt.format('        ', 22, 23) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + red_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'F7'
        temp = field_fmt.format('        ', 22, 30) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + blue_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'Backword'
        temp = field_fmt.format('        ', 22, 33) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + red_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'F8'
        temp = field_fmt.format('        ', 22, 44) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + blue_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'Forward'
        temp = field_fmt.format('        ', 22, 47) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + red_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'F9'
        temp = field_fmt.format('        ', 22, 57) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + blue_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'Action'
        temp = field_fmt.format('        ', 22, 61) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + red_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'F10'
        temp = field_fmt.format('        ', 22, 69) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + blue_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        text = 'Cancel'
        temp = field_fmt.format('        ', 22, 73) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + red_color_field_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        self.print_separate_line(file)
        return

    def print_resource(self, file, command, resource, index, length):
        text = str(command).upper() + " " + str(resource).upper() + "("

        temp = field_fmt.format('        ', 4, 5) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(len(text)) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + color_field_fmt.format("BLUE") + ','
        color_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(color_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(text)
        initial_field = temp + '\n'
        file.write(initial_field)

        temp = field_fmt.format(str(resource).upper() + str(index), 4, 5 + len(text) + 1) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(length) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + color_field_fmt.format("WHITE")
        color_field = temp + '\n'
        file.write(color_field)

        temp = field_fmt.format('        ', 4, 5 + len(text) + 1 + length + 1) + ','
        pos_filed = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(pos_filed)

        temp = ' '.rjust(15) + lenth_fmt.format(1) + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + screen_label_attrb_fmt + ','
        len_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(len_field)

        temp = ' '.rjust(15) + color_field_fmt.format("BLUE") + ','
        color_field = temp + 'X\n'.rjust(max_cloumn-len(temp)+1, ' ')
        file.write(color_field)

        temp = ' '.rjust(15) + initial_field_fmt.format(')')
        initial_field = temp + '\n'
        file.write(initial_field)

        self.print_separate_line(file)
        return

    def print_inquire_map(self):

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        size = len(root.findall('argument'))

        filename = []
        file = []
        for i in range(0, int(size/20) + 1) :
            filename.append(output_map.format(str(self.command[0:3]).upper() + str(self.resource[0:3]).upper() + str(i)) + ".map")
            file.append(open(filename[i], mode='w', encoding='utf-8'))
            self.print_mapset_define(file[i])
            self.print_map_define(file[i], str(self.command[0:3]).upper() + str(self.resource[0:3]).upper() + str(i))

            for argument in root.findall('argument'):
                name = argument.get('name')
                if (str(name).upper() == str(self.resource).upper()):
                    length = int(argument.find('length').text)
                    self.print_subject(file[i])
                    self.print_resource(file[i], self.command, self.resource, i, length)

        count = 0
        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if (str(name).upper() != str(self.resource).upper()):
                if value == 'data-area':
                    type = argument.find('type').text
                    if type == "Character":
                        length = int(argument.find('length').text)
                        if (length > 16):
                            length = 16
                    else:
                        length = 15
                    self.print_dfhmdf(file[int(count/20)], int(count%10), int(int(count/10)%2),
                                      field_name=name, field_value=value, field_type=type, field_length=length)

                elif value == 'cvda':
                    self.print_dfhmdf(file[int(count/20)], int(count%10), int(int(count/10)%2),
                                      field_name=name, field_value='cvda', field_type='cvda', field_length=15)
                count = count + 1

        for f in file:
            self.print_msg(f)
            self.print_menu(f)
            self.print_copyright(f)
            self.print_mapset_final(f)

        return

    def print_set_map(self):

        xml_file = input_xml.format(self.systemcommand)
        xml = ET.parse(xml_file)
        root = xml.getroot()

        size = len(root.findall('argument'))

        filename = []
        file = []
        for i in range(0, int(size/20) + 1) :
            filename.append(output_map.format(str(self.command[0:3]).upper() + str(self.resource[0:3]).upper() + str(i)) + ".map")
            file.append(open(filename[i], mode='w', encoding='utf-8'))
            self.print_mapset_define(file[i])
            self.print_map_define(file[i], str(self.command[0:3]).upper() + str(self.resource[0:3]).upper() + str(i))

            for argument in root.findall('argument'):
                name = argument.get('name')
                if (str(name).upper() == str(self.resource).upper()):
                    length = int(argument.find('length').text)
                    self.print_subject(file[i])
                    self.print_resource(file[i], self.command, self.resource, i, length)

        count = 0
        for argument in root.findall('argument'):
            name = argument.get('name')
            value = argument.find('value').text

            if (str(name).upper() != str(self.resource).upper()):

                if value == 'data-value':
                    type = argument.find('type').text
                    initial = ""
                    if type == "Character":
                        length = int(argument.find('length').text)
                        if length > 16:
                            initial = "{} - Character".format(str(length))
                            length = 16
                        else:
                            initial = "{} - Character".format(str(length))
                    elif type == "Fullword binary":
                        length = 15
                        initial = "{} - {}".format(argument.find('start').text, argument.find('end').text)
                    elif type == "Halfword binary":
                        length = 15
                        initial = "{} - {}".format(argument.find('start').text, argument.find('end').text)
                    else:
                        length = 15

                    self.print_dfhmdf(file[int(count/20)], int(count%10), 0,
                                      field_name=name, field_value=value, field_type=type, field_length=length, field_initial=initial)

                elif value == 'cvda':
                    cvda_list = []
                    for cvda in argument.findall('cvda'):
                        cvda_list.append(cvda.text)

                    initial = " | ".join(cvda_list)

                    initial = "(" + initial + ")"

                    self.print_dfhmdf(file[int(count/20)], int(count%10), 0,
                                      field_name=name, field_value='cvda', field_type='cvda', field_length=15, field_initial=initial)
                count = count + 1


        for f in file:
            self.print_msg(f)
            self.print_menu(f)
            self.print_copyright(f)
            self.print_mapset_final(f)

        return
