from Backtest_data_handling import *
import pandas as pd
import matplotlib.pyplot as plt
from mplcursors import cursor




initial_fund = 10000
stock_number = 0


data = pd.read_csv(file_path)
num_line = data.shape[0]


class MACD():
    def __init__(self) -> None:
        self.signal = data['signal']
        self.date = data['交易日期']
        self.fund = initial_fund
        self.stock_number = stock_number

    def buy_action(self, buy_price):
        remaining_fund = self.fund % buy_price
        self.stock_number = self.fund // buy_price
        self.fund = remaining_fund
        return self.fund, self.stock_number

    def sell_action(self, sell_price):
        left_over = self.fund
        remaining_fund = self.stock_number * sell_price
        self.fund = remaining_fund + left_over
        self.stock_number = 0
        return self.fund, self.stock_number
        
    def tracking(self):
        dates = self.date[:196]
        x_value = list(dates)
        plt.plot(x_value, self.track)
        plt.xlabel('Date')
        plt.ylabel('Fund remaining')
        plt.title('Returns of MACD strategy')
        cursor(hover = True)

        tick_positions = range(0, num_line-1, 50)
        plt.xticks(tick_positions)

        plt.show()


    def MACD_backtest(self):
        n = 0
        self.track = []
        for index, value in enumerate(self.signal):
            if value == 2.0:
                buy_price = data.at[index, '收盘价']
                self.track.append(self.fund)
                self.buy_action(buy_price)
                # To keep track of the fund at each stage
                # print('Fund amount is: ' + str(fund_EMA), 'Number of stocks is: ' + str(stock_number))
                
            elif value == 1.0:
                sell_price = data.at[index, '收盘价']
                self.sell_action(sell_price)
                # To keep track of the fund at each stage
                # print('Fund amount is: ' + str(fund_EMA), 'Number of stocks is: ' + str(stock_number))
                self.track.append(self.fund)
                

            else:
                current_price = data.at[index, '收盘价']
                asset = self.fund + self.stock_number*current_price
                self.track.append(asset)
                
                
            n += 1
            if n > num_line:
                break
        self.tracking()
        final_fund_MACD = stock_number*data.at[num_line-1, '收盘价'] + self.fund
        print('MACD策略最终资金为: ' + str(final_fund_MACD))

        perc_gain_MACD = ((final_fund_MACD - initial_fund)/initial_fund)*100
        print('The percentage gain for the MACD method is: ' + str(perc_gain_MACD) + '%')


class control():
    def __init__(self) -> None:
        self.serial = data.iloc[:, 0]
        self.date = data['交易日期']

    def tracking(self):
        dates = self.date[:196]
        x_value = list(dates)
        plt.plot(x_value, self.track)
        plt.xlabel('Date')
        plt.ylabel('Fund remaining')
        plt.title('Returns of Control strategy')
        cursor(hover = True)

        tick_positions = range(0, num_line-1, 50)
        plt.xticks(tick_positions)

        plt.show()

    def control_backtest(self):
        self.track = []
        for index, value in enumerate(self.serial):
            
            if value == 0:
                remaining_fund = initial_fund% data.at[index, '收盘价']
                stock_number = initial_fund//data.at[index, '收盘价']
                self.track.append(initial_fund)

                # To show the current status
                # print('Fund amount is: ' + str(remaining_fund), 'Number of stocks is: ' + str(stock_number))
            elif value == num_line -1:
                final_fund_control = remaining_fund + stock_number*data.at[index, '收盘价']
                # To show the final amount
                self.track.append(final_fund_control)
                
            else:
                current_price = data.at[index, '收盘价']
                asset = remaining_fund + stock_number*current_price
                self.track.append(asset)
            
        self.tracking()
            
                
        print('对照组最终资金为: ' + str(final_fund_control))
        perc_gain_control = ((final_fund_control - initial_fund)/initial_fund)*100
        print("The percentage gain for the control setup is: " + str(perc_gain_control) +'%')


trial_MACD = MACD()
trial_MACD.MACD_backtest()

trial_control = control()
trial_control.control_backtest()
