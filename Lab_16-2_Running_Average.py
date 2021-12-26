import cv2 as cv
import numpy as np
 

def handler_thresh(x):
    thresh_value = cv.getTrackbarPos('Thershold','motion')
    alpha_percant = cv.getTrackbarPos('alpha','motion')
    print(f"thresh_value:{thresh_value} / alpha_percent:{alpha_percant}")

def main():
    thresh_value = 4
    alpha_percant = 50 #เรียนรู้แค่ 50% หรือครึ่งๆกลางๆ
    cv.namedWindow('motion',cv.WINDOW_NORMAL)
    cv.createTrackbar('Thershold', 'motion', thresh_value, 255, handler_thresh)
    cv.createTrackbar('alpha', 'motion', alpha_percant, 100, handler_thresh)
    vdofile = 'depth.avi'
    cap = cv.VideoCapture(vdofile)
    if not cap.isOpened():
        print("Cannot open vdo")
        exit()
    ret, frame = cap.read() 
    frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    background = frame.copy()
    while True:
        thresh_value = cv.getTrackbarPos('Thershold','motion')
        alpha_percant = cv.getTrackbarPos('alpha','motion')
        alpha = alpha_percant/100 #จะได้ค่าจำนวน 1 ถ้าจะให้จำนวนเต็มให้ใส่ // แต่ถ้าใส่ / อย่างเดียวให้เอาจุดทศนิยมด้วย
        ret, frame = cap.read() 
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        # Calc motion
        motion_no_thres = np.abs(frame - background) #เฟรมปัจจุบันมาลบกับเฟรมอดีต |current - old [t-xx] | > threshold -> isMotion part 
        # Updateting background for next frame
        #background = (alpha * frame) + ((1-alpha) * background) 
        # How to use -> addWeight Image = alpha * image1 + bata * image2 + y
        background = cv.addWeighted(frame, alpha, background, (1-alpha), 0) # (alpha * frame) + ((1-alpha) * background)
        #print(1-alpha)
        ref,motion = cv.threshold(motion_no_thres,thresh_value,255,cv.THRESH_BINARY)
        cv.imshow('frame', frame)
        cv.imshow('motion',motion)
        cv.imshow('background',background)
        if cv.waitKey(50) == 27: #ถ้าอยากให้วีดีโอเร่งเร็วขึ้นก็ลดwaitkey เป็น10 ถ้าอยากให้ช้าก็เพิ่ม waitkey มากขึ้น 100-1000-10000
            break
    cap.release()
 
if __name__ == "__main__":
    main()