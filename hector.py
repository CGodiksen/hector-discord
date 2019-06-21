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
        # Ignore if the message is from the bot itself
        if message.author == self.user:
            return

        if message.content == "!hello":
            await message.channel.send("Hi!")

        if message.content == "!get_out":
            if message.author.id == ***REMOVED***:
                await self.close()

        if message.content == "!member_count":
            server = message.guild
            await message.channel.send(server.name + " has " +
                                       str(len(server.members)) + " members")

        # Lets the user specify a message and dm's that message to them after
        # a specified amount of time
        if message.content.startswith("!remind_me ", 0, 11):
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

        if message.content == "!birthday":
            await message.channel.send(self.get_birthday())

        if message.content == "!commands":
            await message.channel.send("The currently available commands are:\n"
                                       "!hello\n"
                                       "!member_count\n"
                                       "!remind_me ***message*** ***time***\n"
                                       "!birthday")

    @staticmethod
    def get_birthday():

        with open("birthdays.csv", "r+") as fileobject:
            birthdays = csv.reader(fileobject)

            for birthday in birthdays:
                if birthday[0] == str(date.today().day) \
                        and birthday[1] == str(date.today().month):
                    return "Happy birthday " + birthday[2].title() + "!"

        return "There is nothing to be happy about today"


client = Hector()
client.run("***REMOVED***")
