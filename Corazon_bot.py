# -*- coding: utf-8 -*-
"""
This is a test Discord bot for practice using the discord API. It was inspired by popular One Piece character Corazon,
who it quotes when prompted.
"""

import discord
import nest_asyncio
import configparser

#Credentials 
config = configparser.ConfigParser()
config.read('Corazon_config.ini')
TOKEN = config['Discord']['token']
my_channel = config['Discord']['channel']
my_channel = int(my_channel)



intents = discord.Intents.default()
intents.message_content = True

nest_asyncio.apply()

client = discord.Client(intents = intents)



#Discord Commands for the Corazon chatbot
commands = ["!Law","!Mingo","!Doffy","!Future","!Acting","!Sengoku","!Navy","!Habits","!Thumbs","!Stop", "fuckit"]


#Helper methods
def list_commands(commands):
    command_text = ""
    print("List of Commands:")
    for each in commands:
        temp = each
        temp2 = "\n"
        print(f"Command: {temp}")
        if commands.index(each) == 0:
            command_text = command_text + temp
        else:
            command_text = command_text + temp2 + temp
    # print(command_text)
    return(command_text)

def get_img(text):
    with open(text, 'rb') as f:
        picture = discord.File(f)
    return picture
def get_channels():
    channel_list = ""
    for server in client.servers:
        for channel in server.channels:
            if channel.type == 'Text':
                channel_list + channel + ", "
    return channel_list

# def get_all_chans():
    # channel_list = client.get_chann
    # return channel_list



#Discord events to listen for
@client.event
async def on_ready():
    print("\nwe have liftoff.".format(client))
    channel = client.get_channel(my_channel)
    print(f"\nChannel : {channel}")
    await channel.send("Corazon Connected \U0001F601")
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    username = str(message.author).split('#',0)
    user_message = str(message.content)
    print(user_message)
    channel = str(message.channel)
    if message.channel.name == "general":
        print(f"Responding to {username} on the {channel} channel.\nMessage: {user_message}")
        
        
        if user_message.startswith("!Commands"):
            commds = list_commands(commands)
            await message.channel.send(commds)
            return
        elif user_message.startswith("!Law"):
            await message.channel.send('You are the one in pain.')
            return
        elif user_message.startswith("!Mingo"):
            await message.channel.send("Go to jail, don't collect $100.")
            return
        elif user_message.startswith("!Doffy"):
            await message.channel.send("How did you turn up like this, how did you turn up like this?")
            return
        elif user_message.startswith("!Future"):
            await message.channel.send("If you ever think of me in the future, I want you to remember me smiling. \U0001f642")
            return
        elif user_message.startswith("!Acting"):
            await message.channel.send("It's all an act.")
            return
        elif user_message.startswith("!Sengoku"):
            await message.channel.send("Budha Buddy.")
            return
        elif user_message.startswith("!Navy"):
            await message.channel.send("...")
            return
        elif user_message.startswith("!Habits"):
            await message.channel.send("Old Habits die hard.")
            return
        elif user_message.startswith("!Thumbs"):
            pic = get_img("test_image.jpg")
            await message.channel.send(file=pic)
            return
        elif user_message.startswith("!Stop"):
            await message.channel.send("Shutting down Corazon.")
            await client.close()
    if user_message.startswith("fuckit"):
        await message.channel.send("FUCK IT ALLLL")
client.run(TOKEN)