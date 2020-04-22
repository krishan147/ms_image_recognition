import requests
import json
import pandas as pd
import time

# subscription_key = 'add key here'

def readFile(file):

    df_post = pd.read_csv(file, encoding='Latin-1')
    return df_post

# #def maxFacialAge(df_post):
#     #url = ""
#     #try this? https://console.faceplusplus.com/dashboard
#     #ibm https://developer.ibm.com/exchanges/models/all/max-facial-age-estimator/

def msFaceRec(df_post):

    list_firstComment = (df_post['firstComment']).tolist()
    list_imageUrl = (df_post['imageUrl']).tolist()
    list_likesCount = (df_post['likesCount']).tolist()
    list_locationName = (df_post['locationName']).tolist()
    list_ownerUsername = (df_post['ownerUsername']).tolist()
    list_timestamp = (df_post['timestamp']).tolist()
    list_url = (df_post['url']).tolist()
    list_searchterm = (df_post['searchterm']).tolist()
    #list_hd_profile_pic = (df_post['hd_profile_pic']).tolist()

    subscription_key = 'ecc21e5ce2274f1f86e93dc47cadca44'
    face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}


    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    list_frames = []
    x = 0
    for firstComment, imageUrl, likesCount, locationName, ownerUsername, timestamp, url, searchterm in zip(list_firstComment,
                                                                                                           list_imageUrl,
                                                                                                           list_likesCount,
                                                                                                           list_locationName,
                                                                                                           list_ownerUsername,
                                                                                                           list_timestamp,
                                                                                                           list_url,
                                                                                                           list_searchterm):

        try:
            if x != 2000:
                response = requests.post(face_api_url, params=params,
                                         headers=headers, json={"url": imageUrl})
                time.sleep(1)
                data = (json.dumps(response.json()))
                data = json.loads(data)

                if len(data) == 0:
                    pass
                else:

                    #df = pd.DataFrame.from_dict(data[0])

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

                    # print (face_position)
                    #
                    # print (smile, gender, age, moustache, beard, sideburns, glasses, anger, contempt, disgust, fear,
                    #        happiness, neutral, sadness, surprise, eyeMakeup, lipMakeup, bald, hairblack, hairblackcon,
                    #        hairbrown,hairbrowncon,hairgray,hairgraycon,hairother,hairothercon,hairblondcon,hairred,hairredcon)

                    df_framed = pd.DataFrame({'image_url':[imageUrl],
                                              'firstComment': [firstComment],
                                              'likesCount': [likesCount],
                                              'locationName': [locationName],
                                              'ownerUsername': [ownerUsername],
                                              'timestamp': [timestamp],
                                              'url': [url],
                                              'searchterm': [searchterm],
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

                    list_frames.append(df_framed)
                    x = x + 1
                    print (x)
            if x == 2000:
                break
        except Exception as err:
            print ("error: ", err)
            time.sleep(4)
            pass

    df_historical = pd.concat(list_frames)
    df_historical.to_csv("results/last_results.csv")

df_post = readFile('check/hd_profile_pic.csv')
#maxFacialAge(df_post)
msFaceRec(df_post)




# , columns = ['firstComment', 'imageUrl', 'likesCount', 'locationName', 'ownerUsername', 'timestamp', 'url', 'searchterm', 'face_position', 'smile', 'gender',
#                             'age', 'moustache', 'beard',
#                             'sideburns', 'glasses', 'anger',
#                             'contempt', 'disgust',
#                             'fear',
#                             'happiness', 'neutral',
#                             'sadness',
#                             'surprise', 'eyeMakeup',
#                             'lipMakeup',
#                                       'bald',
#                                       'hairblack',
#                                       'hairblackcon',
#                                       'hairbrown',
#                                       'hairbrowncon',
#                                       'hairgray',
#                                       'hairgraycon',
#                                       'hairother',
#                                       'hairothercon',
#                                       'hairblond',
#                                       'hairblondcon',
#                                       'hairred',
#                                       'hairredcon']
