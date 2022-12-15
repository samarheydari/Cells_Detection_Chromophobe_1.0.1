from tkinter import filedialog
import cv2 as cv
from feature_1_for_threshold_test import threshold_test
from feature_1 import step1
from feature_3 import step2
from data_smooth_new_try_1_4_3 import step3
from feature_4 import step4
from feature_4_all import step5
import numpy as np
import time
from Bar_system import set_Bar
from PIL import Image
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.messagebox

# place your directory here
#path_slides = r'C:\\Users\\samar\\Downloads\\Cells_Detection_Chromophobe_1.0.1-5ce7f036b1a407a9e775ce3cccd2d685a4b66e86\\Cells_Detection_Chromophobe_1.0.1-5ce7f036b1a407a9e775ce3cccd2d685a4b66e86\\test_image\\Oncocytoma'



def main(path_slides = ''):
    start_time = time.time()
    not_circle_rate=[]
    non_circle_rate_list=[]

    Cells_quantity, Cells_density, Cell_nucleus_color , threshold_value = step1(path_slides)

    # print(Cells_quantity)
    for i in range(1, Cells_quantity):
        try:
            print("System is working on No: ", i + 1, " Cell. Total cells: ", Cells_quantity)

            step2(i)

            step3(i)

            non_circle_rate_list.append(step4(i))
            step5(i, Cells_quantity, not_circle_rate)

        except:
            pass
    display = cv.imread("bin\\temp_display.bmp")
    dateandtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    stop_time = time.time()
    cost = stop_time - start_time
    V_1 = float(Cells_density)
    V_2 = float(Cell_nucleus_color)
    V_3 = float(np.mean(non_circle_rate_list))
    x = float (threshold_value)
   #Result
    if V_2 >= 175:
        Result_value = -1
    elif V_2 < 150:
        Result_value = 1
    else:
        if V_1 < 1.20 :
            Result_value = round((1 * ((V_1 - 0.565) / 0.282) + 1 * ((V_2 - x) /3.6) + 2 * ((V_3 - 0.234) / 0.030)), 3)
        elif 1.20<= V_1 <= 1.25:
            Result_value = round((1 * ((V_1 - 0.565) / 0.282) + 1 * ((V_2 - x) /2.81) + 2 * ((V_3 - 0.234) / 0.030)), 3)

        elif 1.25 <V_1 < 1.70:
            Result_value = round((1 * ((V_1 - 0.635) / 0.282) + 1 * ((V_2 - x) /2.65) + 2 * ((V_3 - 0.234) / 0.030)), 3)
        elif 1.70 <=V_1 < 1.90:#fixed
            Result_value = round((1 * ((V_1 - 0.765) / 0.282) + 1 * ((V_2 - x) /2.18) + 2 * ((V_3 - 0.234) / 0.030)), 3)
        elif 1.90 <= V_1 <2.1:
            Result_value = round((1 * ((V_1 - 0.865) / 0.282) + 1 * ((V_2 - x) /1.9) + 2 * ((V_3 - 0.234) / 0.030)), 3)
        else :
            Result_value = round((1 * ((V_1 - 1.865) / 0.282) + 1 * ((V_2 - x) /7) + 2 * ((V_3 - 0.234) / 0.030)), 3)


    #Bar
    set_Bar(Result_value)
    x_offset1 = 210
    y_offset1 = display.shape[0]- 390
    img_bar = cv.imread('bin\\bar.png')
    barx, bary = img_bar.shape[0:2]
    img_bar1 = cv.resize(img_bar, (int(bary-100 / 2), int(barx / 2)))
    # display[y_offset1:y_offset1 + img_bar1.shape[0], x_offset1:x_offset1 + img_bar1.shape[1]] = img_bar1

    #Text
    cv.putText(display, dateandtime, (40, 60), cv.FONT_HERSHEY_SIMPLEX, 0.5,
               (0, 0, 0), 1)
    cv.putText(display, "Result Value:" + str(Result_value), (80, display.shape[0]-400), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    if Result_value >= 0:
        cv.putText(display, "Detection Reslut: Oncocytoma", (80, display.shape[0]-350), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    else:
        cv.putText(display, "Dection Reslut: Chromophobe", (80, display.shape[0] - 350), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    cv.putText(display, "Total cells number: "+str(Cells_quantity), (80, display.shape[0]-300), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv.putText(display, "Total cells density: "+str(Cells_density), (80, display.shape[0]-250), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv.putText(display, "Aveage cell nucleus color depth: " + str(round(Cell_nucleus_color,3)), (80, display.shape[0] - 200),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv.putText(display, "Non-circle Value:" + str(round(np.mean(non_circle_rate_list),3)), (80, display.shape[0] - 150),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv.putText(display, "Running time: " + str(round(cost)) + " second", (80, display.shape[0] - 10), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (0, 0, 0), 1)
    cv.putText(display, "Running time: " + str(cost)+" second", (80, display.shape[0] - 100),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    #r1 = cv.imread("bin\\overview_result1.bmp")
    #r2 = cv.imread("bin\\cell_clean.bmp")
    #cv.imshow("Overview", r1)
    #cv.imshow("cell_clean", r2)
    #cv.imshow("Final output", display)
    cv.imwrite("bin\\output\\Final_Result.bmp", display)
    cv.imshow("Final_Result", display)
   
    print("===================Result===================")
    if Result_value > 0 :
        print("               Oncocytoma")
    else:
        print('               chromophobe')
    print("result value : ", Result_value)
    print("cells density : ", Cells_density)

    print("not_circle_rate : ",np.mean(non_circle_rate_list))

    print("Cell nucleus color depth : ", Cell_nucleus_color)
    print("%s cost %s second" % (os.path.basename(sys.argv[0]), cost))

    plt.hist(non_circle_rate_list,bins=20)
    plt.title('non_circle_rate')
    plt.show()
    # shutil.rmtree("bin\\output_single")
    # os.mkdir("bin\\output_single")
    # cv.waitKey()




import os,shutil
def mymovefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile) 
        if not os.path.exists(fpath):
            os.makedirs(fpath) 
        shutil.move(srcfile,dstfile) 
        print ("move %s -> %s"%( srcfile,dstfile))
def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:

        fpath,fname=os.path.split(dstfile) 
        if not os.path.exists(fpath):
            os.makedirs(fpath) 
        shutil.copyfile(srcfile,dstfile) 
        print ("copy %s -> %s"%( srcfile,dstfile))


from PIL import Image
def convert2pdf():
    tkinter.messagebox.showinfo('PDF has downloaded in to result_pdf dir')
def closeallwindows():
    cv.destroyAllWindows()
    plt.close()

root = Tk()
path = StringVar()
sw = root.winfo_screenwidth()

sh = root.winfo_screenheight()

ww = 350
wh = 160

x = (sw-ww) / 2
y = (sh-wh) / 2
root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
root.title("Cancer detect")
Label(root,text = "Path:").grid(row = 0, column = 0)
Entry(root, textvariable = path).grid(row = 0, column = 1)

Button(root, text = "Start", command =lambda :main(0) ).grid(row = 0, column = 2)
#Button(root, text = "Close All Windows", command =lambda :closeallwindows() ).grid(row = 0, column = 3)
#Button(root, text = "Download PDF", command =lambda :convert2pdf() ).grid(row = 0, column = 4)

from PIL import Image, ImageTk

root.mainloop()