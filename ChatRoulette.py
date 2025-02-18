import discord
import random
import requests
import asyncio
from discord.ext import commands
from datetime import datetime
import tk
import os
from PIL import Image
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import io
import sudo as sudoku
import cv2
import numpy as np
import easyocr

def tirer_film_au_hasard(api_key):
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": api_key,
        "language": "fr-FR",
        "sort_by": "popularity.desc",  # Trier par popularité
        "page": random.randint(1, 10)  # Tirer une page au hasard entre 1 et 10
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        films = data["results"]
        
        if films:
            film_choisi = random.choice(films)
            titre = film_choisi["title"]
            description = film_choisi["overview"]
            image_path = film_choisi["poster_path"]
            image_url = f"https://image.tmdb.org/t/p/w500{image_path}"  # URL complète de l'image
            
            
            
            return titre, description, image_url
        else:
            return "Aucun film trouvé", "", ""
    else:
        return "Erreur lors de la récupération des films", "", ""

# Exemple d'utilisation


carList = ['<@333966716520628226> Maxence', '<@1046487582109876264> Jean', '<@309034764965380106> Etienne', 
        '<@367319844581801994> Gabriel', '<@449122128248438784> Nicolas', '<@577465394449874976> Damien']
carListSR = ['<@1046487582109876264> Jean', '<@309034764965380106> Etienne', '<@449122128248438784> Nicolas']
carListDL = ['<@333966716520628226> Maxence', '<@367319844581801994> Gabriel', '<@577465394449874976> Damien']
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

authorized_user_id = 333966716520628226  # Remplacez par votre propre ID Discord

TOKEN = tk.get_tk()
api_key = tk.get_tk_TMDB()

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

@bot.event
async def on_message(message):
    # Ignore les messages envoyés par le bot lui-même
    if message.author == bot.user:
        return

    # Vérifie si le message est un message privé (DM)
    if isinstance(message.channel, discord.DMChannel):
        print(f"Message privé reçu de {message.author}: {message.content}")
        #await message.channel.send("Merci pour votre message !")
        if message.content == "!sudo" and message.attachments:
            # Créez un contexte factice pour appeler la commande
            ctx = await bot.get_context(message)
            await sudo(ctx)
        else:
        
            message = f"{message.author}: {message.content}"
            await send_message_to_channel(1291744785190883339, message)
    else:
        await bot.process_commands(message)

