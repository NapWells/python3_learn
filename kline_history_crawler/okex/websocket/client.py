from websocket import create_connection

if __name__ == '__main__':
    while True:
        try:
            ws = create_connection(url="wss://real.okcoin.com:10440/websocket/okcoinapi")
            print('connection successful')
            break
        except Exception:
            print('connect ws error,retry...')
            raise Exception
    i = 0