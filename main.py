import tweepy
from dotenv import load_dotenv
import os
import cv2
load_dotenv()

auth = tweepy.OAuthHandler(os.environ.get("CD_CONSUMER_KEY"), os.environ.get("CD_CONSUMER_SECRET"))
auth.set_access_token(os.environ.get("CD_API_TOKEN"), os.environ.get("CD_API_SECRET"))

api = tweepy.API(auth)

# def getImage():
#     cap = cv2.VideoCapture(1)
#     while(True):
#         ret, frame = cap.read()
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

#         cv2.imshow('frame', rgb)
#         out = cv2.imwrite('capture.jpg', frame)
#         break

#     cap.release()
#     cv2.destroyAllWindows()

def postTweet():
    media = api.media_upload('./codeday.png')
    api.update_status("CodeDay", media_ids = [media.media_id_string])

if __name__ == "__main__":
    postTweet()