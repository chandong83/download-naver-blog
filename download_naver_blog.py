import sys
import requests
import parsing_blog
from bs4 import BeautifulSoup

def crawler(blog_url, file_name):
    try:        
        blog_soup = BeautifulSoup(requests.get(blog_url).text, 'lxml')
        #print(blog_soup)
        for link in blog_soup.select('iframe#mainFrame'):
            redirect_url = "http://blog.naver.com" + link.get('src')
            redirect_soup = BeautifulSoup(requests.get(redirect_url).text, 'lxml')                            
            with open('orig_' + file_name,  "w", encoding='utf-8') as fp:
                fp.write(str(redirect_soup))

            with open(file_name,  "w", encoding='utf-8') as fp:
                if 'se_component' in str(redirect_soup):
                    for sub_content in redirect_soup.select('div.se_component'):
                        txt = str(sub_content)
                        parsing_blog.parsing(fp, sub_content)
                else:
                    for sub_content in redirect_soup.select('div.se-component'):
                        txt = str(sub_content)
                        parsing_blog.parsing(fp, sub_content)
                
        return True
    except Exception as e:
         print(e)
         return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('python .\download_naver_blog.py [url of naver blog] [output]')
        print('ex> python .\download_naver_blog.py https://blog.naver.com/chandong83/221951781607 blog.html')
        exit(-1)
    #print(url)
    url = sys.argv[1]
    output = sys.argv[2]
    #if crawler('https://blog.naver.com/chandong83/221951781607', 'blog.html'):
    print(url)
    if crawler(url, output):
        print('done')
    else:
        print('failed')
