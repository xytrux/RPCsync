import tkinter as tk
from tkinter import filedialog
import os
import json
from pypresence import Presence
import time

# Create a Tkinter window
window = tk.Tk()
window.title("RPCsync")

# Set up the UI components
error_message_label = tk.Label(window, text="", fg="red")
error_message_label.pack()

# Function to create a labeled entry field and pack it inline
def create_labeled_entry(parent, label_text, entry_width):
    frame = tk.Frame(parent)
    frame.pack(side="top", pady=5)

    label = tk.Label(frame, text=label_text)
    label.pack(side="left")

    entry = tk.Entry(frame, width=entry_width)
    entry.pack(side="left")

    return entry

# Create labeled entry fields and pack them inline
rpc_name_entry = create_labeled_entry(window, "RPC Name:", 30)
client_id_entry = create_labeled_entry(window, "Client ID:", 30)
details_entry = create_labeled_entry(window, "Details:", 30)
state_entry = create_labeled_entry(window, "State:", 30)
large_image_entry = create_labeled_entry(window, "Large Image:", 30)
large_text_entry = create_labeled_entry(window, "Large Image Text (optional):", 30)
small_image_entry = create_labeled_entry(window, "Small Image (optional):", 30)
small_text_entry = create_labeled_entry(window, "Small Image Text (optional):", 30)
button1_label_entry = create_labeled_entry(window, "Button 1 Label (optional):", 30)
button1_url_entry = create_labeled_entry(window, "Button 1 URL (optional):", 30)
button2_label_entry = create_labeled_entry(window, "Button 2 Label (optional):", 30)
button2_url_entry = create_labeled_entry(window, "Button 2 URL (optional):", 30)
start_checkbutton_var = tk.IntVar()
start_checkbutton = tk.Checkbutton(window, text="Time Elapsed", variable=start_checkbutton_var)
start_checkbutton.pack(side="top", pady=5)

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
        "large_image": large_image,
        "large_text": large_text,
        "small_image": small_image,
        "small_text": small_text,
        "buttons": []
    }

    # Add button 1 if label and URL are provided
    if button1_label and button1_url:
        presence["buttons"].append({"label": button1_label, "url": button1_url})

    # Add button 2 if label and URL are provided
    if button2_label and button2_url:
        presence["buttons"].append({"label": button2_label, "url": button2_url})

    # Check if the "Time Elapsed" option is checked
    if start_checkbutton_var.get() == 1:
        presence["start"] = int(time.time())

    discord_rpc.update(**presence)

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

# Callback function to save the RPC inputs to a JSON file
def save_rpc():
    rpc_name = rpc_name_entry.get()
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
    start_checked = start_checkbutton_var.get()

    if rpc_name == "":
        error_message_label.config(text="Error: RPC Name is required")
        return

    rpc_data = {
        "client_id": client_id,
        "details": details,
        "state": state,
        "large_image": large_image,
        "large_text": large_text,
        "small_image": small_image,
        "small_text": small_text,
        "button1_label": button1_label,
        "button1_url": button1_url,
        "button2_label": button2_label,
        "button2_url": button2_url,
        "start_checked": start_checked
    }

    file_path = tk.filedialog.asksaveasfilename(
        initialdir="Presences",
        title="Save RPC File",
        defaultextension=".json",
        filetypes=(("JSON files", "*.json"),)
    )

    if file_path:
        with open(file_path, "w") as file:
            json.dump(rpc_data, file, indent=4)

# Callback function to load the RPC inputs from a JSON file
# Callback function to load the RPC inputs from a JSON file
def load_rpc():
    file_path = tk.filedialog.askopenfilename(
        initialdir="Presences",
        title="Load RPC File",
        filetypes=(("JSON files", "*.json"),)
    )

    if file_path:
        with open(file_path, "r") as file:
            rpc_data = json.load(file)

        rpc_name_entry.delete(0, "end")
        rpc_name_entry.insert(0, os.path.splitext(os.path.basename(file_path))[0])
        client_id_entry.delete(0, "end")
        client_id_entry.insert(0, rpc_data.get("client_id", ""))
        details_entry.delete(0, "end")
        details_entry.insert(0, rpc_data.get("details", ""))
        state_entry.delete(0, "end")
        state_entry.insert(0, rpc_data.get("state", ""))
        large_image_entry.delete(0, "end")
        large_image_entry.insert(0, rpc_data.get("large_image", ""))
        large_text_entry.delete(0, "end")
        large_text_entry.insert(0, rpc_data.get("large_text", ""))
        small_image_entry.delete(0, "end")
        small_image_entry.insert(0, rpc_data.get("small_image", ""))
        small_text_entry.delete(0, "end")
        small_text_entry.insert(0, rpc_data.get("small_text", ""))
        button1_label_entry.delete(0, "end")
        button1_label_entry.insert(0, rpc_data.get("button1_label", ""))
        button1_url_entry.delete(0, "end")
        button1_url_entry.insert(0, rpc_data.get("button1_url", ""))
        button2_label_entry.delete(0, "end")
        button2_label_entry.insert(0, rpc_data.get("button2_label", ""))
        button2_url_entry.delete(0, "end")
        button2_url_entry.insert(0, rpc_data.get("button2_url", ""))
        start_checkbutton_var.set(rpc_data.get("start_checked", 0))

# Create an "Update" button
update_button = tk.Button(window, text="Update", command=update_presence)
update_button.pack()

# Create a "Clear" button
clear_button = tk.Button(window, text="Clear", command=clear_presence)
clear_button.pack()

# Create a "Save" button
save_button = tk.Button(window, text="Save", command=save_rpc)
save_button.pack()

# Create a "Load" button
load_button = tk.Button(window, text="Load", command=load_rpc)
load_button.pack()

# Run the Tkinter event loop
window.mainloop()
