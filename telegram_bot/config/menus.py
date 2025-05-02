from telethon import Button

# Main Menu
MAIN_MENU = [
    [Button.inline("📰 Notícias", b"news"),
     Button.inline("🏆 Destaques", b"highlights")],
    [Button.inline("📊 Classificação", b"ranking"),
     Button.inline("👥 Elenco", b"roster")],
    [Button.inline("💬 Comunidade", b"community")]
]

# Community Menu
COMMUNITY_MENU = [
    [Button.inline("💬 Chat dos Fãs", b"fan_chat"),
     Button.inline("📱 Redes Sociais", b"social_media")],
    [Button.inline("🔙 Voltar", b"back")]
]

# Social Media Menu
SOCIAL_MEDIA_MENU = [
    [Button.url("Instagram", "https://www.instagram.com/furiagg/")],
    [Button.url("X (Twitter)", "https://x.com/FURIA")],
    [Button.url("Discord", "https://discord.gg/furia")],
    [Button.url("YouTube", "https://www.youtube.com/@FURIAggCS")],
    [Button.url("Twitch", "https://www.twitch.tv/furiatv")],
    [Button.inline("🔙 Voltar", b"back_community")]
]

# Roster Menu
ROSTER_MENU = [
    [Button.url("FalleN", "https://www.hltv.org/player/2023/fallen")],
    [Button.url("KSCERATO", "https://www.hltv.org/player/15631/kscerato")],
    [Button.url("yuurih", "https://www.hltv.org/player/12553/yuurih")],
    [Button.url("YEKINDAR", "https://www.hltv.org/player/13915/yekindar")],
    [Button.url("molodoy", "https://www.hltv.org/player/24144/molodoy")],
    [Button.url("sidde (Coach)", "https://www.hltv.org/coach/24267/sidde")],
    [Button.inline("🔙 Voltar", b"back")]
] 