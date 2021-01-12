# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from flask import Flask,request,render_template
from flask import Flask,request,render_template
import pickle
import numpy
import sklearn
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__,template_folder='templates')
model = pickle.load(open('model.pkl','rb'))


@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    liveStreamID = request.form.get('liveStreamID',False)
    beginTime = request.form.get('beginTime',False)
    endTime = request.form.get('endTime',False)
    duration = request.form.get('duration',False)
    closeBy = request.form.get('closeBy',False)
    maxLiveViewerCount = request.form.get('maxLiveViewerCount',False)
    maxLiveViewerTime = request.form.get('maxLiveViewerTime',False)
    privateLiveStream = request.form.get('privateLiveStream',False)
    receivedLikeCount = request.form.get('receivedLikeCount',False)
    isShow = request.form.get('isShow',False)
    userID = request.form.get('userID',False)
    registerCountry = request.form.get('registerCountry',False)
    uniqueViewerCount = request.form.get('uniqueViewerCount',False)
    ios = request.form.get('ios',False)
    android = request.form.get('android',False)
    durationGTE5sec = request.form.get('durationGTE5sec',False)
    durationGTE2min = request.form.get('durationGTE2min',False)
    durationGTE10min = request.form.get('durationGTE10min',False)
    avgViewerDuration = request.form.get('avgViewerDuration',False)
    count = request.form.get('count',False)
    receivePointEstimated = request.form.get('receivePointEstimated',False)
    
    dict = {'liveStreamID':int(liveStreamID),
            'beginTime':str(beginTime),
            'endTime':str(endTime),
            'duration':int(duration),
            'closeBy':str(closeBy),
            'maxLiveViewerCount':int(maxLiveViewerCount),
            'maxLiveViewerTime':str(maxLiveViewerTime),
            'privateLiveStream':int(privateLiveStream),
            'receivedLikeCount':int(receivedLikeCount),
            'isShow':bool(isShow),
            'userID':int(userID),
            'registerCountry':str(registerCountry),
            'uniqueViewerCount':int(uniqueViewerCount),
            'ios':int(ios),
            'android':int(android),
            'durationGTE5sec':int(durationGTE5sec),
            'durationGTE2min':int(durationGTE2min),
            'durationGTE10min':int(durationGTE10min),
            'avgViewerDuration':float(avgViewerDuration),
            'count':int(count),
            'receivePointEstimated':int(receivePointEstimated)}
    df = pd.DataFrame([dict])
    df.drop(['liveStreamID','userID',
             'maxLiveViewerTime','registerCountry'],axis=1,inplace=True)
    df.drop(['beginTime',
             'endTime',
             'avgViewerDuration',
             'privateLiveStream','isShow'],axis = 1,inplace=True)
    df['duration']=(df['duration']/60)
    
    if closeBy== 'Freezed':
        df['closeBy_Freezed'] = 1
        df['closeBy_Incoming call'] = 0
        df['closeBy_Keep alive failed'] = 0
        df['closeBy_Killed'] = 0
        df['closeBy_Publish failed'] = 0
        df['closeBy_Upload failed'] = 0
        df['closeBy_disconnect'] = 0
        df['closeBy_end by new stream'] = 0
        df['closeBy_normalEnd'] = 0
    elif closeBy == 'Incoming call':
        df['closeBy_Freezed'] = 0
        df['closeBy_Incoming call'] = 1
        df['closeBy_Keep alive failed'] = 0
        df['closeBy_Killed'] = 0
        df['closeBy_Publish failed'] = 0
        df['closeBy_Upload failed'] = 0
        df['closeBy_disconnect'] = 0
        df['closeBy_end by new stream'] = 0
        df['closeBy_normalEnd'] = 0
    elif closeBy == 'Keep alive failed':
        df['closeBy_Freezed'] = 0
        df['closeBy_Incoming call'] = 0
        df['closeBy_Keep alive failed'] = 1
        df['closeBy_Killed'] = 0
        df['closeBy_Publish failed'] = 0
        df['closeBy_Upload failed'] = 0
        df['closeBy_disconnect'] = 0
        df['closeBy_end by new stream'] = 0
        df['closeBy_normalEnd'] = 0
    elif closeBy == 'Killed':
        df['closeBy_Freezed'] = 0
        df['closeBy_Incoming call'] = 0
        df['closeBy_Keep alive failed'] = 0
        df['closeBy_Killed'] = 1
        df['closeBy_Publish failed'] = 0
        df['closeBy_Upload failed'] = 0
        df['closeBy_disconnect'] = 0
        df['closeBy_end by new stream'] = 0
        df['closeBy_normalEnd'] = 0
    elif closeBy == 'Publish failed':
        df['closeBy_Freezed'] = 0
        df['closeBy_Incoming call'] = 0
        df['closeBy_Keep alive failed'] = 0
        df['closeBy_Killed'] = 0
        df['closeBy_Publish failed'] = 1
        df['closeBy_Upload failed'] = 0
        df['closeBy_disconnect'] = 0
        df['closeBy_end by new stream'] = 0
        df['closeBy_normalEnd'] = 0
    elif closeBy == 'Upload failed':
        df['closeBy_Freezed'] = 0
        df['closeBy_Incoming call'] = 0
        df['closeBy_Keep alive failed'] = 0
        df['closeBy_Killed'] = 0
        df['closeBy_Publish failed'] = 0
        df['closeBy_Upload failed'] = 1
        df['closeBy_disconnect'] = 0
        df['closeBy_end by new stream'] = 0
        df['closeBy_normalEnd'] = 0
    elif closeBy == 'disconnect':
        df['closeBy_Freezed'] = 0
        df['closeBy_Incoming call'] = 0
        df['closeBy_Keep alive failed'] = 0
        df['closeBy_Killed'] = 0
        df['closeBy_Publish failed'] = 0
        df['closeBy_Upload failed'] = 0
        df['closeBy_disconnect'] = 1
        df['closeBy_end by new stream'] = 0
        df['closeBy_normalEnd'] = 0
    elif closeBy == 'end by new stream':
        df['closeBy_Freezed'] = 0
        df['closeBy_Incoming call'] = 0
        df['closeBy_Keep alive failed'] = 0
        df['closeBy_Killed'] = 0
        df['closeBy_Publish failed'] = 0
        df['closeBy_Upload failed'] = 0
        df['closeBy_disconnect'] = 0
        df['closeBy_end by new stream'] = 1
        df['closeBy_normalEnd'] = 0
    elif closeBy == 'normalEnd':
        df['closeBy_Freezed'] = 0
        df['closeBy_Incoming call'] = 0
        df['closeBy_Keep alive failed'] = 0
        df['closeBy_Killed'] = 0
        df['closeBy_Publish failed'] = 0
        df['closeBy_Upload failed'] = 0
        df['closeBy_disconnect'] = 0
        df['closeBy_end by new stream'] = 0
        df['closeBy_normalEnd'] = 1
    else:
        df['closeBy_Freezed'] = 0
        df['closeBy_Incoming call'] = 0
        df['closeBy_Keep alive failed'] = 0
        df['closeBy_Killed'] = 0
        df['closeBy_Publish failed'] = 0
        df['closeBy_Upload failed'] = 0
        df['closeBy_disconnect'] = 0
        df['closeBy_end by new stream'] = 0
        df['closeBy_normalEnd'] = 0
    df.drop('closeBy',axis=1,inplace=True)
    prediction = model.predict (df)
    if prediction == 0:
        return render_template('index.html',
                               prediction_text ='Not A good Streammer',
                               )
    else:
        return render_template('index.html',
                               prediction_text ='Look like a good Streemer',
                               )

if __name__ == "__main__":
    app.run(debug=True)