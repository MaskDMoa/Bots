import telebot
import subprocess
import pyautogui
import time

BOT_TOKEN = "SEU_TOKEN_AQUI"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['clear'])
def apagar_texto(message):
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)
    pyautogui.press("delete")
    bot.reply_to(message, "Texto apagado.")


@bot.message_handler(commands=['notepad'])
def abrir_notepad(message):
    subprocess.Popen(["notepad.exe"])
    time.sleep(1)
    bot.reply_to(message, "Notepad aberto. Use /type para digitar.")

@bot.message_handler(func=lambda msg: not msg.text.startswith("/"))
def digitar(message):
    texto = message.text.replace("/type", "", 1).strip()

    if not texto:
        bot.reply_to(message, "Use: /type seu texto aqui")
        return

    pyautogui.write(texto, interval=0.03)
    bot.reply_to(message, "Texto digitado com sucesso.")
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

        bot.reply_to(message, f"{saida}")

    except Exception as e:
        bot.reply_to(message, f"Erro: {str(e)}")


bot.infinity_polling()
