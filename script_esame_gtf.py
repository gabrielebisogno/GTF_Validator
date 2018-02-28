#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from time import *
from termcolor import colored
#-------------------------------------------------------------------------------
#Funzioni

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def print_status(code, i, stream = 0, error_code = '', arg1 = '', arg2 = '', arg3 = ''):

    if stream == 0:
        if code == 'ok':
            print(colored("Riga " + str(i) +" --->  sintatticamente corretta", "green"))
    else:
        if error_code == 'bad_tran':
            text1 = "Identificatore di trascrizione (transcript_id) non valido ---> " + arg1 + " " + "\n.......\n"

        elif error_code == 'bad_gene_id':
            text1 = "Identificatore del gene (gene_id) non valido ---> " + arg1 + " " + "\n.......\n"

        elif error_code == 'bad_attribute_form':
            text1 = "Forma attributi non corretta ---> "  + arg1  + "\n.......\n" #da sistemare

        elif error_code == 'bad_strand':
            text1 = ("Valore campo strand non valido ---> " + arg1 + "\n.......\n")

        elif error_code == 'bad_frame':
            text1 = ("Valore campo frame non valido ---> " + arg1 + "\n.......\n")

        elif error_code == 'bad_length':
            text1 = ("Lunghezza start/stop codon non corretta ---> " + str(arg1) + "\n.......\n")

        elif error_code == 'bad_feature':
            text1 = "Il valore della feature è scorretto ---> " + arg1 + " ;\n.......\n"

        elif error_code == 'bad_index':
            text1 = "I valori di inizio o fine feature non sono corretti ---> " + arg1 + ' ' + arg2 + "\n.......\n"

        elif error_code == 'bad_score':
            text1 = "Il valore di score non è corretto ---> " + arg1 + "\n.......\n"

        elif error_code == 'id_sorg':
            text1 = "Il valore dell'id sorgente non corrisponde a quello aspettato (" + idsorg + ") ---> " + arg1 + "\n.......\n"

        elif error_code == 'software':
            text1 = "Il nome software non corrisponde a quello aspettato (" + software + ") ---> " + arg1 + "\n.......\n"

        elif error_code == 'not_empty_gene_value':
            text1 = "Il campo gene_value non è vuoto ---> " + arg1 + "\n.......\n"

        elif error_code == 'not_empty_tran_value':
            text1 = "Il campo transcript_value non è vuoto ---> " + arg1 + "\n.......\n"

        else:
            text1 = "Codice errore sconosciuto"

        if code == 'bad':
            print(colored("Riga " + str(i) +" --->  sintatticamente non corretta", "red"))

        sleep(0.5)
        text = "----------------Causa_Errore-------------------\n"

        print_stream(text)
        print_stream(text1)


def print_stream(text):
    for char in text:
       sys.stdout.write(char)
       sys.stdout.flush()
       sleep(0.05)


def attribute_check(attributes, j, flag, empty = 0):

    try:
        attr = re.search('^(\w+)\s\"(\S*)\";\s(\w+)\s\"(\S*)\";(\s(\w+)\s\"(\S*)\";)*(\s+#+.*)*$', attributes)
        tran_id = attr.group(1)
        tran_value =attr.group(2)
        gene_id =attr.group(3)
        gene_value = attr.group(4)

        if tran_id == "transcript_id":

            if gene_id == "gene_id":

                if empty == 0:

                    print_status('ok',i)

                else:

                    if tran_value == '':

                        if gene_value == '':

                            print_status('ok',i)

                        else:
                            j = j + 1
                            flag = False
                            print_status('bad', i, 1, 'not_empty_gene_value', gene_value)

                    else:
                        j = j + 1
                        flag = False
                        print_status('bad', i, 1, 'not_empty_tran_value', tran_value)

            else:
                j = j + 1
                flag = False
                print_status('bad', i, 1, 'bad_gene_id', gene_id)

        else:
            j = j + 1
            flag = False
            print_status('bad', i, 1, 'bad_tran', tran_id)

    except Exception:
        j = j + 1
        flag = False
        print_status('bad', i, 1, 'bad_attribute_form', attributes)

    return j, flag

#-------------------------------------------------------------------------------

with open(sys.argv[1],'r') as gtf_input_file:
    gtf_file_rows = gtf_input_file.readlines()

flag = True
i = 0
j = 0


print("-----------------------------------------------------------------------")
print("---------------------------SCRIPT_EXECUTE------------------------------")
print("-----------------------------------------------------------------------")
print("\n")
text= "--------------------------Controllo_File_GTF---------------------------\n\n"
text1="Esecuzione controllo...\n"

