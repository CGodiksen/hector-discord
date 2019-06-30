# Token: ***REMOVED***
# Permissions: 8
# Client ID: ***REMOVED***
# OAUTH2 URL: ***REMOVED***
import discord
import asyncio
import csv
import dateutil.parser
from datetime import date
import datetime


class Hector(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)

        # Create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    # A task that is run on a loop in it's own thread, it does something every 60 seconds.
    async def background_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            # Calls the check_events and check_birthday functions if the time is exactly 8.15 in the morning.
            if datetime.datetime.now().hour == 8 and datetime.datetime.now().minute == 15:
                await self.check_events()
                await self.check_birthday()

            await asyncio.sleep(60)

    async def on_message(self, message):
        # Obtaining some necessary information about the message
        server = message.guild

        # Ignore if the message is from the bot itself.
        if message.author == self.user:
            return

        if message.content == "!hello":
            await message.channel.send("Hi!")

        if message.content == "!get_out":
            await self.get_out(message)

        if message.content.startswith("!remind_me ", 0, 11):
            await self.remind_me(message)

        if message.content == "!commands":
            await self.commands(message)

        if message.content.startswith("!add_event ", 0, 11):
            await self.add_event(message)

        # Ensuring that these commands can only be called in a server text channel.
        if type(message.channel) is discord.TextChannel:
            if message.content == "!member_count":
                await self.member_count(message, server)

            if message.content.startswith("!add_birthday ", 0, 14):
                await self.add_birthday(message)

    # Shuts down the bot if the command was made by me (and only me).
    async def get_out(self, message):
        if message.author.id == ***REMOVED***:
            await self.close()

    # Sends a message containing the amount of members in a server, if the command request was made in a server.
    @staticmethod
    async def member_count(message, server):
        try:
            await message.channel.send(server.name + " has " + str(len(server.members)) + " members")
        except AttributeError:
            await message.channel.send("This is not a server you fool!")

    # Lets the user specify a message and dm's that message to them after
    # a specified amount of time.
    @staticmethod
    async def remind_me(message):
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

    # Adds a new birthday to the list of birthdays
    @staticmethod
    async def add_birthday(message):
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

    # Sends a happy birthday message if it's someone in the servers birthday.
    @staticmethod
    async def check_birthday():
        with open("birthdays.csv", "r") as file:
            birthdays = csv.reader(file)
            # Checking if it's a persons birthday by checking if the day and month are the same (ignoring year)
            for row in birthdays:
                if dateutil.parser.parse(row[2]).date().day == date.today().day \
                        and dateutil.parser.parse(row[2]).date().month == date.today().month:
                    await client.get_channel(int(row[0])).send("Happy birthday " + row[1].title() + "!")

    # Sends a list of the currently available commands for Hector
    @staticmethod
    async def commands(message):
        await message.channel.send("The currently available commands are:\n"
                                   "!hello\n"
                                   "!member_count\n"
                                   "!remind_me ***message*** ***time***\n"
                                   "!add_event ***message*** ***date***\n"
                                   "!add_birthday ***name*** ***date***")

    # Creating a new event that will be added to the list of events for the specific server
    @staticmethod
    async def add_event(message):
        # TODO: Make it possible to add events to private chats
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

    # Looking through the list of events and sending the events that are happening today
    @staticmethod
    async def check_events():
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

    # TODO: Make an analyse() function that can give information regarding a specific user


client = Hector()
client.run("***REMOVED***")
