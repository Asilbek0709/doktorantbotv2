from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Вопросы и ответы по направлениям
qa_data = {
    "doktorantura": {
        "Doktoranturaga hujjat topshirishning dastlabki bosqichi haqida ma’lumot bering.":
            "Siz dastlab ONE ID tizimi orqali DARAJA.ILMIY.UZ platformasiga kirib ro‘yxatdan o‘tishingiz va so’ralgan hujjatlarni yuklashingiz kerak.",
        "Doktoranturaga topshirish uchun qanday hujjatlar kerak?":
            "- Ariza\n- Magistrlik diplomi\n- Ilmiy maqolalar\n- Ilmiy izlanish konsepsiyasi\n- Tarjimai hol\n- Tavsifnoma\n"
            "- Mehnat faoliyati hujjati (agar mavjud bo‘lsa)\n- Ilmiy rahbar rozilik xati\n- Pasport nusxasi\n"
            "- Xorijiy til sertifikati (PDF, 5MB gacha)",
        "PhD yo‘nalishiga qabul qilinish uchun ariza shakli qanday yoziladi?":
            "Ariza namunasini ushbu havoladan yuklab oling https://uzjoku.uz/uz/aktivnost-anown8qshe/ilmiy-faoliyat-up/scientificactivity",
        "Doktoranturaga hujjat qabul qilish muddati qachon boshlanadi?":
            "Hujjatlar 15-sentyabrdan – 15-oktyabrgacha qabul qilinadi. Aniq muddat universitet saytida e'lon qilinadi. (https://t.me/uzjmcu, https://uzjoku.uz/uz)",
        "Qabul imtihonlari qanday shaklda o'tadi?":
            "10.00.09 Jurnalistika, 23.00.02 – Siyosiy institutlar, jarayonlar va texnologiyalar Ixtisosligi fanidan yozma imtihon va suhbat shaklida tashkil etiladi. 4 SAVOL, yozma, tadqiqotchining ilmiy ishi bo`yicha 1 ta SAVOL og‘zaki shaklda bo‘ladi \n – Xorijlik doktorantlar faqat suhbat asosida qabul qilinadi.",
        "Tayanch doktoranturada (PhD) o'qish qancha vaqt davom etadi?":
            "Tayanch doktoranturada tahsil olish muddati 3 yil. (Shu muddat ichida tadqiqotchi kafedra muhokamasidan va ilmiy seminardan o‘tib, himoyaga chiqishi shart)",
        "Doktoranturada (DSc) o'qish qancha vaqt davom etadi?" :
            "Doktoranturada tahsil olish muddati 3 yil. (Shu muddat ichida tadqiqotchi kafedra muhokamasidan va ilmiy seminardan o‘tib, himoyaga chiqishi shart)",
        "Doktorantlarga stipendiya to'lanadimi?":
            "Ha, doktorantlarga har oy belgilangan miqdorda stipendiya to'lanadi. (xorijiy doktorantlarga to'lanmaydi)",
        "Tayanch doktoranturada (PhD)ga topshirish uchun til sertifikati talab etiladimi?":
            "Ha, CEFR bo'yicha kamida B2, IELTS 5.5 talab etiladi. (Turk, Arab, Yapon, Koreys kabi tillarda B2 yoki C1)",
        "Ilmiy maqolalarni qayerda chop etish kerak?":
            "OAK ro'yxatidagi jurnallarda, xalqaro va respublika konferensiyalarida, xalqaro ilmiy bazalarida maqolalar chop etilishi kerak",
        "Doktoranturadan keyingi imkoniyatlar nimalar? ":
            "– Doktoranturani yakunlaganlar PhD, DSc ilmiy darajasiga ega bo'ladi, \n – oliy ta'lim tizimida maoshi nisbatan yuqori bo'ladi, \n – dotsent, professor unvonlarini olishi, ilmiy rahbar va ilmiy maslahatchi lavozimlarda faoliyat yuritishlari mumkin.",
        "Tayanch doktoranturaga topshirish uchun uchun maqola soni nechta bolishi kerak?":
            "Kamida 1 ta ilmiy maqola va 2 ta tezis taqdim etilishi talab etiladi. Har biri uchun havola va nusxa bo'lishi zarur.",
        "Ilmiy rahbarni qanday tanlash mumkin?":
            "Ilmiy yo'nalishingiz bo'yicha O‘zJOKUda mavjud kafedrada faoliyat yuritayotgan dotsent yoki professor unvoniga ega bo‘lgan professor o’qituvchi ilmiy rahbar sifatida tanlanib, rasman tasdiqlanadi.",
        "Ilmiy konsepsiyani qanday tayyorlash kerak?":
            "Konsepsiyada tadqiqot mavzusi, maqsadi, vazifalari, yangiligi, ilmiy va amaliy ahamiyati hamda tadqiqot metodlari ko'rsatiladi.",
        "Dissertatsiyani qaysi tilda yozish mumkun?":
            "O‘zbekiston Respublikasi qonunchiligiga muvofiq dissertatsiya o‘zbek, rus, ingliz va qoraqalpoq tillarida yozilishi mumkun.",
        "Tayanch doktorantlar ilmiy-tadqiqot ishi bo‘yicha hisobotini qay tarzda topshiradi?":
            "Tayanch doktorantlar yiliga uch marta amalga oshirgan ilmiy faoliyati bo‘yicha (O‘zbekiston Respublikasi Vazirlar Mahkamasining 304- qaroriga asosan: LEX.UZ - O'zbekiston qonunchiligi) hisobot topshiradi. DARAJA.ILMIY.UZ platformasiga so‘ralgan ma’lumotlarni yuklashi zarur. Attestatsiya komissiyasida og‘zaki suhbatdan o‘tadi.",


    },
    
    "mustaqil": {
        "Mustaqil izlanuvchilikka hujjat topshirishning dastlabki bosqichi haqida ma’lumot bering.":
            "Siz dastlab one id tizimi orqali DARAJA.ILMIY.UZ platformasiga kirib ro‘yxatdan o‘tishingiz va so’ralgan hujjatlarni yuklashingiz kerak",
        "Mustaqil izlanuvchilikka topshirish uchun qanday hujjatlar kerak?":
            "– ariza \n – magistrlik diplomi (agar mustaqil izlanuvchi DSc bo‘lsa PhD diplomi) \n – ilmiy maqolalar \n – ilmiy izlanish konsepsiyasi \n – qisqacha tarjimai hol \n – tavsifnoma \n – mehnat faoliyatini ko‘rsatuvchi hujjat tasdiqlangan nusxasi (agar mavjud bo‘lsa) \n – ilmiy rahbar rozilik xati (dissertatsiya mavzusini tasdiqlovchi hujjat). \n – pasport nusxasi (Barcha hujjatlar PDF variantda o‘rtacha 5 MB dan oshmagan bolishi kerak) \n – xorijiy til sertifikati",
        "Mustaqil izlanuvchilikka (PhD, DSc) yo‘nalishiga qabul qilinish uchun ariza shakli qanday yoziladi?":
            "Ariza namunasini ushbi havoladan yuklab oling https://uzjoku.uz/uz/aktivnost-anown8qshe/ilmiy-faoliyat-up/scientificactivity",
        "Mustaqil izlanuvchilikka hujjat qabul qilish muddati qachon boshlanadi?":
            "Mustaqil izlanuvchilik (PhD) (DSc) uchun hujjat qabul qilish har yili to’rt marta, ya’ni har bir chorakda boshlanadi va 1 oy davom etadi. Masalan: \n – 15 – yanvardan – 15 - fevralgacha \n – 15 – apreldan – 15 - maygacha \n – 15-iyuldan-15avgustgacha  \n – 15 – oktyabrdan – 15 - noyabrgacha \n \n Aniq muddat universitet saytida e'lon qilinadi. (https://t.me/uzjmcu, https://uzjoku.uz/uz)",
        "Qabul imtihonlari qanday shaklda o'tadi?":
            "10.00.09 Jurnalistika, 23.00.02 – Siyosiy institutlar, jarayonlar va texnologiyalar Ixtisosligi fanidan yozma imtihon va suhbat shaklida tashkil etiladi. 4 SAVOL, yozma, tadqiqotchining ilmiy ishi bo`yicha 1 ta SAVOL og‘zaki shaklda bo‘ladi \n – Xorijlik doktorantlar faqat suhbat asosida qabul qilinadi.",
        "Mustaqil izlanuvchilik (PhD, DSc) muddati qancha vaqt davom etadi?":
            "Mustaqil izlanuvchilik muddati 3 yil. (Shu muddat ichida tadqiqotchi kafedra muhokamasidan va ilmiy seminardan o‘tib, himoyaga chiqishi shart)",
        "Mustaqil izlanuvchilarga stipendiya to'lanadimi?":
            "Yo‘q, mustaqil izlanuvchilarga stipendiya to'lanmaydi.Chunki ular asosiy ish o‘rnidan ajralmagan holda tadqiqot olib borishadi.",
        "Mustaqil izlanuvchilikka topshirish uchun til sertifikati talab etiladimi?":
            "Yo‘q, til sertifikati talab etilmaydi",
        "Ilmiy maqolalarni qaerda chop etish kerak?":
            "OAK ro'yxatidagi jurnallarda, xalqaro va respublika konferensiyalarida, xalqaro ilmiy bazalarida maqolalar chop etilishi kerak.",
        "Mustaqil izlanuvchilikkadan keyingi imkoniyatlar nimalar?":
            "– Mustaqil izlanuvchilikni yakunlaganlar PhD, DSc ilmiy darajasiga ega bo'ladi, \n – oliy ta'lim tizimida maoshi nisbatan yuqori bo'ladi, \n – dotsent, professor unvonlarini olishi, ilmiy rahbar va ilmiy \n maslahatchi lavozimlarda faoliyat yuritishlari mumkin.",
        "Mustaqil izlanuvchilikka topshirish uchun uchun maqola soni nechta bolishi kerak?":
            "Kamida 1 ta ilmiy maqola va 2 ta tezis taqdim etilishi talab etiladi. Har biri uchun havola va nusxa bo'lishi zarur.",
        "Ilmiy rahbarni qanday tanlash mumkin?":
            "Ilmiy yo'nalishingiz bo'yicha O‘zJOKUda mavjud kafedrada faoliyat yuritayotgan dotsent yoki professor unvoniga ega bo‘lgan professor o’qituvchi ilmiy rahbar sifatida tanlanib, rasman tasdiqlanadi.",
        "Ilmiy konsepsiyani qanday tayyorlash kerak?":
            "Konsepsiyada tadqiqot mavzusi, maqsadi, vazifalari, yangiligi, ilmiy va amaliy ahamiyati hamda tadqiqot metodlari ko'rsatiladi.",
        "Mustaqil tadqiqotchilarning doktoranturadan farqi nimada?":
            "– mustaqil izlanuvchilarga stipendiya to'lanmaydi.Chunki ular asosiy ish o‘rnidan ajralmagan holda tadqiqot olib borishadi.",
        "Mustaqil izlanuvchilar ilmiy-tadqiqot ishi bo‘yicha hisobotini qay tarzda topshiradi?":
            "Mustaqil izlanuvchilar yiliga ikki marta, ya’ni har olti oyda amalga oshirgan ilmiy faoliyati bo‘yicha (O‘zbekiston Respublikasi Vazirlar Mahkamasining 304- qaroriga asosan: LEX.UZ - O'zbekiston qonunchiligi) hisobot topshiradi. DARAJA.ILMIY.UZ platformasiga so‘ralgan ma’lumotlarni yuklashi zarur. Attestatsiya komissiyasida og‘zaki suhbatdan o‘tadi.",
        "Dissertatsiyani qaysi tilda yozish mumkun?":
            "O‘zbekiston Respublikasi qonunchiligiga muvofiq dissertatsiya o‘zbek, rus, ingliz va qoraqalpoq tillarida yozilishi mumkun.",





    },
    
    "xalqaro": {
        "Chet el fuqarolari mustaqil izlanuvchilikka hujjat topshirishning dastlabki bosqichi haqida ma’lumot bering.":
            "Siz dastlab DARAJA.ILMIY.UZ platformasiga kirib xorijiy izlanuvchi sifatida ro‘yxatdan o‘tishingiz va so’ralgan hujjatlarni yuklashingiz kerak. https://uzjoku.uz/uz/aktivnost-anown8qshe/ilmiy-faoliyat-up/scientificactivity ",
        "Mustaqil izlanuvchilikka topshirish uchun qanday hujjatlar kerak?":
            "- ariza \n - magistrlik diplomi (agar mustaqil izlanuvchi DSc bosqichiga topshirmoqchi bo‘lsa PhD diplomi) \n - ilmiy maqolalar \n - qisqacha tarjimai hol \n - tavsifnoma \n - mehnat faoliyatini ko‘rsatuvchi hujjat tasdiqlangan nusxasi (agar mavjud bo‘lsa) \n - ilmiy rahbar rozilik xati (dissertatsiya mavzusini tasdiqlovchi hujjat). \n - pasport nusxasi \n (Barcha hujjatlar PDF variantda o‘rtacha 5 MB dan oshmagan bolishi kerak) \n - xorijiy til sertifikati ",
        "Mustaqil izlanuvchilikka (PhD, DSc) yo‘nalishiga qabul qilinish uchun ariza shakli qanday yoziladi?":
            "Ariza namunasini ushbu havloadan yuklab oling https://uzjoku.uz/uz/aktivnost-anown8qshe/ilmiy-faoliyat-up/scientificactivity",
        "Mustaqil izlanuvchilikka hujjat qabul qilish muddati qachon boshlanadi?":
            "Mustaqil izlanuvchilik (PhD) (DSc) uchun hujjat qabul qilish har yili to’rt marta, ya’ni har bir chorakda boshlanadi va 1 oy davom etadi. Masalan: \n – 15 – yanvardan – 15 - fevralgacha \n – 15 – apreldan – 15 - maygacha \n – 15-iyuldan-15avgustgacha \n – 15 – oktyabrdan – 15 - noyabrgacha \n \nAniq muddat universitet saytida e'lon qilinadi. (https://t.me/uzjmcu, https://uzjoku.uz/uz)",
        "Qabul imtihonlari qanday shaklda o'tadi?":
            "10.00.09 Jurnalistika ixtisosligi fanidan suhbat shaklida tashkil etiladi. 23.00.02 – Siyosiy institutlar, jarayonlar va texnologiyalar Ixtisosligi fanidan suhbat shaklida tashkil etiladi. \n Tadqiqotchining ilmiy ishi bo`yicha attestatsiya komissiyasi tomonidan berilgan SAVOLlarga JAVOBi berishi kerak. Xorijlik doktorantlar faqat suhbat asosida qabul qilinadi.",
        "Mustaqil izlanuvchilik (PhD, DSc) muddati qancha vaqt davom etadi?":
            "Mustaqil izlanuvchilik muddati 3 yil. (Shu muddat ichida tadqiqotchi kafedra muhokamasidan va ilmiy seminardan o‘tib, himoyaga chiqishi shart)",
        "Xorijlik mustaqil izlanuvchilar uchun (PhD, DSc) kontrakt miqdori qancha?":
            "To'liq ma'lumot olish uchun O'zJOKU ilmiy bo'limiga murojaat qiling: +998 97 447 17 18 Buranova Barno (telegram kontakti), +99890 979 46 56 Zamaleeva Eleonora (telegram kontakti), +99888 010 05 02 - O'rinbekov Jasur (WatsApp kontakti) international.jmcu@gmail.com (Xalqaro bo'lim) 1 yil ichida kafedra muhokamasidan va ilmiy seminardan o‘tib, himoyaga chiqsa keyingi yillar uchun to‘lov qilmaydi.",
        "Kontrakt to‘lovi qay tarzda amalga oshiriladi?":
            "Xorijlik mustaqil izlanuvchilar uchun universitetning maxsus hisob raqami mavjud. Chet el fuqarolari valyuta hisobida to'lovni amalga oshirishi uchun @adventurerau40 shu manzilga murojjat qilishi kerak.",
        "Mustaqil izlanuvchilarga stipendiya to'lanadimi? ":
            "Yo‘q, mustaqil izlanuvchilarga stipendiya to'lanmaydi.Chunki ular asosiy ish o‘rnidan ajralmagan holda tadqiqot olib borishadi.",
        "Mustaqil izlanuvchilikka topshirish uchun til sertifikati talab etiladimi?":
            "Yo‘q, til sertifikati talab etilmaydi",
        "Ilmiy maqolalarni qaerda chop etish kerak?":
            "OAK ro'yxatidagi jurnallarda, xalqaro va respublika konferensiyalarida, xalqaro ilmiy bazalarida maqolalar chop etilishi kerak.",
        "Mustaqil izlanuvchilikkadan keyingi imkoniyatlar nimalar? ":
            "– mustaqil izlanuvchilikni yakunlaganlar PhD, DSc ilmiy darajasiga ega bo'ladi, \n – oliy ta'lim tizimida maoshi nisbatan yuqori bo'ladi, \n – dotsent, professor unvonlarini olishi, ilmiy rahbar va ilmiy maslahatchi lavozimlarda faoliyat yuritishlari mumkin. ",
        "Mustaqil izlanuvchilikka topshirish uchun uchun maqola soni nechta bolishi kerak?":
            "Kamida 1 ta ilmiy maqola va 2 ta tezis taqdim etilishi talab etiladi. Har biri uchun havola va nusxa bo'lishi zarur.",
        "Mustaqil tadqiqotchilarning tayanch doktoranturadan farqi nimada?":
            "– mustaqil izlanuvchilarga stipendiya to'lanmaydi.Chunki ular asosiy ish o‘rnidan ajralmagan holda tadqiqot olib borishadi.",
        "Xorijlik mustaqil izlanuvchilar ilmiy-tadqiqot ishi bo‘yicha hisobotini qay tarzda topshiradi?":
            "Mustaqil izlanuvchilar yiliga ikki marta, ya’ni har olti oyda amalga oshirgan ilmiy faoliyati bo‘yicha (O‘zbekiston Respublikasi Vazirlar Mahkamasining 304- qaroriga asosan: LEX.UZ - O'zbekiston qonunchiligi) hisobot topshiradi. DARAJA.ILMIY.UZ platformasiga so‘ralgan ma’lumotlarni yuklashi zarur. Attestatsiya komissiyasida og‘zaki suhbatdan o‘tadi. Yiliga bir marta monitoringga kelishi kerak.",
        "Dissertatsiyani qaysi tilda yozish mumkun?":
            "O‘zbekiston Respublikasi qonunchiligiga muvofiq dissertatsiya o‘zbek, rus, ingliz va qoraqalpoq tillarida yozilishi mumkun.",
    
    },


    "stajyor": {
        "Stajor-tadqiqotchilikka hujjat topshirish uchun qanday talablar bor?":
            "Siz dastlab ONE ID tizimi orqali DARAJA.ILMIY.UZ platformasiga kirib ro‘yxatdan o‘tishingiz va so’ralgan hujjatlarni yuklashibgiz kerak",
        "Stajor-tadqiqotchilikka topshirish uchun qanday hujjatlar kerak?":
            "– ariza \n – magistrlik diploma \n – ilmiy maqolalar \n – ilmiy izlanish konsepsiyasi \n – qisqacha tarjimai hol \n – tavsifnoma \n – mehnat faoliyatini ko‘rsatuvchi hujjat tasdiqlangan nusxasi (agar mavjud bo‘lsa) \n – ilmiy rahbar rozilik xati (dissertatsiya mavzusini tasdiqlovchi hujjat). \n – pasport nusxasi \n – (Barcha hujjatlar PDF variantda o‘rtacha 5 MB dan oshmagan bolishi kerak) \n – xorijiy til sertifikati ",
        "Stajor-tadqiqotchilikka qabul qilinish uchun ariza shakli qanday yoziladi?":
            "Ariza namunasini ushbu havoladan yuklab oling https://uzjoku.uz/uz/aktivnost-anown8qshe/ilmiy-faoliyat-up/scientificactivity",
        "Stajor-tadqiqotchilikka hujjat qabul qilish muddati qachon boshlanadi?":
            "Hujjatlar 15-sentyabrdan – 15-oktyabrgacha qabul qilinadi. Aniq muddat universitet saytida e'lon qilinadi. (https://t.me/uzjmcu, https://uzjoku.uz/uz)",
        "Qabul imtihonlari qanday shaklda o'tadi?":
            "10.00.09 Jurnalistika, 23.00.02 – Siyosiy institutlar, jarayonlar va texnologiyalar Ixtisosligi fanidan yozma imtihon va suhbat shaklida tashkil etiladi. 4 SAVOL: , yozma, tadqiqotchining ilmiy ishi bo`yicha 1 ta SAVOL: og‘zaki shaklda bo‘ladi \n – Xorijlik doktorantlar faqat suhbat asosida qabul qilinadi.",
        "Stajor-tadqiqotchilikda (PhD) o'qish qancha vaqt davom etadi?":
            "Stajor-tadqiqotchilikda tahsil olish muddati 1 yil. (Shu muddat ichida tadqiqotchi dissertatsiya mavzusini kafedra muhokamasidan o‘tkazib, ishning ilmiy konsepsiyasini shakllantirishi kerak)",
        "Stajor-tadqiqotchilarga stipendiya to'lanadimi?":
            "Ha, stajor-tadqiqotchilarga har oy belgilangan miqdorda stipendiya to'lanadi. (xorijiy stajor-tadqiqotchilarga to'lanmaydi)",
        "Stajor-tadqiqotchilikda (PhD)ga topshirish uchun til sertifikati talab etiladimi?":
            "Yo‘q",
        "Ilmiy maqolalarni qaerda chop etish kerak?":
            "OAK ro'yxatidagi jurnallarda, xalqaro va respublika konferensiyalarida, xalqaro ilmiy bazalarida maqolalar chop etilishi kerak.",
        "Stajor-tadqiqotchilikka topshirish uchun uchun maqola soni nechta bo‘lishi kerak?":
            "Kamida 1 ta ilmiy maqola va 2 ta tezis taqdim etilishi talab etiladi. Har biri uchun havola va nusxa bo'lishi zarur.",
        "Ilmiy rahbarni qanday tanlash mumkin?":
            "Ilmiy yo'nalishingiz bo'yicha O‘zJOKUda mavjud kafedrada faoliyat yuritayotgan dotsent yoki professor unvoniga ega bo‘lgan professor o’qituvchi ilmiy rahbar sifatida tanlanib, rasman tasdiqlanadi.",
        "Ilmiy konsepsiyani qanday tayyorlash kerak?":
            "Konsepsiyada tadqiqot mavzusi, maqsadi, vazifalari, yangiligi, ilmiy va amaliy ahamiyati hamda tadqiqot metodlari ko'rsatiladi.",
        "Dissertatsiyani qaysi tilda yozish mumkun?":
            "O‘zbekiston Respublikasi qonunchiligiga muvofiq dissertatsiya o‘zbek, rus, ingliz va qoraqalpoq tillarida yozilishi mumkun.",
        "Stajor-tadqiqotchilar ilmiy-tadqiqot ishi bo‘yicha hisobotini qay tarzda topshiradi?":
            "Stajor-tadqiqotchilar yiliga uch marta amalga oshirgan ilmiy faoliyati bo‘yicha (O‘zbekiston Respublikasi Vazirlar Mahkamasining 304- qaroriga asosan: LEX.UZ - O'zbekiston qonunchiligi) hisobot topshiradi. DARAJA.ILMIY.UZ platformasiga so‘ralgan ma’lumotlarni yuklashi zarur. Attestatsiya komissiyasida og‘zaki suhbatdan o‘tadi.",
        "Stajor-tadqiqotchilikdan keyingi imkoniyatlar nimalar?":
            "Stajor-tadqiqotchilikni yakunlaganlar PhD tayanch doktoranturaga qabul qilinadi.",
    }
}

