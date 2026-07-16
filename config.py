import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pytgcalls import PyTgCalls

# For Local Deploy
if os.path.exists(".env"):
    load_dotenv(".env")

# Necessary Vars
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
HNDLR = os.getenv("HNDLR", ".") # تم تغييره إلى نقطة لسهولة التحكم كمساعد

# إعداد العميل الرئيسي (الحساب الشخصي) والمكالمات
bot = Client(SESSION, API_ID, API_HASH)
call_app = PyTgCalls(bot)

# رابط البث المباشر لإذاعة القرآن الكريم من القاهرة
QURAN_STREAM_URL = "https://zeno.fm"
