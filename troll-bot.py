name: Build and Test

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install cryptography keyboard
    
    - name: Run bot (автоматическая активация)
      run: |
        python troll-bot.py
      env:
        ACTIVATION_KEY: "awesminute"
