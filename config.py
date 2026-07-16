import os
from dotenv import load_dotenv
from pyrogram import Client

# تحميل متغيرات البيئة من ملف .env المحلي بالسيرفر
if os.path.exists(".env"):
    load_dotenv(".env")

# المتغيرات الأساسية للتشغيل
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
HNDLR = os.getenv("HNDLR", ".")  # رمز التحكم في الحساب (النقطة .)

# رابط بث راديو إذاعة القرآن الكريم الافتراضي (إذا لم يتم وضع رابط يوتيوب)
QURAN_STREAM_URL = "https://zeno.fm"

# بناء عميل تيليجرام ومكتبة البث المباشر للمكالمات
bot = Client(SESSION, API_ID, API_HASH)
