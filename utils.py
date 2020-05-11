import os
def check_folder(folder):
    try:
        if not(os.path.isdir(folder)):
            os.makedirs(os.path.join(folder))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print(folder + ' 폴더를 생성하지 못 했습니다.')
            raise
        return False
    return True

def check_out_folder():    
    return check_folder('out')


def check_chromedriver(driver_path):
    if os.path.isfile(driver_path + '.exe'):
        return driver_path
    elif os.path.isfile('chromedriver/chromedriver' + '.exe'):
        return os.path.join('chromedriver/chromedriver')
    return None

