import socket
import time


HOST = 'localhost'


first = True

while True:
    sendIP = False
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((HOST, 55555))
    SERVER.listen(2) # obs: vai ser conectados dois clients a esse server
    if first > 0:
        print('Esperando uma próxima conexão')
    
    CLIENT_1, address = SERVER.accept()
    CLIENT_2, address_2 = SERVER.accept()
    print('Conexão estabelecida!')
    print(f'1º Usuário: {address}')
    print(f'2º Usuário: {address_2}')
    first = False
    while not sendIP:
        print('lalala')
        CLIENT_1.sendto(bytes(f'{address_2[1]}', 'utf-8'), address_2)
        CLIENT_2.sendto(bytes(f'{address[1]}', 'utf-8'), address)
        print('Envio concluído')
        sendIP = True
        CLIENT_1.close()
        CLIENT_2.close()
    
    
