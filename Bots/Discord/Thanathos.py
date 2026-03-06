import discord
from discord.ext import commands
import asyncio
import random
import json
import os

# ================= Configurações Iniciais =================
DADOS_FILE = 'dados_jogo.json'

dados = {
    "canais_permitidos": [],
    "cargos_permitidos": [],
    "personagens": []
}

def carregar_dados():
    global dados
    if os.path.exists(DADOS_FILE):
        with open(DADOS_FILE, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    else:
        salvar_dados()

def salvar_dados():
    with open(DADOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

carregar_dados() # Carrega os dados salvos quando o bot ligar

# Lendo o token de um txt
try:
    with open("token.txt", "r", encoding="utf-8") as f:
        TOKEN = f.read().strip()
except FileNotFoundError:
    print("❌ Arquivo token.txt não encontrado! Crie o arquivo e cole o token do bot dentro dele.")
    exit()

# ================= Configuração do Bot =================
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

jogos_ativos = {}

class JogoEmoji:
    def __init__(self, bot, canal, personagem):
        self.bot = bot
        self.canal = canal
        self.personagem = personagem
        self.indice_dica = 1 
        self.tempo_espera = 20 
        self.task_dica = bot.loop.create_task(self.loop_dicas())
        
    async def enviar_dica(self):
        emojis_atuais = "".join(self.personagem["emojis"][:self.indice_dica])
        embed = discord.Embed(
            title="🤔 Quem é o personagem?",
            description=f"Dica {self.indice_dica}/{len(self.personagem['emojis'])}:\n\n# {emojis_atuais}",
            color=discord.Color.yellow()
        )
        embed.set_footer(text="Digite o nome no chat para adivinhar! | Use !dica para pular o tempo.")
        await self.canal.send(embed=embed)

    async def loop_dicas(self):
        try:
            await self.enviar_dica()
            while self.indice_dica < len(self.personagem["emojis"]):
                await asyncio.sleep(self.tempo_espera)
                self.indice_dica += 1
                await self.enviar_dica()
            
            await asyncio.sleep(self.tempo_espera)
            await self.canal.send(f"⏰ **Tempo esgotado!** Ninguém acertou.\nO personagem era: **{self.personagem['nome']}**.")
            encerrar_jogo(self.canal.id)
            
        except asyncio.CancelledError:
            pass

def encerrar_jogo(canal_id):
    if canal_id in jogos_ativos:
        jogo = jogos_ativos[canal_id]
        if not jogo.task_dica.done():
            jogo.task_dica.cancel()
        del jogos_ativos[canal_id]

# ====== Verificações ======
def e_canal_permitido(ctx):
    if not dados["canais_permitidos"]:
        return True
    return ctx.channel.id in dados["canais_permitidos"]

def tem_permissao_gerencia(ctx):
    # O dono do servidor ou administrador sempre pode
    if ctx.author.guild_permissions.administrator:
        return True
    
    # Se o usuario tiver um dos cargos permitidos
    cargos_usuario = [role.id for role in ctx.author.roles]
    for cargo_id in dados["cargos_permitidos"]:
        if cargo_id in cargos_usuario:
            return True
            
    return False

# ================= Comandos de Gerenciamento =================

@bot.command()
async def addcanal(ctx, canal_id: int):
    """(Admin) Autoriza um canal a ter o bot funcinando"""
    if not tem_permissao_gerencia(ctx):
        await ctx.send("❌ Você não tem permissão para usar este comando.")
        return
        
    if canal_id not in dados["canais_permitidos"]:
        dados["canais_permitidos"].append(canal_id)
        salvar_dados()
        await ctx.send(f"✅ Canal <#{canal_id}> adicionado aos canais permitidos.")
    else:
        await ctx.send("⚠️ Este canal já está na lista.")

@bot.command()
async def addcargo(ctx, cargo: discord.Role):
    """(Admin) Autoriza um cargo a adicionar personagens e canais"""
    # Apenas gerentes natos do servidor podem adicionar novos cargos de gerência
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Apenas **administradores do servidor** podem adicionar cargos de gerência.")
        return
        
    if cargo.id not in dados["cargos_permitidos"]:
        dados["cargos_permitidos"].append(cargo.id)
        salvar_dados()
        await ctx.send(f"✅ Cargo **{cargo.name}** adicionado! Quem tiver ele poderá adicionar personagens e canais.")
    else:
        await ctx.send("⚠️ Este cargo já tem permissão.")

@bot.command()
async def addpersonagem(ctx, nome: str, emojis: str, respostas: str):
    """
    (Admin) Adiciona um novo personagem.
    Uso: !addpersonagem "Nome" "🦇, 👨, 🌃" "batman, bruce wayne"
    """
    if not tem_permissao_gerencia(ctx):
        await ctx.send("❌ Você não tem permissão para usar este comando.")
        return
        
    lista_emojis = [e.strip() for e in emojis.split(',')]
    lista_respostas = [r.strip().lower() for r in respostas.split(',')]
    
    novo_pers = {
        "nome": nome,
        "emojis": lista_emojis,
        "respostas_aceitas": lista_respostas
    }
    
    dados["personagens"].append(novo_pers)
    salvar_dados()
    await ctx.send(f"✅ O personagem **{nome}** foi salvo com sucesso! ({len(lista_emojis)} emojis cadastrados e {len(lista_respostas)} respostas aceitas)")

# ================= Comandos do Jogo =================

@bot.event
async def on_ready():
    print(f'🤖 Bot logado e pronto como {bot.user}')
    print(f'✅ Carregados {len(dados["personagens"])} personagens!')

@bot.command()
async def iniciar(ctx):
    if not e_canal_permitido(ctx):
        await ctx.send("❌ Este comando não está permitido neste canal.")
        return

    if ctx.channel.id in jogos_ativos:
        await ctx.send("❌ Já existe um jogo rolando neste canal! Adivinhe ou espere acabar.")
        return

    if not dados["personagens"]:
        await ctx.send("❌ Nenhum personagem cadastrado! Use o comando `!addpersonagem` primeiro.")
        return

    personagem_sorteado = random.choice(dados["personagens"])
    jogo = JogoEmoji(bot, ctx.channel, personagem_sorteado)
    jogos_ativos[ctx.channel.id] = jogo

@bot.command()
async def dica(ctx):
    if not e_canal_permitido(ctx):
        return

    if ctx.channel.id not in jogos_ativos:
        await ctx.send("❌ Não há nenhum jogo rolando. Digite `!iniciar` para começar.")
        return

    jogo = jogos_ativos[ctx.channel.id]
    
    if jogo.indice_dica >= len(jogo.personagem["emojis"]):
        await ctx.send("⚠️ Todas as dicas já foram dadas! Tentem adivinhar no chat.")
        return

    jogo.task_dica.cancel()
    jogo.indice_dica += 1
    jogo.task_dica = bot.loop.create_task(jogo.loop_dicas())

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Processa comandos primeiro (!iniciar, !dica, !addpersonagem)
    await bot.process_commands(message)

    # Depois checa se a mensagem é um chute em um jogo ativo
    if message.channel.id in jogos_ativos:
        if e_canal_permitido(message): 
            jogo = jogos_ativos[message.channel.id]
            chute_do_usuario = message.content.lower().strip()
            
            for resposta in jogo.personagem["respostas_aceitas"]:
                if resposta == chute_do_usuario:
                    await message.reply(f"🎉 **Parabéns!** Você acertou! O personagem era **{jogo.personagem['nome']}**!")
                    encerrar_jogo(message.channel.id) 
                    return

bot.run(TOKEN)
