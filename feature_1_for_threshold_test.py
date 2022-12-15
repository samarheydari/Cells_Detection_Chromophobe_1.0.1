#xu_yang 2020/5/25 cell_detection_1.0.0
#get masked cells image
import cv2 as cv
import os
from pylab import *
import time 
from tqdm import tqdm

import tkinter as tk
from tkinter import filedialog






def step1(file_path,threshold_value):

    cell_area_hist_list=[]



    img = cv.imread(file_path)
    img_original=img
    img= cv.copyMakeBorder(img,80,450,60,60, cv.BORDER_CONSTANT,value=[255,255,255])
    img_masked=img.copy()
    img_nucleus_white_img=img.copy()
    #-----preprocess-----
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gauss = cv.GaussianBlur(gray, (5, 5), 5)
    ret, thresh = cv.threshold(gauss, threshold_value, 255, 0)
   
    erode = cv.erode(thresh, None, iterations=1)

    #-----remove outlines-----

    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            erode[0][j]=255
    #-----find contours-----
    cnts, hierarchy = cv.findContours(erode.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    def cnt_area(cnt):
      area = cv.contourArea(cnt)
      return area
    counter_number=0

    for i in range(0, len(cnts)):
        x, y, w, h = cv.boundingRect(cnts[i])
        if 250 <= cnt_area(cnts[i]) <= 0.2*(img.shape[0]*img.shape[1]) and w*h<1500 :
            cell_area_hist_list.append(cnt_area(cnts[i]))
            counter_number+=1

    return counter_number
def threshold_value_test(start_value,end_value,temp_path):
    threshold_value_list=[i for i in range(start_value,end_value,5)]
    threshold_value_numberofcells_list = []

    start_value = 155
    end_value = 230
    
    for i in tqdm(range(start_value,end_value,5),desc='Threshold Value Testing'):
        try:

            temp_threshold_value=step1(temp_path,i)
            threshold_value_numberofcells_list.append(temp_threshold_value)

        except:
            threshold_value_numberofcells_list.append(0)
            print("Program error. Break. Error value= ",i)

    plt.plot(threshold_value_list, threshold_value_numberofcells_list, "r.-")

    plt.legend(['original data', 'smooth data', 'standard circle'], prop={'size': 15})

    font1 = {
        'weight': 'normal',
        'size': 20,
    }

    plt.tick_params(labelsize=15)
    plt.xlabel('threshold', font1)
    plt.ylabel('number of cells', font1)

    target_x=threshold_value_list[threshold_value_numberofcells_list.index(max(threshold_value_numberofcells_list))]
    target_y=max(threshold_value_numberofcells_list)
    plt.plot(target_x, target_y,"x")
    plt.axvline(target_x)

    print("Suggestion Threshold_value is: ", target_x )
    plt.savefig('bin\\threshold.png')
    plt.show()
    return target_x

def threshold_test(temp_path1):

    start = time.time()
    result=threshold_value_test(155,230,temp_path1)
    end=time.time()
    print('Running time: %s Seconds'%(end-start))

    print(result)
    return result
if __name__ == "__main__":
    def open_method():

        #path = 'C:\\Users\\samar\\Downloads\\Cells_Detection_Chromophobe_1.0.1-main\\Cells_Detection_Chromophobe_1.0.1-main\\Single_Cell'
        for i in os.listdir(path):
            path_file = os.path.join(path, i)
            if os.path.isfile(path_file):
                os.remove(path_file)
            else:
                for f in os.listdir(path_file):
                    path_file2 = os.path.join(path_file, f)
                    if os.path.isfile(path_file2):
                        os.remove(path_file2)
        file_path = filedialog.askopenfilename()
        # -----read-----
        root = tk.Tk()
        root.withdraw()
        return file_path


    temp_path = open_method()

    threshold_test(temp_path)

