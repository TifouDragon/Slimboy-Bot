
"""
Games Commands Plugin
Système de jeux et mini-jeux pour tous les utilisateurs
"""

import discord
from discord.ext import commands
from discord import app_commands
import logging
import random
import asyncio
from typing import Optional
import json
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class GamesCommands(commands.Cog):
    """Commandes de jeux et mini-jeux"""

    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
        self.user_scores = self.load_scores()
        
    def load_scores(self):
        """Charger les scores des utilisateurs"""
        try:
            if os.path.exists("game_scores.json"):
                with open("game_scores.json", "r", encoding="utf-8") as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_scores(self):
        """Sauvegarder les scores"""
        try:
            with open("game_scores.json", "w", encoding="utf-8") as f:
                json.dump(self.user_scores, f, indent=2)
        except Exception as e:
            logger.error(f"Erreur sauvegarde scores: {e}")
    
    def add_score(self, user_id: str, game: str, points: int):
        """Ajouter des points à un utilisateur"""
        if user_id not in self.user_scores:
            self.user_scores[user_id] = {}
        if game not in self.user_scores[user_id]:
            self.user_scores[user_id][game] = 0
        self.user_scores[user_id][game] += points
        self.save_scores()

    @app_commands.command(name="deviner-nombre", description="🎯 Devinez le nombre entre 1 et 100!")
    async def guess_number(self, interaction: discord.Interaction):
        """Jeu de devinette de nombre"""
        if str(interaction.user.id) in self.active_games:
            await interaction.response.send_message("❌ Vous avez déjà un jeu en cours!", ephemeral=True)
            return
            
        number = random.randint(1, 100)
        attempts = 0
        max_attempts = 7
        
        self.active_games[str(interaction.user.id)] = {
            'game': 'guess_number',
            'number': number,
            'attempts': attempts,
            'max_attempts': max_attempts
        }
        
        embed = discord.Embed(
            title="🎯 Jeu de Devinette",
            description=f"J'ai choisi un nombre entre **1** et **100**!\nVous avez **{max_attempts}** tentatives pour le deviner.",
            color=0x00FF00
        )
        embed.add_field(name="💡 Comment jouer", value="Tapez simplement un nombre dans le chat!", inline=False)
        embed.set_footer(text="Tapez 'stop' pour arrêter le jeu")
        
        await interaction.response.send_message(embed=embed)
        
        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel
        
        while attempts < max_attempts:
            try:
                message = await self.bot.wait_for('message', timeout=60.0, check=check)
                
                if message.content.lower() == 'stop':
                    del self.active_games[str(interaction.user.id)]
                    await message.reply("🛑 Jeu arrêté! Le nombre était: **{}**".format(number))
                    return
                
                try:
                    guess = int(message.content)
                except ValueError:
                    await message.reply("❌ Veuillez entrer un nombre valide!")
                    continue
                
                attempts += 1
                self.active_games[str(interaction.user.id)]['attempts'] = attempts
                
                if guess == number:
                    points = max(10, 50 - (attempts * 5))
                    self.add_score(str(interaction.user.id), "deviner_nombre", points)
                    del self.active_games[str(interaction.user.id)]
                    
                    embed = discord.Embed(
                        title="🎉 Félicitations!",
                        description=f"Vous avez trouvé le nombre **{number}** en **{attempts}** tentatives!",
                        color=0xFFD700
                    )
                    embed.add_field(name="🏆 Points gagnés", value=f"**{points}** points", inline=True)
                    await message.reply(embed=embed)
                    return
                    
                elif guess < number:
                    hint = "📈 Plus grand!"
                else:
                    hint = "📉 Plus petit!"
                
                remaining = max_attempts - attempts
                if remaining > 0:
                    await message.reply(f"{hint} Il vous reste **{remaining}** tentatives.")
                    
            except asyncio.TimeoutError:
                del self.active_games[str(interaction.user.id)]
                await interaction.followup.send("⏰ Temps écoulé! Le nombre était: **{}**".format(number))
                return
        
        # Échec
        del self.active_games[str(interaction.user.id)]
        embed = discord.Embed(
            title="💔 Échec!",
            description=f"Vous n'avez pas trouvé le nombre **{number}** en {max_attempts} tentatives.",
            color=0xFF0000
        )
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="pierre-papier-ciseaux", description="✂️ Jouez à pierre-papier-ciseaux contre le bot!")
    @app_commands.describe(choix="Votre choix: pierre, papier ou ciseaux")
    @app_commands.choices(choix=[
        app_commands.Choice(name="🗿 Pierre", value="pierre"),
        app_commands.Choice(name="📄 Papier", value="papier"),
        app_commands.Choice(name="✂️ Ciseaux", value="ciseaux")
    ])
    async def rock_paper_scissors(self, interaction: discord.Interaction, choix: app_commands.Choice[str]):
        """Pierre-papier-ciseaux"""
        bot_choices = ["pierre", "papier", "ciseaux"]
        bot_choice = random.choice(bot_choices)
        
        emojis = {"pierre": "🗿", "papier": "📄", "ciseaux": "✂️"}
        
        user_choice = choix.value
        
        # Déterminer le gagnant
        if user_choice == bot_choice:
            result = "🤝 Égalité!"
            color = 0xFFFF00
            points = 1
        elif (user_choice == "pierre" and bot_choice == "ciseaux") or \
             (user_choice == "papier" and bot_choice == "pierre") or \
             (user_choice == "ciseaux" and bot_choice == "papier"):
            result = "🎉 Vous gagnez!"
            color = 0x00FF00
            points = 3
        else:
            result = "😢 Vous perdez!"
            color = 0xFF0000
            points = 0
        
        if points > 0:
            self.add_score(str(interaction.user.id), "pierre_papier_ciseaux", points)
        
        embed = discord.Embed(
            title="✂️ Pierre-Papier-Ciseaux",
            description=result,
            color=color
        )
        embed.add_field(name="Votre choix", value=f"{emojis[user_choice]} {user_choice.title()}", inline=True)
        embed.add_field(name="Mon choix", value=f"{emojis[bot_choice]} {bot_choice.title()}", inline=True)
        if points > 0:
            embed.add_field(name="🏆 Points", value=f"+{points} points", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="memory", description="🧠 Jeu de mémoire - mémorisez la séquence!")
    async def memory_game(self, interaction: discord.Interaction):
        """Jeu de mémoire"""
        if str(interaction.user.id) in self.active_games:
            await interaction.response.send_message("❌ Vous avez déjà un jeu en cours!", ephemeral=True)
            return
        
        sequence = []
        level = 1
        max_level = 10
        
        emojis = ["🔴", "🔵", "🟢", "🟡", "🟣", "🟠"]
        
        self.active_games[str(interaction.user.id)] = {
            'game': 'memory',
            'sequence': sequence,
            'level': level
        }
        
        embed = discord.Embed(
            title="🧠 Jeu de Mémoire",
            description="Mémorisez la séquence d'emojis et reproduisez-la!",
            color=0x9932CC
        )
        embed.add_field(name="📋 Instructions", 
                       value="1. Je vais afficher une séquence\n2. Mémorisez-la\n3. Reproduisez-la en réagissant aux emojis", 
                       inline=False)
        
        await interaction.response.send_message(embed=embed)
        
        while level <= max_level:
            # Ajouter un nouvel emoji à la séquence
            sequence.append(random.choice(emojis))
            
            # Afficher la séquence
            sequence_str = " ".join(sequence)
            embed = discord.Embed(
                title=f"🧠 Niveau {level}",
                description=f"Mémorisez cette séquence:\n\n{sequence_str}",
                color=0x9932CC
            )
            embed.set_footer(text="Cette séquence va disparaître dans 3 secondes...")
            
            message = await interaction.followup.send(embed=embed)
            
            # Ajouter les réactions possibles
            for emoji in emojis:
                await message.add_reaction(emoji)
            
            await asyncio.sleep(3 + level * 0.5)  # Plus de temps pour les niveaux élevés
            
            # Cacher la séquence
            embed = discord.Embed(
                title=f"🧠 Niveau {level}",
                description="Reproduisez la séquence en cliquant sur les emojis dans l'ordre!",
                color=0x9932CC
            )
            embed.add_field(name="Séquence à reproduire", value=f"{len(sequence)} emojis", inline=True)
            await message.edit(embed=embed)
            
            # Collecter les réponses
            user_sequence = []
            
            def check(reaction, user):
                return user == interaction.user and str(reaction.emoji) in emojis and reaction.message == message
            
            for _ in range(len(sequence)):
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                    user_sequence.append(str(reaction.emoji))
                    await message.remove_reaction(reaction.emoji, user)
                except asyncio.TimeoutError:
                    del self.active_games[str(interaction.user.id)]
                    await interaction.followup.send("⏰ Temps écoulé!")
                    return
            
            # Vérifier la séquence
            if user_sequence == sequence:
                points = level * 5
                self.add_score(str(interaction.user.id), "memory", points)
                
                if level == max_level:
                    embed = discord.Embed(
                        title="🏆 PARFAIT!",
                        description=f"Vous avez terminé tous les niveaux!\nScore total: **{level * 5}** points",
                        color=0xFFD700
                    )
                    del self.active_games[str(interaction.user.id)]
                    await interaction.followup.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(
                        title="✅ Correct!",
                        description=f"Niveau {level} réussi! +{points} points\nPassage au niveau {level + 1}...",
                        color=0x00FF00
                    )
                    await interaction.followup.send(embed=embed)
                    level += 1
                    await asyncio.sleep(2)
            else:
                total_points = (level - 1) * 5
                embed = discord.Embed(
                    title="❌ Erreur!",
                    description=f"Séquence incorrecte au niveau {level}.\nVous avez gagné **{total_points}** points au total!",
                    color=0xFF0000
                )
                embed.add_field(name="Séquence correcte", value=" ".join(sequence), inline=False)
                embed.add_field(name="Votre séquence", value=" ".join(user_sequence), inline=False)
                del self.active_games[str(interaction.user.id)]
                await interaction.followup.send(embed=embed)
                return

    @app_commands.command(name="quiz", description="🧐 Quiz de culture générale!")
    async def quiz(self, interaction: discord.Interaction):
        """Quiz de culture générale"""
        # Charger les questions déjà posées à cet utilisateur
        user_id = str(interaction.user.id)
        if user_id not in self.user_scores:
            self.user_scores[user_id] = {}
        
        if "quiz_history" not in self.user_scores[user_id]:
            self.user_scores[user_id]["quiz_history"] = []
        
        questions = [
            # GÉOGRAPHIE
            {
                "question": "Quelle est la capitale de la France?",
                "options": ["A) Lyon", "B) Paris", "C) Marseille", "D) Toulouse"],
                "correct": "B",
                "explanation": "Paris est la capitale de la France depuis 987."
            },
            {
                "question": "Combien y a-t-il de continents?",
                "options": ["A) 5", "B) 6", "C) 7", "D) 8"],
                "correct": "C",
                "explanation": "Il y a 7 continents: Afrique, Antarctique, Asie, Europe, Amérique du Nord, Océanie et Amérique du Sud."
            },
            {
                "question": "Quel est le plus grand océan du monde?",
                "options": ["A) Atlantique", "B) Indien", "C) Arctique", "D) Pacifique"],
                "correct": "D",
                "explanation": "L'océan Pacifique couvre environ 46% de la surface océanique mondiale."
            },
            {
                "question": "Dans quel pays se trouve Machu Picchu?",
                "options": ["A) Bolivie", "B) Pérou", "C) Équateur", "D) Colombie"],
                "correct": "B",
                "explanation": "Machu Picchu est une ancienne cité inca située au Pérou."
            },
            {
                "question": "Quelle est la capitale du Japon?",
                "options": ["A) Osaka", "B) Kyoto", "C) Tokyo", "D) Nagoya"],
                "correct": "C",
                "explanation": "Tokyo est la capitale du Japon depuis 1868."
            },
            {
                "question": "Quel est le plus petit pays du monde?",
                "options": ["A) Monaco", "B) Vatican", "C) San Marin", "D) Liechtenstein"],
                "correct": "B",
                "explanation": "Le Vatican est le plus petit État souverain du monde avec 0,44 km²."
            },
            {
                "question": "Dans quel océan se trouve l'île de Madagascar?",
                "options": ["A) Atlantique", "B) Pacifique", "C) Indien", "D) Arctique"],
                "correct": "C",
                "explanation": "Madagascar se trouve dans l'océan Indien, au large de l'Afrique."
            },
            {
                "question": "Quelle est la capitale de l'Australie?",
                "options": ["A) Sydney", "B) Melbourne", "C) Canberra", "D) Perth"],
                "correct": "C",
                "explanation": "Canberra est la capitale de l'Australie depuis 1913."
            },
            {
                "question": "Quel fleuve traverse Paris?",
                "options": ["A) Loire", "B) Seine", "C) Rhône", "D) Garonne"],
                "correct": "B",
                "explanation": "La Seine traverse Paris et divise la ville en Rive Droite et Rive Gauche."
            },
            {
                "question": "Combien d'États composent les États-Unis?",
                "options": ["A) 48", "B) 49", "C) 50", "D) 51"],
                "correct": "C",
                "explanation": "Les États-Unis sont composés de 50 États depuis l'admission d'Hawaï en 1959."
            },
            {
                "question": "Quel est le plus grand désert du monde?",
                "options": ["A) Sahara", "B) Gobi", "C) Antarctique", "D) Kalahari"],
                "correct": "C",
                "explanation": "L'Antarctique est le plus grand désert du monde (désert polaire)."
            },
            {
                "question": "Dans quel pays se trouvent les pyramides de Gizeh?",
                "options": ["A) Soudan", "B) Égypte", "C) Libye", "D) Éthiopie"],
                "correct": "B",
                "explanation": "Les pyramides de Gizeh se trouvent en Égypte, près du Caire."
            },
            
            # SCIENCES
            {
                "question": "Quel est l'élément chimique avec le symbole 'O'?",
                "options": ["A) Or", "B) Oxygène", "C) Osmium", "D) Olivier"],
                "correct": "B",
                "explanation": "O est le symbole de l'oxygène dans le tableau périodique."
            },
            {
                "question": "Quelle est la planète la plus proche du Soleil?",
                "options": ["A) Vénus", "B) Mars", "C) Mercure", "D) Terre"],
                "correct": "C",
                "explanation": "Mercure est la planète la plus proche du Soleil dans notre système solaire."
            },
            {
                "question": "Combien de pattes a une araignée?",
                "options": ["A) 6", "B) 8", "C) 10", "D) 12"],
                "correct": "B",
                "explanation": "Les araignées ont 8 pattes, ce qui les distingue des insectes."
            },
            {
                "question": "Quel est le symbole chimique de l'or?",
                "options": ["A) Go", "B) Au", "C) Or", "D) Ag"],
                "correct": "B",
                "explanation": "Au vient du latin 'aurum' qui signifie or."
            },
            {
                "question": "Quelle planète est surnommée la planète rouge?",
                "options": ["A) Vénus", "B) Mars", "C) Jupiter", "D) Saturne"],
                "correct": "B",
                "explanation": "Mars est appelée la planète rouge à cause de sa couleur rougeâtre."
            },
            {
                "question": "Combien d'os y a-t-il dans le corps humain adulte?",
                "options": ["A) 196", "B) 206", "C) 216", "D) 226"],
                "correct": "B",
                "explanation": "Un adulte a 206 os dans son corps."
            },
            {
                "question": "Quelle est la vitesse de la lumière?",
                "options": ["A) 300 000 km/s", "B) 150 000 km/s", "C) 450 000 km/s", "D) 600 000 km/s"],
                "correct": "A",
                "explanation": "La vitesse de la lumière dans le vide est d'environ 300 000 km/s."
            },
            {
                "question": "Quel gaz représente 78% de l'atmosphère terrestre?",
                "options": ["A) Oxygène", "B) Azote", "C) Dioxyde de carbone", "D) Argon"],
                "correct": "B",
                "explanation": "L'azote représente environ 78% de l'atmosphère terrestre."
            },
            {
                "question": "Combien de cœurs a une pieuvre?",
                "options": ["A) 1", "B) 2", "C) 3", "D) 4"],
                "correct": "C",
                "explanation": "Les pieuvres ont 3 cœurs et du sang bleu."
            },
            {
                "question": "Quel est l'organe le plus lourd du corps humain?",
                "options": ["A) Foie", "B) Cerveau", "C) Poumons", "D) Peau"],
                "correct": "D",
                "explanation": "La peau est l'organe le plus lourd, pesant environ 16% du poids corporel."
            },
            
            # HISTOIRE
            {
                "question": "En quelle année l'homme a-t-il marché sur la Lune pour la première fois?",
                "options": ["A) 1967", "B) 1969", "C) 1971", "D) 1973"],
                "correct": "B",
                "explanation": "Neil Armstrong et Buzz Aldrin ont marché sur la Lune le 20 juillet 1969."
            },
            {
                "question": "En quelle année a commencé la Première Guerre mondiale?",
                "options": ["A) 1912", "B) 1914", "C) 1916", "D) 1918"],
                "correct": "B",
                "explanation": "La Première Guerre mondiale a commencé en 1914."
            },
            {
                "question": "Qui était le premier empereur romain?",
                "options": ["A) Jules César", "B) Auguste", "C) Néron", "D) Trajan"],
                "correct": "B",
                "explanation": "Auguste (Octave) fut le premier empereur romain en 27 av. J.-C."
            },
            {
                "question": "En quelle année est tombé le mur de Berlin?",
                "options": ["A) 1987", "B) 1989", "C) 1991", "D) 1993"],
                "correct": "B",
                "explanation": "Le mur de Berlin est tombé le 9 novembre 1989."
            },
            {
                "question": "Quelle civilisation a construit les pyramides de Gizeh?",
                "options": ["A) Babyloniens", "B) Grecs", "C) Égyptiens", "D) Perses"],
                "correct": "C",
                "explanation": "Les anciennes pyramides de Gizeh ont été construites par les Égyptiens."
            },
            {
                "question": "En quelle année a eu lieu la Révolution française?",
                "options": ["A) 1789", "B) 1792", "C) 1799", "D) 1804"],
                "correct": "A",
                "explanation": "La Révolution française a commencé en 1789."
            },
            
            # LITTÉRATURE
            {
                "question": "Qui a écrit 'Les Misérables'?",
                "options": ["A) Émile Zola", "B) Victor Hugo", "C) Gustave Flaubert", "D) Alexandre Dumas"],
                "correct": "B",
                "explanation": "Victor Hugo a écrit Les Misérables, publié en 1862."
            },
            {
                "question": "Qui a écrit 'Romeo et Juliette'?",
                "options": ["A) Charles Dickens", "B) William Shakespeare", "C) Jane Austen", "D) Oscar Wilde"],
                "correct": "B",
                "explanation": "Romeo et Juliette est une tragédie de William Shakespeare."
            },
            {
                "question": "Dans quel livre trouve-t-on le personnage d'Harry Potter?",
                "options": ["A) Le Seigneur des Anneaux", "B) Narnia", "C) Harry Potter", "D) Percy Jackson"],
                "correct": "C",
                "explanation": "Harry Potter est le personnage principal de la série éponyme de J.K. Rowling."
            },
            {
                "question": "Qui a écrit '1984'?",
                "options": ["A) George Orwell", "B) Aldous Huxley", "C) Ray Bradbury", "D) Isaac Asimov"],
                "correct": "A",
                "explanation": "1984 est un roman dystopique de George Orwell publié en 1949."
            },
            
            # ART
            {
                "question": "Qui a peint la Joconde?",
                "options": ["A) Picasso", "B) Van Gogh", "C) Leonardo da Vinci", "D) Monet"],
                "correct": "C",
                "explanation": "La Joconde a été peinte par Leonardo da Vinci entre 1503 et 1519."
            },
            {
                "question": "Dans quel musée se trouve la Joconde?",
                "options": ["A) Musée d'Orsay", "B) Louvre", "C) Prado", "D) Metropolitan"],
                "correct": "B",
                "explanation": "La Joconde est exposée au Musée du Louvre à Paris."
            },
            {
                "question": "Qui a peint 'La Nuit étoilée'?",
                "options": ["A) Pablo Picasso", "B) Claude Monet", "C) Vincent van Gogh", "D) Paul Cézanne"],
                "correct": "C",
                "explanation": "La Nuit étoilée a été peinte par Vincent van Gogh en 1889."
            },
            
            # MUSIQUE
            {
                "question": "Combien de touches a un piano standard?",
                "options": ["A) 76", "B) 88", "C) 96", "D) 104"],
                "correct": "B",
                "explanation": "Un piano standard a 88 touches (52 blanches et 36 noires)."
            },
            {
                "question": "Combien de cordes a une guitare classique?",
                "options": ["A) 4", "B) 5", "C) 6", "D) 7"],
                "correct": "C",
                "explanation": "Une guitare classique a 6 cordes."
            },
            {
                "question": "Quel compositeur a écrit 'La 9ème Symphonie'?",
                "options": ["A) Mozart", "B) Beethoven", "C) Bach", "D) Chopin"],
                "correct": "B",
                "explanation": "La 9ème Symphonie a été composée par Ludwig van Beethoven."
            },
            
            # SPORT
            {
                "question": "Combien de joueurs y a-t-il dans une équipe de football?",
                "options": ["A) 10", "B) 11", "C) 12", "D) 9"],
                "correct": "B",
                "explanation": "Une équipe de football compte 11 joueurs sur le terrain."
            },
            {
                "question": "Tous les combien d'années ont lieu les Jeux Olympiques d'été?",
                "options": ["A) 2 ans", "B) 3 ans", "C) 4 ans", "D) 5 ans"],
                "correct": "C",
                "explanation": "Les Jeux Olympiques d'été ont lieu tous les 4 ans."
            },
            {
                "question": "Dans quel sport utilise-t-on un volant?",
                "options": ["A) Tennis", "B) Badminton", "C) Squash", "D) Ping-pong"],
                "correct": "B",
                "explanation": "Le badminton utilise un volant au lieu d'une balle."
            },
            {
                "question": "Combien de joueurs composent une équipe de basketball sur le terrain?",
                "options": ["A) 4", "B) 5", "C) 6", "D) 7"],
                "correct": "B",
                "explanation": "Chaque équipe de basketball a 5 joueurs sur le terrain."
            },
            
            # MATHÉMATIQUES
            {
                "question": "Combien de côtés a un hexagone?",
                "options": ["A) 5", "B) 6", "C) 7", "D) 8"],
                "correct": "B",
                "explanation": "Un hexagone est une figure géométrique à 6 côtés."
            },
            {
                "question": "Combien de secondes y a-t-il dans une minute?",
                "options": ["A) 50", "B) 60", "C) 70", "D) 100"],
                "correct": "B",
                "explanation": "Il y a 60 secondes dans une minute."
            },
            {
                "question": "Qu'est-ce que Pi (π) approximativement?",
                "options": ["A) 3,14", "B) 2,71", "C) 1,41", "D) 1,73"],
                "correct": "A",
                "explanation": "Pi (π) vaut approximativement 3,14159."
            },
            {
                "question": "Combien fait 12 × 12?",
                "options": ["A) 124", "B) 134", "C) 144", "D) 154"],
                "correct": "C",
                "explanation": "12 × 12 = 144."
            },
            
            # LANGUES
            {
                "question": "Quelle est la langue la plus parlée au monde?",
                "options": ["A) Anglais", "B) Espagnol", "C) Mandarin", "D) Hindi"],
                "correct": "C",
                "explanation": "Le chinois mandarin est parlé par plus d'1 milliard de personnes."
            },
            {
                "question": "Combien de lettres a l'alphabet français?",
                "options": ["A) 24", "B) 25", "C) 26", "D) 27"],
                "correct": "C",
                "explanation": "L'alphabet français a 26 lettres."
            },
            
            # TECHNOLOGIE
            {
                "question": "En quelle année a été créé Discord?",
                "options": ["A) 2013", "B) 2014", "C) 2015", "D) 2016"],
                "correct": "C",
                "explanation": "Discord a été lancé en mai 2015."
            },
            {
                "question": "Que signifie 'WWW'?",
                "options": ["A) World Wide Web", "B) World War Web", "C) World Web Wire", "D) Wide World Web"],
                "correct": "A",
                "explanation": "WWW signifie World Wide Web."
            },
            {
                "question": "Qui a fondé Microsoft?",
                "options": ["A) Steve Jobs", "B) Bill Gates", "C) Mark Zuckerberg", "D) Elon Musk"],
                "correct": "B",
                "explanation": "Microsoft a été fondé par Bill Gates et Paul Allen en 1975."
            },
            {
                "question": "Quel est le langage de programmation créé par Guido van Rossum?",
                "options": ["A) Java", "B) C++", "C) Python", "D) JavaScript"],
                "correct": "C",
                "explanation": "Python a été créé par Guido van Rossum en 1991."
            },
            
            # ÉCONOMIE
            {
                "question": "Quelle est la monnaie de l'Union Européenne?",
                "options": ["A) Dollar", "B) Livre", "C) Euro", "D) Franc"],
                "correct": "C",
                "explanation": "L'Euro est la monnaie officielle de 19 pays de l'Union Européenne."
            },
            {
                "question": "Quelle entreprise a le plus gros chiffre d'affaires mondial?",
                "options": ["A) Apple", "B) Amazon", "C) Walmart", "D) Google"],
                "correct": "C",
                "explanation": "Walmart est généralement l'entreprise avec le plus gros chiffre d'affaires."
            },
            
            # NATURE & ANIMAUX
            {
                "question": "Quel animal est le roi de la jungle?",
                "options": ["A) Tigre", "B) Éléphant", "C) Lion", "D) Gorille"],
                "correct": "C",
                "explanation": "Le lion est traditionnellement appelé le roi de la jungle."
            },
            {
                "question": "Quel est l'animal le plus rapide du monde?",
                "options": ["A) Guépard", "B) Faucon pèlerin", "C) Antilope", "D) Lièvre"],
                "correct": "B",
                "explanation": "Le faucon pèlerin peut atteindre 390 km/h en piqué."
            },
            {
                "question": "Quel est le plus grand mammifère du monde?",
                "options": ["A) Éléphant", "B) Baleine bleue", "C) Girafe", "D) Rhinocéros"],
                "correct": "B",
                "explanation": "La baleine bleue peut mesurer jusqu'à 30 mètres de long."
            },
            {
                "question": "Combien de temps vit approximativement une tortue géante?",
                "options": ["A) 50 ans", "B) 100 ans", "C) 150 ans", "D) 200 ans"],
                "correct": "C",
                "explanation": "Les tortues géantes peuvent vivre plus de 150 ans."
            },
            {
                "question": "Quel oiseau ne peut pas voler?",
                "options": ["A) Autruche", "B) Aigle", "C) Colibri", "D) Cygne"],
                "correct": "A",
                "explanation": "L'autruche est le plus grand oiseau mais ne peut pas voler."
            },
            
            # CINÉMA & TÉLÉVISION
            {
                "question": "Qui a réalisé le film 'Titanic'?",
                "options": ["A) Steven Spielberg", "B) James Cameron", "C) Martin Scorsese", "D) Christopher Nolan"],
                "correct": "B",
                "explanation": "Titanic a été réalisé par James Cameron en 1997."
            },
            {
                "question": "Dans quelle saga trouve-t-on le personnage de Luke Skywalker?",
                "options": ["A) Star Trek", "B) Star Wars", "C) Stargate", "D) Guardians of the Galaxy"],
                "correct": "B",
                "explanation": "Luke Skywalker est un personnage central de Star Wars."
            },
            {
                "question": "Quel film d'animation Disney met en scène une reine des neiges?",
                "options": ["A) Moana", "B) Raiponce", "C) La Reine des Neiges", "D) Mulan"],
                "correct": "C",
                "explanation": "La Reine des Neiges (Frozen) raconte l'histoire d'Elsa."
            },
            
            # GASTRONOMIE
            {
                "question": "Quel pays est à l'origine des sushis?",
                "options": ["A) Chine", "B) Japon", "C) Corée", "D) Thaïlande"],
                "correct": "B",
                "explanation": "Les sushis sont originaires du Japon."
            },
            {
                "question": "Quel ingrédient principal trouve-t-on dans le guacamole?",
                "options": ["A) Tomate", "B) Avocat", "C) Concombre", "D) Poivron"],
                "correct": "B",
                "explanation": "Le guacamole est principalement fait d'avocat."
            },
            {
                "question": "Dans quel pays a été inventée la pizza?",
                "options": ["A) France", "B) Espagne", "C) Italie", "D) Grèce"],
                "correct": "C",
                "explanation": "La pizza moderne a été inventée en Italie, à Naples."
            },
            
            # MYTHOLOGIE
            {
                "question": "Qui est le roi des dieux dans la mythologie grecque?",
                "options": ["A) Poséidon", "B) Zeus", "C) Hadès", "D) Apollon"],
                "correct": "B",
                "explanation": "Zeus est le roi des dieux de l'Olympe dans la mythologie grecque."
            },
            {
                "question": "Comment s'appelle le marteau de Thor?",
                "options": ["A) Gungnir", "B) Mjöllnir", "C) Gram", "D) Excalibur"],
                "correct": "B",
                "explanation": "Mjöllnir est le marteau magique de Thor dans la mythologie nordique."
            },
            
            # CULTURE GÉNÉRALE VARIÉE
            {
                "question": "Combien y a-t-il de minutes dans une heure?",
                "options": ["A) 50", "B) 60", "C) 70", "D) 100"],
                "correct": "B",
                "explanation": "Une heure contient 60 minutes."
            },
            {
                "question": "Quel jour de la semaine vient après mercredi?",
                "options": ["A) Mardi", "B) Jeudi", "C) Vendredi", "D) Samedi"],
                "correct": "B",
                "explanation": "Jeudi vient après mercredi dans la semaine."
            },
            {
                "question": "Combien de saisons y a-t-il dans une année?",
                "options": ["A) 3", "B) 4", "C) 5", "D) 6"],
                "correct": "B",
                "explanation": "Il y a 4 saisons: printemps, été, automne, hiver."
            },
            {
                "question": "Quelle couleur obtient-on en mélangeant rouge et bleu?",
                "options": ["A) Vert", "B) Orange", "C) Violet", "D) Jaune"],
                "correct": "C",
                "explanation": "Rouge + bleu = violet (couleur secondaire)."
            },
            {
                "question": "Quel est le plus grand nombre à un chiffre?",
                "options": ["A) 8", "B) 9", "C) 10", "D) 11"],
                "correct": "B",
                "explanation": "9 est le plus grand chiffre unique (10 a deux chiffres)."
            },
            {
                "question": "Combien de doigts a une main humaine?",
                "options": ["A) 4", "B) 5", "C) 6", "D) 10"],
                "correct": "B",
                "explanation": "Une main humaine a 5 doigts."
            },
            {
                "question": "Quelle est la forme géométrique d'un ballon de football?",
                "options": ["A) Cube", "B) Pyramide", "C) Sphère", "D) Cylindre"],
                "correct": "C",
                "explanation": "Un ballon de football a une forme sphérique."
            },
            {
                "question": "Combien de pattes a un chien?",
                "options": ["A) 2", "B) 4", "C) 6", "D) 8"],
                "correct": "B",
                "explanation": "Les chiens ont 4 pattes."
            },
            {
                "question": "Dans quelle direction se lève le soleil?",
                "options": ["A) Nord", "B) Sud", "C) Est", "D) Ouest"],
                "correct": "C",
                "explanation": "Le soleil se lève à l'Est et se couche à l'Ouest."
            },
            {
                "question": "Combien de jours y a-t-il en février lors d'une année bissextile?",
                "options": ["A) 28", "B) 29", "C) 30", "D) 31"],
                "correct": "B",
                "explanation": "Février a 29 jours lors des années bissextiles."
            },
            {
                "question": "Quel fruit est traditionnellement associé à New York?",
                "options": ["A) Orange", "B) Banane", "C) Pomme", "D) Pêche"],
                "correct": "C",
                "explanation": "New York est surnommée 'Big Apple' (la Grosse Pomme)."
            },
            {
                "question": "Combien de faces a un dé classique?",
                "options": ["A) 4", "B) 6", "C) 8", "D) 12"],
                "correct": "B",
                "explanation": "Un dé classique a 6 faces numérotées de 1 à 6."
            },
            {
                "question": "Quel métal est liquide à température ambiante?",
                "options": ["A) Fer", "B) Cuivre", "C) Mercure", "D) Plomb"],
                "correct": "C",
                "explanation": "Le mercure est le seul métal liquide à température ambiante."
            },
            {
                "question": "Comment appelle-t-on un groupe de lions?",
                "options": ["A) Meute", "B) Troupeau", "C) Harde", "D) Troupe"],
                "correct": "D",
                "explanation": "Un groupe de lions s'appelle une troupe."
            },
            {
                "question": "Quel est l'ingrédient principal du pain?",
                "options": ["A) Riz", "B) Farine", "C) Sucre", "D) Sel"],
                "correct": "B",
                "explanation": "La farine (généralement de blé) est l'ingrédient principal du pain."
            },
            {
                "question": "Combien de dents a un adulte humain normalement?",
                "options": ["A) 28", "B) 30", "C) 32", "D) 34"],
                "correct": "C",
                "explanation": "Un adulte a normalement 32 dents (y compris les dents de sagesse)."
            },
            {
                "question": "Quelle est la devise de la France?",
                "options": ["A) Liberté, Égalité, Fraternité", "B) Dieu et mon droit", "C) E pluribus unum", "D) In God we trust"],
                "correct": "A",
                "explanation": "La devise française est 'Liberté, Égalité, Fraternité'."
            },
            {
                "question": "Quel instrument utilise un chef d'orchestre?",
                "options": ["A) Flûte", "B) Baguette", "C) Violon", "D) Piano"],
                "correct": "B",
                "explanation": "Le chef d'orchestre utilise une baguette pour diriger."
            },
            {
                "question": "Combien de côtés a un triangle?",
                "options": ["A) 2", "B) 3", "C) 4", "D) 5"],
                "correct": "B",
                "explanation": "Un triangle a 3 côtés par définition."
            },
            {
                "question": "Dans quel conte trouve-t-on trois petits cochons?",
                "options": ["A) Le Petit Chaperon Rouge", "B) Hansel et Gretel", "C) Les Trois Petits Cochons", "D) Boucle d'Or"],
                "correct": "C",
                "explanation": "Les trois petits cochons sont les héros du conte éponyme."
            },
            {
                "question": "Quel est le contraire de 'chaud'?",
                "options": ["A) Tiède", "B) Froid", "C) Humide", "D) Sec"],
                "correct": "B",
                "explanation": "Le contraire de 'chaud' est 'froid'."
            },
            {
                "question": "Combien font 10 + 10?",
                "options": ["A) 15", "B) 20", "C) 25", "D) 30"],
                "correct": "B",
                "explanation": "10 + 10 = 20."
            },
            {
                "question": "Quelle planète est la plus éloignée du Soleil?",
                "options": ["A) Uranus", "B) Neptune", "C) Pluton", "D) Saturne"],
                "correct": "B",
                "explanation": "Neptune est la planète la plus éloignée du Soleil (Pluton n'est plus considérée comme une planète)."
            },
            {
                "question": "Quel animal produit le miel?",
                "options": ["A) Papillon", "B) Abeille", "C) Fourmi", "D) Coccinelle"],
                "correct": "B",
                "explanation": "Les abeilles produisent le miel dans leurs ruches."
            },
            {
                "question": "Combien de roues a une bicyclette?",
                "options": ["A) 1", "B) 2", "C) 3", "D) 4"],
                "correct": "B",
                "explanation": "Une bicyclette a 2 roues."
            },
            {
                "question": "Quel est le premier mois de l'année?",
                "options": ["A) Décembre", "B) Janvier", "C) Février", "D) Mars"],
                "correct": "B",
                "explanation": "Janvier est le premier mois de l'année civile."
            },
            {
                "question": "Combien de lettres y a-t-il dans le mot 'DISCORD'?",
                "options": ["A) 6", "B) 7", "C) 8", "D) 9"],
                "correct": "B",
                "explanation": "DISCORD contient 7 lettres: D-I-S-C-O-R-D."
            },
            {
                "question": "Quel outil utilise-t-on pour mesurer la température?",
                "options": ["A) Baromètre", "B) Thermomètre", "C) Hygromètre", "D) Manomètre"],
                "correct": "B",
                "explanation": "Un thermomètre mesure la température."
            },
            {
                "question": "Combien d'ailes a un papillon?",
                "options": ["A) 2", "B) 4", "C) 6", "D) 8"],
                "correct": "B",
                "explanation": "Les papillons ont 4 ailes (2 antérieures et 2 postérieures)."
            },
            {
                "question": "Dans quel récipient fait-on généralement cuire les pâtes?",
                "options": ["A) Poêle", "B) Casserole", "C) Four", "D) Autocuiseur"],
                "correct": "B",
                "explanation": "On fait cuire les pâtes dans une casserole avec de l'eau bouillante."
            },
            {
                "question": "Quel est le symbole chimique du fer?",
                "options": ["A) F", "B) Fe", "C) Fi", "D) Fr"],
                "correct": "B",
                "explanation": "Fe est le symbole du fer (du latin 'ferrum')."
            },
            {
                "question": "Combien de cordes a un violon?",
                "options": ["A) 3", "B) 4", "C) 5", "D) 6"],
                "correct": "B",
                "explanation": "Un violon a 4 cordes accordées en Sol, Ré, La, Mi."
            },
            {
                "question": "Quel fruit pousse sur un pommier?",
                "options": ["A) Poire", "B) Pomme", "C) Cerise", "D) Abricot"],
                "correct": "B",
                "explanation": "Les pommes poussent sur les pommiers."
            },
            {
                "question": "Dans combien de pays peut-on utiliser l'Euro?",
                "options": ["A) 17", "B) 19", "C) 21", "D) 23"],
                "correct": "B",
                "explanation": "L'Euro est utilisé dans 19 pays de la zone Euro."
            },
            
            # NOUVELLES QUESTIONS - TECHNOLOGIE
            {
                "question": "Qui est le fondateur de Microsoft?",
                "options": ["A) Steve Jobs", "B) Bill Gates", "C) Mark Zuckerberg", "D) Elon Musk"],
                "correct": "B",
                "explanation": "Bill Gates a fondé Microsoft avec Paul Allen en 1975."
            },
            {
                "question": "Que signifie 'HTML'?",
                "options": ["A) HyperText Markup Language", "B) Home Tool Markup Language", "C) Hyperlinks Text Mark Language", "D) Hypermedia Text Mode Language"],
                "correct": "A",
                "explanation": "HTML signifie HyperText Markup Language, le langage de balisage du web."
            },
            {
                "question": "Quel réseau social utilise un oiseau bleu comme logo?",
                "options": ["A) Facebook", "B) Instagram", "C) Twitter", "D) LinkedIn"],
                "correct": "C",
                "explanation": "Twitter utilise un oiseau bleu comme logo (maintenant X)."
            },
            {
                "question": "En quelle année YouTube a-t-il été créé?",
                "options": ["A) 2003", "B) 2005", "C) 2007", "D) 2009"],
                "correct": "B",
                "explanation": "YouTube a été créé en février 2005."
            },
            {
                "question": "Quelle entreprise fabrique l'iPhone?",
                "options": ["A) Samsung", "B) Google", "C) Apple", "D) Microsoft"],
                "correct": "C",
                "explanation": "L'iPhone est fabriqué par Apple depuis 2007."
            },
            
            # SPORT
            {
                "question": "Combien de joueurs y a-t-il dans une équipe de football?",
                "options": ["A) 9", "B) 10", "C) 11", "D) 12"],
                "correct": "C",
                "explanation": "Une équipe de football compte 11 joueurs sur le terrain."
            },
            {
                "question": "Dans quel sport utilise-t-on une raquette et une balle jaune?",
                "options": ["A) Badminton", "B) Tennis", "C) Squash", "D) Ping-pong"],
                "correct": "B",
                "explanation": "Le tennis se joue avec une raquette et une balle jaune."
            },
            {
                "question": "Combien de points vaut un panier à 3 points au basket?",
                "options": ["A) 1", "B) 2", "C) 3", "D) 4"],
                "correct": "C",
                "explanation": "Un tir derrière la ligne des 3 points vaut 3 points au basketball."
            },
            {
                "question": "Qui a remporté le plus de Ballon d'Or?",
                "options": ["A) Cristiano Ronaldo", "B) Lionel Messi", "C) Zinedine Zidane", "D) Pelé"],
                "correct": "B",
                "explanation": "Lionel Messi a remporté 8 Ballons d'Or, record absolu."
            },
            {
                "question": "Dans quel sport peut-on marquer un 'home run'?",
                "options": ["A) Cricket", "B) Baseball", "C) Rugby", "D) Football américain"],
                "correct": "B",
                "explanation": "Le home run est un coup au baseball."
            },
            
            # MUSIQUE
            {
                "question": "Qui a chanté 'Thriller'?",
                "options": ["A) Elvis Presley", "B) Michael Jackson", "C) Prince", "D) Freddie Mercury"],
                "correct": "B",
                "explanation": "Thriller est une chanson emblématique de Michael Jackson (1982)."
            },
            {
                "question": "Combien de cordes a une guitare classique?",
                "options": ["A) 4", "B) 5", "C) 6", "D) 7"],
                "correct": "C",
                "explanation": "Une guitare classique standard a 6 cordes."
            },
            {
                "question": "Qui est surnommé 'The King of Pop'?",
                "options": ["A) Elvis Presley", "B) Michael Jackson", "C) Prince", "D) Justin Timberlake"],
                "correct": "B",
                "explanation": "Michael Jackson est surnommé le 'King of Pop'."
            },
            {
                "question": "Quel instrument de musique a des touches noires et blanches?",
                "options": ["A) Guitare", "B) Piano", "C) Saxophone", "D) Trompette"],
                "correct": "B",
                "explanation": "Le piano a des touches noires et blanches."
            },
            {
                "question": "Combien de notes y a-t-il dans une gamme musicale?",
                "options": ["A) 5", "B) 7", "C) 8", "D) 12"],
                "correct": "B",
                "explanation": "Une gamme musicale contient 7 notes (do ré mi fa sol la si)."
            },
            
            # JEUX VIDÉO
            {
                "question": "Quel personnage de jeu vidéo est un plombier italien?",
                "options": ["A) Sonic", "B) Mario", "C) Link", "D) Crash"],
                "correct": "B",
                "explanation": "Mario est un plombier italien, mascotte de Nintendo."
            },
            {
                "question": "Dans Minecraft, quel matériau est le plus solide?",
                "options": ["A) Diamant", "B) Obsidienne", "C) Bedrock", "D) Netherite"],
                "correct": "C",
                "explanation": "Le bedrock (roche-mère) est incassable dans Minecraft."
            },
            {
                "question": "Quel jeu vidéo populaire utilise des 'Pokéballs'?",
                "options": ["A) Zelda", "B) Pokémon", "C) Final Fantasy", "D) Dragon Quest"],
                "correct": "B",
                "explanation": "Les Pokéballs sont utilisées pour capturer des Pokémon."
            },
            {
                "question": "Quelle entreprise a créé la PlayStation?",
                "options": ["A) Nintendo", "B) Microsoft", "C) Sony", "D) Sega"],
                "correct": "C",
                "explanation": "Sony a créé la PlayStation en 1994."
            },
            {
                "question": "Dans quel jeu trouve-t-on les personnages Solid Snake et Big Boss?",
                "options": ["A) Metal Gear", "B) Resident Evil", "C) Silent Hill", "D) Final Fantasy"],
                "correct": "A",
                "explanation": "Solid Snake et Big Boss sont des personnages de Metal Gear."
            },
            
            # CINÉMA SUITE
            {
                "question": "Quel acteur joue Iron Man dans les films Marvel?",
                "options": ["A) Chris Evans", "B) Chris Hemsworth", "C) Robert Downey Jr.", "D) Mark Ruffalo"],
                "correct": "C",
                "explanation": "Robert Downey Jr. incarne Tony Stark/Iron Man."
            },
            {
                "question": "Dans quel film trouve-t-on la phrase 'Que la Force soit avec toi'?",
                "options": ["A) Star Trek", "B) Star Wars", "C) Avatar", "D) Matrix"],
                "correct": "B",
                "explanation": "Cette phrase culte vient de Star Wars."
            },
            {
                "question": "Qui a réalisé 'Le Seigneur des Anneaux'?",
                "options": ["A) Steven Spielberg", "B) Peter Jackson", "C) James Cameron", "D) George Lucas"],
                "correct": "B",
                "explanation": "Peter Jackson a réalisé la trilogie du Seigneur des Anneaux."
            },
            {
                "question": "Quel film d'animation Pixar raconte l'histoire d'un rat cuisinier?",
                "options": ["A) Ratatouille", "B) Cars", "C) Toy Story", "D) Les Indestructibles"],
                "correct": "A",
                "explanation": "Ratatouille (2007) raconte l'histoire de Rémy, un rat qui veut cuisiner."
            },
            {
                "question": "Dans quel film trouve-t-on le personnage de Jack Sparrow?",
                "options": ["A) Pirates", "B) Pirates des Caraïbes", "C) Treasure Island", "D) Hook"],
                "correct": "B",
                "explanation": "Jack Sparrow est le personnage principal de Pirates des Caraïbes."
            },
            
            # ANIMAUX SUITE
            {
                "question": "Quel est l'animal le plus rapide du monde?",
                "options": ["A) Lion", "B) Guépard", "C) Faucon pèlerin", "D) Gazelle"],
                "correct": "B",
                "explanation": "Le guépard peut atteindre 110-120 km/h sur terre."
            },
            {
                "question": "Combien de bosses a un chameau d'Arabie?",
                "options": ["A) 0", "B) 1", "C) 2", "D) 3"],
                "correct": "B",
                "explanation": "Le dromadaire (chameau d'Arabie) a 1 bosse, le chameau de Bactriane en a 2."
            },
            {
                "question": "Quel animal est connu pour changer de couleur?",
                "options": ["A) Serpent", "B) Caméléon", "C) Grenouille", "D) Lézard"],
                "correct": "B",
                "explanation": "Le caméléon peut changer de couleur pour se camoufler."
            },
            {
                "question": "Quel mammifère marin utilise l'écholocation?",
                "options": ["A) Requin", "B) Phoque", "C) Dauphin", "D) Baleine à fanons"],
                "correct": "C",
                "explanation": "Les dauphins utilisent l'écholocation pour naviguer et chasser."
            },
            {
                "question": "Combien de pattes a une araignée?",
                "options": ["A) 6", "B) 8", "C) 10", "D) 12"],
                "correct": "B",
                "explanation": "Les araignées (arachnides) ont toutes 8 pattes."
            },
            
            # GÉOGRAPHIE SUITE
            {
                "question": "Quelle est la capitale de l'Italie?",
                "options": ["A) Milan", "B) Rome", "C) Venise", "D) Florence"],
                "correct": "B",
                "explanation": "Rome est la capitale de l'Italie."
            },
            {
                "question": "Sur quel continent se trouve l'Égypte?",
                "options": ["A) Asie", "B) Europe", "C) Afrique", "D) Amérique"],
                "correct": "C",
                "explanation": "L'Égypte se trouve sur le continent africain."
            },
            {
                "question": "Quelle est la langue la plus parlée au monde?",
                "options": ["A) Anglais", "B) Espagnol", "C) Mandarin", "D) Hindi"],
                "correct": "C",
                "explanation": "Le mandarin est la langue la plus parlée au monde (natifs)."
            },
            {
                "question": "Quel pays a la forme d'une botte?",
                "options": ["A) Espagne", "B) Italie", "C) Grèce", "D) Portugal"],
                "correct": "B",
                "explanation": "L'Italie a une forme caractéristique de botte."
            },
            {
                "question": "Quelle est la capitale de l'Espagne?",
                "options": ["A) Barcelone", "B) Madrid", "C) Séville", "D) Valence"],
                "correct": "B",
                "explanation": "Madrid est la capitale de l'Espagne."
            },
            
            # SCIENCES SUITE
            {
                "question": "Combien de temps met la Terre pour faire un tour complet sur elle-même?",
                "options": ["A) 12 heures", "B) 24 heures", "C) 48 heures", "D) 1 semaine"],
                "correct": "B",
                "explanation": "La Terre fait une rotation complète en 24 heures (un jour)."
            },
            {
                "question": "Quel gaz respirons-nous principalement?",
                "options": ["A) Oxygène", "B) Azote", "C) Dioxyde de carbone", "D) Hydrogène"],
                "correct": "B",
                "explanation": "L'air que nous respirons est composé à 78% d'azote."
            },
            {
                "question": "Combien de chromosomes a un être humain?",
                "options": ["A) 23", "B) 36", "C) 46", "D) 52"],
                "correct": "C",
                "explanation": "Un humain a 46 chromosomes (23 paires)."
            },
            {
                "question": "Quel est l'organe qui pompe le sang?",
                "options": ["A) Poumon", "B) Foie", "C) Cœur", "D) Rein"],
                "correct": "C",
                "explanation": "Le cœur pompe le sang dans tout le corps."
            },
            {
                "question": "Quelle est la température d'ébullition de l'eau au niveau de la mer?",
                "options": ["A) 50°C", "B) 75°C", "C) 100°C", "D) 125°C"],
                "correct": "C",
                "explanation": "L'eau bout à 100°C au niveau de la mer."
            },
            
            # HISTOIRE SUITE
            {
                "question": "En quelle année la Seconde Guerre mondiale s'est-elle terminée?",
                "options": ["A) 1943", "B) 1944", "C) 1945", "D) 1946"],
                "correct": "C",
                "explanation": "La Seconde Guerre mondiale s'est terminée en 1945."
            },
            {
                "question": "Qui a peint la chapelle Sixtine?",
                "options": ["A) Leonardo da Vinci", "B) Michel-Ange", "C) Raphaël", "D) Donatello"],
                "correct": "B",
                "explanation": "Michel-Ange a peint le plafond de la chapelle Sixtine."
            },
            {
                "question": "Quel pharaon égyptien avait un tombeau célèbre?",
                "options": ["A) Toutankhamon", "B) Ramsès II", "C) Cléopâtre", "D) Khéops"],
                "correct": "A",
                "explanation": "Le tombeau de Toutankhamon a été découvert intact en 1922."
            },
            {
                "question": "Dans quelle ville a été signé le traité de Versailles?",
                "options": ["A) Paris", "B) Versailles", "C) Londres", "D) Berlin"],
                "correct": "B",
                "explanation": "Le traité de Versailles a été signé à Versailles en 1919."
            },
            {
                "question": "Qui a découvert l'Amérique en 1492?",
                "options": ["A) Amerigo Vespucci", "B) Christophe Colomb", "C) Marco Polo", "D) Vasco de Gama"],
                "correct": "B",
                "explanation": "Christophe Colomb a découvert l'Amérique en 1492."
            },
            
            # CULTURE GÉNÉRALE VARIÉE SUITE
            {
                "question": "Combien de dents a un adulte?",
                "options": ["A) 28", "B) 30", "C) 32", "D) 36"],
                "correct": "C",
                "explanation": "Un adulte a 32 dents (incluant les dents de sagesse)."
            },
            {
                "question": "Quelle couleur obtient-on en mélangeant jaune et bleu?",
                "options": ["A) Orange", "B) Vert", "C) Violet", "D) Marron"],
                "correct": "B",
                "explanation": "Jaune + bleu = vert."
            },
            {
                "question": "Combien de secondes y a-t-il dans une minute?",
                "options": ["A) 30", "B) 50", "C) 60", "D) 100"],
                "correct": "C",
                "explanation": "Une minute contient 60 secondes."
            },
            {
                "question": "Quel est le contraire de 'chaud'?",
                "options": ["A) Tiède", "B) Froid", "C) Glacé", "D) Frais"],
                "correct": "B",
                "explanation": "Froid est le contraire de chaud."
            },
            {
                "question": "Combien font 5 x 5?",
                "options": ["A) 20", "B) 25", "C) 30", "D) 35"],
                "correct": "B",
                "explanation": "5 × 5 = 25."
            },
            
            # GASTRONOMIE SUITE
            {
                "question": "Quel fromage français a des trous?",
                "options": ["A) Camembert", "B) Brie", "C) Emmental", "D) Roquefort"],
                "correct": "C",
                "explanation": "L'emmental est célèbre pour ses trous."
            },
            {
                "question": "Quelle boisson chaude contient de la caféine?",
                "options": ["A) Thé", "B) Café", "C) Chocolat chaud", "D) Toutes ces réponses"],
                "correct": "D",
                "explanation": "Le thé, le café et le chocolat contiennent tous de la caféine."
            },
            {
                "question": "Quel légume fait pleurer quand on le coupe?",
                "options": ["A) Carotte", "B) Oignon", "C) Tomate", "D) Pomme de terre"],
                "correct": "B",
                "explanation": "L'oignon libère des composés sulfurés qui font pleurer."
            },
            {
                "question": "De quel pays vient le sushi?",
                "options": ["A) Chine", "B) Corée", "C) Japon", "D) Thaïlande"],
                "correct": "C",
                "explanation": "Le sushi est originaire du Japon."
            },
            {
                "question": "Quelle est la base de la pâte à pizza traditionnelle?",
                "options": ["A) Riz", "B) Pomme de terre", "C) Farine de blé", "D) Maïs"],
                "correct": "C",
                "explanation": "La pâte à pizza est faite avec de la farine de blé."
            },
            
            # NOUVELLES QUESTIONS ALÉATOIRES
            {
                "question": "Combien de mois ont 31 jours?",
                "options": ["A) 5", "B) 6", "C) 7", "D) 8"],
                "correct": "C",
                "explanation": "7 mois ont 31 jours: janvier, mars, mai, juillet, août, octobre, décembre."
            },
            {
                "question": "Quel est le plus grand pays du monde?",
                "options": ["A) Canada", "B) Chine", "C) États-Unis", "D) Russie"],
                "correct": "D",
                "explanation": "La Russie est le plus grand pays du monde en superficie."
            },
            {
                "question": "Quelle est la capitale du Canada?",
                "options": ["A) Toronto", "B) Vancouver", "C) Ottawa", "D) Montréal"],
                "correct": "C",
                "explanation": "Ottawa est la capitale du Canada."
            },
            {
                "question": "Quel animal est le symbole de la sagesse?",
                "options": ["A) Hibou", "B) Renard", "C) Éléphant", "D) Aigle"],
                "correct": "A",
                "explanation": "Le hibou est traditionnellement le symbole de la sagesse."
            },
            {
                "question": "Combien de côtés a un hexagone?",
                "options": ["A) 4", "B) 5", "C) 6", "D) 8"],
                "correct": "C",
                "explanation": "Un hexagone a 6 côtés."
            },
            {
                "question": "Quelle est la monnaie du Royaume-Uni?",
                "options": ["A) Euro", "B) Dollar", "C) Livre Sterling", "D) Franc"],
                "correct": "C",
                "explanation": "Le Royaume-Uni utilise la livre sterling (£)."
            },
            {
                "question": "Quel oiseau peut voler en arrière?",
                "options": ["A) Aigle", "B) Colibri", "C) Hirondelle", "D) Moineau"],
                "correct": "B",
                "explanation": "Le colibri est le seul oiseau capable de voler en arrière."
            },
            {
                "question": "Combien d'années y a-t-il dans une décennie?",
                "options": ["A) 5", "B) 10", "C) 20", "D) 50"],
                "correct": "B",
                "explanation": "Une décennie = 10 ans."
            },
            {
                "question": "Quelle planète est surnommée l'étoile du berger?",
                "options": ["A) Mars", "B) Jupiter", "C) Vénus", "D) Mercure"],
                "correct": "C",
                "explanation": "Vénus est appelée l'étoile du berger car très brillante."
            },
            {
                "question": "Quel est le nom du célèbre détective créé par Arthur Conan Doyle?",
                "options": ["A) Hercule Poirot", "B) Sherlock Holmes", "C) Miss Marple", "D) Colombo"],
                "correct": "B",
                "explanation": "Sherlock Holmes est le célèbre détective créé par Conan Doyle."
            },
            {
                "question": "Dans quel pays se trouve la tour Eiffel?",
                "options": ["A) Belgique", "B) Suisse", "C) France", "D) Italie"],
                "correct": "C",
                "explanation": "La tour Eiffel se trouve à Paris, en France."
            },
            {
                "question": "Combien de joueurs y a-t-il dans une équipe de rugby?",
                "options": ["A) 11", "B) 13", "C) 15", "D) 17"],
                "correct": "C",
                "explanation": "Une équipe de rugby à XV compte 15 joueurs."
            },
            {
                "question": "Quel super-héros est aussi appelé l'homme chauve-souris?",
                "options": ["A) Spider-Man", "B) Superman", "C) Batman", "D) Iron Man"],
                "correct": "C",
                "explanation": "Batman signifie 'homme chauve-souris' en anglais."
            },
            {
                "question": "Quelle est la formule chimique de l'eau?",
                "options": ["A) H2O", "B) CO2", "C) O2", "D) NaCl"],
                "correct": "A",
                "explanation": "L'eau a pour formule H2O (2 atomes d'hydrogène, 1 d'oxygène)."
            },
            {
                "question": "Combien de zéros y a-t-il dans un million?",
                "options": ["A) 4", "B) 5", "C) 6", "D) 7"],
                "correct": "C",
                "explanation": "Un million = 1 000 000 (6 zéros)."
            },
            {
                "question": "Quel animal est le roi de la jungle?",
                "options": ["A) Tigre", "B) Lion", "C) Éléphant", "D) Gorille"],
                "correct": "B",
                "explanation": "Le lion est traditionnellement appelé le roi de la jungle."
            },
            {
                "question": "Quelle fête est célébrée le 25 décembre?",
                "options": ["A) Pâques", "B) Halloween", "C) Noël", "D) Nouvel An"],
                "correct": "C",
                "explanation": "Noël est célébré le 25 décembre."
            },
            {
                "question": "Combien de centimètres y a-t-il dans un mètre?",
                "options": ["A) 10", "B) 50", "C) 100", "D) 1000"],
                "correct": "C",
                "explanation": "1 mètre = 100 centimètres."
            },
            {
                "question": "Quel fruit est rouge et pousse sur un arbre?",
                "options": ["A) Fraise", "B) Pomme", "C) Tomate", "D) Cerise"],
                "correct": "B",
                "explanation": "La pomme est rouge et pousse sur un pommier (la cerise aussi, mais la pomme est plus courante)."
            },
            {
                "question": "Quelle est la capitale de la Belgique?",
                "options": ["A) Bruges", "B) Anvers", "C) Bruxelles", "D) Liège"],
                "correct": "C",
                "explanation": "Bruxelles est la capitale de la Belgique."
            }
        ]
        
        # Système anti-répétition: privilégier les questions non posées récemment
        user_history = self.user_scores[user_id]["quiz_history"]
        
        # Si l'utilisateur a répondu à moins de la moitié des questions, privilégier les nouvelles
        if len(user_history) < len(questions) // 2:
            unused_questions = [q for i, q in enumerate(questions) if i not in user_history]
            if unused_questions:
                question = random.choice(unused_questions)
                question_index = questions.index(question)
            else:
                question = random.choice(questions)
                question_index = questions.index(question)
        else:
            # Sinon, éviter les 5 dernières questions posées
            recent_questions = user_history[-5:] if len(user_history) >= 5 else user_history
            available_questions = [q for i, q in enumerate(questions) if i not in recent_questions]
            
            if available_questions:
                question = random.choice(available_questions)
                question_index = questions.index(question)
            else:
                # Si toutes les questions ont été posées récemment, choisir au hasard
                question = random.choice(questions)
                question_index = questions.index(question)
        
        # Ajouter la question à l'historique
        if question_index not in user_history:
            user_history.append(question_index)
            # Garder seulement les 15 dernières questions dans l'historique
            if len(user_history) > 15:
                user_history.pop(0)
            self.save_scores()
        
        embed = discord.Embed(
            title="🧐 Quiz de Culture Générale",
            description=question["question"],
            color=0x3498DB
        )
        
        options_text = "\n".join(question["options"])
        embed.add_field(name="Options", value=options_text, inline=False)
        embed.set_footer(text="Réagissez avec 🇦, 🇧, 🇨 ou 🇩 pour répondre!")
        
        message = await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        
        reactions = ["🇦", "🇧", "🇨", "🇩"]
        for reaction in reactions:
            await message.add_reaction(reaction)
        
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in reactions and reaction.message == message
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            
            user_answer = ["🇦", "🇧", "🇨", "🇩"].index(str(reaction.emoji))
            user_letter = ["A", "B", "C", "D"][user_answer]
            
            if user_letter == question["correct"]:
                points = 10
                self.add_score(str(interaction.user.id), "quiz", points)
                
                embed = discord.Embed(
                    title="🎉 Correct!",
                    description=f"Bonne réponse! +{points} points",
                    color=0x00FF00
                )
            else:
                embed = discord.Embed(
                    title="❌ Incorrect!",
                    description=f"La bonne réponse était: **{question['correct']}**",
                    color=0xFF0000
                )
            
            embed.add_field(name="💡 Explication", value=question["explanation"], inline=False)
            await interaction.followup.send(embed=embed)
            
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="⏰ Temps écoulé!",
                description=f"La bonne réponse était: **{question['correct']}**",
                color=0xFF9900
            )
            embed.add_field(name="💡 Explication", value=question["explanation"], inline=False)
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="scores", description="🏆 Voir vos scores aux jeux")
    async def scores(self, interaction: discord.Interaction, utilisateur: Optional[discord.Member] = None):
        """Afficher les scores d'un utilisateur"""
        target_user = utilisateur or interaction.user
        user_id = str(target_user.id)
        
        if user_id not in self.user_scores:
            embed = discord.Embed(
                title="🏆 Scores de Jeux",
                description=f"{target_user.mention} n'a pas encore joué!",
                color=0x95A5A6
            )
            await interaction.response.send_message(embed=embed)
            return
        
        user_data = self.user_scores[user_id]
        total_points = sum(user_data.values())
        
        embed = discord.Embed(
            title="🏆 Scores de Jeux",
            description=f"Scores de {target_user.mention}",
            color=0xFFD700
        )
        
        game_names = {
            "deviner_nombre": "🎯 Deviner le Nombre",
            "pierre_papier_ciseaux": "✂️ Pierre-Papier-Ciseaux",
            "memory": "🧠 Jeu de Mémoire",
            "quiz": "🧐 Quiz"
        }
        
        for game, points in user_data.items():
            game_display = game_names.get(game, game.replace("_", " ").title())
            embed.add_field(name=game_display, value=f"**{points}** points", inline=True)
        
        embed.add_field(name="🌟 Total", value=f"**{total_points}** points", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="classement", description="🏅 Voir le classement des joueurs")
    async def leaderboard(self, interaction: discord.Interaction):
        """Afficher le classement des joueurs"""
        if not self.user_scores:
            embed = discord.Embed(
                title="🏅 Classement des Joueurs",
                description="Aucun joueur dans le classement pour le moment!",
                color=0x95A5A6
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Calculer le total de points pour chaque joueur
        player_totals = {}
        for user_id, games in self.user_scores.items():
            total = sum(games.values())
            if total > 0:
                player_totals[user_id] = total
        
        # Trier par points décroissants
        sorted_players = sorted(player_totals.items(), key=lambda x: x[1], reverse=True)
        
        embed = discord.Embed(
            title="🏅 Classement des Joueurs",
            description="Top 10 des meilleurs joueurs",
            color=0xFFD700
        )
        
        medals = ["🥇", "🥈", "🥉"]
        
        for i, (user_id, total_points) in enumerate(sorted_players[:10]):
            try:
                user = self.bot.get_user(int(user_id))
                if user:
                    medal = medals[i] if i < 3 else f"**{i+1}.**"
                    embed.add_field(
                        name=f"{medal} {user.display_name}",
                        value=f"{total_points} points",
                        inline=False
                    )
            except:
                continue
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="say", description="🗣️ Faire parler le bot (discrètement)")
    @app_commands.describe(
        message="Le message que le bot doit dire",
        channel="Canal où envoyer le message (optionnel)"
    )
    async def say_command(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
        """Faire parler le bot sans révéler qui a utilisé la commande"""
        
        # Vérifier que l'utilisateur a les permissions nécessaires
        if not (interaction.user.guild_permissions.manage_messages or 
                interaction.user.guild_permissions.administrator):
            await interaction.response.send_message(
                "❌ Vous devez avoir la permission 'Gérer les messages' pour utiliser cette commande.",
                ephemeral=True
            )
            return
        
        # Limiter la longueur du message
        if len(message) > 2000:
            await interaction.response.send_message(
                "❌ Le message est trop long! Maximum 2000 caractères.",
                ephemeral=True
            )
            return
        
        # Vérifier si le message contient des mentions @ everyone ou @ here
        if "@everyone" in message.lower() or "@here" in message.lower():
            await interaction.response.send_message(
                "❌ Vous ne pouvez pas utiliser @everyone ou @here dans cette commande.",
                ephemeral=True
            )
            return
        
        # Déterminer le canal de destination
        target_channel = channel or interaction.channel
        
        # Vérifier que le bot peut écrire dans ce canal
        if not target_channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(
                f"❌ Je n'ai pas la permission d'écrire dans {target_channel.mention}.",
                ephemeral=True
            )
            return
        
        try:
            # Répondre discrètement à l'utilisateur
            await interaction.response.send_message(
                f"✅ Message envoyé dans {target_channel.mention}!",
                ephemeral=True
            )
            
            # Envoyer le message dans le canal cible
            await target_channel.send(message)
            
            # Log de l'action (pour les modérateurs)
            logger.info(f"Say command used by {interaction.user} ({interaction.user.id}) in {interaction.guild.name}: '{message}' in #{target_channel.name}")
            
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas les permissions nécessaires pour envoyer ce message.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de l'envoi du message: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(name="jeux-aide", description="❓ Aide sur les jeux disponibles")
    async def games_help(self, interaction: discord.Interaction):
        """Aide sur les jeux"""
        embed = discord.Embed(
            title="🎮 Jeux Disponibles",
            description="Voici tous les jeux auxquels vous pouvez jouer!",
            color=0x9932CC
        )
        
        games_info = [
            ("🎯 `/deviner-nombre`", "Devinez un nombre entre 1 et 100\n• 7 tentatives maximum\n• Plus de points si trouvé rapidement"),
            ("✂️ `/pierre-papier-ciseaux`", "Jouez contre le bot\n• 3 points si victoire\n• 1 point si égalité"),
            ("🧠 `/memory`", "Jeu de mémoire avec séquences\n• 10 niveaux progressifs\n• 5 points par niveau réussi"),
            ("🧐 `/quiz`", "Quiz de culture générale\n• **150+ questions** disponibles\n• Sujets très variés\n• Système anti-répétition intelligent\n• 10 points par bonne réponse"),
            ("🏆 `/scores`", "Voir vos scores ou ceux d'un autre joueur"),
            ("🏅 `/classement`", "Voir le top 10 des joueurs"),
            ("🗣️ `/say`", "Faire parler le bot discrètement\n• Nécessite permission 'Gérer les messages'")
        ]
        
        for name, description in games_info:
            embed.add_field(name=name, value=description, inline=False)
        
        embed.set_footer(text="Amusez-vous bien! 🎉")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(GamesCommands(bot))
