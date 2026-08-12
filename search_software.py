import sys
if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from collections import defaultdict
import re
from pathlib import Path


SURAH_NAME_TO_NO = {
    "فاتحه": 1,
    "بقره": 2,
    "آل‌عمران": 3,
    "نساء": 4,
    "مائده": 5,
    "انعام": 6,
    "اعراف": 7,
    "انفال": 8,
    "توبه": 9,
    "یونس": 10,
    "هود": 11,
    "یوسف": 12,
    "رعد": 13,
    "ابراهیم": 14,
    "حجر": 15,
    "نحل": 16,
    "اسراء": 17,
    "کهف": 18,
    "مریم": 19,
    "طه": 20,
    "انبیاء": 21,
    "حج": 22,
    "مومنون": 23,
    "نور": 24,
    "فرقان": 25,
    "شعراء": 26,
    "نمل": 27,
    "قصص": 28,
    "عنکبوت": 29,
    "روم": 30,
    "لقمان": 31,
    "سجده": 32,
    "احزاب": 33,
    "سبا": 34,
    "فاطر": 35,
    "یس": 36,
    "صافات": 37,
    "ص": 38,
    "زمر": 39,
    "غافر": 40,
    "فصلت": 41,
    "شوری": 42,
    "زخرف": 43,
    "دخان": 44,
    "جاثیه": 45,
    "احقاف": 46,
    "محمد": 47,
    "فتح": 48,
    "حجرات": 49,
    "ق": 50,
    "ذاریات": 51,
    "طور": 52,
    "نجم": 53,
    "قمر": 54,
    "رحمن": 55,
    "واقعه": 56,
    "حدید": 57,
    "مجادله": 58,
    "حشر": 59,
    "ممتحنه": 60,
    "صف": 61,
    "جمعه": 62,
    "منافقون": 63,
    "تغابن": 64,
    "طلاق": 65,
    "تحریم": 66,
    "ملک": 67,
    "قلم": 68,
    "حاقه": 69,
    "معارج": 70,
    "نوح": 71,
    "جن": 72,
    "مزمل": 73,
    "مدثر": 74,
    "قیامت": 75,
    "دهر": 76,
    "مرسلات": 77,
    "نبا": 78,
    "نازعات": 79,
    "عبس": 80,
    "تکویر": 81,
    "انفطار": 82,
    "مطففین": 83,
    "انشقاق": 84,
    "بروج": 85,
    "طارق": 86,
    "اعلی": 87,
    "غاشیه": 88,
    "فجر": 89,
    "بلد": 90,
    "شمس": 91,
    "لیل": 92,
    "ضحی": 93,
    "انشراح": 94,
    "تین": 95,
    "علق": 96,
    "قدر": 97,
    "بینه": 98,
    "زلزال": 99,
    "عادیات": 100,
    "قارعه": 101,
    "تکاثر": 102,
    "عصر": 103,
    "همزه": 104,
    "فیل": 105,
    "قریش": 106,
    "ماعون": 107,
    "کوثر": 108,
    "کافرون": 109,
    "نصر": 110,
    "مسد": 111,
    "اخلاص": 112,
    "فلق": 113,
    "ناس": 114,
}

SURAH_NO_TO_NAME = {v: k for k, v in SURAH_NAME_TO_NO.items()}


def resolve_surah_name(surah_input):
    """
    ورودی می‌تواند:
    - str: نام سوره
    - int: شماره سوره
    خروجی: نام استاندارد سوره (str) یا None
    """
    if isinstance(surah_input, str):
        return surah_input if surah_input in SURAH_NAME_TO_NO else None

    if isinstance(surah_input, int):
        return SURAH_NO_TO_NAME.get(surah_input)

    return None




year1_table = [
    {"surah":"علق",     "ranges":[(1,5)],            "topic":"آغاز وحی",                 "year":"سال اول بعثت", "revelation_order":1,  "ayah_count":5,  "word_count":19, "cumulative_ayahs":5,   "cumulative_words":19,  "surah_no":96},
    {"surah":"مدثر",    "ranges":[(1,7)],            "topic":"رسالت",                    "year":"سال اول بعثت", "revelation_order":2,  "ayah_count":7,  "word_count":16, "cumulative_ayahs":12,  "cumulative_words":35,  "surah_no":74},
    {"surah":"عصر",     "ranges":[(1,2)],            "topic":"دو آیه اول",               "year":"سال اول بعثت", "revelation_order":3,  "ayah_count":2,  "word_count":5,  "cumulative_ayahs":14,  "cumulative_words":40,  "surah_no":103},
    {"surah":"ذاریات",  "ranges":[(1,6)],            "topic":"اعلام قیامت",              "year":"سال اول بعثت", "revelation_order":4,  "ayah_count":6,  "word_count":14, "cumulative_ayahs":20,  "cumulative_words":54,  "surah_no":51},
    {"surah":"تکاثر",   "ranges":[(1,2)],            "topic":"مردم‌شناسی",               "year":"سال اول بعثت", "revelation_order":5,  "ayah_count":2,  "word_count":5,  "cumulative_ayahs":22,  "cumulative_words":59,  "surah_no":102},
    {"surah":"طور",     "ranges":[(1,8)],            "topic":"اعلام قیامت",              "year":"سال اول بعثت", "revelation_order":6,  "ayah_count":8,  "word_count":20, "cumulative_ayahs":30,  "cumulative_words":79,  "surah_no":52},
    {"surah":"اخلاص",   "ranges":[(1,4)],            "topic":"تمام سوره",                "year":"سال اول بعثت", "revelation_order":7,  "ayah_count":4,  "word_count":12, "cumulative_ayahs":34,  "cumulative_words":91,  "surah_no":112},

    # غاشیه دو تکه است: 1-5 و 8-16
    {"surah":"غاشیه",   "ranges":[(1,5),(8,16)],     "topic":"توصیف بهشت و جهنم",        "year":"سال اول بعثت", "revelation_order":8,  "ayah_count":14, "word_count":38, "cumulative_ayahs":48,  "cumulative_words":129, "surah_no":88},

    {"surah":"طارق",    "ranges":[(11,17)],          "topic":"وحی و نبوت",               "year":"سال اول بعثت", "revelation_order":9,  "ayah_count":7,  "word_count":21, "cumulative_ayahs":55,  "cumulative_words":150, "surah_no":86},
    {"surah":"انفطار",  "ranges":[(1,5)],            "topic":"حدوث قیامت",               "year":"سال اول بعثت", "revelation_order":10, "ayah_count":5,  "word_count":17, "cumulative_ayahs":60,  "cumulative_words":167, "surah_no":82},
    {"surah":"شمس",     "ranges":[(1,10)],           "topic":"مردم‌شناسی",               "year":"سال اول بعثت", "revelation_order":11, "ayah_count":10, "word_count":31, "cumulative_ayahs":70,  "cumulative_words":198, "surah_no":91},
    {"surah":"کوثر",    "ranges":[(1,3)],            "topic":"تمام سوره",                "year":"سال اول بعثت", "revelation_order":12, "ayah_count":3,  "word_count":10, "cumulative_ayahs":73,  "cumulative_words":208, "surah_no":108},

    # اعلی دو تکه است: 1-6 و 8-9
    {"surah":"اعلی",    "ranges":[(1,6),(8,9)],      "topic":"تذکر و تقویت",             "year":"سال اول بعثت", "revelation_order":13, "ayah_count":8,  "word_count":25, "cumulative_ayahs":81,  "cumulative_words":233, "surah_no":87},

    # بروج دو تکه است: 1-7 و 12-22
    {"surah":"بروج",    "ranges":[(1,7),(12,22)],    "topic":"تنذیر",                    "year":"سال اول بعثت", "revelation_order":14, "ayah_count":17, "word_count":55, "cumulative_ayahs":98,  "cumulative_words":288, "surah_no":85},

    {"surah":"تکویر",   "ranges":[(1,29)],           "topic":"تمام سوره",                "year":"سال اول بعثت", "revelation_order":15, "ayah_count":29, "word_count":103,"cumulative_ayahs":127, "cumulative_words":391, "surah_no":81},
]


