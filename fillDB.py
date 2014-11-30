# coding=utf-8
from GlobalRating.dbAPI import *


add_user("Gogli", "dfdsadg")

from bs4 import BeautifulSoup
from urllib2 import urlopen
import re

html_doc = urlopen('http://www.abiturient.in.ua/ua/vuz_kiev_ua').read()
univerSoup = BeautifulSoup(html_doc)
univerList = []
facultetList = []
for univerName in univerSoup.findAll('a',
                                     href=re.compile('http://www.abiturient.in.ua/ua/vuz_kiev_ua/vuz_kiev_\\d*_ua')):
    ref = univerName['href']
    index = re.compile('http://www.abiturient.in.ua/ua/vuz_kiev_ua/vuz_kiev_(\\d*)_ua').search(ref).group(1)
    univerList.append(univerName.getText())
    html_doc = urlopen('http://www.abiturient.in.ua/ua/vuz_kiev_ua/vuz_kiev_' + index + '_ua')
    facSoup = BeautifulSoup(html_doc)
    sections = facSoup.find('td', text="Факультети")

    add_category(univerName.getText(), "university", test=True)
    id_category = get_category_by_name(univerName.getText())

    try:
        firstTd = sections.find_next_siblings('td')[0]
        lies = firstTd.findAll('li')
        for li in lies:
            add_category(li.text, "department", id_category, test=True)
    except AttributeError:
        print('No facultets')


        #
        # for i in range(len(univerList)):
        # print(univerList[i])