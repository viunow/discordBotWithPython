import discord
import youtube_dl
from discord.ext import commands, tasks
import random
import asyncio

# Variáveis declaradas
# client = commands.Bot(command_prefix = '.')
intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '.', intents = intents)

players = {}

youtube_dl.utils.bug_reports_message = lambda: ''

# Token de acesso do bot, cada bot tem o seu Token próprio. Deve ser privado o Token.
TOKEN = 'Here goes the token access'


# Evento que informa que o bot está online
@client.event
async def on_ready():
    print('Bot is ready.')



# Evento que mostra os comandos suportados pelo bot
@client.command()
async def ajuda(ctx):
    await ctx.send("Lista de comandos atualmente:")
    await ctx.send(".msg = Escrever uma mensagem no chat.\n.ping = Ver o ping do bot.\n.pergunta = Fazer uma pergunta pro bot responder aleatoriamente.")
    # await ctx.send(".ping = Ver o ping do bot.")
    # await ctx.send(".pergunta = Fazer uma pergunta pro bot responder aleatoriamente.")



# Evento quando um membro entra no servidor
@client.event
async def on_member_join(member):
    print(f'{member} está com sede de cachaça e entrou no bar.')



# Evento quando um membro sai do servidor
@client.event
async def on_member_remove(member):
    print(f'{member} foi embora do bar.')    



# .msg para fazer o bot enviar a mensagem como parâmetro
@client.command()
async def msg(ctx, *, arg):
    await ctx.send(arg)



# Evento para mostrar o ping do bot
@client.command()
async def ping(ctx):
    await ctx.send(f'O ping é de {round(client.latency * 1000)}ms')



# Evento que responde uma pergunta, para inserir mais respostas, incluir na variável responses
@client.command()
async def pergunta(ctx, *, question):
    responses = ['Sem dúvidas']
    await ctx.send(random.choice(responses))



# Evento em que o bot fala algo quando é invocado através de .digaalgo
@client.command()
async def digaalgo(ctx):
    responses2 = ['Eu sobrevivo assim, por mal de se trazer as maldições dos próprios que se merecem.', 'Se tem que se fazer, tem que se fazer com a própria pessoa que se merece isso, não com a vida inocente.', 'Vida para o resto da sua vida..']
    await ctx.send(random.choice(responses2))

# Comando que dá join no server
@client.command(name='play', help='Esse comando dá play na música')
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send('Você não está num canal de voz')
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' %e) if e else None)

    await ctx.send(f'**Tocando agora: ** {player.title}')

# Comando que sai do server
@client.command(name='stop', help='Esse comando para a reprodução da música')
async def stop(ctx):
    # channel = ctx.message.author.voice.channel
    # await channel.disconnect()

    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()


#---------------------------------------------------------------| MUSIC CODE |--------------------------------------------------------------------------------------------------#
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
client.run(TOKEN)

