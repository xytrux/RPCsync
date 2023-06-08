import tkinter as tk
from pypresence import Presence
import time

# Create a Tkinter window
window = tk.Tk()
window.title("RPCsync")

# Set the app icon
#window.iconbitmap("app_icon.ico")

# Set up the UI components
error_message_label = tk.Label(window, text="", fg="red")
error_message_label.pack()

client_id_label = tk.Label(window, text="Client ID:")
client_id_label.pack()
client_id_entry = tk.Entry(window)
client_id_entry.pack()

details_label = tk.Label(window, text="Details:")
details_label.pack()
details_entry = tk.Entry(window)
details_entry.pack()

state_label = tk.Label(window, text="State:")
state_label.pack()
state_entry = tk.Entry(window)
state_entry.pack()

large_image_label = tk.Label(window, text="Large Image:")
large_image_label.pack()
large_image_entry = tk.Entry(window)
large_image_entry.pack()

large_text_label = tk.Label(window, text="Large Image Text (optional):")
large_text_label.pack()
large_text_entry = tk.Entry(window)
large_text_entry.pack()

small_image_label = tk.Label(window, text="Small Image (optional):")
small_image_label.pack()
small_image_entry = tk.Entry(window)
small_image_entry.pack()

small_text_label = tk.Label(window, text="Small Image Text (optional):")
small_text_label.pack()
small_text_entry = tk.Entry(window)
small_text_entry.pack()

button1_label_label = tk.Label(window, text="Button 1 Label (optional):")
button1_label_label.pack()
button1_label_entry = tk.Entry(window)
button1_label_entry.pack()

button1_url_label = tk.Label(window, text="Button 1 URL (optional):")
button1_url_label.pack()
button1_url_entry = tk.Entry(window)
button1_url_entry.pack()

button2_label_label = tk.Label(window, text="Button 2 Label (optional):")
button2_label_label.pack()
button2_label_entry = tk.Entry(window)
button2_label_entry.pack()

button2_url_label = tk.Label(window, text="Button 2 URL (optional):")
button2_url_label.pack()
button2_url_entry = tk.Entry(window)
button2_url_entry.pack()

start_checkbutton_var = tk.IntVar()
start_checkbutton = tk.Checkbutton(window, text="Enable Start", variable=start_checkbutton_var)
start_checkbutton.pack()

# Initialize the Discord RPC client
discord_rpc = None

# Callback function to update the presence when the "Update" button is clicked
def update_presence():
    global discord_rpc

    # Clear the error message
    error_message_label.config(text="")

    # Get the client ID, details, state, large image, large image text, small image, small image text, button 1 label, button 1 URL, button 2 label, and button 2 URL from the user input
    client_id = client_id_entry.get()
    details = details_entry.get()
    state = state_entry.get()
    large_image = large_image_entry.get()
    large_text = large_text_entry.get()
    small_image = small_image_entry.get()
    small_text = small_text_entry.get()
    button1_label = button1_label_entry.get()
    button1_url = button1_url_entry.get()
    button2_label = button2_label_entry.get()
    button2_url = button2_url_entry.get()

    if client_id == "":
        error_message_label.config(text="Error: Client ID is required")
        return

    try:
        client_id = int(client_id)
    except ValueError:
        error_message_label.config(text="Error: Invalid Client ID")
        return

    if discord_rpc is None:
        discord_rpc = Presence(client_id)
        discord_rpc.connect()

    # Set the presence details and state
    presence = {
        "details": details,
        "state": state,
        "large_image": large_image
    }

    # Add large image text if provided
    if large_text:
        presence["large_text"] = large_text

    # Add small image and small image text if provided
    if small_image:
        presence["small_image"] = small_image
    if small_text:
        presence["small_text"] = small_text

    # Add buttons if label and URL are provided
    buttons = []
    if button1_label and button1_url:
        buttons.append({
            "label": button1_label,
            "url": button1_url
        })
    if button2_label and button2_url:
        buttons.append({
            "label": button2_label,
            "url": button2_url
        })

    if buttons:
        presence["buttons"] = buttons

    # Check if the start parameter should be included
    if start_checkbutton_var.get():
        presence["start"] = int(time.time())

    try:
        discord_rpc.update(**presence)
    except Exception as e:
        error_message_label.config(text=f"Error: {str(e)}")

# Callback function to clear the Discord RPC presence
def clear_presence():
    global discord_rpc
    if discord_rpc is not None:
        discord_rpc.clear()
        discord_rpc.close()
        discord_rpc = None

    # Clear the error message
    error_message_label.config(text="")

# Ctrl+A shortcut handler
def select_all(event):
    event.widget.select_range(0, "end")
    event.widget.icursor("end")
    return "break"

# Bind Ctrl+A shortcut to text entry fields
client_id_entry.bind("<Control-a>", select_all)
details_entry.bind("<Control-a>", select_all)
state_entry.bind("<Control-a>", select_all)
large_image_entry.bind("<Control-a>", select_all)
large_text_entry.bind("<Control-a>", select_all)
small_image_entry.bind("<Control-a>", select_all)
small_text_entry.bind("<Control-a>", select_all)
button1_label_entry.bind("<Control-a>", select_all)
button1_url_entry.bind("<Control-a>", select_all)
button2_label_entry.bind("<Control-a>", select_all)
button2_url_entry.bind("<Control-a>", select_all)

# Create an "Update" button
update_button = tk.Button(window, text="Update", command=update_presence)
update_button.pack()

# Create a "Clear" button
clear_button = tk.Button(window, text="Clear", command=clear_presence)
clear_button.pack()

# Run the Tkinter event loop
window.mainloop()
