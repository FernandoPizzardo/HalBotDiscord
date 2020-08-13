import fnmatch
import os
import random

import discord
from discord import message, member
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import re

TOKEN = 'NzQyODg1ODY1NjE2ODM0Njcy.XzMoYA.7sXtZbYQZeLfazUxytX1598Mljo'

bot = commands.Bot(command_prefix='>')
client = discord.Client()

# Funções

def read_movie(*movie):
    expression = ''
    for word in movie:
        expression = expression + '/' + word
        print(expression)
    with open(f'wars/{expression}.txt', mode='r') as f:
        data = f.read()
    return data


def check_date(log_date):
    if int(log_date[0]) <= 0 or int(log_date[0]) > 12:
        return True
    elif int(log_date[1]) <= 0 or int(log_date[1]) > 31:
        return True
    elif int(log_date[0]) in [2, 4, 6, 9, 11] and int(log_date[1]) == 31:
        return True
    elif int(log_date[0]) == 2 and int(log_date[1]) == 30:
        return True
    else:
        return False


def check_end_month(log_date):
    if int(log_date[0]) in [1, 3, 7, 8, 10, 12]:
        if int(log_date[1]) == 31:
            return True
        else:
            return False
    elif int(log_date[0]) in [4, 6, 9, 11]:
        if int(log_date[1]) == 30:
            return True
        else:
            return False
    elif int(log_date[0]) == 2:
        if int(log_date[2]) % 4 and int(log_date[2]) != 1900:
            if log_date[1] == 29:
                return True
            else:
                return False
        else:
            if log_date[1] == 28:
                return True
            else:
                return False


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@bot.command(name='blade', help='Blade Runner é o filme favorito do meu criador, irônico não?')
async def blade_runner(ctx):
    blade_runner_quotes = [
        'Quite an experience to live in fear, isn t it? That s what it is to be a slave.',

        (
            'Replicants are like any other machine, are either a benefit or a hazard. If they are a benefit its not my '
            'problem.'
        ),
        'Its too bad she wont live, but then again who does?',
        (

            'Ive seen things you people wouldnt believe.Attack ships on fire off the shoulder of Orion. '
            'I watched c-beams glitter in the dark near the Tannhuser Gate.All those moments will be lost in time, '
            'like tears in rain. Time to die'
        ),

    ]
    response = random.choice(blade_runner_quotes)
    await ctx.send(response)




@bot.command(name='date', help="Pull's info from the date from wikipedia(MM/DD/YYYY)")
async def get_date(ctx, date):
    rex = re.compile("^[0-9]{2}[/][0-9]{2}[/][0-9]{4}$")
    if not rex.match(date):
        response = 'Wrong Format for the date, please enter MM/DD/YYYY'
    else:
        log = date.split('/')
        months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
                  '05': 'May', '06': 'June', '07': 'July', '08': 'August',
                  '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
        if check_date(log):
            response = 'Wrong date, be sure to use the MM/DD/YYYY format'
        else:
            log[1] = (str(int(log[1])))
            next_day = str(int(log[1]) + 1)
            url = f"https://en.wikipedia.org/wiki/{months[log[0]]}_{log[2]}"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, features='html.parser')
            if check_end_month(log):
                end_point = 'References'
            else:
                end_point = f"{months[log[0]]} {next_day}, {log[2]} ("
            info = soup.text[soup.text.rfind(f"{months[log[0]]} {log[1]}, {log[2]} (")
                             : soup.text.rfind(end_point)]
            response = re.sub("[\[].*?[\]]", "", info)
            if response == '':
                response = "Something odd happened, maybe wikipedia does't have info on that month or that day"
            elif len(response) > 2000:
                response = response[:1990] + '...'
    await ctx.send(response)


@bot.command(name='star', help='Crawl de star wars no Discord, mande list para saber mais')
async def star_wars(ctx, subject='', *especification):
    if subject == '':
        response = 'Qual filme?'
    elif subject == 'list':
        list_of_files = os.listdir('wars')
        pattern = '*.txt'
        list_of_movies= [entry.replace('.txt', '') for entry in list_of_files if fnmatch.fnmatch(entry, pattern)]
        response = 'Os filmes disponíveis são:\n\n'
        for movie in list_of_movies:
            response = response + movie + '\n'
    else:
        try:
            response = " A long time ago, in a galaxy far, far, away... \n" + read_movie(subject, *especification)
        except FileNotFoundError:
            response = 'I am sorry ' + {member.name} + ' im afraid i cant do that'

    await ctx.send(response)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


bot.run(TOKEN)
