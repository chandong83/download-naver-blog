import os
def check_out_folder():
    try:
        if not(os.path.isdir('out')):
            os.makedirs(os.path.join('out'))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('out 폴더를 생성하지 못 했습니다.')
            raise
        return False
    return True

def check_chromedriver(driver_path):
    if os.path.isfile(driver_path + '.exe'):
        return driver_path
    elif os.path.isfile('chromedriver/chromedriver' + '.exe'):
        return os.path.join('chromedriver/chromedriver')
    return None

