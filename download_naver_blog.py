import sys
import requests
import parsing_blog
from bs4 import BeautifulSoup

out_path = 'out/'

def crawler(blog_url, file_name):
    try:   
        soup = BeautifulSoup(requests.get(blog_url).text, 'lxml')        
        with open(out_path + 'full_' + file_name,  "w", encoding='utf-8') as fp_full:
            fp_full.write(str(soup))

        with open(out_path + file_name,  "w", encoding='utf-8') as fp:
            txt = ''
            if 'se_component' in str(soup):
                for sub_content in soup.select('div.se_component'):
                    txt += parsing_blog.parsing(sub_content)
            else:
                for sub_content in soup.select('div.se-component'):
                    txt += parsing_blog.parsing(sub_content)
            fp.write(txt)            
        return True
    except Exception as e:
         print(e)
         return False


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
        #url = 'https://blog.naver.com/PostList.nhn?blogId=chandong83&from=postList&categoryNo=125'
        url = 'https://blog.naver.com/chandong83/221951781607'
        output = 'parse.html'
        print(url)

    redirect_url = parsing_blog.redirect_url(url)
    if crawler(redirect_url, output):        
        print('완료하였습니다. out 폴더를 확인하세요.')
    else:
        print('실패하였습니다.')
