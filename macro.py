import sys
import download_naver_blog
import utils

def run(read_file, start, total):
    with open(read_file, 'r', encoding='utf-8') as fp:
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

if __name__ == '__main__':
    #debug = True
    debug = False
    if debug is False:
        if len(sys.argv) != 4:
            print('python .\macro.py [url list file] [start index] [total count]')
            print('ex> python .\macro.py out/list.csv 1 10')
            exit(-1)
        file_path = sys.argv[1]
        start = int(sys.argv[2])
        total = int(sys.argv[3])
    else:
        print('디버그 모드')
        file_path = 'out/list.csv'
        start = 1
        total = 2

    run(file_path, start, total)
