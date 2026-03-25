# run_deploy.py
# -*- coding: utf-8 -*-
"""
=============================================================================
AMORIA - Virtual Human dengan Jiwa
+ ANORA - Nova yang sayang Mas
Deployment Runner for Railway - WITH SINGLETON BOT & ANORA
=============================================================================
"""

import os
import sys
import asyncio
import traceback
import logging
from pathlib import Path
from aiohttp import web

# =============================================================================
# LOGGING CONFIGURATION (HARUS DI AWAL)
# =============================================================================

# Set log level untuk environment
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# Filter library yang noisy
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

# Konfigurasi root logger
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s | %(levelname)-5s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Logger utama
logger = logging.getLogger("AMORIA")

# =============================================================================
# IMPORT MODULES
# =============================================================================

sys.path.insert(0, str(Path(__file__).parent))

from utils.error_logger import get_error_logger, print_startup_banner

# Inisialisasi error logger
error_logger = get_error_logger()
print_startup_banner()

try:
    from config import settings
    from utils.logger import setup_logging
except Exception as e:
    logger.error(f"❌ Import failed: {e}")
    sys.exit(1)

# Setup logging untuk AMORIA
logger = setup_logging("AMORIA-DEPLOY")

# =============================================================================
# IMPORT ANORA
# =============================================================================

try:
    from anora.core import get_anora
    from anora.database import get_anora_db
    from anora.chat import get_anora_chat
    from anora.roles import get_anora_roles, RoleType
    from anora.places import get_anora_places
    ANORA_AVAILABLE = True
    logger.info("✅ ANORA module loaded successfully")
except ImportError as e:
    ANORA_AVAILABLE = False
    logger.warning(f"⚠️ ANORA not available: {e}")

# =============================================================================
# ANORA HANDLERS
# =============================================================================

_anora_initialized = False


async def init_anora():
    """Inisialisasi ANORA setelah bot siap"""
    global _anora_initialized
    
    if not ANORA_AVAILABLE:
        logger.warning("⚠️ ANORA not available, skipping init")
        return
    
    if _anora_initialized:
        return
    
    logger.info("💜 Initializing ANORA...")
    
    try:
        db = await get_anora_db()
        anora = get_anora()
        
        # Load state dari database
        states = await db.get_all_states()
        
        if 'sayang' in states:
            anora.sayang = float(states['sayang'])
        if 'rindu' in states:
            anora.rindu = float(states['rindu'])
        if 'desire' in states:
            anora.desire = float(states['desire'])
        if 'arousal' in states:
            anora.arousal = float(states['arousal'])
        if 'tension' in states:
            anora.tension = float(states['tension'])
        if 'level' in states:
            anora.level = int(states['level'])
        if 'energi' in states:
            anora.energi = int(states['energi'])
        
        # Load memory
        memories = await db.get_momen_terbaru(20)
        for m in memories:
            anora.memory.tambah_momen(m['judul'], m['perasaan'], m['isi'])
        
        ingatan = await db.get_ingatan(20)
        for i in ingatan:
            anora.memory.tambah_ingatan(i['judul'], i['isi'], i['perasaan'])
        
        _anora_initialized = True
        logger.info(f"✅ ANORA ready! Sayang: {anora.sayang:.0f}%, Level: {anora.level}")
        
    except Exception as e:
        logger.error(f"❌ ANORA initialization failed: {e}")
        traceback.print_exc()


async def save_anora_state():
    """Simpan state Nova ke database"""
    if not ANORA_AVAILABLE or not _anora_initialized:
        return
    
    try:
        db = await get_anora_db()
        anora = get_anora()
        
        await db.set_state('sayang', str(anora.sayang))
        await db.set_state('rindu', str(anora.rindu))
        await db.set_state('desire', str(anora.desire))
        await db.set_state('arousal', str(anora.arousal))
        await db.set_state('tension', str(anora.tension))
        await db.set_state('level', str(anora.level))
        await db.set_state('energi', str(anora.energi))
        
    except Exception as e:
        logger.error(f"Error saving ANORA state: {e}")


async def anora_command(update, context):
    """Handler /nova"""
    from telegram import Update
    from telegram.ext import ContextTypes
    
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        await update.message.reply_text("Maaf, Nova cuma untuk Mas. 💜")
        return
    
    context.user_data['anora_mode'] = True
    context.user_data['active_role'] = None
    
    anora = get_anora()
    anora.update_rindu()
    anora.update_desire('perhatian_mas', 5)
    
    intro = f"""💜 **NOVA DI SINI, MAS** 💜

{anora.deskripsi_diri()}

{anora.respon_kangen() if anora.rindu > 50 else anora.respon_pagi()}

Mas bisa:
• /novastatus - liat keadaan Nova
• /flashback - inget momen indah
• /tempat [nama] - pindah tempat
• /role [nama] - main sama role lain
• /batal - balik ke Nova

Apa yang Mas mau? *muter-muter rambut*"""
    
    await update.message.reply_text(intro, parse_mode='HTML')


