from Backtest import *
import pandas as pd


initial_fund = 10000
stock_number = 0


data = pd.read_csv(file_path)
num_line = data.shape[0]


class MACD():
    def __init__(self) -> None:
        self.signal = data['signal']
        self.fund = initial_fund

    def buy_action(self, buy_price):
        remaining_fund = self.fund % buy_price
        self.stock_number = self.fund // buy_price
        self.fund = remaining_fund
        return self.fund, self.stock_number

    def sell_action(self, sell_price):
        left_over = self.fund
        remaining_fund = self.stock_number * sell_price
        self.fund = remaining_fund + left_over
        return self.fund
        
    
    def MACD_backtest(self):
        n = 0
        for index, value in enumerate(self.signal):
            if value == 2.0:
                buy_price = data.at[index, '收盘价']
                self.buy_action(buy_price)
                # To keep track of the fund at each stage
                # print('Fund amount is: ' + str(fund_EMA), 'Number of stocks is: ' + str(stock_number))
            elif value == 1.0:
                sell_price = data.at[index, '收盘价']
                self.sell_action(sell_price)
                # To keep track of the fund at each stage
                # print('Fund amount is: ' + str(fund_EMA), 'Number of stocks is: ' + str(stock_number))

            else:
                pass
            n += 1
            if n > num_line:
                break
        final_fund_MACD = stock_number*data.at[num_line-1, '收盘价'] + self.fund
        print('MACD策略最终资金为: ' + str(final_fund_MACD))

        perc_gain_MACD = ((final_fund_MACD - initial_fund)/initial_fund)*100
        print('The percentage gain for the MACD method is: ' + str(perc_gain_MACD) + '%')


trial_MACD = MACD()
trial_MACD.MACD_backtest()

class control():
    def __init__(self) -> None:
        self.serial = data.iloc[:, 0]

    def control_backtest(self):
        for index, value in enumerate(self.serial):
            
            if value == 0:
                remaining_fund = initial_fund% data.at[index, '收盘价']
                stock_number = initial_fund//data.at[index, '收盘价']

                # To show the current status
                # print('Fund amount is: ' + str(remaining_fund), 'Number of stocks is: ' + str(stock_number))
            elif value == num_line -1:
                final_fund_alt = remaining_fund + stock_number*data.at[index, '收盘价']
                # To show the final amount
                
            else:
                pass
        print('对照组最终资金为: ' + str(final_fund_alt))
        perc_gain_control = ((final_fund_alt - initial_fund)/initial_fund)*100
        print("The percentage gain for the control setup is: " + str(perc_gain_control) +'%')

trial_control = control()
trial_control.control_backtest()
