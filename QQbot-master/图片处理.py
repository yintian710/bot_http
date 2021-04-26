#coding=utf-8
import os  #打开文件时需要
from PIL import Image
import re
def size():
    Start_path = 'C:\\Users\\Administrator\\Desktop\\460杀\\'
    End_path = 'C:\\Users\\Administrator\\Desktop\\image\\'
    iphone5_width = 350
    iphone5_depth = 280
    count = 0
    list2 = ['N', 'R', 'SR', 'SSR', 'UR']
    for _ in list2:
        Start_path += _ + '\\'
        # End_path += _ + '\\'
        list1 = os.listdir(Start_path)
        print(list1)
        for pic in list1:
            path = Start_path + pic
            print(path)
            im = Image.open(path)
            w, h = im.size
            if w!=iphone5_width or h!=iphone5_depth:
                print(pic)
                print("图片名称为"+pic+"图片被修改")
                h_new=35
                w_new=25
                count=count+1
                out = im.resize((w_new, h_new), Image.ANTIALIAS)
                new_pic=re.sub(pic[:-4], pic[:-4], pic)
                #print new_pic
                new_path = End_path+new_pic
                print(new_path)
                try:
                    out.save(new_path)
                except:
                    out = out.convert('RGB')
                    out.save(new_path)
        Start_path = 'C:\\Users\\Administrator\\Desktop\\460杀\\'
        End_path = 'C:\\Users\\Administrator\\Desktop\\image\\'

    print('END')
    count=str(count)
    print("共有"+count+"张图片尺寸被修改")


def name():
    format='jpg'
    path = 'C:\\Users\\Administrator\\Desktop\\460杀\\N\\'
    filenames=os.listdir(path) #进入当前目录，并把当前目录下的文件定义为filenames
    for filename in filenames:         #对每一个文件进行遍历操作
        i=filename.split('.')          #用‘.’作为分割符，对文件名字符隔开
        print(i)
        if filename!='change to zip.py' and i[-1]!=format:
        # 由于在操作中要把.py文件放到要修改的文件目录下，所以要过滤.py文件不要做该格式操作，同     时，如果该文件后缀是.zip也不做修改
            t=filename.split('_')       #再一次对文件进行分割，关键字符为‘_’
            os.rename(path+filename, path+i[0]+'.'+format)  #重命名文件

size()