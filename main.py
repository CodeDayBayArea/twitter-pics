import tweepy
# from dotenv import load_dotenv
import os
import cv2
import time
from PIL import Image, ImageTk
import tkinter as tk
# from __future__ import print_function
# load_dotenv()

# auth = tweepy.OAuthHandler(os.environ.get(
#     "CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
# auth.set_access_token(os.environ.get("API_TOKEN"),
#                       os.environ.get("API_SECRET"))

# api = tweepy.API(auth)

# LE_IMAGE = None

w1 = tk.Tk()
w1.title("Sketchy")
w1.geometry("480x320")
label = tk.Label(w1)
label.grid(row=0, column=3)
cap = cv2.VideoCapture(0)


def getImage():
    # while(True):
    # time.sleep(1)
    ret, frame = cap.read()
    # cv2.imshow('frame', frame)

    image = frame
    grey_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey_img, (21, 21), 0)
    sketch = cv2.divide(grey_img, blur, scale=256.0)
    cv2.imwrite("sketch.png", sketch)

    background = Image.open("sketch.png").convert("RGBA")
    width, height = background.size
    foreground = Image.open("stamp.png").convert("RGBA")
    foreground = foreground.resize(
        (width, int(150*(height/width))))
    background.paste(foreground, (0, 0), mask=foreground)
    background.save("main.png")

    return ImageTk.PhotoImage((background))
    # break

    # cap.release()
    # cv2.destroyAllWindows()


def updateLabel():
    LE_IMAGE = getImage()
    label.imgtk = LE_IMAGE
    label.configure(image=LE_IMAGE)
   # Repeat after an interval to capture continiously
    label.after(20, updateLabel)


def postTweet():
    media = api.media_upload('./main.png')
    api.update_status("CodeDay", media_ids=[media.media_id_string])


def showWindow():

    #    while True:
    #    while True:

    #    print(LE_IMAGE)

    for i in range(6):
        w1.columnconfigure(i, weight=1)
    w1.rowconfigure(1, weight=1)

    bird = tk.Button(w1, text="Post to Twitter", command=postTweet)
    bird.grid(row=2, column=3, sticky='nesw')

    # retake = tk.Button(w1, text="Retake")
    # retake.grid(row=2, column=1, sticky='nesw')

    printer = tk.Button(w1, text="Print photo")
    printer.grid(row=2, column=4, sticky='nesw')

    updateLabel()


#    label=tk.Label(w1,image=LE_IMAGE).pack()


#    updateLabel(label, LE_IMAGE)
    w1.mainloop()


if __name__ == "__main__":
    showWindow()
