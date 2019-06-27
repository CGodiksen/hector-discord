# Token: ***REMOVED***
# Permissions: 8
# Client ID: ***REMOVED***
# OAUTH2 URL: ***REMOVED***
import discord
import asyncio
import csv
from datetime import date


class Hector(discord.Client):
    async def on_ready(self):
        print("We have logged in as " + str(self.user))

    async def on_message(self, message):
        # Ignore if the message is from the bot itself.
        if message.author == self.user:
            return

        if message.content == "!hello":
            await message.channel.send("Hi!")

        if message.content == "!get_out":
            await self.get_out(message)

        if message.content == "!member_count":
            await self.member_count(message)

        if message.content.startswith("!remind_me ", 0, 11):
            await self.remind_me(message)

        if message.content == "!birthday":
            await self.birthday(message)

        if message.content == "!commands":
            await self.commands(message)

    # Shuts down the bot if the command was made by me (and only me).
    async def get_out(self, message):
        if message.author.id == ***REMOVED***:
            await self.close()

    # Sends a message containing the amount of members in a server, if the command request was made in a server.
    @staticmethod
    async def member_count(message):
        try:
            server = message.guild
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
                await message.channel.send("I will remind you of that")
                await asyncio.sleep(time_to_wait * 60)

                if dm_message == "":
                    await message.author.send("You did not specify a message")
                else:
                    await message.author.send(dm_message)
            else:
                await message.channel.send("You can't specify a time that is over 24 hours")

        except ValueError:
            await message.channel.send("You need to specify a time")

    # Sends a happy birthday message if it's someone in the servers birthday.
    @staticmethod
    async def birthday(message):
        with open("birthdays.csv", "r+") as fileobject:
            birthdays = csv.reader(fileobject)

            birthday = False
            for birthday in birthdays:
                if birthday[0] == str(date.today().day) \
                        and birthday[1] == str(date.today().month):
                    await message.channel.send("Happy birthday " + birthday[2].title() + "!")
                    birthday = True

            if not birthday:
                await message.channel.send("There is nothing to be happy about today")

    # Sends a list of the currently available commands for Hector
    @staticmethod
    async def commands(message):
        await message.channel.send("The currently available commands are:\n"
                                   "!hello\n"
                                   "!member_count\n"
                                   "!remind_me ***message*** ***time***\n"
                                   "!birthday")


client = Hector()
client.run("***REMOVED***")
