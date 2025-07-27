from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Вопрос-ответ словарь
qa_data = {
    "Doktoranturaga hujjat topshirish uchun qanday talablar bor?":
        "Siz dastlab one id tizimi orqali DARAJA.ILMIY.UZ platformasiga kirib ro‘yxatdan o‘tishingiz va so’ralgan hujjatlarni yuklashingiz kerak.",
    "Doktoranturaga topshirish uchun qanday hujjatlar kerak?":
        "- Ariza\n- Magistrlik diplomi\n- Ilmiy maqolalar\n- Ilmiy izlanish konsepsiyasi\n- Tarjimai hol\n- Tavsifnoma\n"
        "- Mehnat faoliyati hujjati (agar mavjud bo‘lsa)\n- Ilmiy rahbar rozilik xati\n- Pasport nusxasi\n"
        "- Xorijiy til sertifikati (PDF, 5MB gacha)",
    "PhD yo‘nalishiga qabul qilinish uchun ariza shakli qanday yoziladi?":
        "Hujjatlar namunasini quydagi havola orqali yuklab oling. https://uzjoku.uz/uz/aktivnost-anown8qshe/ilmiy-faoliyat-up/scientificactivity/avqd9xj375gknz2owqsnsna05vnbytlanuyizchnpijqy9o5hk",
    "Doktoranturaga hujjat qabul qilish muddati qachon boshlanadi?":
        "15-sentabrdan 15-oktabrgacha. Aniq muddat universitet saytida e'lon qilinadi: https://uzjoku.uz/uz",
    "Qabul imtihonlari qanday shaklda o'tadi?":
        "Yozma imtihon va suhbat. 4 ta yozma savol, 1 ta og‘zaki. Xorijlik doktorantlar uchun faqat suhbat.",
    "Tayanch doktoranturada (PhD) o'qish qancha vaqt davom etadi?":
        "3 yil. Shu muddat ichida himoyaga chiqishi shart.",
    "Doktoranturada (DSc) o'qish qancha vaqt davom etadi?":
        "3 yil. Shu muddat ichida himoyaga chiqishi shart.",
    "Doktorantlarga stipendiya to'lanadimi?":
        "Ha, to‘lanadi. Xorijliklarga — yo‘q.",
    "PhD ga topshirish uchun til sertifikati talab etiladimi?":
        "Ha. CEFR B2 yoki IELTS 5.5. Boshqa tillar: B2 yoki C1.",
    "Ilmiy maqolalarni qaerda chop etish kerak?":
        "OAK ro‘yxatidagi jurnallarda yoki xalqaro/repsublika konferensiyalarida.",
    "Doktoranturadan keyingi imkoniyatlar nimalar?":
        "- PhD yoki DSc darajasi\n- Maosh yuqori\n- Dotsent/professor unvoni\n- Ilmiy rahbar bo‘lish",
    "PhD uchun nechta maqola kerak?":
        "Kamida 1 ta maqola va 2 ta tezis. Har biri uchun havola va nusxa bo‘lishi kerak.",
    "Ilmiy rahbarni qanday tanlash mumkin?":
        "O‘zJOKUdagi kafedrada ishlovchi professor yoki dotsentdan tanlab olinadi va tasdiqlanadi.",
    "Ilmiy konsepsiyani qanday tayyorlash kerak?":
        "Mavzu, maqsad, vazifa, yangilik, amaliy ahamiyat, metodlar keltiriladi.",
    "Tavsifnoma qanday olinadi?":
        "Ish joyidan yoki ilmiy rahbardan. Unda sizning ilmiy salohiyatingiz ko‘rsatiladi.",
    "Eng muhim va asosiy masalalar bo‘yicha materiallar bilan tanishish/Ознакомиться с материалами по наиболее важным и первичным вопросам0":
        "Eng muhim va asosiy masalalar bo‘yicha materiallar bilan quyidagi havola orqali tanishishingiz mumkin https://uzjoku.uz/uz/aktivnost-anown8qshe/ilmiy-faoliyat-up/scientificactivity \n"
        "Ознакомиться с материалами по наиболее важным и первичным вопросам можно по следующей ссылке https://uzjoku.uz/uz/aktivnost-anown8qshe/ilmiy-faoliyat-up/scientificactivity",
}

# Генерируем список вопросов и ID
questions = list(qa_data.keys())
id_to_question = {f"q{idx+1}": question for idx, question in enumerate(questions)}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton(text=question, callback_data=f"q{idx+1}")]
        for idx, question in enumerate(questions)
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    if update.message:
        await update.message.reply_text("❓ Savoldan birini tanlang:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("❓ Savoldan birini tanlang:", reply_markup=reply_markup)

# Обработка выбора вопроса
async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    btn_id = query.data

    if btn_id == "back":
        await start(update, context)
        return

    question = id_to_question.get(btn_id)
    answer = qa_data.get(question, "Javob topilmadi.")
    back_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back")]
    ])

    await query.edit_message_text(
        f"❓ *{question}*\n\n📘 {answer}",
        parse_mode="Markdown",
        reply_markup=back_markup
    )

# Запуск приложения
def main():
    app = Application.builder().token("7808860481:AAHDoydehllfSz6o_PeDo5CKb5eFo0Ua-3M").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_question))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
