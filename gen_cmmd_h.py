
cre_res = ['connection', 'file', 'journalmodel', 'program', 'tdqueue', 'terminal', 'tranclass', 'transaction', 'tsmodel', 'typeterm', 'webservice']
dis_res = ['connection', 'file', 'journalmodel', 'program', 'tdqueue', 'terminal', 'tranclass', 'transaction', 'tsmodel', 'webservice']
inq_res = ['connection', 'file', 'journalmodel', 'program', 'tdqueue', 'terminal', 'tranclass', 'transaction', 'tsmodel','webservice']
set_res = ['connection', 'file', 'program', 'tdqueue', 'terminal', 'tranclass', 'transaction', 'tsmodel','webservice']

filelist = []
for i in cre_res:
    file = 'spi/output_code/' + i + '/cics_cmmd_create_' + i + '.h'
    filelist.append(file)
    
with open('spi/output_code/cmmd_h/cics_spi_create_cmmd.h', 'w') as outfile:
    for file in filelist:
        try:
            infile = open(file)
        except FileNotFoundError:
            pass
        else:
            outfile.write(infile.read())
            outfile.write('\n')


filelist = []
for i in cre_res:
    file = 'spi/output_code/' + i + '/cics_cmmd_discard_' + i + '.h'
    filelist.append(file)
    
with open('spi/output_code/cmmd_h/cics_spi_discard_cmmd.h', 'w') as outfile:
    for file in filelist:
        try:
            infile = open(file)
        except FileNotFoundError:
            pass
        else:
            outfile.write(infile.read())
            outfile.write('\n')

filelist = []
for i in set_res:
    file = 'spi/output_code/' + i + '/cics_cmmd_set_' + i + '.h'
    filelist.append(file)
    
with open('spi/output_code/cmmd_h/cics_spi_set_cmmd.h', 'w') as outfile:
    for file in filelist:
        try:
            infile = open(file)
        except FileNotFoundError:
            pass
        else:
            outfile.write(infile.read())
            outfile.write('\n')

filelist = []
for i in set_res:
    file = 'spi/output_code/' + i + '/cics_cmmd_inquire_' + i + '.h'
    filelist.append(file)
    
with open('spi/output_code/cmmd_h/cics_spi_inquire_cmmd.h', 'w') as outfile:
    for file in filelist:
        try:
            infile = open(file)
        except FileNotFoundError:
            pass
        else:
            outfile.write(infile.read())
            outfile.write('\n')
