import os
import boto3
from ringcentral import SDK
from botocore.exceptions import ClientError
from credentials import client_id, client_secret, phone, username, extension, password, aws_access_key, aws_access_secret, bucket

# PATH PARAMETERS
accountId = client_id
extensionId = extension
secret = client_secret
aws_key = aws_access_key
aws_secret = aws_access_secret


rcsdk = SDK(accountId, secret, 'https://platform.devtest.ringcentral.com')
platform = rcsdk.platform()
platform.login(username, extensionId, password)

def main():
    get_message_store()

def get_message_store():
    # Setting up boto3 for our upload to S3, using credentials.py
    s3 = boto3.client('s3', aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)

    # Specifying we only want VoiceMail records
    queryParams = {
        'messageType': 'VoiceMail'
    }
    # I had issues using my accountId and extensionId in this request, I'll investigate further
    response = platform.get('/restapi/v1.0/account/~/extension/~/message-store', queryParams)
    # print(response.json().records) <-- use this to see how many records/voicemails/texts/faxes exist, for 1 VM it should be 2 records 
    for record in response.json().records:
        # All records have attachments which is the actual data, we're going to check the type for VM
        for attachment in record.attachments:
            # There are audiorecording and audio transcription attachment types for VM, we're only interested in the recording
            if attachment.type == "AudioRecording":
                # Setting a filename to use when we fetch the content from attachment uri
                fileName = (f'vm-{record.attachments[0].id}.mp3')

            # Now we're going to save the mp3

            # Get the voicemail content - can be audio recording or transcription, this doesn't download the content for us to a file though, we have to make the file ourselves
            content = platform.get(f'{attachment.uri}')
        
            # open/create a file with previously defined name, wb because the content is binary
            file = open(f'{fileName}', "wb")
            # write content from get response to the file
            file.write(content.body())

            # Upload file to s3 bucket
            with open(f'{fileName}', "rb") as file:
                s3.upload_fileobj(file, bucket, "voicemail.mp3")

            # close and save!
            file.close

if __name__ ==  "__main__":
    main()