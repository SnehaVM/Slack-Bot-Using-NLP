import time
from slackclient import SlackClient
import greensheet_response

import MySQLdb

BOT_ID = "U51MTV4MQ"

AT_BOT = "<@" + BOT_ID + ">"
attr = "hello"
slack_client = SlackClient('**********')

def handle_command(command, channel):

    response = greensheet_response.DB_Response(command)
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


    def parse_slack_output(slack_rtm_output):
        output_msgs = slack_rtm_output
        if output_msgs and len(output_msgs) > 0:
            for output in output_msgs:
                if output and 'text' in output and AT_BOT in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(AT_BOT)[1].strip().lower(), \
                           output['channel']
        return None, None

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