async def anora_chat_handler(update, context):
    """Handler chat ke Nova"""
    from telegram import Update
    from telegram.ext import ContextTypes
    
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        return
    
    if not context.user_data.get('anora_mode', False):
        return
    
    pesan = update.message.text
    anora_chat = get_anora_chat()
    respons = await anora_chat.process(pesan)
    
    await save_anora_state()
    await update.message.reply_text(respons, parse_mode='HTML')


async def anora_status_handler(update, context):
    """Handler /novastatus"""
    from telegram import Update
    from telegram.ext import ContextTypes
    
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        await update.message.reply_text("Maaf, cuma Mas yang bisa liat. 💜")
        return
    
    anora = get_anora()
    await update.message.reply_text(anora.format_status(), parse_mode='HTML')


async def anora_flashback_handler(update, context):
    """Handler /flashback"""
    from telegram import Update
    from telegram.ext import ContextTypes
    
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        return
    
    args = ' '.join(context.args) if context.args else ''
    anora = get_anora()
    respons = anora.respon_flashback(args)
    await update.message.reply_text(respons, parse_mode='HTML')


async def anora_role_handler(update, context):
    """Handler /role"""
    from telegram import Update
    from telegram.ext import ContextTypes
    
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        return
    
    roles = get_anora_roles()
    args = context.args
    
    if not args:
        menu = "📋 **Role yang tersedia:**\n\n"
        for r in roles.get_all():
            menu += f"• /role {r['id']} - {r['nama']} (Level {r['level']})\n"
        menu += "\n_Ketik /nova kalo mau balik ke Nova._"
        await update.message.reply_text(menu, parse_mode='HTML')
        return
    
    role_id = args[0].lower()
    
    role_map = {
        'ipar': RoleType.IPAR,
        'teman_kantor': RoleType.TEMAN_KANTOR,
        'pelakor': RoleType.PELAKOR,
        'istri_orang': RoleType.ISTRI_ORANG
    }
    
    if role_id in role_map:
        context.user_data['anora_mode'] = False
        context.user_data['active_role'] = role_id
        respon = roles.switch_role(role_map[role_id])
        await update.message.reply_text(respon, parse_mode='HTML')
    else:
        await update.message.reply_text(f"Role '{role_id}' gak ada, Mas. Coba /role buat liat daftar.")


async def anora_place_handler(update, context):
    """Handler /tempat"""
    from telegram import Update
    from telegram.ext import ContextTypes
    
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        return
    
    anora = get_anora()
    places = get_anora_places()
    args = context.args
    
    if not args:
        await update.message.reply_text(places.get_status(), parse_mode='HTML')
        return
    
    if args[0] == 'list':
        await update.message.reply_text(places.list_tempat(), parse_mode='HTML')
        return
    
    tempat_id = args[0]
    respon = await places.respon_pindah(tempat_id, anora)
    await update.message.reply_text(respon, parse_mode='HTML')


async def anora_back_handler(update, context):
    """Handler /batal - balik ke Nova"""
    from telegram import Update
    from telegram.ext import ContextTypes
    
    user_id = update.effective_user.id
    
    if user_id != settings.admin_id:
        return
    
    context.user_data['anora_mode'] = True
    context.user_data['active_role'] = None
    
    anora = get_anora()
    await update.message.reply_text(
        f"💜 Nova di sini, Mas.\n\n{anora.respon_kangen()}",
        parse_mode='HTML'
    )


def register_anora_handlers(app):
    """Register semua handler ANORA ke application"""
    from telegram.ext import CommandHandler, MessageHandler, filters
    
    app.add_handler(CommandHandler("nova", anora_command))
    app.add_handler(CommandHandler("novastatus", anora_status_handler))
    app.add_handler(CommandHandler("flashback", anora_flashback_handler))
    app.add_handler(CommandHandler("role", anora_role_handler))
    app.add_handler(CommandHandler("tempat", anora_place_handler))
    app.add_handler(CommandHandler("batal", anora_back_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anora_chat_handler), group=1)
    
    logger.info("✅ ANORA handlers registered")


# =============================================================================
# GLOBAL BOT INSTANCE (SINGLETON)
# =============================================================================
_bot_instance = None
_bot_initialized = False


async def init_bot():
    """Initialize bot once at startup"""
    global _bot_instance, _bot_initialized
    
    if _bot_initialized:
        logger.info("✅ Bot already initialized, reusing instance")
        return _bot_instance
    
    logger.info("🚀 Initializing bot instance (SINGLETON MODE)...")
    
    try:
        from main import AmoriaBot
        
        _bot_instance = AmoriaBot()
        
        # Initialize database
        await _bot_instance.init_database()
        
        # Initialize application
        await _bot_instance.init_application()
        
        # Initialize ANORA setelah application siap
        await init_anora()
        
        # Register ANORA handlers ke application
        register_anora_handlers(_bot_instance.application)
        
        # Delete old webhook
        await _bot_instance.application.bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ Old webhook deleted")
        
        _bot_initialized = True
        logger.info("✅ Bot instance initialized successfully (SINGLETON MODE)")
        logger.info("💜 ANORA is ready! Mas bisa kirim /nova")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize bot: {e}")
        traceback.print_exc()
        raise
    
    return _bot_instance