year2_table = [
    {"surah":"انشراح",  "ranges":[(1,8)],  "topic":"تمام سوره", "year":"سال دوم بعثت", "revelation_order":16, "ayah_count":8,  "word_count":27, "cumulative_ayahs":135, "cumulative_words":418, "surah_no":94},
    {"surah":"ضحی",     "ranges":[(1,11)], "topic":"تمام سوره", "year":"سال دوم بعثت", "revelation_order":17, "ayah_count":11, "word_count":38, "cumulative_ayahs":146, "cumulative_words":456, "surah_no":93},
    {"surah":"ناس",     "ranges":[(1,6)],  "topic":"تمام سوره", "year":"سال دوم بعثت", "revelation_order":18, "ayah_count":6,  "word_count":20, "cumulative_ayahs":152, "cumulative_words":476, "surah_no":114},
    {"surah":"نازعات",  "ranges":[(1,26)], "topic":"تنذیر",     "year":"سال دوم بعثت", "revelation_order":19, "ayah_count":26, "word_count":90, "cumulative_ayahs":178, "cumulative_words":566, "surah_no":79},

    {"surah":"مدثر", "ranges":[(8,10)],        "topic":"تنذیر و قیامت",          "year":"سال دوم بعثت", "revelation_order":20},
    {"surah":"لیل",  "ranges":[(1,21)],        "topic":"تمام سوره",              "year":"سال دوم بعثت", "revelation_order":21},
    {"surah":"ماعون","ranges":[(1,7)],         "topic":"تمام سوره",              "year":"سال دوم بعثت", "revelation_order":22},

    # معارج دو تکه: 5–18
    {"surah":"معارج","ranges":[(5,18)],        "topic":"حدوث قیامت و تنذیر",      "year":"سال دوم بعثت", "revelation_order":23},

    {"surah":"شمس",  "ranges":[(11,16)],       "topic":"اولین داستان تنذیری",     "year":"سال دوم بعثت", "revelation_order":24},
    {"surah":"مرسلات",  "ranges":[(1,50)],        "topic":"تمام سوره",              "year":"سال دوم بعثت", "revelation_order":25},
    {"surah":"نبا",  "ranges":[(1,36)],        "topic":"انباء بزرگ",              "year":"سال دوم بعثت", "revelation_order":26},

    # مدثر چندتکه
    {"surah":"مدثر","ranges":[(11,30), (34,55)],        "topic":"توبیخ و تنذیر",            "year":"سال دوم بعثت", "revelation_order":27},

    {"surah":"قریش","ranges":[(1,5)],          "topic":"تمام سوره",              "year":"سال دوم بعثت", "revelation_order":28},

    # نجم (آیات 1–23)
    {"surah":"نجم",  "ranges":[(1,22), (24,25)],        "topic":"اعلام وحی و مبارزه با بت‌ها","year":"سال دوم بعثت","revelation_order":29},

    {"surah":"فجر",  "ranges":[(1,13), (28,31)],        "topic":"تنذیر و تبشیر",            "year":"سال دوم بعثت", "revelation_order":30},
    {"surah":"انشقاق","ranges":[(1,25)],       "topic":"تمام سوره",              "year":"سال دوم بعثت", "revelation_order":31},
    {"surah":"عبس",  "ranges":[(1,43)],        "topic":"تمام سوره",              "year":"سال دوم بعثت", "revelation_order":32},
    {"surah":"همزه","ranges":[(1,9)],          "topic":"تمام سوره",              "year":"سال دوم بعثت", "revelation_order":33},
    {"surah":"کافرون","ranges":[(1,6)],        "topic":"تمام سوره",              "year":"سال دوم بعثت", "revelation_order":34},

    # علق بخش دوم
    {"surah":"علق",  "ranges":[(6,19)],        "topic":"آیات بعدی",               "year":"سال دوم بعثت", "revelation_order":35},

    # غاشیه بخش دوم
    {"surah":"غاشیه","ranges":[(6,7), (17,26)],       "topic":"استدلال‌های توحیدی",      "year":"سال دوم بعثت", "revelation_order":36},

    # قیامت دو بخش
    {"surah":"قیامت","ranges":[(7,13), (20, 40)],        "topic":"حدوث قیامت و غفلت بشر",    "year":"سال دوم بعثت", "revelation_order":37},

    {"surah":"تین",  "ranges":[(1,8)],         "topic":"تمام سوره",              "year":"سال دوم بعثت", "revelation_order":38},

    {"surah":"قیامت","ranges":[(1,6), (14,19)],         "topic":"اعلام زمان قیامت",         "year":"سال دوم بعثت", "revelation_order":39},

    {"surah":"واقعه","ranges":[(1,98)],        "topic":"تمام سوره",              "year":"سال دوم بعثت", "revelation_order":40},

    {"surah":"رحمن","ranges":[(1,6), (9, 27), (46, 77)],         "topic":"خلقت و نعمت",              "year":"سال دوم بعثت", "revelation_order":41},

    # اعلی دو بخش
    {"surah":"اعلی", "ranges":[(7,7), (10,14)],       "topic":"مردم‌شناسی",              "year":"سال دوم بعثت", "revelation_order":42.0},
]



