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
    # I had issues using my accountId and extensionId in this request, I'll investigate furhter
    response = platform.get(f'/restapi/v1.0/account/~/extension/~/message-store')
    # print(response.json().records) <-- use this to see how many records/voicemails/texts/faxes exist, for 1 VM it should be 2 records 
    for record in response.json().records:
        # All records have attachments which is the actual data, we're going to check the type for VM
        for attachment in record.attachments:
            # There are audiorecording and audio transcription attachment types for VM, we're only interested in the recording
            if attachment.type == "AudioRecording":
                if record.type == "VoiceMail":
                    # Setting a filename to use when we fetch the content from attachment uri
                    fileName = ("vm-%s.id.mp3" % record.attachments[0].id)

            # Now we're going to save the mp3

            # Fetch the voicemail content - can be audio recording or transcription 
            content = platform.get(f'{attachment.uri}')
            # open/create a file with previously defined name, wb because the content is binary
            file = open(("%s" % fileName), "wb")
            # write content from get response to the file
            file.write(content.body())
            # close and save!
            file.close

main()