import asyncio
import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

# البيانات الخاصة بك مدمجة وجاهزة بالكامل
API_ID = 26862344
API_HASH = "5650e0b8d2f91adb54e1a6647431e182"
BOT_TOKEN = "5968886182:AAHi2VNoXJOuKiAC3jk_cqdQxEr3Ivu3oKs"

# رابط البث المباشر لإذاعة القرآن الكريم من القاهرة
QURAN_STREAM_URL = "https://zeno.fm"

# تشغيل عميل تيليجرام (Pyrogram)
bot = Client("QuranStreamBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_app = PyTgCalls(bot)

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await message.reply_text(
        "👋 أهلاً بك في بوت بث القرآن الكريم المطور.\n\n"
        "💡 **الأوامر المتاحة في المجموعات:**\n"
        "• `/play` : لبدء بث إذاعة القرآن الكريم في المكالمة الصوتية.\n"
        "• `/stop` : لإيقاف البث ومغادرة المكالمة."
    )

@bot.on_message(filters.command("play") & filters.group)
async def play_quran(client, message):
    chat_id = message.chat.id
    msg = await message.reply_text("🔄 جاري الاتصال بالمحادثة الصوتية وبدء بث القرآن الكريم...")
    
    try:
        # تشغيل البث المباشر داخل المكالمة الصوتية للمجموعة
        await call_app.join_group_call(
            chat_id,
            AudioPiped(QURAN_STREAM_URL)
        )
        await msg.edit_text("✅ تم بدء بث إذاعة القرآن الكريم بنجاح في المحادثة الصوتية.")
    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ أثناء محاولة التشغيل.\nتأكد من فتح المحادثة الصوتية أولاً وتعيين البوت كمشرف.\nالخطأ: {e}")

@bot.on_message(filters.command("stop") & filters.group)
async def stop_quran(client, message):
    chat_id = message.chat.id
    try:
        await call_app.leave_group_call(chat_id)
        await message.reply_text("🛑 تم إيقاف البث ومغادرة المحادثة الصوتية بنجاح.")
    except Exception as e:
        await message.reply_text(f"❌ البوت ليس في مكالمة صوتية حالياً أو حدث خطأ: {e}")

async def main():
    # تشغيل البوت ومكتبة المكالمات معاً
    await bot.start()
    await call_app.start()
    print("⚡ البوت يعمل الآن بنجاح وبانتظار أمر /play في المجموعات!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
