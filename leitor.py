import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3
import threading
import pyperclip
import time

# Estado global
engine_global = None
monitorando = False
ultimo_texto = ""
thread_monitor = None

IDIOMAS = {
    "Português (Brasil)": ["maria", "portuguese", "brazil", "pt-br"],
    "Inglês":             ["zira", "david", "english", "en-us"],
    "Espanhol":           ["spanish", "helena", "sabina", "es-"],
    "Francês":            ["french", "hortense", "fr-"],
    "Alemão":             ["german", "hedda", "de-"],
    "Italiano":           ["italian", "elsa", "it-"],
}

def obter_voz(engine, idioma_escolhido):
    voices = engine.getProperty('voices')
    palavras = IDIOMAS.get(idioma_escolhido, [])
    for voice in voices:
        nome = voice.name.lower()
        try:
            lang = voice.languages[0]
            if isinstance(lang, bytes):
                lang = lang.decode()
            lang = lang.lower()
        except:
            lang = ""
        for p in palavras:
            if p in nome or p in lang:
                return voice.id
    if voices:
        return voices[0].id
    return None

def falar_texto(texto):
    global engine_global
    if not texto:
        return

    if engine_global:
        try:
            engine_global.stop()
        except:
            pass

    botao_ouvir.config(state=tk.DISABLED, text="🔊 Lendo...")
    botao_parar.config(state=tk.NORMAL)

    def rodar():
        global engine_global
        try:
            engine_global = pyttsx3.init()
            engine_global.setProperty('rate', velocidade.get())
            engine_global.setProperty('volume', 1.0)
            voz = obter_voz(engine_global, idioma_var.get())
            if voz:
                engine_global.setProperty('voice', voz)
            engine_global.say(texto)
            engine_global.runAndWait()
        except Exception as e:
            print(f"Erro na leitura: {e}")
        finally:
            botao_ouvir.config(state=tk.NORMAL, text="🔊 Ouvir texto")
            botao_parar.config(state=tk.DISABLED)

    t = threading.Thread(target=rodar, daemon=True)
    t.start()

def falar():
    texto = caixa_texto.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Aviso", "Cole ou digite um texto antes de ouvir!")
        return
    falar_texto(texto)

def parar():
    global engine_global
    if engine_global:
        try:
            engine_global.stop()
        except:
            pass
    botao_ouvir.config(state=tk.NORMAL, text="🔊 Ouvir texto")
    botao_parar.config(state=tk.DISABLED)

def limpar():
    caixa_texto.delete("1.0", tk.END)

# ── Monitor de área de transferência ───────────────────────────────────────
def loop_monitor():
    global ultimo_texto, monitorando
    while monitorando:
        try:
            texto = pyperclip.paste().strip()
            if texto and texto != ultimo_texto:
                ultimo_texto = texto
                janela.after(0, lambda t=texto: falar_texto(t))
        except:
            pass
        time.sleep(0.8)

def toggle_monitor():
    global monitorando, thread_monitor, ultimo_texto
    if monitorando:
        monitorando = False
        botao_monitor.config(text="⚫ Ativar monitor de cópia", bg="#585b70")
        label_dica.config(text="Ative o monitor para ouvir textos copiados automaticamente")
    else:
        ultimo_texto = pyperclip.paste().strip()  # ignora o que já está copiado
        monitorando = True
        thread_monitor = threading.Thread(target=loop_monitor, daemon=True)
        thread_monitor.start()
        botao_monitor.config(text="🟢 Monitor ATIVO — copie qualquer texto (Ctrl+C)", bg="#a6e3a1")
        label_dica.config(text="Selecione um texto em qualquer site e pressione Ctrl+C para ouvir")

# ── Interface ───────────────────────────────────────────────────────────────
janela = tk.Tk()
janela.title("📢 Leitor de Texto em Voz Alta")
janela.geometry("620x580")
janela.configure(bg="#1e1e2e")
janela.resizable(False, False)

tk.Label(janela, text="📢 Leitor de Texto em Voz Alta",
         font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#cdd6f4").pack(pady=12)

tk.Label(janela, text="Cole ou digite o texto abaixo e clique em Ouvir:",
         font=("Segoe UI", 10), bg="#1e1e2e", fg="#a6adc8").pack()

caixa_texto = tk.Text(janela, height=10, width=65, font=("Segoe UI", 11),
                      bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4",
                      relief=tk.FLAT, padx=10, pady=10, wrap=tk.WORD)
caixa_texto.pack(pady=10, padx=20)

frame_config = tk.Frame(janela, bg="#1e1e2e")
frame_config.pack(pady=4)

tk.Label(frame_config, text="🌐 Idioma:", font=("Segoe UI", 10),
         bg="#1e1e2e", fg="#a6adc8").pack(side=tk.LEFT, padx=5)

idioma_var = tk.StringVar(value="Português (Brasil)")
menu_idioma = ttk.Combobox(frame_config, textvariable=idioma_var,
                            values=list(IDIOMAS.keys()), state="readonly", width=20)
menu_idioma.pack(side=tk.LEFT, padx=5)

tk.Label(frame_config, text="  🐢", font=("Segoe UI", 10),
         bg="#1e1e2e", fg="#a6adc8").pack(side=tk.LEFT)

velocidade = tk.Scale(frame_config, from_=100, to=250, orient=tk.HORIZONTAL,
                      length=160, bg="#1e1e2e", fg="#cdd6f4",
                      highlightthickness=0, troughcolor="#313244")
velocidade.set(150)
velocidade.pack(side=tk.LEFT)

tk.Label(frame_config, text="🐇", font=("Segoe UI", 10),
         bg="#1e1e2e", fg="#a6adc8").pack(side=tk.LEFT, padx=3)

frame_botoes = tk.Frame(janela, bg="#1e1e2e")
frame_botoes.pack(pady=10)

botao_ouvir = tk.Button(frame_botoes, text="🔊 Ouvir texto", command=falar,
                         font=("Segoe UI", 11, "bold"), bg="#89b4fa", fg="#1e1e2e",
                         relief=tk.FLAT, padx=18, pady=8, cursor="hand2")
botao_ouvir.pack(side=tk.LEFT, padx=6)

botao_parar = tk.Button(frame_botoes, text="⏹ Parar", command=parar,
                         font=("Segoe UI", 11), bg="#f38ba8", fg="#1e1e2e",
                         relief=tk.FLAT, padx=18, pady=8, cursor="hand2", state=tk.DISABLED)
botao_parar.pack(side=tk.LEFT, padx=6)

botao_limpar = tk.Button(frame_botoes, text="🗑 Limpar", command=limpar,
                          font=("Segoe UI", 11), bg="#a6e3a1", fg="#1e1e2e",
                          relief=tk.FLAT, padx=18, pady=8, cursor="hand2")
botao_limpar.pack(side=tk.LEFT, padx=6)

tk.Frame(janela, bg="#313244", height=2).pack(fill=tk.X, padx=20, pady=8)

botao_monitor = tk.Button(janela, text="⚫ Ativar monitor de cópia",
                           command=toggle_monitor,
                           font=("Segoe UI", 10, "bold"), bg="#585b70", fg="#cdd6f4",
                           relief=tk.FLAT, padx=16, pady=7, cursor="hand2")
botao_monitor.pack(pady=6)

label_dica = tk.Label(janela, text="Ative o monitor para ouvir textos copiados automaticamente",
                       font=("Segoe UI", 9), bg="#1e1e2e", fg="#6c7086")
label_dica.pack()

janela.mainloop()
