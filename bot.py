import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import asyncio
import random
import aiohttp
import json
from datetime import datetime, timedelta

TOKEN = os.environ.get("DISCORD_TOKEN")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

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
CANAL_MEMBRI_ID      = 1516433983817257190
CANAL_LOG_GIVEAWAY_ID = 1517580517799886991

CANALE_MARKET = [
    1516062696293007410,
    1516062759534592071,
    1516063216478715986,
    1516063244081430538,
    1516071041741619230,
    1516062911666323636,
    1513873677223989248,
]

SERVERE_METIN2 = {
    "Romania":          "🗡️ Romania",
    "Tara Romaneasca":  "🏰 Tara Romaneasca",
    "Sapphire [AZURE]": "🔷 Sapphire [AZURE]",
    "Ruby [KIRIN]":     "♦️ Ruby [KIRIN]",
    "Tigerghost":       "👻 Tigerghost",
    "Oceana":           "🌊 Oceana",
}

JOCURI_GAMER = [
    "🏆 League of Legends",
    "🔫 Counter-Strike 2",
    "🪓 Rust",
    "🌀 Dota 2",
    "🚗 GTA",
]

ROL_METIN2     = "⚔️ Metin2"
ROL_GAMER      = "🎮 Gamer"
ROL_VERIFIED   = "⭐ Verified"   # acordat când are ambele
ROL_UNVERIFIED = "Unverified"
ROLURI_STAFF   = ["Admin", "Moderator"]
OWNER_ID       = 401451926681812993

YOUTUBE_HANDLE  = "Tenek13"
ORA_START_CHECK = 15
ORA_END_CHECK   = 23
INTERVAL_MINUTE = 5

INVITE_DATA_FILE = "invite_data.json"
GIVEAWAY_DATA_FILE = "giveaway_data.json"

# ──────────────────────────────────────────────
# TEXTE
# ──────────────────────────────────────────────

MESAJ_VERIFICARE_METIN2 = (
    "## ⚔️ Verificare Metin2\n\n"
    "Ești jucător de Metin2? Apasă butonul de mai jos pentru a obține accesul la canalele de Metin2.\n\n"
    "**Vei primi rolul:** `⚔️ Metin2`"
)

