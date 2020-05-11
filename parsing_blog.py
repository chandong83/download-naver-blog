import requests
import urllib.request
from bs4 import BeautifulSoup

class Parser(object):
    def __init__(self, _path='out', _markdown_mdoe=True):
        self.counter = 0
        self.markdown_mdoe = _markdown_mdoe
        self.folder_path = _path
        if self.markdown_mdoe:
            self.endline = '\n\n'
        else:
            self.endline = '\n'
        # 파싱 리스트
        self.parsing_func_list = [self.link, self.text, self.code, self.img, self.sticker, self.hr, self.textarea, self.video, self.script]


    def is_exist_item(self):
        pass

    @staticmethod
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
    def link(self, content):  
        txt = ''
        if 'se_og_box' in str(content):        
            for sub_content in content.select('.se_og_box'):  
                if self.markdown_mdoe:
                    txt += '[' + str(sub_content['href']) + ']('
                    txt += str(sub_content['href'])
                    txt += ')'
                    txt += self.endline
                else:
                    txt += str(sub_content['href'])
                    txt += self.endline
            return txt
        elif 'se-module-oglink' in str(content):
            for sub_content in content.select('.se-oglink-info'):
                if self.markdown_mdoe:
                    txt += '[' + str(sub_content['href']) + ']('
                    txt += str(sub_content['href'])
                    txt += ')'
                    txt += self.endline
                else:
                    txt += str(sub_content['href'])
                    txt += self.endline
            return txt
        return None

    # 텍스트
    def text(self, content): 
        txt = ''
        if 'se-module-text' in str(content):
            for sub_content in content.select('.se-module-text'):            
                #fp.write(sub_content.text)
                txt += sub_content.text
                txt += self.endline
            return txt
        return None

    # 코드
    def code(self, content): 
        txt = ''
        if 'se-code-source' in str(content):
            for sub_content in content.select('.se-code-source'):
                #fp.write(sub_content.text)
                txt += sub_content.text
                txt += self.endline
            return txt
        return None

    # 이미지
    def img(self,content): 
        txt = ''
        if 'se-image' in str(content) or 'se_image' in str(content):
            for sub_content in content.select('img'):             
                url = sub_content['data-lazy-src']
                if self.markdown_mdoe:
                    txt += '![' + './img/' + str(self.counter)+'.png' + ']('                    
                    txt += './img/' + str(self.counter)+'.png' + ')'   
                    txt += self.endline
                else:
                    txt += '['+ str(self.counter) +']'
                    txt += url
                    txt += self.endline 

                if not self.saveImage(url, self.folder_path + '/img/' + str(self.counter)+'.png'):
                    print(str(content))
                else:
                    self.counter += 1

            return txt       
        return None

    # 스티커 이미지 링크
    def sticker(self, content):     
        txt = ''
        if 'se-sticker' in str(content):
            for sub_content in content.select('img'):
                #fp.write(sub_content['src'])
                txt += sub_content['src']
                txt += self.endline
            return txt    

        if 'se_sticker' in str(content):
            for sub_content in content.select('img'):
                #fp.write(sub_content['src'])
                txt += sub_content['src']
                txt += self.endline
            return txt
        print('####none')
        return None
        
    # 구분선
    def hr(self, content): 
        txt = ''
        if 'se-hr' in str(content):
            for sub_content in content.select('.se-hr'):
                #fp.write(str(sub_content))
                #fp.write(str('<hr /> \n')) #hr 테그
                txt += '<hr />'
                txt += self.endline
            return txt    
        return None

    # 텍스트 영역
    def textarea(self, content): 
        txt = ''
        if 'se_textarea' in str(content):
            for sub_content in content.select('.se_textarea'): 
                #fp.write(str(sub_content))
                txt += str(sub_content)
                txt += self.endline
            return txt            
        return None

    # 비디오 영역
    def video(self, content): 
        txt = ''
        if 'se_video' in str(content):
            for sub_content in content.select('iframe'): 
                #fp.write(sub_content['src'])
                txt += sub_content['src']
                txt += self.endline
            return txt
        return None

    # 스크립트 영역
    def script(self, content): 
        txt = ''
        if '__se_module_data' in str(content):
            for sub_content in content.select('script'): 
                #fp.write(sub_content['data-module'])
                txt += sub_content['data-module']
                txt += self.endline
            return txt
        return None   

    def saveImage(self, url, path):      
        try:    
            urllib.request.urlretrieve(url, path)
            print(path)
            #img_data = requests.get(url).content
            #with open(path, 'wb') as handler:
            #    handler.write(img_data)      
        except Exception as e:
            print(url + ' ' + str(e))
            return False
        return True

    

    def parsing(self, content):
        txt = ''        
        for func in self.parsing_func_list:
            item = func(content)
            if item is not None:
                txt += item
                break

        if txt == '':
            print('unkown tag: ' + str(content))        
        return txt