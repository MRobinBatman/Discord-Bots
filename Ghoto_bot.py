# -*- coding: utf-8 -*-
"""
The idea here is to create a Discord chatbot that you can play little mini-games with. Since I am an anime fan, I themed it after the popular bulter character (inspired by the popular software Jenkins to do so). I have worked on a few mini-games for this and have a few morre in the works.
"""
import numpy as np
import discord
from discord import Colour
import nest_asyncio
import os
import random
import pandas as pd
from  sklearn.linear_model import LinearRegression
import configparser


#Credentials
config = configparser.ConfigParser()
config.read('Ghoto_config.ini')
TOKEN = config['Discord']['token']
my_channel = config['Discord']['channel']

my_channel = int(my_channel)



intents = discord.Intents.default()
intents.message_content = True

nest_asyncio.apply()

client = discord.Client(intents = intents)

#Ghoto Commands
commands = ["!Commands","!Stop","!Height 'your_height_here'","!Ding","!Flip 'number of coins here'"] #, "!Regress "]

person_with_coin = None

#Helper Methods
def get_char(height):    
    df = pd.read_csv("anime_heights.csv")
    
    # print(df.head)
    exact_matches = df.loc[df["Heights(cm)"] == height]
    # print(exact_matches)
    
    if(exact_matches.empty == False):
        if (len(exact_matches)>1):
            print("Multiple Matches, Randomly Assinging One.")
            ans =exact_matches.sample(n=1)
            # lst = [ans["Names"],ans["Heights(cm)"],ans["Image_Url"]]
            print("More than one possibility")
            print(ans[0])
            return ans
        else:
            print("Only one possible answer")
            
            # ans = exact_matches[0]
            print(exact_matches)
            return exact_matches
    
    # closest = df.iloc[(df["Heights(cm)"]-height).abs().argsort()[0],:]
    close = df.iloc[(df["Heights(cm)"] - float(height)).abs().argsort()[0],:]
    print(close)
    print("Estimating Closest.")
    return(close)

def convert_ft_to_cm(input_var):
    cm = input_var
    inches = cm*0.394
    return inches
    
    

def list_commands(commands):
    command_text = ""
    # print("List of Commands:")
    for each in commands:
        temp = each
        temp2 = "\n"
        # print(f"Command: {temp}")
        if commands.index(each) == 0:
            command_text = command_text + temp
        else:
            command_text = command_text + temp2 + temp
    # print(command_text)
    return(command_text)

def get_img(text):
    with open(text, 'rb') as f:
        picture = discord.File(f)
    return

def check_if_reply(mess):
    if mess.reference is not None and not mess.is_system :
         return True
    return False


# def get_all_chans():
    # channel_list = client.get_chann
    # return channel_list


#Discord Events
@client.event
async def on_ready():
    print("\nwe have liftoff.".format(client))
    channel = client.get_channel(my_channel)
    print(f"\nChannel : {channel}")
    await channel.send("Ghoto Connected \U0001F601")
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # if message.content[0] != "!":
    #     return
    username = str(message.author).split('#',0)
    user_message = str(message.content)
    # print(user_message)
    channel = str(message.channel)
    if message.channel.name == "general":
        print(f"Responding to {username} on the {channel} channel.\nMessage: {user_message}")
        
        commds = list_commands(commands)
        if user_message.startswith("!Commands"):
            embed = discord.Embed(
                title = "Commands List:",
                description = commds,
                color = Colour.dark_magenta())
            await message.channel.send(embed=embed)
            # commds = list_commands(commands)
            # await message.channel.send(commds)
            return
        elif user_message.startswith("!Stop"):
            await message.channel.send("Shutting down Ghoto.")
            await client.close()
        elif user_message.startswith("!Height"):
            h = user_message.rsplit(" ")[1]
            char = get_char(h)
            # help(char)
            char_n = char[0]
            char_h= char[1]
            char_im = char[2]
            # await message.channel.send(f"Finding character closest to {h}")
            # await message.channel.send(f"\nHeight: {char_h}")
           
            embed = discord.Embed(
                title = f"The Character closest to your height is: {char_n}",
                description = f"Height : {char_h}",
                color= Colour.blurple()
                )
            embed.set_thumbnail(url= str(char_im))
            # await message.channel.send(f"The Character closest to your height is: \n\n{char_n}\n{char_im}")
            await message.channel.send(embed=embed)
            return
        elif user_message.startswith("!Ding"):
            print("Dong")
        elif user_message.startswith("!Flip"):
            flip_list = []
            flips = user_message.split(" ")
            num_coins = flips[1]
            # print(num_coins)
            await message.channel.send(f"Okay I will flip {num_coins} \U0001FA99.")
            for i in range(0,int(num_coins)):
                coin = random.randint(0, 1)
                if coin == 0:
                    flip_list.append("Heads")
                    # await message.channel.send("Heads")
                else:
                    # await message.channel.send("Tails")
                    flip_list.append("Tails")
            embed = discord.Embed(
                title = "Coin Flips:",
                description = flip_list,
                color = Colour.yellow())
            await message.channel.send(embed = embed)
            return
        elif user_message.startswith("!Regress"):
            user_message = user_message.split(" ")[1:]
            user_message = list(user_message)
            print(user_message[1])
            x = user_message[0]
            y = user_message[1]
            x = np.array(x).reshape(-1,1)
            print(x)
            y = np.array(y)
            model = LinearRegression().fit(x,y)
            score = model.score(x,y)
            print(f"R_sq : {score}")
            
            
                

        if check_if_reply(message) == True:
            print("Is a reply")
            if user_message.startswith("!Guess"):
                print("Guessing")
                guess = user_message.split(" ")[1]
                if(guess == "left"):
                    print("left")

client.run(TOKEN)
