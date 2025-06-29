
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
        questions = [
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
                "question": "Quel est l'élément chimique avec le symbole 'O'?",
                "options": ["A) Or", "B) Oxygène", "C) Osmium", "D) Olivier"],
                "correct": "B",
                "explanation": "O est le symbole de l'oxygène dans le tableau périodique."
            },
            {
                "question": "En quelle année a été créé Discord?",
                "options": ["A) 2013", "B) 2014", "C) 2015", "D) 2016"],
                "correct": "C",
                "explanation": "Discord a été lancé en mai 2015."
            },
            {
                "question": "Quel est le plus grand océan du monde?",
                "options": ["A) Atlantique", "B) Indien", "C) Arctique", "D) Pacifique"],
                "correct": "D",
                "explanation": "L'océan Pacifique couvre environ 46% de la surface océanique mondiale."
            }
        ]
        
        question = random.choice(questions)
        
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
            ("🧐 `/quiz`", "Quiz de culture générale\n• Questions aléatoires\n• 10 points par bonne réponse"),
            ("🏆 `/scores`", "Voir vos scores ou ceux d'un autre joueur"),
            ("🏅 `/classement`", "Voir le top 10 des joueurs")
        ]
        
        for name, description in games_info:
            embed.add_field(name=name, value=description, inline=False)
        
        embed.set_footer(text="Amusez-vous bien! 🎉")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(GamesCommands(bot))
