# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


def sendText(body, to):

    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'ACfe8aa91185356e31ad9390cca0d979ed'
    auth_token = 'd8d79d13533d40357b27518e4bbe8473'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=body,
                        from_='+16184000956',
                        to=to
                    )

    print(message.sid)

sendText('Urgent: The system has been compromised','+16182075730')