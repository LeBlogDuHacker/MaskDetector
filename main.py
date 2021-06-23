import cv2

face = cv2.CascadeClassifier('cascade_files\\haarcascade_frontalface_default.xml')
eye = cv2.CascadeClassifier('cascade_files\\haarcascade_eye.xml')
mouth = cv2.CascadeClassifier('cascade_files\\haarcascade_mcs_mouth.xml')
upper_body = cv2.CascadeClassifier('cascade_files\\haarcascade_upperbody.xml')

bw_threshold = 80

font = cv2.FONT_HERSHEY_SIMPLEX
org = (30, 30)
weared_mask_font_color = (255, 255, 255)
not_weared_mask_font_color = (0, 0, 255)
thickness = 2
font_scale = 1
weared_mask = "Mask"
not_weared_mask = "No_Mask"

cap = cv2.VideoCapture(1)

while 1:
    ret, img = cap.read()
    img = cv2.flip(img, 1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow('black_and_white', black_and_white)

    faces = face.detectMultiScale(gray, 1.1, 4)

    faces_bw = face.detectMultiScale(black_and_white, 1.1, 4)

    if len(faces) == 0 and len(faces_bw) == 0:
        cv2.putText(img, "No face found...", org, font, font_scale, weared_mask_font_color, thickness,
                    cv2.LINE_AA)

    elif len(faces) == 0 and len(faces_bw) == 1:
        cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)

    else:
        for (x, y, w, h) in faces:
            # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

            mouth_rects = mouth.detectMultiScale(gray, 1.5, 5)

            if len(mouth_rects) == 0:
                cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        
            else:
                for (mx, my, mw, mh) in mouth_rects:

                    if (y < my < y + h):
                        cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness,

                                    cv2.LINE_AA)

                        # cv2.rectangle(img, (mx, my), (mx + mh, my + mw), (0, 0, 255), 3)
                        break
    cv2.imshow('Mask Detection', img)
    k = cv2.waitKey(30) & 0xff

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