year3_table = [

    {"surah":"اعلی", "ranges":[(15,19)],       "topic":"مردم‌شناسی",              "year":"سال سوم بعثت", "revelation_order":42.5},
    {"surah":"فاتحه","ranges":[(1,7)],         "topic":"تمام سوره",              "year":"سال سوم بعثت", "revelation_order":43},
    {"surah":"عادیات","ranges":[(1,11)],       "topic":"تمام سوره",              "year":"سال سوم بعثت", "revelation_order":44},
    {"surah":"حاقه",   "ranges":[(38,52)],        "topic":"وحی و نبوت",                 "year":"سال سوم بعثت", "revelation_order":45},
    {"surah":"نازعات", "ranges":[(27,46)],        "topic":"استدلال و توضیح",            "year":"سال سوم بعثت", "revelation_order":46},
    {"surah":"مسد",    "ranges":[(1,5)],          "topic":"تمام سوره",                 "year":"سال سوم بعثت", "revelation_order":47},
    {"surah":"فلق",    "ranges":[(1,5)],          "topic":"تمام سوره",                 "year":"سال سوم بعثت", "revelation_order":48},
    {"surah":"بلد",    "ranges":[(1,20)],         "topic":"تمام سوره",                 "year":"سال سوم بعثت", "revelation_order":49},
    {"surah":"تکاثر",  "ranges":[(3,8)],          "topic":"آیات آخر",                  "year":"سال سوم بعثت", "revelation_order":50},
    {"surah":"فیل",    "ranges":[(1,5)],          "topic":"تمام سوره",                 "year":"سال سوم بعثت", "revelation_order":51},
    {"surah":"قلم",    "ranges":[(1,16)],         "topic":"اعتراض و اعراض نسبت به مشرکین","year":"سال سوم بعثت","revelation_order":52},
    {"surah":"فجر",    "ranges":[(14,27)],        "topic":"مردم‌شناسی و تنذیر آخرت",    "year":"سال سوم بعثت", "revelation_order":53},
    {"surah":"زلزال",  "ranges":[(1,8)],          "topic":"تمام سوره",                 "year":"سال سوم بعثت", "revelation_order":54},
    {"surah":"طارق",   "ranges":[(1,10)],         "topic":"استدلال قیامت",             "year":"سال سوم بعثت", "revelation_order":55},
    {"surah":"نجم",    "ranges":[(34,62)],        "topic":"مردم‌شناسی، حکمت و توحید",   "year":"سال سوم بعثت", "revelation_order":56},
    {"surah":"قارعه",  "ranges":[(1,8)],          "topic":"تمام سوره",                 "year":"سال سوم بعثت", "revelation_order":57},
    {"surah":"صافات",  "ranges":[(1,182)],        "topic":"تمام سوره",                 "year":"سال سوم بعثت", "revelation_order":58},
    {"surah":"انفطار", "ranges":[(6,20)],         "topic":"تذکر و تنذیر قیامت",         "year":"سال سوم بعثت", "revelation_order":59},
    {"surah":"حاقه",   "ranges":[(1,3), (13,37)],         "topic":"قیامت",                     "year":"سال سوم بعثت", "revelation_order":60},
    {"surah":"معارج",  "ranges":[(19,35)],         "topic":"مردم‌شناسی",                "year":"سال سوم بعثت", "revelation_order":61},
    {"surah":"مطففین", "ranges":[(1,36)],         "topic":"تمام سوره",                 "year":"سال سوم بعثت", "revelation_order":62},
    {"surah":"دخان",   "ranges":[(43,59)],        "topic":"توصیف بهشت و جهنم",          "year":"سال سوم بعثت", "revelation_order":63},
    {"surah":"مومنون", "ranges":[(1,11)],         "topic":"بشارت و وصف مؤمنین",         "year":"سال سوم بعثت", "revelation_order":64},
    {"surah":"شعراء",  "ranges":[(52,227)],       "topic":"دنباله داستان موسی و انبیاء","year":"سال سوم بعثت","revelation_order":65},
    {"surah":"ص",      "ranges":[(67,88)],        "topic":"قیامت و خلقت",              "year":"سال سوم بعثت", "revelation_order":66},
    {"surah":"حجر",    "ranges":[(1, 5), (49,99)],        "topic":"داستان‌های تنذیری و نبوت",  "year":"سال سوم بعثت", "revelation_order":67},

    # توجه: این یکی هنوز سال سوم است
    {"surah":"حاقه",   "ranges":[(4, 6)],          "topic":"امم گذشته (بخش اول)",       "year":"سال سوم بعثت", "revelation_order":68.0},

]



year4_table = [
    # فقط ردیف آخر صفحه
    {"surah":"حاقه", "ranges":[(7,12)], "topic":"بقیه امم گذشته", "year":"سال چهارم بعثت", "revelation_order":68.5},
    {"surah":"قدر",   "ranges":[(1,5)],            "topic":"تمام سوره",                 "year":"سال چهارم بعثت", "revelation_order":69},
    {"surah":"ذاریات","ranges":[(7,60)],           "topic":"استدلال و توصیف و تنذیر",   "year":"سال چهارم بعثت", "revelation_order":70},
    {"surah":"قمر",   "ranges":[(1,55)],           "topic":"تمام سوره",                 "year":"سال چهارم بعثت", "revelation_order":71},
    {"surah":"قلم",   "ranges":[(17,52)],          "topic":"تنبیه و تنذیر توحیدی",      "year":"سال چهارم بعثت", "revelation_order":72},
    {"surah":"دخان",  "ranges":[(1,42)],           "topic":"وحی و قیامت و امم گذشته",   "year":"سال چهارم بعثت", "revelation_order":73},
    {"surah":"معارج","ranges":[(1, 4), (36,44)],           "topic":"بحث روی قیامت",             "year":"سال چهارم بعثت", "revelation_order":74},
    {"surah":"طور",   "ranges":[(9, 20), (22,28)],          "topic":"توصیف بهشت و جهنم",          "year":"سال چهارم بعثت", "revelation_order":75},
    {"surah":"زخرف",  "ranges":[(66,78)],          "topic":"آیات قیامت",                "year":"سال چهارم بعثت", "revelation_order":76},
    {"surah":"نوح",   "ranges":[(1,29)],           "topic":"تمام سوره",                 "year":"سال چهارم بعثت", "revelation_order":77},
    {"surah":"رحمن",  "ranges":[(7,8), (28, 45), (78, 78)],   "topic":"عذاب و نعمت",               "year":"سال چهارم بعثت", "revelation_order":78},
    {"surah":"مزمل","ranges":[(1,19)],           "topic":"تمام سوره",                 "year":"سال چهارم بعثت", "revelation_order":79},
    {"surah":"طه",    "ranges":[(1,54)],           "topic":"موسی و فرعون",               "year":"سال چهارم بعثت", "revelation_order":80},
    {"surah":"مریم",  "ranges":[(76,98)],          "topic":"تنذیر آخرت",                "year":"سال چهارم بعثت", "revelation_order":81},
    {"surah":"طور",   "ranges":[(21, 21), (29,49)],          "topic":"جدال توحیدی",               "year":"سال چهارم بعثت", "revelation_order":82},
    {"surah":"حجر",   "ranges":[(6,48)],           "topic":"جدال و استدلال توحیدی",     "year":"سال چهارم بعثت", "revelation_order":83},
    {"surah":"شعراء", "ranges":[(1,51)],           "topic":"ابتدای داستان موسی",        "year":"سال چهارم بعثت", "revelation_order":84},
    {"surah":"دهر",   "ranges":[(1,29)],           "topic":"تمام سوره (جز دو آیه آخر)", "year":"سال چهارم بعثت", "revelation_order":85.0},

]


