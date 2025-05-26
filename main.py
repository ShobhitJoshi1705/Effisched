from flask import Flask, render_template, request, jsonify
from flask_cors import CORS                                      
from ml_model.priority_decider_and_time_allocator import Event
import sqlalchemy
app=Flask(__name__)
CORS(app)
EventsList=[]                                                                      
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
    # unique_events=[dict(t) for t in {tuple(event.items()) for event in events_list}]
    EventsList=data.get('events',[])
    # ob=Event(EventsList)
    # for event in EventsList:
    #     if event["priority"]==None:
    #         event["priority"]=find_Priority(event)
    
    return jsonify({
        "status": "success",
        "message": f"Received {len(events_list)} events",
        "total_stored": len(EventsList)
    }), 200

@app.route('/get-events',methods=['GET'])
def getEventsList():
    for event in EventsList:
        print(event)
    return jsonify(EventsList)

if __name__=='__main__':
    app.run(debug=True)