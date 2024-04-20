import ttkbootstrap as ttk
import re 
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
from API.configuration import load_settings, template
from API.auth import api_login, api_register, get_messages, send_message

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

    messages.yview_scroll(50, 'px')
    # Schedule the next update
    root.after(1000, update_messages)

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

def is_valid_email(email):
    # Simple regex for validating an email address
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def signup():
    email = regEmail.get()
    password = regPassword.get()
    user = regUser.get()
    if not is_valid_email(email):
        Messagebox.show_error(message="An error has occurred while registering your account.", title='Account registration failed!', alert=True,) 
        return False
    if password == ConfirmRegPassword.get():
        print(f"{regUser.get()} - {regEmail.get()} - {regPassword.get()}")
        if api_register(email=email, username=user, cpass=password):
            Messagebox.ok(message="Account has been registered with Brew Services. Please login now.", title='Account registration successful!', alert=True,) 
        else:
            Messagebox.show_error(message="An error has occurred while registering your account.", title='Account registration failed!', alert=True,) 
    else:
        Messagebox.show_error(message="Passwords do not match.", title='Credential(s) not matching!', alert=True,) 

def send():
    message_text = Message.get()
    send_message(message_text)

    sent = ToastNotification(
        title="Message has been sent!",
        message="Your message has been sent to Brew's servers",
        duration=5000,
        alert=False
    )
    sent.show_toast()

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

messages = ScrolledFrame(discoverFrame, autohide=True, height=600)
messages.enable_scrolling()
messages.pack(fill='both', expand=YES, padx=10, pady=10)

navbar.add(discoverFrame, text="Brew Discover")
navbar.add(ttk.Frame(navbar), text="Brew Settings")

ttk.Separator(master=logLabelFrame, bootstyle="dark").pack(fill="x", padx=10, pady=10)

loginButton = ttk.Button(master=logLabelFrame, text="Login into Brew", bootstyle="success", command=login).pack(fill="x", padx=10, pady=5)

#* Registration
regLabelFrame = ttk.LabelFrame(logLabelFrame, text=" Register a Brew account ",bootstyle="caution")
regLabelFrame.pack(fill="x", padx=10, pady=10)

userLabel = ttk.Label(master=regLabelFrame, text="Username")
userLabel.pack(fill="x", padx=10, pady=5)

regUser = ttk.StringVar()
regUsername = ttk.Entry(master=regLabelFrame, bootstyle="dark", textvariable=regUser)
regUsername.pack(fill="x", padx=10, pady=10)

emailLabel = ttk.Label(master=regLabelFrame, text="Email")
emailLabel.pack(fill="x", padx=10, pady=5)

regEmail = ttk.StringVar()
regEmail = ttk.Entry(master=regLabelFrame, bootstyle="dark", textvariable=regEmail)
regEmail.pack(fill="x", padx=10, pady=10)

passwordLabel = ttk.Label(master=regLabelFrame, text="Password")
passwordLabel.pack(fill="x", padx=10, pady=5)

regPassword = ttk.StringVar()
regPassword = ttk.Entry(master=regLabelFrame, bootstyle="dark", textvariable=regPassword, show="*")
regPassword.pack(fill="x", padx=10, pady=10)

confirmPasswordLabel = ttk.Label(master=regLabelFrame, text="Confirm Password")
confirmPasswordLabel.pack(fill="x", padx=10, pady=5)

ConfirmRegPassword = ttk.StringVar()
ConfirmRegPassword = ttk.Entry(master=regLabelFrame, bootstyle="dark", textvariable=ConfirmRegPassword, show="*")
ConfirmRegPassword.pack(fill="x", padx=10, pady=10)

createAccountButton = ttk.Button(master=regLabelFrame, text="Create Account", bootstyle="dark", command=signup).pack(fill="x", padx=10, pady=5)

#* Brew discover page
Message = ttk.StringVar()
MessageEntry = ttk.Entry(master=discoverFrame, bootstyle="dark", textvariable=Message)

MessageSendButton = ttk.Button(master=discoverFrame, bootstyle="info", text="Send message", command=send)


MessageEntry.pack(fill="x", padx=10, pady=10)
MessageSendButton.pack(fill="x", padx=10, pady=10)

root.update()
root.mainloop()