year5_table = [
    {"surah":"دهر",   "ranges":[(30,31)],          "topic":"دو آیه آخر",                "year":"سال پنجم بعثت", "revelation_order":85.5},
    {"surah":"ص",       "ranges":[(1,24), (29, 66)],           "topic":"توصیف انبیاء و تنذیر",      "year":"سال پنجم بعثت", "revelation_order":86},
    {"surah":"ق",       "ranges":[(1,45)],           "topic":"تمام سوره",                 "year":"سال پنجم بعثت", "revelation_order":87},
    {"surah":"یس",      "ranges":[(1,83)],           "topic":"تمام سوره",                 "year":"سال پنجم بعثت", "revelation_order":88},
    {"surah":"عصر",     "ranges":[(3,3)],            "topic":"آیه آخر",                   "year":"سال پنجم بعثت", "revelation_order":89},
    {"surah":"مومنون",  "ranges":[(12,118)],         "topic":"خلقت، نعمت انبیاء و آخرت",  "year":"سال پنجم بعثت", "revelation_order":90},
    {"surah":"فصلت",    "ranges":[(1,7)],            "topic":"قرآن و رسالت در برابر مشرکین","year":"سال پنجم بعثت","revelation_order":91},
    {"surah":"زخرف",  "ranges":[(1,65),(79,89)], "topic":"جدال توحیدی",          "year":"سال پنجم بعثت", "revelation_order":92},
    {"surah":"احزاب", "ranges":[(1,1),(2,2),(3,3),(7,7),(8,8),(41,47),(63,68)],
                      "topic":"آیات کلی زمینه قبلی", "year":"سال پنجم بعثت", "revelation_order":93},
    {"surah":"انبیاء","ranges":[(1,10)],          "topic":"ده آیه اول",          "year":"سال پنجم بعثت", "revelation_order":94.0},
]


year6_table = [
    {"surah":"انبیاء","ranges":[(11,112)],       "topic":"بقیه سوره",                 "year":"سال ششم بعثت", "revelation_order":94.5},
    {"surah":"جن",    "ranges":[(1,28)],         "topic":"تمام سوره",                 "year":"سال ششم بعثت", "revelation_order":95},
    {"surah":"نبا",   "ranges":[(37,41)],        "topic":"تنذیر قیامت",                "year":"سال ششم بعثت", "revelation_order":96},
    {"surah":"بروج",  "ranges":[(8,11)],         "topic":"توضیح",                     "year":"سال ششم بعثت", "revelation_order":97},
    {"surah":"مریم",  "ranges":[(1,34),(42,75)], "topic":"ولادت یحیی و مریم و مسیح",  "year":"سال ششم بعثت", "revelation_order":98},
    {"surah":"بینه",  "ranges":[(1,9)],          "topic":"تمام سوره",                 "year":"سال ششم بعثت", "revelation_order":99},
    {"surah":"لقمان", "ranges":[(1,10)],         "topic":"قرآن و مردم‌شناسی و توحید", "year":"سال ششم بعثت", "revelation_order":100},
    {"surah":"روم",   "ranges":[(1,26)],         "topic":"ثلث اول",                   "year":"سال ششم بعثت", "revelation_order":101},
    {"surah":"فرقان", "ranges":[(1,77)],         "topic":"تمام سوره",                 "year":"سال ششم بعثت", "revelation_order":102},
    {"surah":"طه",    "ranges":[(55,73)],        "topic":"سحره، سامری، آدم",           "year":"سال ششم بعثت", "revelation_order":103.0},
]

year7_table = [
    {"surah":"طه",     "ranges":[(74,135)],                         "topic":"بقیه سوره",              "year":"سال هفتم بعثت", "revelation_order":103.5},
    {"surah":"ملک",    "ranges":[(1,30)],                           "topic":"تمام سوره",              "year":"سال هفتم بعثت", "revelation_order":104},
    {"surah":"ابراهیم","ranges":[(43,52)],                          "topic":"تنذیر و توصیف آخرت",     "year":"سال هفتم بعثت", "revelation_order":105},
    {"surah":"مریم",   "ranges":[(35,41)],                          "topic":"توضیحات راجع به حضرت عیسی","year":"سال هفتم بعثت","revelation_order":106},
    {"surah":"نحل",    "ranges":[(1,34),(43,66),(100,107),(121,129)],"topic":"توحیدی، تربیتی، وحدت",   "year":"سال هفتم بعثت", "revelation_order":107},
    {"surah":"کهف",
     "ranges":[(1,7),(59, 110)],
     "topic":"ذوالقرنین، لقاء پروردگار",
     "year":"سال هفتم بعثت",
     "revelation_order":108},

    {"surah":"بقره",
     "ranges":[(1,19),(148,152),(154,158),(200,205),(245,246)],
     "topic":"مردم‌شناسی و جهاد",
     "year":"سال هفتم بعثت",
     "revelation_order":109},

    {"surah":"سجده",
     "ranges":[(1,26)],
     "topic":"۲۶ آیه اول",
     "year":"سال هفتم بعثت",
     "revelation_order":110.0},
]

year8_table = [
    {"surah":"سجده",   "ranges":[(27,30)],                       "topic":"بقیه سوره", "year":"سال هشتم بعثت", "revelation_order":110.5},
    {"surah":"مدثر",   "ranges":[(31,34)],                       "topic":"توضیح فرشتگان", "year":"سال هشتم بعثت", "revelation_order":111},
    {"surah":"اسراء",  "ranges":[(9,54),(63,67),(73,83),(103,111)], "topic":"معرفت و تربیت، موسی و فرعون", "year":"سال هشتم بعثت", "revelation_order":112},
    {"surah":"غافر",   "ranges":[(1,6),(54,62)],                 "topic":"بخشش و یاری خدا و تکذیب مشرکین", "year":"سال هشتم بعثت", "revelation_order":113},
    {"surah":"نمل",    "ranges":[(1,95)],                        "topic":"تمام سوره", "year":"سال هشتم بعثت", "revelation_order":114},
    {"surah":"زمر",    "ranges":[(30,38),(54,66)],               "topic":"مرگ، آخرت، توبه", "year":"سال هشتم بعثت", "revelation_order":115},
    {"surah":"جاثیه",  "ranges":[(1,36)],                        "topic":"تمام سوره", "year":"سال هشتم بعثت", "revelation_order":116},
    {"surah":"تغابن",  "ranges":[(1,18)],                        "topic":"تمام سوره", "year":"سال هشتم بعثت", "revelation_order":117},
    {"surah":"هود",    "ranges":[(1,24)],                        "topic":"۲۴ آیه اول", "year":"سال هشتم بعثت", "revelation_order":118.0},
]


