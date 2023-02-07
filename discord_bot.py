# Discord Interactions
from discord import app_commands, utils
import discord
# Read json file
from json import loads

# Setup absolutely minimalistic intents
intents = discord.Intents.none()

# Create custom DiscordPy Client
# To allow for immediate updates
class AClient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.none())
        self.synced = False
        self.added = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'Logged in as Name: {client.user.name} - ID:{client.user.id}')

# Load token
key = loads(open('creds.json').read())['token']

# Instantiate DiscordPy
client = AClient()
tree = app_commands.CommandTree(client)

##########
# Setting Embeds
##########

async def send_embed(interaction, address, state):
    embed = discord.Embed(title = "Your address is whitelisted! <a:luv:1015375946343260243>" if state else None, color = discord.Color.green() if state else discord.Color.red())
    embed.add_field(name = 'Your Address' if state else "Your address is not whitelisted! <a:shy:1015376121992335390>", value = f"{address[:4]}...{address[-4:]}" if state else "Please submit your wallet address and try again later.\n", inline = False)
    embed.set_footer(text = "bubblies Whitelist Checker", icon_url = "https://media.discordapp.net/attachments/995581487409799179/1010343809990795304/robot-head.png")
    await interaction.response.send_message(embed = embed, ephemeral = True)

async def not_eth_address(interaction):
    embed = discord.Embed(color = discord.Color.orange())
    embed.add_field(name = "That is not a valid Ethereum Address! <a:shy:1015376121992335390>", value = "Please check your address and try again.", inline = False)
    embed.set_footer(text = "bubblies Whitelist Checker", icon_url = "https://media.discordapp.net/attachments/995581487409799179/1010343809990795304/robot-head.png")
    await interaction.response.send_message(embed = embed, ephemeral = True)

##########

# The actual /check command
@app_commands.checks.cooldown(1, 5, key = lambda i: (i.user.id))
@tree.command(name = 'check', description = 'Check if address is whitelisted!')
async def self(interaction: discord.Interaction, address: str):
    if len(address) != 42 and address[0] != '0':
        await not_eth_address(interaction)
    with open('whitelist.txt', 'r') as file:
        addresses = file.read().lower().splitlines()
    if address.lower() in addresses:
        await send_embed(interaction, address, state = True)
    else:
        await send_embed(interaction, address, state = False)

# What to do if they're on cooldown
@tree.error
async def self(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"You are on cooldown for {round(error.retry_after, 2)} seconds! Please try again later", ephemeral = True)
    else: raise error

##########
# Main Running Loop
##########

if __name__ == '__main__':
    client.run(key)

##########