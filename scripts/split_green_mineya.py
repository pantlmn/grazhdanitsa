from lxml import etree
import os, re

namespaces = {'w':'{http://www.gribuser.ru/xml/fictionbook/2.0}'}


delete_punctiation = {r'[,.!?\(\)\[\];\t\n\r]' : '',
r'\s+' : ' '}

latinize = {
r'[ьъ]([АИОУЫЭаиоуыэ])' : r'y\1',
r'($|[АЕИОУЫЭЮЯаеиоуыэюя])е' : r'\1ye',
'А' : 'A',
'Б' : 'B',
'В' : 'V',
'Г' : 'G',
'Д' : 'D',
'Е' : 'E',
'Ё' : 'Yo',
'Ж' : 'Zh',
'З' : 'Z',
'И' : 'I',
'Й' : 'Y',
'К' : 'K',
'Л' : 'L',
'М' : 'M',
'Н' : 'N',
'О' : 'O',
'П' : 'P',
'Р' : 'R',
'С' : 'S',
'Т' : 'T',
'У' : 'U',
'Ф' : 'F',
'Х' : 'Kh',
'Ц' : 'Ts',
'Ч' : 'Ch',
'Ш' : 'Sh',
'Щ' : 'Shch',
'Ъ' : '',
'Ы' : 'Y',
'Ь' : '',
'Э' : 'E',
'Ю' : 'Yu',
'Я' : 'Ya',
'а' : 'a',
'б' : 'b',
'в' : 'v',
'г' : 'g',
'д' : 'd',
'е' : 'e',
'ё' : 'yo',
'ж' : 'zh',
'з' : 'z',
'и' : 'i',
'й' : 'y',
'к' : 'k',
'л' : 'l',
'м' : 'm',
'н' : 'n',
'о' : 'o',
'п' : 'p',
'р' : 'r',
'с' : 's',
'т' : 't',
'у' : 'u',
'ф' : 'f',
'х' : 'kh',
'ц' : 'ts',
'ч' : 'ch',
'ш' : 'sh',
'щ' : 'shch',
'ъ' : '',
'ы' : 'y',
'ь' : '',
'э' : 'e',
'ю' : 'yu',
'я' : 'ya',
chr(0x0301) : '',
'†' : '+',
':' : '',
'/' : ''}

def sub_by_dictionary(string, dictionary):
    for item in dictionary.keys():
        string = re.sub(item, dictionary[item], string)
    return string

def day_txt_ru(node):
    full_text = etree.tostring(node, method='text', encoding='unicode').strip()
    full_text = sub_by_dictionary(full_text, delete_punctiation)
    return(full_text)


def modify_day_txt(node):
    full_text = etree.tostring(node, method='text', encoding='unicode').strip()
    full_text = sub_by_dictionary(full_text, delete_punctiation)
    full_text = '_'.join(full_text.split(' ')[:5])
    full_text = sub_by_dictionary(full_text, latinize)
    return(full_text)

# input_files = {
# 9: '17580-Минея-Сентябрь-(гражданским-шрифтом).fb2',
# 1 : '19482-Минея-Январь-(гражданским-шрифтом).fb2',
# 10 : '20290-Минея-Октябрь-(гражданским-шрифтом).fb2',
# 2 : '20950-Минея-Февраль-(гражданским-шрифтом).fb2',
# 3 : '21374-Минея-Март-(гражданским-шрифтом).fb2',
# 4 : '21656-Минея-Апрель-(гражданским-шрифтом).fb2',
# 5 : '22003-Минея-Май-(гражданским-шрифтом).fb2',
# 6 : '22251-Минея-Июнь-(гражданским-шрифтом).fb2',
# 7 : '22588-Минея-Июль-(гражданским-шрифтом).fb2',
# 8 : '22910-Минея-Август-(гражданским-шрифтом).fb2',
# 12 : '23471-Минея-Декабрь-(гражданским-шрифтом).fb2',
# 11 : '23912-Минея-Ноябрь-(гражданским-шрифтом).fb2'
# }
input_files = {
1 : '01.fb2',
2 : '02.fb2',
3 : '03.fb2',
4 : '04.fb2',
5 : '05.fb2',
6 : '06.fb2',
7 : '07.fb2',
8 : '08.fb2',
9 : '09.fb2',
10 : '10.fb2',
11 : '11.fb2',
12 : '12.fb2'
}

