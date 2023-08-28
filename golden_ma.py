import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime, timedelta

def calculate_moving_averages(ticker_symbol):
    # Define the date range for checking the moving averages (last 2 days)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=2)

    # Download historical price data from Yahoo Finance
    stock = yf.Ticker(ticker_symbol)
    history = stock.history(period="1y")

    # Calculate moving averages
    history['MA_50'] = history['Close'].rolling(window=50).mean()
    history['MA_200'] = history['Close'].rolling(window=200).mean()

    # Get the latest moving average values
    ma_50 = history['MA_50'].iloc[-1]
    ma_200 = history['MA_200'].iloc[-1]

     # Check if the 50-day MA is greater than the 200-day MA in the previous row
    prev_ma_50 = history['MA_50'].iloc[-2]
    prev_ma_200 = history['MA_200'].iloc[-2]

    # Check if the 50-day MA is greater than the 200-day MA
    if ma_50 > ma_200 and prev_ma_50 <= prev_ma_200:
        send_email(ticker_symbol, ma_50, ma_200)

def send_email(ticker_symbol, ma_50, ma_200):
    # Email configuration
    sender_email = 'avipy123@gmail.com'
    receiver_email = 'avihay19999@gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'avipy123@gmail.com'
    smtp_password = 'utojxwxtefdltzes'

    # Compose email message
    subject = f'Golden Cross Alert: {ticker_symbol}'
    body = f'The 50-day moving average ({ma_50:.2f}) is greater than the 200-day moving average ({ma_200:.2f}) for {ticker_symbol}.'
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Define the list of stocks to monitor
stocks = ['QCOM','NIO','QSI']  # Add or remove stocks as needed

# Run the script continuously
for stock in stocks:
        calculate_moving_averages(stock)

    # Wait for 24 hours before checking again
    #time.sleep(24 * 60 * 60)
