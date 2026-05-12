import discord
from discord.ext import commands
import os
import aiohttp      # بۆ کوماندا steal و وێنەیان پێدڤییە
import asyncio      # بۆ کومانداێن remind و کاتژمێران پێدڤییە
import random       # بۆ کومانداێن flip و joke و یارییان پێدڤییە
import datetime     # بۆ کومانداێن stats و ئەنجامێن کاتژمێری پێدڤییە

# ئەڤە ژی بۆ ناساندنا بۆتی و Prefix (نیشانە) یە
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='^', intents=intents)

# ل ڤێرە دشێی دەست ب نڤیسینا کوماندا بکەی...

# --- ئامادەکرنا تۆکنێ ---
# ل سەر Hugging Face دێ ژ بەشێ Secrets وەرگریت
TOKEN = os.environ.get('TOKEN')

# ئەگەر ل سەر کۆمپیوتەری بی و TOKEN نەبوو، ڤێ تۆکنێ ب کار دئینیت
if not TOKEN:
    TOKEN = 'MTQ4NTc0Mzk2OTMxNTg0ODIzOQ.GZ9Q33.KKDn7fIkHkE5IWLK3AjmkWqm7ERh19YXW_Wic8'

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 

bot = commands.Bot(command_prefix='^', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------ REALONES BOT IS ONLINE 24/7 ------')

    #11111
    
    
    # ١ # --- [ڕێکخستنا سەرەکی] ---
STAFF_ROLE_ID = 1462582644956205086 
STAFF_ROLE_ID = 1465553167868629126
LOG_CHANNEL_ID = 1486828183968940052
# لینکێ وێنەیێ تە ل ڤێرە دانی
LOGO_URL = "https://media.discordapp.net/attachments/1461000548764487802/1466427093247201382/Snapchat-570505887.jpg?ex=69c68827&is=69c536a7&hm=a7f9948354e3ea4fad88d65438b470e54d44d529c2a0995f2ed30834e52ee2e6&=&format=webp&width=1005&height=1005" 

# 1.# --- [ڕێکخستنا سەرەکی - ئەڤان بگۆهۆڕە] ---

STAFF_ROLE_ID = 1462582644956205086
LOG_CHANNEL_ID = 1364674414091698176
LOGO_URL = "https://media.discordapp.net/attachments/1461000548764487802/1466427093247201382/Snapchat-570505887.jpg?ex=69c68827&is=69c536a7&hm=a7f9948354e3ea4fad88d65438b470e54d44d529c2a0995f2ed30834e52ee2e6&=&format=webp&width=1005&height=1005" # لینکێ وێنەیێ REAL ONES لێرە دانی

# 1. کلاسا پشتراستکرنا گرتنا تیکێتێ (Confirm Close)
class ConfirmCloseView(discord.ui.View):
    def __init__(self, opener_id):
        super().__init__(timeout=None)
        self.opener_id = opener_id

    @discord.ui.button(label="Close Ticket 🔒", style=discord.ButtonStyle.danger, custom_id="confirm_close_now")
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
        if (staff_role and staff_role in interaction.user.roles) or interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("ئەڤ تیکێتە دێ هێتە گرتن د چەند چرکەکان دا...")
            
            log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                log_embed = discord.Embed(title="Ticket Closed 🔒", color=0xFF0000, timestamp=datetime.now())
                log_embed.add_field(name="Opened By", value=f"<@{self.opener_id}>", inline=True)
                log_embed.add_field(name="Closed By", value=interaction.user.mention, inline=True)
                await log_channel.send(embed=log_embed)

            await asyncio.sleep(3)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("ب تنێ ستاف و ئەدمین دشێن ڤێ کارێ بکەن!", ephemeral=True)

# 2. کلاسا دوگمەیێن ناڤ تیکێتێ (Claim & Close)
class TicketActions(discord.ui.View):
    def __init__(self, opener_id):
        super().__init__(timeout=None)
        self.opener_id = opener_id

    @discord.ui.button(label="Close Ticket 🔒", style=discord.ButtonStyle.danger, custom_id="req_close")
    async def close_request(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
        if (staff_role and staff_role in interaction.user.roles) or interaction.user.guild_permissions.administrator:
            embed = discord.Embed(description="تکایە ل سەر دوگمەیا خوارێ لێبدە بۆ گرتنا تیکێتێ.", color=0xFF0000)
            await interaction.response.send_message(embed=embed, view=ConfirmCloseView(self.opener_id))
        else:
            await interaction.response.send_message("ب تنێ ستاف دشێن تیکێتێ بگرن!", ephemeral=True)

    @discord.ui.button(label="Claim Ticket 📜", style=discord.ButtonStyle.secondary, custom_id="claim_task")
    async def claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff_role = interaction.guild.get_role(STAFF_ROLE_ID)
        if (staff_role and staff_role in interaction.user.roles) or interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(f"ئەڤ تیکێتە ژ لایێ {interaction.user.mention} هاتە وەرگرتن. ✅")
            button.disabled = True
            button.label = "Claimed ✅"
            await interaction.message.edit(view=self)
        else:
            await interaction.response.send_message("ب تنێ ستاف دشێن تیکێتێ وەرگرن!", ephemeral=True)

# 3. کلاسا دەسپێکێ (Apply Ticket Launcher)
class TicketLauncher(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="APPLY TICKET 🎫", style=discord.ButtonStyle.danger, custom_id="main_launcher")
    async def ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # بکارئینانا defer بۆ رێگریکردن ل خەلەتییا Interaction Error
        await interaction.response.defer(ephemeral=True)
        
        guild = interaction.guild
        user = interaction.user
        staff_role = guild.get_role(STAFF_ROLE_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True)

        channel = await guild.create_text_channel(name=f"ticket-{user.name}", overwrites=overwrites)
        await interaction.followup.send(f"تیکێت بۆ تە هاتە ڤەکرن: {channel.mention}", ephemeral=True)

        embed = discord.Embed(title="Ticket Opened", description=f"{user.mention} created a ticket. 🎟️", color=0xFFD700)
        embed.set_footer(text="REALONES System | /close")
        await channel.send(content=f"{user.mention}", embed=embed, view=TicketActions(user.id))

# --- [بۆت] ---
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='^', intents=intents)

    async def setup_hook(self):
        # ئەڤە بۆ هندێ یە کو دوگمە هەمی دەمان کار بکەن (Persistent Views)
        self.add_view(TicketLauncher())

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------ REALONES BOT IS ONLINE ------')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    embed = discord.Embed(
        title="RealOne Ticket 🎫",
        description="**HELP & SUPPORT**\n\nBU HAR TSHTAKE\nTICKET APPLY KA ✅",
        color=0xFF0000
    )
    embed.set_image(url=LOGO_URL) 
    await ctx.send(embed=embed, view=TicketLauncher())

