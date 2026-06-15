import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import asyncio
import random
import aiohttp
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
TOKEN            = os.getenv("DISCORD_TOKEN")
YOUTUBE_API_KEY  = os.getenv("YOUTUBE_API_KEY")

# ──────────────────────────────────────────────
# CONFIGURARE
# ──────────────────────────────────────────────

CANAL_VERIFICARE_ID  = 1513874114027323605
CANAL_WELCOME_ID     = 1516068444997681253
CANAL_REGULAMENT_ID  = 1513873515563192350
CANAL_FAQ_ID         = 1516063846702387360
CANAL_TEPARI_ID      = 1516063981469437982
CANAL_GIVEAWAY_ID    = 1513873592423682109
CANAL_YOUTUBE_ID     = 1513873645485817938

CANALE_MARKET = [
    1516062696293007410,
    1516062759534592071,
    1516063216478715986,
    1516063244081430538,
    1516071041741619230,
    1516062911666323636,
    1513873677223989248,
]

SERVERE = {
    "Romania":          "Romania",
    "Tara Romaneasca":  "Tara Romaneasca",
    "Sapphire [AZURE]": "Sapphire [AZURE]",
    "Ruby [KIRIN]":     "Ruby [KIRIN]",
    "Tigerghost":       "Tigerghost",
    "Oceana":           "Oceana",
}

ROL_VERIFIED   = "Verified"
ROL_UNVERIFIED = "Unverified"
ROLURI_STAFF   = ["Admin", "Moderator"]

# YouTube
YOUTUBE_CHANNEL_ID  = "UCxxxxxxxxxxxxxx"  # ← se completează automat la pornire
YOUTUBE_HANDLE      = "Tenek13"
ORA_START_CHECK     = 15   # începe verificarea la ora 15:00
ORA_END_CHECK       = 23   # oprește verificarea la ora 23:00
INTERVAL_MINUTE     = 5    # verifică la fiecare 5 minute

# ──────────────────────────────────────────────
# TEXTE
# ──────────────────────────────────────────────

MESAJ_VERIFICARE = (
    "## 🏯 Bun venit pe server!\n\n"
    "Pentru a obține acces, apasă butonul de mai jos și completează cele două câmpuri.\n"
    "Durează mai puțin de un minut.\n\n"
    "**Nu posta niciun mesaj în acest canal.**"
)

REGULAMENT_TITLU = "📜 Regulament General"
REGULAMENT_TEXT = (
    "**§1 — Respect și comportament**\n"
    "Tratează toți membrii cu respect indiferent de server, nivel sau experiență. "
    "Jignirile, insultele și hărțuirea nu sunt tolerate.\n\n"
    "**§2 — Limbaj**\n"
    "Limbajul vulgar excesiv este interzis. Mesajele agresive, rasiste, sexiste sau "
    "discriminatorii duc la sancțiuni imediate.\n\n"
    "**§3 — Spam și flood**\n"
    "Interzis spam-ul de mesaje, emoji-uri excesive, caractere repetate sau mențiuni "
    "inutile (@everyone, @here).\n\n"
    "**§4 — Conținut NSFW**\n"
    "Orice conținut pentru adulți, violent sau șocant este strict interzis și duce la ban permanent.\n\n"
    "**§5 — Publicitate**\n"
    "Promovarea altor servere de Discord sau site-uri externe fără acordul administrației este interzisă.\n\n"
    "**§6 — Identitate și conturi**\n"
    "Un singur cont per persoană. Conturile alternative folosite pentru a evita sancțiuni "
    "vor fi banat permanent.\n\n"
    "**§7 — Sancțiuni**\n"
    "Abaterile se sancționează progresiv: avertisment → mute → kick → ban temporar → ban permanent, "
    "în funcție de gravitate.\n\n"
    "**§8 — Deciziile administrației**\n"
    "Deciziile Admin și Moderator sunt finale. Contestațiile se fac prin DM către Admin, nu public.\n\n"
    "**§9 — RMT (Real Money Trading)**\n"
    "Vânzarea, cumpărarea sau schimbul de bunuri, iteme sau conturi contra bani reali este strict "
    "interzisă pe acest server. Orice tentativă de RMT duce la ban permanent fără avertisment prealabil."
)

