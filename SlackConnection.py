from slackclient import SlackClient
from flask import request, Flask

app = Flask(__name__)
slack_token = "Bot token" #replace this with bot token
sc = SlackClient(slack_token)

@app.route('/endpoint', methods=["POST"])
def requestcontroller():
    slack_message = request.get_json()

    if 'challenge' in slack_message:
        return slack_message['challenge']

    if 'user' in slack_message['event']:
        channelid = slack_message['event']['channel']
        usermessage = slack_message['event']['text']

        reponse = getUserTextResponse(usermessage)

        sc.api_call(
            "chat.postMessage",
            channel=channelid,
            text=reponse
        )
        return '200'
    else:
        return '200'


def getUserTextResponse(usertext):
    '''
    Implement this message according to your usecase
    :param usertext: User message
    :return: Response for user message
    '''
    pass

if __name__ == '__main__':
    app.run(debug=True, port=8080)
