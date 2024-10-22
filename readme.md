# CDS_Cleaner [![](https://cdn.jsdelivr.net/gh/sindresorhus/awesome@d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome#readme)
> Aplicación destinada a la gestión de miembros de gremio en Albion online y Discord
# Introduccion 
Al ser un codigo nuevo, se espera implementar mejoras dependiendo de las necesidades de las alianzas en Albion Online.
Se deja el código abierto para su uso.

## Requisitos para funcionamiento
# Instalacion en Discord
[Instalación de App en discord](https://discord.com/oauth2/authorize?client_id=1298142956863226029&permissions=3072&integration_type=0&scope=bot)

# Python
El código y su lógica está hecha con Python, a continuación se detallan las librerias utilizadas.
1.	sudo apt install python3-pip
2.	pip install python-dotenv
3.	pip install requests
4.	pip install discord.py
5.  pip install discord-py-slash-command

## ⚡️ Environment Variables
Nombres de variables de entorno, para su uso.
`TOKEN`


## ⚡️ Comandos actuales
> /validate_members discord_server_id(Id del servidor de discord) tag(Tag de members del gremio ej: [CDS]) gremio_id(El id del gremio en albion)

El gremio id lo puedes obtener por la API de albion (ejemplo: https://gameinfo.albiononline.com/api/gameinfo/search?q=Hakendo), identificando el campo "GuildId"



# Contribute
Para poder contribuir, usted debera copiar el repositorio desde la main hacia una nueva rama y realizar el PR correspondiente.
