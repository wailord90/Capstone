# ---- start code (python3) ----
# ---- camtar.py ----
# imports
import os, sys, time
import cv2
import numpy

# init camera
camera = cv2.VideoCapture(0)
#camera.set(3, 320)   uncommenting these causes an error
#camera.set(4, 240)   making the video created unusable
time.sleep(0.5) #gives camera time to initialize (jeremy)

# master frame
master = None

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 10.0, (640,480))

while (True):
    ret, preFrame = camera.read()
    # Our operations on the frame come here
    #gray = cv2.cvtColor(preFrame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('The Frame', preFrame)

    # key delay and action
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #cv2.destroyWindow('The Frame')
        while(1):
            # grab a frame
            grabbed, frame0 = camera.read()
            # end of feed
            if not grabbed:  # error handle (jeremy)
                break


            # gray frame
            frame1 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)

            # blur frame
            frame2 = cv2.GaussianBlur(frame1, (21, 21), 0)

            # initialize master
            if master is None:
                master = frame2
                continue

            # delta frame
            frame3 = cv2.absdiff(master, frame2)

            # threshold frame
            frame4 = cv2.threshold(frame3, 15, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes
            kernel = numpy.ones((5, 5), numpy.uint8)
            frame5 = cv2.dilate(frame4, kernel, iterations=4)

            # find contours on thresholded image
            contours, nada = cv2.findContours(frame5.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # make coutour frame
            frame6 = frame0.copy()

            # target contours
            targets = []

            # loop over the contours
            for c in contours:

                # if the contour is too small, ignore it
                if cv2.contourArea(c) < 500:
                    continue

                # contour data
                M = cv2.moments(c)  # ;print( M )
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                x, y, w, h = cv2.boundingRect(c)
                rx = x + int(w / 2)
                ry = y + int(h / 2)
                ca = cv2.contourArea(c)

                # plot contours
                cv2.drawContours(frame6, [c], 0, (0, 0, 255), 2)
                cv2.rectangle(frame6, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame6, (cx, cy), 2, (0, 0, 255), 2)
                cv2.circle(frame6, (rx, ry), 2, (0, 255, 0), 2)

                # save target contours
                targets.append((rx, ry, ca))

            # make target
            area = sum([x[2] for x in targets])
            mx = 0
            my = 0
            if targets:
                for x, y, a in targets:
                    mx += x
                    my += y
                mx = int(round(mx / len(targets), 0))
                my = int(round(my / len(targets), 0))

            # plot target
            tr = 50
            frame7 = frame0.copy()
            if targets:
                out.write(frame0)
                cv2.circle(frame7, (mx, my), tr, (0, 0, 255, 0), 2)
                cv2.line(frame7, (mx - tr, my), (mx + tr, my), (0, 0, 255, 0), 2)
                cv2.line(frame7, (mx, my - tr), (mx, my + tr), (0, 0, 255, 0), 2)
            # update master
            master = frame2

            # display
            #cv2.imshow("Frame0: Raw", frame0)
            #cv2.imshow("Frame1: Gray", frame1)
            #cv2.imshow("Frame2: Blur", frame2)
            #cv2.imshow("Frame3: Delta", frame3)
            #cv2.imshow("Frame4: Threshold", frame4)
            #cv2.imshow("Frame5: Dialated", frame5)
            cv2.imshow("Frame6: Contours", frame6)
            #cv2.imshow("Frame7: Target", frame7)
            if cv2.waitKey(1) & 0xFF == ord('w'):
                break
        break

# When everything done, release the capture
camera.release()
out.release()
cv2.destroyAllWindows()
