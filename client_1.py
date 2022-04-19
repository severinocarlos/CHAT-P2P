import socket
import time
import threading
import random
import datetime

class Client:
    """        
        - Criação de um web socket baseado em protocolo TCP -
        buildSocket: Criação/conexão com o usuário/servidor
        main: administra e cria as threads
        seqNum: retorna um inteiro para sair formatado em sequência na mensagem
        send: Envia a mensagem lida
        receive: Recebe a mensagem enviado
    """
    def __init__(self):
        
        self.i = 0
        self.users = ['Severino', 'Lucas', 'Joao', 'Victor', 'Neto', 'Alejandro']
        self.HOST = 'localhost'
        self.PORT_SERVER = 55555

    def buildSocket(self, port):
        self.CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CLIENT.connect((self.HOST, port))
 
        return
    
    def main(self):

        Client.buildSocket(self, 55555) # criando o socket e conectando com o servidor
        self.USER = random.choice(self.users)
        
        print(f'Olá {self.USER}, aguardando confirmação...')
        addr = self.CLIENT.recvfrom(1024) # recebimento do endereço do outro user
        
        # obtendo o endereço IP e a porta do outro user
        addrUser = int(addr[0].decode())
        print(f'Endereço de porta do outro usuário: {addrUser}')

        # fechadno a conexão com o servidor para deixar ele pronto para uma próxima conexão
        self.CLIENT.close()
        #criando outro socket para fazer a conexão com o outro user
        Client.buildSocket(self, addrUser)

        #inicialização das threads
        th1 = threading.Thread(target=Client.send, args= [self])
        th2 = threading.Thread(target=Client.receive, args=[self])

        th1.start()
        th2.start()

    def seqNum(self):
        self.i += 1
        return self.i

    def send(self):
        while True:
            print('\n> Se você deseja encerrar a conexão digite [encerrar]')
            msg = input('')

            try:
                if msg == 'encerrar':
                    self.CLIENT.sendall(bytes(f'A conexão foi encerrado por {self.USER}','utf-8'))
                    self.CLIENT.close()
                else:
                    self.CLIENT.sendall(bytes(f'{Client.seqNum(self)}. [{time.strftime("%X")} {datetime.date.today()}]  <{self.USER}> {msg}', 'utf-8'))
                    print('*** Mensagem enviada com sucesso! ***')
            except:
                self.CLIENT.close()
                exit()
    def receive(self):
        while True:
            try:
                msg = self.CLIENT.recv(1024).decode('utf-8')
                print(f'\n{msg}')
            except:
                print('Conexão encerrada...\nAperte [ENTER] para voltar ao console')

                self.CLIENT.close()
                exit()

test = Client()
test.main()

