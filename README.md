# 네이버 블로그 파일로 저장


MarkDown 형태로 저장됩니다.


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
    python .\download_naver_blog.py https://blog.naver.com/chandong83/221951781607 blog.md
    
    해당 링크의 폴더가 out 폴더에 생성되고 이미지는 img 폴더에 추가됩니다.
<br>
<br>
<br>


## 리스트 정보 얻기 - 작업중 

자세한 정보는 https://blog.naver.com/chandong83/221955351945 확인해주세요.


블로그 상단에 있는 카테고리 리스트 정보를 얻어 옵니다.

아래 링크에서 자신의 PC에 설치된 크롬 브라우저 버전과 맞는 chromedirver 설치합니다.

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
    로그인 완료되면 하단 창에 리스트를 얻을 주소 입력합니다.


## 리스트 정보로 일괄 다운로드하기 - 작업중

[사용 설명]
    
    먼저 get_category_list.py 를 사용해 out/list.csv 파일을 만듭니다.
    아래의 명령으로 list.csv에 있는 내용을 가져옵니다.

    python .\macro.py [링크 리스트 파일] [시작] [총 개수]
     - 링크 리스트 파일 : get_category_list.py로 생성한 리스트 파일
     - 시작 : 해당 리스트 파일에서 내용을 가져올 시작 번호 1번부터 시작
     - 총 개수 : 시작 번호부터 가져올 총 개수
  
    python .\macro.py .\out\list.csv 1 2
     - out\list.cvs 파일에 1번부터 2개 가져오라는 명령 
  
    