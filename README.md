# BB and RSI freqtrade bot
This is the strategy, config, and hyperopt for a bot ive been working on the last couple of weeks. The indicators used ar Bolinger Bands and Relative Strength Index.
It has been built and optimized for Bittrex with USDT pairs. Please test before use, and ofcourse, this is for educational purposes only ;)

## How it chooses to buy and sell
The bot will buy when the close of the candle crosses the bottom Bollinger Band and when the RSI is less than a certain value, and will sell based on when the minimal ROI is reached. The minimal ROI has been determiend by hyperoptimizing the strategy on 365 days. 
![graph](https://user-images.githubusercontent.com/59344613/103338483-6c8e8880-4a33-11eb-900d-55d8008048b7.png)

# Some screenshots from backtesting
backtested on 2020-12-30

## One year
![365day](https://user-images.githubusercontent.com/59344613/103338288-bcb91b00-4a32-11eb-9200-a7cef10788b9.JPG)

## ~ Half a Year
![halfyear](https://user-images.githubusercontent.com/59344613/103338521-85973980-4a33-11eb-9436-27691f2c0233.JPG)

## One Month
![onemonth](https://user-images.githubusercontent.com/59344613/103338523-8760fd00-4a33-11eb-9e56-45cb5a3da9ff.JPG)


Please feel free to contact me with questions, and leave issues if found.
