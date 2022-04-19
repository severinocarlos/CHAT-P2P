import socket

HOST = 'localhost'

first = True

while True:
    sendIP = False
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((HOST, 55555))
    SERVER.listen(2) # obs: vai ser conectados dois clients a esse server
    
    if not first:
        print('Esperando uma próxima conexão')
    #aceitando a conexão dos dois clients
    CLIENT_1, address = SERVER.accept()
    CLIENT_2, address_2 = SERVER.accept()

    print('-'*32)
    print('Conexão estabelecida!')
    print(f'\n1º Usuário com endereço IP: {address[0]} e porta {address[1]}')
    print(f'2º Usuário com endereço IP: {address_2[0]} e porta {address_2[1]}')
    first = False
    
    while not sendIP:
        '''
            Só irá rodar até trocar as informações de endereços/porta dos dois usuários
            e posteriomente vai fechar e conexão com esses clients ficando já pronto para uma próxima conexão!
        '''
        CLIENT_1.sendto(bytes(f'{address_2[1]}', 'utf-8'), address_2)
        CLIENT_2.sendto(bytes(f'{address[1]}', 'utf-8'), address)
        print('Envio concluído\n')
        print('-'*32)
        sendIP = True
        CLIENT_1.close()
        CLIENT_2.close()
    
    
