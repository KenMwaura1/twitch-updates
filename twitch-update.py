import os
import requests
import africastalking as at
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv('Client-ID')
print(client_id)
access_token = os.getenv('access_token')
at_username = os.getenv('at_username')
at_api_key = os.getenv('at_api_key')
at.initialize(at_username, at_api_key)
sms = at.SMS
app = at.Application
print(app.fetch_application_data())
# res = sms.send(message="test", recipients=["+254773428397"])
# print(res)
print(sms.fetch_messages())

endpoint = "https://api.twitch.tv/helix/streams?"
headers = {"Client-ID": f"{client_id}",
           "Authorization": f"Bearer {access_token}"}
params = {"user_login": ["Solary", "averagejonas", "shivfps"]}
response = requests.get(endpoint, params=params, headers=headers)
json_response = response.json()
print(json_response)
streams = json_response.get('data', [])
is_active = lambda stream: stream.get('type') == 'live'
streams_active = filter(is_active, streams)
at_least_one_stream_active = any(streams_active)
print(at_least_one_stream_active)
if at_least_one_stream_active:
    stream_id = []
    viewer_count = []
    user_name = []
    start = []
    title = []
    live_n = False
    for s in streams:
        print(s['id'])
        stream_id.append(s['id'])
        viewer_count.extend([s['user_name'], s['viewer_count'], s['started_at'], s['game_name']])
        user_name.append(s['user_name'])
        title.append(s['game_name'])

    print(viewer_count)
    print(stream_id)
    print(user_name)
    print(title)
