import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException

# Load environment variables from .env file
load_dotenv()

# Discord bot token (replace 'YOUR_TOKEN_HERE' with your bot token)
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents(members=True, guilds=True)

# Discord bot command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# URL of the Selenium Grid server
SELENIUM_GRID_URL = "http://172.17.0.2:4444/wd/hub"  # Replace 'selenium_hub' with the hostname of your Selenium Grid container

options = webdriver.ChromeOptions()

# Function to capture and send the screenshot
async def capture_and_send():
    # Connect to the Selenium Grid server to use a remote ChromeDriver
    driver = webdriver.Remote(
    command_executor=SELENIUM_GRID_URL,
    options=options
    )
    
    try:
        # Load the webpage
        url = "https://edition.cnn.com/markets/fear-and-greed"
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        
        # Find the specific image element by XPath
        image_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section[4]/section[1]/section[1]')))

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
                    file = discord.File("screenshot.png")
                    await channel.send(file=file)
                else:
                    break
                    
    finally:
        # Quit the WebDriver
        driver.quit()

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