# 1. Hello Command
@bot.command()
async def hello(ctx):
    await ctx.send('Hello! I am REALONES bot. I am online 24/7 now!')

# 2. Kick ban unban Command
# --- ١. کوماندا Ban ب ڕێکا ID یان Mention ---
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *, reason="hiii"):
    try:
        await ctx.message.delete()
        
        # ١. پشکنین کا ئایا ئەڤ کەسە بەری نوکە یێ باندکرییە یان نە
        is_banned = False
        async for entry in ctx.guild.bans():
            if entry.user.id == user.id:
                is_banned = True
                break
        
        if is_banned:
            already_banned_embed = discord.Embed(
                title="⚠️ ئاگاداری",
                description=f"{user.mention} بەری نوکە یێ هاتییە باندکرن! نکارم جارەکا دی باند بکەم.",
                color=0xf1c40f # ڕەنگێ زەرد
            )
            return await ctx.send(embed=already_banned_embed)

        # ٢. ئەگەر یێ باندکری نەبوو، باند بکە
        await ctx.guild.ban(user, reason=reason)

        embed = discord.Embed(title="⛔ ئەندام هاتە باندکرن", color=0xff0000, timestamp=datetime.datetime.now())
        embed.add_field(name="👤 کەسێ باندبووی:", value=f"{user.mention} (`{user.id}`)", inline=False)
        embed.add_field(name="📝 هوکار:", value=f"`{reason}`", inline=False)
        embed.add_field(name="👮 ژ لایێ ئەدمین:", value=f"{ctx.author.mention}", inline=False)
        embed.set_thumbnail(url=user.display_avatar.url)
        await ctx.send(embed=embed)

    except Exception as e:
        error_embed = discord.Embed(
            title="❌ خەلەتی د باندکرنێ دا",
            description=f"نەشێم {user.mention} باند بکەم.\n**ئەڕۆڕ:** `{str(e)}`",
            color=0xff0000
        )
        await ctx.send(embed=error_embed)

# --- ٢. کوماندا Kick ب ڕێکا ID یان Mention ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *, reason="hiii"):
    try:
        await ctx.message.delete()
        await ctx.guild.kick(user, reason=reason)

        embed = discord.Embed(title="👢 ئەندام هاتە دەرخستن", color=0xf1c40f, timestamp=datetime.datetime.now())
        embed.add_field(name="👤 کەسێ دەرکەفتی:", value=f"{user.mention} (`{user.id}`)", inline=False)
        embed.add_field(name="📝 هوکار:", value=f"`{reason}`", inline=False)
        embed.add_field(name="👮 ژ لایێ ئەدمین:", value=f"{ctx.author.mention}", inline=False) # دێ چیتە بن هوکاری
        embed.set_thumbnail(url=user.display_avatar.url)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ کێشەیەک چێبوو: {e}", delete_after=5)

