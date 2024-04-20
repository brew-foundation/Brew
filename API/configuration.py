import json
import os


template = {
    'manifest': {
        'version': '0.1.0-dev',

        'build': '2024.04.19.0.1.0Dev1',
    },

    'settings': {
        'UI': {
            'theme': 'darkly'
        }
    }
}

user_root_dir = os.path.expanduser('~')
settings_file_path = os.path.join(user_root_dir, 'brew.json')

def load_settings():
    # Initialize variables at the start of the function to ensure they are always defined
    settings = {}
    ui_settings = None
    manifest = {}
    reset_occurred = False
    file_created = False

    if os.path.exists(settings_file_path):
        with open(settings_file_path, 'r') as file:
            current_settings = json.load(file)

            settings = current_settings.get('settings', {})
            manifest = current_settings.get('manifest', {})
            ui_settings = settings.get('UI', None)

            if current_settings.get('manifest', {}).get('build') != template.get('manifest', {}).get('build'):
                with open(settings_file_path, 'w') as file:
                    json.dump(template, file, indent=4)
                reset_occurred = True
    else:
        with open(settings_file_path, 'w') as file:
            json.dump(template, file, indent=4)
    
        with open(settings_file_path, 'r') as file:
            current_settings = json.load(file)

            settings = current_settings.get('settings', {})
            manifest = current_settings.get('manifest', {})
            ui_settings = settings.get('UI', None)

            if current_settings.get('manifest', {}).get('build') != template.get('manifest', {}).get('build'):
                with open(settings_file_path, 'w') as file:
                    json.dump(template, file, indent=4)

    return {
        'settings': settings,
        'ui_settings': ui_settings,
        'manifest': manifest,
        'reset_occurred': reset_occurred,
    }
