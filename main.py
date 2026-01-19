import discord
from discord import app_commands
from discord.ext import commands
import random
import os

# Le token et ton ID seront ajoutés plus tard sur Railway
TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

codes_valides = set()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot prêt et connecté")

# =====================
# /codegenerer (SEULEMENT TOI)
# =====================
@bot.tree.command(name="codegenerer", description="Génère un code unique")
async def codegenerer(interaction: discord.Interaction):

    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(
            "❌ Tu n'as pas la permission d'utiliser cette commande.",
            ephemeral=True
        )
        return

    code = str(random.randint(100000, 999999))
    codes_valides.add(code)

    await interaction.response.send_message(
        f"✅ Code généré : **{code}**",
        ephemeral=True
    )

# =====================
# TIRAGE DES POINTS (TRÈS DUR)
# =====================
def tirage_points():
    roll = random.randint(1, 100000)

    if roll <= 60000:
        return random.randint(1, 1000)
    elif roll <= 85000:
        return random.randint(1000, 5000)
    elif roll <= 95000:
        return random.randint(5000, 10000)
    elif roll <= 98500:
        return random.randint(10000, 15000)
    elif roll <= 99500:
        return random.randint(15000, 18000)
    elif roll <= 99900:
        return random.randint(18000, 19900)
    else:
        return random.randint(19900, 20000)

# =====================
# RARETÉ
# =====================
def rarete(points):
    if points <= 1000:
        return "Commun"
    elif points <= 5000:
        return "Rare"
    elif points <= 10000:
        return "Très rare"
    elif points <= 15000:
        return "Épique"
    elif points <= 18000:
        return "Légendaire"
    elif points <= 19900:
        return "Mythique"
    else:
        return "Impossible"

# =====================
# COULEUR SELON RARETÉ
# =====================
def couleur_rarete(r):
    couleurs = {
        "Commun": discord.Color.light_grey(),
        "Rare": discord.Color.blue(),
        "Très rare": discord.Color.purple(),
        "Épique": discord.Color.orange(),
        "Légendaire": discord.Color.gold(),
        "Mythique": discord.Color.red(),
        "Impossible": discord.Color.from_rgb(0, 0, 0)
    }
    return couleurs.get(r, discord.Color.default())

# =====================
# /codeutiliser
# =====================
@bot.tree.command(name="codeutiliser", description="Utilise un code")
@app_commands.describe(code="Entre ton code")
async def codeutiliser(interaction: discord.Interaction, code: str):

    if code not in codes_valides:
        await interaction.response.send_message(
            "❌ **Code invalide**",
            ephemeral=True
        )
        return

    codes_valides.remove(code)

    points = tirage_points()
    r = rarete(points)

    embed = discord.Embed(
        title="🎉 GAIN OBTENU",
        description=(
            f"Bravo 🎊 {interaction.user.mention}\n\n"
            f"💰 Tu as gagné **{points} points**\n"
            f"🏆 Rareté : **{r}**\n\n"
            f"🎫 Va réclamer ton gain dans un ticket !"
        ),
        color=couleur_rarete(r)
    )

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
