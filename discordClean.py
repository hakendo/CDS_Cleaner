import requests
import os
import json
from discord import Embed
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv  # Importa la librería dotenv


# Cargar variables del archivo .env
load_dotenv()

# Token del bot de Discord (asegúrate de mantenerlo seguro y no compartirlo públicamente)
bot_token = os.getenv('TOKEN')

# URL de la API de Albion Online para obtener los miembros de la guild (aquí puedes hacer que también sea parametrizable si lo necesitas)
albion_url = "https://gameinfo.albiononline.com/api/gameinfo/guilds/[id_gremio]/members"

# Inicializar el bot de Discord con los intents necesarios
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Sincronizar los comandos de slash al iniciar el bot
async def sync_commands(guild=None):
    if guild:
        await bot.tree.sync(guild=guild)
    else:
        await bot.tree.sync()
    print("Comandos slash sincronizados correctamente.")

# Obtener la lista de miembros de Discord
def get_discord_members(discord_server_id):
    url = f'https://discord.com/api/v10/guilds/{discord_server_id}/members'
    headers = {
        'Authorization': f'Bot {bot_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'limit': 1000  # Limitar a 1000 miembros por solicitud
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()  # Devolver la lista de miembros en formato JSON
    else:
        print(f"Error al obtener miembros de Discord: {response.status_code}")
        return []

# Obtener la lista de miembros de la API de Albion Online
def get_albion_members(gremio_id):
    response = requests.get(albion_url.replace("[id_gremio]", gremio_id))
    
    if response.status_code == 200:
        return response.json()  # Devolver la lista de miembros en formato JSON
    else:
        print(f"Error al obtener miembros de Albion Online: {response.status_code}")
        return []

# Filtrar y comparar los miembros de Discord con los miembros de Albion Online
def compare_discord_with_albion(discord_members, albion_members, tag):
    # Obtener solo los nombres de los miembros de la API de Albion en minúsculas
    albion_names = [member.get("Name").lower() for member in albion_members if member.get("Name")]

    # Filtrar los miembros de Discord cuyos nicknames contienen el tag en minúsculas
    cds_discord_members = [member for member in discord_members if member.get("nick") and tag in member.get("nick")]

    # Preparar resultados
    result = ""
    for cds_member in cds_discord_members:
        # Eliminar el tag y convertir el nickname a minúsculas
        discord_nickname = cds_member.get("nick").replace(tag, "").strip().lower()
        
        # Comparar el nickname sin el tag en minúsculas con los nombres en Albion Online en minúsculas
        if discord_nickname not in albion_names:
            result += f"'{discord_nickname}' NO existe en el Gremio.\n"
    
    return result

# Función para enviar el contenido en uno o más embeds si es demasiado largo
async def send_large_embed(interaction, content, title="Resultados de la comparación"):
    # Dividimos el contenido en trozos de 2048 caracteres o menos
    chunks = [content[i:i + 2048] for i in range(0, len(content), 2048)]
    
    for i, chunk in enumerate(chunks):
        # Si es el primer chunk, le ponemos el título original. Si no, le añadimos un índice
        embed_title = f"{title} (Parte {i+1})" if i > 0 else title

        embed = Embed(title=embed_title, description=chunk)
        
        # Enviar el embed
        await interaction.followup.send(embed=embed)

# Comando de slash para hacer la comparación
@bot.tree.command(name="validate_members", description="Compara miembros de Discord con los de Albion Online")
@app_commands.describe(discord_server_id="ID del servidor de Discord", tag="Tag para filtrar miembros (por defecto: [CDS])", gremio_id="Identificador del gremio en AlbionOnline. (Por defecto: iFYtpnd8RGSCR_OLZXZzng)")
async def validate_members(interaction: discord.Interaction, discord_server_id: str, tag: str = "[CDS]", gremio_id: str="iFYtpnd8RGSCR_OLZXZzng"):
    # Indicar que el bot está procesando
    await interaction.response.defer()

    # Obtener miembros de Discord y Albion
    discord_members = get_discord_members(discord_server_id)
    albion_members = get_albion_members(gremio_id)
    
    if discord_members and albion_members:
        # Comparar los miembros
        result = compare_discord_with_albion(discord_members, albion_members, tag)
        
        # Enviar el contenido usando embeds
        if result:
            await send_large_embed(interaction, result)
        else:
            await interaction.followup.send("Todos los miembros de Discord están en el gremio de Albion.")
    else:
        await interaction.followup.send("Hubo un problema al obtener los miembros.")

# Inicializar el bot
@bot.event
async def on_ready():
    print(f"Bot {bot.user} conectado exitosamente.")
    # Sincronizar comandos de slash con todos los servidores
    await sync_commands()

# Ejecutar el bot
bot.run(bot_token)
