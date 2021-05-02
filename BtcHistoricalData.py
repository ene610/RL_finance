import pandas as pd
import numpy as np
import math
class MarketData():
    #per ora utilizzato BTC/USDT

    def __init__(self):
        # open_position = [quantity_base, quantity_quote, price]
        self.open_position = [-1, -1, -1]

        # TUTTE le candele
        self.market = self.init_upload()
        # Solo le candele interessanti per l'osservazione
        self.indicators = self.market[:20]
        # Se vendessi adesso avresti questa percentuale di guadagno
        #self.indicators['if_sell'] = -1

        #numero di contanti disponibili ma potrebbe tranquillamente esser la percentuale di monete in suo possesso
        self.balance = 10000
        self.profit_loss = 0
        self.index = 0

        self.countdown = 20
        self.already_sold = False

    def action(self, action):
        # action : 0 = hold , 1 = buy , 2 = sell tutto

        if action == 1:
            self.open_position[2] = self.indicators.iloc[19]['close']
            self.open_position[0] = self.balance / self.open_position[2]
            self.open_position[1] = self.balance

        if action == 2:
            self.balance = self.indicators.iloc[19]['close'] * self.open_position[0]
            self.already_sold = True

        self.index += 1
        self.countdown -= 1


    def observe(self):

        self.indicators = self.market.iloc[self.index : 20 + self.index]
        #TODO elimina colonne superflue
        flatten_indicators = self.indicators.to_numpy().flatten()
        obs = np.concatenate((flatten_indicators, self.open_position))
        # obs : [[1,2,34,5,6]*20] + [1,2,2]

        return obs


    def view(self):
        print("-" * 10)
        print(self.indicators)
        print(self.open_position)
        print("-" * 10)

    def is_done(self):
        #pensavo di procedere aspettando il tempo di chiusura di un azione e forzarlo o dare un parziale dopo tot step
        if self.already_sold or self.countdown == 0:
            if not self.already_sold:
                self.balance = self.indicators.iloc[19]['close'] * self.open_position[0]
            self.profit_loss += self.indicators.iloc[19]["close"] - self.open_position[2]
            return True
        return False

    def init_upload(self):
        # C:\Users\Ene\PycharmProjects\pythonProject\Binance_BTCUSDT_minute.csv
        path = "Binance_BTCUSDT_minute.csv"
        df = pd.read_csv(path, skiprows=1)
        df = df.iloc[::-1]
        #print(df.columns)
        #df = df.drop(columns=['unix', 'date', 'symbol', 'Volume BTC', 'low', 'tradecount', 'high', 'open'])
        # df['pct_5'] = df['close'].rolling(int(5))/df['close']
        #print(np.roll(df['close'], shift=-(int(5))) / df['close'])
        #df['R5'] = np.roll(df['close'], shift=(int(5))) / df['close']

        # diff_close_pct_5 = differenza percentuale tra il close alla candela attuale e quello della candela di 5 timestamps fa?
        df['diff_close_pct_5'] = ((df['close'] / np.roll(df['close'], shift=(int(5)))) * 100) - 100
        df['diff_close_pct_10'] = ((df['close'] / np.roll(df['close'], shift=(int(10)))) * 100) - 100

        df['diff_close_pct_15'] = ((df['close'] / np.roll(df['close'], shift=(int(15)))) * 100) - 100
        # Delete the first 15 rows
        df = df.iloc[15:]

        #print(df)

        return df

    def evaluete(self):
        #sharpe-ratio = (return of portfolio - risk-free rate ) / standard deviation of the portfolio’s excess return
        if self.open_position[2] == -1:
            return 0
        else:
            alfa = 0.8
            # prezzo a quanto ho comprato: self.open_position[2]
            # prezzo attuale: self.indicators[19]["close"]
            # prezzo precedente: self.indicators[18]["close"]

            reward_total = math.tanh(self.indicators.iloc[19]["close"] - self.open_position[2])
            reward_step = math.tanh(self.indicators.iloc[19]["close"] - self.indicators.iloc[18]["close"])

            # ibrido
            reward = alfa * reward_total + (1 - alfa) * reward_step
            return reward

    def reset(self):
        if self.index >= (self.market.shape[0] - 20):
            self.index = 0
        self.open_position = [-1, -1, -1]
        self.balance = 10000