MESAJ_VERIFICARE_GAMER = (
    "## 🎮 Verificare Gaming\n\n"
    "Joci alte jocuri? Apasă butonul de mai jos pentru a obține accesul la canalele de gaming.\n\n"
    "**Vei primi rolul:** `🎮 Gamer`"
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
intents.invites = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

giveaway_data = {}
giveaway_history = {}
# istoric giveaway-uri finalizate recent — permite reroll. { msg_id: {premiu, participanti, canal_id} }
GIVEAWAY_HISTORY_FILE = "giveaway_history.json"

invite_tracker = {}
cached_invites = {}
youtube_channel_id_resolved = None
live_anuntat = False


# ──────────────────────────────────────────────
# INVITE DATA PERSISTENT
# ──────────────────────────────────────────────

def load_invite_data() -> dict:
    try:
        with open(INVITE_DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_invite_data(data: dict):
    try:
        with open(INVITE_DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"⚠️  Eroare la salvarea invite_data: {e}")

def get_invite_count(user_id: int) -> int:
    data = load_invite_data()
    return data.get(str(user_id), {}).get("invites", 0)

def add_invite(inviter_id: int, invited_id: int):
    data = load_invite_data()
    key = str(inviter_id)
    if key not in data:
        data[key] = {"invites": 0, "invited_by": None, "invited_users": []}
    data[key]["invites"] += 1
    if invited_id not in data[key]["invited_users"]:
        data[key]["invited_users"].append(invited_id)
    inv_key = str(invited_id)
    if inv_key not in data:
        data[inv_key] = {"invites": 0, "invited_by": None, "invited_users": []}
    data[inv_key]["invited_by"] = inviter_id
    save_invite_data(data)

def remove_invite(invited_id: int):
    data = load_invite_data()
    inv_key = str(invited_id)
    inviter_id = data.get(inv_key, {}).get("invited_by")
    if inviter_id:
        key = str(inviter_id)
        if key in data and data[key]["invites"] > 0:
            data[key]["invites"] -= 1
            if invited_id in data[key]["invited_users"]:
                data[key]["invited_users"].remove(invited_id)
        save_invite_data(data)
    return inviter_id

def get_inviter(user_id: int):
    data = load_invite_data()
    return data.get(str(user_id), {}).get("invited_by")

def set_invite_count(user_id: int, count: int):
    """Setează manual numărul de invitații al unui user (admin override)."""
    data = load_invite_data()
    key = str(user_id)
    if key not in data:
        data[key] = {"invites": 0, "invited_by": None, "invited_users": []}
    data[key]["invites"] = count
    save_invite_data(data)

def get_leaderboard_invitatii() -> list:
    """Returnează lista (user_id, invites) sortată descrescător."""
    data = load_invite_data()
    lista = [(int(uid), info.get("invites", 0)) for uid, info in data.items()]
    lista = [item for item in lista if item[1] > 0]
    lista.sort(key=lambda x: x[1], reverse=True)
    return lista


# ──────────────────────────────────────────────
# GIVEAWAY DATA PERSISTENT
# ──────────────────────────────────────────────

def save_giveaway_data():
    """Salvează giveaway_data în JSON, convertind set/datetime în formate serializabile."""
    try:
        serializable = {}
        for msg_id, data in giveaway_data.items():
            d = dict(data)
            d["participanti"] = list(d["participanti"])
            d["end_time"] = d["end_time"].isoformat()
            serializable[str(msg_id)] = d
        with open(GIVEAWAY_DATA_FILE, "w") as f:
            json.dump(serializable, f, indent=2)
    except Exception as e:
        print(f"⚠️  Eroare la salvarea giveaway_data: {e}")

def load_giveaway_data() -> dict:
    """Încarcă giveaway_data din JSON, reconvertind tipurile."""
    try:
        with open(GIVEAWAY_DATA_FILE, "r") as f:
            raw = json.load(f)
        result = {}
        for msg_id_str, d in raw.items():
            d["participanti"] = set(d["participanti"])
            d["end_time"] = datetime.fromisoformat(d["end_time"])
            # invite_codes și invitati_de au chei int salvate ca string în JSON
            d["invite_codes"] = {int(k): v for k, v in d.get("invite_codes", {}).items()}
            d["invitati_de"] = {int(k): v for k, v in d.get("invitati_de", {}).items()}
            result[int(msg_id_str)] = d
        return result
    except Exception:
        return {}

def save_giveaway_history():
    try:
        serializable = {}
        for msg_id, h in giveaway_history.items():
            serializable[str(msg_id)] = {
                "premiu": h["premiu"],
                "participanti": list(h["participanti"]),
                "canal_id": h["canal_id"],
            }
        with open(GIVEAWAY_HISTORY_FILE, "w") as f:
            json.dump(serializable, f, indent=2)
    except Exception as e:
        print(f"⚠️  Eroare la salvarea giveaway_history: {e}")

def load_giveaway_history() -> dict:
    try:
        with open(GIVEAWAY_HISTORY_FILE, "r") as f:
            raw = json.load(f)
        return {
            int(msg_id_str): {
                "premiu": h["premiu"],
                "participanti": set(h["participanti"]),
                "canal_id": h["canal_id"],
            }
            for msg_id_str, h in raw.items()
        }
    except Exception:
        return {}


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

def parse_durata(text: str) -> int | None:
    """Parsează durată flexibilă: '3d', '2h', '30m', '1d12h30m' -> secunde totale."""
    import re
    text = text.strip().lower().replace(" ", "")
    pattern = r'(\d+)([dhm])'
    matches = re.findall(pattern, text)
    if not matches:
        return None

    total_secunde = 0
    for valoare, unitate in matches:
        valoare = int(valoare)
        if unitate == 'd':
            total_secunde += valoare * 86400
        elif unitate == 'h':
            total_secunde += valoare * 3600
        elif unitate == 'm':
            total_secunde += valoare * 60

    return total_secunde if total_secunde > 0 else None

async def verifica_si_da_verified(member: discord.Member, guild: discord.Guild):
    """Dacă userul are atât Metin2 cât și Gamer, îi dă Verified."""
    await asyncio.sleep(1)
    # Refetch member pentru a avea rolurile actualizate
    try:
        member = await guild.fetch_member(member.id)
    except Exception:
        pass
    role_names = [r.name for r in member.roles]
    if ROL_METIN2 in role_names and ROL_GAMER in role_names:
        rol_verified = discord.utils.get(guild.roles, name=ROL_VERIFIED)
        if rol_verified and rol_verified not in member.roles:
            await member.add_roles(rol_verified, reason="A completat ambele verificări")
            print(f"✅ {member.name} a primit ⭐ Verified")

async def get_youtube_channel_id(handle: str) -> str | None:
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

async def genereaza_invite(guild: discord.Guild) -> discord.Invite | None:
    canal = guild.get_channel(CANAL_VERIFICARE_ID)
    if not canal:
        return None
    try:
        invite = await canal.create_invite(max_age=0, max_uses=0, unique=True)
        return invite
    except discord.Forbidden:
        return None

def embed_giveaway(data: dict, guild: discord.Guild) -> discord.Embed:
    conditii_text = data.get("conditii", "").strip() or "Nicio condiție — participare liberă!"
    membri_minim = data.get("membri_minim")
    membri_actuali = guild.member_count if guild else 0
    numar_castigatori = data.get("numar_castigatori", 1)

    if membri_minim and not data.get("pornit"):
        status = f"⏳ Așteptăm **{membri_actuali}/{membri_minim}** membri pentru a porni countdown-ul"
    else:
        timestamp = int(data["end_time"].timestamp())
        status = f"**⏰ Extragere:** <t:{timestamp}:F>\n**⏳ Timp rămas:** <t:{timestamp}:R>"

    castigatori_text = f"**🏆 Câștigători:** {numar_castigatori}\n" if numar_castigatori > 1 else ""

    desc = (
        f"**Premiu:** {data['premiu']}\n"
        f"{castigatori_text}\n"
        f"**📋 Condiții și detalii:**\n{conditii_text}\n\n"
        f"Apasă butonul **Participă** după ce ai completat taskurile.\n\n"
        f"{status}"
    )

    embed = discord.Embed(title="🎉 GIVEAWAY", description=desc, color=0xFEE75C)
    embed.set_footer(text="Giveaway • Hydra Prestige")
    return embed


# ──────────────────────────────────────────────
# TASK YOUTUBE LIVE
# ──────────────────────────────────────────────

@tasks.loop(minutes=INTERVAL_MINUTE)
async def verifica_live():
    global live_anuntat, youtube_channel_id_resolved
    ora_acum = datetime.utcnow().hour + 2
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
# TASK CONTOR MEMBRI GIVEAWAY
# ──────────────────────────────────────────────

@tasks.loop(seconds=30)
async def verifica_membrii_giveaway():
    for msg_id, data in list(giveaway_data.items()):
        if data.get("membri_minim") and not data.get("pornit"):
            canal = bot.get_channel(data["canal_id"])
            if not canal:
                continue
            guild = canal.guild
            if guild.member_count >= data["membri_minim"]:
                data["pornit"] = True
                data["end_time"] = datetime.utcnow() + timedelta(seconds=data["secunde_durata"])
                asyncio.create_task(countdown_giveaway(msg_id, data["secunde_durata"]))
                save_giveaway_data()
                print(f"✅ Giveaway {msg_id} pornit")
            try:
                msg = await canal.fetch_message(msg_id)
                await msg.edit(embed=embed_giveaway(data, guild))
            except Exception:
                pass


# ──────────────────────────────────────────────
# TASK COUNTER MEMBRI
# ──────────────────────────────────────────────

@tasks.loop(minutes=1)
async def update_member_counter():
    canal = bot.get_channel(CANAL_MEMBRI_ID)
    if not canal:
        return
    guild = canal.guild
    nou_nume = f"👥 𝗺𝗲𝗺𝗯𝗿𝗶𝗶: {guild.member_count}"
    if canal.name != nou_nume:
        try:
            await canal.edit(name=nou_nume)
        except Exception as e:
            print(f"⚠️  Eroare update counter membri: {e}")


# ──────────────────────────────────────────────
# VERIFICARE METIN2 — Modal + Dropdown
# ──────────────────────────────────────────────

class NicknameMetin2Modal(discord.ui.Modal, title="Verificare Metin2"):
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

        rol_metin2 = discord.utils.get(guild.roles, name=ROL_METIN2)
        if not rol_metin2:
            await interaction.response.send_message("⚠️ Rolul Metin2 nu a fost găsit. Contactează un admin.", ephemeral=True)
            return

        nume_rol_server = SERVERE_METIN2.get(self.server_ales)
        rol_server = discord.utils.get(guild.roles, name=nume_rol_server) if nume_rol_server else None

        nick_nou = f"{member.name} | {self.nickname.value.strip()}"
        if len(nick_nou) > 32:
            nick_nou = nick_nou[:32]

        roluri_de_dat = [rol_metin2]
        if rol_server:
            roluri_de_dat.append(rol_server)

        primul_metin2 = rol_metin2 not in member.roles  # verificăm ÎNAINTE de add_roles

        try:
            await member.add_roles(*roluri_de_dat, reason="Verificare Metin2 completată")
            rol_unverified = discord.utils.get(guild.roles, name=ROL_UNVERIFIED)
            if rol_unverified and rol_unverified in member.roles:
                await member.remove_roles(rol_unverified, reason="Verificare completată")
            try:
                await member.edit(nick=nick_nou)
            except discord.Forbidden:
                pass
        except discord.Forbidden:
            await interaction.response.send_message("⚠️ Nu am permisiuni suficiente.", ephemeral=True)
            return

        await verifica_si_da_verified(member, guild)
        await interaction.response.send_message("✅ Verificare Metin2 completată!", ephemeral=True)

        # DM doar la prima obținere a rolului Metin2
        if primul_metin2:
            roluri_text = ROL_METIN2 + (f" + {nume_rol_server}" if rol_server else "")
            embed = discord.Embed(
                title="🏯 Bun venit în comunitate!",
                description=(
                    f"Salut, **{nick_nou}**!\n\n"
                    f"🎮 **Server:** {self.server_ales}\n"
                    f"⚔️ **Nickname ingame:** {self.nickname.value.strip()}\n"
                    f"🏷️ **Roluri primite:** {roluri_text}\n\n"
                    f"Acum ai acces la canalele de Metin2. Ne vedem pe câmpul de luptă!\n\n"
                    f"Mulțumim că te-ai alăturat comunității! Pentru orice problemă contactează un Admin sau Moderator."
                ),
                color=0xE8B84B
            )
            embed.set_footer(text="Metin2 Community • Hydra Prestige")
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                pass


class ServerMetin2Dropdown(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=s, value=s) for s in SERVERE_METIN2]
        super().__init__(
            placeholder="Alege serverul pe care joci...",
            min_values=1, max_values=1,
            options=options,
            custom_id="server_metin2_select"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(NicknameMetin2Modal(self.values[0]))


class DropdownMetin2View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ServerMetin2Dropdown())


class ServerMetin2ToggleDropdown(discord.ui.Select):
    """Dropdown pentru schimbarea serverelor Metin2 — toggle add/remove."""
    def __init__(self, member_role_names: list):
        options = []
        for display, rol_name in SERVERE_METIN2.items():
            are_rol = rol_name in member_role_names
            options.append(discord.SelectOption(
                label=display,
                value=display,
                emoji="✅" if are_rol else "➕",
                description="Apasă să scoți" if are_rol else "Apasă să adaugi"
            ))
        super().__init__(
            placeholder="Alege serverele tale...",
            min_values=0, max_values=len(SERVERE_METIN2),
            options=options,
            custom_id="server_metin2_toggle_select"
        )
        self.member_role_names = member_role_names

    async def callback(self, interaction: discord.Interaction):
        guild  = interaction.guild
        member = interaction.user
        selectate = set(self.values)

        roluri_de_adaugat = []
        roluri_de_scos = []

        for display, rol_name in SERVERE_METIN2.items():
            rol = discord.utils.get(guild.roles, name=rol_name)
            if not rol:
                continue
            are_rol = rol_name in self.member_role_names
            vrea_rol = display in selectate

            if vrea_rol and not are_rol:
                roluri_de_adaugat.append(rol)
            elif not vrea_rol and are_rol:
                roluri_de_scos.append(rol)

        if roluri_de_adaugat:
            await member.add_roles(*roluri_de_adaugat, reason="Schimbare server Metin2")
        if roluri_de_scos:
            await member.remove_roles(*roluri_de_scos, reason="Schimbare server Metin2")

        # Dacă nu mai are niciun server Metin2, scoatem și rolul Metin2 și Verified
        await asyncio.sleep(1)
        member = await guild.fetch_member(member.id)
        role_names_now = [r.name for r in member.roles]
        are_server_metin2 = any(rn in role_names_now for rn in SERVERE_METIN2.values())

        if not are_server_metin2:
            rol_metin2 = discord.utils.get(guild.roles, name=ROL_METIN2)
            rol_verified = discord.utils.get(guild.roles, name=ROL_VERIFIED)
            to_remove = []
            if rol_metin2 and rol_metin2 in member.roles:
                to_remove.append(rol_metin2)
            if rol_verified and rol_verified in member.roles:
                to_remove.append(rol_verified)
            if to_remove:
                await member.remove_roles(*to_remove, reason="Niciun server Metin2 selectat")

        await interaction.response.send_message("✅ Rolurile de server au fost actualizate!", ephemeral=True)


class VerificareMetin2View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verificare Metin2", style=discord.ButtonStyle.primary, emoji="⚔️", custom_id="verificare_metin2_btn")
    async def verificare_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        rol = discord.utils.get(interaction.guild.roles, name=ROL_METIN2)
        member_role_names = [r.name for r in interaction.user.roles]

        if rol and rol in interaction.user.roles:
            # Are deja Metin2 — toggle dropdown
            view = discord.ui.View(timeout=120)
            view.add_item(ServerMetin2ToggleDropdown(member_role_names))
            await interaction.response.send_message(
                "## ⚔️ Gestionează serverele Metin2\n\n✅ = ai rolul | ➕ = nu ai rolul\nSelectează serverele dorite:",
                view=view, ephemeral=True
            )
            return
        await interaction.response.send_message(
            "## ⚔️ Alege serverul Metin2\n\nPe ce server joci?",
            view=DropdownMetin2View(), ephemeral=True
        )


# ──────────────────────────────────────────────
# VERIFICARE GAMER — Dropdown jocuri
# ──────────────────────────────────────────────

class JocDropdown(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=j, value=j) for j in JOCURI_GAMER]
        super().__init__(
            placeholder="Alege jocul/jocurile tale...",
            min_values=1, max_values=len(JOCURI_GAMER),
            options=options,
            custom_id="joc_select"
        )

    async def callback(self, interaction: discord.Interaction):
        guild  = interaction.guild
        member = interaction.user
        jocuri_alese = self.values

        rol_gamer = discord.utils.get(guild.roles, name=ROL_GAMER)
        primul_gamer = rol_gamer not in member.roles  # verificăm ÎNAINTE de add_roles

        if not rol_gamer:
            await interaction.response.send_message("⚠️ Rolul Gamer nu a fost găsit. Contactează un admin.", ephemeral=True)
            return

        roluri_de_dat = [rol_gamer]
        for joc in jocuri_alese:
            rol_joc = discord.utils.get(guild.roles, name=joc)
            if rol_joc:
                roluri_de_dat.append(rol_joc)

        try:
            await member.add_roles(*roluri_de_dat, reason="Verificare Gamer completată")
            rol_unverified = discord.utils.get(guild.roles, name=ROL_UNVERIFIED)
            if rol_unverified and rol_unverified in member.roles:
                await member.remove_roles(rol_unverified, reason="Verificare completată")
        except discord.Forbidden:
            await interaction.response.send_message("⚠️ Nu am permisiuni suficiente.", ephemeral=True)
            return

        await verifica_si_da_verified(member, guild)

        jocuri_text = ", ".join(jocuri_alese)
        await interaction.response.send_message(
            f"✅ Ai primit rolul **{ROL_GAMER}** + **{jocuri_text}**!",
            ephemeral=True
        )

        # DM doar la prima obținere a rolului Gamer
        if primul_gamer:
            embed_dm = discord.Embed(
                title="🎮 Bun venit în comunitate!",
                description=(
                    f"Salut, **{member.display_name}**!\n\n"
                    f"🎮 **Jocuri:** {jocuri_text}\n"
                    f"🏷️ **Roluri primite:** {ROL_GAMER} + {jocuri_text}\n\n"
                    f"Acum ai acces la canalele de gaming!\n\n"
                    f"Mulțumim că te-ai alăturat comunității! Pentru orice problemă contactează un Admin sau Moderator."
                ),
                color=0x2ECC71
            )
            embed_dm.set_footer(text="Hydra Prestige • Community")
            try:
                await member.send(embed=embed_dm)
            except discord.Forbidden:
                pass


class DropdownGamerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(JocDropdown())


class JocToggleDropdown(discord.ui.Select):
    """Dropdown pentru schimbarea jocurilor — toggle add/remove."""
    def __init__(self, member_role_names: list):
        options = []
        for joc in JOCURI_GAMER:
            are_rol = joc in member_role_names
            options.append(discord.SelectOption(
                label=joc,
                value=joc,
                emoji="✅" if are_rol else "➕",
                description="Apasă să scoți" if are_rol else "Apasă să adaugi"
            ))
        super().__init__(
            placeholder="Alege jocurile tale...",
            min_values=0, max_values=len(JOCURI_GAMER),
            options=options,
            custom_id="joc_toggle_select"
        )
        self.member_role_names = member_role_names

    async def callback(self, interaction: discord.Interaction):
        guild  = interaction.guild
        member = interaction.user
        selectate = set(self.values)

        roluri_de_adaugat = []
        roluri_de_scos = []

        for joc in JOCURI_GAMER:
            rol = discord.utils.get(guild.roles, name=joc)
            if not rol:
                continue
            are_rol = joc in self.member_role_names
            vrea_rol = joc in selectate

            if vrea_rol and not are_rol:
                roluri_de_adaugat.append(rol)
            elif not vrea_rol and are_rol:
                roluri_de_scos.append(rol)

        if roluri_de_adaugat:
            await member.add_roles(*roluri_de_adaugat, reason="Schimbare jocuri")
        if roluri_de_scos:
            await member.remove_roles(*roluri_de_scos, reason="Schimbare jocuri")

        # Dacă nu mai are niciun joc, scoatem și Gamer și Verified
        await asyncio.sleep(1)
        member = await guild.fetch_member(member.id)
        role_names_now = [r.name for r in member.roles]
        are_joc = any(j in role_names_now for j in JOCURI_GAMER)

        if not are_joc:
            rol_gamer = discord.utils.get(guild.roles, name=ROL_GAMER)
            rol_verified = discord.utils.get(guild.roles, name=ROL_VERIFIED)
            to_remove = []
            if rol_gamer and rol_gamer in member.roles:
                to_remove.append(rol_gamer)
            if rol_verified and rol_verified in member.roles:
                to_remove.append(rol_verified)
            if to_remove:
                await member.remove_roles(*to_remove, reason="Niciun joc selectat")
        else:
            # Are jocuri — verificăm dacă trebuie dat Verified
            await verifica_si_da_verified(member, guild)

        await interaction.response.send_message("✅ Rolurile de jocuri au fost actualizate!", ephemeral=True)


class VerificareGamerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verificare Gaming", style=discord.ButtonStyle.success, emoji="🎮", custom_id="verificare_gamer_btn")
    async def verificare_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        rol = discord.utils.get(interaction.guild.roles, name=ROL_GAMER)
        member_role_names = [r.name for r in interaction.user.roles]

        if rol and rol in interaction.user.roles:
            # Are deja Gamer — toggle dropdown
            view = discord.ui.View(timeout=120)
            view.add_item(JocToggleDropdown(member_role_names))
            await interaction.response.send_message(
                "## 🎮 Gestionează jocurile tale\n\n✅ = ai rolul | ➕ = nu ai rolul\nSelectează jocurile dorite:",
                view=view, ephemeral=True
            )
            return
        await interaction.response.send_message(
            "## 🎮 Alege jocul/jocurile tale",
            view=DropdownGamerView(), ephemeral=True
        )


# ──────────────────────────────────────────────
# GIVEAWAY
# ──────────────────────────────────────────────

class GiveawayModal(discord.ui.Modal, title="Creează Giveaway"):
    premiu = discord.ui.TextInput(label="Premiu", placeholder="ex: 1.000.000 Yang", max_length=100)
    durata = discord.ui.TextInput(
        label="Durată",
        placeholder="ex: 3d, 2h, 30m, 1d12h",
        max_length=20
    )
    membri_minim = discord.ui.TextInput(
        label="Membri minim pentru start (opțional)",
        placeholder="ex: 50 — lasă gol dacă nu e necesar",
        required=False,
        max_length=6
    )
    conditii = discord.ui.TextInput(
        label="Condiții și detalii",
        placeholder="ex: Subscribe YouTube: https://...\nFollow Instagram: https://...",
        required=False,
        max_length=1000,
        style=discord.TextStyle.paragraph
    )

    def __init__(self, mentioneaza_everyone: bool = True, numar_castigatori: int = 1):
        super().__init__()
        self.mentioneaza_everyone = mentioneaza_everyone
        self.numar_castigatori = numar_castigatori

    async def on_submit(self, interaction: discord.Interaction):
        secunde_durata = parse_durata(self.durata.value)
        if not secunde_durata:
            await interaction.response.send_message(
                "❌ Format durată invalid. Folosește ex: `3d`, `2h`, `30m`, `1d12h`.", ephemeral=True
            )
            return
        if secunde_durata > 365 * 86400:
            await interaction.response.send_message("❌ Durata maximă e 365 de zile.", ephemeral=True)
            return

        membri_min = None
        if self.membri_minim.value.strip():
            try:
                membri_min = int(self.membri_minim.value.strip())
                if membri_min < 1:
                    raise ValueError
            except ValueError:
                await interaction.response.send_message("❌ Numărul de membri trebuie să fie un număr pozitiv.", ephemeral=True)
                return

        canal = bot.get_channel(CANAL_GIVEAWAY_ID)
        if not canal:
            await interaction.response.send_message("❌ Canalul de giveaway nu a fost găsit.", ephemeral=True)
            return

        guild = interaction.guild
        pornit = True
        end_time = datetime.utcnow() + timedelta(seconds=secunde_durata)

        if membri_min and guild.member_count < membri_min:
            pornit = False

        data = {
            "participanti": set(),
            "invite_codes": {},
            "invitati_de": {},
            "premiu": self.premiu.value.strip(),
            "end_time": end_time,
            "secunde_durata": secunde_durata,
            "conditii": self.conditii.value.strip(),
            "canal_id": CANAL_GIVEAWAY_ID,
            "membri_minim": membri_min,
            "pornit": pornit,
            "mentioneaza_everyone": self.mentioneaza_everyone,
            "numar_castigatori": self.numar_castigatori,
        }

        view = GiveawayView()
        mesaj_mention = "@everyone" if self.mentioneaza_everyone else None
        msg = await canal.send(mesaj_mention, embed=embed_giveaway(data, guild), view=view)
        data["msg_id"] = msg.id
        giveaway_data[msg.id] = data
        save_giveaway_data()

        try:
            await interaction.message.delete()
        except Exception:
            pass

        await interaction.response.send_message("✅ Giveaway creat cu succes!", ephemeral=True, delete_after=5)

        if pornit:
            asyncio.create_task(countdown_giveaway(msg.id, secunde_durata))
        else:
            if not verifica_membrii_giveaway.is_running():
                verifica_membrii_giveaway.start()


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
        user = interaction.user

        if user.id in data["participanti"]:
            await interaction.response.send_message("✅ Ești deja înscris!", ephemeral=True)
            return

        conditii = data.get("conditii", "").strip()
        mesaj = f"Completează condițiile și apasă **Confirm înscriere**:\n\n{conditii}" if conditii else "Apasă **Confirm înscriere** pentru a participa."
        await interaction.response.send_message(mesaj, view=ConfirmView(msg_id), ephemeral=True)


async def inscrie_participant_giveaway(msg_id: int, user: discord.User, guild: discord.Guild, adaugat_manual: bool = False):
    """Înscrie un user la giveaway — folosit de butonul Confirm și de /adauga-participant.
    Returnează True dacă s-a înscris cu succes, False dacă era deja înscris sau giveaway-ul nu există."""
    if msg_id not in giveaway_data:
        return False

    data = giveaway_data[msg_id]
    if user.id in data["participanti"]:
        return False

    data["participanti"].add(user.id)
    total = len(data["participanti"])

    # Generăm invitație unică doar dacă userul nu are deja una pentru acest giveaway
    if data.get("membri_minim") and user.id not in data["invite_codes"]:
        invite = await genereaza_invite(guild)
        if invite:
            data["invite_codes"][user.id] = invite.code
            invite_tracker[invite.code] = user.id
            try:
                embed_dm = discord.Embed(
                    title="🎟️ Linkul tău de invitație",
                    description=(
                        f"Ești înscris la giveaway! 🎉\n\n"
                        f"**Invitațiile pe server îți aduc șanse în plus:**\n"
                        f"1 invitație = 1 ticket bonus la tragerea la sorți\n\n"
                        f"**Linkul tău unic:**\n{invite.url}\n\n"
                        f"Cu cât inviți mai mulți prieteni, cu atât ai șanse mai mari!"
                    ),
                    color=0xFEE75C
                )
                embed_dm.set_footer(text="Hydra Prestige • Metin2 Community")
                await user.send(embed=embed_dm)
            except discord.Forbidden:
                pass

    save_giveaway_data()

    # Notificare în canalul de log
    canal_log = bot.get_channel(CANAL_LOG_GIVEAWAY_ID)
    if canal_log:
        sufix = " *(adăugat manual)*" if adaugat_manual else ""
        try:
            await canal_log.send(
                f"📝 **{user.display_name}** s-a înscris la giveaway-ul **{data['premiu']}**{sufix}\n"
                f"📊 Total participanți: **{total}**"
            )
        except Exception:
            pass

    return True


