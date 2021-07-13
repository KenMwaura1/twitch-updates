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
print(sms.fetch_messages(int("ATXid_50c822e96bd467716bf56c543b8c53dc")))

endpoint = "https://api.twitch.tv/helix/streams?"
headers = {"Client-ID": f"{client_id}",
           "Authorization": f"Bearer {access_token}"}
params = {"user_login": ["Solary", "averagejonas"]}
response = requests.get(endpoint, params=params, headers=headers)
json_response = response.json()
print(json_response)
streams = json_response.get('data', [])
is_active = lambda stream: stream.get('type') == 'live'
streams_active = filter(is_active, streams)
at_least_one_stream_active = any(streams_active)
