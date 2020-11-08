# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os.path as path
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as t

FILE_NAME = "portfolio.txt"
Receipt = "receipt.txt"

def getCurrentPortfolio():
    file_exists = path.isfile(FILE_NAME)
    
    stocks = {}
    # We want stocks to look like this ----> {"GOOG": 2, "AAPL": 3, "FACEBOOK": 2}
    
    if file_exists == False:
        balance = 100000
    else:
        port_file = open(FILE_NAME, 'r')
        for line in port_file:
            line_array = line.split()
            if line_array[0] == "balance:":
                balance = float(line_array[1])
                
            if line_array[0] == "stocks:":
                for i in range(1, len(line_array)):
                    stock = line_array[i]
                    stock_data = stock.split(',')
                    ticker = stock_data[0]
                    num_shares = int(stock_data[1])
                    stocks[ticker] = num_shares
                
        port_file.close()
        
    
    
        
    
    return balance, stocks

def saveCurrentPortfolio(balance, stocks):
    port_file = open(FILE_NAME, 'w+')
    port_file.write("balance: "+ str(balance) + '\n')
    port_file.write("stocks: ")
    
    for key in stocks.keys():
        num_shares = stocks[key]
        port_file.write(key + "," + str(num_shares) + " ")
    
    port_file.close()

def createReceipt(ticker, num_shares, buyorsell):
    stock_wanted = yf.Ticker(ticker)
    current_price = stock_wanted.history(period="5d")["Close"][-1]
    port_file = open(Receipt, 'a')    
    receipt = ""
    if buyorsell == 1:
        receipt = str(num_shares) + " shares of " + ticker +  " at a price of $" + str(current_price) + " for a total purchase of $" + str(num_shares* current_price)
        port_file.write(receipt + '\n')
        port_file.close()
    else:
        receipt = str(num_shares) + " shares of " + ticker +  " at a price of $" + str(current_price) + " for a total sale of $" + str(num_shares* current_price)
        port_file.write(receipt + '\n')
        port_file.close()
        
    
    
def buyStock(ticker, num_shares):
    balance,stocks = getCurrentPortfolio()
    stock_wanted = yf.Ticker(ticker)
    current_price = stock_wanted.history(period="5d")["Close"][-1]
    buyorsell = 1
    
    
    total_cost = current_price * num_shares
    if total_cost > balance:
        print("Sorry, you do not have enough money! ")
        money_needed = total_cost - balance
        print("You need $" + str(money_needed) + "more")
        return balance, stocks
    
    balance -= total_cost
    if ticker in stocks:
        stocks[ticker] += num_shares
    else:
        stocks[ticker] = num_shares
    createReceipt(ticker, num_shares, buyorsell)
    
    return balance, stocks

def sellStock(ticker, num_shares):
    balance,stocks = getCurrentPortfolio()
    buyorsell = 2
    if ticker not in stocks:
        print("Sorry, you do not have this stock!") 
        return balance, stocks
        
    stock_wanted = yf.Ticker(ticker)
    current_price = stock_wanted.history(period="5d")["Close"][-1]
    total_sale = current_price * num_shares
    numsharesyouown = stocks[ticker]
    
    if num_shares > numsharesyouown:
        print("Sorry, you are trying to sell more than you own! ")
        print("You can only sell up to " + str(numsharesyouown))
        return balance, stocks
    
    balance += total_sale
    stocks[ticker] -= num_shares
    createReceipt(ticker, num_shares, buyorsell)
    return balance, stocks

