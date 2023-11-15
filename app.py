# main.py

from espacewrapper import API
from flask import Flask, request, jsonify
import re
from datetime import date
from datetime import timedelta
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/refresh', methods=['GET'])
def setup():
    global events
    yesterday = date.today() - timedelta(days=1)
    espaceapi = API()
    events = espaceapi.get_next_events(str(yesterday), 2000)
    return "Updated!"

@app.route('/api/get_events', methods=['POST'])
def extract():
    request_data = request.get_json()
    
    input_day = request_data['date']
    input_start_time = request_data['startTime']
    input_end_time = request_data['endTime']
    
    calendar_data = {}
    def getRoomId(room: []) -> []:
        rooms = []
        room_id = {"Dining Area I": 0, # activities
                "Dining Area II": 1, 
                "Plaza Booth1": 2, 
                "Plaza Booth2": 3,
                "Plaza Booth3": 4, 
                "Plaza Booth4": 5,
                "A3": 6,
                "River Plaza": 7,
                "Y4": 8,
                "C1": 9, # chapels
                "F1": 10,
                "SG1": 11,
                "K4 (Splash)": 12, # children center
                "K8": 13,
                "K9": 14,
                "K10": 15,
                "K11 (Checkout Room)": 16,
                "K12 (Dive)": 17,
                "E5": 18, # classrooms
                "E6": 19,
                "F2": 20,
                "G10": 21,
                "G11": 22,
                "G5": 23,
                "G6": 24,
                "H18": 25,
                "Y2": 26,
                "Y5": 27,
                "Booth 1": 28, # lobby
                "Booth 2": 29,
                "D4/D7": 30, # nursery
                "E1/E10": 31, # preschool
                "E2/E4": 32}

        for room_name, number in room_id.items():
            for r in room:
                if room_name in r:
                    rooms.append(number)
                
        return rooms
    
    for event in events['Data']:
        
        # event's date
        event_day = event['EventStart'][0:10]
        year = event_day[0:4]
        month = event_day[5:7]
        date = event_day[8:10]
        
        rooms = []
        for item in event['Items']:
            if item['ItemType'] == 'Space':
                rooms.append(item['Name'])

        new_event = {
            'name': event['EventName'],
            'start_time': event['EventStart'][11:16],
            'end_time': event['EventEnd'][11:16],
            'room': rooms,
            'roomid': getRoomId(rooms)
        }
        
        
        if year in calendar_data and month in calendar_data[year] and date in calendar_data[year][month]:
            # Add the new event to the existing list of events for the specified date
            calendar_data[year][month][date].append(new_event)
        else:
            # If the date does not exist, create the necessary structure
            calendar_data.setdefault(year, {}).setdefault(month, {})[date] = [new_event]
    
    
    def overlap(start_time: str, end_time: str, test_start_time: str, test_end_time: str) -> bool:
        start_time_minutes = toMinutes(start_time)
        end_time_minutes = toMinutes(end_time)
        test_start_time_minutes = toMinutes(test_start_time)
        test_end_time_minutes = toMinutes(test_end_time)
        
        return test_end_time_minutes > start_time_minutes and test_start_time_minutes < end_time_minutes
    
    def toMinutes(time: str) -> int:
        hours = 0
        minutes = 0
        pattern = r"(\d+):(\d+)"
        match = re.match(pattern, time)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            
        return hours*60 + minutes
    
    year = input_day[0:4]
    month = input_day[5:7]
    date = input_day[8:10]

    invalid_rooms = []
    try:
        for event in calendar_data[year][month][date]:
            if(overlap(event['start_time'], event['end_time'], input_start_time, input_end_time)):
                invalid_rooms.append(event)
    except:
        print("No events exist for date: ", input_day)

    return jsonify(invalid_rooms)

setup()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5001)