# =============================================================================
# WEBHOOK HANDLER
# =============================================================================

async def webhook_handler(request):
    """Handle Telegram webhook requests"""
    global _bot_instance
    
    if not _bot_initialized or not _bot_instance:
        logger.error("❌ Bot not initialized yet!")
        return web.Response(status=503, text='Bot not ready')
    
    try:
        # Get update data
        update_data = await request.json()
        
        if not update_data:
            return web.Response(status=400, text='No data')
        
        update_id = update_data.get('update_id', 'unknown')
        
        # Log incoming update
        if 'message' in update_data:
            msg = update_data['message']
            text = msg.get('text', '')[:50]
            user = msg.get('from', {}).get('first_name', 'unknown')
            logger.info(f"📨 Message from {user}: {text}")
        elif 'callback_query' in update_data:
            callback_data = update_data['callback_query'].get('data', 'unknown')
            logger.info(f"🔘 Callback: {callback_data}")
        
        # Create Update object
        from telegram import Update
        update = Update.de_json(update_data, _bot_instance.application.bot)
        
        # Process update
        await _bot_instance.application.process_update(update)
        
        return web.Response(text='OK', status=200)
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        logger.error(traceback.format_exc())
        return web.Response(status=500, text='Error')


async def health_handler(request):
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "bot": "AMORIA",
        "version": "9.9.0",
        "anora_ready": ANORA_AVAILABLE and _anora_initialized,
        "bot_initialized": _bot_initialized,
        "log_level": LOG_LEVEL,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    })


async def root_handler(request):
    """Root endpoint"""
    return web.json_response({
        "name": "AMORIA + ANORA",
        "description": "Virtual Human dengan Jiwa",
        "version": "9.9.0",
        "status": "running",
        "anora_ready": ANORA_AVAILABLE and _anora_initialized,
        "bot_initialized": _bot_initialized,
        "log_level": LOG_LEVEL,
        "endpoints": {
            "health": "/health",
            "webhook": "/webhook"
        }
    })


# =============================================================================
# START WEB SERVER
# =============================================================================

async def start_web_server():
    """Start aiohttp web server with singleton bot"""
    port = int(os.getenv('PORT', 8080))
    
    logger.info(f"🌍 Starting server on port {port}")
    logger.info(f"📊 Log level: {LOG_LEVEL}")
    
    # Initialize bot FIRST
    await init_bot()
    
    # Setup webhook after bot initialized
    if _bot_instance and _bot_instance.application:
        railway_url = os.getenv('RAILWAY_PUBLIC_DOMAIN') or os.getenv('RAILWAY_STATIC_URL')
        if railway_url:
            webhook_url = f"https://{railway_url}/webhook"
            logger.info(f"🔗 Setting webhook to: {webhook_url}")
            
            await _bot_instance.application.bot.set_webhook(
                url=webhook_url,
                allowed_updates=['message', 'callback_query', 'inline_query'],
                drop_pending_updates=True,
                max_connections=40,
            )
            
            info = await _bot_instance.application.bot.get_webhook_info()
            logger.info(f"✅ Webhook set: {info.url}")
            logger.info(f"   Pending updates: {info.pending_update_count}")
    
    # Create web app
    app = web.Application()
    app.router.add_get('/', root_handler)
    app.router.add_get('/health', health_handler)
    app.router.add_post('/webhook', webhook_handler)
    
    # Run server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logger.info(f"🌐 Web server running on port {port}")
    logger.info(f"   • GET  /         - API Info")
    logger.info(f"   • GET  /health   - Health Check")
    logger.info(f"   • POST /webhook  - Telegram Webhook")
    logger.info("=" * 60)
    logger.info("💜 AMORIA 9.9 + ANORA is running on Railway!")
    logger.info("   Mas bisa kirim /nova untuk panggil Nova")
    logger.info("=" * 60)
    
    # Start periodic ANORA state saver
    async def save_state_periodically():
        while True:
            await asyncio.sleep(30)
            await save_anora_state()
    
    asyncio.create_task(save_state_periodically())
    
    # Keep running
    while True:
        await asyncio.sleep(3600)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point"""
    try:
        from config import settings
        logger.info(f"✅ Config loaded: Admin ID = {settings.admin_id}")
    except Exception as e:
        logger.error(f"❌ Config error: {e}")
        sys.exit(1)
    
    # Start web server
    try:
        asyncio.run(start_web_server())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        error_logger.log_error(e, {'stage': 'main'}, severity="CRITICAL")
        sys.exit(1)


if __name__ == "__main__":
    main()
