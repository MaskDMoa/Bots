import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class InscricaoSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="🏆 Inscrever-se no torneio",
                value="join",
                description="Participar como jogador"
            ),
            discord.SelectOption(
                label="👁 Apenas assistir",
                value="watch",
                description="Entrar como espectador"
            )
        ]

        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        escolha = self.values[0]

        if escolha == "join":
            guild = interaction.guild
            categoria = interaction.channel.category
            usuario = interaction.user

            overwrite = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                usuario: discord.PermissionOverwrite(read_messages=True, view_channel=True),
                guild.me: discord.PermissionOverwrite(view_channel=True)
            }

            canal = await guild.create_text_channel(
                name=f"Duelista-{usuario.name}",
                category=categoria,
                overwrites=overwrite
            )

        embed = discord.Embed(
            title="📜 Regras Oficiais – Yu-Gi-Oh! Grand Tournament",
            description=(
            "**Para validar sua inscrição, você deve enviar:**\n\n"
            "1️⃣ **Nome do seu Deck**\n"
            "2️⃣ **Imagem do deck completo** (print do simulador ou foto legível)\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "## 🧾 Regras do Torneio\n\n"
            "🔹 **1. Deck Fixo**\n"
            "Após o envio e aprovação, seu deck fica **bloqueado**. Qualquer alteração resultará em **desclassificação**.\n\n"

            "🔹 **2. Era Permitida**\n"
            "Somente cartas até a **3ª Geração de Yu-Gi-Oh!** são permitidas.\n"
            "_(DM, GX e 5D’s)_\n\n"

            "🔹 **3. Meta Proibido**\n"
            "Decks considerados **Meta** ou **Tier competitivo** estão **proibidos**.\n"
            "O torneio prioriza **criatividade e equilíbrio**.\n\n"

            "🔹 **4. Mecânicas Permitidas**\n"
            "✔ Fusão\n"
            "✔ Synchro\n"
            "✔ Xyz\n\n"
            "❌ Link\n"
            "❌ Pêndulo\n"
            "❌ Qualquer mecânica posterior\n\n"

            "🔹 **5. Banlist**\n"
            "Baseada na **banlist oficial da Konami**, ajustada pela staff.\n\n"

            "🔹 **6. Formato das Partidas**\n"
            "Todas as partidas serão **Melhor de 3 (MD3)**.\n\n"

            "🔹 **7. Conduta**\n"
            "Ofensas, abuso de regras ou comportamento tóxico resultarão em **eliminação imediata**.\n\n"

            "🔹 **8. Print Obrigatório**\n"
            "Em caso de disputa, os jogadores devem fornecer **prints do duelo**.\n\n"

            "🔹 **9. Desconexões**\n"
            "Uma queda dá direito a **1 reinício**. Segunda queda = derrota.\n\n"

            "🔹 **10. Decisão da Staff**\n"
            "A **staff tem a palavra final** sobre decks, duelos e disputas.\n\n"

            "🔹 **11. Plataforma**\n"
            "As Disputas acontecerão na Plataforma **Master Duel**, durante o duelo os 2 duelistas devem estar em call mostrando a tela do jogo.\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ **Ao enviar seu deck, você concorda com todas as regras acima.**"
        ),
        color=discord.Color.gold()
    )
            
        await canal.send(embed=embed)

        await canal.send(
            f"{usuario.mention}, Obrigado pela participação!\n"
            "Por favor, envie agora o **nome do seu deck** e depois a **imagem do deck completo**."
        )


class InscricaoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(InscricaoSelect())


# ========== COMANDO PARA ENVIAR O PAINEL ==========
@bot.command()
@commands.has_role("Nome do cargo ou ID do cargo que pode usar o comando")
async def painel(ctx):
    embed = discord.Embed(
        description=(
            "# Yu-Gi-Oh! Grand Tournament \n\n\n"
            "## Bem-vindo ao grandioso torneio de Yu-Gi-Oh! Prepare-se para duelar com os melhores e mostrar suas habilidades. \n\n" 
            "### Mostre a todos que você é o verdadeiro Rei dos Duelos! \n\n" 
            "### Coloque seu deck a prova e oblitere seus oponentes para conquistar a vitória suprema!" 
        ),
        color=discord.Color.purple()
    )

    embed.set_image(url="https://i.imgur.com/vsbc8RB.jpeg")

    await ctx.send(embed=embed, view=InscricaoView())


bot.run("SEU_TOKEN_AQUI")