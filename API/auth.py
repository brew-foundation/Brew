import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def api_login(user, cpass):
    session = supabase.auth.sign_in_with_password({ "email": user, "password": cpass })
    
    return session, True

def api_register(user, cpass, username):
    session = supabase.auth.sign_up_with_password({ "email": user, "password": cpass, "data": {
    "username": username
  }})
    return session

def get_messages():
    
    messages = supabase.table('Messages').select('*').execute()
    
    better_messages = []
    for message in messages.data:
        formatted_message = {
            "id": message['message_id'],
            "user": message['user'],
            "message": message['message'],
        }
        better_messages.append(formatted_message)

    print(better_messages)
    return better_messages

def send_message(message):
    session = supabase.auth.get_session()
    supabase.table('Messages').insert([{'user': session.user.user_metadata.username, 'message': message}]).execute()


