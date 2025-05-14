import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

pacote_hosts = r"C:\Windows\System32\drivers\etc\hosts"
destino = "127.0.0.1"

def modificar_hosts(url, bloquear=True):
    if "www.www" in url or not url.strip():
        messagebox.showerror("Erro", "URL inválida. Por favor, tente novamente.")
        return

    dominio_principal = url[4:] if url.startswith("www.") else url
    urls = [dominio_principal, "www." + dominio_principal]

    try:
        with open(pacote_hosts, 'r') as arquivo:
            linhas = arquivo.readlines()

        if bloquear:
            for site in urls:
                if any(site == linha.split()[1].strip() for linha in linhas if linha.startswith(destino)):
                    messagebox.showerror("Erro", f"{site} já está bloqueado. Por favor, tente novamente!")
                    return
            with open(pacote_hosts, 'a') as arquivo:
                for site in urls:
                    arquivo.write(f"{destino} {site}\n")
            messagebox.showinfo("Sucesso", f"{' e '.join(urls)} foram bloqueados com sucesso!")
        else:
            desbloqueados = [site for site in urls if not any(site in linha for linha in linhas)]
            if desbloqueados:
                messagebox.showerror("Erro", f"{' e '.join(desbloqueados)} não estão bloqueados.")
                return

            novas_linhas = [linha for linha in linhas if not any(site in linha for site in urls)]

            with open(pacote_hosts, 'w') as arquivo:
                arquivo.writelines(novas_linhas)

            messagebox.showinfo("Sucesso", f"{' e '.join(urls)} foram desbloqueados com sucesso!")
    except Exception as erro:
        messagebox.showerror("Erro", f"Ocorreu um erro: {erro}")

def listar_bloqueados():
    try:
        with open(pacote_hosts, 'r') as arquivo:
            bloqueados = [linha.split()[1].strip() for linha in arquivo if linha.startswith(destino)]
            if bloqueados:
                messagebox.showinfo("Sites Bloqueados", "\n".join(bloqueados))
            else:
                messagebox.showinfo("Sites Bloqueados", "Nenhum site está bloqueado.")
    except Exception as erro:
        messagebox.showerror("Erro", f"Ocorreu um erro ao listar os sites bloqueados: {erro}")

class SolicitarURL(tk.Toplevel):
    def __init__(self, elemento_pai, title=None):
        super().__init__(elemento_pai)
        self.transient(elemento_pai)
        if title:
            self.title(title)
        self.grab_set()
        self.result = None

        self.geometry("400x200")
        self.label = ttk.Label(self, text="Digite a URL para bloquear/desbloquear:", font=("Plus-Jakarta-Sans", 14))
        self.label.pack(padx=20, pady=10)

        self.entrada_url = ttk.Entry(self, width=50) 
        self.entrada_url.pack(padx=20, pady=10, ipady=5)

        botoes_frame = ttk.Frame(self)
        botoes_frame.pack(pady=10)

        self.confirmar_botao = ttk.Button(botoes_frame, text="Confirmar", command=self.confirmar)
        self.confirmar_botao.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5) 

        self.cancelar_botao = ttk.Button(botoes_frame, text="Cancelar", command=self.cancelar)
        self.cancelar_botao.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

        self.protocol("WM_DELETE_WINDOW", self.cancelar)

    def confirmar(self):
        self.result = self.entrada_url.get().strip()
        self.destroy()

    def cancelar(self):
        self.result = None
        self.destroy()

def solicitar_url(elemento_pai):
    dialogo = SolicitarURL(elemento_pai, title="Bloquear/Desbloquear Site")
    elemento_pai.wait_window(dialogo)
    return dialogo.result 

def bloquear_site():
    url = solicitar_url(janela)
    if url:
        modificar_hosts(url, bloquear=True)

def desbloquear_site():
    url = solicitar_url(janela)
    if url:
        modificar_hosts(url, bloquear=False)

janela = tk.Tk()
janela.title("Gerenciador de Bloqueio de Sites")
janela.geometry("350x350")
janela.resizable(False, False)

try:
    imagem_rick = Image.open("rick.png")
    imagem_rick = imagem_rick.resize((360, 360), Image.Resampling.LANCZOS)
    bg_imagem = ImageTk.PhotoImage(imagem_rick)

    imagem_rick_label = tk.Label(janela, image=bg_imagem)
    imagem_rick_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Erro ao carregar imagem de fundo: {e}")

style = ttk.Style()
style.configure("TButton", font=("Plus-Jakarta-Sans", 12), padding=10)
style.configure("TLabel", font=("Plus-Jakarta-Sans", 16))

daneo_titulo = ttk.Label(janela, text="Bloqueador de Sites", font=("Plus-Jakarta-Sans", 18, "bold"))
daneo_titulo.pack(pady=20)

bloquear_url = ttk.Button(janela, text="Bloquear Site", command=bloquear_site)
bloquear_url.pack(pady=10, fill="x", padx=20)

desbloquear_url = ttk.Button(janela, text="Desbloquear Site", command=desbloquear_site)
desbloquear_url.pack(pady=10, fill="x", padx=20)

listar_botao = ttk.Button(janela, text="Listar Sites Bloqueados", command=listar_bloqueados)
listar_botao.pack(pady=10, fill="x", padx=20)

sair_botao = ttk.Button(janela, text="Sair", command=janela.quit)
sair_botao.pack(pady=15, fill="x", padx=15)

janela.mainloop()
