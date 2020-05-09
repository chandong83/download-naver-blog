import requests
from bs4 import BeautifulSoup

def is_exist_item():
    pass


# 링크
def link(fp, content):  
    if 'se_og_box' in str(content):        
        for sub_content in content.select('.se_og_box'):            
            fp.write(str(sub_content['href']))
        return True            
    elif 'se-module-oglink' in str(content):
        for sub_content in content.select('.se-oglink-info'):
            fp.write(str(sub_content['href']))
        return True            
    return False

# 텍스트
def text(fp, content): 
    if 'se-module-text' in str(content):
        for sub_content in content.select('.se-module-text'):            
            fp.write(sub_content.text)
        return True            
    return False

# 코드
def code(fp, content): 
    if 'se-code-source' in str(content):
        for sub_content in content.select('.se-code-source'):
            fp.write(sub_content.text)
        return True            
    return False

# 이미지
def img(fp, content): 
    if 'se-image' in str(content) or 'se_image' in str(content):
        for sub_content in content.select('img'): 
            url = sub_content['data-lazy-src']
            fp.write(url)
            fp.write('\n')
            #saveImage(url, )
        return True         
    return False

# 스티커 이미지 링크
def sticker(fp, content):     
    if 'se-sticker' in str(content):
        for sub_content in content.select('img'):
            fp.write(sub_content['src'])
        return True    

    if 'se_sticker' in str(content):
        for sub_content in content.select('img'):
            fp.write(sub_content['src'])
        return True            
    return False
    
# 구분선
def hr(fp, content): 
    if 'se-hr' in str(content):
        for sub_content in content.select('.se-hr'):
            #fp.write(str(sub_content))
            fp.write(str('<hr /> \n')) #hr 테그
        return True            
    return False

# 텍스트 영역
def textarea(fp, content): 
    if 'se_textarea' in str(content):
        for sub_content in content.select('.se_textarea'): 
            fp.write(str(sub_content))
        return True            
    return False

# 비디오 영역
def video(fp, content): 
    if 'se_video' in str(content):
        for sub_content in content.select('iframe'): 
            fp.write(sub_content['src'])
        return True   
    return False

# 스크립트 영역
def script(fp, content): 
    if '__se_module_data' in str(content):
        for sub_content in content.select('script'): 
            fp.write(sub_content['data-module'])
        return True   

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


def parsing(fp, content):
    for func in parsing_func_list:
        if func(fp, content):
            return
    else:
        print('unkown tag: ' + str(content))