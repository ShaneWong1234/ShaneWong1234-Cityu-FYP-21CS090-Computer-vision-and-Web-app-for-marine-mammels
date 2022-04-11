import pandas as pd
import os
import shutil

imageDirPath = "C:\\Users\\Administrator\\Desktop\\Work\\Dataset\\images"
trainingDirPath = "C:\\Users\\Administrator\\Desktop\\Work\\Dataset\\training"
testDirPath = "C:\\Users\\Administrator\\Desktop\\Work\\Dataset\\test"
original = pd.read_csv("./combined_annotation.csv")
unique = original.drop_duplicates(subset=['filename'], keep='last')
testUnique = unique.sample(frac=0.20)
testCSV = original
trainingCSV = original

for filename in testUnique["filename"]:
    imagePath = imageDirPath + "\\" + filename
    testPath = testDirPath + "\\" + filename
    shutil.move(imagePath, testPath)

    trainingCSV = trainingCSV[trainingCSV["filename"] != filename] 


trainingUnique = trainingCSV.drop_duplicates(subset=['filename'], keep='last')
for filename in trainingUnique["filename"]:
    imagePath = imageDirPath + "\\" + filename
    trainingPath = trainingDirPath + "\\" + filename
    shutil.move(imagePath, trainingPath)

    testCSV = testCSV[testCSV["filename"] != filename]

print("Original :" + str(len(original)))
print("Test: " + str(len(testCSV)))
print("Training: " + str(len(trainingCSV)))

testCSV.to_csv('C:\\Users\\Administrator\\Desktop\\Work\\Dataset\\test\\test.csv', index=False)
trainingCSV.to_csv('C:\\Users\\Administrator\\Desktop\\Work\\Dataset\\training\\training.csv', index=False)
