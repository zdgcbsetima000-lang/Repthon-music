import asyncio
from pyrogram import filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL
from config import bot, API_ID, API_HASH, SESSION, QURAN_STREAM_URL, HNDLR

# ربط تطبيق المكالمات بالعميل الرئيسي
call_app = PyTgCalls(bot)

def get_youtube_stream(url):
    """ دالة سحب رابط الصوت الخام من بث يوتيوب المباشر """
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'live_from_start': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']

@bot.on_message(filters.command("play", prefixes=HNDLR) & filters.me)
async def play_audio(client, message):
    chat_id = message.chat.id
    
    # إذا قام المستخدم بكتابة الأمر وبجانبه رابط (مثال: .play رابط-يوتيوب)
    if len(message.command) > 1:
        youtube_url = message.text.split(None, 1)[1]
        msg = await message.reply_text("🔄 جاري فك تشفير بث يوتيوب والاتصال بالمحادثة الصوتية...")
        try:
            loop = asyncio.get_event_loop()
            stream_url = await loop.run_in_executor(None, get_youtube_stream, youtube_url)
        except Exception as e:
            return await msg.edit_text(f"❌ فشل استخراج الصوت من يوتيوب.\nالخطأ: {e}")
    else:
        # إذا كتب الأمر .play فقط بدون روابط، يتم تشغيل راديو القرآن الكريم من القاهرة تلقائياً
        stream_url = QURAN_STREAM_URL
        msg = await message.reply_text("🔄 جاري الاتصال بالمحادثة وبدء بث إذاعة القرآن الكريم...")

    try:
        # تشغيل البث المباشر في المكالمة الصوتية للمجموعة
        await call_app.join_group_call(chat_id, AudioPiped(stream_url))
        await msg.edit_text("✅ تم بدء البث الصوتي بنجاح داخل المحادثة الصوتية.")
    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ أثناء التشغيل.\nتأكد من فتح المحادثة الصوتية أولاً لحسابك.\nالخطأ: {e}")

@bot.on_message(filters.command("stop", prefixes=HNDLR) & filters.me)
async def stop_audio(client, message):
    chat_id = message.chat.id
    try:
        await call_app.leave_group_call(chat_id)
        await message.reply_text("🛑 تم إيقاف البث ومغادرة المحادثة الصوتية بنجاح.")
    except Exception as e:
        await message.reply_text(f"❌ الحساب ليس في مكالمة صوتية حالياً: {e}")

async def main():
    await bot.start()
    await call_app.start()
    print("⚡ السورس المحدث يعمل الآن بنجاح 100%!")
    print(f"💡 التحكم من حسابك الشخصي باستخدام الأمر: {HNDLR}play")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
