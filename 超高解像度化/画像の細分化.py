# coding utf-8
import cv2
import os
import time
import xlwt
import csv
import sys
import pandas as pd


#画像枚数
images = 50

#ぼかしのスケール
G=10

#何pixel単位で分割するか指定する。
separate_pxl = 20

#保存するExcelsheetの準備
xl_bk = xlwt.Workbook()
sheet_name ="Dataset"
sheet1 =xl_bk.add_sheet(sheet_name)


#分割したい画像が存在するdirectorypath
input_dir ="D:\\jifuku\\M2\\プログラミングpython\\Deep Learning\\超高解像度化\\image"

start = time.time()
if  os.path.exists(sheet_name +".xlsx"):
   print("すでに同じ名前のエクセルファイルが存在します。\n"
         "プログラムを停止します。")
   sys.exit()
cd = os.getcwd()

for n in range(images):
    os.chdir(input_dir)

    #リストを毎回初期化する必要があるため、forの中で宣言
    list_lrname = []
    list_trname = []


    img_name = "trim"+str(n)+".bmp"
    input_img = cv2.imread(img_name)

    height, width, channels = input_img.shape

    height_splits = int(height / separate_pxl)
    width_splits = int(width / separate_pxl)

    #print("この画像サイズは(%d,%d)です。\n"
         # "これを%d×%dに分割し、このデータ群をラベルとします。"
          #% (height, width, height_splits, width_splits))

    os.chdir(cd)
    image_name = []

    for i in range(height_splits):
        clp1 = input_img[i * separate_pxl:i * separate_pxl + separate_pxl, 0:width]

        for a in range(width_splits):
            clp2 = clp1[0:separate_pxl, a * separate_pxl:a * separate_pxl + separate_pxl]
            image_name.append(clp2)

    #print("分割後の画像枚数　%s枚" % len(image_name))

    dir_name = "label"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    os.chdir("./" + dir_name)

    for i in range(len(image_name)):
        save_name = "lr_%03d_%02d.bmp" % (n,i)
        s = "./label/" + save_name
        list_lrname.append(s)
        cv2.imwrite(save_name, image_name[i])

    #excelへの書き込み。画像ごとに毎回書き込む
        a = n*len(image_name)

        sheet1.write(a+i, 0, list_lrname[i])

    os.chdir(cd)


    #print("次に、入力画像を平滑化(ぼかし)することで故意に画質を劣化させます。\n"
     #     "劣化させたのち、先ほどと同様に画像を分割します。\n"
      #    "これを訓練画像とします。")

    blur = cv2.blur(input_img, (G, G))
    cv2.imwrite("blur.bmp", blur)

    height, width_blur, channels = blur.shape

    height_splits = int(height / separate_pxl)
    width_splits = int(width / separate_pxl)

    #print("この画像サイズは(%d,%d)です。\n"
     #     "これを%d×%dに分割し、このデータ群を正解とします。"
      #    % (height, width, height_splits, width_splits))

    image_name = []

    for i in range(height_splits):
        clp1 = input_img[i * separate_pxl:i * separate_pxl + separate_pxl, 0:width]

        for a in range(width_splits):
            clp2 = clp1[0:separate_pxl, a * separate_pxl:a * separate_pxl + separate_pxl]
            image_name.append(clp2)

    #print("画像枚数　%s枚" % len(image_name))

    dir_name = "training"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    os.chdir("./" + dir_name)

    for i in range(len(image_name)):
        save_name = "%02dtr_%03d_%02d.bmp" % (G,n,i)
        s = "./training/" + save_name
        list_trname.append(s)

        cv2.imwrite(save_name, image_name[i])


    #Excelに書き込み
    #書き込み開始位置は（画像枚数）×（分割数）分の行の間隔をあけて書き込めば連続で行ける

        sheet1.write( n * len(image_name)+i,1, list_trname[i])

    os.chdir(cd)

xl_bk.save("dataset.xls")


end = time.time() - start
print("%06f 秒かかった" % end)