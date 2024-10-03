import discord
import random
import requests
import asyncio
from discord.ext import commands
from datetime import datetime
import tk

carList = ['<@333966716520628226> Maxence', '<@1046487582109876264> Jean', '<@309034764965380106> Etienne', 
        '<@367319844581801994> Gabriel', '<@449122128248438784> Nicolas', '<@577465394449874976> Damien']
dico = {
    'm': '<@333966716520628226> Maxence',
    'j': '<@1046487582109876264> Jean',
    'e': '<@309034764965380106> Etienne',
    'g': '<@367319844581801994> Gabriel',
    'n': '<@449122128248438784> Nicolas',
    'd': '<@577465394449874976> Damien'
}
allList = ['<@398621496358207490>', '<@309034764965380106>', '<@1046487582109876264>', '<@333966716520628226>',
          '<@755788837850185820>', '<@367319844581801994>', '<@196708995589865473>', '<@459750215931658250>',
          '<@550373848424382479>', '<@449122128248438784>', '<@577465394449874976>']
resto = ["Sandwich Intermarché", "Sandwich Boulangerie", "Sandwich Maison"]

TOKEN = tk.get_tk()

# Activer les intents requis
intents = discord.Intents.default()
intents.message_content = True  # Ajoute ceci pour que le bot puisse lire le contenu des messages

# Création du bot avec le préfixe '!'
bot = commands.Bot(command_prefix='!', intents=intents)

# Événement lors de la connexion du bot
@bot.event
async def on_ready(): 
    print(f'Bot connecté en tant que {bot.user}')
    #reset_cooldowns.start()  # Démarrer la tâche planifiée


async def manage_car_args(arg):
    # Vérifier si l'argument commence par un tiret et récupérer les lettres
    if arg.startswith('-'):
        lettres = arg[1:]  # Retirer le tiret
    else:
        return carList  # Si ce n'est pas un argument valide, retourner la liste d'origine

    # Dictionnaire pour correspondance
    dico = {
        'm': '<@333966716520628226> Maxence',
        'j': '<@1046487582109876264> Jean',
        'e': '<@309034764965380106> Etienne',
        'g': '<@367319844581801994> Gabriel',
        'n': '<@449122128248438784> Nicolas',
        'd': '<@577465394449874976> Damien'
    }

    # Créer un duplicata de carList
    liste_modifiee = carList.copy()

    # Retirer les éléments correspondants
    for lettre in lettres:
        if lettre in dico:
            element_a_retirer = dico[lettre]
            if element_a_retirer in liste_modifiee:
                liste_modifiee.remove(element_a_retirer)

    return liste_modifiee

# Commande !car avec gestion des arguments
@bot.command(name="car")
async def car(ctx, arg=None):
    # Si l'argument est "-lundi", appelle une autre fonction
    print(arg)
    
    if arg:
        Lst = await manage_car_args(arg)
        print('------',Lst)
        await car_message(ctx, Lst)
    else:
        await car_message(ctx, carList)

async def car_message(ctx, List):
    print("Commande !car reçue")
    deux_noms = random.sample(List, 2)
    await ctx.send(f"Les deux pilotes du jour sont : {deux_noms[0]} et {deux_noms[1]}")










# Dictionnaire pour stocker les utilisateurs ayant utilisé la commande dans la journée
user_cooldowns_bk = {}

# Date de la dernière réinitialisation du dictionnaire
last_reset_date_bk = datetime.now().date()

# Commande !bk
@bot.command(name="bk")
async def bk(ctx):
    global last_reset_date_bk
    user_id = ctx.author.id  # ID de l'utilisateur qui a utilisé la commande
    now = datetime.now().date()

    # Vérifier si la date a changé (nouvelle journée)
    if now != last_reset_date_bk:
        print('clear')
        user_cooldowns_bk.clear()  # Réinitialiser le dictionnaire
        last_reset_date_bk = now  # Mettre à jour la date de reset

    # Vérifier si l'utilisateur a déjà utilisé la commande aujourd'hui
    if user_id in user_cooldowns_bk:
        last_used = user_cooldowns_bk[user_id]

        # Si l'utilisateur a utilisé la commande aujourd'hui, on bloque
        if last_used == now:
            await ctx.send(f"{ctx.author.mention}, tu as déjà utilisé cette commande aujourd'hui ! Réessaie demain.")
            return

    # Enregistrer la nouvelle utilisation
    user_cooldowns_bk[user_id] = now

    # Envoi du message
    await ctx.send("Est-ce que nous allons manger au Burger King ?")
    await asyncio.sleep(2)

    await ctx.send("Laissez-moi réfléchir...")    
    await asyncio.sleep(2)
    
    await ctx.send("Hmm...")
    await asyncio.sleep(2)

    await ctx.send("Je pense que la réponse est...")
    await asyncio.sleep(2)

    # Déterminer aléatoirement si vous allez au Burger King 1/10
    if random.choice([True, False, False, False, False, False, False, False, False, False]):
        await ctx.send(f"Oui, nous allons manger au Burger King ! 🎉")
    else:
        await ctx.send("Non, on ne mange pas au Burger King. 😢 ")