year9_table = [
    {"surah":"هود",    "ranges":[(25,123)],          "topic":"بقیه سوره", "year":"سال نهم بعثت", "revelation_order":118.5},
    {"surah":"فصلت",   "ranges":[(8,38)],            "topic":"تجلیل خدا، تنذیر، تربیت، معرفت", "year":"سال نهم بعثت", "revelation_order":119},
    {"surah":"روم",    "ranges":[(27,60)],           "topic":"دو ثلث آخر", "year":"سال نهم بعثت", "revelation_order":120},
    {"surah":"اسراء",  "ranges":[(1,8),(84,102)],    "topic":"بنی‌اسرائیل و وحی و معرفت", "year":"سال نهم بعثت", "revelation_order":121},
    {"surah":"اعراف",  "ranges":[(57,111)],          "topic":"بحث و برخورد با پیامبران", "year":"سال نهم بعثت", "revelation_order":122.0},
]


year10_table = [
    {"surah":"اعراف",   "ranges":[(112,154),(176,205)], "topic":"بحث انبیاء با امم گذشته", "year":"سال دهم بعثت", "revelation_order":122.5},
    {"surah":"نور",     "ranges":[(45,56)],             "topic":"مردم‌شناسی",              "year":"سال دهم بعثت", "revelation_order":123},
    {"surah":"حج",      "ranges":[(18,30),(43,68)],     "topic":"توحید و تنذیر، جدال، اعلام حج", "year":"سال دهم بعثت", "revelation_order":124},
    {"surah":"انعام",   "ranges":[(1,30),(74,82),(105,117)], "topic":"تعلیم و جدال توحیدی، مکاشفه ابراهیم", "year":"سال دهم بعثت", "revelation_order":125},
    {"surah":"عنکبوت",  "ranges":[(1,69)],             "topic":"تمام سوره",               "year":"سال دهم بعثت", "revelation_order":126},
    {"surah":"سبا",     "ranges":[(10,12)],            "topic":"داود و سبأ، توحید و نبوت", "year":"سال دهم بعثت", "revelation_order":127.0},
]

year11_table = [
    {"surah":"سبا",   "ranges":[(13,54)],      "topic":"بقیه آیات",         "year":"سال یازدهم بعثت", "revelation_order":127.5},
    {"surah":"یونس",  "ranges":[(72,109)],      "topic":"انبیاه",         "year":"سال یازدهم بعثت", "revelation_order":128},
    {"surah":"یوسف",  "ranges":[(1,111)],      "topic":"تمام سوره",         "year":"سال یازدهم بعثت", "revelation_order":129},
    {"surah":"قصص",   "ranges":[(1,44)],       "topic":"داستان طولانی موسی", "year":"سال یازدهم بعثت", "revelation_order":130.0},
]


year12_table = [
    {"surah":"قصص",   "ranges":[(45,75),(85,88)], "topic":"ادامه آیات قصص", "year":"سال دوازدهم بعثت", "revelation_order":130.5},
    {"surah":"مزمل",  "ranges":[(20,20)],         "topic":"آیه آخر",        "year":"سال دوازدهم بعثت", "revelation_order":131},
    {"surah":"غافر",  "ranges":[(7,53),(63,85)],  "topic":"مؤمن آل فرعون، توصیف خدا و تنذیر مشرکین", "year":"سال دوازدهم بعثت", "revelation_order":132},
    {"surah":"نجم",   "ranges":[(23,23),(26,33)], "topic":"توضیح و توبیخ مشرکین", "year":"سال دوازدهم بعثت", "revelation_order":133},
    {"surah":"ص",     "ranges":[(25,28)],         "topic":"الحاقی تربیتی و توحیدی", "year":"سال دوازدهم بعثت", "revelation_order":134},
    {"surah":"کهف",
     "ranges":[(28,58)],
     "topic":"دو باغ، زندگی دنیا، قیامت، قرآن، رسالت و هلاکت",
     "year":"سال دوازدهم بعثت",
     "revelation_order":135},

    {"surah":"لقمان",
     "ranges":[(11,34)],
     "topic":"حکمت و معرفت",
     "year":"سال دوازدهم بعثت",
     "revelation_order":136},

    {"surah":"ابراهیم",
     "ranges":[(1,5), (7, 35), (37, 42)],
     "topic":"رسالت و توحید، تنذیر، دعای ابراهیم",
     "year":"سال دوازدهم بعثت",
     "revelation_order":137},

    {"surah":"شوری",
     "ranges":[(1,14)],
     "topic":"۱۴ آیه اول",
     "year":"سال دوازدهم بعثت",
     "revelation_order":138.0},
]


year13_table = [
    {"surah":"شوری",
     "ranges":[(15,53)],
     "topic":"بقیه آیات",
     "year":"سال سیزدهم بعثت / اول هجرت",
     "revelation_order":138.5},

    {"surah":"بقره",
     "ranges":[(28,37),(186,191)],
     "topic":"خلقت آدم، حکم جنگ",
     "year":"سال سیزدهم بعثت / اول هجرت",
     "revelation_order":139},

    {"surah":"فاطر",
     "ranges":[(4,8),(10,12), (14,45)],
     "topic":"آیات اولیه",
     "year":"سال سیزدهم بعثت / اول هجرت",
     "revelation_order":140},

    {"surah":"زمر",
     "ranges":[(1,29),(39,53)],
     "topic":"توحیدی، تنذیر، توصیف قرآن",
     "year":"سال سیزدهم بعثت / اول هجرت",
     "revelation_order":141},

    {"surah":"محمد",
     "ranges":[(1,38)],
     "topic":"تمام سوره",
     "year":"سال سیزدهم بعثت / اول هجرت",
     "revelation_order":142},

    {"surah":"انفال",
     "ranges":[(1,60)],
     "topic":"۶ آیه اول",
     "year":"سال سیزدهم بعثت / اول هجرت",
     "revelation_order":143.0},
]

year2_hijri_table = [
    {"surah":"انفال",
     "ranges":[(61,76)],
     "topic":"بقیه آیات",
     "year":"سال دوم هجرت",
     "revelation_order":143.5},

    {"surah":"صف",
     "ranges":[(1,14)],
     "topic":"تمام سوره",
     "year":"سال دوم هجرت",
     "revelation_order":144},

    {"surah":"فصلت",
     "ranges":[(39,54)],
     "topic":"استدلال قیامت، قرآن و توحید",
     "year":"سال دوم هجرت",
     "revelation_order":145},

    {"surah":"اسراء",
     "ranges":[(55,62),(68,72)],
     "topic":"اخلاقی، توحیدی و نبوت",
     "year":"سال دوم هجرت",
     "revelation_order":146},

    {"surah":"احقاف",
     "ranges":[(1,13),(26,27)],
     "topic":"توحید، نبوت و استقامت",
     "year":"سال دوم هجرت",
     "revelation_order":147},

     {"surah":"نحل",
     "ranges":[(35,42),(67,91),(108,120)],
     "topic":"جدال توحیدی و تشریعی، نعم الهی و تقویت روحی",
     "year":"سال دوم هجرت",
     "revelation_order":148},

    {"surah":"مائده",
     "ranges":[(10,14),(23,29),(37,44)],
     "topic":"انضباطی و داستانی و تشریعی",
     "year":"سال دوم هجرت",
     "revelation_order":149},

    {"surah":"جمعه",
     "ranges":[(1,11)],
     "topic":"تمام سوره",
     "year":"سال دوم هجرت",
     "revelation_order":150},

    {"surah":"آل‌عمران",
     "ranges":[(30,93)],
     "topic":"ولادت مریم و عیسی، اهل کتاب، جنگ احد",
     "year":"سال دوم هجرت",
     "revelation_order":151.0},
]

