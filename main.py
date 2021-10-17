import os
import discord
import requests
import json
import wikipedia
import random
from replit import db
from keep_alive import keep_alive
import pyjokes
import praw

reddit = praw.Reddit(
  client_id=os.environ['CLIENT_ID'],
  client_secret=os.environ['REDDIT_SECRET'],
  username="DebadritoSop",
  password=os.environ['REDDIT_PASSWORD'],
  user_agent="pythonpraw"
)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return quote

def get_joke():
  joke = pyjokes.get_joke()
  return joke

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements

  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def search_wikipedia(query):
  q = query.replace("#wikipedia", "").replace(" ", "")
  result = wikipedia.summary(q, 3)
  return result

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]
starter_encouragements = ["Cheer Up! :smile:", 
"Hang In There!", 
"You are a great person! :thumbsup:",
"Dont be sad or Depressed!"]

client = discord.Client()
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content
  
  if message.content.startswith('#hello'):
    await message.channel.send("Hello! :wave:")
  
  if message.content.startswith('#inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if message.content.startswith('#wikipedia'):
    await message.channel.send("Searching Wikipedia.... :innocent: ")
    result = search_wikipedia(message.content)
    await message.channel.send(result)

  # options = starter_encouragements
  if "encouragements" in db.keys():
    options = list(starter_encouragements) + list(db["encouragements"])
  if any(word in msg for word in sad_words):
    m = f"{random.choice(options)}"
    await message.channel.send(m)
  
  if msg.startswith("#new"):
    encouraging_message = msg.split("#new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added! :thumbsup:")
  
  if msg.startswith("#list"):
    await message.channel.send(options)
  
  if msg.startswith("#thanks"):
    await message.channel.send("Thats My Pleasure! :thumbsup:")

  if msg.startswith("#joke"):
    await message.channel.send(f"{get_joke()} :rofl:")
  if msg.startswith("#bye"):
    await message.channel.send("Bye!")
  
  if msg.startswith("#meme"):
    await message.channel.send("Wait.. Finding a meme...")
    subreddit = reddit.subreddit("memes")
    top = subreddit.top(limit=100)
    all_subs = []
    for submission in top:
      all_subs.append(submission)
    
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title=name)
    em.set_image(url=url)
    await message.channel.send(embed=em)
  

key = os.environ['KEY']

keep_alive()
client.run(key)
