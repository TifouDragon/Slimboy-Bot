"""
Embed Utilities
Functions for creating Discord embeds for ban list display
"""

import discord
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def create_ban_list_embed(banned_users, page, per_page, guild_name, ban_info=None, search_term=None):
    """
    Create a Discord embed for displaying banned users list

    Args:
        banned_users: List of discord.BanEntry objects
        page: Current page number
        per_page: Number of bans per page
        guild_name: Name of the guild/server
        ban_info: Dictionary with audit log information

    Returns:
        discord.Embed: Formatted embed with ban information
    """

    # Calculate pagination
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    page_bans = banned_users[start_index:end_index]

    total_pages = (len(banned_users) + per_page - 1) // per_page

    # Create embed
    title = "📋 Liste des Bannis du Serveur"
    if search_term and search_term.strip():
        title += f" - Recherche: {search_term}"
        description = f"Résultats de recherche pour **{search_term}** dans **{guild_name}**"
    else:
        description = f"Affichage des utilisateurs bannis de **{guild_name}**"

    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )

    # Add ban entries
    for i, ban_entry in enumerate(page_bans, start=start_index + 1):
        user = ban_entry.user
        reason = ban_entry.reason

        # Format user information with clickable profile picture thumbnail
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        user_info = f"**{user.display_name}** [🖼️]({avatar_url})\n"
        user_info += f"ID: `{user.id}`\n"

        # Add ban reason and moderator info from audit logs
        audit_info = ban_info.get(user.id) if ban_info else None

        if audit_info:
            moderator = audit_info['moderator']
            audit_reason = audit_info['reason']
            ban_timestamp = audit_info['timestamp']

            # Show who banned the user
            if moderator.bot:
                user_info += f"🤖 **Banni par le bot:** {moderator.display_name}\n"
            else:
                user_info += f"👮 **Banni par le modérateur:** {moderator.display_name}\n"

            # Show ban date
            user_info += f"**Date du ban:** {ban_timestamp.strftime('%d/%m/%Y %H:%M')}\n"

            # Show reason from audit log or ban entry
            display_reason = audit_reason or reason
            if display_reason and display_reason.strip():
                user_info += f"**Raison:** {display_reason}\n"
            else:
                user_info += "**Raison:** Aucune raison fournie\n"
        else:
            # Fallback to ban entry reason if no audit log info
            if reason and reason.strip():
                user_info += f"**Raison:** {reason}\n"

                # Try to identify if banned by a bot from reason text
                bot_indicators = {
                    "dyno": "Dyno",
                    "carl-bot": "Carl-bot", 
                    "carl bot": "Carl-bot",
                    "mee6": "MEE6",
                    "ticket tool": "Ticket Tool",
                    "modmail": "ModMail",
                    "automod": "AutoMod",
                    "auto-mod": "AutoMod",
                    "security": "Security Bot",
                    "raid": "Anti-Raid Bot",
                    "anti-raid": "Anti-Raid Bot",
                    "pancake": "Pancake",
                    "groovy": "Groovy",
                    "rythm": "Rythm",
                    "fredboat": "FredBoat",
                    "pokecord": "Pokecord",
                    "mudae": "Mudae",
                    "dank memer": "Dank Memer",
                    "tatsu": "Tatsu",
                    "arcane": "Arcane",
                    "epic rpg": "Epic RPG",
                    "idle miner": "Idle Miner",
                    "reaction": "Reaction Role Bot"
                }

                reason_lower = reason.lower()
                detected_bot = None

                for indicator, bot_name in bot_indicators.items():
                    if indicator in reason_lower:
                        detected_bot = bot_name
                        break

                if detected_bot:
                    user_info += f"🤖 **Probablement banni par:** {detected_bot}\n"
                elif "bot" in reason_lower:
                    user_info += f"🤖 **Probablement banni par:** Un bot\n"
            else:
                user_info += "**Raison:** Aucune raison fournie\n"
                user_info += "⚠️ **Banni par:** Inconnu (pas d'accès aux logs d'audit)\n"

        # Add field to embed
        embed.add_field(
            name=f"{i}. {user.display_name}",
            value=user_info,
            inline=False
        )

    # Add pagination info with watermark
    embed.set_footer(
        text=f"Page {page}/{total_pages} • Total: {len(banned_users)} bannis • Affichage: {len(page_bans)} bannis • Créé par @Ninja Iyed"
    )

    return embed

def create_error_embed(title, description, error_type="error"):
    """
    Create an error embed

    Args:
        title: Error title
        description: Error description
        error_type: Type of error (error, warning, info)

    Returns:
        discord.Embed: Error embed
    """

    colors = {
        "error": discord.Color.red(),
        "warning": discord.Color.orange(),
        "info": discord.Color.blue()
    }

    icons = {
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️"
    }

    embed = discord.Embed(
        title=f"{icons.get(error_type, '❌')} {title}",
        description=description,
        color=colors.get(error_type, discord.Color.red()),
        timestamp=datetime.utcnow()
    )

    return embed

def create_no_bans_embed(guild_name):
    """
    Create embed for when no bans are found

    Args:
        guild_name: Name of the guild/server

    Returns:
        discord.Embed: No bans embed
    """

    embed = discord.Embed(
        title="📋 Liste des Bannis du Serveur",
        description=f"Aucun utilisateur banni trouvé sur **{guild_name}**.\n\n✅ Ce serveur a une liste de bannis propre !",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )

    embed.set_footer(text=f"Serveur: {guild_name} • Créé par @Ninja Iyed")

    return embed