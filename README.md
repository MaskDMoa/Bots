# 🤖 Meus Bots

Este repositório contém dois projetos distintos de Bots criados para automatizar tarefas em diferentes plataformas.

---

## 🃏 Discord – Bot de Inscrição para Torneios de Yu-Gi-Oh!

Um bot desenvolvido para facilitar o gerenciamento de inscrições de jogadores em torneios organizados através do Discord.

### ⚙️ Requisitos
- **Python** 3.x
- Bibliotecas do discord.py instaladas

### 🎯 Funcionalidades Principais
- 📝 Cadastro rápido de jogadores para o torneio

---

## 📱 Telegram – Bot de Controle do Computador via CMD

Um bot inovador que permite o controle remoto de uma máquina Windows diretamente pelo Telegram, como se você estivesse usando o terminal no próprio PC.

### ⚙️ Requisitos
- **Python** 3.x
- Computador executando **Windows**

### 🔧 Como Funciona
Quando o script do bot está sendo executado no PC alvo, ele escuta comandos enviados através do aplicativo do Telegram e os reproduz na máquina Windows usando o PowerShell. Além disso, qualquer texto comum enviado no chat será diretamente digitado no computador.

### 🎯 Comandos de Controle Remoto
| Comando | Descrição |
|---|---|
| `/cmd "comando"` | Executa um comando arbitrário no PowerShell local |
| `/clear` | Apaga todo o texto digitado anteriormente |
| `/notepad` | Abre o aplicativo Bloco de Notas |
| `[Texto comum]` | Digita o texto fornecido no computador |