year3_hijri_table = [
    {"surah":"آل‌عمران",
     "ranges":[(94,176)],
     "topic":"بقیه آیات",
     "year":"سال سوم هجرت",
     "revelation_order":151.5},

    {"surah":"منافقون",
     "ranges":[(1,11)],
     "topic":"تمام سوره",
     "year":"سال سوم هجرت",
     "revelation_order":152},

    {"surah":"حج",
     "ranges":[(1, 17),(31,42),(69,77)],
     "topic":"توحید، قیامت، عبادت",
     "year":"سال سوم هجرت",
     "revelation_order":153},

    {"surah":"آل‌عمران",
     "ranges":[(1,29),(177,200)],
     "topic":"مردم‌شناسی",
     "year":"سال سوم هجرت",
     "revelation_order":154},

    {"surah":"اعراف",
     "ranges":[(1,30)],
     "topic":"خلقت آدم، قیامت، توحید",
     "year":"سال سوم هجرت",
     "revelation_order":155.0},
]


year4_hijri_table = [
    {"surah":"اعراف",
     "ranges":[(31,56),(155,175)],
     "topic":"ادامه آیات اعراف",
     "year":"سال چهارم هجرت",
     "revelation_order":155.5},

    {"surah":"حشر",
     "ranges":[(1,24)],
     "topic":"تمام سوره",
     "year":"سال چهارم هجرت",
     "revelation_order":156},

    {"surah":"زمر",
     "ranges":[(67,75)],
     "topic":"توصیف قیامت و تقسیم مردم",
     "year":"سال چهارم هجرت",
     "revelation_order":157},

    {"surah":"سبا",
     "ranges":[(1,9)],
     "topic":"توحید و نبوت",
     "year":"سال چهارم هجرت",
     "revelation_order":158},

    {"surah":"توبه",
     "ranges":[(38,71)],
     "topic":"منافقین",
     "year":"سال چهارم هجرت",
     "revelation_order":159},

     {"surah":"یونس",
     "ranges":[(1,71)],
     "topic":"استدلال توحید و نبوت",
     "year":"سال چهارم هجرت",
     "revelation_order":160},
]


year5_hijri_table = [
    {"surah":"حدید", "ranges":[(1,8)],     "topic":"۸ آیه اول سوره",            "year":"سال پنجم هجرت", "revelation_order":161.0},
    {"surah":"حدید", "ranges":[(9,29)],    "topic":"بقیه آیات",                 "year":"سال پنجم هجرت", "revelation_order":161.5},
    {"surah":"نحل",  "ranges":[(91,99)],   "topic":"تشریعی و اجتماعی و اخلاقی", "year":"سال پنجم هجرت", "revelation_order":162},
    {"surah":"نور",  "ranges":[(1,33)],    "topic":"آیات افک",                  "year":"سال پنجم هجرت", "revelation_order":163},
    {"surah":"بقره", "ranges":[(38,147)],  "topic":"بنی‌اسرائیل، ابراهیم، قبله", "year":"سال پنجم هجرت", "revelation_order":164},
    {"surah":"احزاب","ranges":[(4, 6), (9,22)],    "topic":"آیات مدنی",                 "year":"سال پنجم هجرت", "revelation_order":165.0},
]

year6_hijri_table = [
    {"surah":"احزاب","ranges":[(23,40), (48, 52), (56, 62), (69, 73)],   "topic":"بقیه آیات",                 "year":"سال ششم هجرت", "revelation_order":165.5},
    {"surah":"نساء", "ranges":[(47,60),(130,148), (149, 174)], "topic":"اهل کتاب، مردم‌شناسی", "year":"سال ششم هجرت", "revelation_order":166},
    {"surah":"انعام","ranges":[(31,73),(83,104),(118,134), (155, 165)],
                      "topic":"جدال توحیدی، نبوت، تشریع", "year":"سال ششم هجرت", "revelation_order":167},
    {"surah":"رعد", "ranges":[(1,12)],     "topic":"12 آیه اول",            "year":"سال ششم هجرت", "revelation_order":168.0},
]


year7_hijri_table = [
    {"surah":"رعد",  "ranges":[(13,43)],   "topic":"بقیه آیات",                 "year":"سال هفتم هجرت", "revelation_order":168.5},
    {"surah":"توبه", "ranges":[(72,130)],  "topic":"منافقین، مؤمنین، کفار",      "year":"سال هفتم هجرت", "revelation_order":169},
    {"surah":"فتح",  "ranges":[(1,29)],    "topic":"تمام سوره",                 "year":"سال هفتم هجرت", "revelation_order":170},
    {"surah":"طلاق", "ranges":[(8,12)],    "topic":"تنذیر و توحید",              "year":"سال هفتم هجرت", "revelation_order":171},
    {"surah":"مائده","ranges":[(56,88)],   "topic":"روابط با اهل کتاب",          "year":"سال هفتم هجرت", "revelation_order":172},
    {"surah":"حجرات","ranges":[(1,18)],    "topic":"تمام سوره",                 "year":"سال هفتم هجرت", "revelation_order":173},
    {"surah":"قصص",  "ranges":[(76,84)],   "topic":"داستان قارون",              "year":"سال هفتم هجرت", "revelation_order":174},
]


year8_hijri_table = [
    {"surah":"نساء", "ranges":[(1, 45),(61,125)],  "topic":"تشریعی و جهاد و مردم‌شناسی", "year":"سال هشتم هجرت", "revelation_order":175},
    {"surah":"کهف",  "ranges":[(8,27)],    "topic":"داستان اصحاب کهف",           "year":"سال هشتم هجرت", "revelation_order":176},
    {"surah":"توبه",
     "ranges":[(1,37)],
     "topic":"آیات برائت",
     "year":"سال هشتم هجرت",
     "revelation_order":177},

    {"surah":"احقاف",
     "ranges":[(14,25),(28,31)],
     "topic":"والدین، احقاف، جن‌ها، تنذیر و تقویت",
     "year":"سال هشتم هجرت",
     "revelation_order":178.0},
]


