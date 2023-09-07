'''
pip install bs4 rich
website: https://www.52shuku.vip
'''

from bs4 import BeautifulSoup
import requests
import re
import sys
from rich.progress import track

def getChapters(homepage, url):
    link = requests.get(homepage)
    bs = BeautifulSoup(link.content, "html.parser")
    txt_name = bs.find('h1', {'class':'article-title'}).contents[0].split('_')[0]
    contents = bs.find_all('li', {'class':'mulu'})
    chapter_url = []
    # chapter_list = []
    for i in contents:
        chapter_url.append(url + str(i.find('a')['href'].split('/')[-1]))
        # chapter_list.append(i.text)
    return txt_name, chapter_url

def saveTxt(file_name, chapter_url):
    file = open(file_name+'.txt', 'w')
    # for link, title in zip(chapter_url, chapter_list):
    for link in track(chapter_url):
        page_url = requests.get(link)
        bs = BeautifulSoup(page_url.content, 'html.parser')
        page_content = bs.find('div', {'id': 'text'})
        tmp_exp = re.compile('p>(.*?)</p')
        tmp_text = '\n'.join(tmp_exp.findall(str(page_content)))
        tmp_exp = re.compile('<(.*?)>')
        txt = tmp_exp.sub('',tmp_text)
        # file.write(title)
        file.write(txt + '\n')
    print('DONE')
    file.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please provide the link of book homepage, e.g., https://www.52shuku.vip/tuili/b/bjOxa.html")
    else:
        homepage = sys.argv[1]
        url = '/'.join(homepage.split('/')[:-1])+'/'
        txt_name, chapter_url = getChapters(homepage, url)
        saveTxt(txt_name, chapter_url)
