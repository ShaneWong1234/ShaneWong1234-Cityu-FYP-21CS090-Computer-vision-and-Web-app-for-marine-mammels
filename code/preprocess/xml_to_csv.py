#Based on https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py
import xml.etree.ElementTree as X
import os
import glob
import pandas as pd

path = 'C:\\Users\\Administrator\\Desktop\\Work\\Dataset\\images'
fileList = []
for xml in glob.glob(path + '\*.xml'):
    t = X.parse(xml)
    r = t.getroot()
    for each in r.findall('object'):
        row = (r.find('filename').text,
            int(r.find('size')[0].text),
            int(r.find('size')[1].text),
            'dolphin',
            int(each[4][0].text),
            int(each[4][1].text),
            int(each[4][2].text),
            int(each[4][3].text)
            )
        fileList.append(row)

label_column = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
df = pd.DataFrame(fileList, columns=label_column)
df.sort_values(by=['filename'])
df.to_csv(('annotation.csv'), index=None)