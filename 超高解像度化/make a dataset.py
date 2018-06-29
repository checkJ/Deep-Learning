#このプログラムは、データセットのためのdirectory作成及びcvsファイルを作成するプログラムです
import os
import pandas as pd

original_path = os.getcwd()

#データセットを作成するdirectoryの指定
#指定後、そのdirに移動
while True:
    a = "\\"
    print("どのフォルダにデータセットを作成しますか？\n"
          "※絶対パスでお願いします。\は自動で%sに変換します。"
          %repr(a))
    i = input()
    dir_path = repr(i)


    print("[%s]\n"
          "OK？[y/n]"
          %dir_path)
    ii = input()

    if ii == "y":
        if os.path.lexists(i) == 1 :
            os.chdir(i)
            break

cd = os.getcwd()
print(cd)

# データセットの名前を決める。
#作成したのち、作業dirをデータセットフォルダの中に移動
while True:
    print("データセットのディレクトリの名前を決めてください。")
    dataset_name = input()

    print("[%s] でよろしいですか？[y/n]" % dataset_name)
    i = input()

    if i == "y":
        if os.path.exists(dataset_name):
            print("すでに同じ名前のファイルが存在します。")
            continue
        else:
            os.mkdir(dataset_name)
            os.chdir(dataset_name)
            break


#データセット内部のサブディレクトリの作成
os.mkdir("tr_img")
os.mkdir("lr_img")
os.mkdir("validation")

csv_file = open("dataset.csv",a)



header_data = ["x:label_img","y:trining_img"]