class ConfirmView(discord.ui.View):
    def __init__(self, msg_id: int):
        super().__init__(timeout=120)
        self.msg_id = msg_id

    @discord.ui.button(label="✅ Confirm înscriere", style=discord.ButtonStyle.primary)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.msg_id not in giveaway_data:
            await interaction.response.send_message("❌ Giveaway-ul nu mai este activ.", ephemeral=True)
            return

        succes = await inscrie_participant_giveaway(self.msg_id, interaction.user, interaction.guild)
        if not succes:
            await interaction.response.send_message("✅ Ești deja înscris!", ephemeral=True)
            return

        total = len(giveaway_data[self.msg_id]["participanti"])
        await interaction.response.send_message(
            f"🎉 Ești înscris! Mult succes!\n📊 Participanți: **{total}**",
            ephemeral=True
        )


async def countdown_giveaway(msg_id: int, secunde: int):
    await asyncio.sleep(secunde)
    await finalizeaza_giveaway(msg_id)


async def finalizeaza_giveaway(msg_id: int):
    """Extrage câștigătorul unui giveaway — apelabil din countdown sau manual."""
    if msg_id not in giveaway_data:
        return
    data = giveaway_data[msg_id]
    canal = bot.get_channel(data["canal_id"])
    if not canal:
        return

    # Dezactivăm mesajul original (butonul Participă) dacă încă există
    try:
        msg_original = await canal.fetch_message(msg_id)
        embed_vechi = msg_original.embeds[0] if msg_original.embeds else None
        if embed_vechi:
            embed_vechi.description += "\n\n**🔒 Acest giveaway s-a încheiat.**"
        view_dezactivat = discord.ui.View(timeout=None)
        await msg_original.edit(embed=embed_vechi, view=view_dezactivat)
    except Exception:
        pass

    participanti = list(data["participanti"])
    if not participanti:
        await canal.send("🎉 Giveaway-ul s-a încheiat dar nu a existat niciun participant.")
        del giveaway_data[msg_id]
        save_giveaway_data()
        return

    tickete = list(participanti)
    for user_id in participanti:
        bonus = get_invite_count(user_id)
        tickete.extend([user_id] * bonus)

    numar_castigatori = min(data.get("numar_castigatori", 1), len(participanti))
    castigatori_ids = []
    tickete_ramase = list(tickete)
    for _ in range(numar_castigatori):
        castigator_id = random.choice(tickete_ramase)
        castigatori_ids.append(castigator_id)
        # Scoatem toate ticketele câștigătorului ca să nu fie ales din nou
        tickete_ramase = [t for t in tickete_ramase if t != castigator_id]
        if not tickete_ramase:
            break

    linii_castigatori = []
    for cid in castigatori_ids:
        castigator = canal.guild.get_member(cid)
        nume = castigator.mention if castigator else f"<@{cid}>"
        linii_castigatori.append(nume)

    if len(linii_castigatori) == 1:
        castigatori_text = f"🎉 **Câștigătorul este:** {linii_castigatori[0]}"
    else:
        lista_text = "\n".join(f"🎉 {n}" for n in linii_castigatori)
        castigatori_text = f"🎉 **Câștigătorii sunt:**\n{lista_text}"

    embed = discord.Embed(
        title="🏆 Giveaway încheiat!",
        description=(
            f"**Premiu:** {data['premiu']}\n\n"
            f"{castigatori_text}\n\n"
            f"📊 Total participanți: **{len(participanti)}**\n"
            f"🎟️ Total tickete: **{len(tickete)}**\n\n"
            f"Mulțumim tuturor pentru participare și vă mai așteptăm!"
        ),
        color=0x57F287
    )
    embed.set_footer(text="Hydra Prestige • Metin2 Community")
    mesaj_mention = "@everyone" if data.get("mentioneaza_everyone", True) else None
    await canal.send(mesaj_mention, embed=embed)

    # Salvăm în istoric pentru posibil reroll ulterior
    giveaway_history[msg_id] = {
        "premiu": data["premiu"],
        "participanti": set(participanti),
        "canal_id": data["canal_id"],
    }
    save_giveaway_history()

    del giveaway_data[msg_id]
    save_giveaway_data()


# ──────────────────────────────────────────────
# SISTEM CUFERE — Joc de ghicit
# ──────────────────────────────────────────────

cufere_data = {}
# { msg_id: { intrebare, end_time, secunde_durata, canal_id, raspunsuri: [(user_id, text, timestamp)] } }


def embed_cufere(data: dict) -> discord.Embed:
    if not data.get("incheiat"):
        timestamp = int(data["end_time"].timestamp())
        status = f"**⏰ Se încheie:** <t:{timestamp}:R>"
    else:
        status = "**🔒 Acest joc s-a încheiat.**"

    desc = (
        f"**{data['intrebare']}**\n\n"
        f"Apasă butonul **Ghicește** și scrie răspunsul tău!\n\n"
        f"{status}"
    )
    embed = discord.Embed(title="📦 GHICEȘTE ȘI CÂȘTIGĂ", description=desc, color=0xE67E22)
    embed.set_footer(text="Hydra Prestige • Metin2 Community")
    return embed


class CufereRaspunsModal(discord.ui.Modal, title="Răspunsul tău"):
    raspuns = discord.ui.TextInput(
        label="Răspunsul tău",
        placeholder="ex: 5 cufere",
        max_length=100
    )

    def __init__(self, msg_id: int):
        super().__init__()
        self.msg_id = msg_id

    async def on_submit(self, interaction: discord.Interaction):
        if self.msg_id not in cufere_data:
            await interaction.response.send_message("❌ Jocul nu mai este activ.", ephemeral=True)
            return

        data = cufere_data[self.msg_id]
        user = interaction.user

        # Verificăm dacă userul a răspuns deja — îi actualizăm răspunsul
        existing_idx = None
        for idx, (uid, _, _) in enumerate(data["raspunsuri"]):
            if uid == user.id:
                existing_idx = idx
                break

        if existing_idx is not None:
            data["raspunsuri"][existing_idx] = (user.id, self.raspuns.value.strip(), datetime.utcnow())
            await interaction.response.send_message("✅ Răspunsul tău a fost actualizat!", ephemeral=True)
        else:
            data["raspunsuri"].append((user.id, self.raspuns.value.strip(), datetime.utcnow()))
            await interaction.response.send_message("✅ Răspunsul tău a fost înregistrat!", ephemeral=True)


class CufereView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📦 Ghicește", style=discord.ButtonStyle.primary, custom_id="cufere_ghiceste")
    async def ghiceste(self, interaction: discord.Interaction, button: discord.ui.Button):
        msg_id = interaction.message.id
        if msg_id not in cufere_data:
            await interaction.response.send_message("❌ Jocul nu mai este activ.", ephemeral=True)
            return
        await interaction.response.send_modal(CufereRaspunsModal(msg_id))


class CufereModal(discord.ui.Modal, title="Creează Joc Cufere"):
    intrebare = discord.ui.TextInput(
        label="Întrebare / Premiu",
        placeholder="ex: Câte cufere credeți că dropez?",
        max_length=200
    )
    durata = discord.ui.TextInput(
        label="Durată",
        placeholder="ex: 5m, 1h, 30m",
        max_length=20
    )

    async def on_submit(self, interaction: discord.Interaction):
        secunde_durata = parse_durata(self.durata.value)
        if not secunde_durata:
            await interaction.response.send_message(
                "❌ Format durată invalid. Folosește ex: `5m`, `1h`, `30m`.", ephemeral=True
            )
            return

        canal = interaction.channel
        end_time = datetime.utcnow() + timedelta(seconds=secunde_durata)

        data = {
            "intrebare": self.intrebare.value.strip(),
            "end_time": end_time,
            "secunde_durata": secunde_durata,
            "canal_id": canal.id,
            "raspunsuri": [],
            "incheiat": False,
        }

        view = CufereView()
        msg = await canal.send(embed=embed_cufere(data), view=view)
        cufere_data[msg.id] = data

        try:
            await interaction.message.delete()
        except Exception:
            pass

        await interaction.response.send_message("✅ Joc Cufere creat cu succes!", ephemeral=True, delete_after=5)
        asyncio.create_task(finalizeaza_cufere(msg.id, secunde_durata))


