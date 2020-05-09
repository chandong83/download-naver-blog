from bs4 import BeautifulSoup

# 링크
def link(fp, content):  
    if 'se-module-oglink' in str(content):
        flag = True
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
    if 'se-module-image' in str(content):
        for sub_content in content.select('.se-image-resource'): # image link
            fp.write(sub_content['data-lazy-src'])
        return True            
    return False

# 스티커 이미지 링크
def sticker(fp, content): 
    if 'se-module-sticker' in str(content):
        for sub_content in content.select('.se-sticker-image'): # image link
            fp.write(sub_content['src'])
        return True            
    return False

# 파싱 리스트
parsing_func_list = [link, text, code, img, sticker]

def parsing(fp, content):
    for func in parsing_func_list:
        if func(fp, content):
            return
    else:
        print('unkown tag: ' + str(content))