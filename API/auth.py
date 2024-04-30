import os

import gotrue.errors
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def get_user_data():
    user = supabase.auth.get_user()
    user_info = user.model_dump()

    return {
        'user_id': user_info.get('user')['id'],
    }

def api_login(user, cpass):
    try:
        session = supabase.auth.sign_in_with_password({ "email": user, "password": cpass })
    except gotrue.errors.AuthApiError:
        return False
    except gotrue.errors.AuthInvalidCredentialsError:
        return False
    return session, True
def api_register(email: str, cpass: str, username: str):
    supabase.auth.sign_up({ "email": email, "password": cpass })
    user = supabase.auth.get_user()
    
    user_info = user.model_dump()
    user_id = user_info.get('user')['id']

    if user_id:
        supabase.table('Profiles').insert({"profile_id": user_id, "username": username}).execute()
        return True
    else:
        return False

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

    return better_messages

def send_message(message):
    user_id = get_user_data().get('user_id')

    user_profile = supabase.table('Profiles').select('username').eq('profile_id', user_id).execute()
    username = user_profile.data[0]['username']

    supabase.table('Messages').insert([{'user': username, 'message': message}]).execute()