async def finalizeaza_cufere(msg_id: int, secunde: int):
    await asyncio.sleep(secunde)
    if msg_id not in cufere_data:
        return
    data = cufere_data[msg_id]
    data["incheiat"] = True
    canal = bot.get_channel(data["canal_id"])
    if not canal:
        return

    try:
        msg_original = await canal.fetch_message(msg_id)
        await msg_original.edit(embed=embed_cufere(data), view=discord.ui.View(timeout=None))
    except Exception:
        pass

    if not data["raspunsuri"]:
        await canal.send("📦 Jocul s-a încheiat dar nu a existat niciun răspuns.")
        del cufere_data[msg_id]
        return

    linii = []
    for user_id, raspuns, _ in data["raspunsuri"]:
        linii.append(f"<@{user_id}> — **{raspuns}**")

    embed = discord.Embed(
        title="📦 Răspunsurile primite",
        description=(
            f"**{data['intrebare']}**\n\n" + "\n".join(linii)
        ),
        color=0xE67E22
    )
    embed.set_footer(text="Hydra Prestige • Metin2 Community")
    await canal.send(embed=embed)
    del cufere_data[msg_id]


# ──────────────────────────────────────────────
# WELCOME / LEAVE + INVITE TRACKING
# ──────────────────────────────────────────────

@bot.event
async def on_member_join(member: discord.Member):
    rol_unverified = discord.utils.get(member.guild.roles, name=ROL_UNVERIFIED)
    if rol_unverified:
        await member.add_roles(rol_unverified, reason="Rol implicit la intrare")

    inviter = None
    inviter_count = 0
    try:
        invites_after = await member.guild.invites()
        invites_before = cached_invites.get(member.guild.id, {})

        for invite in invites_after:
            uses_before = invites_before.get(invite.code, 0)
            if invite.uses > uses_before:
                if invite.inviter:
                    inviter = invite.inviter
                    add_invite(inviter.id, member.id)
                    inviter_count = get_invite_count(inviter.id)
                    if invite.code in invite_tracker:
                        for msg_id, data in giveaway_data.items():
                            if invite.code in data.get("invite_codes", {}).values():
                                if "invitati_de" not in data:
                                    data["invitati_de"] = {}
                                data["invitati_de"][member.id] = invite_tracker[invite.code]
                break

        cached_invites[member.guild.id] = {i.code: i.uses for i in invites_after}

    except Exception as e:
        print(f"⚠️  Eroare invite tracking: {e}")

    canal = bot.get_channel(CANAL_WELCOME_ID)
    if canal:
        if inviter:
            desc = (
                f"Bun venit pe server, {member.mention}!\n\n"
                f"📨 Invitat de **{inviter.display_name}** "
                f"(total invitații: **{inviter_count}**)\n\n"
                f"Mergi în <#{CANAL_VERIFICARE_ID}> pentru a obține acces."
            )
        else:
            desc = (
                f"Bun venit pe server, {member.mention}!\n\n"
                f"Mergi în <#{CANAL_VERIFICARE_ID}> pentru a obține acces."
            )

        embed = discord.Embed(title="👋 Membru nou!", description=desc, color=0x57F287)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Membri: {member.guild.member_count}")
        await canal.send(embed=embed)


@bot.event
async def on_member_remove(member: discord.Member):
    inviter_id = remove_invite(member.id)

    canal = bot.get_channel(CANAL_WELCOME_ID)
    if canal:
        if inviter_id:
            inviter_count = get_invite_count(inviter_id)
            desc = f"**{member.name}** a părăsit serverul.\n📉 Invitația lui **<@{inviter_id}>** a fost scăzută (total: **{inviter_count}**)"
        else:
            desc = f"**{member.name}** a părăsit serverul."

        embed = discord.Embed(title="🚪 Membru plecat", description=desc, color=0xED4245)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Membri: {member.guild.member_count}")
        await canal.send(embed=embed)

    try:
        invites = await member.guild.invites()
        cached_invites[member.guild.id] = {i.code: i.uses for i in invites}
    except Exception:
        pass


# ──────────────────────────────────────────────
# COMENZI
# ──────────────────────────────────────────────

@tree.command(name="mute", description="Dezactivează scrisul unui membru")
@app_commands.describe(membru="Membrul de mutat", motiv="Motivul")
async def mute(interaction: discord.Interaction, membru: discord.Member, motiv: str = "Nespecificat"):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
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
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
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
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
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
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
        return
    try:
        await membru.ban(reason=motiv)
        embed = discord.Embed(title="🔨 Ban aplicat", description=f"**Membru:** {membru.name}\n**Motiv:** {motiv}", color=0xED4245)
        embed.set_footer(text=f"Acțiune de: {interaction.user.name}")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Nu am permisiuni suficiente.", ephemeral=True)


class AnuntModal(discord.ui.Modal, title="Creează Anunț"):
    titlu = discord.ui.TextInput(label="Titlu", placeholder="ex: Eveniment nou: Duelul Profeților", max_length=256)
    text = discord.ui.TextInput(
        label="Conținut",
        placeholder="Scrie aici textul complet al anunțului...",
        style=discord.TextStyle.paragraph,
        max_length=4000
    )
    imagine = discord.ui.TextInput(
        label="Link imagine (opțional)",
        placeholder="https://...",
        required=False,
        max_length=300
    )

    def __init__(self, canal_id: int):
        super().__init__()
        self.canal_id = canal_id

    async def on_submit(self, interaction: discord.Interaction):
        canal = bot.get_channel(self.canal_id)
        if not canal:
            await interaction.response.send_message("❌ Canalul nu a fost găsit.", ephemeral=True)
            return

        embed = discord.Embed(
            title=self.titlu.value.strip(),
            description=self.text.value.strip(),
            color=0x5865F2
        )
        if self.imagine.value.strip():
            embed.set_image(url=self.imagine.value.strip())
        embed.set_footer(text=f"Anunț de {interaction.user.display_name} • Hydra Prestige")
        embed.timestamp = datetime.utcnow()

        await canal.send(embed=embed)
        await interaction.response.send_message(f"✅ Anunț postat în <#{self.canal_id}>!", ephemeral=True)


@tree.command(name="anunt", description="Postează un anunț formatat ca embed într-un canal ales")
@app_commands.describe(canal="Canalul în care se postează anunțul")
async def anunt_cmd(interaction: discord.Interaction, canal: discord.TextChannel):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
        return
    await interaction.response.send_modal(AnuntModal(canal.id))


@tree.command(name="cufere", description="Creează un joc de ghicit (ex: câte cufere dropezi)")
async def cufere_cmd(interaction: discord.Interaction):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
        return
    await interaction.response.send_modal(CufereModal())


@tree.command(name="help", description="Vezi toate comenzile disponibile ale botului")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📖 Comenzi disponibile",
        description="Lista completă a comenzilor botului Confucius.",
        color=0x5865F2
    )
    embed.add_field(
        name="🎉 Giveaway",
        value=(
            "`/giveaway` — creează un giveaway nou\n"
            "`/anuleaza-giveaway [message_id]` — anulează un giveaway activ\n"
            "`/extrage-giveaway [message_id]` — extrage câștigătorul înainte de termen\n"
            "`/participanti-giveaway [message_id]` — vezi participanții activi\n"
            "`/reroll-giveaway [message_id]` — extrage alt câștigător dacă cel curent nu îndeplinește condițiile\n"
            "Right-click pe membru → Apps → **Adaugă la giveaway** — adaugă manual un participant"
        ),
        inline=False
    )
    embed.add_field(
        name="📦 Cufere",
        value="`/cufere` — creează un joc de ghicit (ex: câte cufere dropezi)",
        inline=False
    )
    embed.add_field(
        name="📊 Invitații",
        value=(
            "`/invitatii [@membru]` — vezi câte invitații a adus un membru\n"
            "`/leaderboard-invitatii` — clasamentul membrilor după invitații\n"
            "`/seteaza-invitatii [@membru] [numar]` — setează manual invitațiile (admin)"
        ),
        inline=False
    )
    embed.add_field(
        name="📢 Anunțuri",
        value="`/anunt [canal]` — postează un anunț formatat ca embed în orice canal",
        inline=False
    )
    embed.add_field(
        name="🛡️ Moderare",
        value=(
            "`/mute [membru] [motiv]` — dezactivează scrisul\n"
            "`/timeout [membru] [minute] [motiv]` — aplică timeout\n"
            "`/kick [membru] [motiv]` — dă afară un membru\n"
            "`/ban [membru] [motiv]` — banează permanent"
        ),
        inline=False
    )
    embed.set_footer(text="Hydra Prestige • Metin2 Community")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="giveaway", description="Creează un giveaway")
