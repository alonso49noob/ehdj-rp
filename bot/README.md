# Bot de Discord de FarBeyond

Responde preguntas sobre el mod, conversa con la comunidad y publica un resumen semanal de cambios.
Funciona con **Gemini** o con **Claude**, a tu elección, usando la documentación del repo (`README.md`, `LEEME_PLAYTEST.md`, `docs/**/*.md`) como base.

## Cuándo responde
- Cuando lo mencionan (`@bot`), le responden a un mensaje suyo o le escriben por DM.
- Siempre, en los canales listados en `CHAT_CHANNEL_IDS` (opcional).
- Resumen semanal (lunes 16:00 UTC) en `ANNOUNCE_CHANNEL_ID`, a partir de `git log` de los últimos 7 días.

## Puesta en marcha
1. En el [portal de desarrolladores](https://discord.com/developers/applications): crea la aplicación, ve a **Bot**,
   activa **Message Content Intent** y copia el token.
2. Invítalo con permisos de ver canales, leer historial, enviar mensajes y responder (OAuth2 → URL Generator → `bot`).
3. Consigue una clave de API: Gemini en <https://aistudio.google.com/apikey> (tiene capa gratuita) o Claude en <https://console.anthropic.com>.
4. Configura las variables de `.env.example` en tu hosting (Railway, Fly.io, VPS...). **No subas tokens al repo.**
5. Arranque local:
   ```bash
   cd bot && pip install -r requirements.txt
   export DISCORD_TOKEN=... GEMINI_API_KEY=...   # o ANTHROPIC_API_KEY=...
   python bot.py
   ```
   o con Docker, desde la raíz del repo: `docker build -f bot/Dockerfile -t farbeyond-bot . && docker run --env-file bot/.env farbeyond-bot`.

El bot lee la documentación al arrancar: reinícialo (o redespliega) cuando cambien los docs.

## Proveedor y coste
Si solo defines `GEMINI_API_KEY` usa Gemini (`GEMINI_MODEL`, por defecto `gemini-2.5-flash`); si defines `ANTHROPIC_API_KEY`
usa Claude (`CLAUDE_MODEL`, por defecto `claude-haiku-5-5`, con la documentación en caché de prompt). Si pones ambas, elige con
`LLM_PROVIDER=gemini` o `claude`. Revisa en tu consola los límites y precios vigentes del modelo que elijas.
