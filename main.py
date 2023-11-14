from espacewrapper import API

espaceapi = API()

events = espaceapi.get_next_days(7)

print(events)

for event in events['Data']:
    for item in event['Items']:
        if item['ItemType'] == 'Space':
            print(item['Name'])