MARKET_TITLU = "📜 Reguli Market"
MARKET_TEXT = (
    "**1.** Descrieți clar ce vindeți — nume item, cantitate, server, preț\n"
    "**2.** Adăugați o poză cu itemul/itemele scoase la vânzare\n"
    "**3.** Negocierile se fac în privat — nu umpleți canalul cu oferte și contraoferte\n"
    "**4.** Limbaj decent — fără jigniri la adresa cumpărătorilor sau vânzătorilor\n"
    "**5.** Fără spam — un singur anunț per item, nu repostați la fiecare 5 minute\n"
    "**6.** RMT strict interzis — vânzarea contra bani reali duce la ban permanent"
)

FAQ_TITLU = "❓ FAQ — Întrebări frecvente"
FAQ_TEXT = (
    "Ai o întrebare legată de joc? Posteaz-o aici!\n\n"
    "Orice întrebare e binevenită — despre clase, iteme, quest-uri, mecanici de joc sau "
    "orice altceva legat de Metin2. Oricine știe răspunsul este încurajat să ajute.\n\n"
    "**Nimeni nu se naște învățat — respectați întrebările celorlalți.**"
)

TEPARI_TITLU = "⚠️ Raportare Țepari"
TEPARI_TEXT = (
    "Acest canal este destinat raportării tentativelor de înșelăciune sau a tranzacțiilor frauduloase.\n\n"
    "Postează dovezile pe care le ai — screenshot-uri, nume jucător, server, descrierea situației. "
    "Cu cât mai multe dovezi, cu atât mai rapid putem acționa.\n\n"
    "**Administrația nu se implică în dispute fără dovezi clare.**"
)

# ──────────────────────────────────────────────

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

giveaway_data = {}
youtube_channel_id_resolved = None
live_anuntat = False  # evităm spam dacă botul redetectează același live


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

REGULAMENT_IMAGE = "https://i.imgur.com/tZSdWtK.jpeg"

async def trimite_odata(canal, titlu, text, culoare=0xE8B84B, imagine=None):
    async for msg in canal.history(limit=30):
        if msg.author == bot.user and msg.embeds:
            if msg.embeds[0].title == titlu:
                print(f"⏭️  Mesaj deja existent în #{canal.name}, skip.")
                return
    embed = discord.Embed(title=titlu, description=text, color=culoare)
    if imagine:
        embed.set_image(url=imagine)
    embed.set_footer(text="Hydra Prestige • Metin2 Community")
    await canal.send(embed=embed)
    print(f"✅ Mesaj trimis în #{canal.name}")

def are_rol_staff(member: discord.Member) -> bool:
    return any(r.name in ROLURI_STAFF for r in member.roles)

async def get_youtube_channel_id(handle: str) -> str | None:
    """Rezolvă handle-ul YouTube (@Tenek13) în channel ID."""
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&q={handle}&type=channel&key={YOUTUBE_API_KEY}"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            items = data.get("items", [])
            if items:
                return items[0]["snippet"]["channelId"]
    return None

async def check_live(channel_id: str) -> dict | None:
    """Verifică dacă canalul e live. Returnează datele live-ului sau None."""
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&channelId={channel_id}&eventType=live&type=video&key={YOUTUBE_API_KEY}"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            items = data.get("items", [])
            if items:
                item = items[0]
                video_id = item["id"]["videoId"]
                titlu = item["snippet"]["title"]
                thumbnail = item["snippet"]["thumbnails"]["high"]["url"]
                return {
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "titlu": titlu,
                    "thumbnail": thumbnail,
                }
    return None


# ──────────────────────────────────────────────
# TASK YOUTUBE LIVE
# ──────────────────────────────────────────────

@tasks.loop(minutes=INTERVAL_MINUTE)
async def verifica_live():
    global live_anuntat, youtube_channel_id_resolved

    ora_acum = datetime.utcnow().hour + 2  # UTC+2 Romania
    if not (ORA_START_CHECK <= ora_acum < ORA_END_CHECK):
        return

    if not youtube_channel_id_resolved:
        return

    live = await check_live(youtube_channel_id_resolved)

    if live and not live_anuntat:
        canal = bot.get_channel(CANAL_YOUTUBE_ID)
        if canal:
            embed = discord.Embed(
                title="🔴 LIVE ACUM pe YouTube!",
                description=f"**{live['titlu']}**\n\n🎮 Hai să ne vedem pe stream!\n\n[👉 Intră pe live]({live['url']})",
                color=0xFF0000
            )
            embed.set_image(url=live["thumbnail"])
            embed.set_footer(text="Metin2 Community • Hydra Prestige")
            await canal.send("@everyone", embed=embed)
            live_anuntat = True
            print(f"✅ Live anunțat: {live['titlu']}")

    elif not live and live_anuntat:
        live_anuntat = False
        print("ℹ️  Live încheiat, resetat flag.")


