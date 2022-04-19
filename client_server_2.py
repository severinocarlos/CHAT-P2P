import socket
import time
import threading
import random
import datetime

class Client:
    """        
        - Criação de um web socket baseado em protocolo TCP -
        buildSocket: Criação/conexão com o servidor
        main: administra e cria as threads e bind uma porta para que o outro usuário
        que faz posse do endereço/porta possa se conectar
        seqNum: retorna um inteiro para sair formatado em sequência na mensagem
        send: Envia a mensagem lida
        receive: Recebe a mensagem enviado
    """
    def __init__(self):
        self.i = 0
        self.users = ['Thayna', 'Ana', 'Carol', 'Fernanda', 'Raissa', 'Bonna']
        self.HOST = 'localhost'
        self.PORT_SERVER = 55555
        self.PORT_CLIENT = random.randint(20001, 40000)
    
    def buildSocket(self):
        self.CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CLIENT.bind((self.HOST, self.PORT_CLIENT))
        self.CLIENT.connect((self.HOST, self.PORT_SERVER))
        
        return

    def main(self):
        
        #criação do socket para fazer a conexão com o servidor
        Client.buildSocket(self)
        USER = random.choice(self.users)
        
        print(f'Olá {USER}, aguardando confirmação...')
        # recebimento do endereço do outro usuário
        addr = self.CLIENT.recvfrom(1024)
        addrUser = int(addr[0].decode()) # só pra identificar que peguei o endereço de porta do outro User
        print(f'Endereço de porta do outro usuário: {addrUser}')
        
        # fechando a conexão com o servidor para deixar ele pronto para uma próxima conexão
        self.CLIENT.close()
        
        # criando um novo socket para fazer a conexão com o novo cliente (ele vai servir como servidor)
        CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CLIENT.bind((self.HOST, self.PORT_CLIENT))
        CLIENT.listen(1)
        CLIENT_FRIEND, _addr = CLIENT.accept()

        #criação das threads
        th1 = threading.Thread(target=Client.send, args= [self, CLIENT_FRIEND, USER])
        th2 = threading.Thread(target=Client.receive, args=[self, CLIENT_FRIEND])

        th1.start()
        th2.start()

    def seqNum(self):
        self.i += 1
        return self.i

    def send(self, CLIENT, user):

        while True:
            print('\n> Se você deseja encerrar a conexão digite [encerrar]')
            msg = input('')
            
            try:
                if msg == 'encerrar':
                    CLIENT.sendall(bytes(f'A conexão foi encerrado por {user}','utf-8'))
                    CLIENT.close()
                else:
                    CLIENT.sendall(bytes(f'{Client.seqNum(self)}. [{time.strftime("%X")} {datetime.date.today()}] <{user}> {msg}', 'utf-8'))
                    print('*** Mensagem enviada com sucesso! ***')
            except:
                CLIENT.close()
                exit()
    def receive(self, CLIENT):
        while True:
            try:
                msg = CLIENT.recv(1024).decode('utf-8')
                
                print(f'\n{msg}')
            except:
                print('Conexão encerrada...\nAperte [ENTER] para voltar ao console')
                CLIENT.close()
                exit()



test = Client()
test.main()
