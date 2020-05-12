import sys
import requests
from bs4 import BeautifulSoup


#import parsing_blog 
from parsing_blog import Parser
import utils

out_path = 'out'
folder_path = ''
def crawler(blog_url, path, file_name):
    parser = Parser(path, True)
    try:   
        soup = BeautifulSoup(requests.get(blog_url).text, 'lxml')        
        with open(path + '/' + 'full_' + file_name,  "w", encoding='utf-8') as fp_full:
            fp_full.write(str(soup))

        with open(path + '/' + file_name,  "w", encoding='utf-8') as fp:
            txt = ''
            if 'se_component' in str(soup):
                for sub_content in soup.select('div.se_component'):
                    txt += parser.parsing(sub_content)
            else:
                for sub_content in soup.select('div.se-component'):
                    txt += parser.parsing(sub_content)
            fp.write(txt)            
        return True
    except Exception as e:
         print(e)
         return False


def run(url, output):
    global out_path
    if not utils.check_out_folder():
        print('폴더 생성에 실패했습니다.')
        exit(-1)
        
    save_folder_path=''
    redirect_url=''
    redirect_url = Parser.redirect_url(url)
    #print('redirect url :' + redirect_url)
    for item in redirect_url.split('&'):
        if item.find('logNo=') >= 0:
            #item[redirect_url.find('logNo='), len('logNo='):]
            value = item.split('=')
            #print('content name: ' + value[1])            
            save_folder_path = out_path + '/' + value[1]
            if utils.check_folder(save_folder_path):
                #print(value[1] + ' 폴더를 생성했습니다. ')
                if utils.check_folder(save_folder_path+'/img'):
                    print(value[1] + '와 ' + value[1] + 'img 폴더를 생성했습니다. ')

    if crawler(redirect_url, save_folder_path, output):        
        #print('완료하였습니다. out 폴더를 확인하세요.')
        pass
    else:
        print(save_folder_path + '실패하였습니다.')

if __name__ == '__main__':
    #debug = True 
    debug = False
    if debug is False:
        if len(sys.argv) != 3:
            print('python .\download_naver_blog.py [url of naver blog] [output]')
            print('ex> python .\download_naver_blog.py https://blog.naver.com/chandong83/221951781607 blog.html')
            exit(-1)
        #print(url)
        url = sys.argv[1]
        output = sys.argv[2]
    else:    
        print('디버그 모드')
        url = 'https://blog.naver.com/chandong83/221810614177'
        output = 'parse.html'
        print(url)

    run(url, output)