# ──────────────────────────────────────────────
# VERIFICARE — Modal + Dropdown
# ──────────────────────────────────────────────

class NicknameModal(discord.ui.Modal, title="Un ultim pas"):
    nickname = discord.ui.TextInput(
        label="Nickname ingame",
        placeholder="ex: FireX3D",
        min_length=2,
        max_length=30,
    )

    def __init__(self, server_ales: str):
        super().__init__()
        self.server_ales = server_ales

    async def on_submit(self, interaction: discord.Interaction):
        guild  = interaction.guild
        member = interaction.user

        rol_verified = discord.utils.get(guild.roles, name=ROL_VERIFIED)
        if not rol_verified:
            await interaction.response.send_message("⚠️ Rolul Verified nu a fost găsit. Contactează un admin.", ephemeral=True)
            return

        nume_rol_server = SERVERE.get(self.server_ales)
        rol_server = discord.utils.get(guild.roles, name=nume_rol_server) if nume_rol_server else None

        nick_nou = f"{member.name} | {self.nickname.value.strip()}"
        if len(nick_nou) > 32:
            nick_nou = nick_nou[:32]

        roluri_de_dat = [rol_verified]
        if rol_server:
            roluri_de_dat.append(rol_server)

        try:
            await member.add_roles(*roluri_de_dat, reason="Verificare completată")
            try:
                await member.edit(nick=nick_nou)
            except discord.Forbidden:
                pass
        except discord.Forbidden:
            await interaction.response.send_message("⚠️ Nu am permisiuni suficiente. Contactează un admin.", ephemeral=True)
            return

        await interaction.response.send_message("✅ Verificare completată! Ai primit accesul la server.", ephemeral=True)

        roluri_text = ROL_VERIFIED + (f" + {nume_rol_server}" if rol_server else "")
        embed = discord.Embed(
            title="🏯 Bun venit în comunitate!",
            description=(
                f"Salut, **{nick_nou}**!\n\n"
                f"🎮 **Server:** {self.server_ales}\n"
                f"⚔️ **Nickname ingame:** {self.nickname.value.strip()}\n"
                f"🏷️ **Roluri primite:** {roluri_text}\n\n"
                f"Acum ai acces complet la server. Ne vedem pe câmpul de luptă!\n\n"
                f"Mulțumim că te-ai alăturat comunității, sperăm să te simți bine! "
                f"Pentru orice problemă poți contacta un Administrator sau un Moderator."
            ),
            color=0xE8B84B
        )
        embed.set_footer(text="Metin2 Community • Hydra Prestige")
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            pass


class ServerDropdown(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=s, value=s) for s in SERVERE]
        super().__init__(
            placeholder="Alege serverul pe care joci...",
            min_values=1, max_values=1,
            options=options,
            custom_id="server_select"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(NicknameModal(self.values[0]))


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ServerDropdown())


class VerificareView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Începe verificarea", style=discord.ButtonStyle.primary, emoji="⚔️", custom_id="verificare_btn")
    async def verificare_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        rol = discord.utils.get(interaction.guild.roles, name=ROL_VERIFIED)
        if rol and rol in interaction.user.roles:
            await interaction.response.send_message("✅ Ești deja verificat!", ephemeral=True)
            return
        await interaction.response.send_message(
            "## ⚔️ Pasul 1 — Alege serverul\n\nPe ce server Metin2 joci?",
            view=DropdownView(), ephemeral=True
        )


# ──────────────────────────────────────────────
# GIVEAWAY
# ──────────────────────────────────────────────

