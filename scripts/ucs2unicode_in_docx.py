import lxml.etree as et
from cslavonic import ucs_codec

ucs_codec.register_UCS()

NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def ns(tag):
    return '{' + NS + '}' + tag

def reencode(text):
    return text.encode('cp1251', 'replace').decode('ucs')

def reencode2(text):
    out = []
    special = {}
    # 'Ҵ' : 'ⷮ',
    #             'ҳ' : 'ⷩ',
    #             'ӡ' : '',
    #             'ҭ' : 'ᲅ',
    #             'ү' : 'д',
    #             'ұ' : 'ⷨ',
    #             'ҍ' : '̾',
    #             'Ѹ' : '҃',
    #             'ѹ' : '҃',
    #             'ѣ' : 'ѣ',
    #             'ӥ' : 'ⷧ҇',
    #             'ҥ' : 'ѻ',
    #             '҉' : 'ⷣꙵ',
    #             'ҋ' : 'и҆',
    #             'Ӥ' : 'ⷷ',
    #             'ѥ' : 'ѥ',
    #             'Ӣ' : 'ⷶ҇',
    #             'ӄ' : 'ꙋ҆́',
    #             'ӈ' : 'ꙋ́',
    #             'ҧ' : 'ѣ̀',
    #             'Ҧ' : 'ѣ́',
    #             'ӭ' : 'ⷽ҇'}
    for c in text:
        try:
            c = c.encode('cp1251').decode('ucs')
        except:
            try:
                c = special[c]
            except:
                c = '?'
        out.append(c)
    return ''.join(out)

with open('document.xml', 'rb') as f:
    xml = et.fromstring(f.read())

bad_chars = {}

ucs = False
for elt in xml.iter():
    if elt.tag == ns('rFonts'):
        if elt.get(ns('hAnsi')) == 'Fedorovsk UCS':
            ucs = True
        else:
            ucs = False
    elif elt.tag == ns('t') and ucs:
        print (elt.text)
        for c in elt.text:
            try:
                c.encode('cp1251')
            except:
                bad_chars[c] = elt.text
        txt = reencode2(elt.text)
        print(txt)
        elt.text = txt
with open('zip/word/document.xml', 'wb') as f:
    f.write(et.tostring(xml, pretty_print=True, encoding="utf-8"))

# for c in sorted(bad_chars.keys()):
#     print(c.encode('unicode-escape').decode(), c, '::', bad_chars[c], '::', reencode(bad_chars[c]))

# print('ҭ'.encode('unicode-escape'))