# --- ٣. کوماندا Unban ب ڕێکا ID ---
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: str): # مە کرە سترینگ دا ئەڕۆڕا ئایدی نەمینیت
    try:
        # ١. سڕینا نامەیا کوماندا تە
        await ctx.message.delete()

        # ٢. پەیداکرنا بەکارهێنەری
        user = await bot.fetch_user(int(user_id))
        
        # ٣. لادانا باندی
        await ctx.guild.unban(user)

        # ئیمبێدا سەرکەفتنێ
        embed = discord.Embed(
            title="✅ ئەندام هاتە ئازادکرن",
            color=0x2ecc71,
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="👤 کەسێ ئازادبووی:", value=f"{user.mention} (`{user.id}`)", inline=False)
        embed.add_field(name="👮 ژ لایێ ئەدمین:", value=f"{ctx.author.mention}", inline=False)
        embed.set_thumbnail(url=user.display_avatar.url)
        
        await ctx.send(embed=embed)

    except Exception as e:
        # ئیمبێدا خەلەتیێ (دێ مینیت)
        error_embed = discord.Embed(
            title="❌ کێشەیەک چێبوو د Unban دا",
            description=f"ئەو ئایدییا تە دایە `{user_id}` نەهاتە دیتن یان یێ باندکری نینە.\n\n**ئەڕۆڕ:** `{str(e)}`",
            color=0xff0000
        )
        await ctx.send(embed=error_embed)

# 3. counting 

# 5. Clear Command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'🧹 Deleted {amount} messages.', delete_after=5)

# 6. Send Private Message (DM)
@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, user: discord.User, *, message):
    try:
        await user.send(f"**Message from {ctx.guild.name}:**\n{message}")
        await ctx.send(f"✅ Message sent to {user.mention} privately.")
    except:
        await ctx.send("❌ I couldn't send a DM to this user.")

# 7.Timeout Command 
@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, user_id: int, minutes: int):
    try:
        user = await ctx.guild.fetch_member(user_id)
        duration = datetime.timedelta(minutes=minutes)
        await user.timeout(duration)
        await ctx.send(f"✅ User {user.mention} has been timed out for {minutes} minutes.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

# 8.Untimeout Command 
# @bot.command()
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, user_id: int):
    try:
        user = await ctx.guild.fetch_member(user_id)
        await user.timeout(None)
        await ctx.send(f"✅ Timeout removed for {user.mention}.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

 # 9.Server info 
 # @bot.command()
async def server(ctx):
    name = str(ctx.guild.name)
    member_count = str(ctx.guild.member_count)
    await ctx.send(f"✅ Server Name: {name}\n👥 Total Members: {member_count}")

# 10.Lock Channel
@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    # ئەڤە دێ رۆلێ @everyone ل ناڤ سێرڤەری دۆزیتەڤە
    everyone = ctx.guild.default_role
    # ئەڤە دێ دەستهەلاتا نامە ناردنێ ل وی کەناڵی کەتە False
    await ctx.channel.set_permissions(everyone, send_messages=False)
    await ctx.send("🔒 This channel has been locked.")

# 11.Unlock Channel
@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Channel has been unlocked.")

# 12.USER INFO 
@bot.command()
async def whois(ctx, user_id: int):
    try:
        user = await ctx.guild.fetch_member(user_id)
        roles = [role.mention for role in user.roles[1:]] # @everyone ناگریت
        await ctx.send(f"👤 **User:** {user.mention}\n🆔 **ID:** {user.id}\n📅 **Joined:** {user.joined_at.strftime('%Y-%m-%d')}\n🎭 **Roles:** {' '.join(roles) if roles else 'None'}")
    except:
        await ctx.send("❌ Error: User not found in this server.")

# 13.Clear User
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearuser(ctx, user_id: int, amount: int = 10):
    def is_user(m):
        return m.author.id == user_id
        
    deleted = await ctx.channel.purge(limit=amount, check=is_user)
    await ctx.send(f"✅ Deleted {len(deleted)} messages from {user_id}.", delete_after=5)

# 14.Old Name
@bot.command()
async def oldname(ctx, user_id: int):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.send(f"📌 The global name for this ID is: **{user.name}**")
    except Exception:
        await ctx.send("❌ Error: Could not find any user with this ID.")

# 15.Server Icon
@bot.command()
async def icon(ctx):
    if ctx.guild.icon:
        await ctx.send(f"🖼️ Server Icon:\n{ctx.guild.icon.url}")
    else:
        await ctx.send("❌ This server has no icon.")

# 16.Say 
@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message: str):
    await ctx.message.delete() # ناما تە ژێدبەت دا کو بتنێ یا بۆتی بمینیت
    await ctx.send(message)
