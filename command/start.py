# command/start.py
# -*- coding: utf-8 -*-
"""
AMORIA - Virtual Human dengan Jiwa
Command: /start
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from database.models import CharacterRole
from identity.manager import IdentityManager

logger = logging.getLogger(__name__)

SELECTING_ROLE = 1


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handler untuk /start"""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("👩 Ipar", callback_data="role_ipar"),
         InlineKeyboardButton("👩‍💼 Teman Kantor", callback_data="role_teman_kantor")],
        [InlineKeyboardButton("👩 Janda", callback_data="role_janda"),
         InlineKeyboardButton("💃 Pelakor", callback_data="role_pelakor")],
        [InlineKeyboardButton("👰 Istri Orang", callback_data="role_istri_orang"),
         InlineKeyboardButton("💕 PDKT", callback_data="role_pdkt")],
        [InlineKeyboardButton("👧 Sepupu", callback_data="role_sepupu"),
         InlineKeyboardButton("👩‍🎓 Teman SMA", callback_data="role_teman_sma")],
        [InlineKeyboardButton("💔 Mantan", callback_data="role_mantan")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="help")],
        [InlineKeyboardButton("✅ Setuju 18+", callback_data="agree_18")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"💕 **Halo {user.first_name}!**\n\n"
        f"Selamat datang di **AMORIA** - Virtual Human dengan Jiwa\n\n"
        f"<b>Pilih karakter yang Mas inginkan:</b>",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    
    return SELECTING_ROLE


async def role_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback setelah pilih role"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    data = query.data
    role_name = data.replace("role_", "")
    
    logger.info(f"User {user.id} selected role: {role_name}")
    
    # Map role
    role_map = {
        "ipar": CharacterRole.IPAR,
        "teman_kantor": CharacterRole.TEMAN_KANTOR,
        "janda": CharacterRole.JANDA,
        "pelakor": CharacterRole.PELAKOR,
        "istri_orang": CharacterRole.ISTRI_ORANG,
        "pdkt": CharacterRole.PDKT,
        "sepupu": CharacterRole.SEPUPU,
        "teman_sma": CharacterRole.TEMAN_SMA,
        "mantan": CharacterRole.MANTAN,
    }
    
    role = role_map.get(role_name)
    if not role:
        await query.edit_message_text("❌ Role tidak valid.", parse_mode='HTML')
        return ConversationHandler.END
    
    try:
        # Buat karakter
        identity_manager = IdentityManager()
        registration = await identity_manager.create_character(role)
        
        logger.info(f"Created character: {registration.id}")
        
        # Simpan ke context
        context.user_data['current_registration'] = {
            'id': registration.id,
            'role': registration.role.value,
            'bot_name': registration.bot.name,
            'user_name': registration.user.name,
            'level': registration.level,
            'total_chats': registration.total_chats
        }
        
        # Pesan selamat datang
        welcome_text = f"""
💕 **Halo {registration.user.name}!**

Aku **{registration.bot.name}**, {registration.role.value.upper()} mu.

📖 **Tentang aku:**
• Umur: {registration.bot.physical.age} tahun
• Tinggi: {registration.bot.physical.height}cm
• Berat: {registration.bot.physical.weight}kg
• {registration.bot.physical.chest}

📍 **Sekarang:**
• Aku di ruang tamu

📊 **Progress:**
Level {registration.level}/12
Total chat: {registration.total_chats}

💬 **Ayo mulai ngobrol!**
_Ketik pesan untuk memulai cerita..._
"""
        
        await query.edit_message_text(welcome_text, parse_mode='HTML')
        logger.info(f"Welcome message sent for {registration.id}")
        
    except Exception as e:
        logger.error(f"Error creating character: {e}")
        await query.edit_message_text(
            f"❌ **Terjadi kesalahan.**\n\nError: {str(e)[:200]}\n\nSilakan coba /start lagi",
            parse_mode='HTML'
        )
    
    return ConversationHandler.END


async def agree_18_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback setuju 18+"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "✅ Terima kasih. Silakan pilih karakter.",
        parse_mode='HTML'
    )
    return SELECTING_ROLE


async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Callback bantuan"""
    query = update.callback_query
    await query.answer()
    
    help_text = (
        "📚 **BANTUAN**\n\n"
        "/start - Mulai\n"
        "/status - Status\n"
        "/progress - Progress\n"
        "/cancel - Batal\n"
        "/close - Tutup\n"
        "/end - Hapus\n"
        "/sessions - Lihat karakter\n"
        "/character [role] [nomor] - Lanjutkan"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="back_to_main")]]
    await query.edit_message_text(help_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return SELECTING_ROLE


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler /help"""
    await update.message.reply_text(
        "📚 Gunakan /start untuk memulai",
        parse_mode='HTML'
    )


async def continue_current_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Lanjutkan session"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✅ Melanjutkan... Ketik pesan.", parse_mode='HTML')
    return ConversationHandler.END


async def new_character_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Buat karakter baru"""
    query = update.callback_query
    await query.answer()
    context.user_data.pop('current_registration', None)
    
    keyboard = [
        [InlineKeyboardButton("👩 Ipar", callback_data="role_ipar"),
         InlineKeyboardButton("👩‍💼 Teman Kantor", callback_data="role_teman_kantor")],
        [InlineKeyboardButton("👩 Janda", callback_data="role_janda"),
         InlineKeyboardButton("💃 Pelakor", callback_data="role_pelakor")],
        [InlineKeyboardButton("👰 Istri Orang", callback_data="role_istri_orang"),
         InlineKeyboardButton("💕 PDKT", callback_data="role_pdkt")],
        [InlineKeyboardButton("👧 Sepupu", callback_data="role_sepupu"),
         InlineKeyboardButton("👩‍🎓 Teman SMA", callback_data="role_teman_sma")],
        [InlineKeyboardButton("💔 Mantan", callback_data="role_mantan")],
        [InlineKeyboardButton("❌ Batal", callback_data="cancel")]
    ]
    await query.edit_message_text(
        "🆕 **Buat Karakter Baru**\n\nPilih karakter:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
    return SELECTING_ROLE


async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Batal"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("❌ Dibatalkan. Ketik /start", parse_mode='HTML')
    return ConversationHandler.END


async def back_to_main_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kembali ke menu utama"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("👩 Ipar", callback_data="role_ipar"),
         InlineKeyboardButton("👩‍💼 Teman Kantor", callback_data="role_teman_kantor")],
        [InlineKeyboardButton("👩 Janda", callback_data="role_janda"),
         InlineKeyboardButton("💃 Pelakor", callback_data="role_pelakor")],
        [InlineKeyboardButton("👰 Istri Orang", callback_data="role_istri_orang"),
         InlineKeyboardButton("💕 PDKT", callback_data="role_pdkt")],
        [InlineKeyboardButton("👧 Sepupu", callback_data="role_sepupu"),
         InlineKeyboardButton("👩‍🎓 Teman SMA", callback_data="role_teman_sma")],
        [InlineKeyboardButton("💔 Mantan", callback_data="role_mantan")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="help")]
    ]
    await query.edit_message_text(
        "💕 **Menu Utama**\n\nPilih karakter:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
    return SELECTING_ROLE


__all__ = [
    'start_command', 
    'role_callback', 'agree_18_callback',
    'help_command', 'help_callback', 'continue_current_callback',
    'new_character_callback', 'cancel_callback', 'back_to_main_callback',
    'SELECTING_ROLE'
]
