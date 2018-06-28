# coding utf-8
import cv2
import os
import time

start = time.time()


#何pixel単位で分割するか指定する。
separate_pxl = 30

cd = os.getcwd()

input_img = cv2.imread("sample.bmp")

height,width,channels = input_img.shape

height_splits = int(height/separate_pxl)
width_splits = int(width/separate_pxl)

print("この画像サイズは(%d,%d)です。\n"
      "これを%d×%dに分割し、20pixel四方にします。\n"
      "このデータ群をラベルとします。"
      %(height,width,height_splits,width_splits))

image_name = []

for i in range(height_splits):
    clp1 = input_img[i*separate_pxl:i*separate_pxl+separate_pxl, 0:width]

    for a in range(width_splits):
        clp2 = clp1[0:separate_pxl,a*separate_pxl:a*separate_pxl+separate_pxl]
        image_name.append(clp2)

print("画像枚数　%s枚"%len(image_name))

dir_name = "separates"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
os.chdir("./"+dir_name)


for i in range(len(image_name)):

    save_name = "lr_%05d.bmp"%i
    cv2.imwrite(save_name,image_name[i])

os.chdir(cd)


print("次に、入力画像を平滑化(ぼかし)することで故意に画質を劣化させます。\n"
      "劣化させたのち、先ほどと同様に画像を分割します。\n"
      "これを訓練画像とします。")

blur = cv2.blur(input_img,(10,10))
cv2.imwrite("blur.bmp",blur)

height,width_blur,channels = blur.shape

height_splits = int(height/separate_pxl)
width_splits = int(width/separate_pxl)

print("この画像サイズは(%d,%d)です。\n"
      "これを%d×%dに分割し、20pixel四方にします。\n"
      "このデータ群を正解とします。"
      %(height,width,height_splits,width_splits))

image_name = []

for i in range(height_splits):
    clp1 = input_img[i*separate_pxl:i*separate_pxl+separate_pxl, 0:width]

    for a in range(width_splits):
        clp2 = clp1[0:separate_pxl,a*separate_pxl:a*separate_pxl+separate_pxl]
        image_name.append(clp2)

print("画像枚数　%s枚"%len(image_name))

dir_name = "Blur_separates"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
os.chdir("./"+dir_name)


for i in range(len(image_name)):

    save_name = "tr_%05d.bmp"%i
    cv2.imwrite(save_name,image_name[i])



#Excelに書き込む



end = time.time()-start
print("%06f 秒かかった"%end)