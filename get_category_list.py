import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from bs4 import BeautifulSoup

from parsing_blog import Parser
import utils

debug_mode = False      # 디버그 모드 - url 고정
user_reads = True       # 로그인하여 조회수도 함께 얻기
skip_dump_file = True   # 덤프 데이터 얻기

is_done = False
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


def start_parsing(driver):
    try:
        toggle_button = driver.find_element_by_xpath('//*[@id="toplistSpanBlind"]')
        if toggle_button.text == '목록열기': # 리스트가 닫혀있음
            toggle_button.click()            
            time.sleep(1)         
    except:
        print('목록 버튼을 찾지 못 했습니다.')
        print('프로그램을 종료합니다.')
        return False
    
    

    try:
        driver.find_element_by_xpath('//*[@id="listCountToggle"]').click()        
    except:
        print('줄 보기 버튼을 찾지 못 했습니다.')
        print('프로그램을 종료합니다.')
        return False
    

    try:
        driver.find_element_by_xpath('//*[@id="changeListCount"]/a[5]').click()         
    except:
        print('30줄 보기 버튼을 찾지 못 했습니다.')
        print('프로그램을 종료합니다.')
        return False

    time.sleep(1) 
    index = 0
                
    fp_csv = open(out_path + 'list.csv',  "w", encoding='utf-8')    
    write_file_csv_header(fp_csv) # 해더 파일에 쓰기 
    while True:        
        while True:
            index += 1
            parsing(driver, str(index), fp_csv)
            if not get_next_tab(driver):                
                break
        
        if not get_next_pages(driver):
            break
    fp_csv.close()
    return True

def get_next_tab(driver):    
    time.sleep(1) 
    box = driver.find_element_by_xpath('//*[@id="toplistWrapper"]/div[2]/div')
    select_next_page = False
    cur_page = ''
    try:
        buttons = driver.find_elements_by_css_selector('.page._goPageTop')        
        try:
            cur = driver.find_element_by_css_selector('.page.pcol3._goPageTop')
            print('(현재 위치)' + cur.text + ',', end='')
            cur_page = cur.text
        except NoSuchElementException as e:
            #print('no such current element')
            pass
        except Exception as e:
            print(e)
            pass

        for button in buttons:            
            if select_next_page:
                print(' ' + button.text + ' 번 페이지로 이동합니다. ')
                button.click()
                time.sleep(1)
                return True            
            #print(button.text + ',', end='')
            try:
                if cur_page == button.text:
                    select_next_page = True
            except NoSuchElementException as e:
                pass
            except Exception as e:
                print(e)
                return False

    except Exception as e:
        print(e)

    return False

def get_next_pages(driver):    
    time.sleep(1) 
    box = driver.find_element_by_xpath('//*[@id="toplistWrapper"]/div[2]/div')
    try:        
        button = driver.find_element_by_css_selector('.next.pcol2._goPageTop').click()        
        print(' 다음 페이지로 이동합니다.')
    except NoSuchElementException as e:
        print(' 더 이상 다음 페이지가 없습니다.')
        return False
    except Exception as e:
        print(e)
        return False

    return True


def parsing(driver, index, fp_csv):  
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    print(index + '페이지 리스트를 읽어옵니다.')
    if not skip_dump_file:
        with open(out_path + index + '_' +'full_content.html',  "w", encoding='utf-8') as fp_full_content:
            fp_full_content.write(str(soup))

    if not skip_dump_file:
        fp_category_list = open(out_path + index + '_' + 'category_list.html',  "w", encoding='utf-8')
    
    for list in soup.select('.blog2_categorylist'):        
        if not skip_dump_file:
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

    if not skip_dump_file:
        fp_category_list.close()

class MyListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        print("Before navigating to ", url)

    def before_navigate_back(self, driver):
        print("before navigating back ", driver.current_url)

    def after_navigate_back(self, driver):
        print("After navigating back ", driver.current_url)

    def before_navigate_forward(self, driver):
        print("before navigating forward ", driver.current_url)

    def after_navigate_forward(self, driver):
        print("After navigating forward ", driver.current_url)

    def before_find(self, by, value, driver):
        print("before_find")

    def after_find(self, by, value, driver):
        print("after_find")

    def before_click(self, element, driver):
        print("before_click")

    def after_click(self, element, driver):
        print("after_click")

    def before_change_value_of(self, element, driver):
        print("before_change_value_of")

    def after_change_value_of(self, element, driver):
        print("after_change_value_of")

    def before_execute_script(self, script, driver):
        print("before_execute_script")

    def after_execute_script(self, script, driver):
        print("after_execute_script")

    def before_close(self, driver):
        print("before_close")

    def after_close(self, driver):
        print("after_close")

    def before_quit(self, driver):
        print("before_quit")

    def after_quit(self, driver):
        print("after_quit")

    def on_exception(self, exception, driver):
        print("on_exception")

    def after_navigate_to(self, url, driver):
        global is_done                
        if 'https://nid.naver.com/nidlogin.login' in url:
            #print('login screen, no need to parse')
            return
        start_parsing(driver)
        is_done = True



if __name__ == '__main__':    
    driver_path = utils.check_chromedriver(chrome_driver_path)
    if driver_path is None:
        print('크롬드라이버가 없습니다. 아래의 링크에서 PC에 설치된 크롬 브라우저 버전과 맞는 드라이버를 먼저 다운로드해주세요.')
        print('https://chromedriver.storage.googleapis.com/index.html')
        print('다운로드한 드라이버는 dhromedriver 폴더에 넣으시면 됩니다.')
        exit(-1)
    if user_reads:
        print('로그인 화면으로 이동합니다.')
        print('로그인 화면이 보이면, 로그인을 시도해 주세요.')    
    
    driver_plain = webdriver.Chrome(driver_path)
    driver = EventFiringWebDriver(driver_plain, MyListener())

    if user_reads:
        driver.get('https://nid.naver.com/nidlogin.login')    
        driver.implicitly_wait(3)
    if not debug_mode: 
        while True:
            if user_reads:
                url = input("로그인이 성공하였다면, 리스트를 얻을 링크주소를 입력후 엔터키를 입력하세요.\n:")
            else:
                url = input("리스트를 얻을 링크주소를 입력후 엔터키를 입력하세요.\n:")
            if not url:
                print('키입력이 없습니다. 다시입력해주세요.')
            else:
                break
    else:
        url = 'https://blog.naver.com/PostList.nhn?blogId=chandong83&from=postList&categoryNo=10'

    if not utils.check_out_folder():
        exit(-1)

    print(url + ' : 주소의 정보를 읽어옵니다.')    
    driver.get(Parser.redirect_url(url))
    while is_done is not True:
        time.sleep(1)        
    driver.implicitly_wait(3)
    print('완료 되었습니다. list.csv 파일을 확인해주세요.')
    input()    
    driver.close()	
