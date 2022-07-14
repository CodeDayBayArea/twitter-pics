import tweepy
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage
import cv2
import time
from PIL import Image, ImageTk
import tkinter as tk
from math import floor
import imghdr
load_dotenv()

scale_factor = 0.58

# auth = tweepy.OAuthHandler(os.environ.get(
#     "CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
# auth.set_access_token(os.environ.get("API_TOKEN"),
#                       os.environ.get("API_SECRET"))

# api = tweepy.API(auth)


EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
TO_ADDRESS = os.environ.get("TO_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


w1 = tk.Tk()
w1.title("Sketchy")
w1.geometry("800x600")
# w1.attributes('-fullscreen', True)
label = tk.Label(w1)
label.grid(row=0, column=1, sticky='nesw')
cap = cv2.VideoCapture(0)


def getImage():
    ret, frame = cap.read()

    image = frame
    grey_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey_img, (21, 21), 0)
    sketch = cv2.divide(grey_img, blur, scale=256.0)
    # sketch = cv2.resize(sketch, (w1.winfo_width(), w1.winfo_height()-0), interpolation = cv2.INTER_AREA)
    cv2.imwrite("sketch.png", sketch)

    background = Image.open("sketch.png").convert("RGBA")
    width, height = background.size
    foreground = Image.open("stamp.png").convert("RGBA")
    foreground = foreground.resize(
        (width, int(150*(height/width))))
    background.paste(foreground, (0, 0), mask=foreground)
    background = background.resize((floor(background.size[0]*scale_factor), floor(background.size[1]*scale_factor)))
    background.save("main.png")

    return ImageTk.PhotoImage((background))


def updateLabel():
    LE_IMAGE = getImage()
    label.imgtk = LE_IMAGE
    label.configure(image=LE_IMAGE)
   # Repeat after an interval to capture continiously
    label.after(5, updateLabel)


def postTweet():
    media = api.media_upload('./main.png')
    api.update_status("CodeDay", media_ids=[media.media_id_string])


def printPhoto():
    msg = EmailMessage()
    msg['Subject'] = 'New Photo!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_ADDRESS
    msg.set_content('Here is your new photo!')

    with open("main.png", 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
    msg.add_attachment(file_data, maintype='image', subtype=file_type)

    with smtplib.SMTP_SSL('smtp.mailgun.org', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def showWindow():

    for i in range(4):
        w1.columnconfigure(i, weight=1)
    w1.rowconfigure(1, weight=1)

    bird = tk.Button(w1, text="Post to Twitter", command=postTweet)
    bird.grid(row=2, column=2, sticky='nesw')

    retake = tk.Button(w1, text="Retake")
    retake.grid(row=2, column=1, sticky='nesw')

    printer = tk.Button(w1, text="Print photo", command=printPhoto)
    printer.grid(row=2, column=1, sticky='nesw')

    updateLabel()

    w1.mainloop()


if __name__ == "__main__":
    showWindow()