print_stream(text)

print("File ----> " + sys.argv[1] + "\n")

print_stream(text1)

first_line = True

for row in gtf_file_rows:
    sleep(0.05)
    i = i + 1
    record_list = row.rstrip().split('\t')

    search_comments = re.search('^#+.*$',record_list[0])
    if search_comments is not None:
        print(colored('Riga ' + str(i) + ' di commento ', 'green'))

    else:

        if first_line:
            idsorg = record_list[0]
            software = record_list[1]
            text = 'id sorgente: ' + idsorg +'\n'
            print_stream(text)
            text = 'software: ' + software + '\n'
            print_stream(text)
            first_line = False

        if is_number(record_list[3]) and is_number(record_list[4]) and ( int(record_list[3]) < int(record_list[4])) :

            if record_list[5] == '.' or is_number(record_list[5]):

                if record_list[0] == idsorg :

                    if record_list[1] == software:

                        if record_list[6] == "-" or record_list[6] == "+":

                            if record_list[2] == "exon":

                                if record_list[7] == '.':

                                    j, flag = attribute_check(record_list[8], j, flag)

                                else:
                                    j = j + 1
                                    flag = False
                                    print_status('bad', i, 1, 'bad_frame', record_list[7])

                            elif record_list[2] == "CDS":

                                if int(record_list[7])>=0 and int(record_list[7])<= 2:

                                    j, flag = attribute_check(record_list[8], j, flag)

                                else:
                                    j = j + 1
                                    flag = False
                                    print_status('bad', i, 1, 'bad_frame', record_list[7])

                            elif (record_list[2] == 'start_codon' or record_list[2] == 'stop_codon'):

                                if (int(record_list[4]) - int(record_list[3])) <= 2:

                                    if int(record_list[7]) <= 2 and int(record_list[7]) >= 0 :

                                        j, flag = attribute_check(record_list[8], j, flag)

                                    else:
                                        j = j + 1
                                        flag = False
                                        print_status('bad', i, 1, 'bad_frame', record_list[7])

                                else:
                                    j = j + 1
                                    flag = False
                                    print_status('bad', i, 1, 'bad_length', int(record_list[4]) - int(record_list[3]))

                            elif (record_list[2] == '5UTR' or record_list[2] == '3UTR'):

                                if record_list[7] == '.':

                                    j, flag = attribute_check(record_list[8], j, flag)

                                else:
                                    j = j + 1
                                    flag = False
                                    print_status('bad', i, 1, 'bad_frame', record_list[7])

                            elif (record_list[2] == 'inter' or record_list[2] == 'inter_CNS'):

                                if record_list[7] == '.':

                                    j, flag = attribute_check(record_list[8], j, flag, 1)

                                else:
                                    j = j + 1
                                    flag = False
                                    print_status('bad', i, 1, 'bad_frame', record_list[7])

                            elif (record_list[2] == 'intron_CNS'):

                                if record_list[7] == '.':

                                    j, flag = attribute_check(record_list[8], j, flag)

                                else:
                                    j = j + 1
                                    flag = False
                                    print_status('bad', i, 1, 'bad_frame', record_list[7])

                            else:
                                j = j + 1
                                flag = False
                                print_status('bad', i, 1, 'bad_feature', record_list[2])

                        else:
                            j = j + 1
                            flag = False
                            print_status('bad', i, 1, 'bad_strand', record_list[6])

                    else:
                        j = j + 1
                        flag = False
                        print_status('bad', i, 1, 'software', record_list[1])

                else:
                    j = j + 1
                    flag = False
                    print_status('bad', i, 1, 'id_sorg', record_list[0])

            else:
                j = j + 1
                flag = False
                print_status('bad', i, 1, 'bad_score', record_list[5])

        else:
            j = j + 1
            flag = False
            print_status('bad', i, 1, 'bad_index', record_list[3], record_list[4])


text = ".....\n"
print_stream(text)

print("-----------------------------------------------------------------------")
print("-------------------Esito_Finale_Controllo-----------------------------\n")
sleep(1)

text = "Il file ha " + str(j) +" righe sintatticamente non corrette\n\n"
print_stream(text)

if flag:
    print(colored("File " + sys.argv[1] +  " Sintatticamente CORRETTO", "green"))
else:
    print(colored("--------------File " + sys.argv[1] +  " Sintatticamente NON corretto---------------\n", "red"))

print("-----------------------------------------------------------------------")
print("---------------------------SCRIPT_END----------------------------------")
print("-----------------------------------------------------------------------")
