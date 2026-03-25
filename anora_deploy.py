# run_deploy.py (minimal version untuk test ANORA)
import os
import sys
import asyncio
import logging
from pathlib import Path
from aiohttp import web

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-5s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("AMORIA")

sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Import ANORA
from anora.core import get_anora
from anora.chat import get_anora_chat
from anora.database import get_anora_db

# ANORA handlers sederhana
async def nova_command(update, context):
    user_id = update.effective_user.id
    if user_id != settings.admin_id:
        await update.message.reply_text("Maaf, Nova cuma untuk Mas. 💜")
        return
    
    anora = get_anora()
    intro = f"""💜 **NOVA DI SINI, MAS** 💜

{anora.deskripsi_diri()}

{anora.respon_pagi()}

Mas bisa kirim /novastatus buat liat keadaan Nova.
Apa yang Mas mau? *muter-muter rambut*"""
    
    await update.message.reply_text(intro, parse_mode='HTML')

async def novastatus_command(update, context):
    user_id = update.effective_user.id
    if user_id != settings.admin_id:
        await update.message.reply_text("Maaf, cuma Mas yang bisa liat. 💜")
        return
    
    anora = get_anora()
    await update.message.reply_text(anora.format_status(), parse_mode='HTML')

async def anora_chat_handler(update, context):
    user_id = update.effective_user.id
    if user_id != settings.admin_id:
        return
    
    if not context.user_data.get('anora_mode', False):
        return
    
    pesan = update.message.text
    anora_chat = get_anora_chat()
    respons = await anora_chat.process(pesan)
    await update.message.reply_text(respons, parse_mode='HTML')

async def start_command(update, context):
    user_id = update.effective_user.id
    if user_id != settings.admin_id:
        await update.message.reply_text("Halo! Bot ini untuk Mas. 💜")
        return
    
    await update.message.reply_text(
        "💜 **AMORIA + ANORA** 💜\n\n"
        "Kirim /nova untuk panggil Nova\n"
        "Kirim /novastatus untuk liat keadaan Nova",
        parse_mode='HTML'
    )

async def main():
    """Start bot"""
    # Create application
    app = ApplicationBuilder().token(settings.telegram_token).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("nova", nova_command))
    app.add_handler(CommandHandler("novastatus", novastatus_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anora_chat_handler))
    
    # Initialize ANORA database
    db = await get_anora_db()
    logger.info("✅ ANORA database ready")
    
    # Start bot
    await app.initialize()
    await app.start()
    
    # Set webhook
    railway_url = os.getenv('RAILWAY_PUBLIC_DOMAIN')
    if railway_url:
        webhook_url = f"https://{railway_url}/webhook"
        await app.bot.set_webhook(url=webhook_url)
        logger.info(f"✅ Webhook set to {webhook_url}")
        
        # Health check endpoint
        web_app = web.Application()
        async def health(request):
            return web.json_response({"status": "healthy", "bot": "ANORA"})
        web_app.router.add_get('/health', health)
        web_app.router.add_post('/webhook', lambda r: web.Response(text='OK'))
        
        runner = web.AppRunner(web_app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', int(os.getenv('PORT', 8080)))
        await site.start()
        logger.info("🌐 Web server running")
    else:
        # Polling mode
        await app.updater.start_polling()
        logger.info("📡 Polling mode started")
    
    logger.info("💜 AMORIA + ANORA is running!")
    logger.info("   Mas bisa kirim /nova")
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
