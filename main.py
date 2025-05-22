from flask import Flask, render_template, request, jsonify
from flask_cors import CORS                                      
import pickle as pkl
import pandas as pd
app=Flask(__name__)
CORS(app)
Events=[]                                                                      
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')
@app.route('/welcome_back')
def afterlog():
    return render_template('afterlog.html')

@app.route('/calender.html')
def calender():
    return render_template('calender.html')

@app.route('/save-events', methods=['POST'])
def addEvent():
    data = request.get_json()
    print("Received event:", data)
    events_list = data.get('events', [])
    Events.extend(events_list)
    return jsonify({
        "status": "success",
        "message": f"Received {len(events_list)} events",
        "total_stored": len(Events)
    }), 200
def getPriority(duration,deadline):
    with open('ml_model\\priority_model.pkl','rb') as priority_model:
        model= pkl.load(priority_model)
    priority=model.predict([duration,deadline])
    return priority

def findPriority():
    for event in Events['events']:
        duration = event['duration']
        deadline = event['deadline']
        priority=getPriority(duration=duration,deadline=deadline)
        event['priority']=priority   

@app.route('/get-events',methods=['GET'])
def getEvents():
    # findPriority()
    for event in Events:
        print(event)
    return jsonify(Events)

if __name__=='__main__':
    app.run(debug=True)