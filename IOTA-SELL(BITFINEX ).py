import bitfinexpy, time

# PARAMS USER #
KEY = ''
SECRET_KEY = ''
bitfinex = bitfinexpy.API(environment="live", key=KEY, secret_key=SECRET_KEY)
MARGEN_PRECIO = 0.0000005
cantidad = 100
PRECIO_OBJETIVO = 0.0000254
#PRECIO_INICIAL = PRECIO_OBJETIVO - MARGEN_PRECIO - 0.01*MARGEN DE PRECIO O ASÍ...
PRECIO_INICIAL = 0.000023
mercado = 'iotbtc'
peticiones = 0 
segundos = 0
segundos=int(time.strftime('%S'))
segundos=segundos+(int(time.strftime('%M'))*60)
segundos=segundos+(int(time.strftime('%H'))*3600)


#TICKER BID, ASK
def price_bid_ask(mercado):
    global peticiones
    global segundos
    peticiones=peticiones+1
    print('peticiones=')
    print(peticiones)
    print(time.strftime('%H:%M:%S'))
    #print(time.strftime('%H'))
    #time.sleep(60)
    segundos2=int(time.strftime('%S'))
    segundos2=segundos2+(int(time.strftime('%M'))*60)
    segundos2=segundos2+(int(time.strftime('%H'))*3600)
    #print(segundos2)
    #print(time.strftime('%H:%M:%S'))
    #print(type(time.strftime('%H:%M:%S')))
    if(((segundos2-segundos)<60 ) & (peticiones==7)):
        time.sleep(60)
        segundos=segundos2
        peticiones=0
    if(((segundos2-segundos)>60 ) & (peticiones>7)):
        segundos=segundos2
        peticiones=0
    res_ticker = bitfinex.ticker(symbol=mercado)
    bid = float(res_ticker['bid'])
    ask = float(res_ticker['ask'])
    return bid, ask

#ACTIVE ORDERS
def analisis_ordenes_abiertas():
    ordenes = []
    ordenes_a_cancelar = []
    active_orders = bitfinex.active_orders()
    for orden in active_orders:
        ordenes.append(orden)
        # print("id:", orden['id'], "\nmercado:", orden['symbol'], "\nprecio", orden['price'], "\ncompra/venta", orden['side'], "\nis_live:", orden['is_live'], "\nis_cancelled: ", orden['is_cancelled'], "\nremaining_amount", orden['remaining_amount'], "\nexecuted_amount", orden['executed_amount'])
    print("TOTAL ORDENES ABIERTAS: ", len(ordenes))
    return ordenes

#CREACION DE NUEVAS ORDENES:
def crear_orden_venta(mercado, cantidad, bid):
    print("NOS SALIMOS DE {} a precio {} cantidad {}".format(mercado, precio, cantidad))
    orden_mercado(mercado, cantidad, bid, 'sell',"exchange market")

#New ORDER
def orden_mercado(mercado, cantidad, precio, buy_sell, tipo_order):
    orden_creada = bitfinex.new_order(symbol=mercado, amount=cantidad, price=precio, side=buy_sell, order_type="exchange market") #cambiando order_type a market (antes exchange_limit")
    print(orden_creada)


#BALANCES
def wallets():
    print('####################### WALLETS #######################')
    wallets = bitfinex.wallet_balances()
    for crypto in wallets:
        print('CRYPTO {}:{} AVAILABLE {}'.format(crypto['currency'], crypto['amount'], crypto['available']))
    print('#######################################################')

def cancel_order(id):
    print("CANCELAMOS ORDER")
    bitfinex.cancel_order(id)
    wallets()

#SYMBOLS MARKETS
# print('LISTA DE MERCADOS EN BITFINEX', bitfinex.symbols())
bid, ask = price_bid_ask('iotbtc')
print("PRECIO_INICIAL FIJADO: ", PRECIO_INICIAL)
print("PRECIO_OBJETIVO FIJADO: ", PRECIO_OBJETIVO)
stop_loss = PRECIO_OBJETIVO
print("STOP LOSS: ", stop_loss)
wallets()
analisis_ordenes_abiertas()
#crear_orden_venta('iotusd', str(10), str(3))
wallets()
analisis_ordenes_abiertas()
operaciones_completada = False
while operaciones_completada == False:
    #ACTUALIZAR PRECIOS:
    bid_ant = bid
    ask_ant = ask
    bid, ask = price_bid_ask('iotbtc')
    if bid_ant != bid and bid >= PRECIO_INICIAL:
        print('BID: {}. ASK: {}.'.format(bid, ask))
        print('INCREMENTO %: ', 100*(bid/PRECIO_INICIAL-1))
        if bid > stop_loss + MARGEN_PRECIO: # CONDICION PARA ACTUALIZAR LA VARIABLE DE STOP_LOSS
            stop_loss = bid - MARGEN_PRECIO
            print('NUEVO STOP-LOSS: {}'.format(stop_loss))
            # print('EJERCUTAMOS ACTUALIZACION DE ORDENES!!!')
            # ordenes, contador_cancel = analisis_ordenes_abiertas(bid, stop_loss)
            # crear_ordenes('iotusd', stop_loss, bid, MARGEN_PRECIO, contador_cancel)

    #MIRAR SI TENEMOS QUE VENDER:
    if bid <= stop_loss and bid > PRECIO_OBJETIVO:
        crear_orden_venta('iotbtc', str(cantidad), str(precio))
        operaciones_completada = True
        wallets()
        time.sleep(1)
        
    time.sleep(5)
print('FINAL PROCESO')