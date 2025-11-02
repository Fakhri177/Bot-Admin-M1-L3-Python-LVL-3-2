import discord
from discord.ext import commands
from config import token  # Import the bot's token from configuration file

intents = discord.Intents.default()
intents.members = True  # Allows the bot to work with users and ban them
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    # Mengirim pesan ucapan selamat
    for channel in member.guild.text_channels:
        await channel.send(f'Selamat datang, {member.mention}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "https://" in message.content or "http://" in message.content:
        # Simpan data pengguna yang mengirim link
        user_info = f"Pengguna: {message.author} (ID: {message.author.id})\nPesan: {message.content}"
        print (f"TERDETEKSI LINK:\n {user_info}")

        # Kirim pemberitahuan di channel
        await message.channel.send(f"⚠️ {message.author.mention} mengirim tautan dan akan diblokir!")

        # Hapus pesan yang mengandung link
        await message.delete()

        # Blokir pengguna
        try:
            await message.author.ban(reason="Mengirim tautan di server.")
            print(f"{message.author} telah diblokir.")
        except discord.Forbidden:
            await message.channel.send("❌ Bot tidak memiliki izin untuk memblokir pengguna ini.")
        except Exception as e:
            await message.channel.send(f"Terjadi kesalahan: {e}")

    else:
        # Jika tidak ada link, bisa lanjut ke command lain (wajib agar command lain tetap jalan)
        await bot.process_commands(message)


@bot.command()
async def info(ctx):
    await ctx.send("Hi! I'm a chat manager bot!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("It is not possible to ban a user with equal or higher rank!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"User {member.name} was banned.")
    else:
        await ctx.send("This command should point to the user you want to ban. For example: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have sufficient permissions to execute this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found.")

bot.run(token)