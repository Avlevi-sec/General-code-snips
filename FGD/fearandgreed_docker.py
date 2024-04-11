import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException

# Load environment variables from .env file
load_dotenv()

# Set up the Chrome driver
chrome_driver_path = "/usr/local/bin/chromedriver"
service = Service(chrome_driver_path)
service.start()

# Set Chrome options to run headless (without opening browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument("--disable-gpu")
# Initialize the Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Discord bot token (replace 'YOUR_TOKEN_HERE' with your bot token)
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents(members=True, guilds=True)

# Discord bot command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to capture and send the screenshot
async def capture_and_send():
    # Load the webpage
    url = "https://edition.cnn.com/markets/fear-and-greed"
    driver.get(url)
    wait = WebDriverWait(driver, 4)
    driver.set_page_load_timeout(10)  # Set a 10-second timeout for page load
    # Find the specific image element by class name
    #image_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section[4]/section[1]/section[1]')))
    image_element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/section[4]/section[1]/section[1]')))
    # Get the size of the image element
    size = image_element.size

    # Resize the browser window to fit the entire image element
    driver.set_window_size(size['width'], size['height'])  

    # Get the screenshot of the image element
    screenshot = image_element.screenshot_as_png

    # Save the screenshot as a file
    with open("screenshot.png", "wb") as f:
        f.write(screenshot)

    # Send the screenshot as a file to the channel where the bot was added
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                print(f"adding to channel named: {channel.name}")
                file = discord.File("screenshot.png")
                await channel.send(file=file)
            else:
                print(f"didn't work on channel named: {channel.name}")
                break

# Background task to capture and send screenshot every 24 hours
@tasks.loop(hours=24)
async def send_screenshot():
    await capture_and_send()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    send_screenshot.start()

# Run the bot
bot.run(TOKEN)

