import tkinter as tk
from tkinter import filedialog
from pypresence import Presence
import json
import time

# Create a tkinter window
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

# Callback function to clear the input fields
def clear_inputs():
    client_id_entry.delete(0, tk.END)
    details_entry.delete(0, tk.END)
    state_entry.delete(0, tk.END)
    large_image_entry.delete(0, tk.END)
    large_text_entry.delete(0, tk.END)
    small_image_entry.delete(0, tk.END)
    small_text_entry.delete(0, tk.END)
    button1_label_entry.delete(0, tk.END)
    button1_url_entry.delete(0, tk.END)
    button2_label_entry.delete(0, tk.END)
    button2_url_entry.delete(0, tk.END)
    start_checkbutton_var.set(0)

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

# Callback function to save the presence data to a JSON file
def save_presence():
    data = {
        "client_id": client_id_entry.get(),
        "details": details_entry.get(),
        "state": state_entry.get(),
        "large_image": large_image_entry.get(),
        "large_text": large_text_entry.get(),
        "small_image": small_image_entry.get(),
        "small_text": small_text_entry.get(),
        "button1_label": button1_label_entry.get(),
        "button1_url": button1_url_entry.get(),
        "button2_label": button2_label_entry.get(),
        "button2_url": button2_url_entry.get(),
        "start_checked": start_checkbutton_var.get()
    }

    file_path = tk.filedialog.asksaveasfilename(title="Save RPC File", filetypes=(("JSON files", "*.json"),))
    if file_path:
        with open(file_path, "w") as file:
            json.dump(data, file)
            error_message_label.config(text="Presence saved successfully")

# Callback function to load the presence data from a JSON file
def load_presence():
    file_path = tk.filedialog.askopenfilename(initialdir="Presences", title="Select RPC File", filetypes=(("JSON files", "*.json"),))
    if file_path:
        with open(file_path, "r") as file:
            try:
                rpc_data = json.load(file)
                client_id_entry.delete(0, tk.END)
                client_id_entry.insert(0, rpc_data.get("client_id", ""))
                details_entry.delete(0, tk.END)
                details_entry.insert(0, rpc_data.get("details", ""))
                state_entry.delete(0, tk.END)
                state_entry.insert(0, rpc_data.get("state", ""))
                large_image_entry.delete(0, tk.END)
                large_image_entry.insert(0, rpc_data.get("large_image", ""))
                large_text_entry.delete(0, tk.END)
                large_text_entry.insert(0, rpc_data.get("large_text", ""))
                small_image_entry.delete(0, tk.END)
                small_image_entry.insert(0, rpc_data.get("small_image", ""))
                small_text_entry.delete(0, tk.END)
                small_text_entry.insert(0, rpc_data.get("small_text", ""))
                button1_label_entry.delete(0, tk.END)
                button1_label_entry.insert(0, rpc_data.get("button1_label", ""))
                button1_url_entry.delete(0, tk.END)
                button1_url_entry.insert(0, rpc_data.get("button1_url", ""))
                button2_label_entry.delete(0, tk.END)
                button2_label_entry.insert(0, rpc_data.get("button2_label", ""))
                button2_url_entry.delete(0, tk.END)
                button2_url_entry.insert(0, rpc_data.get("button2_url", ""))
                start_checkbutton_var.set(rpc_data.get("start_checked", 0))
                error_message_label.config(text="Presence loaded successfully")
            except json.JSONDecodeError as e:
                error_message_label.config(text=f"Error: Invalid JSON file - {str(e)}")
            except Exception as e:
                error_message_label.config(text=f"Error: {str(e)}")

# Create buttons for actions
update_button = tk.Button(window, text="Update Presence", command=update_presence)
update_button.pack(side="top", pady=5)

clear_presence_button = tk.Button(window, text="Clear Presence", command=clear_presence)
clear_presence_button.pack(side="top", pady=5)

clear_inputs_button = tk.Button(window, text="Clear Inputs", command=clear_inputs)
clear_inputs_button.pack(side="top", pady=5)

save_button = tk.Button(window, text="Save Presence", command=save_presence)
save_button.pack(side="top", pady=5)

load_button = tk.Button(window, text="Load Presence", command=load_presence)
load_button.pack(side="top", pady=5)

# Run the tkinter event loop
window.mainloop()
