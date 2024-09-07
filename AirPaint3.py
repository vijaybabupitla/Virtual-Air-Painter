import cv2
import numpy as np
import time
import os
import handTrackingModule as htm

def virtual_Painter():
    # print("started")
    brushThickness = 5
    eraserThickness = 150

    directory = r'C:\Users\MUKTAR\Desktop'
    filename = 'airCanva.jpg'

    folderPath = "HeaderNew"
    myList = os.listdir(folderPath)
    myList.sort()
    print(myList)
    overlayList = []
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    print(len(overlayList))
    header = overlayList[0]
    drawColor = (255, 0, 255)
    shape = 'freestyle'
    cap = cv2.VideoCapture(0)
    cap.set(3, 960)
    cap.set(4, 540)

    detector = htm.HandDectector(detectionCon=0.85, maxHands=1)
    xp, yp = 0, 0
    imgCanvas = np.zeros((540, 960, 3), np.uint8)
    while True:

        # 1. Import image
        success, img = cap.read()
        img = cv2.flip(img, 1)

        # 2. Find Hand Landmarks
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            # print(lmList)

            # tip of index and middle fingers
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            x0, y0 = lmList[4][1:]
            # 3. Check which fingers are up
            fingers = detector.fingerUp()
            # print(fingers)

            # 4. If Selection Mode - Two finger are up
            if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                # print("Selection Mode")
                # # Checking for the click
                if y1 < 100:
                    if 89 < x1 < 162:
                        header = overlayList[0]
                        drawColor = (255, 0, 255)
                        shape = 'freestyle'
                    elif 180 < x1 < 254:
                        header = overlayList[4]
                        drawColor = (0, 0, 255)
                        shape = 'freestyle'
                    elif 272 < x1 < 346:
                        header = overlayList[8]
                        drawColor = (0, 255, 0)
                        shape = 'freestyle'
                    elif 785 < x1 < 875:
                        header = overlayList[12]
                        drawColor = (0, 0, 0)
                        shape = 'freestyle'
                    # elif x1 < 250:
                    #     header = overlayList[9]
                    #plela yaha per phir upper
                    if 700 <x1 < 777 and drawColor == (255,0,255):
                        header = overlayList[0]
                        shape = 'freestyle'
                    elif 375 < x1 < 465 and drawColor == (255,0,255):
                        header = overlayList[1]
                        shape = 'circle'
                    elif 465 < x1 < 577 and drawColor == (255,0,255):
                        header = overlayList[2]
                        shape = 'rectangle'
                    elif 577 < x1 < 700 and drawColor == (255,0,255):
                        header = overlayList[3]
                        shape ='elipse'
                        
                    elif 700 <x1 < 777 and drawColor == (0,0,255):
                        header = overlayList[4]
                        shape = 'freestyle'         
                    elif 375 < x1 < 465 and drawColor == (0,0,255):
                        header = overlayList[5]
                        shape = 'circle'
                    elif 465 < x1 < 577 and drawColor == (0,0,255):
                        header = overlayList[6]
                        shape = 'rectangle'
                    elif 577 < x1 < 700 and drawColor == (0,0,255):
                        header = overlayList[7]
                        shape ='elipse'

                    elif 700 <x1 < 777 and drawColor == (0,255,0):
                        header = overlayList[8]
                        shape = 'freestyle'
                    elif 375 < x1 < 465 and drawColor == (0,255,0):
                        header = overlayList[9]
                        shape = 'circle'
                    elif 465 < x1 < 577 and drawColor == (0,255,0):
                        header = overlayList[10]
                        shape = 'rectangle'
                    elif 577 < x1 < 700 and drawColor == (0,255,0):
                        header = overlayList[11]
                        shape ='elipse'

                    if 875<x1<959:
                        os.chdir(directory)
                        cv2.imwrite(filename,imgCanvas)
            

                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, drawColor)
                # print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

                if drawColor == (0, 0, 0):
                    eraserThickness = 50
                    z1, z2 = lmList[4][1:]
                    # print(z1,z2)
                    result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                    # print(result)
                    if result < 0:
                        result = -1 * result
                    u = result
                    if fingers[1] and fingers[4]:
                        eraserThickness = u
                    # print(eraserThickness)
                    # cv2.putText(img, str("eraserThickness="), (0, 700), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    # cv2.putText(img, str(int(eraserThickness)), (450, 700), cv2.FONT_HERSHEY_PLAIN, 3,
                                # (255, 0, 255), 3)
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

                else:
                    brushThickness = 5
                    # z1, z2 = lmList[4][1:]
                    # print(z1,z2)
                    # result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                    # print(result)
                    # if result < 0:
                    #     result = -1 * result
                    # u = result
                    # brushThickness = int(u)
                    # print(eraserThickness)

                    #draw
                    if shape == 'freestyle' and fingers[1] and fingers[2] == False and fingers[3] == False and fingers[4] == False:
                        # z1, z2 = lmList[4][1:]
                        # ## print(z1,z2)
                        # result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                        # ## print(result)
                        # if result < 0:
                        #     result = -1 * result
                        # u = result
                        # cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                        # if u<=25:
                        #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                        #     cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                        ## cv2.putText(img, str(u), (600, 700), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        ## cv2.putText(img, str("brushThickness="), (0, 700), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        ## cv2.putText(img, str(int(brushThickness)), (450, 700), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255),3)
                        cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
                        # print("draw mode")
                        
                        if xp==0 and yp==0:
                            xp,yp = x1,y1
                        else:    
                            cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                            cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)

                        xp,yp = x1,y1


                    # Rectangle
                    if shape == 'rectangle':
                        z1, z2 = lmList[4][1:]
                        # print(z1,z2)
                        result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                        # print(result)
                        if result < 0:
                            result = -1 * result
                        u = result
                        cv2.rectangle(img, (x0, y0), (x1, y1), drawColor)
                        cv2.putText(img, "Diagonal Length = ", (10, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
                        cv2.putText(img, str(u), (170, 120), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
                        if fingers[4]:
                            cv2.rectangle(imgCanvas, (x0, y0), (x1, y1), drawColor)
                            cv2.circle




                    #Circle
                    if shape == 'circle':
                        z1, z2 = lmList[4][1:]
                        # print(z1,z2)
                        result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                        # print(result)
                        if result < 0:
                            result = -1 * result
                        u = result
                        cv2.putText(img, "Radius = ", (10, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
                        cv2.putText(img, str(u), (100, 120), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
                        cv2.circle(img,(x0,y0),u,drawColor)
                        if fingers[4]:
                            cv2.circle(imgCanvas, (x0, y0), u, drawColor)



                    #Ellipse
                    if shape == 'elipse':
                        z1, z2 = lmList[4][1:]
                        # cv2.ellipse(img,(x1,y1),(int(z1/2),int(z2/2)),0,0,360,255,0)
                        a = z1-x1
                        b= (z2-x2)
                        if x1 >250:
                            b=int(b/2)
                        if a <0:
                            a=-1*a
                        if b<0:
                            b=-1*b
                        cv2.ellipse(img, (x1, y1),(a,b), 0,0,360, drawColor, 0)
                        cv2.putText(img, "Major AL = ", (10,120), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1)
                        cv2.putText(img, "Minor AL = ", (10,140), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1)
                        cv2.putText(img, str(a), (120, 120), cv2.FONT_HERSHEY_PLAIN, 1, (123, 20, 255), 1)
                        cv2.putText(img, str(b), (120, 140), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
                        if fingers[4]:
                            cv2.ellipse(imgCanvas, (x1, y1), (a, b), 0, 0, 360, drawColor, 0)

                xp, yp = x1, y1

           


            # Clear Canvas when 2 fingers are up
            if fingers[2] and fingers[3] and fingers[0]==0 and fingers[1]==0 and fingers[4]==0:
                imgCanvas = np.zeros((540, 960, 3), np.uint8)

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        # Setting the header image
        img[0:100, 0:960] = header
        img[500:540,0:960] = overlayList[13]
        # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)

        cv2.imshow("Air Canvas", img)
        cv2.imshow("Canvas", imgCanvas)
        # cv2.imshow("Inv", imgInv)
        cv2.waitKey(1)





virtual_Painter()