class GiveawayModal(discord.ui.Modal, title="Creează Giveaway"):
    premiu = discord.ui.TextInput(label="Premiu", placeholder="ex: 1.000.000 Yang", max_length=100)
    durata = discord.ui.TextInput(label="Durată (în zile)", placeholder="ex: 7", max_length=3)
    youtube = discord.ui.TextInput(label="Link YouTube (opțional)", placeholder="https://youtube.com/@canal", required=False, max_length=200)
    instagram = discord.ui.TextInput(label="Link Instagram (opțional)", placeholder="https://instagram.com/cont", required=False, max_length=200)
    tiktok = discord.ui.TextInput(label="Link TikTok (opțional)", placeholder="https://tiktok.com/@cont", required=False, max_length=200)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            zile = int(self.durata.value.strip())
            if zile < 1 or zile > 365:
                raise ValueError
        except ValueError:
            await interaction.response.send_message("❌ Durata trebuie să fie un număr între 1 și 365.", ephemeral=True)
            return

        end_time = datetime.utcnow() + timedelta(days=zile)
        timestamp = int(end_time.timestamp())
        canal = bot.get_channel(CANAL_GIVEAWAY_ID)
        if not canal:
            await interaction.response.send_message("❌ Canalul de giveaway nu a fost găsit.", ephemeral=True)
            return

        taskuri = []
        if self.youtube.value.strip():
            taskuri.append(f"[📺 Subscribe pe YouTube]({self.youtube.value.strip()})")
        if self.instagram.value.strip():
            taskuri.append(f"[📸 Follow pe Instagram]({self.instagram.value.strip()})")
        if self.tiktok.value.strip():
            taskuri.append(f"[🎵 Follow pe TikTok]({self.tiktok.value.strip()})")

        taskuri_text = "\n".join(taskuri) if taskuri else "Nicio condiție — participare liberă!"

        embed = discord.Embed(
            title="🎉 GIVEAWAY",
            description=(
                f"**Premiu:** {self.premiu.value.strip()}\n\n"
                f"**📋 Condiții de participare:**\n{taskuri_text}\n\n"
                f"Apasă butonul **Participă** după ce ai completat taskurile.\n\n"
                f"**⏰ Extragere:** <t:{timestamp}:F>\n"
                f"**⏳ Timp rămas:** <t:{timestamp}:R>"
            ),
            color=0xFEE75C
        )
        embed.set_footer(text=f"Giveaway creat de {interaction.user.name} • Hydra Prestige")

        view = GiveawayView()
        msg = await canal.send("@everyone", embed=embed, view=view)

        giveaway_data[msg.id] = {
            "participanti": set(),
            "premiu": self.premiu.value.strip(),
            "end_time": end_time,
            "youtube": self.youtube.value.strip(),
            "instagram": self.instagram.value.strip(),
            "tiktok": self.tiktok.value.strip(),
            "msg_id": msg.id,
            "canal_id": CANAL_GIVEAWAY_ID,
        }

        try:
            await interaction.message.delete()
        except Exception:
            pass

        await interaction.response.send_message("✅ Giveaway creat cu succes!", ephemeral=True, delete_after=5)
        asyncio.create_task(countdown_giveaway(msg.id, zile * 86400))


class GiveawayView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎉 Participă", style=discord.ButtonStyle.success, custom_id="giveaway_participa")
    async def participa(self, interaction: discord.Interaction, button: discord.ui.Button):
        msg_id = interaction.message.id
        if msg_id not in giveaway_data:
            await interaction.response.send_message("❌ Giveaway-ul nu mai este activ.", ephemeral=True)
            return

        data = giveaway_data[msg_id]
        if interaction.user.id in data["participanti"]:
            await interaction.response.send_message("✅ Ești deja înscris!", ephemeral=True)
            return

        taskuri = []
        if data["youtube"]:
            taskuri.append(f"[📺 Subscribe pe YouTube]({data['youtube']})")
        if data["instagram"]:
            taskuri.append(f"[📸 Follow pe Instagram]({data['instagram']})")
        if data["tiktok"]:
            taskuri.append(f"[🎵 Follow pe TikTok]({data['tiktok']})")

        mesaj = ("Completează taskurile și apasă **Confirm înscriere**:\n\n" + "\n".join(taskuri)) if taskuri else "Apasă **Confirm înscriere** pentru a participa."
        await interaction.response.send_message(mesaj, view=ConfirmView(msg_id), ephemeral=True)