@bot.event
async def send_message_to_channel(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        print(f"Channel with ID {channel_id} not found")

async def remove_driver(arg):
    lettres = arg[1:]  # Retirer le tiret
    liste_modifiee = carList.copy()


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
    await car_message(ctx, user, arg)

async def car_message(ctx, user, arg):
    print("Commande !car reçue",type(user),user.display_name)
    Liste_driver = []
    print(type(arg))
    if arg[0]=="-":
        print('1')
        Liste_driver = await remove_driver(arg)
    elif arg[0]=="+":
        print('2')
        Liste_driver = await choose_driver(arg)
    elif arg=="SRDL":
        Liste_driver = random.sample(carListSR, 1)
        Liste_driver.append(random.choice(carListDL))   
    else :
        print('3')
        Liste_driver = carList
    if(len(Liste_driver) >= 2):
        while True:
            tirage_aleatoire = random.sample(Liste_driver, 2)
            if tirage_aleatoire[0] != tirage_aleatoire[1]:
                break
        await ctx.send(f"Les deux pilotes du jour sont : {tirage_aleatoire[0]} et {tirage_aleatoire[1]}")
    else:
        await ctx.send(f"Erreur dans la commande")










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
    print(ctx)
    await ctx.send(f"test")

# Commande !test avec deux arguments (arg2 peut contenir des espaces)
@bot.command(name="test1", hidden=True)
async def test(ctx, arg1: int = None, *, arg2=None):
    print("Commande !test reçue")
    user = ctx.author
    if ctx.author.id != authorized_user_id:
        await ctx.send("Vous n'avez pas la permission d'éxecuter cette commande.")
        return
    
    if user.display_name == "Albus":
        print(f"Argument 1 : {type(arg1)}")
        print(f"Argument 2 : {arg2}")  # arg2 peut contenir des espaces
        await send_message_to_channel(arg1, arg2)


# Commande !test2 pour envoyer un DM à un utilisateur spécifique
@bot.command(name="test2", hidden=True)
async def test2(ctx, user_id: int = None, *, message=None):
    print("Commande !test2 reçue")
    if ctx.author.id != authorized_user_id:
        await ctx.send("Vous n'avez pas la permission d'éxecuter cette commande.")
        return
    
    # Vérifie si l'ID utilisateur et le message sont fournis
    if user_id is None or message is None:
        await ctx.send("Merci de fournir un ID utilisateur et un message.")
        return

    try:
        # Récupère l'utilisateur à partir de l'ID
        user = await bot.fetch_user(user_id)
        
        if user:
            # Envoie un DM à l'utilisateur
            await user.send(message)
            await ctx.send(f"Message envoyé à {user.display_name} avec succès !")
        else:
            await ctx.send(f"Utilisateur avec l'ID {user_id} non trouvé.")
    except Exception as e:
        print(f"Erreur : {e}")
        await ctx.send(f"Impossible d'envoyer le message : {str(e)}")

# Commande !test3 pour répondre à un message spécifique dans un canal
@bot.command(name="test3", hidden=True)
async def test3(ctx, channel_id: int, message_id: int, *, msg=None):
    print("Commande !test3 reçue")
    if ctx.author.id != authorized_user_id:
        await ctx.send("Vous n'avez pas la permission d'éxecuter cette commande.")
        return
    
    # Vérifie si le message est fourni
    if msg is None:
        await ctx.send("Merci de fournir un message à envoyer.")
        return

    # Récupère le canal à partir de l'ID
    channel = bot.get_channel(channel_id)

    if channel is None:
        await ctx.send(f"Canal avec l'ID {channel_id} non trouvé.")
        return

    try:
        # Récupère le message à partir de l'ID
        message = await channel.fetch_message(message_id)

        if message:
            # Répondre au message
            await message.reply(msg)
            await ctx.send("Message répondu avec succès !")
        else:
            await ctx.send(f"Message avec l'ID {message_id} non trouvé dans le canal.")
    except Exception as e:
        print(f"Erreur : {e}")
        await ctx.send(f"Impossible de répondre au message : {str(e)}")


# Commande !reboot pour redémarrer le serveur (seulement par l'utilisateur spécifié)
@bot.command(name="reboot", hidden=True)
async def reboot(ctx):
    # ID de l'utilisateur autorisé à redémarrer le serveur (remplacez par votre ID Discord)
    

    # Vérifie si l'utilisateur qui a envoyé la commande est autorisé
    if ctx.author.id == authorized_user_id:
        await ctx.send("Redémarrage du serveur en cours...")
        print("Redémarrage du serveur initié par l'utilisateur autorisé.")
        
        # Commande pour redémarrer le serveur
        os.system("sudo reboot")
    else:
        await ctx.send("Vous n'avez pas la permission de redémarrer le serveur.")
        print(f"L'utilisateur {ctx.author} a tenté de redémarrer le serveur sans autorisation.")


# Commande !film pour redémarrer le serveur (seulement par l'utilisateur spécifié)
@bot.command(name="film")
async def film(ctx):
    film, description, url = tirer_film_au_hasard(api_key)
    await ctx.send(film)
    await ctx.send(description)
    await ctx.send(url)





@bot.command(name="noel", help="Organise un Secret Santa 🎅")
async def noel(ctx, *participants: discord.Member):
    if ctx.author.id != authorized_user_id:
        await ctx.send("Vous n'avez pas la permission d'éxecuter cette commande.")
        try:
            await ctx.author.send("Tu viens de tirer au sors Albus, bravo a toi tu peux lui faire un cadeau d'une valeur d 150euros.")
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}, je n'ai pas pu vous envoyer un message privé. Activez vos MP ou contactez Albus.")
        return
    
    if len(participants) < 2:
        await ctx.send("Il faut au moins 2 participants pour organiser un Secret Santa !")
        return

    # Création de la liste des participants
    participants_list = list(participants)
    random.shuffle(participants_list)

    # Création des paires Secret Santa
    assignments = {}
    for i in range(len(participants_list)):
        santa = participants_list[i]
        recipient = participants_list[(i + 1) % len(participants_list)]  # La personne suivante
        assignments[santa] = recipient

    # Notification des participants
    for santa, recipient in assignments.items():
        try:
            await santa.send(f"🎅 HoHoHo 🎅")
            await santa.send(f"🎁 Bonjour {santa.display_name} 🎁")
            await santa.send(f"Tu es le Secret Santa de **{recipient.display_name}** !")
            await santa.send(f"🤫 Garde cela secret et prépare un joli cadeau d'une valeur de 20 euros max pour cette personne!")
            await santa.send(f"Les cadeaux seront dévoilés jeudi soir !")
            await send_message_to_channel(1318238365849620510, f"{santa.display_name} fait un cadeau à {recipient.display_name}")
        except discord.Forbidden:
            await ctx.send(f"Je n'ai pas pu envoyer un message privé à {santa.mention}. 😢")

    await ctx.send("🎅 Le Secret Santa a été organisé avec succès ! Vérifiez vos messages privés pour savoir à qui offrir un cadeau. 🎄")



# Commande !sudo
@bot.command()
async def sudo(ctx):
    print("Commande !sudo reçue")
    
    if isinstance(ctx.channel, discord.DMChannel):
        sender = ctx.author
    else:
        sender = ctx.channel

    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]

        # Télécharger l'image
        image_bytes = await attachment.read()
        pil_image = Image.open(io.BytesIO(image_bytes))

        # Convertir PIL -> NumPy pour OpenCV
        image_np = np.array(pil_image)

        # Envoyer un message pour prévenir que le traitement commence
        processing_message = await sender.send("🔍 Je cherche une solution au Sudoku...")

        try:
            # Timeout après 30 secondes
            processed_image = await asyncio.wait_for(
                asyncio.to_thread(sudoku.sudo, image_np), timeout=30
            )

            # Convertir NumPy -> PIL
            processed_pil = Image.fromarray(processed_image)

            # Sauvegarder l'image en mémoire
            img_io = io.BytesIO()
            processed_pil.save(img_io, format="PNG")
            img_io.seek(0)

            # Supprimer le message "🔍 Je cherche..."
            await processing_message.delete()

            # Envoyer l'image modifiée
            await sender.send(file=discord.File(img_io, "modified.png"))

        except asyncio.TimeoutError:
            print('ici')
            await processing_message.edit(content="⏳ L'algorithme a mis trop de temps à résoudre le Sudoku ! ❌")

        except Exception as e:
            await processing_message.edit(content=f"⚠️ Une erreur s'est produite : `{str(e)}`")

    else:
        await sender.send("❌ Envoie une image avec la commande !")
        

# Lancer le bot
bot.run(TOKEN)  