# 17.Role list 
@bot.command()
async def roles(ctx):
    role_list = [role.name for role in ctx.guild.roles if role.name != "@everyone"]
    await ctx.send(f"🎭 **Server Roles ({len(role_list)}):**\n{', '.join(role_list)}")

# 18. Announce Command
@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, url: str, *, message: str):
    # ژێبرنا نامەیا تە دا کو تەنێ یا بۆتی بمینیت
    try:
        await ctx.message.delete()
    except:
        pass

    # دروستکرنا قالبه‌كێ پاقژ و فەرمی
    embed = discord.Embed(
        description=message, # ل ڤێرە نامەیا تە ب دلێ تە دەرکەڤیت
        color=0x2f3136 # ڕەنگێ تارێ فەرمی یێ دیسکۆردێ
    )
    
    # دانانا وێنەی (لینکێ وێنەی دێ ون بیت و تەنێ وێنە دێ مینیت)
    embed.set_image(url=url)
    
    # ناردنا نامەیێ دگەل @everyone
    await ctx.send(content="@everyone", embed=embed)

# 19.Onlinee Member
@bot.command()
async def online(ctx):
    online_count = len([m for m in ctx.guild.members if m.status != discord.Status.offline])
    await ctx.send(f"🟢 Members Online: **{online_count}**")

# 20.Poll
@bot.command()
async def poll(ctx, *, question: str):
    message = await ctx.send(f"📊 **POLL:** {question}")
    await message.add_reaction("✅")
    await message.add_reaction("❌")


# 21.Alert 
@bot.command()
@commands.has_permissions(manage_messages=True)
async def alert(ctx, user_id: int, *, message: str = "Please check the server!"):
    try:
        user = await bot.fetch_user(user_id)
        # دروستکرنا نامەکا جوان بۆ DM
        alert_msg = (
            f"⚠️ **URGENT ALERT FROM {ctx.guild.name}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **From Admin:** {user.mention}\n"
            f"📝 **Message:** {message}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👉 Please return to the server immediately!"
        )
        await user.send(alert_msg)
        await ctx.send(f"✅ Alert successfully sent to {user.mention}.")
    except Exception:
        await ctx.send(f"❌ Could not send alert to <@{user_id}>. (DMs are closed)")
# 22.Clear All
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearall(ctx, amount: int = 100):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"🧹 Cleared {amount} messages!", delete_after=5)


# 23. Warn Command
# --- [⚠️ REALONES WARNING SYSTEM - FINAL VERSION] ---

# ئایدییێن رۆلان ل ڤێرە دابنێ
WARN_ROLE_ID = 1488661667100233902  # ئایدییا رۆلێ Warned
STAFF_ROLE_ID = 1462582644956205086 # ئایدییا ئەو رۆلێ دشێت وارنینگێ بدەت

