import os
import requests
import africastalking as at
from dotenv import load_dotenv
from datetime import datetime

from db_models import main, add_stream, check_stream, Stream, Message

load_dotenv()
client_id = os.getenv('Client-ID')
print(client_id)
access_token = os.getenv('access_token')
at_username = os.getenv('at_username')
at_api_key = os.getenv('at_api_key')
mobile_number = os.getenv('mobile_number')
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
    # stream_id = []
    # viewer_count = []
    # user_name = []
    # start = []
    # title = []
    message = []
    live_n = False
    for s in streams:
        print(s['id'])
        # stream_id.append(s['id'])
        # user_name.append(s['user_name'])
        # title.append(s['game_name'])
        converted_time = datetime.strptime(s['started_at'], "%Y-%m-%dT%H:%M:%SZ")
        message.append([s['id'], s['user_name'], s['title'], s['viewer_count'], converted_time, s['game_name']])

        add_stream(main(), s['id'], s['user_name'], s['viewer_count'], s['user_id'],
                   s['game_name'], s['title'], converted_time)


    def stream_notification(live_message):
        m1 = session.query(Message).filter(Message.message == live_message[0][0]).one_or_none()
        print(message)

        """try:
            at_response = sms.send(live_message, [mobile_number])
            add_message(at_response.id, live_message, datetime.datetime.now(), s['id'])
        except Exception as e:
            print(f"Houston we have a problem: {e}")"""


    stream_notification(message)

""" print(viewer_count) 
    print(stream_id)
    print(user_name)
    print(title)"""


def stream_query(session):
    s1 = session.query(Stream).all()


stream_query(main())
