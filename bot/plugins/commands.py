from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot import Translation, LOGGER # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error
import random

db = Database()

force_channel = "wudixh13"

PICS = [
"https://telegra.ph/file/7a264da82c92e56430feb.jpg",
"https://telegra.ph/file/23f226130bfdc3ef0baad.jpg",
"https://telegra.ph/file/4b91500e1254a6e1b203e.jpg"
]

@Client.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, update):
    
    if force_channel:
        try:
            user = await bot.get_chat_member(force_channel, update.from_user.id)
            if user.status == "kicked out":
                await update.reply_text("You Are Banned")
                return
        except UserNotParticipant :
            await update.reply_text(
                text="🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🤭.\n\nനിങ്ങൾക്ക് മൂവീസ് വേണോ? എങ്കിൽ തായെ കാണുന്ന ഞങ്ങളുടെ മെയിൻ ചാനലിൽ ജോയിൻ ചെയ്യുക.😂\nഎന്നിട്ട് ഗ്രൂപ്പിൽ പോയി വീണ്ടും മൂവിയിൽ ക്ലിക് ചെയ്ത് start കൊടുത്തു നോക്കൂ..!😁",
                reply_markup=InlineKeyboardMarkup( [[
                 InlineKeyboardButton("🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🤭", url=f"t.me/{force_channel}")
                 ]]
                 )
            )
            return
    
    try:
        file_uid = update.command[1]
    except IndexError:
        file_uid = False
    
    if file_uid:
        file_id, file_name, file_caption, file_type, file_size = await db.get_file(file_uid)
        
        if (file_id or file_type) == None:
            return
  #FILE SIZE COMPRESSING>>>>>      
        if file_size < 1024:
            file_size = f"[{file_size} B]"
        elif file_size < (1024**2):
            file_size = f"[{str(round(file_size/1024, 2))} KB]"
        elif file_size < (1024**3):
            file_size = f"[{str(round(file_size/(1024**2), 2))} MB]"
        elif file_size < (1024**4):
            file_size = f"[{str(round(file_size/(1024**3), 2))} GB]"
#CUSTOM FILE CAPTION       
        caption = f""" 📂 <em>File Name</em>: <code>Kᴜᴛᴛᴜ Bot | {file_name} </code> \n\n🖇 <em>File Size</em>: <code> {file_size} </code>"""
        
        try:
            await update.reply_cached_media(
                file_id,
                quote=True,
                caption = caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton('💕Movie Group❤️', url="https://t.me/wudixh")
                        ]]
                ))
        except Exception as e:
            await update.reply_text(f"<b>Error:</b>\n<code>{e}</code>", True, parse_mode=enums.ParseMode.HTML)
            LOGGER(name).error(e)
        return
#pmstart
    buttons = [[
                    InlineKeyboardButton('Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ💕', url=f"http://t.me/im_kuttu2_bot?startgroup=true")
                ],[
                    InlineKeyboardButton('Mᴏᴠɪᴇ ɢʀᴏᴜᴘ🎥', url='https://t.me/wudixh')
                ],[
                    InlineKeyboardButton('Hᴇʟᴘ🔧', callback_data="help")
           ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.reply_photo(
        photo=random.choice(PICS),
        caption=Translation.HELP_TEXT.format(update.from_user.first_name),
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )


@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, update):
    buttons = [[
            InlineKeyboardButton('🏡ʜᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('Aʙᴏᴜᴛ🖥', callback_data='about')
        ],[
            InlineKeyboardButton('🔐ᴄʟᴏsᴇ', callback_data='close')
        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.reply_photo(
        photo=random.choice(PICS),
        caption=Translation.HELP_TEXT,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )


@Client.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(bot, update):
    
    buttons = [[
            InlineKeyboardButton('Oᴡɴᴇʀ👤', url='https://t.me/wudixh13/4')
        ], [
            InlineKeyboardButton('🏡ʜᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('ʙᴀᴄᴋ👈', callback_data='help')
        ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.reply_photo(
        photo=random.choice(PICS),
        caption=Translation.ABOUT_TEXT,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )
