#!/bin/bash

# run this bot continuously. 

echo "Starting Reddit Bot in continuous mode..."

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

while true; do
    echo "Starting bot at $(date)"
    python3 bot.py
    
    echo "Bot stopped at $(date). Restarting in 30 seconds..."
    sleep 30
done 