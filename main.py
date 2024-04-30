from pydub import AudioSegment
from pydub.playback import play
from ttkbootstrap.toast import ToastNotification
from API.configuration import load_settings, template
from API.auth import api_login, api_register, get_messages, send_message

config = load_settings()
authSuccess = False
messages_widgets = []

settings = config['settings']
ui_settings = config['ui_settings']
manifest = config['manifest']

if ui_settings is not None and ui_settings['theme'] is None:
    root = ttk.Window(title="Brew 🍵", themename='darkly', size=[600, 800], resizable=[False, False])
else:
    root = ttk.Window(title="Brew 🍵", themename=ui_settings['theme'] if ui_settings else 'darkly', size=[600, 800],
                      resizable=[False, False])

if config['reset_occurred']:
    resetToast = ToastNotification(
        title="Setting configuration has been reset",
        message=f"Version, {template.get('manifest').get('build')} has been released. "
                "To ensure compatibility, settings have been reset to default. Sorry for the inconvenience.",
        duration=100000,
        alert=True
    )
    resetToast.show_toast()

