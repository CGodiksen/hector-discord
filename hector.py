"""A simple discord bot named Hector.

The discord bot is implemented using a class based design and the "discord.Client" superclass from the
"discord" python package.
"""
import discord
import asyncio
import csv
import dateutil.parser
from datetime import date
import datetime
import json
from bs4 import BeautifulSoup
import requests


class Hector(discord.Client):
    """
    Class representing a discord bot object. The function "on_message" from the super class
    "discord.Clint" is overwritten to implement the functionality of the available commands.
    """

    def __init__(self, **options):
        """Initializing the necessary elements from the super class and starting the looping background task."""
        super().__init__(**options)

        # Create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.background_task())

    async def on_ready(self):
        """Displaying information about the bot when it is ready to run."""
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def background_task(self):
        """Background task that loops and makes a check every 60 second for a specific condition."""
        await self.wait_until_ready()
        while not self.is_closed():
            # Calls the check_events and check_birthday functions if the time is exactly 8.15 in the morning.
            if datetime.datetime.now().hour == 8 and datetime.datetime.now().minute == 15:
                await self.check_events()
                await self.check_birthday()

            await asyncio.sleep(60)

    async def on_message(self, message):
        """
        This method is called every time a message is sent and if the message contains
        a command then that command is executed via another class method.
        """
        # Obtaining some necessary information about the message
        server = message.guild

        # Ignore if the message is from the bot itself.
        if message.author == self.user:
            return

        if message.content == "!hello":
            await self.hello(message)

        if message.content == "!get_out":
            await self.get_out(message)

        if message.content.startswith("!remind_me ", 0, 11):
            await self.remind_me(message)

        if message.content == "!commands":
            await self.commands(message)

        if message.content.startswith("!add_event ", 0, 11):
            await self.add_event(message)

        if message.content.startswith("!lookup ", 0, 8):
            await self.lookup(message)

        # Ensuring that these commands can only be called in a server text channel.
        if type(message.channel) is discord.TextChannel:
            if message.content == "!member_count":
                await self.member_count(message, server)

            if message.content.startswith("!add_birthday ", 0, 14):
                await self.add_birthday(message)

    async def get_out(self, message):
        """Shuts down the bot if the command was made by the owner of the bot."""
        # Pulling the owner ID from the config file and using it to check if the message is sent by the owner.
        with open("config.json", "r") as config_file:
            if message.author.id == json.load(config_file)["owner id"]:
                await self.close()

    @staticmethod
    async def hello(message):
        """Sends a message saying "Hi!"."""
        await message.channel.send("Hi!")

    @staticmethod
    async def member_count(message, server):
        """Sends a message displaying the amount of members in a server."""
        await message.channel.send(server.name + " has " + str(len(server.members)) + " members")

    @staticmethod
    async def remind_me(message):
        """Lets the user specify a message and dm's that message to them after a specified amount of time."""
        message_list = message.content.split()

        # Splitting the message into the different parts
        dm_message = " ".join(message_list[1:-1])

        # Only works if a time is specified
        try:
            time_to_wait = int(message_list[-1])
            if time_to_wait <= 1440:
                # React with the thumbs up emoji. \N{THUMBS UP SIGN} is the unicode name for the emoji.
                await message.add_reaction("\N{THUMBS UP SIGN}")
                await asyncio.sleep(time_to_wait * 60)

                if dm_message == "":
                    await message.author.send("You did not specify a message")
                else:
                    await message.author.send(dm_message)
            else:
                await message.channel.send("You can't specify a time that is over 24 hours")

        except ValueError:
            await message.channel.send("You need to specify a time")

    @staticmethod
    async def add_birthday(message):
        """Adds a new birthday to the list of birthdays for the given server."""
        message_list = message.content.split()

        # Splitting the message into the different parts
        birthday_name = " ".join(message_list[1:-1])
        birthday_date = message_list[-1]

        # Checking if the given date can be parsed into a datetime.datetime object
        try:
            dateutil.parser.parse(message_list[-1])
        except ValueError:
            await message.channel.send("This is not a supported date format")
            return

        # Adding the birthday to the csv file of birthdays
        with open("birthdays.csv", "a", newline="") as file:
            birthday_writer = csv.writer(file)
            birthday_writer.writerow([message.channel.id, birthday_name, birthday_date])
            await message.add_reaction("\N{THUMBS UP SIGN}")

    @staticmethod
    async def check_birthday():
        """
        Sends a happy birthday message if it's someones birthday.
        The message is sent in the same channel the birthday was added in.
        """
        with open("birthdays.csv", "r") as file:
            birthdays = csv.reader(file)
            # Checking if it's a persons birthday by checking if the day and month are the same (ignoring year)
            for row in birthdays:
                if dateutil.parser.parse(row[2]).date().day == date.today().day \
                        and dateutil.parser.parse(row[2]).date().month == date.today().month:
                    await client.get_channel(int(row[0])).send("Happy birthday " + row[1].title() + "!")

    @staticmethod
    async def commands(message):
        """Sends a list of the currently available commands for Hector."""
        await message.channel.send("The currently available commands are:\n"
                                   "!hello\n"
                                   "!member_count\n"
                                   "!remind_me ***message*** ***time***\n"
                                   "!add_event ***message*** ***date***\n"
                                   "!add_birthday ***name*** ***date***\n"
                                   "!lookup ***term***")

    @staticmethod
    async def add_event(message):
        """Adds a new event to the list of active events for the specific server."""
        message_list = message.content.split()

        # Splitting the message into the different parts
        event_message = " ".join(message_list[1:-1])
        event_date = message_list[-1]

        # Checking if the given date can be parsed into a datetime.datetime object.
        try:
            dateutil.parser.parse(message_list[-1])
        except ValueError:
            await message.channel.send("This is not a supported date format")
            return

        # Ensuring that the entered date is in the future and not today or in the past.
        if dateutil.parser.parse(message_list[-1]) <= datetime.datetime.now():
            await message.channel.send("That is in the past, let's think about the future instead.")
            return

        # If it's a private chat we need to use the author id so we can send a private message.
        # The problem with saving the dm_channel id is that dm channels are not kept in the cache for long.
        if type(message.channel) is discord.TextChannel:
            message_id = message.channel.id
        else:
            message_id = message.author.id

        # Appending the file that contains the currently active events
        with open("events.csv", "a", newline="") as file:
            event_writer = csv.writer(file)

            event_writer.writerow([message_id, event_message, event_date])
            await message.add_reaction("\N{THUMBS UP SIGN}")

    @staticmethod
    async def check_events():
        """
        Looks through the list of events and sends the events that are scheduled for today.
        If an event is sent then it is deleted from the file containing the currently active events.
        """
        # Trying to open the file for reading, if it doesnt exist it throws an OSError.
        try:
            with open("events.csv", "r") as file:
                active_events = []

                # Goes through all the rows and checks if it scheduled for today, if so it sends the specified message
                # if not it adds it to the list of still active events.
                for row in csv.reader(file):
                    if dateutil.parser.parse(row[2]).date() == date.today():
                        # The id (row[0]) can either be a server channel id or a message author id from a dm channel.
                        if type(client.get_channel(int(row[0]))) is discord.TextChannel:
                            await client.get_channel(int(row[0])).send(row[1])
                        else:
                            await client.get_user(int(row[0])).send(row[1])
                    else:
                        active_events.append(row)

            # Overwriting the file so it only contains the currently active events
            with open("events.csv", "w", newline="") as file:
                event_writer = csv.writer(file)

                for row in active_events:
                    event_writer.writerow(row)
        except OSError:
            return

    @staticmethod
    async def lookup(message):
        """Looks up a term in the MI book index and sends the section link that contains information about it."""
        term = message.content[8:]

        # The url containing the index for the book "Artificial intelligence: Foundations of computational agents".
        url = "https://artint.info/2e/html/ArtInt2e.idx.html"
        index_site = requests.get(url)

        # Creating a html lxml parser with beautifulsoup4, this is used for pulling data out of the websites html.
        index_parser = BeautifulSoup(index_site.text, "lxml")

        # Creating an id that corresponds to the requested look up term, this id will be used to find the correct link.
        lookup_id = term.replace(" ", "")

        # If the given term does not exist, we want to catch the exception and give a relevant error message.
        try:
            # Finding the section href link that contains the target word using the lookup id.
            section_link = index_parser.find("li", id=lookup_id).find("a", {"class": "ltx_ref"}).get("href")
        except AttributeError:
            await message.channel.send("I can't find any sections that contain information about \"" + term + "\"")
            return

        # The section_link needs to be appended to the rest of the url to create a visitable url.
        section_link = "https://artint.info/2e/html/" + section_link

        # Sending the link that corresponds to the target word.
        await message.channel.send("You can find information on \"" + term + "\" at: \n" + section_link)

        # TODO: Send a message containing the specific paragraph that contains the information needed.
        # Grabbing the html from the section site and creating a bs4 parser for it, the same as above for the index.
        # section_site = requests.get(section_link)
        # section_parser = BeautifulSoup(section_site.text, "lxml")

    # TODO: Make an analyse() function that can give information regarding a specific user

    # TODO: Make a translate function that can translate a non-english and non-danish message into english


client = Hector()

# Pulling the token from the config file and using it to run the bot.
with open("config.json", "r") as config:
    client.run(json.load(config)["token"])
