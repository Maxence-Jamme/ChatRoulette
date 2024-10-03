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


async def remove_driver(arg):
    lettres = arg[1:]  # Retirer le tiret
    liste_modifiee = carList

    for lettre in lettres:
        if lettre in dico:
            element_a_retirer = dico[lettre]
            if element_a_retirer in liste_modifiee:
                liste_modifiee.remove(element_a_retirer)

    return liste_modifiee

async def choose_driver(arg):
    # Liste modifiable de tous les pilotes possibles
    liste_modifiee = list(dico.values())
    
    # Liste des pilotes choisis
    pilotes_choisis = []

    if arg:
        # Argument fourni : retirer les pilotes correspondants
        lettres = arg[1:]  # Retirer le tiret
        for lettre in lettres:
            if lettre in dico:
                pilote = dico[lettre]
                if pilote in liste_modifiee:
                    pilotes_choisis.append(pilote)
                    liste_modifiee.remove(pilote)

    # S'il manque un ou deux pilotes, les choisir aléatoirement
    while len(pilotes_choisis) < 2:
        pilote_aleatoire = random.choice(liste_modifiee)
        pilotes_choisis.append(pilote_aleatoire)
        liste_modifiee.remove(pilote_aleatoire)
    
    return pilotes_choisis

# Commande !car avec gestion des arguments
@bot.command(name="car")
async def car(ctx, arg=None):
    user = ctx.author
    if arg == None:
        arg = ' '
    for i in range(10):
        await car_message(ctx, user, arg)

async def car_message(ctx, user, arg):
    print("Commande !car reçue",type(user),user.display_name)

    if arg[0]=="-":
        print('1')
        Liste_driver = await remove_driver(arg)
    elif arg[0]=="+":
        print('2')
        Liste_driver = await choose_driver(arg)
    elif user.display_name in ['Albus', 'jean_gmrch']:
        print('3')
        Liste_driver = carList + ['<@309034764965380106> Etienne', '<@449122128248438784> Nicolas']*3
    else :
        print('4')
        Liste_driver = carList
    print(Liste_driver)
    while True:
        tirage_aleatoire = random.sample(Liste_driver, 2)
        if tirage_aleatoire[0] != tirage_aleatoire[1]:
            break
    await ctx.send(f"Les deux pilotes du jour sont : {tirage_aleatoire[0]} et {tirage_aleatoire[1]}")










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

# Lancer le bot
bot.run(TOKEN)  
