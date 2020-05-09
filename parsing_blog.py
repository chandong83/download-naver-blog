import requests
from bs4 import BeautifulSoup

def is_exist_item():
    pass


def redirect_url(blog_url):
    if 'PostList.nhn' not in blog_url:
        try:        
            print('리다이렉트 주소를 가져옵니다.') 
            blog_soup = BeautifulSoup(requests.get(blog_url).text, 'lxml')
            for link in blog_soup.select('iframe#mainFrame'):
                redirect_url = "http://blog.naver.com" + link.get('src')
            return redirect_url
        except Exception as e:
            print(e)
            return ''
    else:
        return blog_url

# 링크
def link(content):  
    txt = ''
    if 'se_og_box' in str(content):        
        for sub_content in content.select('.se_og_box'):            
            #fp.write(str(sub_content['href']))
            txt += str(sub_content['href'])
        return txt
    elif 'se-module-oglink' in str(content):
        for sub_content in content.select('.se-oglink-info'):
            #fp.write(str(sub_content['href']))
            txt += str(sub_content['href'])
        return txt
    return None

# 텍스트
def text(content): 
    txt = ''
    if 'se-module-text' in str(content):
        for sub_content in content.select('.se-module-text'):            
            #fp.write(sub_content.text)
            txt += sub_content.text
        return txt
    return None

# 코드
def code(content): 
    txt = ''
    if 'se-code-source' in str(content):
        for sub_content in content.select('.se-code-source'):
            #fp.write(sub_content.text)
            txt += sub_content.text
        return txt
    return None

# 이미지
def img(content): 
    txt = ''
    if 'se-image' in str(content) or 'se_image' in str(content):
        for sub_content in content.select('img'): 
            url = sub_content['data-lazy-src']
            #fp.write(url)
            #fp.write('\n')
            txt += url
            #saveImage(url, )
        return txt       
    return None

# 스티커 이미지 링크
def sticker(content):     
    txt = ''
    if 'se-sticker' in str(content):
        for sub_content in content.select('img'):
            #fp.write(sub_content['src'])
            txt += sub_content['src']
        return txt    

    if 'se_sticker' in str(content):
        for sub_content in content.select('img'):
            #fp.write(sub_content['src'])
            txt += sub_content['src']
        return txt
    print('####none')
    return None
    
# 구분선
def hr(content): 
    txt = ''
    if 'se-hr' in str(content):
        for sub_content in content.select('.se-hr'):
            #fp.write(str(sub_content))
            #fp.write(str('<hr /> \n')) #hr 테그
            txt += '<hr />'
        return txt    
    return None

# 텍스트 영역
def textarea(content): 
    txt = ''
    if 'se_textarea' in str(content):
        for sub_content in content.select('.se_textarea'): 
            #fp.write(str(sub_content))
            txt += str(sub_content)
        return txt            
    return None

# 비디오 영역
def video(content): 
    txt = ''
    if 'se_video' in str(content):
        for sub_content in content.select('iframe'): 
            #fp.write(sub_content['src'])
            txt += sub_content['src']
        return txt
    return None

# 스크립트 영역
def script(content): 
    txt = ''
    if '__se_module_data' in str(content):
        for sub_content in content.select('script'): 
            #fp.write(sub_content['data-module'])
            txt += sub_content['data-module']
        return txt
    return None   

def saveImage(url, path):      
    try:    
        img_data = requests.get(url).content
        with open(path, 'wb') as handler:
            handler.write(img_data)      
    except Exception as e:
        print(e)
        return False

# 파싱 리스트
parsing_func_list = [link, text, code, img, sticker, hr, textarea, video, script]


def parsing(content):
    txt = ''
    for func in parsing_func_list:
        item = func(content)
        if item is not None:
            txt += item + '\n'
            break

    if txt == '':
        print('unkown tag: ' + str(content))        
    return txt