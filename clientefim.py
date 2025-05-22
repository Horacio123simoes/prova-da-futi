import socket
import threading
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# Variáveis globais
cliente = None
nome_entry = None
foto_perfil = None
imagem_label = None

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
        mensagem_formatada = f'{nome_entry}: {mensagem}'
        try:
            cliente.send(mensagem_formatada.encode())
            exibir_mensagem(mensagem_formatada, recebido=False)  # Exibir mensagem enviada
            entarmensagem.delete(0, END)  # Limpar campo de entrada
        except:
            print('Erro no envio da mensagem')

def selecionar_foto():
    global foto_perfil, imagem_label
    caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
    if caminho:
        imagem = Image.open(caminho)
        imagem = imagem.resize((60, 60))
        foto_perfil = ImageTk.PhotoImage(imagem)
        imagem_label.config(image=foto_perfil)

def exibir_mensagem(mensagem, recebido=False):
    tela.config(state=NORMAL)
    # Escolher cor e alinhamento conforme tipo de mensagem
    if recebido:
        cor = 'blue'  # Cinzento claro
        alinhamento = 'right'
    else:
        cor = 'green'  # Azul claro
        alinhamento = 'left'
    
    # Inserir mensagem no Text com tag
    tela.insert(END, mensagem + '\n')
    tela.tag_add(alinhamento, "end-1l", "end-1c")
    tela.tag_config(alinhamento, justify=alinhamento, background=cor)
    
    tela.config(state=DISABLED)

def iniciar_conexao():
    global cliente,nome_entry
    nome_entry = nome.get()
    nome.delete(0, END)
    if not nome_entry.strip():
        return
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 5000))

    # Iniciar thread para receber mensagens
    th = threading.Thread(target=receber_mensagem, args=(cliente,))
    th.daemon = True
    th.start()

    # Remove widgets após entrar
    nome.place_forget()
    buttonentrar.place_forget()
    imagem_label.place(x=10, y=180)
    nome_l.config(text=nome_entry)

# Interface
windows = Tk()
cor4 = "#99cccc" #azul claro ou descarregado
cor5 = "White" #branco
cor1 = "#222222" #preto descarregado
windows.geometry("750x410")
windows.title("HORACIO chat")
windows.config(background=cor1)

frame1 = Frame(windows, width=500, height=50, background=cor4)
frame1.place(x=230, y=10)

labeltexto = Label(frame1, text="try chat", width=15, height=2, background=cor4, font=("Arial 15"), foreground=cor5)
labeltexto.place(x=5, y=2)

nome_l = Label(windows, width=15, background=cor1, text="Inserir o nome", foreground=cor5)
nome_l.place(x=115, y=180, anchor=CENTER)

linha1 = Label(windows, width=35, background=cor4)
linha1.place(x=0, y=256)

linha2 = Label(windows, width=35, background=cor4)
linha2.place(x=0, y=150)

nome = Entry(windows, width=35, background=cor5)
nome.place(x=10, y=200)

# Área clicável para escolher a imagem
imagem_label = Label(windows, width=60, height=60, bg=cor5)
imagem_label.place(x=100, y=20)
imagem_label.bind("<Button-1>", lambda e: selecionar_foto())

frame2 = Frame(windows, width=500, height=300, background=cor5)
frame2.place(x=230, y=70)

# Entrada de mensagens
entarmensagem = Entry(windows, width=68)
entarmensagem.place(x=230, y=378)
entarmensagem.bind(enviar_mensagem_evento)  # Enviar ao pressionar Enter

tela = Text(windows, state=DISABLED, width=62, height=18, bg=cor5)
tela.place(x=230, y=70)

buttonenviar = Button(windows,command=enviar_mensagem_evento,width=10, height=0, background=cor4, text="Enviar", foreground=cor5,)
buttonenviar.place(x=651, y=375)

buttonentrar = Button(windows, command=iniciar_conexao, width=6, height=0, background=cor4, text="Entrar", foreground=cor5)
buttonentrar.place(x=120, y=240, anchor=CENTER)

windows.mainloop()