def single_day_history(ticker):
    stock_wanted = yf.Ticker(ticker)
    current_price = stock_wanted.history(period="5d")["Close"][-1]
    print(ticker.upper() + "'s" + " current price is $" + str(current_price))
    x_values = []
    y_values = []
        
    Days = { 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday", 7:"Sunday" }
    date = t.date.today()
    day_number = int(date.isoweekday())
        
    for i in range(0, 5):
    
        if day_number == 7 or day_number == 6:
            day_number = 5
    
        if i == 0:
            day_number -= 0
        else:
            day_number -= 1
    
        if day_number == 0:
            day_number = 5
        
        previous_day = Days[day_number]
        x_values.append(previous_day)
    x_values.reverse()
        
    for i in range(0, 5):
        current_price = stock_wanted.history(period="5d")["Close"][i]
        y_values.append(current_price)
    plt.plot(x_values, y_values)
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.title("Last Five Days For " + ticker.upper())
    return plt.show()



def show_portfolio_graph():
    y_values = []
    y_values_total = []
    all_stocks = []
    num_shares_you_own = []
    day1 = 0
    day2 = 0
    day3 = 0
    day4 = 0
    day5 = 0
    for key in stocks.keys():
        all_stocks.append(key)
        num_shares_you_own.append(stocks[key])
    for j in range(0, len(all_stocks)):
        stock_wanted = yf.Ticker(all_stocks[j])
        for i in range(0, 5):
            current_price = stock_wanted.history(period="5d")["Close"][i]
            y_values.append(current_price * float(num_shares_you_own[j]))
        for i in range(0, 5):
            y_values_total.append(y_values[i])
           
        y_values = []
               
    counter = 0
    for i in range(0, len(y_values_total), 5):
        day1 += float(y_values_total[i])
        counter +=1
    for i in range(1, len(y_values_total), 5):
        day2 += float( y_values_total[i])
    for i in range(2, len(y_values_total), 5):
        day3 += float( y_values_total[i])
    for i in range(3, len(y_values_total), 5):
        day4 += float( y_values_total[i])
    for i in range(4, len(y_values_total), 5):
        day5 += float( y_values_total[i])

    print("The total value of your stocks is $" + str(day5))
        
    y_values = [day1, day2, day3, day4, day5]
       
    Days = { 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday", 7:"Sunday" }
    date = t.date.today()
    day_number = int(date.isoweekday())
    x_values = []
    for i in range(0, 5):
    
        if day_number == 7 or day_number == 6:
            day_number = 5
    
        if i == 0:
            day_number -= 0
        else:
            day_number -= 1
    
        if day_number == 0:
            day_number = 5
        
        previous_day = Days[day_number]
        x_values.append(previous_day)
    x_values.reverse()
        
    plt.plot(x_values, y_values)
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.title("Last Five Days For Portfolio" )
    return plt.show()


        
        


balance,stocks = getCurrentPortfolio()

while True:
    user_input = input("What would you like to do? (Buy/Sell/Show/Quit/Search/Receipt) ").lower()
    
    if user_input == "quit":
        saveCurrentPortfolio(balance, stocks)
        break
    elif user_input == "buy":
        ticker = input("Enter in what stock you want:")
        num_shares = int(input("Enter in how many shares:"))
        balance, stocks = buyStock(ticker, num_shares)
        saveCurrentPortfolio(balance, stocks)
    elif user_input == "sell":
        ticker = input("Enter in what stock you want to sell:")
        num_shares = int(input("Enter in how many shares: "))
        balance, stocks = sellStock(ticker, num_shares)
        saveCurrentPortfolio(balance, stocks)
    elif user_input == "show":
        print("Your current balance is $" + str(balance))
        print("Your current stocks: " + str(stocks))
        Total_Portfolio_Value = 0
        for key in stocks.keys():
            stock_wanted = yf.Ticker(key)
            current_price = stock_wanted.history(period="5d")["Close"][-1]
            Total_Portfolio_Value += stocks[key] * current_price
        Total_Portfolio_Value += balance
        print("Your total portfolio value is $" + str(Total_Portfolio_Value))
        show_portfolio_graph() 
    elif user_input == "search":
        ticker = input("Enter in what stock you want to search: ")
        single_day_history(ticker)
    #elif user_input == "receipt":
        #figure out how to print receipt
    else:
        print("Choose a valid insrtuction!")
        