class ConfirmView(discord.ui.View):
    def __init__(self, msg_id: int):
        super().__init__(timeout=120)
        self.msg_id = msg_id

    @discord.ui.button(label="✅ Confirm înscriere", style=discord.ButtonStyle.primary)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.msg_id not in giveaway_data:
            await interaction.response.send_message("❌ Giveaway-ul nu mai este activ.", ephemeral=True)
            return
        giveaway_data[self.msg_id]["participanti"].add(interaction.user.id)
        total = len(giveaway_data[self.msg_id]["participanti"])
        await interaction.response.send_message(f"🎉 Ești înscris! Mult succes!\n📊 Participanți: **{total}**", ephemeral=True)


async def countdown_giveaway(msg_id: int, secunde: int):
    await asyncio.sleep(secunde)
    if msg_id not in giveaway_data:
        return
    data = giveaway_data[msg_id]
    canal = bot.get_channel(data["canal_id"])
    if not canal:
        return
    participanti = list(data["participanti"])
    if not participanti:
        await canal.send("🎉 Giveaway-ul s-a încheiat dar nu a existat niciun participant. Mai încercați data viitoare!")
        del giveaway_data[msg_id]
        return
    castigator_id = random.choice(participanti)
    castigator = canal.guild.get_member(castigator_id)
    nume_castigator = castigator.mention if castigator else f"<@{castigator_id}>"
    embed = discord.Embed(
        title="🏆 Giveaway încheiat!",
        description=(
            f"**Premiu:** {data['premiu']}\n\n"
            f"🎉 **Câștigătorul este:** {nume_castigator}\n\n"
            f"📊 Total participanți: **{len(participanti)}**\n\n"
            f"Mulțumim tuturor pentru participare și vă mai așteptăm!"
        ),
        color=0x57F287
    )
    embed.set_footer(text="Hydra Prestige • Metin2 Community")
    await canal.send("@everyone", embed=embed)
    del giveaway_data[msg_id]


# ──────────────────────────────────────────────
# COMENZI MODERARE
# ──────────────────────────────────────────────

@tree.command(name="mute", description="Dezactivează scrisul unui membru")
@app_commands.describe(membru="Membrul de mutat", motiv="Motivul")
async def mute(interaction: discord.Interaction, membru: discord.Member, motiv: str = "Nespecificat"):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea să folosești această comandă.", ephemeral=True)
        return
    try:
        await membru.edit(mute=True)
        embed = discord.Embed(title="🔇 Mute aplicat", description=f"**Membru:** {membru.mention}\n**Motiv:** {motiv}", color=0xED4245)
        embed.set_footer(text=f"Acțiune de: {interaction.user.name}")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Nu am permisiuni suficiente.", ephemeral=True)


@tree.command(name="timeout", description="Aplică timeout unui membru")
@app_commands.describe(membru="Membrul", minute="Durata în minute", motiv="Motivul")
async def timeout_cmd(interaction: discord.Interaction, membru: discord.Member, minute: int, motiv: str = "Nespecificat"):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea să folosești această comandă.", ephemeral=True)
        return
    try:
        await membru.timeout(timedelta(minutes=minute), reason=motiv)
        embed = discord.Embed(title="⏱️ Timeout aplicat", description=f"**Membru:** {membru.mention}\n**Durată:** {minute} minute\n**Motiv:** {motiv}", color=0xFEE75C)
        embed.set_footer(text=f"Acțiune de: {interaction.user.name}")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Nu am permisiuni suficiente.", ephemeral=True)


@tree.command(name="kick", description="Dă afară un membru din server")
@app_commands.describe(membru="Membrul", motiv="Motivul")
async def kick(interaction: discord.Interaction, membru: discord.Member, motiv: str = "Nespecificat"):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea să folosești această comandă.", ephemeral=True)
        return
    try:
        await membru.kick(reason=motiv)
        embed = discord.Embed(title="👢 Kick aplicat", description=f"**Membru:** {membru.name}\n**Motiv:** {motiv}", color=0xED4245)
        embed.set_footer(text=f"Acțiune de: {interaction.user.name}")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Nu am permisiuni suficiente.", ephemeral=True)