@bot.command(name="warn")
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    """کوماندایێ وارنینگێ ب ئایدی یان تاگ دگەل ئۆتۆ رۆل و نامەیا تایبەت"""
    
    # 1. پشکنینا دەستوورێ ستافی (ئەگەر ستاف بیت یان ئەدمین)
    staff_role = ctx.guild.get_role(STAFF_ROLE_ID)
    is_staff = staff_role in ctx.author.roles if staff_role else False
    is_admin = ctx.author.guild_permissions.administrator

    if not is_staff and not is_admin:
        return await ctx.send("❌ **تو دەستیر دای نینی ڤێ کوماندێ ب کار بینی!**")

    # 2. زێدەکرنا رۆلێ وارنینگێ ب ئۆتۆماتیکی
    warn_role = ctx.guild.get_role(WARN_ROLE_ID)
    if warn_role:
        try:
            await member.add_roles(warn_role)
        except Exception as e:
            print(f"Error adding role: {e}")
            await ctx.send("⚠️ **من نەشیا رۆلێ وارنینگێ بدەمە ئەندامی (رۆلێ بۆتی یێ نزمە)!**")
    else:
        return await ctx.send("❌ **ئایدییا رۆلێ وارنینگێ خەلەتە، ل ناو کۆدی چاک بکە!**")

    # 3. دروستکرنا Embed بۆ ناو سێرڤەرێ (وەک وێنەیێ تە دڤێت)
    server_embed = discord.Embed(title="⚠️ WARNING", color=0xe74c3c)
    server_embed.description = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
    server_embed.add_field(name="👤 User:", value=f"{member.mention} (`{member.id}`)", inline=False)
    server_embed.add_field(name="📝 Reason:", value=f"```{reason}```", inline=False)
    server_embed.add_field(name="🛡️ Staff:", value=ctx.author.mention, inline=False)
    server_embed.set_thumbnail(url=member.display_avatar.url)
    server_embed.set_footer(text="REALONES FAMILY PROTECTION", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
    
    await ctx.send(embed=server_embed)

    # 4. دروستکرنا Embed بۆ ناو DM (نامەیا تایبەت بۆ ئەندامی)
    try:
        dm_embed = discord.Embed(
            title="⚠️ ئاگەهدارییا وارنینگێ | REALONES",
            description=(
                f"سڵاڤ {member.name}، تە وارنینگەک وەرگرت ل سێرڤەرێ **{ctx.guild.name}**\n\n"
                f"**📝 ئەگەر (Reason):**\n`{reason}`\n\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                "تکایە یاسایێن سێرڤەری بپارێزە دا کو تووشی سزادانا گرانتر نەبی."
            ),
            color=0xe74c3c
        )
        # وێنەیێ مافیا بۆ ناو DM
        dm_embed.set_image(url="https://i.postimg.cc/mD8D1Vj6/godfather.jpg")
        dm_embed.set_footer(text="REALONES FAMILY SYSTEM")
        
        await member.send(embed=dm_embed)
    except discord.Forbidden:
        await ctx.send(f"⚠️ **ئاگەهداری:** {member.mention} نامەیێن تایبەت (DM) گرتینە، نامە بۆ نەچوو بەس وارنینگ وەرگرت.")

# --- [پشتراست بە ئەڤ دێڕە ل دوماهیکا on_message هەبیت] ---
# await bot.process_commands(message)

# 25.ticket
@bot.command()
async def ticket(ctx, *, reason: str = "Support"):
    # دروستکرنا کەناڵەکێ نوو یێ ڤەشارتی
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    channel = await ctx.guild.create_text_channel(name=f"ticket-{ctx.author.name}", overwrites=overwrites)
    await channel.send(f"📩 **New Ticket Created!**\n👤 **User:** {ctx.author.mention}\n📝 **Reason:** {reason}\nAdmin will help you soon.")
    await ctx.send(f"✅ Ticket created here: {channel.mention}")

# 26.close ticket
@bot.command()
@commands.has_permissions(manage_channels=True)
async def close(ctx):
    await ctx.send("🔒 **Closing ticket in 5 seconds...**")
    import asyncio
    await asyncio.sleep(5)
    await ctx.channel.delete()

# 27.Server Mute (speakstop)
@bot.command()
@commands.has_permissions(mute_members=True)
async def speakstop(ctx):
    vc = ctx.author.voice.channel
    for member in vc.members:
        if not member.guild_permissions.administrator:
            await member.edit(mute=True)
    await ctx.send(f"🔇 Everyone in **{vc.name}** has been muted.")

@bot.command()
@commands.has_permissions(mute_members=True)
async def speakstart(ctx):
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=False)
    await ctx.send(f"🔊 Everyone in **{vc.name}** is unmuted.")

# 28.spam 
from collections import defaultdict
user_messages = defaultdict(list)

@bot.event
async def on_message(message):
    if message.author.bot: return
    
    now = discord.utils.utcnow().timestamp()
    user_messages[message.author.id].append(now)
    
    # ئەگەر پتر ژ ٥ نامان د ٥ کێلەکا دا بنێرێت
    user_messages[message.author.id] = [t for t in user_messages[message.author.id] if now - t < 5]
    
    if len(user_messages[message.author.id]) > 2:
        await message.delete()
        await message.channel.send(f"🚫 {message.author.mention}, slow down! No spamming.", delete_after=3)
    
    await bot.process_commands(message)

# 29.Jail
@bot.command()
@commands.has_permissions(manage_roles=True)
async def jail(ctx, member: discord.Member):
    if member.guild_permissions.administrator:
        return await ctx.send("❌ تو نەشی ئەدمینەکی زیندان بکەی!")

    # گوهۆڕینا دەستهەلاتان د هەمی کەناڵان دا
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(member, 
                send_messages=False, 
                connect=False, 
                add_reactions=False, 
                view_channel=False # ئەگەر تە ڤیا چ کەناڵان نەبینیت
            )
        except:
            continue
            
    await ctx.send(f"⛓️ **{member.display_name}** ب سەرکەفتی هاتە زیندانکرن ل هەمی کەناڵان!")

 # 30.unjail
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unjail(ctx, member: discord.Member):
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(member, overwrite=None)
        except:
            continue
            
    await ctx.send(f"🔓 **{member.display_name}** هاتە ئازادکرن و دەستهەلاتێن وی زڤڕینەڤە.")