year9_hijri_table = [
    {"surah":"احقاف",
     "ranges":[(32,35)],
     "topic":"بقیه آیات",
     "year":"سال نهم هجرت",
     "revelation_order":178.5},

    {"surah":"نصر",
     "ranges":[(1,3)],
     "topic":"تمام سوره",
     "year":"سال نهم هجرت",
     "revelation_order":179},

    {"surah":"ابراهیم",
     "ranges":[(6, 6), (36, 36)],
     "topic":"آیات تکمیلی",
     "year":"سال نهم هجرت",
     "revelation_order":180},

    {"surah":"مجادله",
     "ranges":[(1,23)],
     "topic":"تمام سوره",
     "year":"سال نهم هجرت",
     "revelation_order":181},

    {"surah":"مائده",
     "ranges":[(30,36),(89,120)],
     "topic":"داستان و تشریع، مائده",
     "year":"سال نهم هجرت",
     "revelation_order":182},

    {"surah":"بقره",
     "ranges":[(19,27), (153, 153), (160, 185), (192, 199), (206, 243), (255, 255), (263, 274)],
     "topic":"تنذیر و تشریع، ایمان اجتماعی",
     "year":"سال نهم هجرت",
     "revelation_order":183.0},
]


year10_hijri_table = [
    {"surah":"بقره",
     "ranges":[(275,283)],
     "topic":"بقیه آیات",
     "year":"سال دهم هجرت",
     "revelation_order":183.5},

    {"surah":"ممتحنه",
     "ranges":[(1,13)],
     "topic":"تمام سوره",
     "year":"سال دهم هجرت",
     "revelation_order":184},

    {"surah":"فاطر",
     "ranges":[(1,3),(9,9), (13, 13), (19, 19)],
     "topic":"آیات مدنی",
     "year":"سال دهم هجرت",
     "revelation_order":185},

    {"surah":"تحریم",
     "ranges":[(1,12)],
     "topic":"تمام سوره",
     "year":"سال دهم هجرت",
     "revelation_order":186},

    {"surah":"انعام",
     "ranges":[(135,154)],
     "topic":"جدال تشریعی",
     "year":"سال دهم هجرت",
     "revelation_order":187},

    {"surah":"طلاق",
     "ranges":[(1,7)],
     "topic":"تشریع طلاق",
     "year":"سال دهم هجرت",
     "revelation_order":188},
     {"surah":"نساء",
     "ranges":[(46,46), (175, 175), (126, 129), (3, 4), (6, 7), (12, 12), (13, 16), (29, 30)],
     "topic":"تشریعی و بعدی",
     "year":"سال دهم هجرت",
     "revelation_order":189},

    {"surah":"نور",
     "ranges":[(34,44), (57, 64)],
     "topic":"ایمانی و تشریعی بلند",
     "year":"سال دهم هجرت",
     "revelation_order":190},

    {"surah":"مائده",
     "ranges":[(15,22),(45,55)],
     "topic":"اهل کتاب",
     "year":"سال دهم هجرت",
     "revelation_order":191},

    {"surah":"بقره",
     "ranges":[(159,159),(244,244),(247,254), (256, 259)],
     "topic":"آیات بلند اهل کتاب و ایمانی",
     "year":"سال دهم هجرت",
     "revelation_order":192.0},
]


year11_hijri_table = [

    {"surah":"بقره",
     "ranges":[(260,262),(284,286)],
     "topic":"بقیه آیات بلند اهل کتاب و ایمانی",
     "year":"سال یازدهم هجرت",
     "revelation_order":192.5},

    {"surah":"احزاب",
     "ranges":[(53,55)],
     "topic":"تکمیلی و بعدی",
     "year":"سال یازدهم هجرت",
     "revelation_order":193},

    {"surah":"مائده",
     "ranges":[(1,9)],
     "topic":"تشریعی بلند",
     "year":"سال یازدهم هجرت",
     "revelation_order":194},
]

table = []
table.extend(year1_table)
table.extend(year2_table)
table.extend(year3_table)
table.extend(year4_table)
table.extend(year5_table)
table.extend(year6_table)
table.extend(year7_table)
table.extend(year8_table)
table.extend(year9_table)
table.extend(year10_table)
table.extend(year11_table)
table.extend(year12_table)
table.extend(year13_table)
table.extend(year2_hijri_table)
table.extend(year3_hijri_table)
table.extend(year4_hijri_table)
table.extend(year5_hijri_table)
table.extend(year6_hijri_table)
table.extend(year7_hijri_table)
table.extend(year8_hijri_table)
table.extend(year9_hijri_table)
table.extend(year10_hijri_table)
table.extend(year11_hijri_table)






# def validate_ranges(table):
#     surah_ayahs = defaultdict(list)
#     issues = []

#     # جمع‌آوری همه آیات هر سوره
#     for row in table:
#         surah = row["surah"]
#         order = row["revelation_order"]
#         for a, b in row["ranges"]:
#             for ayah in range(a, b + 1):
#                 surah_ayahs[surah].append((ayah, order))

#     # بررسی هر سوره
#     for surah, ayahs in surah_ayahs.items():
#         ayahs.sort()  # بر اساس شماره آیه

#         seen = {}
#         ayah_numbers = [a for a, _ in ayahs]

#         # 1️⃣ آیه تکراری
#         for a, order in ayahs:
#             if a in seen:
#                 issues.append(
#                     f"❌ تکرار آیه {a} در سوره «{surah}» "
#                     f"(ترتیب‌ها: {seen[a]} و {order})"
#                 )
#             else:
#                 seen[a] = order

#         # 2️⃣ شکاف (gap)
#         for prev, curr in zip(ayah_numbers, ayah_numbers[1:]):
#             if curr != prev + 1:
#                 issues.append(
#                     f"⚠️ شکاف بین آیه {prev} و {curr} در سوره «{surah}»"
#                 )

#     return issues


# issues = validate_ranges(table)

# if issues:
#     print("\n" + "="*60)
#     print("⚠️ گزارش اعتبارسنجی بازه‌های آیات")
#     print("="*60)
#     for i in issues:
#         print(i)
#     print("="*60)
# else:
#     print("✅ هیچ overlap یا gap غیرمنتظره‌ای پیدا نشد.")




def find_ayah_info(surah_name, ayah_number, table):
    for row in table:
        if row["surah"] != surah_name:
            continue
        for a, b in row["ranges"]:
            if a <= ayah_number <= b:
                return row
    return None


def print_ayah_info(surah, ayah, info):
    if info is None:
        print("یافت نشد")
        return

    matched = None
    for a, b in info["ranges"]:
        if a <= ayah <= b:
            matched = (a, b)
            break

    print(f"سوره: {surah}")
    print(f"آیه: {ayah}")
    print(f"گروه آیات نازل‌شده: {matched[0]} تا {matched[1]}")
    print(f"موضوع: {info['topic']}")
    print(f"سال نزول: {info['year']}")
    print(f"ترتیب نزول: {info['revelation_order']}")
    print(f"تعداد آیات این گروه: {info['ayah_count']}")
    print(f"تعداد کلمات این گروه: {info['word_count']}")
    print(f"جمع آیات تا این مرحله: {info['cumulative_ayahs']}")
    print(f"جمع کلمات تا این مرحله: {info['cumulative_words']}")


