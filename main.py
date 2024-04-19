import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.scrolled import ScrolledFrame
from API.configuration import load_settings, template
from API.auth import api_login, api_register, get_messages

config = load_settings()
authSuccess = False
messages_widgets = []

settings = config['settings']
ui_settings = config['ui_settings']
manifest = config['manifest']

if ui_settings is not None and ui_settings['theme'] == None:
    root = ttk.Window(title="Brew 🍵", themename='darkly', size=[600, 800], resizable=[False, False])
else:
    root = ttk.Window(title="Brew 🍵", themename=ui_settings['theme'] if ui_settings else 'darkly', size=[600, 800], resizable=[False, False])

if config['reset_occurred']:
    resetToast = ToastNotification(
        title="Setting configuration has been reset",
        message=f"Version, {template.get('manifest').get('build')} has been released. To ensure compatibility, settings have been reset to default. Sorry for the inconvenience.",
        duration=None,
        alert=True
    )
    resetToast.show_toast()


def update_messages():
    global messages_widgets
    # Destroy all widgets currently in the ScrolledFrame
    for widget in messages_widgets:
        widget.destroy()
    # Clear the list after destroying the widgets
    messages_widgets.clear()

    responses = get_messages()
    for response in responses:
        # Create a new label for each message
        message_label = ttk.Label(messages, text=f'{response["user"]} - {response["message"]}')
        message_label.pack(anchor=W)
        # Add the newly created label to the list for tracking
        messages_widgets.append(message_label)

    # Schedule the next update
    root.after(10000, update_messages)

def login():
    global authSuccess  # Indicate that we're using the global variable
    authSuccess = api_login(user.get(), cpass.get())
    if authSuccess:
        logLabelFrame.pack_forget()
        root.update()
        navbar.pack(fill="both", padx=10, pady=10)
        update_messages()
    else:
        print("Auth Failed")

def signup():
    ...

#* Login area
logLabelFrame = ttk.LabelFrame(root, text=" Brew Account ",bootstyle="light")
logLabelFrame.pack(fill="x", padx=10, pady=10)

userLabel = ttk.Label(master=logLabelFrame, text="Email")
userLabel.pack(fill="x", padx=10, pady=5)


user = ttk.StringVar()
username = ttk.Entry(master=logLabelFrame, bootstyle="dark", textvariable=user)
username.pack(fill="x", padx=10, pady=10)

passwordLabel = ttk.Label(master=logLabelFrame, text="Password")
passwordLabel.pack(fill="x", padx=10, pady=5)

cpass = ttk.StringVar()
password = ttk.Entry(master=logLabelFrame, bootstyle="dark", textvariable=cpass, show="*")
password.pack(fill="x", padx=10, pady=10)

#* When logged in with a valid session ID
navbar = ttk.Notebook(root, bootstyle="dark")

discoverFrame = ttk.Frame(navbar)

messages = ScrolledFrame(discoverFrame, autohide=True)
messages.pack(fill=BOTH, expand=YES, padx=10, pady=10)

navbar.add(discoverFrame, text="Brew Discover")
navbar.add(ttk.Frame(navbar), text="Brew Settings")


#* Buttons
ttk.Separator(master=logLabelFrame, bootstyle="dark").pack(fill="x", padx=10, pady=10)

loginButton = ttk.Button(master=logLabelFrame, text="Login into Brew", bootstyle="success", command=login).pack(fill="x", padx=10, pady=5)

createAccountButton = ttk.Button(master=logLabelFrame, text="Create Account", bootstyle="dark", command=signup).pack(fill="x", padx=10, pady=5)


root.update()
root.mainloop()
