import tweepy
# from dotenv import load_dotenv
import os
# from turtle import back
import cv2
import time
from PIL import Image, ImageTk
import tkinter as tk
# load_dotenv()

# auth = tweepy.OAuthHandler(os.environ.get(
#     "CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
# auth.set_access_token(os.environ.get("API_TOKEN"),
#                       os.environ.get("API_SECRET"))

# api = tweepy.API(auth)


def getImage():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        time.sleep(2)


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
        background.save("newsketch.png")
        break

    cap.release()
    cv2.destroyAllWindows()
def test():
    pass

def postTweet():
    # getImage()
   w1=tk.Tk()
#    w1.attributes('-fullscreen', True)
   w1.title("Sketchy")
   w1.geometry("480x320")  
   for i in range(3):
    w1.columnconfigure(i, weight=1)
   w1.rowconfigure(1, weight=1)
#    bottomFrame = tk.Frame(w1)
#    bottomFrame.pack(side=tk.BOTTOM)
   # Width, height in pixels


#    img = Image.open("./assets/birdy.png")
#    resized_image= img.resize((40,40), Image.ANTIALIAS)
#    photo = ImageTk.PhotoImage(resized_image)
#    bird = tk.Button(w1, text="Post to Twitter", image=photo, width=50, height=50)
   bird = tk.Button(w1, text="Post to Twitter")
   bird.grid(row=2, column=1)
#    bird.pack()

#    img = Image.open("./assets/retake.png")
#    resized_image= img.resize((40,40), Image.ANTIALIAS)
#    photo = ImageTk.PhotoImage(resized_image)
   retake = tk.Button(w1, text="Retake")
   retake.grid(row=2, column=2)

#    retake.pack()

#    img = Image.open("./assets/printer.png")
#    resized_image= img.resize((40,40), Image.ANTIALIAS)
#    photo = ImageTk.PhotoImage(resized_image)
   printer = tk.Button(w1, text="Print photo")
   printer.grid(row=2, column=3)

#    printer.pack()

   w1.mainloop()
    # media = api.media_upload('./newsketch.png')
    # api.update_status("CodeDay", media_ids=[media.media_id_string])


if __name__ == "__main__":
    postTweet()
