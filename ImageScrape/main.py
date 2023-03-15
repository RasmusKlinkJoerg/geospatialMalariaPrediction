import pyautogui
import time
import csv
import numpy as np
import cv2
import os

delete_and_focus = (554, 176)
search = (590, 176)
zoom_in = (382, 212)
zoom_out = (380, 246)
def click():
    try:
        pass
        pyautogui.click()
    except:
        pass

def scrape_image(cords, filename, tries = 3):
    pyautogui.moveTo(delete_and_focus)
    click()
    pyautogui.typewrite(cords)
    pyautogui.moveTo(search)
    time.sleep(0.2)
    click()
    pyautogui.moveTo(zoom_out)
    time.sleep(0.2)
    click()
    time.sleep(0.2)
    click()
    time.sleep(0.2)
    click()
    time.sleep(0.2)
    click()
    time.sleep(3)
    img = pyautogui.screenshot(imageFilename=filename, region=(1300,450,1024,1024))
    np_img = np.array(img)
    #print("white",np.sum(np_img == 255))
    gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)
    #print("gray",gray)
    print("diff",np.max(gray)-np.min(gray))
    if np.max(gray)-np.min(gray) < 50 or np.sum(np_img == 255) > 4000000:
        if tries<=0:
            with open('errors.txt', 'a') as f:
                f.write(filename+'\n')
            return
        tries = tries - 1
        time.sleep(0.2)
        click()
        time.sleep(0.2)
        click()
        time.sleep(0.2)
        click()
        time.sleep(0.2)
        click()
        time.sleep(0.2)
        click()
        time.sleep(0.2)
        click()
        time.sleep(5)
        scrape_image(cords=cords, filename=filename, tries=tries)

def run(start_at = 0, end_at = 99999):
        with open('long_lat_year_with_confidential_from2010to18_size10orGreater.csv', newline='') as csvfile:
            rowreader = csv.reader(csvfile, delimiter=',')
            for row in rowreader:
                if rowreader.line_num < start_at:
                    continue
                if rowreader.line_num > end_at:
                    #print(rowreader.line_num, end_at)
                    return
                if int(row[3]) > 2014:
                    continue
                id = row[0]
                lat = row[1]
                lon = row[2]
                cords = lat + "," + lon
                cords = cords.replace("-", "/")  # changes - to / as pyautogui has another keyboard layout

                filename = "satellite_data_v2/" + id + "_" + lat + ", " + lon + ".png"

                scrape_image(cords=cords, filename=filename)

check_file = os.path.isfile('errors.txt')
if not check_file:
    #create the file
    with open('errors.txt', 'w') as fp:
        pass

time.sleep(2)
#run(start_at=5500,end_at=6000)



already = []
for img in os.listdir("satellite_data_v2"):
    already.append(img.split("_")[0])


''''Method for scraping the rest'''
#needToBeMade = []
a = 0
with open('long_lat_year_with_confidential_from2010to18_size10orGreater.csv', newline='') as csvfile:
    rowreader = csv.reader(csvfile, delimiter=',')
    for row in rowreader:
        if row[0] in already or int(row[3]) <= 2017:
            continue
        else:
            if a > 1000:
                continue
            a=a+1
            #needToBeMade.append(row[0])

            id = row[0]
            lat = row[1]
            lon = row[2]
            cords = lat + "," + lon
            cords = cords.replace("-", "/")  # changes - to / as pyautogui has another keyboard layout

            filename = "satellite_data_v2/" + id + "_" + lat + ", " + lon + ".png"
            scrape_image(cords=cords, filename=filename)
#print(needToBeMade)
#print(len(needToBeMade))


#bruger kort 2014-11-12 fra før 2014. Derefter 2017-04-19. Derefter 2020-11-18


'''Method for fixing the white images'''
'''a = 300
for filename in os.listdir('satellite_data_v2'):
    img = cv2.imread("satellite_data_v2/"+filename, cv2.IMREAD_GRAYSCALE)
    #print(filename)
    if np.max(img)-np.min(img) < 50 and a>=0:
        print(filename)
        id=int(filename.split('_')[0])+1

        run(start_at=id,end_at=id)
        a = a-1
        #break
        #scrape_image(filename=filename,c)'''