@app_commands.describe(
    mentioneaza_everyone="Trimite @everyone la postare? (implicit: da)",
    numar_castigatori="Câți câștigători să extragă? (implicit: 1)"
)
async def giveaway_cmd(interaction: discord.Interaction, mentioneaza_everyone: bool = True, numar_castigatori: int = 1):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
        return
    if numar_castigatori < 1 or numar_castigatori > 20:
        await interaction.response.send_message("❌ Numărul de câștigători trebuie să fie între 1 și 20.", ephemeral=True)
        return
    await interaction.response.send_modal(GiveawayModal(mentioneaza_everyone, numar_castigatori))


class AlegeGiveawayDropdown(discord.ui.Select):
    """Dropdown pentru alegerea giveaway-ului când sunt mai multe active."""
    def __init__(self, target_user: discord.Member):
        self.target_user = target_user
        options = []
        for msg_id, data in giveaway_data.items():
            label = data["premiu"][:90]
            options.append(discord.SelectOption(label=label, value=str(msg_id)))
        super().__init__(placeholder="Alege giveaway-ul...", options=options[:25])

    async def callback(self, interaction: discord.Interaction):
        msg_id = int(self.values[0])
        succes = await inscrie_participant_giveaway(msg_id, self.target_user, interaction.guild, adaugat_manual=True)
        if succes:
            await interaction.response.send_message(
                f"✅ {self.target_user.mention} a fost adăugat la giveaway-ul **{giveaway_data[msg_id]['premiu']}**!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"⚠️ {self.target_user.mention} este deja înscris la acest giveaway.",
                ephemeral=True
            )


@tree.context_menu(name="Adaugă la giveaway")
async def adauga_participant_context(interaction: discord.Interaction, member: discord.Member):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
        return

    if not giveaway_data:
        await interaction.response.send_message("❌ Nu există niciun giveaway activ momentan.", ephemeral=True)
        return

    if len(giveaway_data) == 1:
        msg_id = list(giveaway_data.keys())[0]
        succes = await inscrie_participant_giveaway(msg_id, member, interaction.guild, adaugat_manual=True)
        if succes:
            await interaction.response.send_message(
                f"✅ {member.mention} a fost adăugat la giveaway-ul **{giveaway_data[msg_id]['premiu']}**!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"⚠️ {member.mention} este deja înscris la acest giveaway.",
                ephemeral=True
            )
        return

    view = discord.ui.View(timeout=60)
    view.add_item(AlegeGiveawayDropdown(member))
    await interaction.response.send_message(
        f"Alege giveaway-ul pentru a-l adăuga pe {member.mention}:",
        view=view, ephemeral=True
    )


@tree.command(name="reroll-giveaway", description="Extrage alt câștigător dacă cel curent nu îndeplinește condițiile")
@app_commands.describe(message_id="ID-ul mesajului giveaway-ului încheiat", exclude="ID-ul userului de exclus (opțional)")
async def reroll_giveaway(interaction: discord.Interaction, message_id: str, exclude: str = None):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
        return

    try:
        msg_id = int(message_id.strip())
    except ValueError:
        await interaction.response.send_message("❌ ID invalid.", ephemeral=True)
        return

    # Pentru reroll căutăm în istoricul mesajelor, deoarece giveaway-ul e deja șters din giveaway_data
    # Folosim un mecanism simplu: cerem staff-ul să dea reroll imediat după extragere, cât mai există backup
    backup = giveaway_history.get(msg_id)
    if not backup:
        await interaction.response.send_message(
            "❌ Nu mai există date pentru acest giveaway (s-a încheiat și nu mai e în istoric).", ephemeral=True
        )
        return

    participanti = list(backup["participanti"])
    exclude_id = None
    if exclude:
        try:
            exclude_id = int(exclude.strip().replace("<@", "").replace(">", "").replace("!", ""))
        except ValueError:
            exclude_id = None

    if exclude_id and exclude_id in participanti:
        participanti.remove(exclude_id)

    if not participanti:
        await interaction.response.send_message("❌ Nu mai există participanți eligibili pentru reroll.", ephemeral=True)
        return

    tickete = list(participanti)
    for uid in participanti:
        tickete.extend([uid] * get_invite_count(uid))

    castigator_id = random.choice(tickete)
    castigator = interaction.guild.get_member(castigator_id)
    nume = castigator.mention if castigator else f"<@{castigator_id}>"

    canal = bot.get_channel(backup["canal_id"])
    embed = discord.Embed(
        title="🔄 Reroll Giveaway!",
        description=(
            f"**Premiu:** {backup['premiu']}\n\n"
            f"🎉 **Noul câștigător este:** {nume}\n\n"
            f"Mulțumim pentru înțelegere!"
        ),
        color=0x57F287
    )
    embed.set_footer(text="Hydra Prestige • Metin2 Community")
    if canal:
        await canal.send(embed=embed)
    await interaction.response.send_message("✅ Reroll efectuat cu succes!", ephemeral=True)


@tree.command(name="participanti-giveaway", description="Vezi câți participanți sunt la un giveaway activ")
@app_commands.describe(message_id="ID-ul mesajului giveaway-ului")
async def participanti_giveaway(interaction: discord.Interaction, message_id: str):
    try:
        msg_id = int(message_id.strip())
    except ValueError:
        await interaction.response.send_message("❌ ID invalid.", ephemeral=True)
        return

    if msg_id not in giveaway_data:
        await interaction.response.send_message("❌ Nu există niciun giveaway activ cu acest ID.", ephemeral=True)
        return

    data = giveaway_data[msg_id]
    participanti = list(data["participanti"])
    total_tickete = len(participanti)
    for uid in participanti:
        total_tickete += get_invite_count(uid)

    embed = discord.Embed(
        title="📊 Participanți giveaway",
        description=(
            f"**Premiu:** {data['premiu']}\n\n"
            f"👥 **Participanți:** {len(participanti)}\n"
            f"🎟️ **Total tickete:** {total_tickete}"
        ),
        color=0x5865F2
    )

    if participanti and len(participanti) <= 30:
        lista = "\n".join(f"<@{uid}>" for uid in participanti)
        embed.add_field(name="Lista participanți", value=lista, inline=False)

    embed.set_footer(text="Hydra Prestige • Metin2 Community")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="extrage-giveaway", description="Extrage câștigătorul unui giveaway înainte de termen")
@app_commands.describe(message_id="ID-ul mesajului giveaway-ului")
async def extrage_giveaway(interaction: discord.Interaction, message_id: str):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
        return
    try:
        msg_id = int(message_id.strip())
    except ValueError:
        await interaction.response.send_message("❌ ID invalid.", ephemeral=True)
        return

    if msg_id not in giveaway_data:
        await interaction.response.send_message("❌ Nu există niciun giveaway activ cu acest ID.", ephemeral=True)
        return

    data = giveaway_data[msg_id]
    canal = bot.get_channel(data["canal_id"])

    await finalizeaza_giveaway(msg_id)
    await interaction.response.send_message("✅ Giveaway extras cu succes, înainte de termen!", ephemeral=True)


