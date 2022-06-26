import tweepy
from dotenv import load_dotenv
import os
import cv2
from PIL import Image, ImageTk
import tkinter as tki
from __future__ import print_function
# load_dotenv()

# auth = tweepy.OAuthHandler(os.environ.get(
#     "CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
# auth.set_access_token(os.environ.get("API_TOKEN"),
#                       os.environ.get("API_SECRET"))

# api = tweepy.API(auth)


def getImage():
    cap = cv2.VideoCapture(0)
    while(True):
        frame = cap.read()
        cv2.imshow('frame', frame)
        image = frame
        grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
        break

    cap.release()
    cv2.destroyAllWindows()
def postTweet():
    media = api.media_upload('./main.png')
    api.update_status("CodeDay", media_ids=[media.media_id_string])
def showWindow():
   w1=tk.Tk()
   w1.title("Sketchy")
   w1.geometry("480x320")
   for i in range(3):
     w1.columnconfigure(i, weight=1)
   w1.rowconfigure(1, weight=1)

   bird = tk.Button(w1, text="Post to Twitter")
   bird.grid(row=2, column=1)

   retake = tk.Button(w1, text="Retake")
   retake.grid(row=2, column=2)

   printer = tk.Button(w1, text="Print photo")
   printer.grid(row=2, column=3)

   w1.mainloop()

if __name__ == "__main__":
    showWindow()
