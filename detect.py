import animeface
import PIL.Image

import cv2
import sys
import os.path
import math
import numpy as np 

import glob
files = glob.glob('imgs/*.jpg', recursive=True)

def crop_face(filename):
    im = PIL.Image.open(filename)

    faces = animeface.detect(im)

    if len(faces) != 1:
        return None

    image = cv2.imread(filename, cv2.IMREAD_COLOR)

    def imcrop(img, bbox): 
        x1,y1,x2,y2 = bbox
        if x1 < 0 or y1 < 0 or x2 > img.shape[1] or y2 > img.shape[0]:
            img, x1, x2, y1, y2 = pad_img_to_fit_bbox(img, x1, x2, y1, y2)
        return img[y1:y2, x1:x2, :]

    def pad_img_to_fit_bbox(img, x1, x2, y1, y2):
        img = np.pad(img, ((np.abs(np.minimum(0, y1)), np.maximum(y2 - img.shape[0], 0)),
                   (np.abs(np.minimum(0, x1)), np.maximum(x2 - img.shape[1], 0)), (0,0)), mode="constant", constant_values=255)
        y1 += np.abs(np.minimum(0, y1))
        y2 += np.abs(np.minimum(0, y1))
        x1 += np.abs(np.minimum(0, x1))
        x2 += np.abs(np.minimum(0, x1))
        return img, x1, x2, y1, y2

    for face in faces:
        L_x = face.left_eye.pos.x + face.left_eye.pos.height//2
        L_y = face.left_eye.pos.y + face.left_eye.pos.width//2 
        R_x = face.right_eye.pos.x + face.right_eye.pos.height//2
        R_y = face.right_eye.pos.y + face.right_eye.pos.width//2

        dx = L_x - R_x
        dy = L_y - R_y

        deg = math.atan(dy/dx) * 360 / (2*math.pi)
        if math.fabs(deg) > 60:
            deg = 0.0           # something wrong???

        print(dx, dy, deg)

        x = face.face.pos.x
        y = face.face.pos.y
        w = face.face.pos.width
        h = face.face.pos.height

        cx = x  +  h//2
        cy = y  +  w//2

        image = np.pad(image, ((2*x,2*x), (2*y,2*y), (0,0)), mode="constant", constant_values=255)
        rows,cols,_ = image.shape

        M = cv2.getRotationMatrix2D((0/2,0/2),deg,1)
        image = cv2.warpAffine(image,M,(cols,rows), borderValue=(255,255,255), flags=cv2.INTER_CUBIC)

        faces = animeface.detect(PIL.Image.fromarray(image))
        if len(faces) != 1:
            continue

        face = faces[0]

        x = face.face.pos.x
        y = face.face.pos.y
        w = face.face.pos.width + 10
        h = face.face.pos.height + 10

        chinx = face.chin.pos.x
        chiny = face.chin.pos.y

        cx = x  +  h//2
        cy = y  +  w//2

        d = h 

        cy = chiny - d + d//3

        if cy - d < 0:
            cy -= (cy-d)//2

        image = imcrop(image, (cx - d, cy - d, cx+d, cy+d ) )

        cv2.imwrite("{}_cropped.jpg".format(filename), image)



crop_face(sys.argv[1])