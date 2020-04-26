#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/24 19:49

from PIL import Image, ImageChops,ImageDraw
from dust.compare_picture.html_demo import createHTML
import os,random


class compare:
    def __init__(self):
        roots = []
        file = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        for root, dirs, files in os.walk("{}/report/compare_pic_report/".format(file)):
            # print(root)
            roots.append(root)
        self.reference = roots[1]  
        self.test = roots[2]  
        self.diff = roots[3]  
        self.html_report = roots[-3]+"\\index_report.html"  

    def compare_images(self, path_one, path_two, diff_save_location):
        image_one = Image.open(path_one)
        image_two = Image.open(path_two)
        try:
            diff = ImageChops.difference(image_one, image_two)
            if diff.getbbox() is None:#不同图片位置的尺寸
                image_one.save(diff_save_location)
                return diff_save_location,("true","pass",diff.getbbox(),0)
            else:
                diff.save(diff_save_location)
                return diff_save_location,("false","fail",diff.getbbox(),diff.getprojection(),1)
        except ValueError as e:
            text = ("表示图片大小和box对应的宽度不一致，参考API说明使用2纬的box避免上述问题")
            print("【{0}】{1}".format(e, text))

    def find_zone(self,x,y,test,diff):
        x,y=x,y
        x_use = self.deal_data(x);y_use = self.deal_data(y)
        finall = self.combine(x_use,y_use)
        use = self.judge_img(Image.open(diff),finall)
        self.draw_pic(Image.open(test),use,diff)

    def deal_data(self,use_list):
        use = [];real = []
        for i in range(len(use_list)):
            if use_list[i] == 1:
                use.append(i)
        real.append(use[0]);real.append(use[-1])
        for j in range(1, len(use)):
            if use[j] - use[j - 1] > 7:
                real.append(use[j - 1]);real.append(use[j])
        return (sorted(set(real)))

    def combine(self,x,y):
        finall_zones = []
        for u in range(0, len(x) // 2 + 1, 2):
            for w in range(0, len((y)) // 2 + 1, 2):
                finall_zone = x[u:u + 2] + y[w:w + 2]
                finall_zone[1], finall_zone[2] = finall_zone[2], finall_zone[1]
                finall_zones.append(finall_zone)
        return finall_zones

    def judge_img(self,img,finall):
        use=[]
        for i in finall:
            pass_num = 0
            x = random.sample(range(i[0],i[2]),4)#随机点数4，需要根据各个坐标中的平均值进行填写
            y = random.sample(range(i[1],i[3]),4)
            for j in range(len(x)):
                if img.getpixel((x[j], y[j])) != (0,0,0,0) and img.getpixel((x[j], y[j]))!=(0,0,0) :
                    pass_num+=1
            if pass_num!=0:
                use.append(i)
        return sorted(use)

    def draw_pic(self,image,zones,diff_path):
        draw = ImageDraw.Draw(image)
        for i in zones:
            draw.line([(i[0], i[1]), (i[0], i[3]), (i[2], i[3]), (i[2], i[1]), (i[0], i[1])], fill=(255, 0, 0), width=5)
        image.save(diff_path)

    def create_html(self,reference,test,diff,info):
        reference_pic1 = reference.split("bitmaps_reference\\")[1];test_pic1 = test.split('bitmaps_test\\')[1]
        diff_pic1= diff.split('diff_image\\')[1]
        reference_pic, diff_pic, test_pic, file_name, html_filepath\
            =reference_pic1,diff_pic1,test_pic1,reference_pic1,self.html_report
        createHTML(reference_pic, diff_pic, test_pic, file_name, html_filepath,info[0],info[1],info[2])

    def all_files(self):
        reference,test = [],[]
        for root , dirs , files in os.walk(self.reference):
           for i in files:
               reference.append(self.reference+"\\"+i)
        for root , dirs , files in os.walk(self.test):
           for j in files:
               test.append(self.test+"\\"+j)
        for n in range(len(reference)):
            diff_pic = self.diff+"\\"+"%d.png"%n
            diff,info = self.compare_images(reference[n],test[n],diff_pic)
            if info[-1]==0:
                self.create_html(reference[n],test[n],diff,info)
            else:
                self.find_zone(info[3][0],info[3][1],test[n],diff)
                self.create_html(reference[n],test[n],diff,info)

if __name__ == '__main__':
    file = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    print(file)
    # compare().all_files()