# ------------
# -- BOUFFE --
# ------------

# Commande !bbq
@bot.command()
async def bbq(ctx):
    print("Commande !bbq reçue")
    await ctx.send(f"Ce soir on mange {random.choice(['barbecue au BAT O', 'barbecue à la plancha', 'tacos à la plancha'])} !")

# Commande !manger
@bot.command()
async def manger(ctx):
    print("Commande !manger reçue")
    repas = random.choice(resto)
    await ctx.send(f"Le repas du jour sera : {repas}")


# ------------
# --- SEXE ---
# ------------

# Commande !pote
@bot.command()
async def pote(ctx):
    print("Commande !pote reçue")
    await ctx.send(f"{random.choice(allList)}Tu dois tenir sa queue pendant qu'il pisse")

# Commande !biscotte
@bot.command()
async def biscotte(ctx):
    print("Commande !biscotte reçue")
    await ctx.send(f"On a pas de biscotte, mais on a une sacrée envie de jouer... {random.choice(allList)} tu seras la biscotte !")

# Commande !branlette
@bot.command()
async def branlette(ctx):
    print("Commande !branlette reçue")
    if random.choice([True, False]):
        await ctx.send(f"Ce soir branlette !")
    else:
        await ctx.send("Ce soir pas de branlette")

# Commande !ph
@bot.command(name="ph")
async def ph(ctx):
    print("Commande !ph reçue")
    channel_id = ctx.channel.id
    print(channel_id)
    if channel_id == 1166358335805734942:
        url = 'https://fr.pornhub.com/random'  # Remplace par l'URL souhaitée
        response = requests.get(url)
        user = random.choice(allList)
        await ctx.send(f"Vidéo recommandée par {user} : {response.url}")
    else :
        await ctx.send(f"Suite à un abus d'utilisation de la commande, celle ci n'est disponible que dans le chanel NSFW !")

# ------------
# --- BALEK --
# ------------

# Commande !feu
@bot.command()
async def feu(ctx):
    print("Commande !feu reçue")
    await ctx.send(f"Ce soir c'est {random.choice(allList)} qui gere le feu au barbecue !")

# Commande !paie
@bot.command()
async def paie(ctx):
    print("Commande !paie reçue")
    await ctx.send(f"C'est {random.choice(allList)} qui paye !")

# Commande !flo
@bot.command()
async def flo(ctx):
    print("Commande !flo reçue")
    await ctx.send(f"Tu {random.choice(['dois arriver à l heure en cours', 'peux ne pas venir en cours, tu choisis', 'peux arriver avec minimum 5 minutes de retard', 'peux arriver à l heure que tu veux en cours'])} !")

# Commande !ping
@bot.command()
async def ping(ctx):
    print("Commande !ping reçue")
    print(ctx)
    await ctx.send(f"pong")

# Commande !test
@bot.command()
async def test(ctx):
    print("Commande !test reçue")
    print(ctx.author)
    await ctx.send(f"test")

@bot.command(name="D20")
async def d20(ctx):
    result = random.randint(1, 20)  # Tirer un nombre aléatoire entre 1 et 20
    await ctx.send(f"Tu as tiré : {result}")

# Commande !actionmonstre
@bot.command(name="actionmonstre")
async def action_monstre(ctx):
    actions = ["Attaque direct", "Pouvoir", "Avancé", "Reculer"]  # Liste des actions
    decision = random.choice(actions)  # Choisir une action aléatoire
    await ctx.send(f"Le monstre a choisi de : {decision}")

# Lancer le bot
bot.run(TOKEN)  
