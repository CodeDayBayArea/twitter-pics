import tweepy
# from dotenv import load_dotenv
import os
# from turtle import back
import cv2
import time
from PIL import Image
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


def postTweet():
    getImage()
    # media = api.media_upload('./newsketch.png')
    # api.update_status("CodeDay", media_ids=[media.media_id_string])


if __name__ == "__main__":
    postTweet()
