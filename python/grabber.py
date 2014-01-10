import cv2
import numpy as np
import math
import argparse


#TODO: Classa, ktorej budem davat objekty
#TODO: Ako zistim ostrost objektu? Nech vyberiem najlepsi frame
#TODO: Ako budem sledovat posuvanie?
    
def subimage(image, p1, p2, p3, w, h):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    transformation = np.array([
        [float(x3 - x2) / w, float(x2 - x1) / h, x1],
        [float(y3 - y2) / w, float(y2 - y1) / h, y1],
    ])
    return cv2.warpAffine(
        image,
        transformation,
        (int(w), int(h)),
        flags=cv2.WARP_INVERSE_MAP
    )

def getImagesIterable(captureDevice):
    while True:
        ret = captureDevice.read()
        if ret[0] == False:
            break
        yield ret[1]


def main(input_filename):
    cv2.namedWindow('video')
    cv2.namedWindow('image')
    
    downscale = 0.25
    
    video = cv2.VideoCapture(input_filename)
    for image in getImagesIterable(video):
        img2 = cv2.resize(image, (0, 0), fx=downscale, fy=downscale)
        img = cv2.GaussianBlur(img2, (5, 5), 0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = np.zeros((gray.shape), np.uint8)
        kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        
        close = cv2.morphologyEx(gray, cv2.MORPH_CLOSE,kernel1)
        div = np.float32(gray)/(close)
        res = np.uint8(cv2.normalize(div, div, 0, 255, cv2.NORM_MINMAX))
        
        thresh = cv2.adaptiveThreshold(res, 255, 0, 1, 19, 2)

        contour, _ = cv2.findContours(
            thresh.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        best_cnt = []
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        img3 = img2.copy()
        for cnt in contour:
            area = cv2.contourArea(cnt)
            if area > 1000:
                cnt = cv2.convexHull(cnt)
                area = cv2.contourArea(cnt)
                mar = cv2.minAreaRect(cnt)
                _, (xx, yy), _ = mar
                minarea = xx*yy
                if abs(minarea - area)/area > 0.06:
                    continue
                rectangle = cv2.cv.BoxPoints(mar)
                best_cnt.append(np.array(rectangle, dtype=cnt.dtype))
                karta = subimage(
                    image,
                    (rectangle[2][0] / downscale, rectangle[2][1] / downscale),
                    (rectangle[1][0] / downscale, rectangle[1][1] / downscale),
                    (rectangle[0][0] / downscale, rectangle[0][1] / downscale),
                    mar[1][1] / downscale,
                    mar[1][0] / downscale
                )
                cv2.imshow('image', karta)
            
        best_cnt = np.array(best_cnt)
        cv2.drawContours(img2, best_cnt, -1, (255, 0, 255), 3)
        cv2.drawContours(mask, best_cnt, -1, (255, 255, 255), -1)

        #cv2.drawContours(mask,best_cnt,-1,0,2)        
        res = cv2.bitwise_and(img3, mask)
        #DOTO -- ziskanie karty, trackovanie pozicie aby sme vedeli
        cv2.imshow('video',
            np.vstack([ 
                   np.hstack([
                        cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB),
                        img2
                    ]),
                   np.hstack([mask, res])
            ]))
        
        if cv2.waitKey(1) == 27:
            break
        continue
        
#===============================================================================
#        kernelx = cv2.getStructuringElement(cv2.MORPH_RECT,(2,10))
# 
#        dx = cv2.Sobel(res,cv2.CV_16S,1,0)
#        dx = cv2.convertScaleAbs(dx)
#        cv2.normalize(dx,dx,0,255,cv2.NORM_MINMAX)
#        ret,close = cv2.threshold(dx,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# 
#        close = cv2.morphologyEx(close,cv2.MORPH_DILATE,kernelx,iterations = 1)
# 
#        contour, hier = cv2.findContours(
#            close,
#            cv2.RETR_EXTERNAL,
#            cv2.CHAIN_APPROX_SIMPLE
#        )
#        for cnt in contour:
#            x,y,w,h = cv2.boundingRect(cnt)
#            if h/w > 5:
#                cv2.drawContours(close,[cnt],0,255,-1)
#            else:
#                cv2.drawContours(close,[cnt],0,0,-1)
#        close = cv2.morphologyEx(close,cv2.MORPH_CLOSE,None,iterations = 2)
# 
#        closex = close.copy()
#===============================================================================

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video', type=str, help="input video")
    args = parser.parse_args()
    main(args.video)
    