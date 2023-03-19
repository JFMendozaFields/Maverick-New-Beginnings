import discord
import requests
from graphqlclient import GraphQLClient
import ssl
import os

token = os.environ.get("TOKEN")
ssl._create_default_https_context = ssl._create_unverified_context

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

graphql_client = GraphQLClient('https://www.dnd5eapi.co/graphql')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('Salutations, young one!')

    if message.content.startswith('!charisma'):
        # Define the query (fixed missing quote)
        query = """
        {
            abilityScore(name: "Charisma") {
                name
                desc
            }
        }
        """
        # Executes the query and gets response
        result = graphql_client.execute(query)

        # Sends response as a message in Discord
        await message.channel.send(result)

    elif message.content.startswith('!beholder'):
        # Define the API endpoint and the query parameter
        endpoint = 'https://api.open5e.com/monsters/'
        params = {'name': 'Beholder'}

        # Make a GET request to the API
        response = requests.get(endpoint, params=params)

        # Check if response is successful (status code 200)
        if response.status_code == 200:
            # Send the response content as a message in Discord
            await message.channel.send(response.json())
        else:
            # Handle errors by sending a message in Discord
            await message.channel.send(f"Request failed with status code {response.status_code}")
            

client.run(token)
