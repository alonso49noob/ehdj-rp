# Bot de Discord de FarBeyond

Responde preguntas sobre el mod, conversa con la comunidad y publica un resumen semanal de cambios.
Usa la API de Claude con la documentación del repo (`README.md`, `LEEME_PLAYTEST.md`, `docs/**/*.md`) como base.

## Cuándo responde
- Cuando lo mencionan (`@bot`), le responden a un mensaje suyo o le escriben por DM.
- Siempre, en los canales listados en `CHAT_CHANNEL_IDS` (opcional).
- Resumen semanal (lunes 16:00 UTC) en `ANNOUNCE_CHANNEL_ID`, a partir de `git log` de los últimos 7 días.

## Puesta en marcha
1. En el [portal de desarrolladores](https://discord.com/developers/applications): crea la aplicación, ve a **Bot**,
   activa **Message Content Intent** y copia el token.
2. Invítalo con permisos de ver canales, leer historial, enviar mensajes y responder (OAuth2 → URL Generator → `bot`).
3. Consigue una clave de API en <https://console.anthropic.com>.
4. Configura las variables de `.env.example` en tu hosting (Railway, Fly.io, VPS...). **No subas tokens al repo.**
5. Arranque local:
   ```bash
   cd bot && pip install -r requirements.txt
   export DISCORD_TOKEN=... ANTHROPIC_API_KEY=...
   python bot.py
   ```
   o con Docker, desde la raíz del repo: `docker build -f bot/Dockerfile -t farbeyond-bot . && docker run --env-file bot/.env farbeyond-bot`.

El bot lee la documentación al arrancar: reinícialo (o redespliega) cuando cambien los docs.

## Coste
Por defecto usa `claude-haiku-5-5` con la documentación en caché de prompt, así que cada respuesta cuesta una fracción de céntimo.
Cambia `CLAUDE_MODEL` si quieres respuestas más elaboradas.
