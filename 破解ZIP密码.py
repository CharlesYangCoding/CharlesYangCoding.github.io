

import zipfile
import itertools

filename = "新建位图图像.zip"

def uncompress(filename,password):
    try:
        with zipfile.ZipFile(filename) as zfile:
            zfile.extractall("C:/Users/User/Desktop/",pwd = password.encode("utf-8"))
        return True
    except:
        return False

chars = "abcdefghijklmnopqrstuvwxyz0123456789"
for c in itertools.permutations(chars ,4):
    password = "".join(c)
    result = uncompress(filename,password)
    if not result:
        continue
    else:
        print("解压成功",password)
        break
