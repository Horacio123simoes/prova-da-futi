import socket
import threading
from tkinter import *

# Variáveis globais
cliente = None
nome_usuario = None

# Função para receber mensagens do servidor
def receber_mensagem(cliente_socket):
    while True:
        try:
            mensagem = cliente_socket.recv(1024)
            if not mensagem:
                break
            else:
                exibir_mensagem(mensagem.decode(), recebido=True)  # Exibir mensagem recebida
        except:
            print('Erro ao receber mensagem')
            break

# Função para enviar mensagens ao servidor
def enviar_mensagem_evento(event=None):
    mensagem = entarmensagem.get()
    if mensagem.strip():
        mensagem_formatada = f'{nome_usuario}: {mensagem}'
        try:
            cliente.send(mensagem_formatada.encode())
            exibir_mensagem(mensagem_formatada, recebido=False)  # Exibir mensagem enviada
            entarmensagem.delete(0, END)  # Limpar campo de entrada
        except:
            print('Erro no envio da mensagem')

# Função para exibir mensagens na tela com formatação
def exibir_mensagem(mensagem, recebido=False):
    tela.config(state=NORMAL)
    
    # Escolher cor e alinhamento conforme tipo de mensagem
    if recebido:
        cor = '#d3d3d3'  # Cinzento claro
        alinhamento = 'right'
    else:
        cor = '#add8e6'  # Azul claro
        alinhamento = 'left'
    
    # Inserir mensagem no Text com tag
    tela.insert(END, mensagem + '\n')
    tela.tag_add(alinhamento, "end-1l", "end-1c")
    tela.tag_config(alinhamento, justify=alinhamento, background=cor)
    
    tela.config(state=DISABLED)

# Função para iniciar conexão com o servidor
def iniciar_conexao():
    global cliente, nome_usuario
    nome_usuario = nome.get().strip()
    if not nome_usuario:
        return
    
    try:
        # Criar socket e conectar
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(('127.0.0.1', 5000))
    except:
        print("Não foi possível conectar ao servidor.")
        return

    # Iniciar thread para receber mensagens
    th = threading.Thread(target=receber_mensagem, args=(cliente,))
    th.daemon = True
    th.start()

    # Remover entrada de nome e botão entrar
    nome.destroy()
    nome_l.destroy()
    buttonentrar.destroy()
    linha1.destroy()
    linha2.destroy()

# Interface gráfica (Tkinter)
windows = Tk()

# Cores
cor1 = "Yellow"
cor2 = "Red"
cor3 = "Blue"
cor4 = "#99cccc"
cor5 = "White"
corjanela = "#222222"

# Configuração da janela
windows.geometry("750x410")
windows.title("HORACIO chat")
windows.config(background=corjanela)

# Frame de título
frame1 = Frame(windows, width=500, height=50, background=cor4)
frame1.place(x=230, y=10)

labeltexto = Label(frame1, text="try chat", width=15, height=2, background=cor4,
                   font=("Arial 15"), foreground=cor5)
labeltexto.place(x=5, y=2)

# Label e entrada de nome
nome_l = Label(windows, width=15, background=corjanela, text="Inserir o nome", foreground=cor5)
nome_l.place(x=115, y=180, anchor=CENTER)

linha1 = Label(windows, width=35, background=cor4)
linha1.place(x=0, y=256)

linha2 = Label(windows, width=35, background=cor4)
linha2.place(x=0, y=150)

nome = Entry(windows, width=35, background=cor5)
nome.place(x=10, y=200)

# Frame de mensagens
frame2 = Frame(windows, width=500, height=300, background=cor5)
frame2.place(x=230, y=70)

# Entrada de mensagens
entarmensagem = Entry(windows, width=68)
entarmensagem.place(x=230, y=378)
entarmensagem.bind(enviar_mensagem_evento)  # Enviar ao pressionar Enter

# Caixa de texto para exibir mensagens
tela = Text(windows, state=DISABLED, width=62, height=18, bg='white')
tela.place(x=230, y=70)

# Botão para enviar mensagem
buttonenviar = Button(windows, width=10, height=0, background=cor4,text="Enviar", foreground=cor5, command=enviar_mensagem_evento)
buttonenviar.place(x=651, y=375)

# Botão para entrar no chat
buttonentrar = Button(windows, command=iniciar_conexao, width=6, height=0,background=cor4, text="Entrar", foreground=cor5)
buttonentrar.place(x=120, y=240, anchor=CENTER)

windows.mainloop()
