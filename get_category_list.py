import time
import requests
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from bs4 import BeautifulSoup

import parsing_blog


out_path = 'out/'
chrome_driver_path = 'E:\Program Files\chromedriver_win32\chromedriver'


class category_list:
    def __init__(self, title='', reads='', date='', link='', comment_count=''):
        self.title = title
        self.reads = reads
        self.date = date
        self.link = link
        self.comment_count = comment_count

def write_file_tab(fp, item):
    temp = 'title : ' + item.title + '\n\t' \
        + 'reads : ' + item.reads + '\n\t' \
        + 'date : ' + item.date + '\n\t' \
        + 'link : ' + item.link + '\n\t' \
        + 'comment count : ' + item.comment_count + '\n'
    fp.write(temp)


def write_file_csv_header(fp):
    temp = 'title\treads\tdate\tlink\tcomment count\n'
    fp.write(temp)

def write_file_csv(fp, item):
    temp = item.title   + '\t' \
            + item.reads + '\t' \
            + item.date  + '\t' \
            + item.link  + '\t' \
            + item.comment_count + '\n'
    fp.write(temp)

is_done = False
class MyListener(AbstractEventListener):
    def after_navigate_to(self, url, driver):
        global is_done                
        if 'https://nid.naver.com/nidlogin.login' in url:
            #print('login screen, no need to parse')
            return

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        with open(out_path+'full_content.html',  "w", encoding='utf-8') as fp_full_content:
            fp_full_content.write(str(soup))
            with open(out_path+'category_list.html',  "w", encoding='utf-8') as fp_category_list:                
                with open(out_path+'list.csv',  "w", encoding='utf-8') as fp_csv:
                    write_file_csv_header(fp_csv) # 해더 파일에 쓰기 
                    for list in soup.select('.blog2_categorylist'):
                        fp_category_list.write(str(list))  # 카테고리별 저장
                        for tbody in list.select('tbody'):                                              
                            for tr in tbody.select('tr'):   
                                if 'tr_tag' in str(tr):
                                    #print(str(tr)) #태그 정보는 제외
                                    continue
                                
                                item = category_list()
                                for td_title in tr.select('td.title'):                          
                                    for a in td_title.select('a'):
                                        item.title = a.text
                                    for num in td_title.select('.num'):
                                        item.comment_count = num.text[1:-1]
                                        
                                for td_read in tr.select('td.read'):
                                    item.reads = td_read.text
                                
                                for td_date in tr.select('td.date'):
                                    item.date = td_date.text
                                
                                for td_title in tr.select('td.title'):                            
                                    for a in td_title.select('a'):
                                        item.link = str(a['href'])                                
                                write_file_csv(fp_csv, item)
        is_done = True



if __name__ == '__main__':    
    print('로그인 화면으로 이동합니다.')
    print('로그인 화면이 보이면, 로그인을 시도해 주세요.')
    driver_plain = webdriver.Chrome(chrome_driver_path)
    driver = EventFiringWebDriver(driver_plain, MyListener())
    driver.get('https://nid.naver.com/nidlogin.login')    
    
    while True:
        url = input("로그인이 성공하였다면, 리스트를 얻을 링크주소를 입력후 엔터키를 입력하세요.\n:")
        if not url:
            print('키입력이 없습니다. 다시입력해주세요.')
        else:
            break
    print(url + ' : 주소의 정보를 읽어옵니다.')    
    driver.get(parsing_blog.redirect_url(url))
    while is_done is not True:
        time.sleep(1)
        #print('is done ' + str(is_done))
    driver.implicitly_wait(3)
    print('완료 되었습니다. list.csv 파일을 확인해주세요.')

    driver.close()	
