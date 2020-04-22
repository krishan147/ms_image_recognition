import requests
import json
import pandas as pd
import time
from random import randrange

def msFaceRec(name, username, followers, following, post, description, hd_profile_pic):

    subscription_key = 'add key here'
    face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    response = requests.post(face_api_url, params=params,
                             headers=headers, json={"url": hd_profile_pic})
    time.sleep(1 + randrange(0, 2))
    data = (json.dumps(response.json()))
    data = json.loads(data)

    if len(data) == 0:
        pass
    else:
        face_position = data[0]['faceRectangle']
        smile = data[0]['faceAttributes']['smile']
        gender = data[0]['faceAttributes']['gender']
        age = data[0]['faceAttributes']['age']
        moustache = data[0]['faceAttributes']['facialHair']['moustache']
        beard = data[0]['faceAttributes']['facialHair']['beard']
        sideburns = data[0]['faceAttributes']['facialHair']['sideburns']
        glasses = data[0]['faceAttributes']['glasses']

        anger = data[0]['faceAttributes']['emotion']['anger']
        contempt = data[0]['faceAttributes']['emotion']['contempt']
        disgust = data[0]['faceAttributes']['emotion']['disgust']
        fear = data[0]['faceAttributes']['emotion']['fear']
        happiness = data[0]['faceAttributes']['emotion']['happiness']
        neutral = data[0]['faceAttributes']['emotion']['neutral']
        sadness = data[0]['faceAttributes']['emotion']['sadness']
        surprise = data[0]['faceAttributes']['emotion']['surprise']

        eyeMakeup = data[0]['faceAttributes']['makeup']['eyeMakeup']
        lipMakeup = data[0]['faceAttributes']['makeup']['lipMakeup']

        bald = data[0]['faceAttributes']['hair']['bald']

        hairblack = data[0]['faceAttributes']['hair']['hairColor'][0]['color']
        hairblackcon = data[0]['faceAttributes']['hair']['hairColor'][0]['confidence']
        hairbrown = data[0]['faceAttributes']['hair']['hairColor'][1]['color']
        hairbrowncon = data[0]['faceAttributes']['hair']['hairColor'][1]['confidence']
        hairgray = data[0]['faceAttributes']['hair']['hairColor'][2]['color']
        hairgraycon = data[0]['faceAttributes']['hair']['hairColor'][2]['confidence']
        hairother = data[0]['faceAttributes']['hair']['hairColor'][3]['color']
        hairothercon = data[0]['faceAttributes']['hair']['hairColor'][3]['confidence']
        hairblond = data[0]['faceAttributes']['hair']['hairColor'][4]['color']
        hairblondcon = data[0]['faceAttributes']['hair']['hairColor'][4]['confidence']
        hairred = data[0]['faceAttributes']['hair']['hairColor'][5]['color']
        hairredcon = data[0]['faceAttributes']['hair']['hairColor'][5]['confidence']

        df_framed = pd.DataFrame({'name':[name],
                                  'username': [username],
                                  'followers': [followers],
                                  'following': [following],
                                  'post': [post],
                                  'description': [description],
                                  'hd_profile_pic': [hd_profile_pic],
                        'face_position': [face_position], 'smile': [smile], 'gender': [gender],
                        'age': [age], 'moustache': [moustache], 'beard': [beard],
                        'sideburns': [sideburns], 'glasses': [glasses], 'anger': [anger],
                        'contempt': [contempt], 'disgust': [disgust],
                        'fear': [fear],
                        'happiness': [happiness], 'neutral': [neutral],
                        'sadness': [sadness],
                        'surprise': [surprise], 'eyeMakeup': [eyeMakeup],
                        'lipMakeup': [lipMakeup],
                                  'bald': [bald],
                                  'hair1': [hairblack],
                                  'hair1con': [hairblackcon],
                                  'hair2': [hairbrown],
                                  'hair2con': [hairbrowncon],
                                  'hair3': [hairgray],
                                  'hair3con': [hairgraycon],
                                  'hair4': [hairother],
                                  'hair4con': [hairothercon],
                                  'hair5': [hairblond],
                                  'hair5con': [hairblondcon],
                                  'hair6': [hairred],
                                  'hair6con': [hairredcon]
                    })

        return df_framed

df_post = pd.read_csv('check/hd_profile_pic.csv')
list_name = df_post["name"].tolist()
list_username = df_post["username"].tolist()
list_followers = df_post["followers"].tolist()
list_following = df_post["following"].tolist()
list_post = df_post["post"].tolist()
list_description = df_post["description"].tolist()
list_hd_profile_pics = df_post["hd_profile_pic"].tolist()

list_frames = []
x = 0

for name, username, followers, following, post, description, hd_profile_pic in zip(list_name, list_username, list_followers, list_following, list_post, list_description, list_hd_profile_pics):
    try:
        df_framed = msFaceRec(name, username, followers, following, post, description, hd_profile_pic)
        x = x + 1
        print(x)
        list_frames.append(df_framed)
    except Exception as er:
        print (er)
        pass

df_frames = pd.concat(list_frames)
df_frames.to_csv("results/last_results.csv")
