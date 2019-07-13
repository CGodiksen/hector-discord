# Hector
Hector is a very simple discord bot meant as a learning project for the creator. This is not a discord bot that tries to
innovate in any shape or form.

## Installation
If you want to download and use Hector for yourself then some setup is required.  

First, you need to install all the required python packages that are used in the project, this can be done by navigating to where you normally install python packages and using the command ```$ pip install requirements.txt```. This will pull the required packages from the included requirements.txt file and install them.

Secondly, you need to set up a ```config.json``` file in the main project directory. This file is needed to store your bots token and your own personal ID from discord. The token is used to run the bot and your ID is used to make it so only you can run the privileged command <b>!get_out</b>, that shuts down the bot. Just create a new file called ```config.json``` and make it contain the following:
```
{
  "token": YourTokenStringHere
  "owner id": YourIDIntHere
}
```
When you have completed these two steps then Hector should be fully functional. 
## Usage
The currently available commands for Hector are:  

<b>!hello</b>  
Says Hi!

<b>!member_count</b>  
Returns the amount of members in the server the message was sent from.

<b>!remind_me <em>message time</em></b>  
Sends a private message to the person who sent the command, containing the specified message. The message is sent after a specified
amount of time has passed (Max 24 hours in the future).

<b>!add_birthday <em>name date</em></b>  
Adds a new birthday to the list of birthdays being kept in the system. An automatic birthday greeting will be sent from the system at 8.15 on the specified day in the text channel where the <b>!add_birthday</b> entry was made.

<b>!add_event <em>message date</em></b>  
Adds an event to the system that contains the specified message. At 8.15 on the specified date the system will resend the message in the chat where the event was created, thereby working as an alert system. This can also be seen as the long term version of 
<b>!remind_me</b>.

<b>!commands</b>  
Displays a list of the currently available commands for Hector. 

## Current use


Hector is currently running on a Raspberry Pi 3b+ and is therefore not meant for widespread use. The current scope of Hectors use
is one discord server with 6 members and a private discord server with only me in it for testing purposes.

## Contributing
This project is currently private and there is no plans on making outside contributions to the project available in the near future.
