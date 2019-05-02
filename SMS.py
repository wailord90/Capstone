# Download the helper library from https://www.twilio.com/docs/python/install
import os

from twilio.rest import Client


def sendText(body, to):

    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=body,
                        from_='+17082953780',
                        to=to
                    )

    print(message.sid)

sendText('Urgent: The system has been compromised','+16182075730')