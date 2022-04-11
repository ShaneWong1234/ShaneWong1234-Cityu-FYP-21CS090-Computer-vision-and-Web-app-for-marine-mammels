from posixpath import basename
import albumentations as A
import cv2
import os
import glob
import pandas as pd
import re

path = 'C:\\Users\\Administrator\\Desktop\\Work\\Dataset\\images'
class_labels = ['dolphins']
ori_annontation = pd.read_csv("C:\\Users\\Administrator\\Desktop\\Work\\code\\annotation.csv")
list_of_aug = []

for name in ori_annontation['filename'].unique():
    imgPath = path + '\\' + name
    baseName = re.sub('[^0-9]', '', name)
    endPath = path + '\\' + str(int(baseName)+4402) + ".jpg"
    endName = str(int(baseName)+4402) + ".jpg"
    image = cv2.imread(imgPath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    bboxes = []
    
    desired = ori_annontation.loc[ori_annontation['filename'] == name]
    twoDdesired = desired.to_numpy()
    for everyRow in desired.itertuples():
        bboxes.append([everyRow.xmin, everyRow.ymin, everyRow.xmax, everyRow.ymax, 'dolphin'])
    
    change = A.Compose([
    A.OneOf([
    A.RandomRotate90(p=0.5),
    A.VerticalFlip(p=0.5), 
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.RandomCrop(height=900, width=1600, p=0.5),
    ], p=1)], bbox_params=A.BboxParams(format='pascal_voc'))

    after = change(image=image, bboxes=bboxes)
    changed_image = after['image']
    changed_bbox = after['bboxes']

    save_flag = cv2.imwrite(endPath, changed_image)
    if save_flag == True:
        print("Successfully saved")
    else:
        print("Failed to save")

    for everyChanged_bbox in changed_bbox:
        row = (
            endName,
            twoDdesired[0][1],
            twoDdesired[0][2],
            twoDdesired[0][3],
            everyChanged_bbox[0],
            everyChanged_bbox[1],
            everyChanged_bbox[2],
            everyChanged_bbox[3]
        )
        list_of_aug.append(row)

label_column = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
df = pd.DataFrame(list_of_aug, columns=label_column)
df.sort_values(by=['filename'])
df.to_csv(('aug_annotation.csv'), index=None)


