import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from priority_predictor_task_sorter import Event, EventPriorityQueue

# Loading Priority Predictor Pipeline
with open("priority_model.pkl", "rb") as f:
    priority_pipeline = pickle.load(f)

# Loading Time Allocator Pipeline
with open("alloc_hours_model.pkl", "rb") as f:
    time_pipeline = pickle.load(f)

time_model   = time_pipeline['model']
time_scaler  = time_pipeline['scaler']
time_encoder = time_pipeline['encoder']

# Creatin Priority Queue
queue = EventPriorityQueue()

# Example Tasks
sample_tasks = [
    {"event_name": "Online Course", "deadline": "2025-05-27T12:00:00", "duration": 3},
    {"event_name": "Project Work", "deadline": "2025-05-29T18:00:00", "duration": 4},
    {"event_name": "Assignnt", "deadline": "2025-06-01T09:00:00", "duration": 8},
]

for t in sample_tasks:
    evt = Event(**t)
    queue.add_event(evt)

print(f"Queue created with {len(queue)} tasks.")

# User's free time
free_hours = float(input("Enter your free hours available today: "))
print(f"\nRemaining Free hours: {free_hours} hours\n")

while free_hours > 0:
    event = queue.pop_event()
    if event is None:
        print("No more tasks to allocate.")
        break

    print(f"Working on {event.event_name} (duration={event.duration}h, priority={event.priority})")

    # Building features for time allocation
    feat = event.to_feature_dict()
    if event.event_name in time_encoder.classes_:
        task_code = int(time_encoder.transform([event.event_name])[0])
    else:
        task_code = 0

    df_time = pd.DataFrame([{
        'duration':       feat['duration'],
        'priority':       event.priority,
        'hours_left':     feat['hours_remaining'],
        'days_remaining': max(1, int(feat['hours_remaining'] // 24)),
        'task_enc':       task_code
    }])

    # Scale only numeric features, then append task_enc
    numeric_cols = ['duration', 'priority', 'hours_left', 'days_remaining']
    num_scaled = time_scaler.transform(df_time[numeric_cols])
    task_enc_arr = df_time[['task_enc']].to_numpy().reshape(-1, 1)
    X_scaled = np.hstack([num_scaled, task_enc_arr])

    # Predict allocation hours
    # Scale numeric features into DataFrame
    df_scaled = pd.DataFrame(
        time_scaler.transform(df_time[numeric_cols]),
        columns=numeric_cols
    )
    df_scaled['task_enc'] = df_time['task_enc']
    alloc = int(round(time_model.predict(df_scaled)[0]))
    alloc = max(1, min(alloc, free_hours, int(event.duration)))
    print(f"\nAllocating {alloc}h to {event.event_name}")

    # Update duration and hours
    event.duration -= alloc
    free_hours    -= alloc

    if event.duration > 0:
        new_feat = event.to_feature_dict()
        df_prio = pd.DataFrame([{
            'duration':        new_feat['duration'],
            'hours_remaining': new_feat['hours_remaining'],
            'time_pressure':   new_feat['time_pressure']
        }])
        new_prio = int(round(priority_pipeline.predict(df_prio)[0]))
        event.priority = new_prio
        print(f"Remaining duration={event.duration}h, new priority={event.priority}\n")
        queue.add_event(event)
    else:
        print(f"{event.event_name} is completed!\n")

print(f"Remaining free hours: {free_hours}h")