def neat_print(filename, text):
    with open(filename, 'w') as f:
        print_me = re.sub('<p>', '\n<p>', text)
        print_me = re.sub('style>', 'red>', text)
        for line in print_me.split('\n'):
            line = line.strip()
            if line:
                print(line, file = f)



input_path = '/Users/pantlmn/Desktop/slavcorpora/green-mineya/fb2/'
for month, file_path in input_files.items():
    tree = etree.parse(input_path + file_path)
    root = tree.getroot()

    output_path = '/Users/pantlmn/Desktop/slavcorpora/green-mineya/split/%02d' % month
    os.makedirs(output_path, exist_ok=True)

    day = 0
    for e_body in tree.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}body'):
        if not 'name' in e_body.attrib:
            for e_section in e_body.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}section'):
                day += 1
                sluzhba_id = 0
                day_txt_node = e_section.find('{http://www.gribuser.ru/xml/fictionbook/2.0}title/{http://www.gribuser.ru/xml/fictionbook/2.0}p')
                if day_txt_node is not None:
                    day_txt = day_txt_node.text
                else:
                    print('Error in month %d, day %d' % (month, day))
                    day_txt = 'error!!!'
                # print(day)
                for e_sluzhba in e_section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}section'):
                    sluzhba_header_node = e_sluzhba.find('{http://www.gribuser.ru/xml/fictionbook/2.0}title/{http://www.gribuser.ru/xml/fictionbook/2.0}p')
                    sluzhba_header_txt = modify_day_txt(sluzhba_header_node)
                    # if sluzhba_header_node is not None:
                    #     sluzhba_header_txt = modify_day_txt(sluzhba_header_node)
                    #     sluzhba_header_txt_ru = day_txt_ru(sluzhba_header_node)
                    # else:
                    #     print('Error in month %d, day %d, sluzhba %d' % (month, day, sluzhba_id+1))
                    #     sluzhba_header_txt = 'error!!!'
                    sluzhba_len = len(e_sluzhba)
                    last_accented_par_id = -1
                    for par_id in range(sluzhba_len):
                        if re.findall(chr(0x0301), etree.tostring(e_sluzhba[par_id], encoding="unicode")):
                            last_accented_par_id = par_id
                    # print ('Последний с ударением: %d из %d' % (last_accented_par_id + 1, sluzhba_len))
                    # sluzhba_id += 1
                    # print_me = etree.tostring(e_sluzhba, encoding="unicode")
                    # total_length = len(print_me)
                    # accents_count = len(re.findall(chr(0x0301), print_me))
                    # accents_ratio = 100 * accents_count / total_length
                    # if accents_ratio < 1:
                    #     subdir = '/vitae'
                    # elif accents_ratio > 7:
                    #     subdir = '/hymni'
                    # else:
                    #     subdir = ''
                    start_string = '<section xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:xlink="http://www.w3.org/1999/xlink"/>'
                    e_subtrees = {'hymni' : etree.fromstring(start_string),
                                  'vita'  : etree.fromstring(start_string)}
                    if last_accented_par_id >= 0:
                        for par in e_sluzhba[:last_accented_par_id + 1]:
                            e_subtrees['hymni'].append(par)
                            # print (len(e_subtrees['hymni']))
                    if last_accented_par_id < (sluzhba_len - 1):
                        for par in e_sluzhba:
                            e_subtrees['vita'].append(par)
                    for subdir, e_subtree in e_subtrees.items():
                        # print('%s: %s, %d' %(sluzhba_header_txt, subdir, len(e_subtree)))
                        if len(e_subtree):
                            sluzhba_id += 1
                            print_me = etree.tostring(e_subtree, encoding="unicode")
                            os.makedirs(output_path + '/' + subdir, exist_ok=True)
                            output_file = output_path + '/' + subdir + '/%02d_%02d.%d--%s.txt' % (month, day, sluzhba_id, sluzhba_header_txt)
                            neat_print(output_file, print_me)
                    # print("%s\t%.2f\t%d" % (sluzhba_header_txt_ru, 100*accents_count/total_length, total_length))
                    # if (day == 1) and (sluzhba_id == 1):
