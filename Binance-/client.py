# Binance API
# https://python-binance.readthedocs.io/en/latest/overview.html#installation
#
#     SeveruS 01/17/2021

from binance.client import Client
from binance.websockets import BinanceSocketManager
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from Coin_Trader import *
from Hesaplama import *
from decimal import Decimal, ROUND_HALF_UP
from binance.enums import *
import time


global sembol
app=QApplication(sys.argv)
winMain=QMainWindow()
ui=Ui_CoinTrader()
ui.setupUi(winMain)
winMain.show()



def Starting():

    try:
        global conn_key
        global conn_key2
        global conn_key3
        global bm
        global client
        global usd_quantity
        usd_quantity=11
        global try_quantity
        try_quantity=100
        #ui.coin3_input.show("TRY")
        #coin1=ui.coin1_input.text()
        #coin2=ui.coin2_input.text()
        #coin3=ui.coin3_input.text()
        api_key = ''
        api_secret = ''
        client = Client(api_key, api_secret)

        bm = BinanceSocketManager(client, user_timeout=60)
        conn_key = bm.start_symbol_ticker_socket("BTCUSDT", process_message)
        conn_key2 = bm.start_symbol_ticker_socket("BTCTRY", process_message)
        conn_key3 = bm.start_symbol_ticker_socket("USDTTRY", process_message)
        bm.start()


    except:
        bm.stop_socket(conn_key, conn_key2, conn_key3)
        bm.close()
        print("[ERROR] Websocket connection error")
        time.sleep(2)
        print("[RETRY] Connection to websocket")
        Starting()


def process_message(msg):
    try:
        assignment(msg["s"], msg["b"], msg["a"], msg["c"])


    except:
         print("[ERROR] msg could not be sent")



def assignment(symbol2,buy_value,sell_value,price):
    global list1
    global list2
    global list3

    if symbol2=="BTCUSDT":
        list1=[symbol2,buy_value,sell_value,price]

    elif symbol2=="BTCTRY":
        list2 = [symbol2,buy_value, sell_value, price]

    else:
        list3 = [symbol2,buy_value, sell_value, price]


    if list1 != None and list2 != None and list3!= None :

        tl_deger=float(list3[1])
        btc_deger=float(list1[2])
        btc_usd_try=tl_deger*btc_deger

        btctry_deger=float(list2[1])
        fark=btc_usd_try-btctry_deger

        if fark>500 :
            while (True):
                print("==============AL===================")
                i=int(0)
                qua=round(float(usd_quantity / btc_deger),6)
                print(qua)
                order1 = client.create_order(
                    symbol='BTCUSDT',
                    side=SIDE_BUY,
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    newClientOrderId=2021,
                    quantity=qua,
                    price=list1[2]
                )
                print("BTC USDT alış emri oluşturuldu")
                print(list3[1])

                time.sleep(1)
                balance = client.get_asset_balance(asset='BTC')
                deger1=float(balance["free"])
                mevcut_btc = round(deger1-0.0000005,6)

                while(True):
                    if qua>=mevcut_btc:
                        print("if qua>=mevcut_btc")
                        time.sleep(1)
                        order2 = client.create_order(
                            symbol='BTCTRY',
                            side=SIDE_SELL,
                            type=ORDER_TYPE_LIMIT,
                            timeInForce=TIME_IN_FORCE_GTC,
                            quantity=list2[1],
                            price=satis_degeri)
                        time.sleep(3)
                        balance_try = client.get_asset_balance(asset='TRY')
                        deger2 = int(balance_try["free"])
                        print(deger2)

                        if deger2>=60:
                            print("if bala içi")
                            order3 = client.create_order(
                                symbol='USDTTRY',
                                side=SIDE_BUY,
                                type=ORDER_TYPE_LIMIT,
                                timeInForce=TIME_IN_FORCE_GTC,
                                quantity=11,
                                price=list3[1])

                            print("usd try sonu")
                            i=i+1
                            time.sleep(5)
                            break
                        else:
                            continue
                    else:
                        continue
                if i==1:
                    i=0
                    break
                else:
                    continue

        else:
            print(fark)

    elif fark<-350:
        print("dafa")
        while (True):
            print("==============AAAAALLLLLLL===================")
            i = int(0)
            qua = round(float(try_quantity / btc_deger), 6)
            print(qua)
            order1 = client.create_order(
                symbol='BTCTRY',
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                newClientOrderId=2021,
                quantity=qua,
                price=list1[2]
            )
            print("BTC USDT alış emri oluşturuldu")
            print(list3[1])

            time.sleep(1)
            balance = client.get_asset_balance(asset='BTC')
            deger1 = float(balance["free"])
            mevcut_btc = round(deger1 - 0.0000005, 6)

            while (True):
                if qua >= mevcut_btc:
                    time.sleep(1)
                    order2 = client.create_order(
                        symbol='BTCUSDT',
                        side=SIDE_SELL,
                        type=ORDER_TYPE_LIMIT,
                        timeInForce=TIME_IN_FORCE_GTC,
                        quantity=list2[1],
                        price=satis_degeri)
                    time.sleep(3)
                    balance_try = client.get_asset_balance(asset='USDT')
                    deger2 = int(balance_try["free"])
                    print(deger2)

                    if deger2 >= 60:
                        order3 = client.create_order(
                            symbol='USDTTRY',
                            side=SIDE_SELL,
                            type=ORDER_TYPE_LIMIT,
                            timeInForce=TIME_IN_FORCE_GTC,
                            quantity=11,
                            price=list3[1])

                        i = i + 1
                        time.sleep(5)
                        break
                    else:
                        continue
                else:
                    continue
            if i == 1:
                i = 0
                break
            else:
                continue

    else:
        print(fark)




def Stop_conn():
    answer=QMessageBox.question(winMain,"Exit","Çıkcan mı?",QMessageBox.Yes|QMessageBox.No)
    if answer==QMessageBox.Yes:
        print("Server cancelled")
        bm.stop_socket(conn_key, conn_key2, conn_key3)
        bm.close()
        sys.exit(app.exec_())
    else:
        winMain.show()



ui.pushButton.clicked.connect(Starting)
ui.pushButton_2.clicked.connect(Stop_conn)



sys.exit(app.exec_())





#ui.pushButton.clicked.connect(Start)


#ui.pushButton_2.c

#balance = client.get_asset_balance("USDT")
#print(balance["free"])


# order1=client.order_market_buy(
#     symbol='BTCUSDT',
#     quantity=qua)
# ---------------------------------------------------------
# ---------------------------------------------------------
# order2 = client.order_market_sell(
#     symbol='BTCTRY',
#     quantity=bala
# )
# ---------------------------------------------------------
# ---------------------------------------------------------
# time.sleep(1)

# order3 = client.order_market_buy(
#     symbol='USDTTRY',
#     quantity=10
# )
# time.sleep(5)
# ---------------------------------------------------------



