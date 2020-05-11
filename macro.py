import download_naver_blog
import utils

start = 1
total = 0
'''
u = 'http://blogthumb2.naver.net/MjAyMDA1MTFfNCAg/MDAxNTg5MTY1Nzc4MDI0.SCr-z_qgxAO6lfN69vwgAihDmnOvneUrW-1iGyzM-1Yg.O4sv1WfEK9V7OKQX-lWpvrMB-ByEpFZqhiaIuH6Sg6Mg.PNG.chandong83/image.png?type=w2'
utils.saveImage(u, 'a.png')
exit()
'''
with open('out/list.csv', 'r', encoding='utf-8') as fp:
    lines = fp.readlines()
    for line_count, line in enumerate(lines):
        items = line.split('\t')
        if line_count == 0:
            continue
        '''
        if line_count == 0:
            for index, item in enumerate(items):            
                print(str(index) + ' : ' + item, end='')
        '''
        if start <= line_count:
            #print(str(line_count) + ' ' + items[3])
            download_naver_blog.run( items[3], 'index.md')
            if total > 0:
                if line_count-start >= total-1:
                    break