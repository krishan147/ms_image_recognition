import requests
import json
import pandas as pd
import time
from random import randrange

def msFaceRec(hd_profile_pic):

    subscription_key = 'enter api key'
    face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    hd_profile_pic = 'https://scstylecaster.files.wordpress.com/2016/12/model-curly-hair-nose-ring.jpg'

    response = requests.post(face_api_url, params=params,
                             headers=headers, json={"url": hd_profile_pic})
    time.sleep(1 + randrange(0, 2))
    data = (json.dumps(response.json()))
    data = json.loads(data)

    print (data["error"]["message"])

    if len(data) == 0:

        df_framed = pd.DataFrame({
            'hd_profile_pic': [hd_profile_pic],
            'face_position': [''], 'smile': [''], 'gender': [''],
            'age': [''], 'moustache': [''], 'beard': [''],
            'sideburns': [''], 'glasses': [''], 'anger': [''],
            'contempt': [''], 'disgust': [''],
            'fear': [''],
            'happiness': [''], 'neutral': [''],
            'sadness': [''],
            'surprise': [''], 'eyeMakeup': [''],
            'lipMakeup': [''],
            'bald': [''],
            'hair1': [''],
            'hair1con': [''],
            'hair2': [''],
            'hair2con': [''],
            'hair3': [''],
            'hair3con': [''],
            'hair4': [''],
            'hair4con': [''],
            'hair5': [''],
            'hair5con': [''],
            'hair6': [''],
            'hair6con': ['']
        })

        return df_framed

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

        df_framed = pd.DataFrame({
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

# df_post = pd.read_csv('check/insta_25700.csv', encoding = "ISO-8859-1", engine='python')
# list_hd_profile_pics = df_post["hd_profile_pic"].tolist()

list_hd_profile_pics = []


list_frames = ['https://icdn5.digitaltrends.com/image/screen-shot-2019-02-15-at-19-16-58-720x720.jpg', 'https://ichef.bbci.co.uk/news/660/cpsprodpb/A87E/production/_108643134_3130.jpg']
x = 0

for hd_profile_pic in list_hd_profile_pics:
    try:
        df_framed = msFaceRec(hd_profile_pic)
        list_frames.append(df_framed)
    except Exception as er:
        print (er)
    x = x + 1
    print(x)

df_results = pd.concat(list_frames)
results = pd.merge(df_post, df_results, on = 'hd_profile_pic')
results.to_csv("results/results.csv")