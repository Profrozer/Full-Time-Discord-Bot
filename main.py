import nextcord as discord
import asyncio
import time
import sys
import os
from colorama import Fore, init
from flask import Flask

init(autoreset=True)

app = Flask(__name__)

# Store your token securely using environment variables
TOKEN = os.environ.get("DISCORD_TOKEN")

client = discord.Client(self_bot=True)

start_time = time.time()
status_value = discord.Status.idle
custom_status = "Coding/Cracking 24/7"

def format_uptime():
    elapsed = int(time.time() - start_time)
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60
    return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"

def readable_status(status_obj):
    return str(status_obj).capitalize()

async def update_uptime():
    while True:
        uptime = format_uptime()
        line = f"{Fore.GREEN}Account has been active for: {uptime}{Fore.RESET}"
        sys.stdout.write('\r' + line.ljust(60))
        sys.stdout.flush()
        await asyncio.sleep(1)

async def enforce_presence():
    while True:
        await client.change_presence(
            status=status_value,
            activity=discord.CustomActivity(name=custom_status)
        )
        await asyncio.sleep(120)  # Re-enforce every 2 minutes

@client.event
async def on_ready():
    username = str(client.user)
    account_id = client.user.id

    await client.change_presence(
        status=status_value,
        activity=discord.CustomActivity(name=custom_status)
    )

    print(f"""{Fore.CYAN}┏━━━━━━━━━━━━━⍟
┃ Account: {username}
┃ Status: {readable_status(status_value)}
┃ Custom Status: {custom_status}
┃ Account ID: {account_id}
┗━━━━━━━━━━━━━⊛{Fore.RESET}""")

    # Print uptime line once
    print(f"{Fore.GREEN}Account has been active for: 00h 00m 00s{Fore.RESET}", end='')

    # Start tasks
    client.loop.create_task(update_uptime())
    client.loop.create_task(enforce_presence())

@app.route('/')
def home():
    return "Discord bot is running!"

def run_bot():
    client.run(TOKEN)

if __name__ == "__main__":
    # Start the Flask app in a separate thread
    thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000)))
    thread.daemon = True
    thread.start()

    # Run the Discord bot
    run_bot()
