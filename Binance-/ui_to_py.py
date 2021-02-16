from PyQt5 import uic

with open('Coin_Trader.py','w',encoding="utf-8") as fout:
    uic.compileUi('Coin_Trader.ui',fout)