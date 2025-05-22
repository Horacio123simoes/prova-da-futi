import socket
import threading

clientes=[]

def brodcast(mensagem,cliente_actual):
    for cliente in clientes:
        if cliente != cliente_actual:
            try:
                cliente.send(mensagem)
            except:
                cliente.close()
                if cliente in clientes:
                    cliente.remove(cliente)

def conectar_cliente(conexao, endereco):
    print(f'[nova conexão]: cliente{endereco}')
    clientes.append(conexao)
    while True:
        try:
            mensagem= conexao.recv(1024)
            if not mensagem:
                break
            else:
                #print(f'{endereco}: {mensagem.decode()}')
                brodcast(mensagem,conexao)
        except:
            break
    print(f'[desconectado] cliente: {endereco}')
    clientes.remove(conexao)
    conexao.close()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('0.0.0.0', 5000))
servidor.listen(2)
print(f'servidor aguardando conexão...')

while True:
    conexao, endereco = servidor.accept()
    th = threading.Thread(target=conectar_cliente, args=(conexao, endereco))
    th.start()




    
