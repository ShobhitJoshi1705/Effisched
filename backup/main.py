from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app)

conection=sqlite3.connect('events.db')
cursor = conection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    title TEXT,
    timeFrom TEXT,
    timeTo TEXT,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    priority TEXT
)
''')
# Load the priority model
with open("ml_model\\priority_model.pkl", "rb") as f:
    priority_model = pickle.load(f)

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

@app.route('/add-event', methods=['POST'])
def add_event():
    data = request.get_json()
    print("Event received:", data)
    event_type = data.get('type')

    if event_type == "fixed":
        print("\nrecieved fixed event\n")
        event = {
            'type': 'fixed',
            'title': data.get('title'),
            'timeFrom': data.get('timeFrom'),
            'timeTo': data.get('timeTo'),
            'day': data.get('day'),
            'month': data.get('month'),
            'year': data.get('year'),
            'priority': None
        }
    
    elif event_type == "flexible":
        title        = data.get('title')
        raw_deadline = data.get('deadline')    # now an int: minutes past midnight
        duration     = float(data.get('duration'))
        eventday=data.get('day')
        
        # --- NEW: convert int→datetime at today’s date midnight + minutes ---
        from datetime import time, timedelta
        today_midnight = datetime.combine(datetime.now().date(), time())
        deadline_dt    = today_midnight + timedelta(minutes=raw_deadline)
        

        # now you can safely subtract
        hours_remaining = (deadline_dt - datetime.now()).total_seconds() / 3600
        hours_remaining = max(1, hours_remaining)
        time_pressure   = duration / hours_remaining

        features = {
            'duration':        duration,
            'hours_remaining': hours_remaining,
            'time_pressure':   time_pressure
        }
        X = pd.DataFrame([features])
        priority = int(round(priority_model.predict(X)[0]))

        event = {
            'day': data.get('day'),
            'month': data.get('month'),
            'year': data.get('year'),
            'type':     'flexible',
            'title':    title,
            'deadline': raw_deadline,  
            'duration': duration,
            'priority': priority
            
        }
        print("wit priority ",event)
        print("EventsList :",EventsList)
        if event not in EventsList:
            EventsList.append(event)
            print("apend successful")
            print("EventsList AFTER APPEND :",EventsList)
        else:
            print("apend unsucessful")
    else:
        return jsonify({"status": "error", "message": "Invalid event type"}), 400

    return jsonify({"status": "success", "message": "Event/Task added successfully"})


@app.route('/get-events', methods=['GET'])
def get_events():
    print("Events in backend:",EventsList)
    return jsonify(EventsList)

def savetoDatabase(new_event):
    cursor.execute('''
        INSERT INTO events (type, title, timeFrom, timeTo, day, month, year, priority)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
    new_event['type'],
    new_event['title'],
    new_event['timeFrom'],
    new_event['timeTo'],
    new_event['day'],
    new_event['month'],
    new_event['year'],
    new_event['priority']
    ))
    conection.commit()
    return True

    
# @app.route('/save-events', methods=['POST'])
# def add_events():
#     data = request.get_json()
#     events_list = data.get('events', [])
#     # For backward compatibility, process fixed-time events
#     for event in events_list:
#         new_event = {
#             'type': 'fixed',
#             'title': event.get('title'),
#             'timeFrom': event.get('events', [{}])[0].get('time', '').split(' - ')[0],
#             'timeTo': event.get('events', [{}])[0].get('time', '').split(' - ')[1] if ' - ' in event.get('events', [{}])[0].get('time', '') else '',
#             'day': event.get('day'),
#             'month': event.get('month'),
#             'year': event.get('year'),
#             'priority': None
#         }
#         if new_event not in EventsList:
#             print("Event Recieved:",new_event)
#             EventsList.append(new_event)
#     return jsonify({
#         "status": "success",
#         "message": f"Received {len(events_list)} events",
#         "total_stored": len(EventsList)
#     })

if __name__ == '__main__':
    app.run(debug=True)