@tree.command(name="anuleaza-giveaway", description="Anulează un giveaway activ")
@app_commands.describe(message_id="ID-ul mesajului giveaway-ului")
async def anuleaza_giveaway(interaction: discord.Interaction, message_id: str):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
        return
    try:
        msg_id = int(message_id.strip())
    except ValueError:
        await interaction.response.send_message("❌ ID invalid.", ephemeral=True)
        return

    if msg_id not in giveaway_data:
        await interaction.response.send_message("❌ Nu există niciun giveaway activ cu acest ID.", ephemeral=True)
        return

    data = giveaway_data[msg_id]
    canal = bot.get_channel(data["canal_id"])

    try:
        msg = await canal.fetch_message(msg_id)
        await msg.delete()
    except Exception:
        pass

    embed = discord.Embed(
        title="❌ Giveaway anulat",
        description=f"Giveaway-ul pentru **{data['premiu']}** a fost anulat de {interaction.user.mention}.",
        color=0xED4245
    )
    embed.set_footer(text="Hydra Prestige • Metin2 Community")
    await canal.send(embed=embed)
    del giveaway_data[msg_id]
    save_giveaway_data()
    await interaction.response.send_message("✅ Giveaway anulat cu succes.", ephemeral=True)


@tree.command(name="invitatii", description="Vezi câte invitații ai adus pe server")
@app_commands.describe(membru="Membrul de verificat (lasă gol pentru tine)")
async def invitatii_cmd(interaction: discord.Interaction, membru: discord.Member = None):
    target = membru or interaction.user
    count = get_invite_count(target.id)
    inviter_id = get_inviter(target.id)
    inviter_text = f"\n📨 Invitat de: <@{inviter_id}>" if inviter_id else ""
    embed = discord.Embed(
        title="📊 Statistici invitații",
        description=f"**{target.display_name}** a adus **{count}** membre pe server.{inviter_text}",
        color=0x5865F2
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="leaderboard-invitatii", description="Vezi clasamentul membrilor după numărul de invitații")
async def leaderboard_invitatii_cmd(interaction: discord.Interaction):
    lista = get_leaderboard_invitatii()
    if not lista:
        await interaction.response.send_message("📊 Nimeni nu a adus încă invitații.", ephemeral=True)
        return

    linii = []
    medalii = ["🥇", "🥈", "🥉"]
    for idx, (user_id, count) in enumerate(lista[:15]):
        prefix = medalii[idx] if idx < 3 else f"`{idx + 1}.`"
        linii.append(f"{prefix} <@{user_id}> — **{count}** invitații")

    embed = discord.Embed(
        title="🏆 Clasament invitații",
        description="\n".join(linii),
        color=0xF1C40F
    )
    embed.set_footer(text="Hydra Prestige • Metin2 Community")
    await interaction.response.send_message(embed=embed)


@tree.command(name="seteaza-invitatii", description="Setează manual numărul de invitații al unui membru")
@app_commands.describe(membru="Membrul de modificat", numar="Numărul nou de invitații")
async def seteaza_invitatii_cmd(interaction: discord.Interaction, membru: discord.Member, numar: int):
    if not are_rol_staff(interaction.user):
        await interaction.response.send_message("❌ Nu ai permisiunea.", ephemeral=True)
        return
    if numar < 0:
        await interaction.response.send_message("❌ Numărul nu poate fi negativ.", ephemeral=True)
        return

    set_invite_count(membru.id, numar)
    embed = discord.Embed(
        title="✅ Invitații actualizate",
        description=f"**{membru.display_name}** are acum **{numar}** invitații.",
        color=0x57F287
    )
    embed.set_footer(text=f"Modificat de: {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ──────────────────────────────────────────────
# ON READY
# ──────────────────────────────────────────────

@bot.event
async def on_ready():
    global youtube_channel_id_resolved
    print(f"✅ Bot pornit ca {bot.user}")

    try:
        guild = bot.guilds[0]
        owner = guild.get_member(OWNER_ID)
        if owner:
            await owner.send(f"✅ Botul a pornit/restartat cu succes la `{datetime.utcnow().strftime('%d.%m.%Y %H:%M')} UTC`")
    except Exception:
        pass

    bot.add_view(VerificareMetin2View())
    bot.add_view(DropdownMetin2View())
    bot.add_view(VerificareGamerView())
    bot.add_view(DropdownGamerView())
    bot.add_view(GiveawayView())
    bot.add_view(CufereView())

    await tree.sync()
    print("✅ Slash commands sincronizate")

    for guild in bot.guilds:
        try:
            invites = await guild.invites()
            cached_invites[guild.id] = {i.code: i.uses for i in invites}
            print(f"✅ Cache invitații încărcat pentru {guild.name}")
        except Exception:
            pass

    update_member_counter.start()
    print("✅ Counter membri pornit")

    # Reîncărcăm giveaway-urile active și reluăm countdown-urile
    giveaway_data.update(load_giveaway_data())
    giveaway_history.update(load_giveaway_history())
    if giveaway_data:
        are_pending_membri = False
        for msg_id, data in giveaway_data.items():
            if data.get("pornit", True):
                ramase = (data["end_time"] - datetime.utcnow()).total_seconds()
                if ramase > 0:
                    asyncio.create_task(countdown_giveaway(msg_id, ramase))
                else:
                    asyncio.create_task(finalizeaza_giveaway(msg_id))
            else:
                are_pending_membri = True
        if are_pending_membri and not verifica_membrii_giveaway.is_running():
            verifica_membrii_giveaway.start()
        print(f"✅ {len(giveaway_data)} giveaway(uri) active reluate din JSON")

    if YOUTUBE_API_KEY:
        youtube_channel_id_resolved = await get_youtube_channel_id(YOUTUBE_HANDLE)
        if youtube_channel_id_resolved:
            print(f"✅ YouTube channel ID rezolvat: {youtube_channel_id_resolved}")
            verifica_live.start()
        else:
            print("⚠️  Nu s-a putut rezolva channel ID-ul YouTube.")
    else:
        print("⚠️  YOUTUBE_API_KEY lipsă")

    # Trimitem cele 2 embeds în #get-started
    canal_vs = bot.get_channel(CANAL_VERIFICARE_ID)
    if canal_vs:
        # Ștergem mesajele vechi ale botului
        async for msg in canal_vs.history(limit=20):
            if msg.author == bot.user:
                try:
                    await msg.delete()
                except Exception:
                    pass

        # Embed Metin2
        embed_metin2 = discord.Embed(
            title="⚔️ Verificare Metin2",
            description=(
                "Ești jucător de **Metin2**? Apasă butonul de mai jos pentru a obține "
                "accesul la canalele de Metin2.\n\n"
                "**Vei primi:** `⚔️ Metin2` + rolul serverului tău"
            ),
            color=0xE8B84B
        )
        embed_metin2.set_footer(text="Hydra Prestige • Metin2 Community")
        await canal_vs.send(embed=embed_metin2, view=VerificareMetin2View())

        # Embed Gaming
        embed_gaming = discord.Embed(
            title="🎮 Verificare Gaming",
            description=(
                "Joci **alte jocuri**? Apasă butonul de mai jos pentru a obține "
                "accesul la canalele de gaming.\n\n"
                "**Vei primi:** `🎮 Gamer` + rolul jocului tău"
            ),
            color=0x2ECC71
        )
        embed_gaming.set_footer(text="Hydra Prestige • Community")
        await canal_vs.send(embed=embed_gaming, view=VerificareGamerView())
        print(f"✅ Embeds trimise în #{canal_vs.name}")

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
# test persistence check