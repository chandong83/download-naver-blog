# 네이버 블로그 파일로 저장


[테스트 버전]<br>
    
    파이선 : 3.7.6
    beautifulsoup4 : 4.9.0
    lxml : 4.5.0
    requests : 2.23.0


[필요 패키지 설치]<br>

    $ pip install beautifulsoup4
    $ pip install lxml
    $ pip install requests


[실행 방법]<br>

    python .\download_naver_blog.py [네이버 블로그 링크] [저장 파일 이름]
    
    예 > 
    python .\download_naver_blog.py https://blog.naver.com/chandong83/221951781607 blog.html
    
<br>
<br>
<br>


## 작업중 

[리스트 정보 얻기]

블로그 상단에 있는 카테고리 리스트 정보를 얻어옴.

아래 링크에서 자신의 PC에 설치된 크롬 브라우저 버전과 맞는 chromedirver 설치

https://chromedriver.storage.googleapis.com/index.html


[테스트 버전]
    
    파이선 : 3.7.6
    beautifulsoup4 : 4.9.0
    lxml : 4.5.0
    requests : 2.23.0
    selenium : 3.141.0

[사용 설명]

    python .\get_category_list.py
    네이버 로그인 창이 나타나면 로그인 
    로그인 완료되면 하단 창에 리스트를 얻을 주소 입력