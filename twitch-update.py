import os
import requests
import africastalking as at
from dotenv import load_dotenv
from datetime import datetime

from db_models import main, add_stream, add_message, Stream, Message

load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
at_username = os.getenv('at_username')
at_api_key = os.getenv('at_api_key')
mobile_number = os.getenv('mobile_number')
at.initialize(at_username, at_api_key)
sms = at.SMS
app = at.Application
print(app.fetch_application_data())

endpoint = "https://api.twitch.tv/helix/streams?"
headers = {"Client-ID": f"{client_id}",
           "Authorization": f"Bearer {client_secret}"}
params = {"user_login": ["Solary", "averagejonas", "shivfps", "shahzam"]}
response = requests.get(endpoint, params=params, headers=headers)
json_response = response.json()
print(json_response)
streams = json_response.get('data', [])
is_active = lambda stream: stream.get('type') == 'live'
streams_active = filter(is_active, streams)
at_least_one_stream_active = any(streams_active)
print(at_least_one_stream_active)
if at_least_one_stream_active:
    message = []
    for s in streams:
        converted_time = datetime.strptime(s['started_at'], "%Y-%m-%dT%H:%M:%SZ")
        message.append([s['id'], s['user_name'], s['title'], s['viewer_count'], converted_time, s['game_name']])

        add_stream(main(), s['id'], s['user_name'], s['viewer_count'], s['user_id'],
                   s['game_name'], s['title'], converted_time)

    def stream_notification(session, live_message):
        m1 = session.query(Message).filter(Message.stream_id == live_message[0][0]).one_or_none()
        if m1 is None:
            print(live_message[0][0])
            print(live_message)
            try:
                at_response = sms.send([live_message], [mobile_number])
                print(at_response)
                message_id = ""
                for res in at_response['SMSMessageData']['Recipients']:
                    print(res['messageId'])
                    message_id = res['messageId']
                    for m in live_message:
                        m1 = ''.join(map(str, m))
                        add_message(session, str(message_id), m1, datetime.now(), m[0])
            except Exception as e:
                print(f"Houston we have a problem: {e}")
        else:
            print(f"Message already sent")


    stream_notification(main(), message)