# 31.Slowmode
@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"🐢 Slowmode هاتە چالاککرن بۆ {seconds} چرکە.")

# 32.steal emoji
@bot.command()
@commands.has_permissions(manage_emojis=True)
async def steal(ctx, emoji: discord.PartialEmoji, *, name=None):
    # ئەگەر ناڤەکێ تایبەت نەدەیتێ، دێ هەمان ناڤێ ئەسلی یێ ئیمۆجی وەرگریت
    if not name:
        name = emoji.name
    
    try:
        # وەرگرتنا وێنەیێ ئیمۆجی ژ سێرڤەرێ دی
        async with aiohttp.ClientSession() as session:
            async with session.get(emoji.url) as resp:
                if resp.status != 200:
                    return await ctx.send("❌ نەشێم وێنەیێ ئیمۆجی وەرگرم.")
                img = await resp.read()
        
        # دروستکرنا ئیمۆجیێ نوو ل سێرڤەرێ تە
        new_emoji = await ctx.guild.create_custom_emoji(name=name, image=img)
        
        embed = discord.Embed(
            title="✅ ئیمۆجی ب سەرکەفتی هاتە زێدە کرن!",
            description=f"ئیمۆجیێ نوو: {new_emoji}\nناڤێ وی: **{name}**",
            color=0x00ffcc
        )
        await ctx.send(embed=embed)
        
    except discord.Forbidden:
        await ctx.send("❌ دەستھەلاتا من نینە ئیمۆجییان زێدە بکەم.")
    except Exception as e:
        await ctx.send(f"❌ کێشەیەک چێبوو: {e}")

# 32.help
@bot.command()
async def helpme(ctx):
    embed = discord.Embed(
        title="📜 REALONES BOT COMMANDS",
        description="لیستا هەمی کومانداێن بۆتی ب شێوەیەکێ رێکخستی:",
        color=0x0055ff
    )
    
    embed.add_field(name="🛡️ Moderation", value="`^kick`, `^ban`, `^warn`, `^mute`, `^clear`, `^nuke`, `^lock`", inline=False)
    embed.add_field(name="⚙️ Admin Tools", value="`^announce`, `^slowmode`, `^say`, `^steal`, `^giveaway`", inline=False)
    embed.add_field(name="👤 General", value="`^avatar`, `^user`, `^server`, `^poll`, `^online`, `^roles`", inline=False)
    embed.add_field(name="⛓️ Jail System", value="`^jail`, `^unjail`", inline=False)
    
    embed.set_footer(text="Developed for REALONES Family")
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    
    await ctx.send(embed=embed)
# 33.clearweb
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearweb(ctx, amount: int = 20):
    def is_link(m):
        return "http" in m.content.lower() or "discord.gg" in m.content.lower()
    
    deleted = await ctx.channel.purge(limit=amount, check=is_link)
    await ctx.send(f"🧹 {len(deleted)} نامێن لینک تێدا هاتنە سڕینەڤە.", delete_after=5)