@tree.command(name="ban", description="Banează un membru permanent")
@app_commands.describe(membru="Membrul", motiv="Motivul")
async def ban(interaction: discord.Interaction, membru: discord.Member, motiv: str = "Nespecificat"):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea să folosești această comandă.", ephemeral=True)
        return
    try:
        await membru.ban(reason=motiv)
        embed = discord.Embed(title="🔨 Ban aplicat", description=f"**Membru:** {membru.name}\n**Motiv:** {motiv}", color=0xED4245)
        embed.set_footer(text=f"Acțiune de: {interaction.user.name}")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Nu am permisiuni suficiente.", ephemeral=True)


@tree.command(name="giveaway", description="Creează un giveaway")
async def giveaway_cmd(interaction: discord.Interaction):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea să folosești această comandă.", ephemeral=True)
        return
    await interaction.response.send_modal(GiveawayModal())


# ──────────────────────────────────────────────
# WELCOME / LEAVE
# ──────────────────────────────────────────────

@bot.event
async def on_member_join(member: discord.Member):
    rol_unverified = discord.utils.get(member.guild.roles, name=ROL_UNVERIFIED)
    if rol_unverified:
        await member.add_roles(rol_unverified, reason="Rol implicit la intrare")
    canal = bot.get_channel(CANAL_WELCOME_ID)
    if canal:
        embed = discord.Embed(
            title="👋 Membru nou!",
            description=f"Bun venit pe server, {member.mention}!\n\nMergi în <#{CANAL_VERIFICARE_ID}> pentru a obține acces.",
            color=0x57F287
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Membri: {member.guild.member_count}")
        await canal.send(embed=embed)


@bot.event
async def on_member_remove(member: discord.Member):
    canal = bot.get_channel(CANAL_WELCOME_ID)
    if canal:
        embed = discord.Embed(title="🚪 Membru plecat", description=f"**{member.name}** a părăsit serverul.", color=0xED4245)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Membri: {member.guild.member_count}")
        await canal.send(embed=embed)


# ──────────────────────────────────────────────
# ON READY
# ──────────────────────────────────────────────

@bot.event
async def on_ready():
    global youtube_channel_id_resolved
    print(f"✅ Bot pornit ca {bot.user}")

    bot.add_view(VerificareView())
    bot.add_view(DropdownView())
    bot.add_view(GiveawayView())

    await tree.sync()
    print("✅ Slash commands sincronizate")

    # Rezolvăm channel ID YouTube din handle
    if YOUTUBE_API_KEY:
        youtube_channel_id_resolved = await get_youtube_channel_id(YOUTUBE_HANDLE)
        if youtube_channel_id_resolved:
            print(f"✅ YouTube channel ID rezolvat: {youtube_channel_id_resolved}")
            verifica_live.start()
        else:
            print("⚠️  Nu s-a putut rezolva channel ID-ul YouTube.")
    else:
        print("⚠️  YOUTUBE_API_KEY lipsă din .env")

    # #get-started
    canal_vs = bot.get_channel(CANAL_VERIFICARE_ID)
    if canal_vs:
        mesaj_existent = None
        async for msg in canal_vs.history(limit=20):
            if msg.author == bot.user and msg.components:
                mesaj_existent = msg
                break
        if mesaj_existent:
            await mesaj_existent.edit(content=MESAJ_VERIFICARE, view=VerificareView())
            print(f"✅ Mesaj actualizat în #{canal_vs.name}")
        else:
            await canal_vs.send(content=MESAJ_VERIFICARE, view=VerificareView())
            print(f"✅ Mesaj trimis în #{canal_vs.name}")

    canal = bot.get_channel(CANAL_REGULAMENT_ID)
    if canal:
        await trimite_odata(canal, REGULAMENT_TITLU, REGULAMENT_TEXT, 0xE8B84B, REGULAMENT_IMAGE)

    canal = bot.get_channel(CANAL_FAQ_ID)
    if canal:
        await trimite_odata(canal, FAQ_TITLU, FAQ_TEXT, 0x5865F2)

    canal = bot.get_channel(CANAL_TEPARI_ID)
    if canal:
        await trimite_odata(canal, TEPARI_TITLU, TEPARI_TEXT, 0xED4245)

    for canal_id in CANALE_MARKET:
        canal = bot.get_channel(canal_id)
        if canal:
            await trimite_odata(canal, MARKET_TITLU, MARKET_TEXT, 0xFEE75C)


bot.run(TOKEN)