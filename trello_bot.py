import os
import requests
from slack_sdk import WebClient
from slack_bolt import App
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID')
TRELLO_LIST_NAME = os.getenv('TRELLO_LIST_NAME')

# Initialize the Slack app (Bolt framework)
app = App(token=SLACK_BOT_TOKEN)

# Fetch Trello cards from the "To Do" list
def get_trello_cards():
    url = f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists?cards=all&key={TRELLO_API_KEY}&token={TRELLO_TOKEN}"
    response = requests.get(url)
    
    # Check for successful response
    if response.status_code == 200:
        lists = response.json()
        tasks = []
        for lst in lists:
            if lst['name'].lower() == TRELLO_LIST_NAME.lower():
                for card in lst['cards']:
                    tasks.append(card['name'])
        return tasks
    else:
        raise Exception(f"Failed to fetch data from Trello API. Status Code: {response.status_code}")

# Post a message to Slack channel
def post_to_slack(channel, message):
    slack_client = WebClient(token=SLACK_BOT_TOKEN)
    response = slack_client.chat_postMessage(channel=channel, text=message)
    return response

# Respond to the message "show me todo"
@app.message("show me todo")
def show_todo_tasks(message, say):
    tasks = get_trello_cards()
    
    # Construct message based on Trello tasks
    if tasks:
        task_list = "\n".join(tasks)
        response_message = f"Here are the 'To Do' tasks:\n{task_list}"
    else:
        response_message = "No tasks found in 'To Do'."
    
    # Post the tasks message back to Slack
    post_to_slack(message['channel'], response_message)

# Start the Slack Bolt app (to listen for events using Socket Mode)
if __name__ == "__main__":
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