# 34.EmbedImage
#  @bot.command()
@commands.has_permissions(manage_messages=True)
async def imgembed(ctx, url, *, title="REALONES ANNOUNCEMENT"):
    await ctx.message.delete()
    
    embed = discord.Embed(title=title, color=0x0055ff)
    embed.set_image(url=url)
    embed.set_footer(text=f"By: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
    
    await ctx.send(embed=embed)

# 35 auto spowner
@bot.event
async def on_message(message):
    # ناهێلیت بۆت بەرسڤا خۆ بدەت
    if message.author.bot:
        return

    # --- تنظیمات ---
    TRIGGER_WORD = "reklam" # ئەو پەیڤا تە دڤێت
    ROLE_ID = 1462582644956205086 # ئایدییا رۆلێ Admin یان Staff
    CHANNEL_ID = 1364674414091698176 # ئایدییا وی کەناڵێ تە دڤێت کوماندا تێدا کار بکەت

    # پشکنین: ئەرێ نامە ل وی کەناڵی هاتینە و پەیڤ تێدا هەبوو؟
    if message.channel.id == CHANNEL_ID:
        if TRIGGER_WORD in message.content.lower():
            embed = discord.Embed(
                description=f" {message.author.mention} ل نێزیکترین دەم بەرسڤا تە دێ هێتە دان ژ لایێ ستافی ڤە.:white_check_mark:",
                color=0xff0000
            )
            # ناردنا نامەیێ دگەل تاگێ رۆلی
            await message.channel.send(content=f"<@&{ROLE_ID}>", embed=embed)
            
            # ئەگەر تە ڤیا نامەیا وی کەسی ژێببەی:
            # await message.delete()

    # ئەڤ دێڕە گەلەک گرنگە دا کومانداێن دی نەوەستن
    await bot.process_commands(message)

# 36 welcome 
invites = {}

@bot.event
async def on_ready():
    # پاشەکەفتکرنا هەمی لینکێن دەعوەتێ دەمێ بۆت ئۆنلاین دبیت
    for guild in bot.guilds:
        try:
            invites[guild.id] = await guild.invites()
        except:
            pass
    print(f"Logged in as {bot.user}")

def find_invite_by_code(invite_list, code):
    for inv in invite_list:
        if inv.code == code:
            return inv
    return None

@bot.event
async def on_member_join(member):
    guild = member.guild
    invites_before = invites.get(guild.id)
    invites_after = await guild.invites()
    
    inviter = "Unknown"
    invite_uses = "0"
    
    # دیتنا وی کەسێ ئەڤ ئەندامە دەعوەتکری
    for invite in invites_before:
        new_invite = find_invite_by_code(invites_after, invite.code)
        if new_invite and invite.uses < new_invite.uses:
            inviter = invite.inviter # ئەڤە ئەو کەسە یێ دەعوەت کری
            invite_uses = new_invite.uses
            break
            
    # نووکرنا لیستا دەعوەتان
    invites[guild.id] = invites_after


    # دروستکرنا ئەو Embed وەک وێنەیێ تە ناردووی
    embed = discord.Embed(
        title="New Member Invited",
        description=f"Welcome {member.mention} 👋,\n\nYou were invited by **{inviter}**, who now has NaN invites!",
        color=0xff4500 # ڕەنگێ پرتەقالی وەک یێ وێنەی
    )
    

    # ئەڤە هەمی ڕستێن تە داخوازکرین د ناڤ یەک پشک دا
    quotes_value = (
        "\"🔥 A new legend has arrived!\",\n"
        "\"🎮 Get ready to dominate!\",\n"
        "\"💀 Another warrior joins the squad!\",\n"
        "\"🚀 Welcome to the chaos!\""
    )
    
    embed.add_field(name="", value=quotes_value, inline=False)
    
    # 3. بەشێ کاتێ هاتنێ (Joined At) ڕێک وەک وێنەی
    now = datetime.datetime.now(datetime.timezone.utc)
    formatted_time = now.strftime("%a %b %d %Y %H:%M:%S GMT+0000")
    join_value = f"{formatted_time}\n(Coordinated Universal Time)"
    embed.add_field(name="Joined At", value=join_value, inline=False)

    # زێدەکرنا ژمارەیا ئەندامان
    embed.add_field(name="Member Count", value=f"You are member #{len(guild.members)}", inline=False)
    
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1459722705904599074/1496259942699765860/r1_mix.png?ex=69e93c29&is=69e7eaa9&hm=c8d54cbfe359de5926013ec4500a8a84ea2a500e440c6c79f9e9819dedc24cb3&") # وێنەیێ مەزن
    embed.set_footer(text="Welcome to the server, enjoy your stay!")

    # بنێرە بۆ ئەو چەناڵێ تو دخوازی (ID چەناڵی لێرە دابنێ)
    channel = bot.get_channel(1361724782458175629) # لێرە ID چەناڵی بگوهۆڕە
    if channel:
        await channel.send(embed=embed)

  # 38.giveway

         
# 39.giveamay2
# # --- 1. پەنجەرەیا پێشبینیێ (Modal) ---
class PredictionModal(discord.ui.Modal, title=' :gift: بەریکانە'):
    score = discord.ui.TextInput(
        label='پێشبینیا تە چیە؟',
        placeholder='پێشبینیا خو بنڤێسە',
        required=True,
        min_length=2,
        max_length=50
    )

    def __init__(self, participants, log_id, target_time):
        super().__init__()
        self.participants = participants
        self.log_id = log_id
        self.target_time = target_time

    async def on_submit(self, interaction: discord.Interaction):
        # پشکنینا کاتی: ئەگەر کاتێ نوکە یێ چوو بیتە پێش دەمێ دیارکری
        if datetime.datetime.now() > self.target_time:
            return await interaction.response.send_message("ببورە، دەمێ پێشبینیێ ب دووماهی هاتییە و بەریکانە ڕاوەستایە! ❌", ephemeral=True)

        if interaction.user in self.participants:
            return await interaction.response.send_message("تە بەری نوکە پێشبینیا خۆ نڤیسییە! ❌", ephemeral=True)
        
        self.participants.append(interaction.user)
        
        log_channel = interaction.guild.get_channel(self.log_id)
        if log_channel:
            log_embed = discord.Embed(title="🎯 پێشبینییەکا نوو هات", color=0x00ffcc, timestamp=datetime.datetime.now())
            log_embed.add_field(name="👤 پشکدار:", value=f"{interaction.user.mention}", inline=True)
            log_embed.add_field(name="⚽ ئەنجام:", value=f"**{self.score.value}**", inline=False)
            log_embed.set_thumbnail(url=interaction.user.display_avatar.url)
            try: await log_channel.send(embed=log_embed)
            except: pass

        await interaction.response.send_message(f"✅ پێشبینیا تە هاتە تۆمارکرن: **{self.score.value}**", ephemeral=True)

# --- 2. کلاسێ دوگمەی ---
class MyGiveawayView(discord.ui.View):
    def __init__(self, timeout, log_id, target_time):
        super().__init__(timeout=timeout)
        self.participants = []
        self.log_id = log_id
        self.target_time = target_time

    @discord.ui.button(label="پێشبینی بکە", emoji="📝", style=discord.ButtonStyle.green)
    async def join_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        # پشکنینا بەری ڤەکرنا شاشا ڕەش
        if datetime.datetime.now() > self.target_time:
            return await interaction.response.send_message("ببورە، کاتێ بەریکانێ ب دووماهی هاتییە! ❌", ephemeral=True)
            
        await interaction.response.send_modal(PredictionModal(self.participants, self.log_id, self.target_time))

# --- 3. کوماندا Giveaway2 ---
@bot.command()
async def giveaway2(ctx, end_time_str: str, *, content: str):
    LOG_CHANNEL_ID = 1338197816660725916
    SPECIAL_ROLE_ID = 1488244673729269780 
    MY_IMAGE_URL = "https://cdn.discordapp.com/attachments/1472835696896249898/1488242647364665544/010fcba7-5abe-4f45-afc2-a9c11a155030.png?ex=69cc1179&is=69cabff9&hm=59348862e0f8b77b06e10e4263ed6c7200eea5a5340e5cb8555bf157af5cea22&" 

    has_role = discord.utils.get(ctx.author.roles, id=SPECIAL_ROLE_ID)
    if not (has_role or ctx.author.guild_permissions.administrator):
        return await ctx.send("❌ تو مۆڵەتا بکارئینانا ڤێ کوماندا نینی!")

    try:
        now = datetime.datetime.now()
        target_time = datetime.datetime.strptime(end_time_str, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        if target_time < now: target_time += datetime.timedelta(days=1)
        
        seconds_left = int((target_time - now).total_seconds())
        discord_timestamp = int(target_time.timestamp())
    except ValueError:
        return await ctx.send("❌ دەمی ب دروستی بنڤیسە (نموونە: `22:00`).")

    if "|" in content:
        requirement, prize = content.split("|", 1)
    else:
        requirement, prize = content, "خەڵاتەکێ نادیار"

    # لێرە target_time دهێتە ناردن بۆ ڤیو و مۆدال دا کۆنترۆڵا کاتی بکەن
    view = MyGiveawayView(timeout=seconds_left, log_id=LOG_CHANNEL_ID, target_time=target_time)
    
    embed = discord.Embed(
        title="🏆 پێشبینیا یاریێ و بەخشین 🏆",
        description=(
            f"🎁 **خەڵات:** **{prize.strip()}**\n"
            f"📜 **مەرج:** {requirement.strip()}\n\n"
            f"⏳ **دێ ب دووماهی هێت:** <t:{discord_timestamp}:R>\n"
            f"⏰ **دەمێ بڕانەوەی:** `{end_time_str}`"
        ),
        color=0x00aaff
    )
    if MY_IMAGE_URL.startswith("http"): embed.set_image(url=MY_IMAGE_URL)
    embed.set_footer(text="REALONES BOT – Real Ones Family")
    
    msg = await ctx.send(content="@everyone", embed=embed, view=view)

    await asyncio.sleep(seconds_left)

    end_embed = discord.Embed(
        title="🎊 GIVEAWAY ENDED - ب دووماهی هات 🎊",
        description=f"🎁 **خەڵات:** **{prize.strip()}**\n\nبەریکانە ب دووماهی هات و دوگمە ڕاوەستیا! 🏁",
        color=0xff0000
    )
    if MY_IMAGE_URL.startswith("http"): end_embed.set_image(url=MY_IMAGE_URL)
    
    await msg.edit(content=None, embed=end_embed, view=None)     
# --- Error Handling ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ This command does not exist!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to do this!")

# --- کارپێکرنا بۆتی ---
if TOKEN:
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("❌ Error: Login failed. Check your Token!")
else:
    print("❌ Error: TOKEN not found!")