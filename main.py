from credentials import client_id, client_secret, phone, username, extension, password

# PATH PARAMETERS
accountId = client_id
extensionId = extension
secret = client_secret

import os
from ringcentral import SDK
rcsdk = SDK(accountId, secret, 'https://platform.devtest.ringcentral.com')
platform = rcsdk.platform()
platform.login(username, extensionId, password)

def main():
    get_message_store()

def get_message_store():
    response = platform.get(f'/restapi/v1.0/account/~/extension/~/message-store')
    print(response.json().records)
    for record in response.json().records:
        print(record.attachments)
        for attachment in record.attachments:
            # There are audiorecording and audio transcription attachment types, we're only interested in the recording
            if attachment.type == "AudioRecording":
                if record.type == "VoiceMail":
                    fileName = "{record.attachments[0].id}.mp3"
            
            # Now we're going to save the mp3
            content = platform.get(f'{attachment.uri}')
            file = open("/content{fileName}", "w")
            file.write(content.body())
            file.close

main()