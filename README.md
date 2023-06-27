# RPCsync

The world's most easy-to-use Discord RPC client

(please drop a star if you enjoy it)

# Features

- Simple, easy-to-use interface
- RPC saving
- Button support
- No advertisements (though I'd appreciate it if you mentioned your RPC was made with it)

# Screenshots

![](https://github.com/Xytrux/RPCsync/blob/main/RPCsync-window.png?raw=true)

![](https://github.com/Xytrux/RPCsync/blob/main/RPCsync-full.png?raw=true)

# Making your RPC

In order to make your RPC, you must head to the [Discord Developer Portal](https://discord.com/developers/applications)

Once you've made your way there, you want to hit "New Application" in the top right corner.

Next, you wanna name your RPC (this will also be what displays in your status. Ex. Playing **Minecraft**)

Once, thats done, you wanna look at the sidebar on the left and click "Rich Presence." Make sure you are on "Art Assets" in the dropdown.

Scroll down and start adding your images!

Once you have added your images, navigate to the OAuth page in the sidebar.

Once there, copy the client ID.

And then simply insert your assets and client ID into the client!

# Guide

This guide provides step-by-step instructions on how to run RPCsync using the provided code. There are 2 ways.

# Script

To simplify the process of running RPCsync, you can use the bash script!

To run the script, open a terminal, navigate to the directory where the script is located, and execute the following command:
```
bash run.sh
```
The script will activate a virtual environment if specified (uncomment the appropriate line), install the required packages, and then run RPCsync.

# Manually

## Step 1: Install the required dependencies

- Make sure you have Python installed on your computer. If not, download and install Python from the official website: [python.org](https://www.python.org/downloads/).
- Open a terminal or command prompt and run the following command to install the necessary packages:
```
pip install pypresence
```
## Step 2: Prepare the code and resources

- Copy the provided code into a text editor and save it with a ".py" extension, for example, `rpcsync.py`.

## Step 3: Run the application

- Open a terminal or command prompt and navigate to the directory where you saved the Python script and icon file.
- Run the following command to start the application:
```
python rpcsync.py
```

## Step 4: Interact with the application

- The application window will open, showing various input fields for configuring the Discord RPC.
- Fill in the required fields, such as the Client ID and presence details.
- Optionally, enable the "Enable Start" checkbox to include the start parameter in the presence.
- Click the "Update" button to update the presence on Discord.
- To clear the presence, click the "Clear" button.
- You can use the Ctrl+A shortcut to select all the text in an input field for easier editing.

## Step 5: Customize and experiment

- Feel free to experiment with different input values and configurations to update your Discord RPC presence as desired.
- You can modify the code to add more functionality or customize the user interface according to your preferences.

That's it! You now have a basic guide on how to run RPCsync using the provided code. Have fun customizing your Discord presence!