# Главное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("1️⃣ Doktorantura PhD/DSc", callback_data="dir_doktorantura")],
        [InlineKeyboardButton("2️⃣ Mustaqil Tadqiqotchilik", callback_data="dir_mustaqil")],
        [InlineKeyboardButton("3️⃣ Xalqaro Tadqiqotchilik", callback_data="dir_xalqaro")],
        [InlineKeyboardButton("4️⃣ Stajor-Tadqiqotchilik", callback_data="dir_stajyor")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        "❓ *Siz ushbu bot orqali qaysi yo'nalishdagi savollarga javob topishni istaysiz?*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# Обработка выбора направления
async def handle_direction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    dir_key = query.data.replace("dir_", "")  # Например, 'phd', 'dsc'

    if dir_key not in qa_data:
        await query.edit_message_text("❗ Nomaʼlum yo‘nalish.")
        return

    questions = list(qa_data[dir_key].keys())
    context.user_data["current_dir"] = dir_key  # Сохраняем текущее направление

    buttons = [[InlineKeyboardButton(q, callback_data=f"q_{idx}")] for idx, q in enumerate(questions)]
    buttons.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")])

    reply_markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text("Savolni tanlang:", reply_markup=reply_markup)

# Обработка выбора вопроса
async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    dir_key = context.user_data.get("current_dir", "")

    if not dir_key or dir_key not in qa_data:
        await query.edit_message_text("❗ Yo‘nalish topilmadi.")
        return

    questions = list(qa_data[dir_key].keys())
    idx = int(query.data.split("_")[1])
    question = questions[idx]
    answer = qa_data[dir_key].get(question, "Javob topilmadi.")

    back_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Orqaga", callback_data=f"dir_{dir_key}")],
        [InlineKeyboardButton("🏠 Asosiy menyu", callback_data="back_main")]
    ])

    await query.edit_message_text(
        f"❓ *{question}*\n\n📘 {answer}",
        parse_mode="Markdown",
        reply_markup=back_markup
    )

# Обработка кнопки возврата
async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(query, context)

# Основной запуск
def main():
    app = Application.builder().token("7808860481:AAHDoydehllfSz6o_PeDo5CKb5eFo0Ua-3M").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_direction, pattern="^dir_"))
    app.add_handler(CallbackQueryHandler(handle_question, pattern="^q_"))
    app.add_handler(CallbackQueryHandler(handle_back, pattern="^back_main$"))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