def find_multiple_ayahs(queries, table):
    results = []
    warnings = []

    for surah_input, ayah in queries:
        surah_name = resolve_surah_name(surah_input)

        if surah_name is None:
            warnings.append(f"⚠️ سوره «{surah_input}» معتبر نیست.")
            continue

        found = False

        for row in table:
            if row["surah"] != surah_name:
                continue

            for a, b in row["ranges"]:
                if a <= ayah <= b:
                    found = True
                    results.append({
                        "سوره": surah_name,
                        "آیه": ayah,
                        "گروه آیات": f"{a} تا {b}",
                        "موضوع": row["topic"],
                        "سال نزول": row["year"],
                        "ترتیب نزول": row["revelation_order"],
                    })
                    break
            if found:
                break

        if not found:
            warnings.append(
                f"⚠️ آیه {ayah} در سوره «{surah_name}» یافت نشد."
            )

    results.sort(key=lambda x: x["ترتیب نزول"])
    return results, warnings



def rtl(text):
    import arabic_reshaper
    from bidi.algorithm import get_display

    return get_display(arabic_reshaper.reshape(text))




def build_year_color_map(results):
    from matplotlib import cm

    years = list(dict.fromkeys(r["سال نزول"] for r in results))  # حفظ ترتیب
    cmap = cm.get_cmap("Pastel1", len(years))
    return {year: cmap(i) for i, year in enumerate(years)}


def show_results_figure_rtl(results, title="نتایج جستجو"):
    import matplotlib.pyplot as plt

    if not results:
        print("یافت نشد")
        return

    year_colors = build_year_color_map(results)

    columns = [rtl(col) for col in results[0].keys()]
    data = [[rtl(str(row[col])) for col in row.keys()] for row in results]

    fig, ax = plt.subplots(figsize=(len(columns)*2.4, len(data)*1.3))
    ax.axis("off")

    table = ax.table(
        cellText=data,
        colLabels=columns,
        cellLoc="center",
        loc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(13)
    table.scale(1.3, 1.7)

    # هدر
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#E6E6E6")

    # رنگ‌بندی ردیف‌ها بر اساس سال نزول
    for i, row_data in enumerate(results, start=1):
        color = year_colors[row_data["سال نزول"]]
        for j in range(len(columns)):
            table[(i, j)].set_facecolor(color)

    ax.set_title(rtl(title), fontsize=15, pad=20)
    plt.show()


# queries = [
#     (34, 20),
#     (96, 4),
#     (740, 6),
#     ("نساء", 552)
# ]

def load_quran_txt(path):
    quran = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            surah, ayah, text = line.split("|", 2)
            surah = int(surah)
            ayah = int(ayah)

            if surah not in quran:
                quran[surah] = {}

            quran[surah][ayah] = text

    return quran


QURAN_TEXT = load_quran_txt(Path(__file__).resolve().with_name("quran-simple.txt"))

# print(QURAN_TEXT[2][255])





# ARABIC_DIACRITICS = re.compile(
#     r"[\u064B-\u0652\u0670]"
# )

ARABIC_DIACRITICS = re.compile(
    r"[\u0610-\u061A\u064B-\u0652\u0670\u06D6-\u06ED]"
)


def remove_diacritics(text):
    return re.sub(ARABIC_DIACRITICS, "", text)


def normalize_arabic(text):
    text = remove_diacritics(text)

    return (
        text
        .replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
        .replace("ٱ", "ا")
        .replace("ك", "ک")   # 🔑 خیلی مهم
        .replace("ي", "ی")   # 🔑
        .replace("ة", "ه")
        .replace("ى", "ی")
        .replace("ؤ", "و")
        .replace("ئ", "ی")
        .replace("ء", "")
        .replace("ـ", "")
        .replace("لَا", "لا")
    )




def find_verses_containing(word, quran_text):
    word_n = normalize_arabic(word)
    results = []

    for surah_no, ayahs in quran_text.items():
        for ayah_no, text in ayahs.items():
            text_n = normalize_arabic(text)
            if word_n in text_n:
                results.append((surah_no, ayah_no))

    return results



# print(find_verses_containing("بسم", QURAN_TEXT))
# print(len(find_verses_containing("کافر", QURAN_TEXT)))
# print(find_verses_containing("الانسان", QURAN_TEXT))


# queries = find_verses_containing("انسان", QURAN_TEXT)
# print(len(queries))

# queries = find_verses_containing("کفر", QURAN_TEXT)
# results, warnings = find_multiple_ayahs(queries, table)

# print(warnings)

# show_results_figure_rtl(
#     results,
#     title="آیات شامل کلمه «انسان» به ترتیب نزول"
# )


# results, warnings = find_multiple_ayahs(queries, table)

# if warnings:
#     print("\n" + "="*60)
#     for w in warnings:
#         print(w)
#     print("="*60 + "\n")

# show_results_figure_rtl(results, title="نمونه جستجوی چندآیه‌ای")


def show_results_paginated(results, title, rows_per_page=20):
    total = len(results)
    pages = (total + rows_per_page - 1) // rows_per_page

    for p in range(pages):
        start = p * rows_per_page
        end = min(start + rows_per_page, total)
        page_results = results[start:end]

        show_results_figure_rtl(
            page_results,
            title=f"{title} (صفحه {p+1} از {pages})"
        )

# print(len(results))

# show_results_paginated(
#     results,
#     title="آیات شامل کلمه «انسان» به ترتیب نزول",
#     rows_per_page=10
# )




def find_verses_multi(words, quran_text, mode="OR"):
    """
    words: لیست کلمات (مثلاً ["انسان", "ناس"])
    mode:
        OR     → حداقل یکی باشد
        AND    → همه باشند
        PHRASE → دقیقاً به همان ترتیب و کنار هم
    """
    if mode not in {"OR", "AND", "PHRASE"}:
        raise ValueError("mode باید OR یا AND یا PHRASE باشد")

    words_n = [normalize_arabic(w.strip()) for w in words if w.strip()]
    if not words_n:
        return []
    results = []

    for surah_no, ayahs in quran_text.items():
        for ayah_no, text in ayahs.items():
            text_n = normalize_arabic(text)

            if mode == "OR":
                if any(w in text_n for w in words_n):
                    results.append((surah_no, ayah_no))

            elif mode == "AND":
                if all(w in text_n for w in words_n):
                    results.append((surah_no, ayah_no))

            elif mode == "PHRASE":
                phrase = " ".join(words_n)
                if phrase in text_n:
                    results.append((surah_no, ayah_no))

    return results


# queries = find_verses_multi(
#     ["انسان", "ناس"],
#     QURAN_TEXT,
#     mode="OR"
# )

# queries = find_verses_multi(
#     ["انسان", "ناس"],
#     QURAN_TEXT,
#     mode="AND"
# )


# results, warnings = find_multiple_ayahs(queries, table)
# show_results_paginated(
#     results,
#     title="آیات شامل «انسان یا ناس» به ترتیب نزول",
#     rows_per_page=10
# )
