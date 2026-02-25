import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
MINI_APP_URL = os.environ.get("MINI_APP_URL", "https://techkkabir-hub.github.io/NCERT-QUIZ")

# Per-user state: subject, score, streak, seen questions (no-repeat system)
user_states = {}

QUESTIONS = [
  {
    "subject": "history",
    "q_hi": "सिंधु घाटी सभ्यता की खोज किसने की?",
    "q_en": "Who discovered the Indus Valley Civilization?",
    "options": [
      {
        "letter": "A",
        "hi": "जॉन मार्शल",
        "en": "John Marshall"
      },
      {
        "letter": "B",
        "hi": "दयाराम साहनी",
        "en": "Dayaram Sahni"
      },
      {
        "letter": "C",
        "hi": "आर.डी. बनर्जी",
        "en": "R.D. Banerjee"
      },
      {
        "letter": "D",
        "hi": "मोर्टिमर व्हीलर",
        "en": "Mortimer Wheeler"
      }
    ],
    "correct": "B",
    "exp_hi": "हड़प्पा की खोज 1921 में दयाराम साहनी ने की।",
    "exp_en": "Harappa was discovered by Dayaram Sahni in 1921.",
    "exam_tag": "UPSC 2018",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "सिंधु घाटी का सबसे बड़ा नगर कौन था?",
    "q_en": "Largest city of Indus Valley Civilization?",
    "options": [
      {
        "letter": "A",
        "hi": "हड़प्पा",
        "en": "Harappa"
      },
      {
        "letter": "B",
        "hi": "मोहनजोदड़ो",
        "en": "Mohenjo-daro"
      },
      {
        "letter": "C",
        "hi": "लोथल",
        "en": "Lothal"
      },
      {
        "letter": "D",
        "hi": "कालीबंगन",
        "en": "Kalibangan"
      }
    ],
    "correct": "B",
    "exp_hi": "मोहनजोदड़ो सिंधु घाटी का सबसे बड़ा नगर था।",
    "exp_en": "Mohenjo-daro was the largest city.",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "ऋग्वेद में कितने मंडल हैं?",
    "q_en": "How many mandalas in Rigveda?",
    "options": [
      {
        "letter": "A",
        "hi": "8",
        "en": "8"
      },
      {
        "letter": "B",
        "hi": "10",
        "en": "10"
      },
      {
        "letter": "C",
        "hi": "12",
        "en": "12"
      },
      {
        "letter": "D",
        "hi": "6",
        "en": "6"
      }
    ],
    "correct": "B",
    "exp_hi": "ऋग्वेद में 10 मंडल और 1028 सूक्त हैं।",
    "exp_en": "Rigveda has 10 mandalas and 1028 hymns.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "महावीर का जन्म कहाँ हुआ?",
    "q_en": "Where was Mahavira born?",
    "options": [
      {
        "letter": "A",
        "hi": "वैशाली",
        "en": "Vaishali"
      },
      {
        "letter": "B",
        "hi": "पाटलिपुत्र",
        "en": "Pataliputra"
      },
      {
        "letter": "C",
        "hi": "कपिलवस्तु",
        "en": "Kapilavastu"
      },
      {
        "letter": "D",
        "hi": "राजगृह",
        "en": "Rajagriha"
      }
    ],
    "correct": "A",
    "exp_hi": "महावीर का जन्म 599 ईसा पूर्व वैशाली में हुआ।",
    "exp_en": "Mahavira was born in Vaishali in 599 BCE.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "बुद्ध को ज्ञान कहाँ मिला?",
    "q_en": "Where did Buddha attain enlightenment?",
    "options": [
      {
        "letter": "A",
        "hi": "सारनाथ",
        "en": "Sarnath"
      },
      {
        "letter": "B",
        "hi": "बोधगया",
        "en": "Bodh Gaya"
      },
      {
        "letter": "C",
        "hi": "कुशीनगर",
        "en": "Kushinagar"
      },
      {
        "letter": "D",
        "hi": "लुंबिनी",
        "en": "Lumbini"
      }
    ],
    "correct": "B",
    "exp_hi": "बुद्ध को बोधगया में बोधि वृक्ष के नीचे ज्ञान मिला।",
    "exp_en": "Buddha attained enlightenment under Bodhi tree in Bodh Gaya.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "जैन धर्म के 24वें तीर्थंकर कौन थे?",
    "q_en": "Who was 24th Tirthankara of Jainism?",
    "options": [
      {
        "letter": "A",
        "hi": "ऋषभदेव",
        "en": "Rishabhdeva"
      },
      {
        "letter": "B",
        "hi": "पार्श्वनाथ",
        "en": "Parshvanatha"
      },
      {
        "letter": "C",
        "hi": "महावीर",
        "en": "Mahavira"
      },
      {
        "letter": "D",
        "hi": "नेमिनाथ",
        "en": "Neminatha"
      }
    ],
    "correct": "C",
    "exp_hi": "महावीर जैन धर्म के 24वें और अंतिम तीर्थंकर थे।",
    "exp_en": "Mahavira was the 24th and last Tirthankara of Jainism.",
    "exam_tag": "CTET 2019",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "सिंधु घाटी के लोग किस धातु से अपरिचित थे?",
    "q_en": "Which metal was unknown to Indus Valley people?",
    "options": [
      {
        "letter": "A",
        "hi": "तांबा",
        "en": "Copper"
      },
      {
        "letter": "B",
        "hi": "कांसा",
        "en": "Bronze"
      },
      {
        "letter": "C",
        "hi": "लोहा",
        "en": "Iron"
      },
      {
        "letter": "D",
        "hi": "सोना",
        "en": "Gold"
      }
    ],
    "correct": "C",
    "exp_hi": "सिंधु घाटी के लोग लोहे से अपरिचित थे।",
    "exp_en": "Indus Valley people were not familiar with iron.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "सिंधु घाटी सभ्यता किस युग से संबंधित है?",
    "q_en": "Indus Valley belongs to which age?",
    "options": [
      {
        "letter": "A",
        "hi": "पाषाण युग",
        "en": "Stone Age"
      },
      {
        "letter": "B",
        "hi": "कांस्य युग",
        "en": "Bronze Age"
      },
      {
        "letter": "C",
        "hi": "लौह युग",
        "en": "Iron Age"
      },
      {
        "letter": "D",
        "hi": "ताम्र युग",
        "en": "Copper Age"
      }
    ],
    "correct": "B",
    "exp_hi": "सिंधु घाटी सभ्यता कांस्य युग से संबंधित है।",
    "exp_en": "Indus Valley belongs to the Bronze Age.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "मोहनजोदड़ो का अर्थ क्या है?",
    "q_en": "What does Mohenjo-daro mean?",
    "options": [
      {
        "letter": "A",
        "hi": "महान नगर",
        "en": "Great city"
      },
      {
        "letter": "B",
        "hi": "मृतकों का टीला",
        "en": "Mound of the dead"
      },
      {
        "letter": "C",
        "hi": "नदी किनारा",
        "en": "Riverbank"
      },
      {
        "letter": "D",
        "hi": "पवित्र स्थान",
        "en": "Holy place"
      }
    ],
    "correct": "B",
    "exp_hi": "मोहनजोदड़ो का अर्थ है 'मृतकों का टीला'।",
    "exp_en": "Mohenjo-daro means 'Mound of the dead'.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "सिंधु सभ्यता का बंदरगाह नगर कौन था?",
    "q_en": "Port city of Indus civilization?",
    "options": [
      {
        "letter": "A",
        "hi": "हड़प्पा",
        "en": "Harappa"
      },
      {
        "letter": "B",
        "hi": "लोथल",
        "en": "Lothal"
      },
      {
        "letter": "C",
        "hi": "मोहनजोदड़ो",
        "en": "Mohenjo-daro"
      },
      {
        "letter": "D",
        "hi": "कालीबंगन",
        "en": "Kalibangan"
      }
    ],
    "correct": "B",
    "exp_hi": "लोथल सिंधु सभ्यता का प्रमुख बंदरगाह नगर था।",
    "exp_en": "Lothal was the major port city of Indus civilization.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "आर्यों की मूल भाषा क्या थी?",
    "q_en": "Original language of Aryans?",
    "options": [
      {
        "letter": "A",
        "hi": "पाली",
        "en": "Pali"
      },
      {
        "letter": "B",
        "hi": "प्राकृत",
        "en": "Prakrit"
      },
      {
        "letter": "C",
        "hi": "संस्कृत",
        "en": "Sanskrit"
      },
      {
        "letter": "D",
        "hi": "अपभ्रंश",
        "en": "Apabhramsha"
      }
    ],
    "correct": "C",
    "exp_hi": "आर्यों की मूल भाषा संस्कृत थी।",
    "exp_en": "Sanskrit was the original language of Aryans.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "वेदों की संख्या कितनी है?",
    "q_en": "How many Vedas are there?",
    "options": [
      {
        "letter": "A",
        "hi": "2",
        "en": "2"
      },
      {
        "letter": "B",
        "hi": "3",
        "en": "3"
      },
      {
        "letter": "C",
        "hi": "4",
        "en": "4"
      },
      {
        "letter": "D",
        "hi": "5",
        "en": "5"
      }
    ],
    "correct": "C",
    "exp_hi": "वेदों की संख्या 4 है - ऋग्वेद, सामवेद, यजुर्वेद, अथर्ववेद।",
    "exp_en": "There are 4 Vedas - Rigveda, Samaveda, Yajurveda, Atharvaveda.",
    "exam_tag": "CTET 2021",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "बौद्ध धर्म की स्थापना किसने की?",
    "q_en": "Who founded Buddhism?",
    "options": [
      {
        "letter": "A",
        "hi": "महावीर",
        "en": "Mahavira"
      },
      {
        "letter": "B",
        "hi": "गौतम बुद्ध",
        "en": "Gautam Buddha"
      },
      {
        "letter": "C",
        "hi": "शंकराचार्य",
        "en": "Shankaracharya"
      },
      {
        "letter": "D",
        "hi": "चाणक्य",
        "en": "Chanakya"
      }
    ],
    "correct": "B",
    "exp_hi": "गौतम बुद्ध ने बौद्ध धर्म की स्थापना की।",
    "exp_en": "Gautam Buddha founded Buddhism.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "बुद्ध का पहला उपदेश कहाँ दिया?",
    "q_en": "Where did Buddha give first sermon?",
    "options": [
      {
        "letter": "A",
        "hi": "बोधगया",
        "en": "Bodh Gaya"
      },
      {
        "letter": "B",
        "hi": "सारनाथ",
        "en": "Sarnath"
      },
      {
        "letter": "C",
        "hi": "लुंबिनी",
        "en": "Lumbini"
      },
      {
        "letter": "D",
        "hi": "कुशीनगर",
        "en": "Kushinagar"
      }
    ],
    "correct": "B",
    "exp_hi": "बुद्ध ने पहला उपदेश सारनाथ में दिया जिसे धम्मचक्कपवत्तन कहते हैं।",
    "exp_en": "Buddha gave first sermon at Sarnath called Dhammachakkapavattana.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "बुद्ध का जन्म कहाँ हुआ था?",
    "q_en": "Where was Buddha born?",
    "options": [
      {
        "letter": "A",
        "hi": "बोधगया",
        "en": "Bodh Gaya"
      },
      {
        "letter": "B",
        "hi": "सारनाथ",
        "en": "Sarnath"
      },
      {
        "letter": "C",
        "hi": "लुंबिनी",
        "en": "Lumbini"
      },
      {
        "letter": "D",
        "hi": "कुशीनगर",
        "en": "Kushinagar"
      }
    ],
    "correct": "C",
    "exp_hi": "बुद्ध का जन्म लुंबिनी (नेपाल) में हुआ था।",
    "exp_en": "Buddha was born in Lumbini (Nepal).",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "चंद्रगुप्त मौर्य का प्रधानमंत्री कौन था?",
    "q_en": "PM of Chandragupta Maurya?",
    "options": [
      {
        "letter": "A",
        "hi": "बिंदुसार",
        "en": "Bindusara"
      },
      {
        "letter": "B",
        "hi": "चाणक्य",
        "en": "Chanakya"
      },
      {
        "letter": "C",
        "hi": "अशोक",
        "en": "Ashoka"
      },
      {
        "letter": "D",
        "hi": "सेल्यूकस",
        "en": "Seleucus"
      }
    ],
    "correct": "B",
    "exp_hi": "चाणक्य (कौटिल्य) चंद्रगुप्त मौर्य के प्रधानमंत्री थे।",
    "exp_en": "Chanakya (Kautilya) was PM of Chandragupta Maurya.",
    "exam_tag": "SSC 2018",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "अशोक के अभिलेख किस लिपि में हैं?",
    "q_en": "Script of Ashoka's inscriptions?",
    "options": [
      {
        "letter": "A",
        "hi": "देवनागरी",
        "en": "Devanagari"
      },
      {
        "letter": "B",
        "hi": "ब्राह्मी",
        "en": "Brahmi"
      },
      {
        "letter": "C",
        "hi": "खरोष्ठी",
        "en": "Kharosthi"
      },
      {
        "letter": "D",
        "hi": "संस्कृत",
        "en": "Sanskrit"
      }
    ],
    "correct": "B",
    "exp_hi": "अशोक के अभिलेख ब्राह्मी लिपि में हैं।",
    "exp_en": "Ashoka's inscriptions are in Brahmi script.",
    "exam_tag": "UPSC 2019",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "गुप्त वंश की स्थापना किसने की?",
    "q_en": "Who founded Gupta dynasty?",
    "options": [
      {
        "letter": "A",
        "hi": "चंद्रगुप्त प्रथम",
        "en": "Chandragupta I"
      },
      {
        "letter": "B",
        "hi": "श्रीगुप्त",
        "en": "Sri Gupta"
      },
      {
        "letter": "C",
        "hi": "समुद्रगुप्त",
        "en": "Samudragupta"
      },
      {
        "letter": "D",
        "hi": "चंद्रगुप्त द्वितीय",
        "en": "Chandragupta II"
      }
    ],
    "correct": "B",
    "exp_hi": "गुप्त वंश की स्थापना श्रीगुप्त ने की।",
    "exp_en": "Gupta dynasty was founded by Sri Gupta.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "समुद्रगुप्त को क्या कहते हैं?",
    "q_en": "What is Samudragupta called?",
    "options": [
      {
        "letter": "A",
        "hi": "भारत का नेपोलियन",
        "en": "Napoleon of India"
      },
      {
        "letter": "B",
        "hi": "भारत का अकबर",
        "en": "Akbar of India"
      },
      {
        "letter": "C",
        "hi": "महान शासक",
        "en": "Great ruler"
      },
      {
        "letter": "D",
        "hi": "विजेता",
        "en": "Conqueror"
      }
    ],
    "correct": "A",
    "exp_hi": "समुद्रगुप्त को भारत का नेपोलियन कहते हैं।",
    "exp_en": "Samudragupta is called Napoleon of India.",
    "exam_tag": "CTET 2020",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "हर्षवर्धन की राजधानी कहाँ थी?",
    "q_en": "Capital of Harshavardhana?",
    "options": [
      {
        "letter": "A",
        "hi": "पाटलिपुत्र",
        "en": "Pataliputra"
      },
      {
        "letter": "B",
        "hi": "कन्नौज",
        "en": "Kannauj"
      },
      {
        "letter": "C",
        "hi": "थानेश्वर",
        "en": "Thaneshwar"
      },
      {
        "letter": "D",
        "hi": "उज्जैन",
        "en": "Ujjain"
      }
    ],
    "correct": "B",
    "exp_hi": "हर्षवर्धन की राजधानी कन्नौज थी।",
    "exp_en": "Kannauj was capital of Harshavardhana.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "अकबर का दरबारी संगीतकार कौन था?",
    "q_en": "Court musician of Akbar?",
    "options": [
      {
        "letter": "A",
        "hi": "तानसेन",
        "en": "Tansen"
      },
      {
        "letter": "B",
        "hi": "बैजू बावरा",
        "en": "Baiju Bawra"
      },
      {
        "letter": "C",
        "hi": "अमीर खुसरो",
        "en": "Amir Khusro"
      },
      {
        "letter": "D",
        "hi": "बीरबल",
        "en": "Birbal"
      }
    ],
    "correct": "A",
    "exp_hi": "तानसेन अकबर के नवरत्नों में से एक थे।",
    "exp_en": "Tansen was one of the nine gems of Akbar.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "चालुक्य वंश की स्थापना किसने की?",
    "q_en": "Who founded Chalukya dynasty?",
    "options": [
      {
        "letter": "A",
        "hi": "पुलकेशी प्रथम",
        "en": "Pulakesi I"
      },
      {
        "letter": "B",
        "hi": "विक्रमादित्य",
        "en": "Vikramaditya"
      },
      {
        "letter": "C",
        "hi": "कीर्तिवर्मन",
        "en": "Kirtivarman"
      },
      {
        "letter": "D",
        "hi": "मंगलेश",
        "en": "Mangalesh"
      }
    ],
    "correct": "A",
    "exp_hi": "चालुक्य वंश की स्थापना पुलकेशी प्रथम ने की।",
    "exp_en": "Chalukya dynasty was founded by Pulakesi I.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "दिल्ली सल्तनत की स्थापना कब हुई?",
    "q_en": "When was Delhi Sultanate established?",
    "options": [
      {
        "letter": "A",
        "hi": "1192",
        "en": "1192"
      },
      {
        "letter": "B",
        "hi": "1206",
        "en": "1206"
      },
      {
        "letter": "C",
        "hi": "1210",
        "en": "1210"
      },
      {
        "letter": "D",
        "hi": "1290",
        "en": "1290"
      }
    ],
    "correct": "B",
    "exp_hi": "दिल्ली सल्तनत की स्थापना 1206 में कुतुबुद्दीन ऐबक ने की।",
    "exp_en": "Delhi Sultanate was established in 1206 by Qutbuddin Aibak.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "कुतुब मीनार किसने बनवाई?",
    "q_en": "Who built Qutub Minar?",
    "options": [
      {
        "letter": "A",
        "hi": "अकबर",
        "en": "Akbar"
      },
      {
        "letter": "B",
        "hi": "कुतुबुद्दीन ऐबक",
        "en": "Qutbuddin Aibak"
      },
      {
        "letter": "C",
        "hi": "इल्तुतमिश",
        "en": "Iltutmish"
      },
      {
        "letter": "D",
        "hi": "बलबन",
        "en": "Balban"
      }
    ],
    "correct": "B",
    "exp_hi": "कुतुब मीनार की नींव कुतुबुद्दीन ऐबक ने रखी।",
    "exp_en": "Qutub Minar was started by Qutbuddin Aibak.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "विजयनगर साम्राज्य की स्थापना किसने की?",
    "q_en": "Who founded Vijayanagara Empire?",
    "options": [
      {
        "letter": "A",
        "hi": "हरिहर और बुक्का",
        "en": "Harihara and Bukka"
      },
      {
        "letter": "B",
        "hi": "कृष्णदेवराय",
        "en": "Krishnadevaraya"
      },
      {
        "letter": "C",
        "hi": "देवराय प्रथम",
        "en": "Devaraya I"
      },
      {
        "letter": "D",
        "hi": "विरूपाक्ष",
        "en": "Virupaksha"
      }
    ],
    "correct": "A",
    "exp_hi": "विजयनगर साम्राज्य की स्थापना 1336 में हरिहर और बुक्का ने की।",
    "exp_en": "Vijayanagara Empire was founded by Harihara and Bukka in 1336.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "पल्लव वंश की राजधानी कहाँ थी?",
    "q_en": "Capital of Pallava dynasty?",
    "options": [
      {
        "letter": "A",
        "hi": "कांचीपुरम",
        "en": "Kanchipuram"
      },
      {
        "letter": "B",
        "hi": "मदुरै",
        "en": "Madurai"
      },
      {
        "letter": "C",
        "hi": "तंजावुर",
        "en": "Thanjavur"
      },
      {
        "letter": "D",
        "hi": "महाबलिपुरम",
        "en": "Mahabalipuram"
      }
    ],
    "correct": "A",
    "exp_hi": "पल्लव वंश की राजधानी कांचीपुरम थी।",
    "exp_en": "Kanchipuram was the capital of Pallava dynasty.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "राष्ट्रकूट वंश का सबसे महान शासक कौन था?",
    "q_en": "Greatest ruler of Rashtrakuta dynasty?",
    "options": [
      {
        "letter": "A",
        "hi": "दन्तिदुर्ग",
        "en": "Dantidurga"
      },
      {
        "letter": "B",
        "hi": "अमोघवर्ष",
        "en": "Amoghavarsha"
      },
      {
        "letter": "C",
        "hi": "ध्रुव",
        "en": "Dhruva"
      },
      {
        "letter": "D",
        "hi": "गोविंद तृतीय",
        "en": "Govinda III"
      }
    ],
    "correct": "B",
    "exp_hi": "अमोघवर्ष राष्ट्रकूट वंश का महान शासक और विद्वान था।",
    "exp_en": "Amoghavarsha was the great ruler and scholar of Rashtrakuta dynasty.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "पाल वंश की स्थापना किसने की?",
    "q_en": "Who founded Pala dynasty?",
    "options": [
      {
        "letter": "A",
        "hi": "धर्मपाल",
        "en": "Dharmapala"
      },
      {
        "letter": "B",
        "hi": "गोपाल",
        "en": "Gopala"
      },
      {
        "letter": "C",
        "hi": "देवपाल",
        "en": "Devapala"
      },
      {
        "letter": "D",
        "hi": "महिपाल",
        "en": "Mahipala"
      }
    ],
    "correct": "B",
    "exp_hi": "पाल वंश की स्थापना गोपाल ने की।",
    "exp_en": "Pala dynasty was founded by Gopala.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "खजुराहो मंदिर किस वंश ने बनवाया?",
    "q_en": "Which dynasty built Khajuraho temples?",
    "options": [
      {
        "letter": "A",
        "hi": "गुप्त",
        "en": "Gupta"
      },
      {
        "letter": "B",
        "hi": "चंदेल",
        "en": "Chandela"
      },
      {
        "letter": "C",
        "hi": "परमार",
        "en": "Paramara"
      },
      {
        "letter": "D",
        "hi": "चालुक्य",
        "en": "Chalukya"
      }
    ],
    "correct": "B",
    "exp_hi": "खजुराहो मंदिर चंदेल वंश ने बनवाए।",
    "exp_en": "Khajuraho temples were built by the Chandela dynasty.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "अलबेरूनी कब भारत आया?",
    "q_en": "When did Alberuni come to India?",
    "options": [
      {
        "letter": "A",
        "hi": "महमूद गजनी के साथ",
        "en": "With Mahmud of Ghazni"
      },
      {
        "letter": "B",
        "hi": "मुहम्मद गोरी के साथ",
        "en": "With Muhammad Ghori"
      },
      {
        "letter": "C",
        "hi": "बाबर के साथ",
        "en": "With Babur"
      },
      {
        "letter": "D",
        "hi": "तैमूर के साथ",
        "en": "With Timur"
      }
    ],
    "correct": "A",
    "exp_hi": "अलबेरूनी महमूद गजनी के साथ भारत आया।",
    "exp_en": "Alberuni came to India with Mahmud of Ghazni.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "पानीपत की पहली लड़ाई कब हुई?",
    "q_en": "When was First Battle of Panipat?",
    "options": [
      {
        "letter": "A",
        "hi": "1526",
        "en": "1526"
      },
      {
        "letter": "B",
        "hi": "1556",
        "en": "1556"
      },
      {
        "letter": "C",
        "hi": "1761",
        "en": "1761"
      },
      {
        "letter": "D",
        "hi": "1600",
        "en": "1600"
      }
    ],
    "correct": "A",
    "exp_hi": "पहली पानीपत की लड़ाई 1526 में बाबर और इब्राहिम लोदी के बीच हुई।",
    "exp_en": "First Battle of Panipat was in 1526 between Babur and Ibrahim Lodi.",
    "exam_tag": "UPSC 2017",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "ताजमहल किसने बनवाया?",
    "q_en": "Who built Taj Mahal?",
    "options": [
      {
        "letter": "A",
        "hi": "अकबर",
        "en": "Akbar"
      },
      {
        "letter": "B",
        "hi": "जहाँगीर",
        "en": "Jahangir"
      },
      {
        "letter": "C",
        "hi": "शाहजहाँ",
        "en": "Shah Jahan"
      },
      {
        "letter": "D",
        "hi": "औरंगजेब",
        "en": "Aurangzeb"
      }
    ],
    "correct": "C",
    "exp_hi": "ताजमहल शाहजहाँ ने 1632-53 में बनवाया।",
    "exp_en": "Taj Mahal was built by Shah Jahan in 1632-53.",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "शिवाजी का जन्म कब हुआ?",
    "q_en": "When was Shivaji born?",
    "options": [
      {
        "letter": "A",
        "hi": "1627",
        "en": "1627"
      },
      {
        "letter": "B",
        "hi": "1630",
        "en": "1630"
      },
      {
        "letter": "C",
        "hi": "1640",
        "en": "1640"
      },
      {
        "letter": "D",
        "hi": "1656",
        "en": "1656"
      }
    ],
    "correct": "B",
    "exp_hi": "शिवाजी का जन्म 19 फरवरी 1630 को हुआ।",
    "exp_en": "Shivaji was born on 19 February 1630.",
    "exam_tag": "Railway 2018",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "1857 की क्रांति का तात्कालिक कारण?",
    "q_en": "Immediate cause of 1857 revolt?",
    "options": [
      {
        "letter": "A",
        "hi": "भारी कर",
        "en": "Heavy taxation"
      },
      {
        "letter": "B",
        "hi": "चर्बी वाले कारतूस",
        "en": "Greased cartridges"
      },
      {
        "letter": "C",
        "hi": "अंग्रेजी शिक्षा",
        "en": "English education"
      },
      {
        "letter": "D",
        "hi": "डलहौजी की नीति",
        "en": "Dalhousie policy"
      }
    ],
    "correct": "B",
    "exp_hi": "चर्बी लगे कारतूस ने 1857 की क्रांति को जन्म दिया।",
    "exp_en": "Greased cartridges triggered 1857 revolt.",
    "exam_tag": "UPSC 2016",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "पानीपत की दूसरी लड़ाई कब हुई?",
    "q_en": "When was Second Battle of Panipat?",
    "options": [
      {
        "letter": "A",
        "hi": "1526",
        "en": "1526"
      },
      {
        "letter": "B",
        "hi": "1556",
        "en": "1556"
      },
      {
        "letter": "C",
        "hi": "1761",
        "en": "1761"
      },
      {
        "letter": "D",
        "hi": "1600",
        "en": "1600"
      }
    ],
    "correct": "B",
    "exp_hi": "पानीपत की दूसरी लड़ाई 1556 में अकबर और हेमू के बीच हुई।",
    "exp_en": "Second Battle of Panipat was in 1556 between Akbar and Hemu.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "अकबर का जन्म कब हुआ?",
    "q_en": "When was Akbar born?",
    "options": [
      {
        "letter": "A",
        "hi": "1542",
        "en": "1542"
      },
      {
        "letter": "B",
        "hi": "1556",
        "en": "1556"
      },
      {
        "letter": "C",
        "hi": "1530",
        "en": "1530"
      },
      {
        "letter": "D",
        "hi": "1605",
        "en": "1605"
      }
    ],
    "correct": "A",
    "exp_hi": "अकबर का जन्म 1542 में हुआ।",
    "exp_en": "Akbar was born in 1542.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "औरंगजेब का मकबरा कहाँ है?",
    "q_en": "Where is Aurangzeb's tomb?",
    "options": [
      {
        "letter": "A",
        "hi": "आगरा",
        "en": "Agra"
      },
      {
        "letter": "B",
        "hi": "दिल्ली",
        "en": "Delhi"
      },
      {
        "letter": "C",
        "hi": "खुल्दाबाद",
        "en": "Khuldabad"
      },
      {
        "letter": "D",
        "hi": "लाहौर",
        "en": "Lahore"
      }
    ],
    "correct": "C",
    "exp_hi": "औरंगजेब का मकबरा खुल्दाबाद (महाराष्ट्र) में है।",
    "exp_en": "Aurangzeb's tomb is at Khuldabad (Maharashtra).",
    "exam_tag": "UPSC 2015",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "मुगल साम्राज्य का संस्थापक कौन था?",
    "q_en": "Who founded the Mughal Empire?",
    "options": [
      {
        "letter": "A",
        "hi": "हुमायूँ",
        "en": "Humayun"
      },
      {
        "letter": "B",
        "hi": "बाबर",
        "en": "Babur"
      },
      {
        "letter": "C",
        "hi": "अकबर",
        "en": "Akbar"
      },
      {
        "letter": "D",
        "hi": "तैमूर",
        "en": "Timur"
      }
    ],
    "correct": "B",
    "exp_hi": "बाबर ने 1526 में मुगल साम्राज्य की स्थापना की।",
    "exp_en": "Babur founded the Mughal Empire in 1526.",
    "exam_tag": "CTET 2021",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "ईस्ट इंडिया कंपनी को व्यापार का अधिकार कब मिला?",
    "q_en": "When did East India Company get trading rights?",
    "options": [
      {
        "letter": "A",
        "hi": "1600",
        "en": "1600"
      },
      {
        "letter": "B",
        "hi": "1608",
        "en": "1608"
      },
      {
        "letter": "C",
        "hi": "1612",
        "en": "1612"
      },
      {
        "letter": "D",
        "hi": "1620",
        "en": "1620"
      }
    ],
    "correct": "A",
    "exp_hi": "ईस्ट इंडिया कंपनी को 1600 में रानी एलिजाबेथ ने व्यापार का अधिकार दिया।",
    "exp_en": "East India Company got trading rights from Queen Elizabeth in 1600.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "पानीपत की तीसरी लड़ाई कब हुई?",
    "q_en": "When was Third Battle of Panipat?",
    "options": [
      {
        "letter": "A",
        "hi": "1526",
        "en": "1526"
      },
      {
        "letter": "B",
        "hi": "1556",
        "en": "1556"
      },
      {
        "letter": "C",
        "hi": "1761",
        "en": "1761"
      },
      {
        "letter": "D",
        "hi": "1799",
        "en": "1799"
      }
    ],
    "correct": "C",
    "exp_hi": "पानीपत की तीसरी लड़ाई 1761 में मराठों और अहमद शाह अब्दाली के बीच हुई।",
    "exp_en": "Third Battle of Panipat was in 1761 between Marathas and Ahmad Shah Abdali.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "टीपू सुल्तान की मृत्यु कब हुई?",
    "q_en": "When did Tipu Sultan die?",
    "options": [
      {
        "letter": "A",
        "hi": "1792",
        "en": "1792"
      },
      {
        "letter": "B",
        "hi": "1795",
        "en": "1795"
      },
      {
        "letter": "C",
        "hi": "1799",
        "en": "1799"
      },
      {
        "letter": "D",
        "hi": "1803",
        "en": "1803"
      }
    ],
    "correct": "C",
    "exp_hi": "टीपू सुल्तान 1799 में श्रीरंगपट्टनम की लड़ाई में मारे गए।",
    "exp_en": "Tipu Sultan died in the Battle of Seringapatam in 1799.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "हुमायूँ का मकबरा कहाँ है?",
    "q_en": "Where is Humayun's tomb?",
    "options": [
      {
        "letter": "A",
        "hi": "आगरा",
        "en": "Agra"
      },
      {
        "letter": "B",
        "hi": "दिल्ली",
        "en": "Delhi"
      },
      {
        "letter": "C",
        "hi": "लाहौर",
        "en": "Lahore"
      },
      {
        "letter": "D",
        "hi": "फतेहपुर सीकरी",
        "en": "Fatehpur Sikri"
      }
    ],
    "correct": "B",
    "exp_hi": "हुमायूँ का मकबरा दिल्ली में है।",
    "exp_en": "Humayun's tomb is in Delhi.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "अकबर ने दीन-ए-इलाही कब शुरू किया?",
    "q_en": "When did Akbar start Din-i-Ilahi?",
    "options": [
      {
        "letter": "A",
        "hi": "1575",
        "en": "1575"
      },
      {
        "letter": "B",
        "hi": "1582",
        "en": "1582"
      },
      {
        "letter": "C",
        "hi": "1590",
        "en": "1590"
      },
      {
        "letter": "D",
        "hi": "1600",
        "en": "1600"
      }
    ],
    "correct": "B",
    "exp_hi": "अकबर ने 1582 में दीन-ए-इलाही धर्म शुरू किया।",
    "exp_en": "Akbar started Din-i-Ilahi religion in 1582.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "शेरशाह सूरी ने कौन सा मार्ग बनवाया?",
    "q_en": "Which road did Sher Shah Suri build?",
    "options": [
      {
        "letter": "A",
        "hi": "जीटी रोड",
        "en": "GT Road"
      },
      {
        "letter": "B",
        "hi": "रेशम मार्ग",
        "en": "Silk Route"
      },
      {
        "letter": "C",
        "hi": "मसाला मार्ग",
        "en": "Spice Route"
      },
      {
        "letter": "D",
        "hi": "शाही मार्ग",
        "en": "Royal Road"
      }
    ],
    "correct": "A",
    "exp_hi": "शेरशाह सूरी ने ग्रांड ट्रंक (जीटी) रोड बनवाया।",
    "exp_en": "Sher Shah Suri built the Grand Trunk (GT) Road.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "बाबरनामा किसने लिखा?",
    "q_en": "Who wrote Baburnama?",
    "options": [
      {
        "letter": "A",
        "hi": "अबुल फजल",
        "en": "Abul Fazl"
      },
      {
        "letter": "B",
        "hi": "बाबर",
        "en": "Babur"
      },
      {
        "letter": "C",
        "hi": "हुमायूँ",
        "en": "Humayun"
      },
      {
        "letter": "D",
        "hi": "अकबर",
        "en": "Akbar"
      }
    ],
    "correct": "B",
    "exp_hi": "बाबरनामा बाबर की आत्मकथा है जो उसने स्वयं लिखी।",
    "exp_en": "Baburnama is Babur's autobiography written by himself.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "प्लासी का युद्ध कब हुआ?",
    "q_en": "When was Battle of Plassey?",
    "options": [
      {
        "letter": "A",
        "hi": "1757",
        "en": "1757"
      },
      {
        "letter": "B",
        "hi": "1760",
        "en": "1760"
      },
      {
        "letter": "C",
        "hi": "1764",
        "en": "1764"
      },
      {
        "letter": "D",
        "hi": "1775",
        "en": "1775"
      }
    ],
    "correct": "A",
    "exp_hi": "प्लासी का युद्ध 1757 में हुआ।",
    "exp_en": "Battle of Plassey was in 1757.",
    "exam_tag": "UPSC 2018",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "बक्सर का युद्ध कब हुआ?",
    "q_en": "When was Battle of Buxar?",
    "options": [
      {
        "letter": "A",
        "hi": "1757",
        "en": "1757"
      },
      {
        "letter": "B",
        "hi": "1761",
        "en": "1761"
      },
      {
        "letter": "C",
        "hi": "1764",
        "en": "1764"
      },
      {
        "letter": "D",
        "hi": "1770",
        "en": "1770"
      }
    ],
    "correct": "C",
    "exp_hi": "बक्सर का युद्ध 1764 में हुआ।",
    "exp_en": "Battle of Buxar was in 1764.",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "INC की स्थापना कब हुई?",
    "q_en": "When was INC founded?",
    "options": [
      {
        "letter": "A",
        "hi": "1885",
        "en": "1885"
      },
      {
        "letter": "B",
        "hi": "1890",
        "en": "1890"
      },
      {
        "letter": "C",
        "hi": "1905",
        "en": "1905"
      },
      {
        "letter": "D",
        "hi": "1857",
        "en": "1857"
      }
    ],
    "correct": "A",
    "exp_hi": "INC की स्थापना 1885 में A.O. Hume ने की।",
    "exp_en": "INC was founded in 1885 by A.O. Hume.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "जलियाँवाला बाग हत्याकांड कब हुआ?",
    "q_en": "When was Jallianwala Bagh massacre?",
    "options": [
      {
        "letter": "A",
        "hi": "1917",
        "en": "1917"
      },
      {
        "letter": "B",
        "hi": "1919",
        "en": "1919"
      },
      {
        "letter": "C",
        "hi": "1920",
        "en": "1920"
      },
      {
        "letter": "D",
        "hi": "1922",
        "en": "1922"
      }
    ],
    "correct": "B",
    "exp_hi": "जलियाँवाला बाग 13 अप्रैल 1919 को हुआ।",
    "exp_en": "Jallianwala Bagh massacre was on 13 April 1919.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "स्थायी बंदोबस्त किसने लागू किया?",
    "q_en": "Who implemented Permanent Settlement?",
    "options": [
      {
        "letter": "A",
        "hi": "लॉर्ड कार्नवालिस",
        "en": "Lord Cornwallis"
      },
      {
        "letter": "B",
        "hi": "लॉर्ड वेलेजली",
        "en": "Lord Wellesley"
      },
      {
        "letter": "C",
        "hi": "लॉर्ड डलहौजी",
        "en": "Lord Dalhousie"
      },
      {
        "letter": "D",
        "hi": "लॉर्ड कर्जन",
        "en": "Lord Curzon"
      }
    ],
    "correct": "A",
    "exp_hi": "स्थायी बंदोबस्त 1793 में लॉर्ड कार्नवालिस ने लागू किया।",
    "exp_en": "Permanent Settlement was implemented by Lord Cornwallis in 1793.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "1857 विद्रोह के समय गवर्नर जनरल कौन था?",
    "q_en": "Governor General during 1857 revolt?",
    "options": [
      {
        "letter": "A",
        "hi": "डलहौजी",
        "en": "Dalhousie"
      },
      {
        "letter": "B",
        "hi": "कैनिंग",
        "en": "Canning"
      },
      {
        "letter": "C",
        "hi": "रिपन",
        "en": "Ripon"
      },
      {
        "letter": "D",
        "hi": "कर्जन",
        "en": "Curzon"
      }
    ],
    "correct": "B",
    "exp_hi": "1857 के समय लॉर्ड कैनिंग गवर्नर जनरल थे।",
    "exp_en": "Lord Canning was Governor General during 1857 revolt.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "लॉर्ड मैकाले ने भारत में शिक्षा नीति कब बनाई?",
    "q_en": "When did Lord Macaulay make education policy?",
    "options": [
      {
        "letter": "A",
        "hi": "1833",
        "en": "1833"
      },
      {
        "letter": "B",
        "hi": "1835",
        "en": "1835"
      },
      {
        "letter": "C",
        "hi": "1840",
        "en": "1840"
      },
      {
        "letter": "D",
        "hi": "1845",
        "en": "1845"
      }
    ],
    "correct": "B",
    "exp_hi": "लॉर्ड मैकाले ने 1835 में अंग्रेजी शिक्षा नीति बनाई।",
    "exp_en": "Lord Macaulay made English education policy in 1835.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "तीसरे आंग्ल-मराठा युद्ध का परिणाम क्या था?",
    "q_en": "Result of Third Anglo-Maratha War?",
    "options": [
      {
        "letter": "A",
        "hi": "मराठों की जीत",
        "en": "Maratha victory"
      },
      {
        "letter": "B",
        "hi": "मराठा साम्राज्य का अंत",
        "en": "End of Maratha empire"
      },
      {
        "letter": "C",
        "hi": "संधि",
        "en": "Treaty"
      },
      {
        "letter": "D",
        "hi": "युद्धविराम",
        "en": "Ceasefire"
      }
    ],
    "correct": "B",
    "exp_hi": "तीसरे आंग्ल-मराठा युद्ध (1817-18) में मराठा साम्राज्य का अंत हो गया।",
    "exp_en": "Third Anglo-Maratha War (1817-18) ended the Maratha empire.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "लॉर्ड डलहौजी की व्यपगत नीति क्या थी?",
    "q_en": "What was Doctrine of Lapse?",
    "options": [
      {
        "letter": "A",
        "hi": "कर वसूली नीति",
        "en": "Tax policy"
      },
      {
        "letter": "B",
        "hi": "राज्य हड़पने की नीति",
        "en": "Policy to annex states"
      },
      {
        "letter": "C",
        "hi": "सेना भर्ती नीति",
        "en": "Army policy"
      },
      {
        "letter": "D",
        "hi": "व्यापार नीति",
        "en": "Trade policy"
      }
    ],
    "correct": "B",
    "exp_hi": "व्यपगत नीति के तहत बिना उत्तराधिकारी के राज्य अंग्रेजों में मिल जाते थे।",
    "exp_en": "Under Doctrine of Lapse, states without heirs were annexed by British.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "भारत में पहली रेलगाड़ी कब चली?",
    "q_en": "When did first train run in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1850",
        "en": "1850"
      },
      {
        "letter": "B",
        "hi": "1853",
        "en": "1853"
      },
      {
        "letter": "C",
        "hi": "1856",
        "en": "1856"
      },
      {
        "letter": "D",
        "hi": "1860",
        "en": "1860"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत में पहली रेलगाड़ी 1853 में मुंबई से थाणे चली।",
    "exp_en": "First train in India ran from Mumbai to Thane in 1853.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "भारत में ब्रिटिश राज की स्थापना कब हुई?",
    "q_en": "When was British Raj established in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1757",
        "en": "1757"
      },
      {
        "letter": "B",
        "hi": "1765",
        "en": "1765"
      },
      {
        "letter": "C",
        "hi": "1858",
        "en": "1858"
      },
      {
        "letter": "D",
        "hi": "1876",
        "en": "1876"
      }
    ],
    "correct": "C",
    "exp_hi": "1857 के विद्रोह के बाद 1858 में ब्रिटिश क्राउन ने भारत का शासन लिया।",
    "exp_en": "British Crown took over India in 1858 after 1857 revolt.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "भारत में पहला मुद्रणालय कहाँ स्थापित हुआ?",
    "q_en": "Where was first printing press in India?",
    "options": [
      {
        "letter": "A",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "B",
        "hi": "गोवा",
        "en": "Goa"
      },
      {
        "letter": "C",
        "hi": "कोलकाता",
        "en": "Kolkata"
      },
      {
        "letter": "D",
        "hi": "मद्रास",
        "en": "Madras"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत में पहला मुद्रणालय 1556 में गोवा में स्थापित हुआ।",
    "exp_en": "First printing press in India was established in Goa in 1556.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "INC के प्रथम अध्यक्ष कौन थे?",
    "q_en": "First President of INC?",
    "options": [
      {
        "letter": "A",
        "hi": "दादाभाई नौरोजी",
        "en": "Dadabhai Naoroji"
      },
      {
        "letter": "B",
        "hi": "व्योमेश चंद्र बनर्जी",
        "en": "Womesh Chandra Bonerjee"
      },
      {
        "letter": "C",
        "hi": "बाल गंगाधर तिलक",
        "en": "Bal Gangadhar Tilak"
      },
      {
        "letter": "D",
        "hi": "गोपाल कृष्ण गोखले",
        "en": "Gopal Krishna Gokhale"
      }
    ],
    "correct": "B",
    "exp_hi": "व्योमेश चंद्र बनर्जी INC के प्रथम अध्यक्ष थे।",
    "exp_en": "Womesh Chandra Bonerjee was first President of INC.",
    "exam_tag": "SSC 2018",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "बंगाल विभाजन कब हुआ?",
    "q_en": "When was Bengal partitioned?",
    "options": [
      {
        "letter": "A",
        "hi": "1903",
        "en": "1903"
      },
      {
        "letter": "B",
        "hi": "1905",
        "en": "1905"
      },
      {
        "letter": "C",
        "hi": "1906",
        "en": "1906"
      },
      {
        "letter": "D",
        "hi": "1911",
        "en": "1911"
      }
    ],
    "correct": "B",
    "exp_hi": "बंगाल विभाजन 1905 में लॉर्ड कर्जन ने किया।",
    "exp_en": "Bengal was partitioned in 1905 by Lord Curzon.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "असहयोग आंदोलन कब शुरू हुआ?",
    "q_en": "When did Non-Cooperation Movement start?",
    "options": [
      {
        "letter": "A",
        "hi": "1919",
        "en": "1919"
      },
      {
        "letter": "B",
        "hi": "1920",
        "en": "1920"
      },
      {
        "letter": "C",
        "hi": "1922",
        "en": "1922"
      },
      {
        "letter": "D",
        "hi": "1930",
        "en": "1930"
      }
    ],
    "correct": "B",
    "exp_hi": "असहयोग आंदोलन 1920 में शुरू हुआ।",
    "exp_en": "Non-Cooperation Movement started in 1920.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "दांडी मार्च कब हुआ?",
    "q_en": "When was Dandi March?",
    "options": [
      {
        "letter": "A",
        "hi": "1920",
        "en": "1920"
      },
      {
        "letter": "B",
        "hi": "1930",
        "en": "1930"
      },
      {
        "letter": "C",
        "hi": "1942",
        "en": "1942"
      },
      {
        "letter": "D",
        "hi": "1915",
        "en": "1915"
      }
    ],
    "correct": "B",
    "exp_hi": "दांडी मार्च 1930 में नमक सत्याग्रह के तहत हुआ।",
    "exp_en": "Dandi March was in 1930 as Salt Satyagraha.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "भारत छोड़ो आंदोलन कब शुरू हुआ?",
    "q_en": "When did Quit India Movement start?",
    "options": [
      {
        "letter": "A",
        "hi": "1940",
        "en": "1940"
      },
      {
        "letter": "B",
        "hi": "1941",
        "en": "1941"
      },
      {
        "letter": "C",
        "hi": "1942",
        "en": "1942"
      },
      {
        "letter": "D",
        "hi": "1943",
        "en": "1943"
      }
    ],
    "correct": "C",
    "exp_hi": "भारत छोड़ो आंदोलन 8 अगस्त 1942 को शुरू हुआ।",
    "exp_en": "Quit India Movement started on 8 August 1942.",
    "exam_tag": "UPSC 2019",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "साइमन कमीशन भारत कब आया?",
    "q_en": "When did Simon Commission come to India?",
    "options": [
      {
        "letter": "A",
        "hi": "1926",
        "en": "1926"
      },
      {
        "letter": "B",
        "hi": "1927",
        "en": "1927"
      },
      {
        "letter": "C",
        "hi": "1928",
        "en": "1928"
      },
      {
        "letter": "D",
        "hi": "1929",
        "en": "1929"
      }
    ],
    "correct": "C",
    "exp_hi": "साइमन कमीशन 1928 में भारत आया।",
    "exp_en": "Simon Commission came to India in 1928.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "स्वदेशी आंदोलन कब शुरू हुआ?",
    "q_en": "When did Swadeshi Movement start?",
    "options": [
      {
        "letter": "A",
        "hi": "1903",
        "en": "1903"
      },
      {
        "letter": "B",
        "hi": "1905",
        "en": "1905"
      },
      {
        "letter": "C",
        "hi": "1907",
        "en": "1907"
      },
      {
        "letter": "D",
        "hi": "1909",
        "en": "1909"
      }
    ],
    "correct": "B",
    "exp_hi": "स्वदेशी आंदोलन 1905 में बंगाल विभाजन के विरोध में शुरू हुआ।",
    "exp_en": "Swadeshi Movement started in 1905 against Bengal partition.",
    "exam_tag": "CTET 2021",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "चौरी-चौरा कांड कब हुआ?",
    "q_en": "When was Chauri Chaura incident?",
    "options": [
      {
        "letter": "A",
        "hi": "1920",
        "en": "1920"
      },
      {
        "letter": "B",
        "hi": "1922",
        "en": "1922"
      },
      {
        "letter": "C",
        "hi": "1930",
        "en": "1930"
      },
      {
        "letter": "D",
        "hi": "1919",
        "en": "1919"
      }
    ],
    "correct": "B",
    "exp_hi": "चौरी-चौरा कांड 5 फरवरी 1922 को हुआ।",
    "exp_en": "Chauri Chaura incident was on 5 February 1922.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "नमक सत्याग्रह कब से कब तक चला?",
    "q_en": "Duration of Salt Satyagraha?",
    "options": [
      {
        "letter": "A",
        "hi": "मार्च-अप्रैल 1930",
        "en": "March-April 1930"
      },
      {
        "letter": "B",
        "hi": "जनवरी-फरवरी 1930",
        "en": "Jan-Feb 1930"
      },
      {
        "letter": "C",
        "hi": "मई-जून 1930",
        "en": "May-June 1930"
      },
      {
        "letter": "D",
        "hi": "अक्टूबर-नवंबर 1930",
        "en": "Oct-Nov 1930"
      }
    ],
    "correct": "A",
    "exp_hi": "नमक सत्याग्रह मार्च-अप्रैल 1930 में चला।",
    "exp_en": "Salt Satyagraha lasted from March-April 1930.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "होमरूल लीग की स्थापना किसने की?",
    "q_en": "Who founded Home Rule League?",
    "options": [
      {
        "letter": "A",
        "hi": "गांधीजी",
        "en": "Gandhiji"
      },
      {
        "letter": "B",
        "hi": "तिलक",
        "en": "Tilak"
      },
      {
        "letter": "C",
        "hi": "गोखले",
        "en": "Gokhale"
      },
      {
        "letter": "D",
        "hi": "नेहरू",
        "en": "Nehru"
      }
    ],
    "correct": "B",
    "exp_hi": "होमरूल लीग की स्थापना 1916 में बाल गंगाधर तिलक ने की।",
    "exp_en": "Home Rule League was founded by Bal Gangadhar Tilak in 1916.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "लखनऊ समझौता कब हुआ?",
    "q_en": "When was Lucknow Pact?",
    "options": [
      {
        "letter": "A",
        "hi": "1914",
        "en": "1914"
      },
      {
        "letter": "B",
        "hi": "1916",
        "en": "1916"
      },
      {
        "letter": "C",
        "hi": "1918",
        "en": "1918"
      },
      {
        "letter": "D",
        "hi": "1920",
        "en": "1920"
      }
    ],
    "correct": "B",
    "exp_hi": "लखनऊ समझौता 1916 में INC और मुस्लिम लीग के बीच हुआ।",
    "exp_en": "Lucknow Pact was in 1916 between INC and Muslim League.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "रॉलेट एक्ट कब पारित हुआ?",
    "q_en": "When was Rowlatt Act passed?",
    "options": [
      {
        "letter": "A",
        "hi": "1917",
        "en": "1917"
      },
      {
        "letter": "B",
        "hi": "1919",
        "en": "1919"
      },
      {
        "letter": "C",
        "hi": "1920",
        "en": "1920"
      },
      {
        "letter": "D",
        "hi": "1921",
        "en": "1921"
      }
    ],
    "correct": "B",
    "exp_hi": "रॉलेट एक्ट 1919 में पारित हुआ।",
    "exp_en": "Rowlatt Act was passed in 1919.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "गांधीजी दक्षिण अफ्रीका से भारत कब लौटे?",
    "q_en": "When did Gandhiji return from South Africa?",
    "options": [
      {
        "letter": "A",
        "hi": "1913",
        "en": "1913"
      },
      {
        "letter": "B",
        "hi": "1914",
        "en": "1914"
      },
      {
        "letter": "C",
        "hi": "1915",
        "en": "1915"
      },
      {
        "letter": "D",
        "hi": "1917",
        "en": "1917"
      }
    ],
    "correct": "C",
    "exp_hi": "गांधीजी 1915 में दक्षिण अफ्रीका से भारत लौटे।",
    "exp_en": "Gandhiji returned to India from South Africa in 1915.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "गांधी-इर्विन समझौता कब हुआ?",
    "q_en": "When was Gandhi-Irwin Pact?",
    "options": [
      {
        "letter": "A",
        "hi": "1930",
        "en": "1930"
      },
      {
        "letter": "B",
        "hi": "1931",
        "en": "1931"
      },
      {
        "letter": "C",
        "hi": "1932",
        "en": "1932"
      },
      {
        "letter": "D",
        "hi": "1933",
        "en": "1933"
      }
    ],
    "correct": "B",
    "exp_hi": "गांधी-इर्विन समझौता 5 मार्च 1931 को हुआ।",
    "exp_en": "Gandhi-Irwin Pact was on 5 March 1931.",
    "exam_tag": "UPSC 2016",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "तिलक ने 'स्वराज मेरा जन्मसिद्ध अधिकार' कब कहा?",
    "q_en": "When did Tilak say 'Swaraj is my birthright'?",
    "options": [
      {
        "letter": "A",
        "hi": "1905",
        "en": "1905"
      },
      {
        "letter": "B",
        "hi": "1907",
        "en": "1907"
      },
      {
        "letter": "C",
        "hi": "1916",
        "en": "1916"
      },
      {
        "letter": "D",
        "hi": "1920",
        "en": "1920"
      }
    ],
    "correct": "B",
    "exp_hi": "तिलक ने 1907 में सूरत कांग्रेस में यह बात कही।",
    "exp_en": "Tilak said this at Surat Congress in 1907.",
    "exam_tag": "SSC 2017",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "भारत में पहली जनगणना कब हुई?",
    "q_en": "When was first census in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1872",
        "en": "1872"
      },
      {
        "letter": "B",
        "hi": "1881",
        "en": "1881"
      },
      {
        "letter": "C",
        "hi": "1891",
        "en": "1891"
      },
      {
        "letter": "D",
        "hi": "1901",
        "en": "1901"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत में पहली नियमित जनगणना 1881 में हुई।",
    "exp_en": "First regular census in India was in 1881.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "भारत में प्रेस पर पहला प्रतिबंध किसने लगाया?",
    "q_en": "Who first restricted press in India?",
    "options": [
      {
        "letter": "A",
        "hi": "लॉर्ड वेलेजली",
        "en": "Lord Wellesley"
      },
      {
        "letter": "B",
        "hi": "लॉर्ड हेस्टिंग्स",
        "en": "Lord Hastings"
      },
      {
        "letter": "C",
        "hi": "लॉर्ड मेटकाफ",
        "en": "Lord Metcalfe"
      },
      {
        "letter": "D",
        "hi": "लॉर्ड कर्जन",
        "en": "Lord Curzon"
      }
    ],
    "correct": "A",
    "exp_hi": "लॉर्ड वेलेजली ने 1799 में प्रेस पर प्रतिबंध लगाया।",
    "exp_en": "Lord Wellesley imposed restrictions on press in 1799.",
    "exam_tag": "UPSC 2017",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "भारत में क्रांतिकारी आंदोलन के जनक कौन थे?",
    "q_en": "Father of revolutionary movement in India?",
    "options": [
      {
        "letter": "A",
        "hi": "भगत सिंह",
        "en": "Bhagat Singh"
      },
      {
        "letter": "B",
        "hi": "बाल गंगाधर तिलक",
        "en": "Bal Gangadhar Tilak"
      },
      {
        "letter": "C",
        "hi": "वासुदेव बलवंत फड़के",
        "en": "Vasudev Balwant Phadke"
      },
      {
        "letter": "D",
        "hi": "चंद्रशेखर आजाद",
        "en": "Chandrashekhar Azad"
      }
    ],
    "correct": "C",
    "exp_hi": "वासुदेव बलवंत फड़के को भारत में क्रांतिकारी आंदोलन का जनक माना जाता है।",
    "exp_en": "Vasudev Balwant Phadke is considered father of revolutionary movement in India.",
    "exam_tag": "SSC 2018",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "भगत सिंह को फाँसी कब दी गई?",
    "q_en": "When was Bhagat Singh hanged?",
    "options": [
      {
        "letter": "A",
        "hi": "1929",
        "en": "1929"
      },
      {
        "letter": "B",
        "hi": "1931",
        "en": "1931"
      },
      {
        "letter": "C",
        "hi": "1930",
        "en": "1930"
      },
      {
        "letter": "D",
        "hi": "1932",
        "en": "1932"
      }
    ],
    "correct": "B",
    "exp_hi": "भगत सिंह, राजगुरु और सुखदेव को 23 मार्च 1931 को फाँसी दी गई।",
    "exp_en": "Bhagat Singh, Rajguru and Sukhdev were hanged on 23 March 1931.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "काकोरी कांड कब हुआ?",
    "q_en": "When was Kakori Conspiracy?",
    "options": [
      {
        "letter": "A",
        "hi": "1922",
        "en": "1922"
      },
      {
        "letter": "B",
        "hi": "1925",
        "en": "1925"
      },
      {
        "letter": "C",
        "hi": "1929",
        "en": "1929"
      },
      {
        "letter": "D",
        "hi": "1931",
        "en": "1931"
      }
    ],
    "correct": "B",
    "exp_hi": "काकोरी कांड 9 अगस्त 1925 को हुआ।",
    "exp_en": "Kakori Conspiracy happened on 9 August 1925.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "चंद्रशेखर आजाद की मृत्यु कब हुई?",
    "q_en": "When did Chandrashekhar Azad die?",
    "options": [
      {
        "letter": "A",
        "hi": "1929",
        "en": "1929"
      },
      {
        "letter": "B",
        "hi": "1931",
        "en": "1931"
      },
      {
        "letter": "C",
        "hi": "1930",
        "en": "1930"
      },
      {
        "letter": "D",
        "hi": "1932",
        "en": "1932"
      }
    ],
    "correct": "B",
    "exp_hi": "चंद्रशेखर आजाद 27 फरवरी 1931 को इलाहाबाद के अल्फ्रेड पार्क में शहीद हुए।",
    "exp_en": "Chandrashekhar Azad died on 27 February 1931 in Allahabad's Alfred Park.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "साइमन कमीशन का बहिष्कार क्यों हुआ?",
    "q_en": "Why was Simon Commission boycotted?",
    "options": [
      {
        "letter": "A",
        "hi": "कोई भारतीय सदस्य नहीं था",
        "en": "No Indian member"
      },
      {
        "letter": "B",
        "hi": "ब्रिटिश विरोध",
        "en": "British opposition"
      },
      {
        "letter": "C",
        "hi": "कांग्रेस विरोध",
        "en": "Congress opposition"
      },
      {
        "letter": "D",
        "hi": "मुस्लिम विरोध",
        "en": "Muslim opposition"
      }
    ],
    "correct": "A",
    "exp_hi": "साइमन कमीशन में कोई भारतीय सदस्य नहीं था, इसलिए बहिष्कार हुआ।",
    "exp_en": "Simon Commission had no Indian member, hence boycott.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "INA (आजाद हिंद फौज) की स्थापना किसने की?",
    "q_en": "Who established INA (Azad Hind Fauj)?",
    "options": [
      {
        "letter": "A",
        "hi": "सुभाष चंद्र बोस",
        "en": "Subhas Chandra Bose"
      },
      {
        "letter": "B",
        "hi": "रास बिहारी बोस",
        "en": "Rash Behari Bose"
      },
      {
        "letter": "C",
        "hi": "मोहन सिंह",
        "en": "Mohan Singh"
      },
      {
        "letter": "D",
        "hi": "शाहनवाज खान",
        "en": "Shah Nawaz Khan"
      }
    ],
    "correct": "C",
    "exp_hi": "INA की स्थापना मूलतः मोहन सिंह ने 1942 में की, बाद में सुभाष चंद्र बोस ने नेतृत्व लिया।",
    "exp_en": "INA was originally established by Mohan Singh in 1942, later led by Subhas Chandra Bose.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "नेहरू रिपोर्ट कब आई?",
    "q_en": "When did Nehru Report come?",
    "options": [
      {
        "letter": "A",
        "hi": "1926",
        "en": "1926"
      },
      {
        "letter": "B",
        "hi": "1928",
        "en": "1928"
      },
      {
        "letter": "C",
        "hi": "1930",
        "en": "1930"
      },
      {
        "letter": "D",
        "hi": "1932",
        "en": "1932"
      }
    ],
    "correct": "B",
    "exp_hi": "नेहरू रिपोर्ट 1928 में मोतीलाल नेहरू की अध्यक्षता में बनी।",
    "exp_en": "Nehru Report came in 1928 under Motilal Nehru's chairmanship.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "गांधीजी का पहला सत्याग्रह भारत में कहाँ हुआ?",
    "q_en": "Where was Gandhiji's first Satyagraha in India?",
    "options": [
      {
        "letter": "A",
        "hi": "अहमदाबाद",
        "en": "Ahmedabad"
      },
      {
        "letter": "B",
        "hi": "खेड़ा",
        "en": "Kheda"
      },
      {
        "letter": "C",
        "hi": "चंपारण",
        "en": "Champaran"
      },
      {
        "letter": "D",
        "hi": "बारदोली",
        "en": "Bardoli"
      }
    ],
    "correct": "C",
    "exp_hi": "गांधीजी का पहला सत्याग्रह 1917 में बिहार के चंपारण में हुआ।",
    "exp_en": "Gandhiji's first Satyagraha in India was in Champaran, Bihar in 1917.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "माउंटबेटन योजना कब घोषित हुई?",
    "q_en": "When was Mountbatten Plan announced?",
    "options": [
      {
        "letter": "A",
        "hi": "मई 1947",
        "en": "May 1947"
      },
      {
        "letter": "B",
        "hi": "जून 1947",
        "en": "June 1947"
      },
      {
        "letter": "C",
        "hi": "जुलाई 1947",
        "en": "July 1947"
      },
      {
        "letter": "D",
        "hi": "अगस्त 1947",
        "en": "August 1947"
      }
    ],
    "correct": "B",
    "exp_hi": "माउंटबेटन योजना 3 जून 1947 को घोषित हुई।",
    "exp_en": "Mountbatten Plan was announced on 3 June 1947.",
    "exam_tag": "UPSC 2015",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "स्वतंत्र भारत के प्रथम प्रधानमंत्री कौन थे?",
    "q_en": "First PM of independent India?",
    "options": [
      {
        "letter": "A",
        "hi": "सरदार पटेल",
        "en": "Sardar Patel"
      },
      {
        "letter": "B",
        "hi": "जवाहरलाल नेहरू",
        "en": "Jawaharlal Nehru"
      },
      {
        "letter": "C",
        "hi": "राजेंद्र प्रसाद",
        "en": "Rajendra Prasad"
      },
      {
        "letter": "D",
        "hi": "मौलाना आजाद",
        "en": "Maulana Azad"
      }
    ],
    "correct": "B",
    "exp_hi": "जवाहरलाल नेहरू स्वतंत्र भारत के प्रथम प्रधानमंत्री थे।",
    "exp_en": "Jawaharlal Nehru was first PM of independent India.",
    "exam_tag": "SSC 2016",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारतीय स्वतंत्रता अधिनियम कब पारित हुआ?",
    "q_en": "When was Indian Independence Act passed?",
    "options": [
      {
        "letter": "A",
        "hi": "1946",
        "en": "1946"
      },
      {
        "letter": "B",
        "hi": "1947",
        "en": "1947"
      },
      {
        "letter": "C",
        "hi": "1948",
        "en": "1948"
      },
      {
        "letter": "D",
        "hi": "1950",
        "en": "1950"
      }
    ],
    "correct": "B",
    "exp_hi": "भारतीय स्वतंत्रता अधिनियम जुलाई 1947 में पारित हुआ।",
    "exp_en": "Indian Independence Act was passed in July 1947.",
    "exam_tag": "Railway 2017",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "सुभाष चंद्र बोस ने INA की स्थापना कहाँ की?",
    "q_en": "Where did Subhas Chandra Bose establish INA?",
    "options": [
      {
        "letter": "A",
        "hi": "जापान",
        "en": "Japan"
      },
      {
        "letter": "B",
        "hi": "सिंगापुर",
        "en": "Singapore"
      },
      {
        "letter": "C",
        "hi": "जर्मनी",
        "en": "Germany"
      },
      {
        "letter": "D",
        "hi": "बर्मा",
        "en": "Burma"
      }
    ],
    "correct": "B",
    "exp_hi": "सुभाष चंद्र बोस ने 1943 में सिंगापुर में INA का नेतृत्व लिया।",
    "exp_en": "Subhas Chandra Bose took leadership of INA in Singapore in 1943.",
    "exam_tag": "UPSC 2014",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत का विभाजन कब हुआ?",
    "q_en": "When was India partitioned?",
    "options": [
      {
        "letter": "A",
        "hi": "14 अगस्त 1947",
        "en": "14 August 1947"
      },
      {
        "letter": "B",
        "hi": "15 अगस्त 1947",
        "en": "15 August 1947"
      },
      {
        "letter": "C",
        "hi": "26 जनवरी 1950",
        "en": "26 January 1950"
      },
      {
        "letter": "D",
        "hi": "1 जनवरी 1948",
        "en": "1 January 1948"
      }
    ],
    "correct": "A",
    "exp_hi": "भारत-पाकिस्तान विभाजन 14-15 अगस्त 1947 को हुआ।",
    "exp_en": "India-Pakistan partition happened on 14-15 August 1947.",
    "exam_tag": "SSC 2015",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "क्रिप्स मिशन भारत कब आया?",
    "q_en": "When did Cripps Mission come to India?",
    "options": [
      {
        "letter": "A",
        "hi": "1940",
        "en": "1940"
      },
      {
        "letter": "B",
        "hi": "1942",
        "en": "1942"
      },
      {
        "letter": "C",
        "hi": "1944",
        "en": "1944"
      },
      {
        "letter": "D",
        "hi": "1946",
        "en": "1946"
      }
    ],
    "correct": "B",
    "exp_hi": "क्रिप्स मिशन 1942 में भारत आया।",
    "exp_en": "Cripps Mission came to India in 1942.",
    "exam_tag": "Railway 2016",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "कैबिनेट मिशन भारत कब आया?",
    "q_en": "When did Cabinet Mission come to India?",
    "options": [
      {
        "letter": "A",
        "hi": "1944",
        "en": "1944"
      },
      {
        "letter": "B",
        "hi": "1945",
        "en": "1945"
      },
      {
        "letter": "C",
        "hi": "1946",
        "en": "1946"
      },
      {
        "letter": "D",
        "hi": "1947",
        "en": "1947"
      }
    ],
    "correct": "C",
    "exp_hi": "कैबिनेट मिशन 1946 में भारत आया।",
    "exp_en": "Cabinet Mission came to India in 1946.",
    "exam_tag": "UPSC 2016",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत को स्वतंत्रता कब मिली?",
    "q_en": "When did India get independence?",
    "options": [
      {
        "letter": "A",
        "hi": "14 अगस्त 1947",
        "en": "14 August 1947"
      },
      {
        "letter": "B",
        "hi": "15 अगस्त 1947",
        "en": "15 August 1947"
      },
      {
        "letter": "C",
        "hi": "26 जनवरी 1950",
        "en": "26 January 1950"
      },
      {
        "letter": "D",
        "hi": "2 अक्टूबर 1947",
        "en": "2 October 1947"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत को 15 अगस्त 1947 को स्वतंत्रता मिली।",
    "exp_en": "India got independence on 15 August 1947.",
    "exam_tag": "SSC 2017",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत के एकीकरण में सबसे बड़ी भूमिका किसकी थी?",
    "q_en": "Who played biggest role in integration of India?",
    "options": [
      {
        "letter": "A",
        "hi": "जवाहरलाल नेहरू",
        "en": "Jawaharlal Nehru"
      },
      {
        "letter": "B",
        "hi": "सरदार पटेल",
        "en": "Sardar Patel"
      },
      {
        "letter": "C",
        "hi": "राजेंद्र प्रसाद",
        "en": "Rajendra Prasad"
      },
      {
        "letter": "D",
        "hi": "मौलाना आजाद",
        "en": "Maulana Azad"
      }
    ],
    "correct": "B",
    "exp_hi": "सरदार वल्लभभाई पटेल ने 562 रियासतों का भारत में विलय कराया।",
    "exp_en": "Sardar Vallabhbhai Patel integrated 562 princely states into India.",
    "exam_tag": "Railway 2018",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत के प्रथम गृहमंत्री कौन थे?",
    "q_en": "First Home Minister of India?",
    "options": [
      {
        "letter": "A",
        "hi": "जवाहरलाल नेहरू",
        "en": "Jawaharlal Nehru"
      },
      {
        "letter": "B",
        "hi": "सरदार पटेल",
        "en": "Sardar Patel"
      },
      {
        "letter": "C",
        "hi": "मौलाना आजाद",
        "en": "Maulana Azad"
      },
      {
        "letter": "D",
        "hi": "राजेंद्र प्रसाद",
        "en": "Rajendra Prasad"
      }
    ],
    "correct": "B",
    "exp_hi": "सरदार पटेल भारत के प्रथम गृहमंत्री थे।",
    "exp_en": "Sardar Patel was India's first Home Minister.",
    "exam_tag": "UPSC 2018",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "राष्ट्रीय स्वयंसेवक संघ (RSS) की स्थापना कब हुई?",
    "q_en": "When was RSS founded?",
    "options": [
      {
        "letter": "A",
        "hi": "1920",
        "en": "1920"
      },
      {
        "letter": "B",
        "hi": "1925",
        "en": "1925"
      },
      {
        "letter": "C",
        "hi": "1930",
        "en": "1930"
      },
      {
        "letter": "D",
        "hi": "1935",
        "en": "1935"
      }
    ],
    "correct": "B",
    "exp_hi": "RSS की स्थापना 1925 में डॉ. केशव बलिराम हेडगेवार ने की।",
    "exp_en": "RSS was founded in 1925 by Dr. Keshav Baliram Hedgewar.",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत-चीन युद्ध कब हुआ?",
    "q_en": "When was India-China war?",
    "options": [
      {
        "letter": "A",
        "hi": "1960",
        "en": "1960"
      },
      {
        "letter": "B",
        "hi": "1962",
        "en": "1962"
      },
      {
        "letter": "C",
        "hi": "1965",
        "en": "1965"
      },
      {
        "letter": "D",
        "hi": "1971",
        "en": "1971"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत-चीन युद्ध 1962 में हुआ।",
    "exp_en": "India-China war was in 1962.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत-पाकिस्तान युद्ध 1971 का परिणाम?",
    "q_en": "Result of India-Pakistan war 1971?",
    "options": [
      {
        "letter": "A",
        "hi": "पाकिस्तान की जीत",
        "en": "Pakistan victory"
      },
      {
        "letter": "B",
        "hi": "भारत की जीत और बांग्लादेश निर्माण",
        "en": "India victory and Bangladesh creation"
      },
      {
        "letter": "C",
        "hi": "युद्धविराम",
        "en": "Ceasefire"
      },
      {
        "letter": "D",
        "hi": "संधि",
        "en": "Treaty"
      }
    ],
    "correct": "B",
    "exp_hi": "1971 के युद्ध में भारत जीता और बांग्लादेश का निर्माण हुआ।",
    "exp_en": "India won 1971 war and Bangladesh was created.",
    "exam_tag": "UPSC 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत में आपातकाल कब लागू हुआ?",
    "q_en": "When was Emergency imposed in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1974",
        "en": "1974"
      },
      {
        "letter": "B",
        "hi": "1975",
        "en": "1975"
      },
      {
        "letter": "C",
        "hi": "1976",
        "en": "1976"
      },
      {
        "letter": "D",
        "hi": "1977",
        "en": "1977"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत में आपातकाल 25 जून 1975 को लागू हुआ।",
    "exp_en": "Emergency was imposed in India on 25 June 1975.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत में पहले परमाणु परीक्षण कब हुआ?",
    "q_en": "When was India's first nuclear test?",
    "options": [
      {
        "letter": "A",
        "hi": "1972",
        "en": "1972"
      },
      {
        "letter": "B",
        "hi": "1974",
        "en": "1974"
      },
      {
        "letter": "C",
        "hi": "1978",
        "en": "1978"
      },
      {
        "letter": "D",
        "hi": "1998",
        "en": "1998"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत का पहला परमाणु परीक्षण 1974 में पोखरण में हुआ।",
    "exp_en": "India's first nuclear test was at Pokhran in 1974.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत में हरित क्रांति के जनक कौन हैं?",
    "q_en": "Father of Green Revolution in India?",
    "options": [
      {
        "letter": "A",
        "hi": "वर्गीज कुरियन",
        "en": "Verghese Kurien"
      },
      {
        "letter": "B",
        "hi": "एम.एस. स्वामीनाथन",
        "en": "M.S. Swaminathan"
      },
      {
        "letter": "C",
        "hi": "नॉर्मन बोरलॉग",
        "en": "Norman Borlaug"
      },
      {
        "letter": "D",
        "hi": "सी. सुब्रमण्यम",
        "en": "C. Subramaniam"
      }
    ],
    "correct": "B",
    "exp_hi": "एम.एस. स्वामीनाथन को भारत में हरित क्रांति का जनक कहते हैं।",
    "exp_en": "M.S. Swaminathan is called father of Green Revolution in India.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "बंगाल विभाजन रद्द कब हुआ?",
    "q_en": "When was Bengal partition annulled?",
    "options": [
      {
        "letter": "A",
        "hi": "1908",
        "en": "1908"
      },
      {
        "letter": "B",
        "hi": "1911",
        "en": "1911"
      },
      {
        "letter": "C",
        "hi": "1915",
        "en": "1915"
      },
      {
        "letter": "D",
        "hi": "1919",
        "en": "1919"
      }
    ],
    "correct": "B",
    "exp_hi": "1905 का बंगाल विभाजन 1911 में रद्द हुआ।",
    "exp_en": "Bengal partition of 1905 was annulled in 1911.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "ऑपरेशन ब्लू स्टार कब हुआ?",
    "q_en": "When was Operation Blue Star?",
    "options": [
      {
        "letter": "A",
        "hi": "1982",
        "en": "1982"
      },
      {
        "letter": "B",
        "hi": "1984",
        "en": "1984"
      },
      {
        "letter": "C",
        "hi": "1986",
        "en": "1986"
      },
      {
        "letter": "D",
        "hi": "1988",
        "en": "1988"
      }
    ],
    "correct": "B",
    "exp_hi": "ऑपरेशन ब्लू स्टार जून 1984 में अमृतसर के स्वर्ण मंदिर में हुआ।",
    "exp_en": "Operation Blue Star happened in June 1984 at Golden Temple, Amritsar.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत में पोखरण-2 परमाणु परीक्षण कब हुआ?",
    "q_en": "When was Pokhran-2 nuclear test?",
    "options": [
      {
        "letter": "A",
        "hi": "1995",
        "en": "1995"
      },
      {
        "letter": "B",
        "hi": "1996",
        "en": "1996"
      },
      {
        "letter": "C",
        "hi": "1998",
        "en": "1998"
      },
      {
        "letter": "D",
        "hi": "2000",
        "en": "2000"
      }
    ],
    "correct": "C",
    "exp_hi": "पोखरण-2 परमाणु परीक्षण मई 1998 में हुआ।",
    "exp_en": "Pokhran-2 nuclear test happened in May 1998.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत में 73वाँ संवैधानिक संशोधन कब हुआ?",
    "q_en": "When was 73rd Constitutional Amendment?",
    "options": [
      {
        "letter": "A",
        "hi": "1990",
        "en": "1990"
      },
      {
        "letter": "B",
        "hi": "1992",
        "en": "1992"
      },
      {
        "letter": "C",
        "hi": "1994",
        "en": "1994"
      },
      {
        "letter": "D",
        "hi": "1996",
        "en": "1996"
      }
    ],
    "correct": "B",
    "exp_hi": "73वाँ संशोधन 1992 में हुआ जिसने पंचायती राज को संवैधानिक दर्जा दिया।",
    "exp_en": "73rd Amendment of 1992 gave constitutional status to Panchayati Raj.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत-पाक के बीच शिमला समझौता कब हुआ?",
    "q_en": "When was Shimla Agreement between India-Pakistan?",
    "options": [
      {
        "letter": "A",
        "hi": "1971",
        "en": "1971"
      },
      {
        "letter": "B",
        "hi": "1972",
        "en": "1972"
      },
      {
        "letter": "C",
        "hi": "1973",
        "en": "1973"
      },
      {
        "letter": "D",
        "hi": "1974",
        "en": "1974"
      }
    ],
    "correct": "B",
    "exp_hi": "शिमला समझौता 2 जुलाई 1972 को इंदिरा गांधी और जुल्फिकार अली भुट्टो के बीच हुआ।",
    "exp_en": "Shimla Agreement was signed on 2 July 1972 between Indira Gandhi and Zulfikar Ali Bhutto.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "सती प्रथा पर कानून कब बना?",
    "q_en": "When was law against Sati made?",
    "options": [
      {
        "letter": "A",
        "hi": "1825",
        "en": "1825"
      },
      {
        "letter": "B",
        "hi": "1829",
        "en": "1829"
      },
      {
        "letter": "C",
        "hi": "1835",
        "en": "1835"
      },
      {
        "letter": "D",
        "hi": "1840",
        "en": "1840"
      }
    ],
    "correct": "B",
    "exp_hi": "राजा राम मोहन राय के प्रयासों से 1829 में सती प्रथा पर कानून बना।",
    "exp_en": "Law against Sati was made in 1829 due to Raja Ram Mohan Roy's efforts.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "भारतीय राष्ट्रीय आंदोलन में नरम दल के नेता कौन थे?",
    "q_en": "Leader of moderates in Indian National Movement?",
    "options": [
      {
        "letter": "A",
        "hi": "बाल गंगाधर तिलक",
        "en": "Bal Gangadhar Tilak"
      },
      {
        "letter": "B",
        "hi": "गोपाल कृष्ण गोखले",
        "en": "Gopal Krishna Gokhale"
      },
      {
        "letter": "C",
        "hi": "लाला लाजपत राय",
        "en": "Lala Lajpat Rai"
      },
      {
        "letter": "D",
        "hi": "विपिन चंद्र पाल",
        "en": "Bipin Chandra Pal"
      }
    ],
    "correct": "B",
    "exp_hi": "गोपाल कृष्ण गोखले नरम दल के प्रमुख नेता थे।",
    "exp_en": "Gopal Krishna Gokhale was the main leader of moderates.",
    "exam_tag": "CTET 2024",
    "class": "कक्षา 9"
  },
  {
    "subject": "history",
    "q_hi": "भारत में विधवा पुनर्विवाह अधिनियम कब बना?",
    "q_en": "When was Widow Remarriage Act in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1850",
        "en": "1850"
      },
      {
        "letter": "B",
        "hi": "1856",
        "en": "1856"
      },
      {
        "letter": "C",
        "hi": "1860",
        "en": "1860"
      },
      {
        "letter": "D",
        "hi": "1870",
        "en": "1870"
      }
    ],
    "correct": "B",
    "exp_hi": "विधवा पुनर्विवाह अधिनियम 1856 में ईश्वरचंद्र विद्यासागर के प्रयासों से बना।",
    "exp_en": "Widow Remarriage Act was passed in 1856 due to Ishwarchandra Vidyasagar's efforts.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "भक्ति आंदोलन के प्रमुख संत कौन थे?",
    "q_en": "Major saint of Bhakti movement?",
    "options": [
      {
        "letter": "A",
        "hi": "कबीर",
        "en": "Kabir"
      },
      {
        "letter": "B",
        "hi": "रामानुज",
        "en": "Ramanuja"
      },
      {
        "letter": "C",
        "hi": "शंकराचार्य",
        "en": "Shankaracharya"
      },
      {
        "letter": "D",
        "hi": "चैतन्य",
        "en": "Chaitanya"
      }
    ],
    "correct": "A",
    "exp_hi": "कबीर भक्ति आंदोलन के सबसे लोकप्रिय संत थे।",
    "exp_en": "Kabir was the most popular saint of Bhakti movement.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "गौतम बुद्ध का बचपन का नाम क्या था?",
    "q_en": "What was Gautam Buddha's childhood name?",
    "options": [
      {
        "letter": "A",
        "hi": "सिद्धार्थ",
        "en": "Siddhartha"
      },
      {
        "letter": "B",
        "hi": "देवदत्त",
        "en": "Devadatta"
      },
      {
        "letter": "C",
        "hi": "आनंद",
        "en": "Ananda"
      },
      {
        "letter": "D",
        "hi": "राहुल",
        "en": "Rahul"
      }
    ],
    "correct": "A",
    "exp_hi": "गौतम बुद्ध का बचपन का नाम सिद्धार्थ था।",
    "exp_en": "Gautam Buddha's childhood name was Siddhartha.",
    "exam_tag": "Railway 2024",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "भारत में साम्यवादी पार्टी की स्थापना कब हुई?",
    "q_en": "When was Communist Party of India founded?",
    "options": [
      {
        "letter": "A",
        "hi": "1918",
        "en": "1918"
      },
      {
        "letter": "B",
        "hi": "1920",
        "en": "1920"
      },
      {
        "letter": "C",
        "hi": "1921",
        "en": "1921"
      },
      {
        "letter": "D",
        "hi": "1925",
        "en": "1925"
      }
    ],
    "correct": "C",
    "exp_hi": "भारतीय कम्युनिस्ट पार्टी की स्थापना 1921 में ताशकंद में हुई।",
    "exp_en": "Communist Party of India was founded in 1921 in Tashkent.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "लाल किले का निर्माण किसने करवाया?",
    "q_en": "Who built Red Fort?",
    "options": [
      {
        "letter": "A",
        "hi": "अकबर",
        "en": "Akbar"
      },
      {
        "letter": "B",
        "hi": "जहाँगीर",
        "en": "Jahangir"
      },
      {
        "letter": "C",
        "hi": "शाहजहाँ",
        "en": "Shah Jahan"
      },
      {
        "letter": "D",
        "hi": "औरंगजेब",
        "en": "Aurangzeb"
      }
    ],
    "correct": "C",
    "exp_hi": "लाल किले का निर्माण शाहजहाँ ने 1638-48 के बीच कराया।",
    "exp_en": "Red Fort was built by Shah Jahan between 1638-48.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "भारत में पहला समाचार पत्र कौन सा था?",
    "q_en": "Which was first newspaper in India?",
    "options": [
      {
        "letter": "A",
        "hi": "बंगाल गजट",
        "en": "Bengal Gazette"
      },
      {
        "letter": "B",
        "hi": "टाइम्स ऑफ इंडिया",
        "en": "Times of India"
      },
      {
        "letter": "C",
        "hi": "हिंदुस्तान टाइम्स",
        "en": "Hindustan Times"
      },
      {
        "letter": "D",
        "hi": "इंडियन एक्सप्रेस",
        "en": "Indian Express"
      }
    ],
    "correct": "A",
    "exp_hi": "बंगाल गजट 1780 में जेम्स ऑगस्टस हिक्की द्वारा भारत का पहला समाचार पत्र था।",
    "exp_en": "Bengal Gazette was India's first newspaper in 1780 by James Augustus Hicky.",
    "exam_tag": "Railway 2024",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "उपनिषद किससे संबंधित हैं?",
    "q_en": "Upanishads are related to?",
    "options": [
      {
        "letter": "A",
        "hi": "दर्शन",
        "en": "Philosophy"
      },
      {
        "letter": "B",
        "hi": "संगीत",
        "en": "Music"
      },
      {
        "letter": "C",
        "hi": "चिकित्सा",
        "en": "Medicine"
      },
      {
        "letter": "D",
        "hi": "गणित",
        "en": "Mathematics"
      }
    ],
    "correct": "A",
    "exp_hi": "उपनिषद भारतीय दर्शन के महत्वपूर्ण ग्रंथ हैं।",
    "exp_en": "Upanishads are important texts of Indian philosophy.",
    "exam_tag": "SSC 2016",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "महाजनपद काल में कितने महाजनपद थे?",
    "q_en": "How many Mahajanapadas were there?",
    "options": [
      {
        "letter": "A",
        "hi": "12",
        "en": "12"
      },
      {
        "letter": "B",
        "hi": "14",
        "en": "14"
      },
      {
        "letter": "C",
        "hi": "16",
        "en": "16"
      },
      {
        "letter": "D",
        "hi": "18",
        "en": "18"
      }
    ],
    "correct": "C",
    "exp_hi": "महाजनपद काल में 16 महाजनपद थे।",
    "exp_en": "There were 16 Mahajanapadas.",
    "exam_tag": "Railway 2016",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "मगध साम्राज्य की राजधानी क्या थी?",
    "q_en": "Capital of Magadha Empire?",
    "options": [
      {
        "letter": "A",
        "hi": "वैशाली",
        "en": "Vaishali"
      },
      {
        "letter": "B",
        "hi": "राजगृह/पाटलिपुत्र",
        "en": "Rajgriha/Pataliputra"
      },
      {
        "letter": "C",
        "hi": "उज्जैन",
        "en": "Ujjain"
      },
      {
        "letter": "D",
        "hi": "तक्षशिला",
        "en": "Taxila"
      }
    ],
    "correct": "B",
    "exp_hi": "मगध की राजधानी पहले राजगृह थी, बाद में पाटलिपुत्र बनी।",
    "exp_en": "Magadha's capital was first Rajgriha, later Pataliputra.",
    "exam_tag": "CTET 2017",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "तक्षशिला कहाँ था?",
    "q_en": "Where was Taxila located?",
    "options": [
      {
        "letter": "A",
        "hi": "भारत",
        "en": "India"
      },
      {
        "letter": "B",
        "hi": "पाकिस्तान",
        "en": "Pakistan"
      },
      {
        "letter": "C",
        "hi": "अफगानिस्तान",
        "en": "Afghanistan"
      },
      {
        "letter": "D",
        "hi": "बांग्लादेश",
        "en": "Bangladesh"
      }
    ],
    "correct": "B",
    "exp_hi": "तक्षशिला अब पाकिस्तान में है।",
    "exp_en": "Taxila is now in Pakistan.",
    "exam_tag": "SSC 2017",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "सुल्तान महमूद गजनी ने भारत पर कितनी बार आक्रमण किया?",
    "q_en": "How many times did Mahmud Ghazni invade India?",
    "options": [
      {
        "letter": "A",
        "hi": "12",
        "en": "12"
      },
      {
        "letter": "B",
        "hi": "17",
        "en": "17"
      },
      {
        "letter": "C",
        "hi": "20",
        "en": "20"
      },
      {
        "letter": "D",
        "hi": "25",
        "en": "25"
      }
    ],
    "correct": "B",
    "exp_hi": "महमूद गजनी ने भारत पर 17 बार आक्रमण किया।",
    "exp_en": "Mahmud Ghazni invaded India 17 times.",
    "exam_tag": "UPSC 2015",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "रजिया सुल्तान किसकी पुत्री थी?",
    "q_en": "Razia Sultan was daughter of?",
    "options": [
      {
        "letter": "A",
        "hi": "कुतुबुद्दीन ऐबक",
        "en": "Qutbuddin Aibak"
      },
      {
        "letter": "B",
        "hi": "इल्तुतमिश",
        "en": "Iltutmish"
      },
      {
        "letter": "C",
        "hi": "बलबन",
        "en": "Balban"
      },
      {
        "letter": "D",
        "hi": "नासिरुद्दीन",
        "en": "Nasiruddin"
      }
    ],
    "correct": "B",
    "exp_hi": "रजिया सुल्तान इल्तुतमिश की पुत्री थी।",
    "exp_en": "Razia Sultan was daughter of Iltutmish.",
    "exam_tag": "SSC 2016",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "अलाउद्दीन खिलजी का बाजार नियंत्रण प्रसिद्ध क्यों था?",
    "q_en": "Why was Alauddin Khilji's market control famous?",
    "options": [
      {
        "letter": "A",
        "hi": "मूल्य नियंत्रण के लिए",
        "en": "For price control"
      },
      {
        "letter": "B",
        "hi": "वस्तु गुणवत्ता के लिए",
        "en": "For quality control"
      },
      {
        "letter": "C",
        "hi": "आयात नियंत्रण के लिए",
        "en": "For import control"
      },
      {
        "letter": "D",
        "hi": "निर्यात नियंत्रण के लिए",
        "en": "For export control"
      }
    ],
    "correct": "A",
    "exp_hi": "अलाउद्दीन ने 4 बाजार बनाए जहाँ मूल्य नियंत्रण था।",
    "exp_en": "Alauddin set up 4 markets with strict price control.",
    "exam_tag": "Railway 2017",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "कृष्णदेवराय किस साम्राज्य के शासक थे?",
    "q_en": "Krishnadevaraya was ruler of which empire?",
    "options": [
      {
        "letter": "A",
        "hi": "चोल",
        "en": "Chola"
      },
      {
        "letter": "B",
        "hi": "विजयनगर",
        "en": "Vijayanagara"
      },
      {
        "letter": "C",
        "hi": "पल्लव",
        "en": "Pallava"
      },
      {
        "letter": "D",
        "hi": "बहमनी",
        "en": "Bahmani"
      }
    ],
    "correct": "B",
    "exp_hi": "कृष्णदेवराय विजयनगर साम्राज्य के महान शासक थे।",
    "exp_en": "Krishnadevaraya was the great ruler of Vijayanagara empire.",
    "exam_tag": "CTET 2017",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "सूफी संत निजामुद्दीन औलिया किस शासक के समकालीन थे?",
    "q_en": "Sufi saint Nizamuddin Auliya was contemporary of?",
    "options": [
      {
        "letter": "A",
        "hi": "अलाउद्दीन खिलजी",
        "en": "Alauddin Khilji"
      },
      {
        "letter": "B",
        "hi": "मुहम्मद बिन तुगलक",
        "en": "Muhammad bin Tughlaq"
      },
      {
        "letter": "C",
        "hi": "बलबन",
        "en": "Balban"
      },
      {
        "letter": "D",
        "hi": "फिरोज तुगलक",
        "en": "Firoz Tughlaq"
      }
    ],
    "correct": "A",
    "exp_hi": "निजामुद्दीन औलिया अलाउद्दीन खिलजी के समकालीन थे।",
    "exp_en": "Nizamuddin Auliya was contemporary of Alauddin Khilji.",
    "exam_tag": "SSC 2018",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "रणजीत सिंह ने सिख साम्राज्य की स्थापना कब की?",
    "q_en": "When did Ranjit Singh establish Sikh Empire?",
    "options": [
      {
        "letter": "A",
        "hi": "1799",
        "en": "1799"
      },
      {
        "letter": "B",
        "hi": "1801",
        "en": "1801"
      },
      {
        "letter": "C",
        "hi": "1805",
        "en": "1805"
      },
      {
        "letter": "D",
        "hi": "1810",
        "en": "1810"
      }
    ],
    "correct": "B",
    "exp_hi": "रणजीत सिंह ने 1801 में पंजाब में सिख साम्राज्य की स्थापना की।",
    "exp_en": "Ranjit Singh established Sikh Empire in Punjab in 1801.",
    "exam_tag": "SSC 2016",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "वेलूर विद्रोह कब हुआ?",
    "q_en": "When was Vellore Mutiny?",
    "options": [
      {
        "letter": "A",
        "hi": "1802",
        "en": "1802"
      },
      {
        "letter": "B",
        "hi": "1806",
        "en": "1806"
      },
      {
        "letter": "C",
        "hi": "1810",
        "en": "1810"
      },
      {
        "letter": "D",
        "hi": "1815",
        "en": "1815"
      }
    ],
    "correct": "B",
    "exp_hi": "वेलूर विद्रोह 1806 में हुआ।",
    "exp_en": "Vellore Mutiny happened in 1806.",
    "exam_tag": "Railway 2016",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "विधवा पुनर्विवाह आंदोलन किसने चलाया?",
    "q_en": "Who led widow remarriage movement?",
    "options": [
      {
        "letter": "A",
        "hi": "राजा राम मोहन राय",
        "en": "Raja Ram Mohan Roy"
      },
      {
        "letter": "B",
        "hi": "ईश्वरचंद्र विद्यासागर",
        "en": "Ishwarchandra Vidyasagar"
      },
      {
        "letter": "C",
        "hi": "दयानंद सरस्वती",
        "en": "Dayananda Saraswati"
      },
      {
        "letter": "D",
        "hi": "स्वामी विवेकानंद",
        "en": "Swami Vivekananda"
      }
    ],
    "correct": "B",
    "exp_hi": "ईश्वरचंद्र विद्यासागर ने विधवा पुनर्विवाह आंदोलन चलाया।",
    "exp_en": "Ishwarchandra Vidyasagar led widow remarriage movement.",
    "exam_tag": "CTET 2018",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "आर्य समाज की स्थापना किसने की?",
    "q_en": "Who founded Arya Samaj?",
    "options": [
      {
        "letter": "A",
        "hi": "राजा राम मोहन राय",
        "en": "Raja Ram Mohan Roy"
      },
      {
        "letter": "B",
        "hi": "स्वामी दयानंद सरस्वती",
        "en": "Swami Dayananda Saraswati"
      },
      {
        "letter": "C",
        "hi": "स्वामी विवेकानंद",
        "en": "Swami Vivekananda"
      },
      {
        "letter": "D",
        "hi": "रामकृष्ण परमहंस",
        "en": "Ramakrishna Paramhansa"
      }
    ],
    "correct": "B",
    "exp_hi": "आर्य समाज की स्थापना 1875 में स्वामी दयानंद सरस्वती ने की।",
    "exp_en": "Arya Samaj was founded by Swami Dayananda Saraswati in 1875.",
    "exam_tag": "SSC 2017",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "ब्रह्म समाज की स्थापना किसने की?",
    "q_en": "Who founded Brahmo Samaj?",
    "options": [
      {
        "letter": "A",
        "hi": "स्वामी विवेकानंद",
        "en": "Swami Vivekananda"
      },
      {
        "letter": "B",
        "hi": "राजा राम मोहन राय",
        "en": "Raja Ram Mohan Roy"
      },
      {
        "letter": "C",
        "hi": "दयानंद सरस्वती",
        "en": "Dayananda Saraswati"
      },
      {
        "letter": "D",
        "hi": "देवेंद्रनाथ टैगोर",
        "en": "Devendranath Tagore"
      }
    ],
    "correct": "B",
    "exp_hi": "ब्रह्म समाज की स्थापना 1828 में राजा राम मोहन राय ने की।",
    "exp_en": "Brahmo Samaj was founded by Raja Ram Mohan Roy in 1828.",
    "exam_tag": "UPSC 2015",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "वुड का घोषणापत्र (1854) किससे संबंधित था?",
    "q_en": "Wood's Despatch (1854) was related to?",
    "options": [
      {
        "letter": "A",
        "hi": "कृषि",
        "en": "Agriculture"
      },
      {
        "letter": "B",
        "hi": "शिक्षा",
        "en": "Education"
      },
      {
        "letter": "C",
        "hi": "व्यापार",
        "en": "Trade"
      },
      {
        "letter": "D",
        "hi": "सेना",
        "en": "Army"
      }
    ],
    "correct": "B",
    "exp_hi": "वुड का घोषणापत्र 1854 भारत में शिक्षा नीति से संबंधित था।",
    "exp_en": "Wood's Despatch 1854 was related to education policy in India.",
    "exam_tag": "UPSC 2016",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "इंडियन नेशनल एसोसिएशन की स्थापना किसने की?",
    "q_en": "Who founded Indian National Association?",
    "options": [
      {
        "letter": "A",
        "hi": "सुरेंद्रनाथ बनर्जी",
        "en": "Surendranath Banerjee"
      },
      {
        "letter": "B",
        "hi": "दादाभाई नौरोजी",
        "en": "Dadabhai Naoroji"
      },
      {
        "letter": "C",
        "hi": "ए.ओ. ह्यूम",
        "en": "A.O. Hume"
      },
      {
        "letter": "D",
        "hi": "फिरोजशाह मेहता",
        "en": "Pherozeshah Mehta"
      }
    ],
    "correct": "A",
    "exp_hi": "INA की स्थापना 1876 में सुरेंद्रनाथ बनर्जी ने की।",
    "exp_en": "INA was founded by Surendranath Banerjee in 1876.",
    "exam_tag": "SSC 2016",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "दिल्ली को भारत की राजधानी कब बनाया गया?",
    "q_en": "When was Delhi made India's capital?",
    "options": [
      {
        "letter": "A",
        "hi": "1905",
        "en": "1905"
      },
      {
        "letter": "B",
        "hi": "1911",
        "en": "1911"
      },
      {
        "letter": "C",
        "hi": "1920",
        "en": "1920"
      },
      {
        "letter": "D",
        "hi": "1947",
        "en": "1947"
      }
    ],
    "correct": "B",
    "exp_hi": "1911 में दिल्ली को भारत की राजधानी बनाया गया।",
    "exp_en": "Delhi was made India's capital in 1911.",
    "exam_tag": "Railway 2016",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "गांधीजी का चंपारण सत्याग्रह क्यों था?",
    "q_en": "What was Gandhiji's Champaran Satyagraha about?",
    "options": [
      {
        "letter": "A",
        "hi": "नमक कर",
        "en": "Salt tax"
      },
      {
        "letter": "B",
        "hi": "नील की खेती",
        "en": "Indigo cultivation"
      },
      {
        "letter": "C",
        "hi": "भूमि कर",
        "en": "Land tax"
      },
      {
        "letter": "D",
        "hi": "कपास कर",
        "en": "Cotton tax"
      }
    ],
    "correct": "B",
    "exp_hi": "चंपारण सत्याग्रह (1917) नील किसानों की समस्याओं के लिए था।",
    "exp_en": "Champaran Satyagraha (1917) was for problems of indigo farmers.",
    "exam_tag": "CTET 2019",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "खिलाफत आंदोलन कब शुरू हुआ?",
    "q_en": "When did Khilafat Movement start?",
    "options": [
      {
        "letter": "A",
        "hi": "1918",
        "en": "1918"
      },
      {
        "letter": "B",
        "hi": "1919",
        "en": "1919"
      },
      {
        "letter": "C",
        "hi": "1920",
        "en": "1920"
      },
      {
        "letter": "D",
        "hi": "1921",
        "en": "1921"
      }
    ],
    "correct": "C",
    "exp_hi": "खिलाफत आंदोलन 1920 में शुरू हुआ।",
    "exp_en": "Khilafat Movement started in 1920.",
    "exam_tag": "SSC 2016",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "भारतीय राष्ट्रीय कांग्रेस का विभाजन किस अधिवेशन में हुआ?",
    "q_en": "In which session did INC split?",
    "options": [
      {
        "letter": "A",
        "hi": "लखनऊ 1916",
        "en": "Lucknow 1916"
      },
      {
        "letter": "B",
        "hi": "कलकत्ता 1906",
        "en": "Calcutta 1906"
      },
      {
        "letter": "C",
        "hi": "सूरत 1907",
        "en": "Surat 1907"
      },
      {
        "letter": "D",
        "hi": "नागपुर 1920",
        "en": "Nagpur 1920"
      }
    ],
    "correct": "C",
    "exp_hi": "INC का विभाजन 1907 के सूरत अधिवेशन में हुआ।",
    "exp_en": "INC split at Surat session in 1907.",
    "exam_tag": "Railway 2017",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "साइमन कमीशन में कितने सदस्य थे?",
    "q_en": "How many members in Simon Commission?",
    "options": [
      {
        "letter": "A",
        "hi": "5",
        "en": "5"
      },
      {
        "letter": "B",
        "hi": "7",
        "en": "7"
      },
      {
        "letter": "C",
        "hi": "9",
        "en": "9"
      },
      {
        "letter": "D",
        "hi": "11",
        "en": "11"
      }
    ],
    "correct": "B",
    "exp_hi": "साइमन कमीशन में 7 ब्रिटिश सदस्य थे।",
    "exp_en": "Simon Commission had 7 British members.",
    "exam_tag": "SSC 2016",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "लाहौर षड्यंत्र केस किससे संबंधित था?",
    "q_en": "Lahore Conspiracy Case was related to?",
    "options": [
      {
        "letter": "A",
        "hi": "भगत सिंह",
        "en": "Bhagat Singh"
      },
      {
        "letter": "B",
        "hi": "चंद्रशेखर आजाद",
        "en": "Chandrashekhar Azad"
      },
      {
        "letter": "C",
        "hi": "सुखदेव",
        "en": "Sukhdev"
      },
      {
        "letter": "D",
        "hi": "भगत सिंह और साथी",
        "en": "Bhagat Singh and associates"
      }
    ],
    "correct": "D",
    "exp_hi": "लाहौर षड्यंत्र केस में भगत सिंह, राजगुरु और सुखदेव पर मुकदमा चला।",
    "exp_en": "Lahore Conspiracy Case involved Bhagat Singh, Rajguru and Sukhdev.",
    "exam_tag": "Railway 2016",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "नेहरू रिपोर्ट किस वर्ष प्रस्तुत की गई?",
    "q_en": "In which year was Nehru Report presented?",
    "options": [
      {
        "letter": "A",
        "hi": "1926",
        "en": "1926"
      },
      {
        "letter": "B",
        "hi": "1928",
        "en": "1928"
      },
      {
        "letter": "C",
        "hi": "1930",
        "en": "1930"
      },
      {
        "letter": "D",
        "hi": "1932",
        "en": "1932"
      }
    ],
    "correct": "B",
    "exp_hi": "नेहरू रिपोर्ट 1928 में प्रस्तुत की गई।",
    "exp_en": "Nehru Report was presented in 1928.",
    "exam_tag": "CTET 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "वेवेल योजना कब प्रस्तुत हुई?",
    "q_en": "When was Wavell Plan presented?",
    "options": [
      {
        "letter": "A",
        "hi": "1943",
        "en": "1943"
      },
      {
        "letter": "B",
        "hi": "1945",
        "en": "1945"
      },
      {
        "letter": "C",
        "hi": "1946",
        "en": "1946"
      },
      {
        "letter": "D",
        "hi": "1947",
        "en": "1947"
      }
    ],
    "correct": "B",
    "exp_hi": "वेवेल योजना 1945 में शिमला सम्मेलन में प्रस्तुत हुई।",
    "exp_en": "Wavell Plan was presented at Shimla Conference in 1945.",
    "exam_tag": "SSC 2016",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "संविधान सभा का गठन कब हुआ?",
    "q_en": "When was Constituent Assembly formed?",
    "options": [
      {
        "letter": "A",
        "hi": "1944",
        "en": "1944"
      },
      {
        "letter": "B",
        "hi": "1946",
        "en": "1946"
      },
      {
        "letter": "C",
        "hi": "1947",
        "en": "1947"
      },
      {
        "letter": "D",
        "hi": "1949",
        "en": "1949"
      }
    ],
    "correct": "B",
    "exp_hi": "संविधान सभा का गठन 1946 में कैबिनेट मिशन के तहत हुआ।",
    "exp_en": "Constituent Assembly was formed in 1946 under Cabinet Mission.",
    "exam_tag": "UPSC 2017",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "तेलंगाना राज्य कब बना?",
    "q_en": "When was Telangana state formed?",
    "options": [
      {
        "letter": "A",
        "hi": "2012",
        "en": "2012"
      },
      {
        "letter": "B",
        "hi": "2013",
        "en": "2013"
      },
      {
        "letter": "C",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "D",
        "hi": "2015",
        "en": "2015"
      }
    ],
    "correct": "C",
    "exp_hi": "तेलंगाना 2 जून 2014 को भारत का 29वाँ राज्य बना।",
    "exp_en": "Telangana became India's 29th state on 2 June 2014.",
    "exam_tag": "Railway 2017",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "भारत में पहला परमाणु रिएक्टर कहाँ स्थापित हुआ?",
    "q_en": "Where was India's first nuclear reactor?",
    "options": [
      {
        "letter": "A",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "B",
        "hi": "कोलकाता",
        "en": "Kolkata"
      },
      {
        "letter": "C",
        "hi": "दिल्ली",
        "en": "Delhi"
      },
      {
        "letter": "D",
        "hi": "चेन्नई",
        "en": "Chennai"
      }
    ],
    "correct": "A",
    "exp_hi": "भारत का पहला परमाणु रिएक्टर 'अप्सरा' 1956 में मुंबई (ट्रॉम्बे) में स्थापित हुआ।",
    "exp_en": "India's first nuclear reactor 'Apsara' was set up in Mumbai (Trombay) in 1956.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "history",
    "q_hi": "प्राचीन भारत का सबसे बड़ा नगर?",
    "q_en": "Largest city of ancient India?",
    "options": [
      {
        "letter": "A",
        "hi": "पाटलिपुत्र",
        "en": "Pataliputra"
      },
      {
        "letter": "B",
        "hi": "तक्षशिला",
        "en": "Taxila"
      },
      {
        "letter": "C",
        "hi": "मोहनजोदड़ो",
        "en": "Mohenjo-daro"
      },
      {
        "letter": "D",
        "hi": "उज्जैन",
        "en": "Ujjain"
      }
    ],
    "correct": "C",
    "exp_hi": "मोहनजोदड़ो प्राचीन भारत का सबसे बड़ा नगर था।",
    "exp_en": "Mohenjo-daro was the largest city of ancient India.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 6"
  },
  {
    "subject": "history",
    "q_hi": "अमीर खुसरो किस राजा के दरबार में थे?",
    "q_en": "Amir Khusro was in court of which king?",
    "options": [
      {
        "letter": "A",
        "hi": "अलाउद्दीन खिलजी",
        "en": "Alauddin Khilji"
      },
      {
        "letter": "B",
        "hi": "बलबन",
        "en": "Balban"
      },
      {
        "letter": "C",
        "hi": "इल्तुतमिश",
        "en": "Iltutmish"
      },
      {
        "letter": "D",
        "hi": "मुहम्मद बिन तुगलक",
        "en": "Muhammad bin Tughlaq"
      }
    ],
    "correct": "A",
    "exp_hi": "अमीर खुसरो अलाउद्दीन खिलजी के दरबारी कवि थे।",
    "exp_en": "Amir Khusro was the court poet of Alauddin Khilji.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 7"
  },
  {
    "subject": "history",
    "q_hi": "'वंदे मातरम' गीत किसने लिखा?",
    "q_en": "Who wrote 'Vande Mataram'?",
    "options": [
      {
        "letter": "A",
        "hi": "रवींद्रनाथ टैगोर",
        "en": "Rabindranath Tagore"
      },
      {
        "letter": "B",
        "hi": "बंकिमचंद्र चटर्जी",
        "en": "Bankimchandra Chaterjee"
      },
      {
        "letter": "C",
        "hi": "सुभाष चंद्र बोस",
        "en": "Subhas Chandra Bose"
      },
      {
        "letter": "D",
        "hi": "बिपिन चंद्र पाल",
        "en": "Bipin Chandra Pal"
      }
    ],
    "correct": "B",
    "exp_hi": "वंदे मातरम बंकिमचंद्र चटर्जी ने 1875 में लिखा।",
    "exp_en": "Vande Mataram was written by Bankimchandra Chaterjee in 1875.",
    "exam_tag": "Railway 2015",
    "class": "कक्षा 8"
  },
  {
    "subject": "history",
    "q_hi": "मॉर्ले-मिंटो सुधार कब हुए?",
    "q_en": "When were Morley-Minto reforms?",
    "options": [
      {
        "letter": "A",
        "hi": "1905",
        "en": "1905"
      },
      {
        "letter": "B",
        "hi": "1909",
        "en": "1909"
      },
      {
        "letter": "C",
        "hi": "1919",
        "en": "1919"
      },
      {
        "letter": "D",
        "hi": "1935",
        "en": "1935"
      }
    ],
    "correct": "B",
    "exp_hi": "मॉर्ले-मिंटो सुधार 1909 में हुए।",
    "exp_en": "Morley-Minto reforms were in 1909.",
    "exam_tag": "CTET 2018",
    "class": "कक्षा 9"
  },
  {
    "subject": "history",
    "q_hi": "अखिल भारतीय मुस्लिम लीग की स्थापना कब हुई?",
    "q_en": "When was All India Muslim League founded?",
    "options": [
      {
        "letter": "A",
        "hi": "1904",
        "en": "1904"
      },
      {
        "letter": "B",
        "hi": "1906",
        "en": "1906"
      },
      {
        "letter": "C",
        "hi": "1910",
        "en": "1910"
      },
      {
        "letter": "D",
        "hi": "1916",
        "en": "1916"
      }
    ],
    "correct": "B",
    "exp_hi": "मुस्लिम लीग की स्थापना 1906 में ढाका में हुई।",
    "exp_en": "Muslim League was founded in Dhaka in 1906.",
    "exam_tag": "UPSC 2017",
    "class": "कक्षा 10"
  },
  {
    "subject": "history",
    "q_hi": "स्वराज पार्टी की स्थापना किसने की?",
    "q_en": "Who founded Swaraj Party?",
    "options": [
      {
        "letter": "A",
        "hi": "गांधीजी",
        "en": "Gandhiji"
      },
      {
        "letter": "B",
        "hi": "मोतीलाल नेहरू और चित्तरंजन दास",
        "en": "Motilal Nehru and CR Das"
      },
      {
        "letter": "C",
        "hi": "तिलक",
        "en": "Tilak"
      },
      {
        "letter": "D",
        "hi": "गोखले",
        "en": "Gokhale"
      }
    ],
    "correct": "B",
    "exp_hi": "स्वराज पार्टी 1923 में मोतीलाल नेहरू और चित्तरंजन दास ने बनाई।",
    "exp_en": "Swaraj Party was formed by Motilal Nehru and CR Das in 1923.",
    "exam_tag": "SSC 2015",
    "class": "कक्षा 11"
  },
  {
    "subject": "history",
    "q_hi": "भारत-पाक प्रथम युद्ध कब हुआ?",
    "q_en": "When was First India-Pakistan war?",
    "options": [
      {
        "letter": "A",
        "hi": "1947",
        "en": "1947"
      },
      {
        "letter": "B",
        "hi": "1948",
        "en": "1948"
      },
      {
        "letter": "C",
        "hi": "1950",
        "en": "1950"
      },
      {
        "letter": "D",
        "hi": "1962",
        "en": "1962"
      }
    ],
    "correct": "A",
    "exp_hi": "पहला भारत-पाकिस्तान युद्ध 1947 में हुआ।",
    "exp_en": "First India-Pakistan war was in 1947.",
    "exam_tag": "Railway 2015",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत की सबसे लंबी नदी कौन सी है?",
    "q_en": "Longest river in India?",
    "options": [
      {
        "letter": "A",
        "hi": "गंगा",
        "en": "Ganga"
      },
      {
        "letter": "B",
        "hi": "गोदावरी",
        "en": "Godavari"
      },
      {
        "letter": "C",
        "hi": "यमुना",
        "en": "Yamuna"
      },
      {
        "letter": "D",
        "hi": "सिंधु",
        "en": "Indus"
      }
    ],
    "correct": "A",
    "exp_hi": "गंगा 2525 km के साथ भारत की सबसे लंबी नदी है।",
    "exp_en": "Ganga at 2525 km is India's longest river.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे बड़ा राज्य कौन सा है?",
    "q_en": "Largest state of India by area?",
    "options": [
      {
        "letter": "A",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      },
      {
        "letter": "B",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      },
      {
        "letter": "C",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "D",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      }
    ],
    "correct": "C",
    "exp_hi": "राजस्थान क्षेत्रफल में भारत का सबसे बड़ा राज्य है।",
    "exp_en": "Rajasthan is India's largest state by area.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में कुल कितने राज्य हैं?",
    "q_en": "How many states in India?",
    "options": [
      {
        "letter": "A",
        "hi": "28",
        "en": "28"
      },
      {
        "letter": "B",
        "hi": "29",
        "en": "29"
      },
      {
        "letter": "C",
        "hi": "27",
        "en": "27"
      },
      {
        "letter": "D",
        "hi": "30",
        "en": "30"
      }
    ],
    "correct": "A",
    "exp_hi": "भारत में 28 राज्य और 8 केंद्र शासित प्रदेश हैं।",
    "exp_en": "India has 28 states and 8 Union Territories.",
    "exam_tag": "CTET 2019",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे छोटा राज्य कौन सा है?",
    "q_en": "Smallest state of India?",
    "options": [
      {
        "letter": "A",
        "hi": "गोवा",
        "en": "Goa"
      },
      {
        "letter": "B",
        "hi": "सिक्किम",
        "en": "Sikkim"
      },
      {
        "letter": "C",
        "hi": "त्रिपुरा",
        "en": "Tripura"
      },
      {
        "letter": "D",
        "hi": "मणिपुर",
        "en": "Manipur"
      }
    ],
    "correct": "A",
    "exp_hi": "गोवा क्षेत्रफल में भारत का सबसे छोटा राज्य है।",
    "exp_en": "Goa is India's smallest state by area.",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत की राजधानी कौन सी है?",
    "q_en": "Capital of India?",
    "options": [
      {
        "letter": "A",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "B",
        "hi": "नई दिल्ली",
        "en": "New Delhi"
      },
      {
        "letter": "C",
        "hi": "कोलकाता",
        "en": "Kolkata"
      },
      {
        "letter": "D",
        "hi": "चेन्नई",
        "en": "Chennai"
      }
    ],
    "correct": "B",
    "exp_hi": "नई दिल्ली भारत की राजधानी है।",
    "exp_en": "New Delhi is the capital of India.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत की सबसे बड़ी मीठे पानी की झील?",
    "q_en": "Largest freshwater lake of India?",
    "options": [
      {
        "letter": "A",
        "hi": "डल झील",
        "en": "Dal Lake"
      },
      {
        "letter": "B",
        "hi": "वुलर झील",
        "en": "Wular Lake"
      },
      {
        "letter": "C",
        "hi": "चिल्का झील",
        "en": "Chilika Lake"
      },
      {
        "letter": "D",
        "hi": "सांभर झील",
        "en": "Sambhar Lake"
      }
    ],
    "correct": "B",
    "exp_hi": "वुलर झील भारत की सबसे बड़ी मीठे पानी की झील है।",
    "exp_en": "Wular Lake is India's largest freshwater lake.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का राष्ट्रीय जलीय प्राणी कौन सा है?",
    "q_en": "National aquatic animal of India?",
    "options": [
      {
        "letter": "A",
        "hi": "मगरमच्छ",
        "en": "Crocodile"
      },
      {
        "letter": "B",
        "hi": "गंगा डॉल्फिन",
        "en": "Gangetic Dolphin"
      },
      {
        "letter": "C",
        "hi": "कछुआ",
        "en": "Turtle"
      },
      {
        "letter": "D",
        "hi": "घड़ियाल",
        "en": "Gharial"
      }
    ],
    "correct": "B",
    "exp_hi": "गंगा डॉल्फिन भारत का राष्ट्रीय जलीय प्राणी है।",
    "exp_en": "Gangetic Dolphin is India's national aquatic animal.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का क्षेत्रफल कितना है?",
    "q_en": "Area of India?",
    "options": [
      {
        "letter": "A",
        "hi": "2.9 मिलियन वर्ग km",
        "en": "2.9 million sq km"
      },
      {
        "letter": "B",
        "hi": "3.28 मिलियन वर्ग km",
        "en": "3.28 million sq km"
      },
      {
        "letter": "C",
        "hi": "3.5 मिलियन वर्ग km",
        "en": "3.5 million sq km"
      },
      {
        "letter": "D",
        "hi": "2.5 मिलियन वर्ग km",
        "en": "2.5 million sq km"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत का क्षेत्रफल 3.28 मिलियन वर्ग km है।",
    "exp_en": "India's area is 3.28 million sq km.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "कर्क रेखा भारत के कितने राज्यों से गुजरती है?",
    "q_en": "Tropic of Cancer passes through how many Indian states?",
    "options": [
      {
        "letter": "A",
        "hi": "6",
        "en": "6"
      },
      {
        "letter": "B",
        "hi": "7",
        "en": "7"
      },
      {
        "letter": "C",
        "hi": "8",
        "en": "8"
      },
      {
        "letter": "D",
        "hi": "9",
        "en": "9"
      }
    ],
    "correct": "C",
    "exp_hi": "कर्क रेखा भारत के 8 राज्यों से गुजरती है।",
    "exp_en": "Tropic of Cancer passes through 8 Indian states.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का राष्ट्रीय पक्षी कौन सा है?",
    "q_en": "National bird of India?",
    "options": [
      {
        "letter": "A",
        "hi": "हंस",
        "en": "Swan"
      },
      {
        "letter": "B",
        "hi": "मोर",
        "en": "Peacock"
      },
      {
        "letter": "C",
        "hi": "तोता",
        "en": "Parrot"
      },
      {
        "letter": "D",
        "hi": "बाज",
        "en": "Eagle"
      }
    ],
    "correct": "B",
    "exp_hi": "मोर भारत का राष्ट्रीय पक्षी है।",
    "exp_en": "Peacock is India's national bird.",
    "exam_tag": "CTET 2021",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का राष्ट्रीय पशु कौन सा है?",
    "q_en": "National animal of India?",
    "options": [
      {
        "letter": "A",
        "hi": "शेर",
        "en": "Lion"
      },
      {
        "letter": "B",
        "hi": "हाथी",
        "en": "Elephant"
      },
      {
        "letter": "C",
        "hi": "बाघ",
        "en": "Tiger"
      },
      {
        "letter": "D",
        "hi": "गाय",
        "en": "Cow"
      }
    ],
    "correct": "C",
    "exp_hi": "बाघ (Royal Bengal Tiger) भारत का राष्ट्रीय पशु है।",
    "exp_en": "Tiger (Royal Bengal Tiger) is India's national animal.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे बड़ा द्वीप कौन सा है?",
    "q_en": "Largest island of India?",
    "options": [
      {
        "letter": "A",
        "hi": "अंडमान",
        "en": "Andaman"
      },
      {
        "letter": "B",
        "hi": "निकोबार",
        "en": "Nicobar"
      },
      {
        "letter": "C",
        "hi": "मिडल अंडमान",
        "en": "Middle Andaman"
      },
      {
        "letter": "D",
        "hi": "लक्षद्वीप",
        "en": "Lakshadweep"
      }
    ],
    "correct": "C",
    "exp_hi": "मिडल अंडमान भारत का सबसे बड़ा द्वीप है।",
    "exp_en": "Middle Andaman is India's largest island.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे पूर्वी बिंदु कहाँ है?",
    "q_en": "Easternmost point of India?",
    "options": [
      {
        "letter": "A",
        "hi": "किबिथू",
        "en": "Kibithu"
      },
      {
        "letter": "B",
        "hi": "इंदिरा पॉइंट",
        "en": "Indira Point"
      },
      {
        "letter": "C",
        "hi": "रनघाट",
        "en": "Ranaghat"
      },
      {
        "letter": "D",
        "hi": "गुहार मोती",
        "en": "Guhar Moti"
      }
    ],
    "correct": "A",
    "exp_hi": "किबिथू भारत का सबसे पूर्वी बिंदु है।",
    "exp_en": "Kibithu is India's easternmost point.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे दक्षिणी बिंदु कौन सा है?",
    "q_en": "Southernmost point of India?",
    "options": [
      {
        "letter": "A",
        "hi": "कन्याकुमारी",
        "en": "Kanyakumari"
      },
      {
        "letter": "B",
        "hi": "इंदिरा पॉइंट",
        "en": "Indira Point"
      },
      {
        "letter": "C",
        "hi": "रामेश्वरम",
        "en": "Rameswaram"
      },
      {
        "letter": "D",
        "hi": "पम्बन",
        "en": "Pamban"
      }
    ],
    "correct": "B",
    "exp_hi": "इंदिरा पॉइंट (अंडमान) भारत का सबसे दक्षिणी बिंदु है।",
    "exp_en": "Indira Point (Andaman) is India's southernmost point.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे अधिक वर्षा कहाँ होती है?",
    "q_en": "Highest rainfall in India?",
    "options": [
      {
        "letter": "A",
        "hi": "चेरापूंजी",
        "en": "Cherrapunji"
      },
      {
        "letter": "B",
        "hi": "मासिनराम",
        "en": "Mawsynram"
      },
      {
        "letter": "C",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "D",
        "hi": "कोलकाता",
        "en": "Kolkata"
      }
    ],
    "correct": "B",
    "exp_hi": "मासिनराम विश्व में सर्वाधिक वर्षा वाला स्थान है।",
    "exp_en": "Mawsynram receives highest rainfall in world.",
    "exam_tag": "UPSC 2018",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "भारत की सबसे लंबी तटरेखा किस राज्य की है?",
    "q_en": "State with longest coastline?",
    "options": [
      {
        "letter": "A",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "B",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      },
      {
        "letter": "C",
        "hi": "गुजरात",
        "en": "Gujarat"
      },
      {
        "letter": "D",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      }
    ],
    "correct": "C",
    "exp_hi": "गुजरात की तटरेखा 1600 km सबसे लंबी है।",
    "exp_en": "Gujarat has longest coastline of 1600 km.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "थार मरुस्थल किस राज्य में है?",
    "q_en": "Thar Desert is in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "गुजरात",
        "en": "Gujarat"
      },
      {
        "letter": "B",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "C",
        "hi": "हरियाणा",
        "en": "Haryana"
      },
      {
        "letter": "D",
        "hi": "पंजाब",
        "en": "Punjab"
      }
    ],
    "correct": "B",
    "exp_hi": "थार मरुस्थल मुख्यतः राजस्थान में है।",
    "exp_en": "Thar Desert is mainly in Rajasthan.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "हिमालय की सबसे ऊँची चोटी?",
    "q_en": "Highest peak of Himalayas?",
    "options": [
      {
        "letter": "A",
        "hi": "K2",
        "en": "K2"
      },
      {
        "letter": "B",
        "hi": "माउंट एवरेस्ट",
        "en": "Mount Everest"
      },
      {
        "letter": "C",
        "hi": "कंचनजंगा",
        "en": "Kanchenjunga"
      },
      {
        "letter": "D",
        "hi": "नंगा पर्बत",
        "en": "Nanga Parbat"
      }
    ],
    "correct": "B",
    "exp_hi": "माउंट एवरेस्ट 8848 मीटर सबसे ऊँची चोटी है।",
    "exp_en": "Mount Everest at 8848m is highest peak.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे ऊँचा जलप्रपात कौन सा है?",
    "q_en": "Highest waterfall in India?",
    "options": [
      {
        "letter": "A",
        "hi": "जोग जलप्रपात",
        "en": "Jog Falls"
      },
      {
        "letter": "B",
        "hi": "दूधसागर जलप्रपात",
        "en": "Dudhsagar Falls"
      },
      {
        "letter": "C",
        "hi": "कुंचिकल जलप्रपात",
        "en": "Kunchikal Falls"
      },
      {
        "letter": "D",
        "hi": "नोहकलिकाई जलप्रपात",
        "en": "Nohkalikai Falls"
      }
    ],
    "correct": "C",
    "exp_hi": "कुंचिकल जलप्रपात (455 m) भारत का सबसे ऊँचा है।",
    "exp_en": "Kunchikal Falls (455 m) is India's highest waterfall.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "चिल्का झील किस राज्य में है?",
    "q_en": "Chilika Lake is in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      },
      {
        "letter": "B",
        "hi": "ओडिशा",
        "en": "Odisha"
      },
      {
        "letter": "C",
        "hi": "पश्चिम बंगाल",
        "en": "West Bengal"
      },
      {
        "letter": "D",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      }
    ],
    "correct": "B",
    "exp_hi": "चिल्का झील ओडिशा में है और यह भारत की सबसे बड़ी तटीय झील है।",
    "exp_en": "Chilika Lake is in Odisha and is India's largest coastal lake.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "गोदावरी नदी का उद्गम कहाँ है?",
    "q_en": "Origin of Godavari river?",
    "options": [
      {
        "letter": "A",
        "hi": "त्र्यंबकेश्वर",
        "en": "Trimbakeshwar"
      },
      {
        "letter": "B",
        "hi": "महाबलेश्वर",
        "en": "Mahabaleshwar"
      },
      {
        "letter": "C",
        "hi": "नासिक",
        "en": "Nasik"
      },
      {
        "letter": "D",
        "hi": "पुणे",
        "en": "Pune"
      }
    ],
    "correct": "A",
    "exp_hi": "गोदावरी नासिक जिले के त्र्यंबकेश्वर से निकलती है।",
    "exp_en": "Godavari originates from Trimbakeshwar in Nasik district.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "अरावली पर्वत किस राज्य में है?",
    "q_en": "Aravalli mountain is in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "गुजरात",
        "en": "Gujarat"
      },
      {
        "letter": "B",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "C",
        "hi": "हरियाणा",
        "en": "Haryana"
      },
      {
        "letter": "D",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      }
    ],
    "correct": "B",
    "exp_hi": "अरावली पर्वत मुख्यतः राजस्थान में है।",
    "exp_en": "Aravalli mountain is mainly in Rajasthan.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "पश्चिमी घाट को और क्या कहते हैं?",
    "q_en": "Western Ghats are also known as?",
    "options": [
      {
        "letter": "A",
        "hi": "विंध्याचल",
        "en": "Vindhyas"
      },
      {
        "letter": "B",
        "hi": "सह्याद्री",
        "en": "Sahyadri"
      },
      {
        "letter": "C",
        "hi": "नीलगिरि",
        "en": "Nilgiris"
      },
      {
        "letter": "D",
        "hi": "अन्नामलाई",
        "en": "Anaimalai"
      }
    ],
    "correct": "B",
    "exp_hi": "पश्चिमी घाट को सह्याद्री पर्वत भी कहते हैं।",
    "exp_en": "Western Ghats are also called Sahyadri mountains.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "भारत की कौन सी नदी 'वृद्ध गंगा' कहलाती है?",
    "q_en": "Which Indian river is called 'Vriddha Ganga'?",
    "options": [
      {
        "letter": "A",
        "hi": "यमुना",
        "en": "Yamuna"
      },
      {
        "letter": "B",
        "hi": "कृष्णा",
        "en": "Krishna"
      },
      {
        "letter": "C",
        "hi": "गोदावरी",
        "en": "Godavari"
      },
      {
        "letter": "D",
        "hi": "कावेरी",
        "en": "Kaveri"
      }
    ],
    "correct": "C",
    "exp_hi": "गोदावरी को वृद्ध गंगा और दक्षिण गंगा भी कहते हैं।",
    "exp_en": "Godavari is also called Vriddha Ganga and Dakshina Ganga.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे बड़ा मैंग्रोव वन कौन सा है?",
    "q_en": "Largest mangrove forest in India?",
    "options": [
      {
        "letter": "A",
        "hi": "भितरकनिका",
        "en": "Bhitarkanika"
      },
      {
        "letter": "B",
        "hi": "सुंदरबन",
        "en": "Sundarbans"
      },
      {
        "letter": "C",
        "hi": "पिचावरम",
        "en": "Pichavaram"
      },
      {
        "letter": "D",
        "hi": "गोवा वन",
        "en": "Goa Forest"
      }
    ],
    "correct": "B",
    "exp_hi": "सुंदरबन विश्व का सबसे बड़ा मैंग्रोव वन है।",
    "exp_en": "Sundarbans is the world's largest mangrove forest.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे ऊँचा बाँध कौन सा है?",
    "q_en": "Highest dam of India?",
    "options": [
      {
        "letter": "A",
        "hi": "भाखड़ा नांगल",
        "en": "Bhakra Nangal"
      },
      {
        "letter": "B",
        "hi": "टिहरी",
        "en": "Tehri"
      },
      {
        "letter": "C",
        "hi": "हीराकुड",
        "en": "Hirakud"
      },
      {
        "letter": "D",
        "hi": "नागार्जुन सागर",
        "en": "Nagarjuna Sagar"
      }
    ],
    "correct": "B",
    "exp_hi": "टिहरी बाँध (260.5 m) भारत का सबसे ऊँचा बाँध है।",
    "exp_en": "Tehri Dam (260.5 m) is India's tallest dam.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "काली मिट्टी किस फसल के लिए उपयुक्त है?",
    "q_en": "Black soil suitable for which crop?",
    "options": [
      {
        "letter": "A",
        "hi": "चावल",
        "en": "Rice"
      },
      {
        "letter": "B",
        "hi": "कपास",
        "en": "Cotton"
      },
      {
        "letter": "C",
        "hi": "गेहूँ",
        "en": "Wheat"
      },
      {
        "letter": "D",
        "hi": "चाय",
        "en": "Tea"
      }
    ],
    "correct": "B",
    "exp_hi": "काली मिट्टी कपास के लिए सबसे उपयुक्त है।",
    "exp_en": "Black soil is most suitable for cotton.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सर्वाधिक चावल कहाँ उगाया जाता है?",
    "q_en": "Maximum rice production in India?",
    "options": [
      {
        "letter": "A",
        "hi": "पंजाब",
        "en": "Punjab"
      },
      {
        "letter": "B",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "C",
        "hi": "पश्चिम बंगाल",
        "en": "West Bengal"
      },
      {
        "letter": "D",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      }
    ],
    "correct": "C",
    "exp_hi": "पश्चिम बंगाल भारत में सर्वाधिक चावल उत्पादन करता है।",
    "exp_en": "West Bengal produces maximum rice in India.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "दक्कन पठार की सबसे महत्वपूर्ण फसल?",
    "q_en": "Most important crop of Deccan Plateau?",
    "options": [
      {
        "letter": "A",
        "hi": "गेहूँ",
        "en": "Wheat"
      },
      {
        "letter": "B",
        "hi": "कपास",
        "en": "Cotton"
      },
      {
        "letter": "C",
        "hi": "चावल",
        "en": "Rice"
      },
      {
        "letter": "D",
        "hi": "मक्का",
        "en": "Maize"
      }
    ],
    "correct": "B",
    "exp_hi": "दक्कन पठार की काली मिट्टी कपास के लिए प्रसिद्ध है।",
    "exp_en": "Deccan Plateau's black soil is famous for cotton.",
    "exam_tag": "UPSC 2019",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "भारत की सबसे ऊँची पर्वत चोटी?",
    "q_en": "Highest mountain peak in India?",
    "options": [
      {
        "letter": "A",
        "hi": "नंदा देवी",
        "en": "Nanda Devi"
      },
      {
        "letter": "B",
        "hi": "कंचनजंगा",
        "en": "Kanchenjunga"
      },
      {
        "letter": "C",
        "hi": "K2",
        "en": "K2"
      },
      {
        "letter": "D",
        "hi": "नंगा पर्बत",
        "en": "Nanga Parbat"
      }
    ],
    "correct": "B",
    "exp_hi": "कंचनजंगा (8586 m) भारत की सबसे ऊँची चोटी है।",
    "exp_en": "Kanchenjunga (8586 m) is India's highest peak.",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "गंगा नदी कहाँ से निकलती है?",
    "q_en": "Where does Ganga originate?",
    "options": [
      {
        "letter": "A",
        "hi": "मानसरोवर",
        "en": "Mansarovar"
      },
      {
        "letter": "B",
        "hi": "गंगोत्री",
        "en": "Gangotri"
      },
      {
        "letter": "C",
        "hi": "यमुनोत्री",
        "en": "Yamunotri"
      },
      {
        "letter": "D",
        "hi": "केदारनाथ",
        "en": "Kedarnath"
      }
    ],
    "correct": "B",
    "exp_hi": "गंगा गंगोत्री ग्लेशियर से निकलती है।",
    "exp_en": "Ganga originates from Gangotri glacier.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "कृष्णा नदी का उद्गम कहाँ है?",
    "q_en": "Origin of Krishna river?",
    "options": [
      {
        "letter": "A",
        "hi": "महाबलेश्वर",
        "en": "Mahabaleshwar"
      },
      {
        "letter": "B",
        "hi": "नासिक",
        "en": "Nasik"
      },
      {
        "letter": "C",
        "hi": "पुणे",
        "en": "Pune"
      },
      {
        "letter": "D",
        "hi": "हम्पी",
        "en": "Hampi"
      }
    ],
    "correct": "A",
    "exp_hi": "कृष्णा नदी महाराष्ट्र के महाबलेश्वर से निकलती है।",
    "exp_en": "Krishna river originates from Mahabaleshwar in Maharashtra.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में लैटेराइट मिट्टी कहाँ पाई जाती है?",
    "q_en": "Where is laterite soil found in India?",
    "options": [
      {
        "letter": "A",
        "hi": "पंजाब",
        "en": "Punjab"
      },
      {
        "letter": "B",
        "hi": "केरल और कर्नाटक",
        "en": "Kerala and Karnataka"
      },
      {
        "letter": "C",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "D",
        "hi": "गुजरात",
        "en": "Gujarat"
      }
    ],
    "correct": "B",
    "exp_hi": "लैटेराइट मिट्टी केरल और कर्नाटक में पाई जाती है।",
    "exp_en": "Laterite soil is found in Kerala and Karnataka.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में चाय की खेती सबसे अधिक कहाँ होती है?",
    "q_en": "Maximum tea cultivation in India?",
    "options": [
      {
        "letter": "A",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "B",
        "hi": "असम",
        "en": "Assam"
      },
      {
        "letter": "C",
        "hi": "पश्चिम बंगाल",
        "en": "West Bengal"
      },
      {
        "letter": "D",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      }
    ],
    "correct": "B",
    "exp_hi": "असम भारत का सबसे बड़ा चाय उत्पादक राज्य है।",
    "exp_en": "Assam is India's largest tea producing state.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सर्वाधिक गेहूँ कहाँ उगाया जाता है?",
    "q_en": "Maximum wheat production in India?",
    "options": [
      {
        "letter": "A",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      },
      {
        "letter": "B",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "C",
        "hi": "पंजाब",
        "en": "Punjab"
      },
      {
        "letter": "D",
        "hi": "हरियाणा",
        "en": "Haryana"
      }
    ],
    "correct": "B",
    "exp_hi": "उत्तर प्रदेश सर्वाधिक गेहूँ उत्पादन करता है।",
    "exp_en": "Uttar Pradesh produces maximum wheat.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "लाल मिट्टी कहाँ पाई जाती है?",
    "q_en": "Where is red soil found?",
    "options": [
      {
        "letter": "A",
        "hi": "पंजाब",
        "en": "Punjab"
      },
      {
        "letter": "B",
        "hi": "गुजरात",
        "en": "Gujarat"
      },
      {
        "letter": "C",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      },
      {
        "letter": "D",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      }
    ],
    "correct": "C",
    "exp_hi": "लाल मिट्टी मुख्यतः तमिलनाडु और तेलंगाना में पाई जाती है।",
    "exp_en": "Red soil is mainly found in Tamil Nadu and Telangana.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे अधिक वन किस राज्य में हैं?",
    "q_en": "State with most forests in India?",
    "options": [
      {
        "letter": "A",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      },
      {
        "letter": "B",
        "hi": "अरुणाचल प्रदेश",
        "en": "Arunachal Pradesh"
      },
      {
        "letter": "C",
        "hi": "छत्तीसगढ़",
        "en": "Chhattisgarh"
      },
      {
        "letter": "D",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      }
    ],
    "correct": "A",
    "exp_hi": "मध्य प्रदेश में सर्वाधिक वन क्षेत्र है।",
    "exp_en": "Madhya Pradesh has maximum forest area.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "कावेरी नदी किस राज्य में नहीं बहती?",
    "q_en": "Kaveri river does NOT flow through which state?",
    "options": [
      {
        "letter": "A",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "B",
        "hi": "कर्नाटक",
        "en": "Karnataka"
      },
      {
        "letter": "C",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      },
      {
        "letter": "D",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      }
    ],
    "correct": "D",
    "exp_hi": "कावेरी केरल, कर्नाटक और तमिलनाडु से बहती है।",
    "exp_en": "Kaveri flows through Kerala, Karnataka and Tamil Nadu.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में मानसून कब आता है?",
    "q_en": "When does monsoon arrive in India?",
    "options": [
      {
        "letter": "A",
        "hi": "मार्च-अप्रैल",
        "en": "March-April"
      },
      {
        "letter": "B",
        "hi": "मई-जून",
        "en": "May-June"
      },
      {
        "letter": "C",
        "hi": "जून-जुलाई",
        "en": "June-July"
      },
      {
        "letter": "D",
        "hi": "अगस्त-सितंबर",
        "en": "August-September"
      }
    ],
    "correct": "C",
    "exp_hi": "दक्षिण-पश्चिमी मानसून जून में केरल पहुँचता है।",
    "exp_en": "South-West monsoon arrives in Kerala in June.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "जनसंख्या में सबसे बड़ा राज्य?",
    "q_en": "Most populous state of India?",
    "options": [
      {
        "letter": "A",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      },
      {
        "letter": "B",
        "hi": "बिहार",
        "en": "Bihar"
      },
      {
        "letter": "C",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "D",
        "hi": "पश्चिम बंगाल",
        "en": "West Bengal"
      }
    ],
    "correct": "C",
    "exp_hi": "उत्तर प्रदेश जनसंख्या में भारत का सबसे बड़ा राज्य है।",
    "exp_en": "Uttar Pradesh is India's most populous state.",
    "exam_tag": "UPSC 2019",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे बड़ा बंदरगाह?",
    "q_en": "Largest port of India?",
    "options": [
      {
        "letter": "A",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "B",
        "hi": "कोलकाता",
        "en": "Kolkata"
      },
      {
        "letter": "C",
        "hi": "चेन्नई",
        "en": "Chennai"
      },
      {
        "letter": "D",
        "hi": "कांडला",
        "en": "Kandla"
      }
    ],
    "correct": "A",
    "exp_hi": "मुंबई भारत का सबसे बड़ा बंदरगाह है।",
    "exp_en": "Mumbai is India's largest port.",
    "exam_tag": "SSC 2018",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "सुंदरबन कहाँ स्थित है?",
    "q_en": "Where is Sundarbans?",
    "options": [
      {
        "letter": "A",
        "hi": "ओडिशा",
        "en": "Odisha"
      },
      {
        "letter": "B",
        "hi": "पश्चिम बंगाल",
        "en": "West Bengal"
      },
      {
        "letter": "C",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      },
      {
        "letter": "D",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      }
    ],
    "correct": "B",
    "exp_hi": "सुंदरबन पश्चिम बंगाल में है।",
    "exp_en": "Sundarbans is in West Bengal.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे लंबा राष्ट्रीय राजमार्ग?",
    "q_en": "Longest National Highway in India?",
    "options": [
      {
        "letter": "A",
        "hi": "NH 44",
        "en": "NH 44"
      },
      {
        "letter": "B",
        "hi": "NH 27",
        "en": "NH 27"
      },
      {
        "letter": "C",
        "hi": "NH 48",
        "en": "NH 48"
      },
      {
        "letter": "D",
        "hi": "NH 52",
        "en": "NH 52"
      }
    ],
    "correct": "A",
    "exp_hi": "NH 44 (3745 km) भारत का सबसे लंबा राजमार्ग है।",
    "exp_en": "NH 44 (3745 km) is India's longest National Highway.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे बड़ा रेगिस्तान?",
    "q_en": "Largest desert of India?",
    "options": [
      {
        "letter": "A",
        "hi": "थार",
        "en": "Thar"
      },
      {
        "letter": "B",
        "hi": "लद्दाख",
        "en": "Ladakh"
      },
      {
        "letter": "C",
        "hi": "कच्छ",
        "en": "Kutch"
      },
      {
        "letter": "D",
        "hi": "स्पीति",
        "en": "Spiti"
      }
    ],
    "correct": "A",
    "exp_hi": "थार मरुस्थल भारत का सबसे बड़ा रेगिस्तान है।",
    "exp_en": "Thar Desert is India's largest desert.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में कुल केंद्र शासित प्रदेश कितने हैं?",
    "q_en": "How many Union Territories in India?",
    "options": [
      {
        "letter": "A",
        "hi": "6",
        "en": "6"
      },
      {
        "letter": "B",
        "hi": "7",
        "en": "7"
      },
      {
        "letter": "C",
        "hi": "8",
        "en": "8"
      },
      {
        "letter": "D",
        "hi": "9",
        "en": "9"
      }
    ],
    "correct": "C",
    "exp_hi": "भारत में 8 केंद्र शासित प्रदेश हैं।",
    "exp_en": "India has 8 Union Territories.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "नर्मदा नदी कहाँ गिरती है?",
    "q_en": "Where does Narmada river flow into?",
    "options": [
      {
        "letter": "A",
        "hi": "बंगाल की खाड़ी",
        "en": "Bay of Bengal"
      },
      {
        "letter": "B",
        "hi": "अरब सागर",
        "en": "Arabian Sea"
      },
      {
        "letter": "C",
        "hi": "हिंद महासागर",
        "en": "Indian Ocean"
      },
      {
        "letter": "D",
        "hi": "कच्छ की खाड़ी",
        "en": "Gulf of Kutch"
      }
    ],
    "correct": "B",
    "exp_hi": "नर्मदा नदी अरब सागर में गिरती है।",
    "exp_en": "Narmada river flows into the Arabian Sea.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में हरित क्रांति का जनक?",
    "q_en": "Father of Green Revolution in India?",
    "options": [
      {
        "letter": "A",
        "hi": "वर्गीज कुरियन",
        "en": "Verghese Kurien"
      },
      {
        "letter": "B",
        "hi": "एम.एस. स्वामीनाथन",
        "en": "M.S. Swaminathan"
      },
      {
        "letter": "C",
        "hi": "नॉर्मन बोरलॉग",
        "en": "Norman Borlaug"
      },
      {
        "letter": "D",
        "hi": "सी. सुब्रमण्यम",
        "en": "C. Subramaniam"
      }
    ],
    "correct": "B",
    "exp_hi": "एम.एस. स्वामीनाथन को भारत में हरित क्रांति का जनक कहते हैं।",
    "exp_en": "M.S. Swaminathan is father of Green Revolution in India.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का कौन सा राज्य तीन ओर से समुद्र से घिरा है?",
    "q_en": "Indian state surrounded by sea on three sides?",
    "options": [
      {
        "letter": "A",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "B",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      },
      {
        "letter": "C",
        "hi": "गुजरात",
        "en": "Gujarat"
      },
      {
        "letter": "D",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      }
    ],
    "correct": "B",
    "exp_hi": "तमिलनाडु तीन ओर से समुद्र से घिरा है।",
    "exp_en": "Tamil Nadu is surrounded by sea on three sides.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "ब्रह्मपुत्र नदी कहाँ से निकलती है?",
    "q_en": "Where does Brahmaputra originate?",
    "options": [
      {
        "letter": "A",
        "hi": "हिमालय",
        "en": "Himalayas"
      },
      {
        "letter": "B",
        "hi": "तिब्बत के मानसरोवर पास",
        "en": "Near Mansarovar in Tibet"
      },
      {
        "letter": "C",
        "hi": "अरुणाचल",
        "en": "Arunachal"
      },
      {
        "letter": "D",
        "hi": "असम",
        "en": "Assam"
      }
    ],
    "correct": "B",
    "exp_hi": "ब्रह्मपुत्र तिब्बत के मानसरोवर झील के पास से निकलती है।",
    "exp_en": "Brahmaputra originates near Mansarovar lake in Tibet.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "कौन सा राज्य सबसे अधिक अंतरराष्ट्रीय सीमाएं साझा करता है?",
    "q_en": "Which state shares most international borders?",
    "options": [
      {
        "letter": "A",
        "hi": "जम्मू-कश्मीर",
        "en": "Jammu-Kashmir"
      },
      {
        "letter": "B",
        "hi": "पश्चिम बंगाल",
        "en": "West Bengal"
      },
      {
        "letter": "C",
        "hi": "अरुणाचल प्रदेश",
        "en": "Arunachal Pradesh"
      },
      {
        "letter": "D",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      }
    ],
    "correct": "A",
    "exp_hi": "जम्मू-कश्मीर पाकिस्तान और चीन दोनों से सीमा साझा करता है।",
    "exp_en": "Jammu-Kashmir shares borders with both Pakistan and China.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत की सबसे पुरानी पर्वत श्रृंखला?",
    "q_en": "Oldest mountain range of India?",
    "options": [
      {
        "letter": "A",
        "hi": "हिमालय",
        "en": "Himalayas"
      },
      {
        "letter": "B",
        "hi": "अरावली",
        "en": "Aravalli"
      },
      {
        "letter": "C",
        "hi": "विंध्याचल",
        "en": "Vindhyas"
      },
      {
        "letter": "D",
        "hi": "सतपुड़ा",
        "en": "Satpura"
      }
    ],
    "correct": "B",
    "exp_hi": "अरावली विश्व की सबसे पुरानी पर्वत श्रृंखलाओं में से एक है।",
    "exp_en": "Aravalli is one of world's oldest mountain ranges.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे अधिक वन किस राज्य में हैं?",
    "q_en": "State with most forests in India?",
    "options": [
      {
        "letter": "A",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      },
      {
        "letter": "B",
        "hi": "अरुणाचल प्रदेश",
        "en": "Arunachal Pradesh"
      },
      {
        "letter": "C",
        "hi": "छत्तीसगढ़",
        "en": "Chhattisgarh"
      },
      {
        "letter": "D",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      }
    ],
    "correct": "A",
    "exp_hi": "मध्य प्रदेश में सर्वाधिक वन क्षेत्र है।",
    "exp_en": "Madhya Pradesh has maximum forest area.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे बड़ा बाँध?",
    "q_en": "Largest dam of India?",
    "options": [
      {
        "letter": "A",
        "hi": "भाखड़ा नांगल",
        "en": "Bhakra Nangal"
      },
      {
        "letter": "B",
        "hi": "टिहरी",
        "en": "Tehri"
      },
      {
        "letter": "C",
        "hi": "हीराकुड",
        "en": "Hirakud"
      },
      {
        "letter": "D",
        "hi": "नागार्जुन सागर",
        "en": "Nagarjuna Sagar"
      }
    ],
    "correct": "C",
    "exp_hi": "हीराकुड बाँध (4.8 km) भारत का सबसे लंबा बाँध है।",
    "exp_en": "Hirakud Dam (4.8 km) is India's longest dam.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे अधिक कोयला कहाँ है?",
    "q_en": "Where are largest coal reserves in India?",
    "options": [
      {
        "letter": "A",
        "hi": "छत्तीसगढ़",
        "en": "Chhattisgarh"
      },
      {
        "letter": "B",
        "hi": "झारखंड",
        "en": "Jharkhand"
      },
      {
        "letter": "C",
        "hi": "ओडिशा",
        "en": "Odisha"
      },
      {
        "letter": "D",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      }
    ],
    "correct": "B",
    "exp_hi": "झारखंड में भारत के सबसे बड़े कोयला भंडार हैं।",
    "exp_en": "Jharkhand has India's largest coal reserves.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे बड़ा अभयारण्य कौन सा है?",
    "q_en": "Largest wildlife sanctuary in India?",
    "options": [
      {
        "letter": "A",
        "hi": "कॉर्बेट",
        "en": "Corbett"
      },
      {
        "letter": "B",
        "hi": "गिर",
        "en": "Gir"
      },
      {
        "letter": "C",
        "hi": "काजीरंगा",
        "en": "Kaziranga"
      },
      {
        "letter": "D",
        "hi": "नल्लामाला",
        "en": "Nallamala"
      }
    ],
    "correct": "D",
    "exp_hi": "नल्लामाला (आंध्र प्रदेश/तेलंगाना) भारत का सबसे बड़ा अभयारण्य है।",
    "exp_en": "Nallamala (Andhra Pradesh/Telangana) is India's largest sanctuary.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का एकमात्र सक्रिय ज्वालामुखी कहाँ है?",
    "q_en": "India's only active volcano?",
    "options": [
      {
        "letter": "A",
        "hi": "अंडमान",
        "en": "Andaman"
      },
      {
        "letter": "B",
        "hi": "बैरन द्वीप",
        "en": "Barren Island"
      },
      {
        "letter": "C",
        "hi": "लक्षद्वीप",
        "en": "Lakshadweep"
      },
      {
        "letter": "D",
        "hi": "निकोबार",
        "en": "Nicobar"
      }
    ],
    "correct": "B",
    "exp_hi": "बैरन द्वीप (अंडमान) भारत का एकमात्र सक्रिय ज्वालामुखी है।",
    "exp_en": "Barren Island (Andaman) is India's only active volcano.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में लौह अयस्क सबसे अधिक कहाँ है?",
    "q_en": "Maximum iron ore in India?",
    "options": [
      {
        "letter": "A",
        "hi": "छत्तीसगढ़",
        "en": "Chhattisgarh"
      },
      {
        "letter": "B",
        "hi": "झारखंड",
        "en": "Jharkhand"
      },
      {
        "letter": "C",
        "hi": "ओडिशा",
        "en": "Odisha"
      },
      {
        "letter": "D",
        "hi": "गोवा",
        "en": "Goa"
      }
    ],
    "correct": "C",
    "exp_hi": "ओडिशा में सर्वाधिक लौह अयस्क भंडार है।",
    "exp_en": "Odisha has maximum iron ore reserves.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे पहले सूर्योदय कहाँ होता है?",
    "q_en": "Where does sun rise first in India?",
    "options": [
      {
        "letter": "A",
        "hi": "असम",
        "en": "Assam"
      },
      {
        "letter": "B",
        "hi": "अरुणाचल प्रदेश",
        "en": "Arunachal Pradesh"
      },
      {
        "letter": "C",
        "hi": "मेघालय",
        "en": "Meghalaya"
      },
      {
        "letter": "D",
        "hi": "मणिपुर",
        "en": "Manipur"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत में सबसे पहले सूर्योदय अरुणाचल प्रदेश में होता है।",
    "exp_en": "Sun rises first in India in Arunachal Pradesh.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "जम्मू-कश्मीर की ग्रीष्मकालीन राजधानी?",
    "q_en": "Summer capital of Jammu-Kashmir?",
    "options": [
      {
        "letter": "A",
        "hi": "जम्मू",
        "en": "Jammu"
      },
      {
        "letter": "B",
        "hi": "श्रीनगर",
        "en": "Srinagar"
      },
      {
        "letter": "C",
        "hi": "लेह",
        "en": "Leh"
      },
      {
        "letter": "D",
        "hi": "कारगिल",
        "en": "Kargil"
      }
    ],
    "correct": "B",
    "exp_hi": "श्रीनगर J&K की ग्रीष्मकालीन राजधानी है।",
    "exp_en": "Srinagar is the summer capital of J&K.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "डिगबोई किस राज्य में है?",
    "q_en": "Digboi is in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "मेघालय",
        "en": "Meghalaya"
      },
      {
        "letter": "B",
        "hi": "असम",
        "en": "Assam"
      },
      {
        "letter": "C",
        "hi": "नागालैंड",
        "en": "Nagaland"
      },
      {
        "letter": "D",
        "hi": "मणिपुर",
        "en": "Manipur"
      }
    ],
    "correct": "B",
    "exp_hi": "डिगबोई असम में है और भारत की पहली तेल रिफाइनरी यहाँ है।",
    "exp_en": "Digboi is in Assam and has India's first oil refinery.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'स्पाइस गार्डन' किसे कहते हैं?",
    "q_en": "Which state is called 'Spice Garden' of India?",
    "options": [
      {
        "letter": "A",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      },
      {
        "letter": "B",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "C",
        "hi": "कर्नाटक",
        "en": "Karnataka"
      },
      {
        "letter": "D",
        "hi": "गोवा",
        "en": "Goa"
      }
    ],
    "correct": "B",
    "exp_hi": "केरल को भारत का स्पाइस गार्डन कहते हैं।",
    "exp_en": "Kerala is called the Spice Garden of India.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत की सबसे लंबी सुरंग?",
    "q_en": "Longest tunnel in India?",
    "options": [
      {
        "letter": "A",
        "hi": "रोहतांग सुरंग",
        "en": "Rohtang Tunnel"
      },
      {
        "letter": "B",
        "hi": "अटल सुरंग",
        "en": "Atal Tunnel"
      },
      {
        "letter": "C",
        "hi": "बनिहाल सुरंग",
        "en": "Banihal Tunnel"
      },
      {
        "letter": "D",
        "hi": "चेनानी-नाशरी",
        "en": "Chenani-Nashri"
      }
    ],
    "correct": "B",
    "exp_hi": "अटल सुरंग (9.02 km) भारत की सबसे लंबी राजमार्ग सुरंग है।",
    "exp_en": "Atal Tunnel (9.02 km) is India's longest highway tunnel.",
    "exam_tag": "UPSC 2017",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में गेहूँ उत्पादन में पहले स्थान पर कौन सा राज्य है?",
    "q_en": "Top state in wheat production?",
    "options": [
      {
        "letter": "A",
        "hi": "पंजाब",
        "en": "Punjab"
      },
      {
        "letter": "B",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "C",
        "hi": "हरियाणा",
        "en": "Haryana"
      },
      {
        "letter": "D",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      }
    ],
    "correct": "B",
    "exp_hi": "उत्तर प्रदेश गेहूँ उत्पादन में पहले स्थान पर है।",
    "exp_en": "Uttar Pradesh is top in wheat production.",
    "exam_tag": "SSC 2018",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में कौन सा राज्य सबसे अधिक दूध उत्पादन करता है?",
    "q_en": "Top milk producing state of India?",
    "options": [
      {
        "letter": "A",
        "hi": "पंजाब",
        "en": "Punjab"
      },
      {
        "letter": "B",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "C",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "D",
        "hi": "गुजरात",
        "en": "Gujarat"
      }
    ],
    "correct": "B",
    "exp_hi": "उत्तर प्रदेश भारत का सबसे बड़ा दूध उत्पादक राज्य है।",
    "exp_en": "Uttar Pradesh is India's largest milk producing state.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे अधिक सोना कहाँ निकाला जाता है?",
    "q_en": "Maximum gold mining in India?",
    "options": [
      {
        "letter": "A",
        "hi": "झारखंड",
        "en": "Jharkhand"
      },
      {
        "letter": "B",
        "hi": "कर्नाटक",
        "en": "Karnataka"
      },
      {
        "letter": "C",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "D",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      }
    ],
    "correct": "B",
    "exp_hi": "कर्नाटक (कोलार) में सर्वाधिक सोना निकाला जाता है।",
    "exp_en": "Karnataka (Kolar) has maximum gold mining.",
    "exam_tag": "UPSC 2019",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का 'मसाला राज्य' किसे कहते हैं?",
    "q_en": "Which state is called 'Spice State' of India?",
    "options": [
      {
        "letter": "A",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "B",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "C",
        "hi": "गुजरात",
        "en": "Gujarat"
      },
      {
        "letter": "D",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      }
    ],
    "correct": "A",
    "exp_hi": "केरल को भारत का मसाला राज्य कहते हैं।",
    "exp_en": "Kerala is called India's spice state.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का 'सिलिकॉन वैली' कहाँ है?",
    "q_en": "Where is India's Silicon Valley?",
    "options": [
      {
        "letter": "A",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "B",
        "hi": "हैदराबाद",
        "en": "Hyderabad"
      },
      {
        "letter": "C",
        "hi": "बेंगलुरु",
        "en": "Bengaluru"
      },
      {
        "letter": "D",
        "hi": "पुणे",
        "en": "Pune"
      }
    ],
    "correct": "C",
    "exp_hi": "बेंगलुरु को भारत की सिलिकॉन वैली कहते हैं।",
    "exp_en": "Bengaluru is called Silicon Valley of India.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे अधिक मूंगफली कहाँ उगाई जाती है?",
    "q_en": "Maximum groundnut production in India?",
    "options": [
      {
        "letter": "A",
        "hi": "गुजरात",
        "en": "Gujarat"
      },
      {
        "letter": "B",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "C",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      },
      {
        "letter": "D",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      }
    ],
    "correct": "A",
    "exp_hi": "गुजरात भारत में सर्वाधिक मूंगफली उत्पादन करता है।",
    "exp_en": "Gujarat produces maximum groundnut in India.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का 'धान का कटोरा' किस राज्य को कहते हैं?",
    "q_en": "Which state is called 'Rice Bowl' of India?",
    "options": [
      {
        "letter": "A",
        "hi": "पश्चिम बंगाल",
        "en": "West Bengal"
      },
      {
        "letter": "B",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      },
      {
        "letter": "C",
        "hi": "छत्तीसगढ़",
        "en": "Chhattisgarh"
      },
      {
        "letter": "D",
        "hi": "ओडिशा",
        "en": "Odisha"
      }
    ],
    "correct": "C",
    "exp_hi": "छत्तीसगढ़ को 'धान का कटोरा' कहते हैं।",
    "exp_en": "Chhattisgarh is called the 'Rice Bowl' of India.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "पूर्वी घाट को क्या कहते हैं?",
    "q_en": "Eastern Ghats are also known as?",
    "options": [
      {
        "letter": "A",
        "hi": "मलयाद्री",
        "en": "Malayadri"
      },
      {
        "letter": "B",
        "hi": "सह्याद्री",
        "en": "Sahyadri"
      },
      {
        "letter": "C",
        "hi": "मलयाद्री",
        "en": "Malayadri"
      },
      {
        "letter": "D",
        "hi": "कोई विशेष नाम नहीं",
        "en": "No special name"
      }
    ],
    "correct": "A",
    "exp_hi": "पूर्वी घाट को मलयाद्री भी कहते हैं।",
    "exp_en": "Eastern Ghats are also called Malayadri.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे अधिक जनसंख्या घनत्व वाला राज्य?",
    "q_en": "Most densely populated state of India?",
    "options": [
      {
        "letter": "A",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "B",
        "hi": "पश्चिम बंगाल",
        "en": "West Bengal"
      },
      {
        "letter": "C",
        "hi": "बिहार",
        "en": "Bihar"
      },
      {
        "letter": "D",
        "hi": "केरल",
        "en": "Kerala"
      }
    ],
    "correct": "C",
    "exp_hi": "बिहार सबसे अधिक जनसंख्या घनत्व वाला राज्य है।",
    "exp_en": "Bihar is the most densely populated state.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सर्वाधिक साक्षरता दर किस राज्य में है?",
    "q_en": "Highest literacy rate in India?",
    "options": [
      {
        "letter": "A",
        "hi": "गोवा",
        "en": "Goa"
      },
      {
        "letter": "B",
        "hi": "मिजोरम",
        "en": "Mizoram"
      },
      {
        "letter": "C",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "D",
        "hi": "हिमाचल प्रदेश",
        "en": "Himachal Pradesh"
      }
    ],
    "correct": "C",
    "exp_hi": "केरल में सर्वाधिक साक्षरता दर है (96.2%)।",
    "exp_en": "Kerala has highest literacy rate (96.2%).",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "'पूर्व का स्कॉटलैंड' किसे कहते हैं?",
    "q_en": "Which is called 'Scotland of the East'?",
    "options": [
      {
        "letter": "A",
        "hi": "मेघालय",
        "en": "Meghalaya"
      },
      {
        "letter": "B",
        "hi": "सिक्किम",
        "en": "Sikkim"
      },
      {
        "letter": "C",
        "hi": "अरुणाचल प्रदेश",
        "en": "Arunachal Pradesh"
      },
      {
        "letter": "D",
        "hi": "मणिपुर",
        "en": "Manipur"
      }
    ],
    "correct": "A",
    "exp_hi": "मेघालय को 'पूर्व का स्कॉटलैंड' कहते हैं।",
    "exp_en": "Meghalaya is called the 'Scotland of the East'.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे कम जनसंख्या घनत्व वाला राज्य?",
    "q_en": "Least densely populated state of India?",
    "options": [
      {
        "letter": "A",
        "hi": "सिक्किम",
        "en": "Sikkim"
      },
      {
        "letter": "B",
        "hi": "अरुणाचल प्रदेश",
        "en": "Arunachal Pradesh"
      },
      {
        "letter": "C",
        "hi": "मिजोरम",
        "en": "Mizoram"
      },
      {
        "letter": "D",
        "hi": "मेघालय",
        "en": "Meghalaya"
      }
    ],
    "correct": "B",
    "exp_hi": "अरुणाचल प्रदेश में सबसे कम जनसंख्या घनत्व है।",
    "exp_en": "Arunachal Pradesh has lowest population density.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'कोयला राजधानी' किसे कहते हैं?",
    "q_en": "Which is called 'Coal Capital' of India?",
    "options": [
      {
        "letter": "A",
        "hi": "रांची",
        "en": "Ranchi"
      },
      {
        "letter": "B",
        "hi": "धनबाद",
        "en": "Dhanbad"
      },
      {
        "letter": "C",
        "hi": "जमशेदपुर",
        "en": "Jamshedpur"
      },
      {
        "letter": "D",
        "hi": "बोकारो",
        "en": "Bokaro"
      }
    ],
    "correct": "B",
    "exp_hi": "धनबाद को भारत की कोयला राजधानी कहते हैं।",
    "exp_en": "Dhanbad is called the Coal Capital of India.",
    "exam_tag": "UPSC 2016",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "लोकटक झील कहाँ है?",
    "q_en": "Where is Loktak Lake?",
    "options": [
      {
        "letter": "A",
        "hi": "असम",
        "en": "Assam"
      },
      {
        "letter": "B",
        "hi": "मेघालय",
        "en": "Meghalaya"
      },
      {
        "letter": "C",
        "hi": "मणिपुर",
        "en": "Manipur"
      },
      {
        "letter": "D",
        "hi": "नागालैंड",
        "en": "Nagaland"
      }
    ],
    "correct": "C",
    "exp_hi": "लोकटक झील मणिपुर में है और यह पूर्वोत्तर भारत की सबसे बड़ी मीठे पानी की झील है।",
    "exp_en": "Loktak Lake is in Manipur and is Northeast India's largest freshwater lake.",
    "exam_tag": "SSC 2017",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का 'इस्पात नगर' किसे कहते हैं?",
    "q_en": "Which is called 'Steel City' of India?",
    "options": [
      {
        "letter": "A",
        "hi": "रांची",
        "en": "Ranchi"
      },
      {
        "letter": "B",
        "hi": "जमशेदपुर",
        "en": "Jamshedpur"
      },
      {
        "letter": "C",
        "hi": "भिलाई",
        "en": "Bhilai"
      },
      {
        "letter": "D",
        "hi": "बोकारो",
        "en": "Bokaro"
      }
    ],
    "correct": "B",
    "exp_hi": "जमशेदपुर (टाटानगर) को भारत का इस्पात नगर कहते हैं।",
    "exp_en": "Jamshedpur (Tatanagar) is called India's Steel City.",
    "exam_tag": "Railway 2018",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'मैनचेस्टर ऑफ इंडिया' किसे कहते हैं?",
    "q_en": "Which is called 'Manchester of India'?",
    "options": [
      {
        "letter": "A",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "B",
        "hi": "कोयंबटूर",
        "en": "Coimbatore"
      },
      {
        "letter": "C",
        "hi": "अहमदाबाद",
        "en": "Ahmedabad"
      },
      {
        "letter": "D",
        "hi": "सूरत",
        "en": "Surat"
      }
    ],
    "correct": "C",
    "exp_hi": "अहमदाबाद को 'मैनचेस्टर ऑफ इंडिया' कहते हैं।",
    "exp_en": "Ahmedabad is called 'Manchester of India'.",
    "exam_tag": "UPSC 2018",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'नीली क्रांति' किससे संबंधित है?",
    "q_en": "Blue Revolution in India is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "जल संरक्षण",
        "en": "Water conservation"
      },
      {
        "letter": "B",
        "hi": "मत्स्य पालन",
        "en": "Fisheries"
      },
      {
        "letter": "C",
        "hi": "नीली मिट्टी",
        "en": "Blue soil"
      },
      {
        "letter": "D",
        "hi": "नदी सफाई",
        "en": "River cleaning"
      }
    ],
    "correct": "B",
    "exp_hi": "नीली क्रांति मत्स्य पालन (Fisheries) से संबंधित है।",
    "exp_en": "Blue Revolution is related to fisheries development.",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'पीली क्रांति' किससे संबंधित है?",
    "q_en": "Yellow Revolution in India is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "सोना",
        "en": "Gold"
      },
      {
        "letter": "B",
        "hi": "तिलहन",
        "en": "Oilseeds"
      },
      {
        "letter": "C",
        "hi": "दालें",
        "en": "Pulses"
      },
      {
        "letter": "D",
        "hi": "मक्का",
        "en": "Maize"
      }
    ],
    "correct": "B",
    "exp_hi": "पीली क्रांति तिलहन उत्पादन से संबंधित है।",
    "exp_en": "Yellow Revolution is related to oilseed production.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'ऑपरेशन फ्लड' किससे संबंधित था?",
    "q_en": "Operation Flood in India was related to?",
    "options": [
      {
        "letter": "A",
        "hi": "बाढ़ नियंत्रण",
        "en": "Flood control"
      },
      {
        "letter": "B",
        "hi": "दूध उत्पादन",
        "en": "Milk production"
      },
      {
        "letter": "C",
        "hi": "मत्स्य पालन",
        "en": "Fisheries"
      },
      {
        "letter": "D",
        "hi": "सिंचाई",
        "en": "Irrigation"
      }
    ],
    "correct": "B",
    "exp_hi": "ऑपरेशन फ्लड श्वेत क्रांति का हिस्सा था और दूध उत्पादन से संबंधित था।",
    "exp_en": "Operation Flood was part of White Revolution related to milk production.",
    "exam_tag": "UPSC 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का 'गेहूँ का कटोरा' किसे कहते हैं?",
    "q_en": "Which is called 'Wheat Bowl' of India?",
    "options": [
      {
        "letter": "A",
        "hi": "हरियाणा",
        "en": "Haryana"
      },
      {
        "letter": "B",
        "hi": "पंजाब",
        "en": "Punjab"
      },
      {
        "letter": "C",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "D",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      }
    ],
    "correct": "B",
    "exp_hi": "पंजाब को भारत का 'गेहूँ का कटोरा' कहते हैं।",
    "exp_en": "Punjab is called the 'Wheat Bowl' of India.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'फलों का राजा' कौन सा है?",
    "q_en": "Which fruit is called 'King of Fruits' in India?",
    "options": [
      {
        "letter": "A",
        "hi": "केला",
        "en": "Banana"
      },
      {
        "letter": "B",
        "hi": "आम",
        "en": "Mango"
      },
      {
        "letter": "C",
        "hi": "अनार",
        "en": "Pomegranate"
      },
      {
        "letter": "D",
        "hi": "अंगूर",
        "en": "Grapes"
      }
    ],
    "correct": "B",
    "exp_hi": "आम को 'फलों का राजा' कहते हैं।",
    "exp_en": "Mango is called the 'King of Fruits'.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे अधिक आम कहाँ उगाया जाता है?",
    "q_en": "Maximum mango production in India?",
    "options": [
      {
        "letter": "A",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      },
      {
        "letter": "B",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      },
      {
        "letter": "C",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "D",
        "hi": "कर्नाटक",
        "en": "Karnataka"
      }
    ],
    "correct": "C",
    "exp_hi": "उत्तर प्रदेश भारत में सर्वाधिक आम उत्पादन करता है।",
    "exp_en": "Uttar Pradesh produces maximum mango in India.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'गुलाबी नगर' कहाँ है?",
    "q_en": "Where is 'Pink City' of India?",
    "options": [
      {
        "letter": "A",
        "hi": "जोधपुर",
        "en": "Jodhpur"
      },
      {
        "letter": "B",
        "hi": "उदयपुर",
        "en": "Udaipur"
      },
      {
        "letter": "C",
        "hi": "जयपुर",
        "en": "Jaipur"
      },
      {
        "letter": "D",
        "hi": "अजमेर",
        "en": "Ajmer"
      }
    ],
    "correct": "C",
    "exp_hi": "जयपुर को 'गुलाबी नगर' (Pink City) कहते हैं।",
    "exp_en": "Jaipur is called the 'Pink City'.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'सुनहरी नगर' कहाँ है?",
    "q_en": "Where is 'Golden City' of India?",
    "options": [
      {
        "letter": "A",
        "hi": "जयपुर",
        "en": "Jaipur"
      },
      {
        "letter": "B",
        "hi": "जोधपुर",
        "en": "Jodhpur"
      },
      {
        "letter": "C",
        "hi": "जैसलमेर",
        "en": "Jaisalmer"
      },
      {
        "letter": "D",
        "hi": "उदयपुर",
        "en": "Udaipur"
      }
    ],
    "correct": "C",
    "exp_hi": "जैसलमेर को 'सुनहरी नगर' (Golden City) कहते हैं।",
    "exp_en": "Jaisalmer is called the 'Golden City'.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का 'IT हब' कौन सा शहर है?",
    "q_en": "IT hub of India?",
    "options": [
      {
        "letter": "A",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "B",
        "hi": "दिल्ली",
        "en": "Delhi"
      },
      {
        "letter": "C",
        "hi": "बेंगलुरु",
        "en": "Bengaluru"
      },
      {
        "letter": "D",
        "hi": "हैदराबाद",
        "en": "Hyderabad"
      }
    ],
    "correct": "C",
    "exp_hi": "बेंगलुरु भारत का IT हब है।",
    "exp_en": "Bengaluru is India's IT hub.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'झीलों का शहर' कहाँ है?",
    "q_en": "Which is called 'City of Lakes' in India?",
    "options": [
      {
        "letter": "A",
        "hi": "श्रीनगर",
        "en": "Srinagar"
      },
      {
        "letter": "B",
        "hi": "उदयपुर",
        "en": "Udaipur"
      },
      {
        "letter": "C",
        "hi": "जयपुर",
        "en": "Jaipur"
      },
      {
        "letter": "D",
        "hi": "नैनीताल",
        "en": "Nainital"
      }
    ],
    "correct": "B",
    "exp_hi": "उदयपुर को 'झीलों का शहर' कहते हैं।",
    "exp_en": "Udaipur is called the 'City of Lakes'.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'भारत का प्रवेश द्वार' किसे कहते हैं?",
    "q_en": "Which is called 'Gateway of India'?",
    "options": [
      {
        "letter": "A",
        "hi": "कोलकाता",
        "en": "Kolkata"
      },
      {
        "letter": "B",
        "hi": "चेन्नई",
        "en": "Chennai"
      },
      {
        "letter": "C",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "D",
        "hi": "कोच्चि",
        "en": "Kochi"
      }
    ],
    "correct": "C",
    "exp_hi": "मुंबई को 'भारत का प्रवेश द्वार' कहते हैं।",
    "exp_en": "Mumbai is called the 'Gateway of India'.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे पश्चिमी बिंदु कहाँ है?",
    "q_en": "Westernmost point of India?",
    "options": [
      {
        "letter": "A",
        "hi": "द्वारका",
        "en": "Dwarka"
      },
      {
        "letter": "B",
        "hi": "सर क्रीक",
        "en": "Sir Creek"
      },
      {
        "letter": "C",
        "hi": "गौर मोता",
        "en": "Gaur Mota"
      },
      {
        "letter": "D",
        "hi": "कच्छ का रन",
        "en": "Rann of Kutch"
      }
    ],
    "correct": "C",
    "exp_hi": "गुजरात में गौर मोता भारत का सबसे पश्चिमी बिंदु है।",
    "exp_en": "Gaur Mota in Gujarat is India's westernmost point.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे उत्तरी बिंदु कहाँ है?",
    "q_en": "Northernmost point of India?",
    "options": [
      {
        "letter": "A",
        "hi": "सियाचिन",
        "en": "Siachen"
      },
      {
        "letter": "B",
        "hi": "इंदिरा कोल",
        "en": "Indira Col"
      },
      {
        "letter": "C",
        "hi": "लेह",
        "en": "Leh"
      },
      {
        "letter": "D",
        "hi": "कारगिल",
        "en": "Kargil"
      }
    ],
    "correct": "B",
    "exp_hi": "इंदिरा कोल (जम्मू-कश्मीर) भारत का सबसे उत्तरी बिंदु है।",
    "exp_en": "Indira Col (J&K) is India's northernmost point.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे अधिक जूट कहाँ उगाई जाती है?",
    "q_en": "Maximum jute production in India?",
    "options": [
      {
        "letter": "A",
        "hi": "बिहार",
        "en": "Bihar"
      },
      {
        "letter": "B",
        "hi": "ओडिशा",
        "en": "Odisha"
      },
      {
        "letter": "C",
        "hi": "पश्चिम बंगाल",
        "en": "West Bengal"
      },
      {
        "letter": "D",
        "hi": "असम",
        "en": "Assam"
      }
    ],
    "correct": "C",
    "exp_hi": "पश्चिम बंगाल भारत में सर्वाधिक जूट उत्पादन करता है।",
    "exp_en": "West Bengal produces maximum jute in India.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "'भारत का बगीचा' किसे कहते हैं?",
    "q_en": "Which state is called 'Garden of India'?",
    "options": [
      {
        "letter": "A",
        "hi": "हिमाचल प्रदेश",
        "en": "Himachal Pradesh"
      },
      {
        "letter": "B",
        "hi": "उत्तराखंड",
        "en": "Uttarakhand"
      },
      {
        "letter": "C",
        "hi": "मेघालय",
        "en": "Meghalaya"
      },
      {
        "letter": "D",
        "hi": "सिक्किम",
        "en": "Sikkim"
      }
    ],
    "correct": "A",
    "exp_hi": "हिमाचल प्रदेश को 'भारत का बगीचा' कहते हैं।",
    "exp_en": "Himachal Pradesh is called the 'Garden of India'.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सर्वाधिक सीमेंट कहाँ बनता है?",
    "q_en": "Maximum cement production in India?",
    "options": [
      {
        "letter": "A",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "B",
        "hi": "गुजरात",
        "en": "Gujarat"
      },
      {
        "letter": "C",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      },
      {
        "letter": "D",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      }
    ],
    "correct": "A",
    "exp_hi": "राजस्थान भारत में सर्वाधिक सीमेंट उत्पादन करता है।",
    "exp_en": "Rajasthan produces maximum cement in India.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'नीलगिरि' किस राज्य में है?",
    "q_en": "Nilgiris are in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "B",
        "hi": "कर्नाटक",
        "en": "Karnataka"
      },
      {
        "letter": "C",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      },
      {
        "letter": "D",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      }
    ],
    "correct": "C",
    "exp_hi": "नीलगिरि पर्वत तमिलनाडु में है।",
    "exp_en": "Nilgiri mountains are in Tamil Nadu.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'सरदार सरोवर परियोजना' किस नदी पर है?",
    "q_en": "Sardar Sarovar Project is on which river?",
    "options": [
      {
        "letter": "A",
        "hi": "नर्मदा",
        "en": "Narmada"
      },
      {
        "letter": "B",
        "hi": "ताप्ती",
        "en": "Tapti"
      },
      {
        "letter": "C",
        "hi": "माही",
        "en": "Mahi"
      },
      {
        "letter": "D",
        "hi": "साबरमती",
        "en": "Sabarmati"
      }
    ],
    "correct": "A",
    "exp_hi": "सरदार सरोवर परियोजना नर्मदा नदी पर है।",
    "exp_en": "Sardar Sarovar Project is on Narmada river.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का सबसे बड़ा नमक उत्पादक राज्य?",
    "q_en": "Largest salt producing state of India?",
    "options": [
      {
        "letter": "A",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "B",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      },
      {
        "letter": "C",
        "hi": "गुजरात",
        "en": "Gujarat"
      },
      {
        "letter": "D",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      }
    ],
    "correct": "C",
    "exp_hi": "गुजरात भारत का सबसे बड़ा नमक उत्पादक राज्य है।",
    "exp_en": "Gujarat is India's largest salt producing state.",
    "exam_tag": "Railway 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'सेब का राज्य' किसे कहते हैं?",
    "q_en": "Which state is called 'Apple State' of India?",
    "options": [
      {
        "letter": "A",
        "hi": "उत्तराखंड",
        "en": "Uttarakhand"
      },
      {
        "letter": "B",
        "hi": "जम्मू-कश्मीर",
        "en": "Jammu-Kashmir"
      },
      {
        "letter": "C",
        "hi": "हिमाचल प्रदेश",
        "en": "Himachal Pradesh"
      },
      {
        "letter": "D",
        "hi": "सिक्किम",
        "en": "Sikkim"
      }
    ],
    "correct": "C",
    "exp_hi": "हिमाचल प्रदेश को 'सेब का राज्य' कहते हैं।",
    "exp_en": "Himachal Pradesh is called the 'Apple State'.",
    "exam_tag": "CTET 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सर्वाधिक तांबा कहाँ मिलता है?",
    "q_en": "Maximum copper in India?",
    "options": [
      {
        "letter": "A",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "B",
        "hi": "झारखंड",
        "en": "Jharkhand"
      },
      {
        "letter": "C",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      },
      {
        "letter": "D",
        "hi": "कर्नाटक",
        "en": "Karnataka"
      }
    ],
    "correct": "A",
    "exp_hi": "राजस्थान में सर्वाधिक तांबा (खेतड़ी) मिलता है।",
    "exp_en": "Rajasthan has maximum copper (Khetri).",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'देवभूमि' किसे कहते हैं?",
    "q_en": "Which is called 'Land of Gods' in India?",
    "options": [
      {
        "letter": "A",
        "hi": "हिमाचल प्रदेश",
        "en": "Himachal Pradesh"
      },
      {
        "letter": "B",
        "hi": "उत्तराखंड",
        "en": "Uttarakhand"
      },
      {
        "letter": "C",
        "hi": "जम्मू-कश्मीर",
        "en": "Jammu-Kashmir"
      },
      {
        "letter": "D",
        "hi": "सिक्किम",
        "en": "Sikkim"
      }
    ],
    "correct": "B",
    "exp_hi": "उत्तराखंड को 'देवभूमि' कहते हैं।",
    "exp_en": "Uttarakhand is called 'Devbhoomi' (Land of Gods).",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत की 'बागों की रानी' किसे कहते हैं?",
    "q_en": "Which is called 'Queen of Gardens' in India?",
    "options": [
      {
        "letter": "A",
        "hi": "उदयपुर",
        "en": "Udaipur"
      },
      {
        "letter": "B",
        "hi": "दार्जिलिंग",
        "en": "Darjeeling"
      },
      {
        "letter": "C",
        "hi": "ऊटी",
        "en": "Ooty"
      },
      {
        "letter": "D",
        "hi": "शिमला",
        "en": "Shimla"
      }
    ],
    "correct": "C",
    "exp_hi": "ऊटी (उधगमंडलम) को 'बागों की रानी' कहते हैं।",
    "exp_en": "Ooty (Udagamandalam) is called the 'Queen of Gardens'.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का राष्ट्रीय फल कौन सा है?",
    "q_en": "National fruit of India?",
    "options": [
      {
        "letter": "A",
        "hi": "केला",
        "en": "Banana"
      },
      {
        "letter": "B",
        "hi": "आम",
        "en": "Mango"
      },
      {
        "letter": "C",
        "hi": "सेब",
        "en": "Apple"
      },
      {
        "letter": "D",
        "hi": "अमरूद",
        "en": "Guava"
      }
    ],
    "correct": "B",
    "exp_hi": "आम भारत का राष्ट्रीय फल है।",
    "exp_en": "Mango is India's national fruit.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का राष्ट्रीय वृक्ष कौन सा है?",
    "q_en": "National tree of India?",
    "options": [
      {
        "letter": "A",
        "hi": "पीपल",
        "en": "Peepal"
      },
      {
        "letter": "B",
        "hi": "बरगद",
        "en": "Banyan"
      },
      {
        "letter": "C",
        "hi": "नीम",
        "en": "Neem"
      },
      {
        "letter": "D",
        "hi": "आम",
        "en": "Mango"
      }
    ],
    "correct": "B",
    "exp_hi": "बरगद (Banyan) भारत का राष्ट्रीय वृक्ष है।",
    "exp_en": "Banyan is India's national tree.",
    "exam_tag": "CTET 2020",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "भारत की मुख्य भूमि का दक्षिणी सिरा?",
    "q_en": "Southernmost tip of Indian mainland?",
    "options": [
      {
        "letter": "A",
        "hi": "रामेश्वरम",
        "en": "Rameswaram"
      },
      {
        "letter": "B",
        "hi": "कन्याकुमारी",
        "en": "Kanyakumari"
      },
      {
        "letter": "C",
        "hi": "इंदिरा पॉइंट",
        "en": "Indira Point"
      },
      {
        "letter": "D",
        "hi": "कोच्चि",
        "en": "Kochi"
      }
    ],
    "correct": "B",
    "exp_hi": "कन्याकुमारी भारत की मुख्य भूमि का सबसे दक्षिणी बिंदु है।",
    "exp_en": "Kanyakumari is the southernmost tip of Indian mainland.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "लद्दाख की राजधानी?",
    "q_en": "Capital of Ladakh?",
    "options": [
      {
        "letter": "A",
        "hi": "कारगिल",
        "en": "Kargil"
      },
      {
        "letter": "B",
        "hi": "लेह",
        "en": "Leh"
      },
      {
        "letter": "C",
        "hi": "श्रीनगर",
        "en": "Srinagar"
      },
      {
        "letter": "D",
        "hi": "जम्मू",
        "en": "Jammu"
      }
    ],
    "correct": "B",
    "exp_hi": "लेह लद्दाख की राजधानी है।",
    "exp_en": "Leh is the capital of Ladakh.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "काजीरंगा राष्ट्रीय उद्यान किसके लिए प्रसिद्ध है?",
    "q_en": "Kaziranga National Park is famous for?",
    "options": [
      {
        "letter": "A",
        "hi": "बाघ",
        "en": "Tiger"
      },
      {
        "letter": "B",
        "hi": "एक सींग वाला गैंडा",
        "en": "One-horned Rhino"
      },
      {
        "letter": "C",
        "hi": "हाथी",
        "en": "Elephant"
      },
      {
        "letter": "D",
        "hi": "शेर",
        "en": "Lion"
      }
    ],
    "correct": "B",
    "exp_hi": "काजीरंगा असम में है और एक सींग वाले गैंडे के लिए प्रसिद्ध है।",
    "exp_en": "Kaziranga is in Assam and famous for one-horned rhino.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "गिर राष्ट्रीय उद्यान किसके लिए प्रसिद्ध है?",
    "q_en": "Gir National Park is famous for?",
    "options": [
      {
        "letter": "A",
        "hi": "बाघ",
        "en": "Tiger"
      },
      {
        "letter": "B",
        "hi": "शेर",
        "en": "Lion"
      },
      {
        "letter": "C",
        "hi": "गैंडा",
        "en": "Rhino"
      },
      {
        "letter": "D",
        "hi": "हिरण",
        "en": "Deer"
      }
    ],
    "correct": "B",
    "exp_hi": "गिर गुजरात में है और एशियाई शेरों के लिए प्रसिद्ध है।",
    "exp_en": "Gir is in Gujarat and famous for Asiatic lions.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "कॉर्बेट राष्ट्रीय उद्यान कहाँ है?",
    "q_en": "Corbett National Park is in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "उत्तराखंड",
        "en": "Uttarakhand"
      },
      {
        "letter": "B",
        "hi": "हिमाचल प्रदेश",
        "en": "Himachal Pradesh"
      },
      {
        "letter": "C",
        "hi": "जम्मू-कश्मीर",
        "en": "Jammu-Kashmir"
      },
      {
        "letter": "D",
        "hi": "असम",
        "en": "Assam"
      }
    ],
    "correct": "A",
    "exp_hi": "कॉर्बेट राष्ट्रीय उद्यान उत्तराखंड में है।",
    "exp_en": "Corbett National Park is in Uttarakhand.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सबसे अधिक सूती कपड़ा कहाँ बनता है?",
    "q_en": "Maximum cotton textile in India?",
    "options": [
      {
        "letter": "A",
        "hi": "अहमदाबाद",
        "en": "Ahmedabad"
      },
      {
        "letter": "B",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "C",
        "hi": "सूरत",
        "en": "Surat"
      },
      {
        "letter": "D",
        "hi": "कोयंबटूर",
        "en": "Coimbatore"
      }
    ],
    "correct": "A",
    "exp_hi": "अहमदाबाद को 'भारत का मैनचेस्टर' कहते हैं।",
    "exp_en": "Ahmedabad is called 'Manchester of India'.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में गन्ना उत्पादन में पहला राज्य?",
    "q_en": "Top sugarcane producing state of India?",
    "options": [
      {
        "letter": "A",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      },
      {
        "letter": "B",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "C",
        "hi": "पंजाब",
        "en": "Punjab"
      },
      {
        "letter": "D",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      }
    ],
    "correct": "B",
    "exp_hi": "उत्तर प्रदेश भारत का सबसे बड़ा गन्ना उत्पादक राज्य है।",
    "exp_en": "Uttar Pradesh is India's largest sugarcane producing state.",
    "exam_tag": "CTET 2021",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सोयाबीन का सबसे बड़ा उत्पादक राज्य?",
    "q_en": "Largest soybean producing state in India?",
    "options": [
      {
        "letter": "A",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      },
      {
        "letter": "B",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      },
      {
        "letter": "C",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "D",
        "hi": "कर्नाटक",
        "en": "Karnataka"
      }
    ],
    "correct": "B",
    "exp_hi": "मध्य प्रदेश सबसे बड़ा सोयाबीन उत्पादक राज्य है।",
    "exp_en": "Madhya Pradesh is the largest soybean producing state.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "महानदी नदी कहाँ से निकलती है?",
    "q_en": "Where does Mahanadi river originate?",
    "options": [
      {
        "letter": "A",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      },
      {
        "letter": "B",
        "hi": "छत्तीसगढ़",
        "en": "Chhattisgarh"
      },
      {
        "letter": "C",
        "hi": "ओडिशा",
        "en": "Odisha"
      },
      {
        "letter": "D",
        "hi": "झारखंड",
        "en": "Jharkhand"
      }
    ],
    "correct": "B",
    "exp_hi": "महानदी छत्तीसगढ़ के रायपुर जिले से निकलती है।",
    "exp_en": "Mahanadi originates from Raipur district of Chhattisgarh.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "ताप्ती नदी कहाँ गिरती है?",
    "q_en": "Where does Tapti river flow into?",
    "options": [
      {
        "letter": "A",
        "hi": "बंगाल की खाड़ी",
        "en": "Bay of Bengal"
      },
      {
        "letter": "B",
        "hi": "अरब सागर",
        "en": "Arabian Sea"
      },
      {
        "letter": "C",
        "hi": "हिंद महासागर",
        "en": "Indian Ocean"
      },
      {
        "letter": "D",
        "hi": "कच्छ की खाड़ी",
        "en": "Gulf of Kutch"
      }
    ],
    "correct": "B",
    "exp_hi": "ताप्ती नदी अरब सागर में गिरती है।",
    "exp_en": "Tapti river flows into the Arabian Sea.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सरिस्का अभयारण्य कहाँ है?",
    "q_en": "Sariska Sanctuary is in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "B",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      },
      {
        "letter": "C",
        "hi": "गुजरात",
        "en": "Gujarat"
      },
      {
        "letter": "D",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      }
    ],
    "correct": "A",
    "exp_hi": "सरिस्का अभयारण्य राजस्थान के अलवर जिले में है।",
    "exp_en": "Sariska Sanctuary is in Alwar district of Rajasthan.",
    "exam_tag": "CTET 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'कांगड़ा घाटी' कहाँ है?",
    "q_en": "Kangra Valley is in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "उत्तराखंड",
        "en": "Uttarakhand"
      },
      {
        "letter": "B",
        "hi": "हिमाचल प्रदेश",
        "en": "Himachal Pradesh"
      },
      {
        "letter": "C",
        "hi": "जम्मू-कश्मीर",
        "en": "Jammu-Kashmir"
      },
      {
        "letter": "D",
        "hi": "सिक्किम",
        "en": "Sikkim"
      }
    ],
    "correct": "B",
    "exp_hi": "कांगड़ा घाटी हिमाचल प्रदेश में है।",
    "exp_en": "Kangra Valley is in Himachal Pradesh.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'मालाबार तट' किस राज्य में है?",
    "q_en": "Malabar Coast is in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      },
      {
        "letter": "B",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "C",
        "hi": "कर्नाटक",
        "en": "Karnataka"
      },
      {
        "letter": "D",
        "hi": "गोवा",
        "en": "Goa"
      }
    ],
    "correct": "B",
    "exp_hi": "मालाबार तट केरल में है।",
    "exp_en": "Malabar Coast is in Kerala.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में कोरोमंडल तट किस राज्य में है?",
    "q_en": "Coromandel Coast is in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "B",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      },
      {
        "letter": "C",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      },
      {
        "letter": "D",
        "hi": "ओडिशा",
        "en": "Odisha"
      }
    ],
    "correct": "B",
    "exp_hi": "कोरोमंडल तट तमिलनाडु में है।",
    "exp_en": "Coromandel Coast is in Tamil Nadu.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'कच्छ का रन' कहाँ है?",
    "q_en": "Rann of Kutch is in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "B",
        "hi": "गुजरात",
        "en": "Gujarat"
      },
      {
        "letter": "C",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      },
      {
        "letter": "D",
        "hi": "हरियाणा",
        "en": "Haryana"
      }
    ],
    "correct": "B",
    "exp_hi": "कच्छ का रन गुजरात में है।",
    "exp_en": "Rann of Kutch is in Gujarat.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "दोआब क्या है?",
    "q_en": "What is Doab?",
    "options": [
      {
        "letter": "A",
        "hi": "दो नदियों के बीच का क्षेत्र",
        "en": "Land between two rivers"
      },
      {
        "letter": "B",
        "hi": "दो पहाड़ों के बीच का क्षेत्र",
        "en": "Land between two mountains"
      },
      {
        "letter": "C",
        "hi": "दो झीलों के बीच का क्षेत्र",
        "en": "Land between two lakes"
      },
      {
        "letter": "D",
        "hi": "एक नदी का डेल्टा",
        "en": "Delta of a river"
      }
    ],
    "correct": "A",
    "exp_hi": "दोआब दो नदियों के बीच के भूमि क्षेत्र को कहते हैं।",
    "exp_en": "Doab is the land between two rivers.",
    "exam_tag": "CTET 2020",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में सर्वाधिक रबर कहाँ उगाया जाता है?",
    "q_en": "Maximum rubber production in India?",
    "options": [
      {
        "letter": "A",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      },
      {
        "letter": "B",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "C",
        "hi": "कर्नाटक",
        "en": "Karnataka"
      },
      {
        "letter": "D",
        "hi": "असम",
        "en": "Assam"
      }
    ],
    "correct": "B",
    "exp_hi": "केरल भारत में सर्वाधिक रबर उत्पादन करता है।",
    "exp_en": "Kerala produces maximum rubber in India.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'नंदन वन' कहाँ है?",
    "q_en": "Where is Nandan Van in India?",
    "options": [
      {
        "letter": "A",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "B",
        "hi": "मध्य प्रदेश",
        "en": "Madhya Pradesh"
      },
      {
        "letter": "C",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "D",
        "hi": "बिहार",
        "en": "Bihar"
      }
    ],
    "correct": "B",
    "exp_hi": "नंदन वन (Nandan Van) मध्य प्रदेश में है।",
    "exp_en": "Nandan Van is in Madhya Pradesh.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का कौन सा राज्य सबसे अधिक खनिज उत्पादन करता है?",
    "q_en": "Which state produces most minerals in India?",
    "options": [
      {
        "letter": "A",
        "hi": "झारखंड",
        "en": "Jharkhand"
      },
      {
        "letter": "B",
        "hi": "छत्तीसगढ़",
        "en": "Chhattisgarh"
      },
      {
        "letter": "C",
        "hi": "ओडिशा",
        "en": "Odisha"
      },
      {
        "letter": "D",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      }
    ],
    "correct": "A",
    "exp_hi": "झारखंड भारत में सबसे अधिक खनिज उत्पादन करता है।",
    "exp_en": "Jharkhand produces most minerals in India.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में बॉक्साइट का सबसे बड़ा उत्पादक?",
    "q_en": "Largest bauxite producer in India?",
    "options": [
      {
        "letter": "A",
        "hi": "झारखंड",
        "en": "Jharkhand"
      },
      {
        "letter": "B",
        "hi": "ओडिशा",
        "en": "Odisha"
      },
      {
        "letter": "C",
        "hi": "छत्तीसगढ़",
        "en": "Chhattisgarh"
      },
      {
        "letter": "D",
        "hi": "गुजरात",
        "en": "Gujarat"
      }
    ],
    "correct": "B",
    "exp_hi": "ओडिशा भारत का सबसे बड़ा बॉक्साइट उत्पादक है।",
    "exp_en": "Odisha is India's largest bauxite producer.",
    "exam_tag": "CTET 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'नीली क्रांति' का संबंध किससे है?",
    "q_en": "Blue Revolution in India is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "जल संरक्षण",
        "en": "Water conservation"
      },
      {
        "letter": "B",
        "hi": "मत्स्य पालन",
        "en": "Fisheries"
      },
      {
        "letter": "C",
        "hi": "नीली मिट्टी",
        "en": "Blue soil"
      },
      {
        "letter": "D",
        "hi": "नदी सफाई",
        "en": "River cleaning"
      }
    ],
    "correct": "B",
    "exp_hi": "नीली क्रांति मत्स्य पालन से संबंधित है।",
    "exp_en": "Blue Revolution is related to fisheries.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "लक्षद्वीप की राजधानी?",
    "q_en": "Capital of Lakshadweep?",
    "options": [
      {
        "letter": "A",
        "hi": "मिनिकॉय",
        "en": "Minicoy"
      },
      {
        "letter": "B",
        "hi": "कवरत्ती",
        "en": "Kavaratti"
      },
      {
        "letter": "C",
        "hi": "अगत्ती",
        "en": "Agatti"
      },
      {
        "letter": "D",
        "hi": "अमिनी",
        "en": "Amini"
      }
    ],
    "correct": "B",
    "exp_hi": "कवरत्ती लक्षद्वीप की राजधानी है।",
    "exp_en": "Kavaratti is the capital of Lakshadweep.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "अंडमान-निकोबार द्वीप समूह की राजधानी?",
    "q_en": "Capital of Andaman-Nicobar?",
    "options": [
      {
        "letter": "A",
        "hi": "पोर्ट ब्लेयर",
        "en": "Port Blair"
      },
      {
        "letter": "B",
        "hi": "कार निकोबार",
        "en": "Car Nicobar"
      },
      {
        "letter": "C",
        "hi": "नील द्वीप",
        "en": "Neil Island"
      },
      {
        "letter": "D",
        "hi": "हैवलॉक",
        "en": "Havelock"
      }
    ],
    "correct": "A",
    "exp_hi": "पोर्ट ब्लेयर अंडमान-निकोबार की राजधानी है।",
    "exp_en": "Port Blair is the capital of Andaman-Nicobar.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत का राष्ट्रीय खेल?",
    "q_en": "National game of India?",
    "options": [
      {
        "letter": "A",
        "hi": "क्रिकेट",
        "en": "Cricket"
      },
      {
        "letter": "B",
        "hi": "हॉकी",
        "en": "Hockey"
      },
      {
        "letter": "C",
        "hi": "कबड्डी",
        "en": "Kabaddi"
      },
      {
        "letter": "D",
        "hi": "फुटबॉल",
        "en": "Football"
      }
    ],
    "correct": "B",
    "exp_hi": "हॉकी भारत का राष्ट्रीय खेल है।",
    "exp_en": "Hockey is India's national sport.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 6"
  },
  {
    "subject": "geography",
    "q_hi": "वैगई नदी किस राज्य में है?",
    "q_en": "Vaigai river is in which state?",
    "options": [
      {
        "letter": "A",
        "hi": "केरल",
        "en": "Kerala"
      },
      {
        "letter": "B",
        "hi": "तमिलनाडु",
        "en": "Tamil Nadu"
      },
      {
        "letter": "C",
        "hi": "कर्नाटक",
        "en": "Karnataka"
      },
      {
        "letter": "D",
        "hi": "आंध्र प्रदेश",
        "en": "Andhra Pradesh"
      }
    ],
    "correct": "B",
    "exp_hi": "वैगई नदी तमिलनाडु में है।",
    "exp_en": "Vaigai river is in Tamil Nadu.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 7"
  },
  {
    "subject": "geography",
    "q_hi": "हैदराबाद किस नदी के किनारे है?",
    "q_en": "Hyderabad is on the banks of which river?",
    "options": [
      {
        "letter": "A",
        "hi": "कृष्णा",
        "en": "Krishna"
      },
      {
        "letter": "B",
        "hi": "मूसी",
        "en": "Musi"
      },
      {
        "letter": "C",
        "hi": "गोदावरी",
        "en": "Godavari"
      },
      {
        "letter": "D",
        "hi": "तुंगभद्रा",
        "en": "Tungabhadra"
      }
    ],
    "correct": "B",
    "exp_hi": "हैदराबाद मूसी नदी के किनारे है।",
    "exp_en": "Hyderabad is on the banks of Musi river.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 8"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में पटसन की खेती सबसे अधिक कहाँ होती है?",
    "q_en": "Maximum jute cultivation in India?",
    "options": [
      {
        "letter": "A",
        "hi": "असम",
        "en": "Assam"
      },
      {
        "letter": "B",
        "hi": "पश्चिम बंगाल",
        "en": "West Bengal"
      },
      {
        "letter": "C",
        "hi": "बिहार",
        "en": "Bihar"
      },
      {
        "letter": "D",
        "hi": "ओडिशा",
        "en": "Odisha"
      }
    ],
    "correct": "B",
    "exp_hi": "पश्चिम बंगाल में सर्वाधिक पटसन होती है।",
    "exp_en": "West Bengal has maximum jute cultivation.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 9"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'ऑपरेशन ग्रीन' किससे संबंधित है?",
    "q_en": "Operation Green in India is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "वन संरक्षण",
        "en": "Forest conservation"
      },
      {
        "letter": "B",
        "hi": "टमाटर, प्याज, आलू",
        "en": "Tomato, Onion, Potato"
      },
      {
        "letter": "C",
        "hi": "हरित ऊर्जा",
        "en": "Green energy"
      },
      {
        "letter": "D",
        "hi": "पर्यावरण",
        "en": "Environment"
      }
    ],
    "correct": "B",
    "exp_hi": "ऑपरेशन ग्रीन TOP (Tomato, Onion, Potato) से संबंधित है।",
    "exp_en": "Operation Green is related to TOP (Tomato, Onion, Potato).",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'कॉफी बोर्ड' का मुख्यालय कहाँ है?",
    "q_en": "Coffee Board headquarters in India?",
    "options": [
      {
        "letter": "A",
        "hi": "चेन्नई",
        "en": "Chennai"
      },
      {
        "letter": "B",
        "hi": "बेंगलुरु",
        "en": "Bengaluru"
      },
      {
        "letter": "C",
        "hi": "मैसूर",
        "en": "Mysuru"
      },
      {
        "letter": "D",
        "hi": "कोच्चि",
        "en": "Kochi"
      }
    ],
    "correct": "B",
    "exp_hi": "कॉफी बोर्ड का मुख्यालय बेंगलुरु में है।",
    "exp_en": "Coffee Board headquarters is in Bengaluru.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में 'रबर बोर्ड' का मुख्यालय कहाँ है?",
    "q_en": "Rubber Board headquarters in India?",
    "options": [
      {
        "letter": "A",
        "hi": "कोच्चि",
        "en": "Kochi"
      },
      {
        "letter": "B",
        "hi": "त्रिवेंद्रम",
        "en": "Thiruvananthapuram"
      },
      {
        "letter": "C",
        "hi": "कोझिकोड",
        "en": "Kozhikode"
      },
      {
        "letter": "D",
        "hi": "मुंबई",
        "en": "Mumbai"
      }
    ],
    "correct": "A",
    "exp_hi": "रबर बोर्ड का मुख्यालय कोच्चि में है।",
    "exp_en": "Rubber Board headquarters is in Kochi.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "geography",
    "q_hi": "भारत में मुंबई उच्च किसके लिए प्रसिद्ध है?",
    "q_en": "Mumbai High is famous for?",
    "options": [
      {
        "letter": "A",
        "hi": "मत्स्य पालन",
        "en": "Fisheries"
      },
      {
        "letter": "B",
        "hi": "तेल और गैस",
        "en": "Oil and gas"
      },
      {
        "letter": "C",
        "hi": "पर्यटन",
        "en": "Tourism"
      },
      {
        "letter": "D",
        "hi": "बंदरगाह",
        "en": "Port"
      }
    ],
    "correct": "B",
    "exp_hi": "मुंबई हाई अरब सागर में तेल और गैस उत्पादन के लिए प्रसिद्ध है।",
    "exp_en": "Mumbai High is famous for oil and gas production in Arabian Sea.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारत का संविधान कब लागू हुआ?",
    "q_en": "When did Indian Constitution come into effect?",
    "options": [
      {
        "letter": "A",
        "hi": "15 अगस्त 1947",
        "en": "15 August 1947"
      },
      {
        "letter": "B",
        "hi": "26 जनवरी 1950",
        "en": "26 January 1950"
      },
      {
        "letter": "C",
        "hi": "26 नवंबर 1949",
        "en": "26 November 1949"
      },
      {
        "letter": "D",
        "hi": "2 अक्टूबर 1950",
        "en": "2 October 1950"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत का संविधान 26 जनवरी 1950 को लागू हुआ।",
    "exp_en": "Indian Constitution came into effect on 26 January 1950.",
    "exam_tag": "UPSC 2019",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारत के प्रथम राष्ट्रपति कौन थे?",
    "q_en": "First President of India?",
    "options": [
      {
        "letter": "A",
        "hi": "जवाहरलाल नेहरू",
        "en": "Jawaharlal Nehru"
      },
      {
        "letter": "B",
        "hi": "डॉ. राजेंद्र प्रसाद",
        "en": "Dr. Rajendra Prasad"
      },
      {
        "letter": "C",
        "hi": "सरदार पटेल",
        "en": "Sardar Patel"
      },
      {
        "letter": "D",
        "hi": "डॉ. अंबेडकर",
        "en": "Dr. Ambedkar"
      }
    ],
    "correct": "B",
    "exp_hi": "डॉ. राजेंद्र प्रसाद भारत के प्रथम राष्ट्रपति थे।",
    "exp_en": "Dr. Rajendra Prasad was first President of India.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "लोकसभा में कुल कितनी सीटें हैं?",
    "q_en": "Total seats in Lok Sabha?",
    "options": [
      {
        "letter": "A",
        "hi": "542",
        "en": "542"
      },
      {
        "letter": "B",
        "hi": "545",
        "en": "545"
      },
      {
        "letter": "C",
        "hi": "543",
        "en": "543"
      },
      {
        "letter": "D",
        "hi": "550",
        "en": "550"
      }
    ],
    "correct": "C",
    "exp_hi": "लोकसभा में 543 निर्वाचित सीटें हैं।",
    "exp_en": "Lok Sabha has 543 elected seats.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारतीय संविधान में मौलिक अधिकार कितने हैं?",
    "q_en": "Fundamental Rights in Indian Constitution?",
    "options": [
      {
        "letter": "A",
        "hi": "5",
        "en": "5"
      },
      {
        "letter": "B",
        "hi": "6",
        "en": "6"
      },
      {
        "letter": "C",
        "hi": "7",
        "en": "7"
      },
      {
        "letter": "D",
        "hi": "8",
        "en": "8"
      }
    ],
    "correct": "B",
    "exp_hi": "भारतीय संविधान में 6 मौलिक अधिकार हैं।",
    "exp_en": "There are 6 Fundamental Rights.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "संविधान के जनक कौन हैं?",
    "q_en": "Father of Indian Constitution?",
    "options": [
      {
        "letter": "A",
        "hi": "जवाहरलाल नेहरू",
        "en": "Jawaharlal Nehru"
      },
      {
        "letter": "B",
        "hi": "डॉ. बी.आर. अंबेडकर",
        "en": "Dr. B.R. Ambedkar"
      },
      {
        "letter": "C",
        "hi": "सरदार पटेल",
        "en": "Sardar Patel"
      },
      {
        "letter": "D",
        "hi": "राजेंद्र प्रसाद",
        "en": "Rajendra Prasad"
      }
    ],
    "correct": "B",
    "exp_hi": "डॉ. बी.आर. अंबेडकर को भारतीय संविधान का जनक कहते हैं।",
    "exp_en": "Dr. B.R. Ambedkar is called Father of Indian Constitution.",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "संविधान सभा के अध्यक्ष कौन थे?",
    "q_en": "President of Constituent Assembly?",
    "options": [
      {
        "letter": "A",
        "hi": "डॉ. अंबेडकर",
        "en": "Dr. Ambedkar"
      },
      {
        "letter": "B",
        "hi": "डॉ. राजेंद्र प्रसाद",
        "en": "Dr. Rajendra Prasad"
      },
      {
        "letter": "C",
        "hi": "जवाहरलाल नेहरू",
        "en": "Jawaharlal Nehru"
      },
      {
        "letter": "D",
        "hi": "सरदार पटेल",
        "en": "Sardar Patel"
      }
    ],
    "correct": "B",
    "exp_hi": "डॉ. राजेंद्र प्रसाद संविधान सभा के अध्यक्ष थे।",
    "exp_en": "Dr. Rajendra Prasad was President of Constituent Assembly.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारत का संविधान कितने समय में बना?",
    "q_en": "How long did it take to make Indian Constitution?",
    "options": [
      {
        "letter": "A",
        "hi": "2 साल 10 महीने 18 दिन",
        "en": "2 years 10 months 18 days"
      },
      {
        "letter": "B",
        "hi": "3 साल 2 महीने",
        "en": "3 years 2 months"
      },
      {
        "letter": "C",
        "hi": "2 साल 6 महीने",
        "en": "2 years 6 months"
      },
      {
        "letter": "D",
        "hi": "4 साल",
        "en": "4 years"
      }
    ],
    "correct": "A",
    "exp_hi": "भारत का संविधान 2 साल 10 महीने 18 दिन में बना।",
    "exp_en": "Indian Constitution was made in 2 years 10 months 18 days.",
    "exam_tag": "CTET 2019",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "संविधान को किस तिथि को अपनाया गया?",
    "q_en": "When was Constitution adopted?",
    "options": [
      {
        "letter": "A",
        "hi": "26 जनवरी 1950",
        "en": "26 January 1950"
      },
      {
        "letter": "B",
        "hi": "26 नवंबर 1949",
        "en": "26 November 1949"
      },
      {
        "letter": "C",
        "hi": "15 अगस्त 1947",
        "en": "15 August 1947"
      },
      {
        "letter": "D",
        "hi": "2 अक्टूबर 1949",
        "en": "2 October 1949"
      }
    ],
    "correct": "B",
    "exp_hi": "संविधान को 26 नवंबर 1949 को अपनाया गया।",
    "exp_en": "Constitution was adopted on 26 November 1949.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारत के नागरिकों को कितने मौलिक कर्तव्य हैं?",
    "q_en": "How many Fundamental Duties do Indian citizens have?",
    "options": [
      {
        "letter": "A",
        "hi": "10",
        "en": "10"
      },
      {
        "letter": "B",
        "hi": "11",
        "en": "11"
      },
      {
        "letter": "C",
        "hi": "12",
        "en": "12"
      },
      {
        "letter": "D",
        "hi": "9",
        "en": "9"
      }
    ],
    "correct": "B",
    "exp_hi": "भारतीय संविधान में 11 मौलिक कर्तव्य हैं।",
    "exp_en": "Indian Constitution has 11 Fundamental Duties.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में राष्ट्रीय आपातकाल की पहली घोषणा कब हुई?",
    "q_en": "When was first National Emergency in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1962",
        "en": "1962"
      },
      {
        "letter": "B",
        "hi": "1965",
        "en": "1965"
      },
      {
        "letter": "C",
        "hi": "1971",
        "en": "1971"
      },
      {
        "letter": "D",
        "hi": "1975",
        "en": "1975"
      }
    ],
    "correct": "A",
    "exp_hi": "भारत में पहला राष्ट्रीय आपातकाल 1962 में चीन युद्ध के समय लगा।",
    "exp_en": "First National Emergency in India was in 1962 during China war.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "मताधिकार की आयु 21 से 18 कब की गई?",
    "q_en": "When was voting age reduced from 21 to 18?",
    "options": [
      {
        "letter": "A",
        "hi": "1984",
        "en": "1984"
      },
      {
        "letter": "B",
        "hi": "1988",
        "en": "1988"
      },
      {
        "letter": "C",
        "hi": "1989",
        "en": "1989"
      },
      {
        "letter": "D",
        "hi": "1991",
        "en": "1991"
      }
    ],
    "correct": "C",
    "exp_hi": "61वें संशोधन (1989) से मतदान आयु 21 से 18 की गई।",
    "exp_en": "61st Amendment (1989) reduced voting age from 21 to 18.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "समानता का अधिकार किस अनुच्छेद में है?",
    "q_en": "Right to equality is in which article?",
    "options": [
      {
        "letter": "A",
        "hi": "अनुच्छेद 12-18",
        "en": "Article 12-18"
      },
      {
        "letter": "B",
        "hi": "अनुच्छेद 14-18",
        "en": "Article 14-18"
      },
      {
        "letter": "C",
        "hi": "अनुच्छेद 19-22",
        "en": "Article 19-22"
      },
      {
        "letter": "D",
        "hi": "अनुच्छेद 23-24",
        "en": "Article 23-24"
      }
    ],
    "correct": "B",
    "exp_hi": "समानता का अधिकार अनुच्छेद 14-18 में है।",
    "exp_en": "Right to equality is in Article 14-18.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "पंचायती राज किस अनुच्छेद से संबंधित है?",
    "q_en": "Panchayati Raj is related to which article?",
    "options": [
      {
        "letter": "A",
        "hi": "अनुच्छेद 40",
        "en": "Article 40"
      },
      {
        "letter": "B",
        "hi": "अनुच्छेद 243",
        "en": "Article 243"
      },
      {
        "letter": "C",
        "hi": "अनुच्छेद 356",
        "en": "Article 356"
      },
      {
        "letter": "D",
        "hi": "अनुच्छेद 370",
        "en": "Article 370"
      }
    ],
    "correct": "B",
    "exp_hi": "पंचायती राज अनुच्छेद 243 से संबंधित है।",
    "exp_en": "Panchayati Raj is related to Article 243.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "अनुच्छेद 21 किससे संबंधित है?",
    "q_en": "Article 21 is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "समानता का अधिकार",
        "en": "Right to equality"
      },
      {
        "letter": "B",
        "hi": "जीवन और व्यक्तिगत स्वतंत्रता",
        "en": "Right to life and personal liberty"
      },
      {
        "letter": "C",
        "hi": "धर्म की स्वतंत्रता",
        "en": "Freedom of religion"
      },
      {
        "letter": "D",
        "hi": "शिक्षा का अधिकार",
        "en": "Right to education"
      }
    ],
    "correct": "B",
    "exp_hi": "अनुच्छेद 21 जीवन और व्यक्तिगत स्वतंत्रता से संबंधित है।",
    "exp_en": "Article 21 is related to right to life and personal liberty.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में किस राज्य में विधान परिषद नहीं है?",
    "q_en": "Which state does NOT have Legislative Council?",
    "options": [
      {
        "letter": "A",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "B",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      },
      {
        "letter": "C",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "D",
        "hi": "बिहार",
        "en": "Bihar"
      }
    ],
    "correct": "C",
    "exp_hi": "राजस्थान में केवल विधानसभा है, विधान परिषद नहीं।",
    "exp_en": "Rajasthan has only Vidhan Sabha, no Legislative Council.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारत के मुख्य न्यायाधीश की नियुक्ति कौन करता है?",
    "q_en": "Who appoints Chief Justice of India?",
    "options": [
      {
        "letter": "A",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "B",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "C",
        "hi": "संसद",
        "en": "Parliament"
      },
      {
        "letter": "D",
        "hi": "उपराष्ट्रपति",
        "en": "Vice President"
      }
    ],
    "correct": "B",
    "exp_hi": "राष्ट्रपति मुख्य न्यायाधीश की नियुक्ति करते हैं।",
    "exp_en": "President appoints the Chief Justice of India.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "राज्यसभा में कुल कितनी सीटें हैं?",
    "q_en": "Total seats in Rajya Sabha?",
    "options": [
      {
        "letter": "A",
        "hi": "245",
        "en": "245"
      },
      {
        "letter": "B",
        "hi": "250",
        "en": "250"
      },
      {
        "letter": "C",
        "hi": "238",
        "en": "238"
      },
      {
        "letter": "D",
        "hi": "260",
        "en": "260"
      }
    ],
    "correct": "A",
    "exp_hi": "राज्यसभा में वर्तमान में 245 सीटें हैं।",
    "exp_en": "Rajya Sabha currently has 245 seats.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "राज्यसभा के सभापति कौन होते हैं?",
    "q_en": "Who is Chairman of Rajya Sabha?",
    "options": [
      {
        "letter": "A",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "B",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "C",
        "hi": "उपराष्ट्रपति",
        "en": "Vice President"
      },
      {
        "letter": "D",
        "hi": "लोकसभा अध्यक्ष",
        "en": "Lok Sabha Speaker"
      }
    ],
    "correct": "C",
    "exp_hi": "उपराष्ट्रपति राज्यसभा के पदेन सभापति हैं।",
    "exp_en": "Vice President is ex-officio Chairman of Rajya Sabha.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में पहले आम चुनाव कब हुए?",
    "q_en": "When were first general elections in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1950",
        "en": "1950"
      },
      {
        "letter": "B",
        "hi": "1951-52",
        "en": "1951-52"
      },
      {
        "letter": "C",
        "hi": "1953",
        "en": "1953"
      },
      {
        "letter": "D",
        "hi": "1955",
        "en": "1955"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत में पहले आम चुनाव 1951-52 में हुए।",
    "exp_en": "First general elections in India were in 1951-52.",
    "exam_tag": "UPSC 2018",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारत का महान्यायवादी किसके द्वारा नियुक्त होता है?",
    "q_en": "Who appoints Attorney General of India?",
    "options": [
      {
        "letter": "A",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "B",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "C",
        "hi": "सुप्रीम कोर्ट",
        "en": "Supreme Court"
      },
      {
        "letter": "D",
        "hi": "लोकसभा",
        "en": "Lok Sabha"
      }
    ],
    "correct": "B",
    "exp_hi": "महान्यायवादी राष्ट्रपति द्वारा नियुक्त होता है।",
    "exp_en": "Attorney General is appointed by President.",
    "exam_tag": "SSC 2018",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "मौलिक कर्तव्य किस संशोधन से जोड़े गए?",
    "q_en": "Fundamental Duties were added by which amendment?",
    "options": [
      {
        "letter": "A",
        "hi": "40वाँ",
        "en": "40th"
      },
      {
        "letter": "B",
        "hi": "42वाँ",
        "en": "42nd"
      },
      {
        "letter": "C",
        "hi": "44वाँ",
        "en": "44th"
      },
      {
        "letter": "D",
        "hi": "46वाँ",
        "en": "46th"
      }
    ],
    "correct": "B",
    "exp_hi": "मौलिक कर्तव्य 42वें संशोधन (1976) से जोड़े गए।",
    "exp_en": "Fundamental Duties were added by 42nd Amendment (1976).",
    "exam_tag": "CTET 2020",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में मतदान की आयु कितनी है?",
    "q_en": "Voting age in India?",
    "options": [
      {
        "letter": "A",
        "hi": "18 वर्ष",
        "en": "18 years"
      },
      {
        "letter": "B",
        "hi": "21 वर्ष",
        "en": "21 years"
      },
      {
        "letter": "C",
        "hi": "25 वर्ष",
        "en": "25 years"
      },
      {
        "letter": "D",
        "hi": "20 वर्ष",
        "en": "20 years"
      }
    ],
    "correct": "A",
    "exp_hi": "भारत में 18 वर्ष में मतदान का अधिकार मिलता है।",
    "exp_en": "Voting age in India is 18 years.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "लोकसभा का कार्यकाल कितना होता है?",
    "q_en": "Term of Lok Sabha?",
    "options": [
      {
        "letter": "A",
        "hi": "4 साल",
        "en": "4 years"
      },
      {
        "letter": "B",
        "hi": "5 साल",
        "en": "5 years"
      },
      {
        "letter": "C",
        "hi": "6 साल",
        "en": "6 years"
      },
      {
        "letter": "D",
        "hi": "3 साल",
        "en": "3 years"
      }
    ],
    "correct": "B",
    "exp_hi": "लोकसभा का सामान्य कार्यकाल 5 साल होता है।",
    "exp_en": "Normal term of Lok Sabha is 5 years.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "प्रस्तावना को संविधान की क्या कहते हैं?",
    "q_en": "Preamble is called what of Constitution?",
    "options": [
      {
        "letter": "A",
        "hi": "परिचय",
        "en": "Introduction"
      },
      {
        "letter": "B",
        "hi": "आत्मा",
        "en": "Soul"
      },
      {
        "letter": "C",
        "hi": "आधार",
        "en": "Base"
      },
      {
        "letter": "D",
        "hi": "अनुसूची",
        "en": "Schedule"
      }
    ],
    "correct": "B",
    "exp_hi": "प्रस्तावना को संविधान की आत्मा कहते हैं।",
    "exp_en": "Preamble is called the soul of the Constitution.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "अनुच्छेद 370 किस राज्य से संबंधित था?",
    "q_en": "Article 370 was related to which state?",
    "options": [
      {
        "letter": "A",
        "hi": "हिमाचल प्रदेश",
        "en": "Himachal Pradesh"
      },
      {
        "letter": "B",
        "hi": "जम्मू-कश्मीर",
        "en": "Jammu-Kashmir"
      },
      {
        "letter": "C",
        "hi": "उत्तराखंड",
        "en": "Uttarakhand"
      },
      {
        "letter": "D",
        "hi": "सिक्किम",
        "en": "Sikkim"
      }
    ],
    "correct": "B",
    "exp_hi": "अनुच्छेद 370 जम्मू-कश्मीर को विशेष दर्जा देता था।",
    "exp_en": "Article 370 gave special status to J&K.",
    "exam_tag": "CTET 2021",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "लोकसभा अध्यक्ष को कौन चुनता है?",
    "q_en": "Who elects Lok Sabha Speaker?",
    "options": [
      {
        "letter": "A",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "B",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "C",
        "hi": "लोकसभा सदस्य",
        "en": "Lok Sabha members"
      },
      {
        "letter": "D",
        "hi": "संसद के दोनों सदन",
        "en": "Both houses"
      }
    ],
    "correct": "C",
    "exp_hi": "लोकसभा अध्यक्ष को लोकसभा सदस्य चुनते हैं।",
    "exp_en": "Lok Sabha Speaker is elected by Lok Sabha members.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारत के पहले लोकसभा अध्यक्ष कौन थे?",
    "q_en": "First Speaker of Lok Sabha?",
    "options": [
      {
        "letter": "A",
        "hi": "जी.वी. मावलंकर",
        "en": "G.V. Mavalankar"
      },
      {
        "letter": "B",
        "hi": "एम.ए. अय्यंगार",
        "en": "M.A. Ayyangar"
      },
      {
        "letter": "C",
        "hi": "हुकुम सिंह",
        "en": "Hukam Singh"
      },
      {
        "letter": "D",
        "hi": "बलि राम भगत",
        "en": "Bali Ram Bhagat"
      }
    ],
    "correct": "A",
    "exp_hi": "जी.वी. मावलंकर लोकसभा के पहले अध्यक्ष थे।",
    "exp_en": "G.V. Mavalankar was the first Speaker of Lok Sabha.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में योजना आयोग की जगह किसने ली?",
    "q_en": "What replaced Planning Commission?",
    "options": [
      {
        "letter": "A",
        "hi": "वित्त आयोग",
        "en": "Finance Commission"
      },
      {
        "letter": "B",
        "hi": "नीति आयोग",
        "en": "NITI Aayog"
      },
      {
        "letter": "C",
        "hi": "आर्थिक सलाहकार परिषद",
        "en": "Economic Advisory Council"
      },
      {
        "letter": "D",
        "hi": "राष्ट्रीय विकास परिषद",
        "en": "National Development Council"
      }
    ],
    "correct": "B",
    "exp_hi": "2015 में NITI Aayog ने योजना आयोग की जगह ली।",
    "exp_en": "NITI Aayog replaced Planning Commission in 2015.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में सर्वोच्च न्यायालय कहाँ है?",
    "q_en": "Where is Supreme Court of India?",
    "options": [
      {
        "letter": "A",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "B",
        "hi": "नई दिल्ली",
        "en": "New Delhi"
      },
      {
        "letter": "C",
        "hi": "कोलकाता",
        "en": "Kolkata"
      },
      {
        "letter": "D",
        "hi": "चेन्नई",
        "en": "Chennai"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत का सर्वोच्च न्यायालय नई दिल्ली में है।",
    "exp_en": "Supreme Court of India is in New Delhi.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारतीय संसद के कितने सदन हैं?",
    "q_en": "How many houses in Indian Parliament?",
    "options": [
      {
        "letter": "A",
        "hi": "1",
        "en": "1"
      },
      {
        "letter": "B",
        "hi": "2",
        "en": "2"
      },
      {
        "letter": "C",
        "hi": "3",
        "en": "3"
      },
      {
        "letter": "D",
        "hi": "4",
        "en": "4"
      }
    ],
    "correct": "B",
    "exp_hi": "भारतीय संसद के दो सदन हैं - लोकसभा और राज्यसभा।",
    "exp_en": "Indian Parliament has two houses.",
    "exam_tag": "UPSC 2017",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "उपराष्ट्रपति का कार्यकाल कितना होता है?",
    "q_en": "Term of Vice President?",
    "options": [
      {
        "letter": "A",
        "hi": "4 साल",
        "en": "4 years"
      },
      {
        "letter": "B",
        "hi": "5 साल",
        "en": "5 years"
      },
      {
        "letter": "C",
        "hi": "6 साल",
        "en": "6 years"
      },
      {
        "letter": "D",
        "hi": "3 साल",
        "en": "3 years"
      }
    ],
    "correct": "B",
    "exp_hi": "उपराष्ट्रपति का कार्यकाल 5 साल होता है।",
    "exp_en": "Vice President has a term of 5 years.",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत के प्रथम उपप्रधानमंत्री कौन थे?",
    "q_en": "First Deputy PM of India?",
    "options": [
      {
        "letter": "A",
        "hi": "जवाहरलाल नेहरू",
        "en": "Jawaharlal Nehru"
      },
      {
        "letter": "B",
        "hi": "सरदार पटेल",
        "en": "Sardar Patel"
      },
      {
        "letter": "C",
        "hi": "मोरारजी देसाई",
        "en": "Morarji Desai"
      },
      {
        "letter": "D",
        "hi": "जगजीवन राम",
        "en": "Jagjivan Ram"
      }
    ],
    "correct": "B",
    "exp_hi": "सरदार पटेल भारत के प्रथम उपप्रधानमंत्री थे।",
    "exp_en": "Sardar Patel was first Deputy PM of India.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारतीय संविधान कितने भागों में विभाजित है?",
    "q_en": "Indian Constitution divided into how many parts?",
    "options": [
      {
        "letter": "A",
        "hi": "20",
        "en": "20"
      },
      {
        "letter": "B",
        "hi": "22",
        "en": "22"
      },
      {
        "letter": "C",
        "hi": "25",
        "en": "25"
      },
      {
        "letter": "D",
        "hi": "28",
        "en": "28"
      }
    ],
    "correct": "B",
    "exp_hi": "भारतीय संविधान में मूलतः 22 भाग थे।",
    "exp_en": "Indian Constitution originally had 22 parts.",
    "exam_tag": "UPSC 2019",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "राष्ट्रपति का कार्यकाल कितना होता है?",
    "q_en": "Term of President of India?",
    "options": [
      {
        "letter": "A",
        "hi": "4 साल",
        "en": "4 years"
      },
      {
        "letter": "B",
        "hi": "5 साल",
        "en": "5 years"
      },
      {
        "letter": "C",
        "hi": "6 साल",
        "en": "6 years"
      },
      {
        "letter": "D",
        "hi": "3 साल",
        "en": "3 years"
      }
    ],
    "correct": "B",
    "exp_hi": "राष्ट्रपति का कार्यकाल 5 साल होता है।",
    "exp_en": "President has a term of 5 years.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में लोकसभा की न्यूनतम आयु कितनी है?",
    "q_en": "Minimum age for Lok Sabha membership?",
    "options": [
      {
        "letter": "A",
        "hi": "21",
        "en": "21"
      },
      {
        "letter": "B",
        "hi": "25",
        "en": "25"
      },
      {
        "letter": "C",
        "hi": "30",
        "en": "30"
      },
      {
        "letter": "D",
        "hi": "35",
        "en": "35"
      }
    ],
    "correct": "B",
    "exp_hi": "लोकसभा सदस्य बनने की न्यूनतम आयु 25 वर्ष है।",
    "exp_en": "Minimum age for Lok Sabha membership is 25 years.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में राज्यसभा की न्यूनतम आयु कितनी है?",
    "q_en": "Minimum age for Rajya Sabha membership?",
    "options": [
      {
        "letter": "A",
        "hi": "25",
        "en": "25"
      },
      {
        "letter": "B",
        "hi": "30",
        "en": "30"
      },
      {
        "letter": "C",
        "hi": "35",
        "en": "35"
      },
      {
        "letter": "D",
        "hi": "21",
        "en": "21"
      }
    ],
    "correct": "B",
    "exp_hi": "राज्यसभा सदस्य बनने की न्यूनतम आयु 30 वर्ष है।",
    "exp_en": "Minimum age for Rajya Sabha membership is 30 years.",
    "exam_tag": "CTET 2021",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारतीय चुनाव आयोग की स्थापना कब हुई?",
    "q_en": "When was Election Commission of India established?",
    "options": [
      {
        "letter": "A",
        "hi": "1949",
        "en": "1949"
      },
      {
        "letter": "B",
        "hi": "1950",
        "en": "1950"
      },
      {
        "letter": "C",
        "hi": "1951",
        "en": "1951"
      },
      {
        "letter": "D",
        "hi": "1952",
        "en": "1952"
      }
    ],
    "correct": "B",
    "exp_hi": "भारतीय चुनाव आयोग की स्थापना 25 जनवरी 1950 को हुई।",
    "exp_en": "Election Commission of India was established on 25 January 1950.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत के प्रथम मुख्य चुनाव आयुक्त कौन थे?",
    "q_en": "First Chief Election Commissioner of India?",
    "options": [
      {
        "letter": "A",
        "hi": "सुकुमार सेन",
        "en": "Sukumar Sen"
      },
      {
        "letter": "B",
        "hi": "के.वी.के. सुंदरम",
        "en": "K.V.K. Sundaram"
      },
      {
        "letter": "C",
        "hi": "एस.पी. सेन वर्मा",
        "en": "S.P. Sen Verma"
      },
      {
        "letter": "D",
        "hi": "टी. स्वामीनाथन",
        "en": "T. Swaminathan"
      }
    ],
    "correct": "A",
    "exp_hi": "सुकुमार सेन भारत के प्रथम मुख्य चुनाव आयुक्त थे।",
    "exp_en": "Sukumar Sen was first Chief Election Commissioner.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "संविधान की प्रस्तावना में 'समाजवाद' और 'धर्मनिरपेक्षता' कब जोड़े गए?",
    "q_en": "When were 'Socialist' and 'Secular' added to preamble?",
    "options": [
      {
        "letter": "A",
        "hi": "1971",
        "en": "1971"
      },
      {
        "letter": "B",
        "hi": "1976",
        "en": "1976"
      },
      {
        "letter": "C",
        "hi": "1978",
        "en": "1978"
      },
      {
        "letter": "D",
        "hi": "1984",
        "en": "1984"
      }
    ],
    "correct": "B",
    "exp_hi": "42वें संशोधन (1976) में ये शब्द जोड़े गए।",
    "exp_en": "These words were added in 42nd Amendment (1976).",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "संविधान में कितनी अनुसूचियाँ हैं?",
    "q_en": "How many schedules in Indian Constitution?",
    "options": [
      {
        "letter": "A",
        "hi": "10",
        "en": "10"
      },
      {
        "letter": "B",
        "hi": "12",
        "en": "12"
      },
      {
        "letter": "C",
        "hi": "8",
        "en": "8"
      },
      {
        "letter": "D",
        "hi": "14",
        "en": "14"
      }
    ],
    "correct": "B",
    "exp_hi": "भारतीय संविधान में 12 अनुसूचियाँ हैं।",
    "exp_en": "Indian Constitution has 12 schedules.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत का राजकीय भाषा क्या है?",
    "q_en": "Official language of India?",
    "options": [
      {
        "letter": "A",
        "hi": "हिंदी",
        "en": "Hindi"
      },
      {
        "letter": "B",
        "hi": "अंग्रेजी",
        "en": "English"
      },
      {
        "letter": "C",
        "hi": "हिंदी और अंग्रेजी",
        "en": "Hindi and English"
      },
      {
        "letter": "D",
        "hi": "संस्कृत",
        "en": "Sanskrit"
      }
    ],
    "correct": "C",
    "exp_hi": "भारत की राजभाषा हिंदी और अंग्रेजी दोनों हैं।",
    "exp_en": "Hindi and English both are official languages of India.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में कितने High Courts हैं?",
    "q_en": "How many High Courts in India?",
    "options": [
      {
        "letter": "A",
        "hi": "21",
        "en": "21"
      },
      {
        "letter": "B",
        "hi": "23",
        "en": "23"
      },
      {
        "letter": "C",
        "hi": "25",
        "en": "25"
      },
      {
        "letter": "D",
        "hi": "28",
        "en": "28"
      }
    ],
    "correct": "C",
    "exp_hi": "भारत में 25 उच्च न्यायालय हैं।",
    "exp_en": "India has 25 High Courts.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "नीति आयोग की स्थापना कब हुई?",
    "q_en": "When was NITI Aayog established?",
    "options": [
      {
        "letter": "A",
        "hi": "2013",
        "en": "2013"
      },
      {
        "letter": "B",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "C",
        "hi": "2015",
        "en": "2015"
      },
      {
        "letter": "D",
        "hi": "2016",
        "en": "2016"
      }
    ],
    "correct": "C",
    "exp_hi": "NITI Aayog की स्थापना 1 जनवरी 2015 को हुई।",
    "exp_en": "NITI Aayog was established on 1 January 2015.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत के राष्ट्रपति को शपथ कौन दिलाता है?",
    "q_en": "Who administers oath to President?",
    "options": [
      {
        "letter": "A",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "B",
        "hi": "मुख्य न्यायाधीश",
        "en": "Chief Justice"
      },
      {
        "letter": "C",
        "hi": "उपराष्ट्रपति",
        "en": "Vice President"
      },
      {
        "letter": "D",
        "hi": "लोकसभा अध्यक्ष",
        "en": "Lok Sabha Speaker"
      }
    ],
    "correct": "B",
    "exp_hi": "सर्वोच्च न्यायालय के मुख्य न्यायाधीश राष्ट्रपति को शपथ दिलाते हैं।",
    "exp_en": "Chief Justice of Supreme Court administers oath to President.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत का संविधान किसने हाथ से लिखा?",
    "q_en": "Who handwrote the Indian Constitution?",
    "options": [
      {
        "letter": "A",
        "hi": "डॉ. राजेंद्र प्रसाद",
        "en": "Dr. Rajendra Prasad"
      },
      {
        "letter": "B",
        "hi": "प्रेम बिहारी नारायण रायजादा",
        "en": "Prem Bihari Narayan Raizada"
      },
      {
        "letter": "C",
        "hi": "डॉ. अंबेडकर",
        "en": "Dr. Ambedkar"
      },
      {
        "letter": "D",
        "hi": "जवाहरलाल नेहरू",
        "en": "Jawaharlal Nehru"
      }
    ],
    "correct": "B",
    "exp_hi": "संविधान की मूल प्रति प्रेम बिहारी नारायण रायजादा ने हाथ से लिखी।",
    "exp_en": "Original Constitution was handwritten by Prem Bihari Narayan Raizada.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में राज्यसभा के सदस्यों का कार्यकाल कितना होता है?",
    "q_en": "Term of Rajya Sabha members?",
    "options": [
      {
        "letter": "A",
        "hi": "4 साल",
        "en": "4 years"
      },
      {
        "letter": "B",
        "hi": "5 साल",
        "en": "5 years"
      },
      {
        "letter": "C",
        "hi": "6 साल",
        "en": "6 years"
      },
      {
        "letter": "D",
        "hi": "3 साल",
        "en": "3 years"
      }
    ],
    "correct": "C",
    "exp_hi": "राज्यसभा सदस्यों का कार्यकाल 6 साल होता है।",
    "exp_en": "Rajya Sabha members serve for 6 years.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "नियंत्रक एवं महालेखा परीक्षक (CAG) की नियुक्ति कौन करता है?",
    "q_en": "Who appoints CAG of India?",
    "options": [
      {
        "letter": "A",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "B",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "C",
        "hi": "वित्त मंत्री",
        "en": "Finance Minister"
      },
      {
        "letter": "D",
        "hi": "संसद",
        "en": "Parliament"
      }
    ],
    "correct": "B",
    "exp_hi": "CAG की नियुक्ति राष्ट्रपति करते हैं।",
    "exp_en": "CAG is appointed by President.",
    "exam_tag": "UPSC 2016",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "राष्ट्रपति शासन किस अनुच्छेद के तहत लागू होता है?",
    "q_en": "President's Rule is imposed under which article?",
    "options": [
      {
        "letter": "A",
        "hi": "अनुच्छेद 352",
        "en": "Article 352"
      },
      {
        "letter": "B",
        "hi": "अनुच्छेद 356",
        "en": "Article 356"
      },
      {
        "letter": "C",
        "hi": "अनुच्छेद 360",
        "en": "Article 360"
      },
      {
        "letter": "D",
        "hi": "अनुच्छेद 370",
        "en": "Article 370"
      }
    ],
    "correct": "B",
    "exp_hi": "राष्ट्रपति शासन अनुच्छेद 356 के तहत लागू होता है।",
    "exp_en": "President's Rule is imposed under Article 356.",
    "exam_tag": "SSC 2017",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "वित्तीय आपातकाल किस अनुच्छेद के तहत लागू होता है?",
    "q_en": "Financial Emergency is under which article?",
    "options": [
      {
        "letter": "A",
        "hi": "अनुच्छेद 352",
        "en": "Article 352"
      },
      {
        "letter": "B",
        "hi": "अनुच्छेद 356",
        "en": "Article 356"
      },
      {
        "letter": "C",
        "hi": "अनुच्छेद 360",
        "en": "Article 360"
      },
      {
        "letter": "D",
        "hi": "अनुच्छेद 370",
        "en": "Article 370"
      }
    ],
    "correct": "C",
    "exp_hi": "वित्तीय आपातकाल अनुच्छेद 360 के तहत लागू होता है।",
    "exp_en": "Financial Emergency is under Article 360.",
    "exam_tag": "Railway 2018",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "राष्ट्रीय आपातकाल किस अनुच्छेद के तहत लागू होता है?",
    "q_en": "National Emergency is under which article?",
    "options": [
      {
        "letter": "A",
        "hi": "अनुच्छेद 352",
        "en": "Article 352"
      },
      {
        "letter": "B",
        "hi": "अनुच्छेद 356",
        "en": "Article 356"
      },
      {
        "letter": "C",
        "hi": "अनुच्छेद 360",
        "en": "Article 360"
      },
      {
        "letter": "D",
        "hi": "अनुच्छेद 370",
        "en": "Article 370"
      }
    ],
    "correct": "A",
    "exp_hi": "राष्ट्रीय आपातकाल अनुच्छेद 352 के तहत लागू होता है।",
    "exp_en": "National Emergency is under Article 352.",
    "exam_tag": "UPSC 2018",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में संघ लोक सेवा आयोग (UPSC) की स्थापना कब हुई?",
    "q_en": "When was UPSC established?",
    "options": [
      {
        "letter": "A",
        "hi": "1923",
        "en": "1923"
      },
      {
        "letter": "B",
        "hi": "1926",
        "en": "1926"
      },
      {
        "letter": "C",
        "hi": "1928",
        "en": "1928"
      },
      {
        "letter": "D",
        "hi": "1950",
        "en": "1950"
      }
    ],
    "correct": "B",
    "exp_hi": "UPSC की स्थापना 1926 में हुई थी।",
    "exp_en": "UPSC was established in 1926.",
    "exam_tag": "SSC 2018",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में पहला राज्यपाल कौन था?",
    "q_en": "Who was first Governor in India?",
    "options": [
      {
        "letter": "A",
        "hi": "लॉर्ड माउंटबेटन",
        "en": "Lord Mountbatten"
      },
      {
        "letter": "B",
        "hi": "सी. राजगोपालाचारी",
        "en": "C. Rajagopalachari"
      },
      {
        "letter": "C",
        "hi": "सरोजिनी नायडू",
        "en": "Sarojini Naidu"
      },
      {
        "letter": "D",
        "hi": "वी.पी. मेनन",
        "en": "V.P. Menon"
      }
    ],
    "correct": "B",
    "exp_hi": "सी. राजगोपालाचारी स्वतंत्र भारत के प्रथम और एकमात्र भारतीय गवर्नर जनरल थे।",
    "exp_en": "C. Rajagopalachari was the first and only Indian Governor-General.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में लोकपाल की स्थापना कब हुई?",
    "q_en": "When was Lokpal established in India?",
    "options": [
      {
        "letter": "A",
        "hi": "2013",
        "en": "2013"
      },
      {
        "letter": "B",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "C",
        "hi": "2019",
        "en": "2019"
      },
      {
        "letter": "D",
        "hi": "2020",
        "en": "2020"
      }
    ],
    "correct": "C",
    "exp_hi": "लोकपाल की स्थापना 2019 में हुई।",
    "exp_en": "Lokpal was established in 2019.",
    "exam_tag": "UPSC 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में आरटीआई (RTI) कब लागू हुआ?",
    "q_en": "When was RTI implemented in India?",
    "options": [
      {
        "letter": "A",
        "hi": "2003",
        "en": "2003"
      },
      {
        "letter": "B",
        "hi": "2005",
        "en": "2005"
      },
      {
        "letter": "C",
        "hi": "2007",
        "en": "2007"
      },
      {
        "letter": "D",
        "hi": "2009",
        "en": "2009"
      }
    ],
    "correct": "B",
    "exp_hi": "RTI (सूचना का अधिकार) अधिनियम 2005 में लागू हुआ।",
    "exp_en": "RTI (Right to Information) Act was implemented in 2005.",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में महिला को मताधिकार कब मिला?",
    "q_en": "When did women get voting rights in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1947",
        "en": "1947"
      },
      {
        "letter": "B",
        "hi": "1950",
        "en": "1950"
      },
      {
        "letter": "C",
        "hi": "1952",
        "en": "1952"
      },
      {
        "letter": "D",
        "hi": "1955",
        "en": "1955"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत में सभी नागरिकों को 1950 में मताधिकार मिला।",
    "exp_en": "All citizens including women got voting rights in 1950.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में CAG की स्थापना कब हुई?",
    "q_en": "When was CAG established in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1948",
        "en": "1948"
      },
      {
        "letter": "B",
        "hi": "1950",
        "en": "1950"
      },
      {
        "letter": "C",
        "hi": "1971",
        "en": "1971"
      },
      {
        "letter": "D",
        "hi": "1976",
        "en": "1976"
      }
    ],
    "correct": "C",
    "exp_hi": "CAG की स्थापना 1971 में हुई।",
    "exp_en": "CAG was established in 1971.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में NHRC की स्थापना कब हुई?",
    "q_en": "When was NHRC established in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1990",
        "en": "1990"
      },
      {
        "letter": "B",
        "hi": "1993",
        "en": "1993"
      },
      {
        "letter": "C",
        "hi": "1995",
        "en": "1995"
      },
      {
        "letter": "D",
        "hi": "1997",
        "en": "1997"
      }
    ],
    "correct": "B",
    "exp_hi": "राष्ट्रीय मानवाधिकार आयोग (NHRC) 1993 में स्थापित हुआ।",
    "exp_en": "NHRC was established in 1993.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत की राष्ट्रीय भाषा क्या है?",
    "q_en": "What is the national language of India?",
    "options": [
      {
        "letter": "A",
        "hi": "हिंदी",
        "en": "Hindi"
      },
      {
        "letter": "B",
        "hi": "अंग्रेजी",
        "en": "English"
      },
      {
        "letter": "C",
        "hi": "भारत की कोई राष्ट्रीय भाषा नहीं है",
        "en": "India has no national language"
      },
      {
        "letter": "D",
        "hi": "संस्कृत",
        "en": "Sanskrit"
      }
    ],
    "correct": "C",
    "exp_hi": "भारत की कोई एक राष्ट्रीय भाषा नहीं है। हिंदी और अंग्रेजी राजभाषाएं हैं।",
    "exp_en": "India has no single national language. Hindi and English are official languages.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में CBI की स्थापना कब हुई?",
    "q_en": "When was CBI established in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1941",
        "en": "1941"
      },
      {
        "letter": "B",
        "hi": "1945",
        "en": "1945"
      },
      {
        "letter": "C",
        "hi": "1963",
        "en": "1963"
      },
      {
        "letter": "D",
        "hi": "1975",
        "en": "1975"
      }
    ],
    "correct": "C",
    "exp_hi": "CBI की स्थापना 1963 में हुई।",
    "exp_en": "CBI was established in 1963.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में IB (Intelligence Bureau) की स्थापना कब हुई?",
    "q_en": "When was IB established in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1887",
        "en": "1887"
      },
      {
        "letter": "B",
        "hi": "1920",
        "en": "1920"
      },
      {
        "letter": "C",
        "hi": "1947",
        "en": "1947"
      },
      {
        "letter": "D",
        "hi": "1950",
        "en": "1950"
      }
    ],
    "correct": "A",
    "exp_hi": "IB की स्थापना 1887 में हुई।",
    "exp_en": "IB was established in 1887.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में GST परिषद का अध्यक्ष कौन होता है?",
    "q_en": "Who chairs GST Council in India?",
    "options": [
      {
        "letter": "A",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "B",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "C",
        "hi": "वित्त मंत्री",
        "en": "Finance Minister"
      },
      {
        "letter": "D",
        "hi": "RBI गवर्नर",
        "en": "RBI Governor"
      }
    ],
    "correct": "C",
    "exp_hi": "वित्त मंत्री GST परिषद के अध्यक्ष होते हैं।",
    "exp_en": "Finance Minister chairs the GST Council.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'जनहित याचिका' (PIL) की शुरुआत किसने की?",
    "q_en": "Who started Public Interest Litigation (PIL) in India?",
    "options": [
      {
        "letter": "A",
        "hi": "जस्टिस पी.एन. भगवती",
        "en": "Justice P.N. Bhagwati"
      },
      {
        "letter": "B",
        "hi": "जस्टिस वाई.वी. चंद्रचूड़",
        "en": "Justice Y.V. Chandrachud"
      },
      {
        "letter": "C",
        "hi": "जस्टिस कृष्णा अय्यर",
        "en": "Justice Krishna Iyer"
      },
      {
        "letter": "D",
        "hi": "जस्टिस हिदायतुल्ला",
        "en": "Justice Hidayatullah"
      }
    ],
    "correct": "A",
    "exp_hi": "जस्टिस पी.एन. भगवती ने भारत में PIL की शुरुआत की।",
    "exp_en": "Justice P.N. Bhagwati started PIL in India.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में वित्त आयोग की स्थापना किस अनुच्छेद के तहत होती है?",
    "q_en": "Finance Commission is established under which article?",
    "options": [
      {
        "letter": "A",
        "hi": "अनुच्छेद 280",
        "en": "Article 280"
      },
      {
        "letter": "B",
        "hi": "अनुच्छेद 356",
        "en": "Article 356"
      },
      {
        "letter": "C",
        "hi": "अनुच्छेद 312",
        "en": "Article 312"
      },
      {
        "letter": "D",
        "hi": "अनुच्छेद 324",
        "en": "Article 324"
      }
    ],
    "correct": "A",
    "exp_hi": "वित्त आयोग अनुच्छेद 280 के तहत स्थापित होता है।",
    "exp_en": "Finance Commission is established under Article 280.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'शून्यकाल' क्या है?",
    "q_en": "What is 'Zero Hour' in India?",
    "options": [
      {
        "letter": "A",
        "hi": "संसद सत्र का पहला घंटा",
        "en": "First hour of Parliament session"
      },
      {
        "letter": "B",
        "hi": "प्रश्नकाल के बाद का समय",
        "en": "Time after Question Hour"
      },
      {
        "letter": "C",
        "hi": "आधी रात का समय",
        "en": "Midnight time"
      },
      {
        "letter": "D",
        "hi": "बजट का समय",
        "en": "Budget time"
      }
    ],
    "correct": "B",
    "exp_hi": "शून्यकाल प्रश्नकाल के ठीक बाद होता है जब सदस्य बिना पूर्व सूचना के मुद्दे उठा सकते हैं।",
    "exp_en": "Zero Hour is right after Question Hour when members raise issues without prior notice.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "संसद में 'प्रश्नकाल' कितने समय का होता है?",
    "q_en": "How long is Question Hour in Parliament?",
    "options": [
      {
        "letter": "A",
        "hi": "30 मिनट",
        "en": "30 minutes"
      },
      {
        "letter": "B",
        "hi": "45 मिनट",
        "en": "45 minutes"
      },
      {
        "letter": "C",
        "hi": "1 घंटा",
        "en": "1 hour"
      },
      {
        "letter": "D",
        "hi": "2 घंटे",
        "en": "2 hours"
      }
    ],
    "correct": "C",
    "exp_hi": "संसद में प्रश्नकाल 1 घंटे का होता है।",
    "exp_en": "Question Hour in Parliament is 1 hour long.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'धन विधेयक' किस सदन में पेश होता है?",
    "q_en": "Money Bill is introduced in which house?",
    "options": [
      {
        "letter": "A",
        "hi": "राज्यसभा",
        "en": "Rajya Sabha"
      },
      {
        "letter": "B",
        "hi": "लोकसभा",
        "en": "Lok Sabha"
      },
      {
        "letter": "C",
        "hi": "दोनों में एक साथ",
        "en": "Both simultaneously"
      },
      {
        "letter": "D",
        "hi": "कोई भी",
        "en": "Either"
      }
    ],
    "correct": "B",
    "exp_hi": "धन विधेयक केवल लोकसभा में पेश होता है।",
    "exp_en": "Money Bill is introduced only in Lok Sabha.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में संविधान का संरक्षक कौन है?",
    "q_en": "Who is guardian of Indian Constitution?",
    "options": [
      {
        "letter": "A",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "B",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "C",
        "hi": "सर्वोच्च न्यायालय",
        "en": "Supreme Court"
      },
      {
        "letter": "D",
        "hi": "संसद",
        "en": "Parliament"
      }
    ],
    "correct": "C",
    "exp_hi": "सर्वोच्च न्यायालय भारतीय संविधान का संरक्षक है।",
    "exp_en": "Supreme Court is the guardian of Indian Constitution.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'मूल ढाँचा सिद्धांत' किस मामले में प्रतिपादित हुआ?",
    "q_en": "Basic Structure Doctrine was propounded in which case?",
    "options": [
      {
        "letter": "A",
        "hi": "गोलकनाथ केस",
        "en": "Golaknath case"
      },
      {
        "letter": "B",
        "hi": "केशवानंद भारती केस",
        "en": "Kesavananda Bharati case"
      },
      {
        "letter": "C",
        "hi": "मिनर्वा मिल्स केस",
        "en": "Minerva Mills case"
      },
      {
        "letter": "D",
        "hi": "मेनका गांधी केस",
        "en": "Menaka Gandhi case"
      }
    ],
    "correct": "B",
    "exp_hi": "मूल ढाँचा सिद्धांत 1973 में केशवानंद भारती केस में प्रतिपादित हुआ।",
    "exp_en": "Basic Structure Doctrine was propounded in Kesavananda Bharati case in 1973.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'समवर्ती सूची' में कितने विषय हैं?",
    "q_en": "How many subjects in Concurrent List?",
    "options": [
      {
        "letter": "A",
        "hi": "47",
        "en": "47"
      },
      {
        "letter": "B",
        "hi": "52",
        "en": "52"
      },
      {
        "letter": "C",
        "hi": "66",
        "en": "66"
      },
      {
        "letter": "D",
        "hi": "97",
        "en": "97"
      }
    ],
    "correct": "B",
    "exp_hi": "समवर्ती सूची में 52 विषय हैं।",
    "exp_en": "Concurrent List has 52 subjects.",
    "exam_tag": "Railway 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में संघ सूची में कितने विषय हैं?",
    "q_en": "How many subjects in Union List?",
    "options": [
      {
        "letter": "A",
        "hi": "66",
        "en": "66"
      },
      {
        "letter": "B",
        "hi": "97",
        "en": "97"
      },
      {
        "letter": "C",
        "hi": "52",
        "en": "52"
      },
      {
        "letter": "D",
        "hi": "61",
        "en": "61"
      }
    ],
    "correct": "B",
    "exp_hi": "संघ सूची में 97 विषय हैं।",
    "exp_en": "Union List has 97 subjects.",
    "exam_tag": "CTET 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में राज्य सूची में कितने विषय हैं?",
    "q_en": "How many subjects in State List?",
    "options": [
      {
        "letter": "A",
        "hi": "52",
        "en": "52"
      },
      {
        "letter": "B",
        "hi": "61",
        "en": "61"
      },
      {
        "letter": "C",
        "hi": "66",
        "en": "66"
      },
      {
        "letter": "D",
        "hi": "97",
        "en": "97"
      }
    ],
    "correct": "C",
    "exp_hi": "राज्य सूची में 66 विषय हैं।",
    "exp_en": "State List has 66 subjects.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में सूचना का अधिकार (RTI) कब लागू हुआ?",
    "q_en": "When was Right to Information Act enacted?",
    "options": [
      {
        "letter": "A",
        "hi": "2003",
        "en": "2003"
      },
      {
        "letter": "B",
        "hi": "2004",
        "en": "2004"
      },
      {
        "letter": "C",
        "hi": "2005",
        "en": "2005"
      },
      {
        "letter": "D",
        "hi": "2006",
        "en": "2006"
      }
    ],
    "correct": "C",
    "exp_hi": "RTI अधिनियम 12 अक्टूबर 2005 को लागू हुआ।",
    "exp_en": "RTI Act came into force on 12 October 2005.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में शिक्षा का अधिकार कब लागू हुआ?",
    "q_en": "When was Right to Education Act implemented?",
    "options": [
      {
        "letter": "A",
        "hi": "2007",
        "en": "2007"
      },
      {
        "letter": "B",
        "hi": "2008",
        "en": "2008"
      },
      {
        "letter": "C",
        "hi": "2009",
        "en": "2009"
      },
      {
        "letter": "D",
        "hi": "2010",
        "en": "2010"
      }
    ],
    "correct": "D",
    "exp_hi": "शिक्षा का अधिकार अधिनियम 1 अप्रैल 2010 को लागू हुआ।",
    "exp_en": "Right to Education Act was implemented on 1 April 2010.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में संसद के संयुक्त अधिवेशन की अध्यक्षता कौन करता है?",
    "q_en": "Who presides over joint session of Parliament?",
    "options": [
      {
        "letter": "A",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "B",
        "hi": "उपराष्ट्रपति",
        "en": "Vice President"
      },
      {
        "letter": "C",
        "hi": "लोकसभा अध्यक्ष",
        "en": "Lok Sabha Speaker"
      },
      {
        "letter": "D",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      }
    ],
    "correct": "C",
    "exp_hi": "लोकसभा अध्यक्ष संसद के संयुक्त अधिवेशन की अध्यक्षता करते हैं।",
    "exp_en": "Lok Sabha Speaker presides over joint session of Parliament.",
    "exam_tag": "Railway 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "'संसदीय विशेषाधिकार' का अर्थ क्या है?",
    "q_en": "What does Parliamentary Privilege mean?",
    "options": [
      {
        "letter": "A",
        "hi": "संसद की विशेष शक्तियाँ",
        "en": "Special powers of Parliament"
      },
      {
        "letter": "B",
        "hi": "सांसदों की विशेष छूट",
        "en": "Special immunity of MPs"
      },
      {
        "letter": "C",
        "hi": "प्रधानमंत्री की शक्तियाँ",
        "en": "PM's powers"
      },
      {
        "letter": "D",
        "hi": "न्यायपालिका की छूट",
        "en": "Judiciary's immunity"
      }
    ],
    "correct": "B",
    "exp_hi": "संसदीय विशेषाधिकार सांसदों को सदन में दी गई विशेष छूट है।",
    "exp_en": "Parliamentary Privilege is special immunity given to MPs in the House.",
    "exam_tag": "SSC 2017",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारत के किस राज्य में दो राजधानियाँ हैं?",
    "q_en": "Which Indian state has two capitals?",
    "options": [
      {
        "letter": "A",
        "hi": "उत्तर प्रदेश",
        "en": "Uttar Pradesh"
      },
      {
        "letter": "B",
        "hi": "हिमाचल प्रदेश",
        "en": "Himachal Pradesh"
      },
      {
        "letter": "C",
        "hi": "जम्मू-कश्मीर",
        "en": "Jammu-Kashmir"
      },
      {
        "letter": "D",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      }
    ],
    "correct": "B",
    "exp_hi": "हिमाचल प्रदेश की दो राजधानियाँ हैं - शिमला (ग्रीष्म) और धर्मशाला (शीत)।",
    "exp_en": "Himachal Pradesh has two capitals - Shimla (summer) and Dharamsala (winter).",
    "exam_tag": "Railway 2018",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'पंचायती राज' संस्था में कितने स्तर हैं?",
    "q_en": "How many tiers in Panchayati Raj in India?",
    "options": [
      {
        "letter": "A",
        "hi": "2",
        "en": "2"
      },
      {
        "letter": "B",
        "hi": "3",
        "en": "3"
      },
      {
        "letter": "C",
        "hi": "4",
        "en": "4"
      },
      {
        "letter": "D",
        "hi": "5",
        "en": "5"
      }
    ],
    "correct": "B",
    "exp_hi": "पंचायती राज की 3 स्तर की संरचना है - ग्राम पंचायत, पंचायत समिति, जिला परिषद।",
    "exp_en": "Panchayati Raj has 3 tier structure - Gram Panchayat, Panchayat Samiti, Zila Parishad.",
    "exam_tag": "SSC 2018",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "नागरिकता संशोधन अधिनियम (CAA) कब पारित हुआ?",
    "q_en": "When was Citizenship Amendment Act (CAA) passed?",
    "options": [
      {
        "letter": "A",
        "hi": "2017",
        "en": "2017"
      },
      {
        "letter": "B",
        "hi": "2018",
        "en": "2018"
      },
      {
        "letter": "C",
        "hi": "2019",
        "en": "2019"
      },
      {
        "letter": "D",
        "hi": "2020",
        "en": "2020"
      }
    ],
    "correct": "C",
    "exp_hi": "CAA दिसंबर 2019 में पारित हुआ।",
    "exp_en": "CAA was passed in December 2019.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में सर्वोच्च न्यायालय की स्थापना कब हुई?",
    "q_en": "When was Supreme Court of India established?",
    "options": [
      {
        "letter": "A",
        "hi": "1947",
        "en": "1947"
      },
      {
        "letter": "B",
        "hi": "1950",
        "en": "1950"
      },
      {
        "letter": "C",
        "hi": "1952",
        "en": "1952"
      },
      {
        "letter": "D",
        "hi": "1955",
        "en": "1955"
      }
    ],
    "correct": "B",
    "exp_hi": "सर्वोच्च न्यायालय की स्थापना 28 जनवरी 1950 को हुई।",
    "exp_en": "Supreme Court was established on 28 January 1950.",
    "exam_tag": "UPSC 2016",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'महाभियोग' प्रक्रिया किसके लिए है?",
    "q_en": "Impeachment process in India is for?",
    "options": [
      {
        "letter": "A",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "B",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "C",
        "hi": "लोकसभा अध्यक्ष",
        "en": "Lok Sabha Speaker"
      },
      {
        "letter": "D",
        "hi": "मुख्यमंत्री",
        "en": "Chief Minister"
      }
    ],
    "correct": "B",
    "exp_hi": "महाभियोग प्रक्रिया राष्ट्रपति को हटाने के लिए है।",
    "exp_en": "Impeachment process is for removing the President.",
    "exam_tag": "SSC 2016",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारतीय संसद की संयुक्त बैठक किस अनुच्छेद के तहत होती है?",
    "q_en": "Joint sitting of Parliament under which article?",
    "options": [
      {
        "letter": "A",
        "hi": "अनुच्छेद 100",
        "en": "Article 100"
      },
      {
        "letter": "B",
        "hi": "अनुच्छेद 108",
        "en": "Article 108"
      },
      {
        "letter": "C",
        "hi": "अनुच्छेद 110",
        "en": "Article 110"
      },
      {
        "letter": "D",
        "hi": "अनुच्छेद 120",
        "en": "Article 120"
      }
    ],
    "correct": "B",
    "exp_hi": "संसद की संयुक्त बैठक अनुच्छेद 108 के तहत होती है।",
    "exp_en": "Joint sitting of Parliament is under Article 108.",
    "exam_tag": "Railway 2017",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत के प्रथम उपराष्ट्रपति कौन थे?",
    "q_en": "First Vice President of India?",
    "options": [
      {
        "letter": "A",
        "hi": "डॉ. राधाकृष्णन",
        "en": "Dr. Radhakrishnan"
      },
      {
        "letter": "B",
        "hi": "डॉ. जाकिर हुसैन",
        "en": "Dr. Zakir Husain"
      },
      {
        "letter": "C",
        "hi": "वी.वी. गिरि",
        "en": "V.V. Giri"
      },
      {
        "letter": "D",
        "hi": "गोपाल स्वरूप पाठक",
        "en": "Gopal Swaroop Pathak"
      }
    ],
    "correct": "A",
    "exp_hi": "डॉ. सर्वपल्ली राधाकृष्णन भारत के प्रथम उपराष्ट्रपति थे।",
    "exp_en": "Dr. S. Radhakrishnan was India's first Vice President.",
    "exam_tag": "UPSC 2015",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "लोकसभा में अविश्वास प्रस्ताव लाने के लिए कितने सदस्यों का समर्थन चाहिए?",
    "q_en": "Members needed to move No-Confidence Motion?",
    "options": [
      {
        "letter": "A",
        "hi": "25",
        "en": "25"
      },
      {
        "letter": "B",
        "hi": "40",
        "en": "40"
      },
      {
        "letter": "C",
        "hi": "50",
        "en": "50"
      },
      {
        "letter": "D",
        "hi": "100",
        "en": "100"
      }
    ],
    "correct": "C",
    "exp_hi": "अविश्वास प्रस्ताव के लिए 50 सदस्यों का समर्थन चाहिए।",
    "exp_en": "No-Confidence Motion needs support of 50 members.",
    "exam_tag": "SSC 2015",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'कोलेजियम प्रणाली' किससे संबंधित है?",
    "q_en": "Collegium system in India is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "संसद",
        "en": "Parliament"
      },
      {
        "letter": "B",
        "hi": "न्यायाधीशों की नियुक्ति",
        "en": "Appointment of judges"
      },
      {
        "letter": "C",
        "hi": "IAS नियुक्ति",
        "en": "IAS appointment"
      },
      {
        "letter": "D",
        "hi": "मंत्रिमंडल",
        "en": "Cabinet"
      }
    ],
    "correct": "B",
    "exp_hi": "कोलेजियम प्रणाली सर्वोच्च न्यायालय के न्यायाधीशों की नियुक्ति से संबंधित है।",
    "exp_en": "Collegium system is related to appointment of Supreme Court judges.",
    "exam_tag": "CTET 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'आदर्श आचार संहिता' कौन लागू करता है?",
    "q_en": "Who enforces Model Code of Conduct in India?",
    "options": [
      {
        "letter": "A",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "B",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "C",
        "hi": "चुनाव आयोग",
        "en": "Election Commission"
      },
      {
        "letter": "D",
        "hi": "सर्वोच्च न्यायालय",
        "en": "Supreme Court"
      }
    ],
    "correct": "C",
    "exp_hi": "आदर्श आचार संहिता चुनाव आयोग द्वारा लागू की जाती है।",
    "exp_en": "Model Code of Conduct is enforced by Election Commission.",
    "exam_tag": "SSC 2016",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'राष्ट्रपति के अध्यादेश' की शक्ति किस अनुच्छेद में है?",
    "q_en": "President's Ordinance power is in which article?",
    "options": [
      {
        "letter": "A",
        "hi": "अनुच्छेद 123",
        "en": "Article 123"
      },
      {
        "letter": "B",
        "hi": "अनुच्छेद 213",
        "en": "Article 213"
      },
      {
        "letter": "C",
        "hi": "अनुच्छेद 352",
        "en": "Article 352"
      },
      {
        "letter": "D",
        "hi": "अनुच्छेद 356",
        "en": "Article 356"
      }
    ],
    "correct": "A",
    "exp_hi": "राष्ट्रपति की अध्यादेश शक्ति अनुच्छेद 123 में है।",
    "exp_en": "President's Ordinance power is in Article 123.",
    "exam_tag": "Railway 2016",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "'संविधान का 86वाँ संशोधन' किससे संबंधित है?",
    "q_en": "86th Constitutional Amendment is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "पंचायती राज",
        "en": "Panchayati Raj"
      },
      {
        "letter": "B",
        "hi": "शिक्षा का अधिकार",
        "en": "Right to Education"
      },
      {
        "letter": "C",
        "hi": "GST",
        "en": "GST"
      },
      {
        "letter": "D",
        "hi": "मतदान आयु",
        "en": "Voting age"
      }
    ],
    "correct": "B",
    "exp_hi": "86वाँ संशोधन शिक्षा के अधिकार से संबंधित है।",
    "exp_en": "86th Amendment is related to Right to Education.",
    "exam_tag": "UPSC 2016",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'राज्य मानवाधिकार आयोग' का गठन किस अधिनियम के तहत होता है?",
    "q_en": "State Human Rights Commission is formed under which act?",
    "options": [
      {
        "letter": "A",
        "hi": "मानवाधिकार अधिनियम 1993",
        "en": "Human Rights Act 1993"
      },
      {
        "letter": "B",
        "hi": "मानवाधिकार अधिनियम 1995",
        "en": "Human Rights Act 1995"
      },
      {
        "letter": "C",
        "hi": "संविधान",
        "en": "Constitution"
      },
      {
        "letter": "D",
        "hi": "संसद अधिनियम",
        "en": "Parliament Act"
      }
    ],
    "correct": "A",
    "exp_hi": "मानवाधिकार संरक्षण अधिनियम 1993 के तहत SHRC का गठन होता है।",
    "exp_en": "State Human Rights Commission is formed under Human Rights Act 1993.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'केंद्र-राज्य संबंध' का आधार क्या है?",
    "q_en": "Basis of Centre-State relations in India?",
    "options": [
      {
        "letter": "A",
        "hi": "एकात्मक व्यवस्था",
        "en": "Unitary system"
      },
      {
        "letter": "B",
        "hi": "संघीय व्यवस्था",
        "en": "Federal system"
      },
      {
        "letter": "C",
        "hi": "लोकतांत्रिक व्यवस्था",
        "en": "Democratic system"
      },
      {
        "letter": "D",
        "hi": "राजतंत्र",
        "en": "Monarchy"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत में केंद्र-राज्य संबंध संघीय व्यवस्था पर आधारित है।",
    "exp_en": "Centre-State relations in India are based on federal system.",
    "exam_tag": "UPSC 2015",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "राज्यपाल की नियुक्ति कौन करता है?",
    "q_en": "Who appoints Governor of a state?",
    "options": [
      {
        "letter": "A",
        "hi": "राज्य विधानसभा",
        "en": "State Legislature"
      },
      {
        "letter": "B",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "C",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "D",
        "hi": "उपराष्ट्रपति",
        "en": "Vice President"
      }
    ],
    "correct": "B",
    "exp_hi": "राज्यपाल की नियुक्ति राष्ट्रपति करते हैं।",
    "exp_en": "Governor is appointed by President.",
    "exam_tag": "Railway 2015",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में मुख्यमंत्री की नियुक्ति कौन करता है?",
    "q_en": "Who appoints Chief Minister in India?",
    "options": [
      {
        "letter": "A",
        "hi": "राष्ट्रपति",
        "en": "President"
      },
      {
        "letter": "B",
        "hi": "राज्यपाल",
        "en": "Governor"
      },
      {
        "letter": "C",
        "hi": "प्रधानमंत्री",
        "en": "Prime Minister"
      },
      {
        "letter": "D",
        "hi": "विधानसभा",
        "en": "State Legislature"
      }
    ],
    "correct": "B",
    "exp_hi": "राज्यपाल मुख्यमंत्री की नियुक्ति करते हैं।",
    "exp_en": "Governor appoints the Chief Minister.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'डाकघर अधिनियम' कब बना?",
    "q_en": "When was Post Office Act in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1896",
        "en": "1896"
      },
      {
        "letter": "B",
        "hi": "1898",
        "en": "1898"
      },
      {
        "letter": "C",
        "hi": "1900",
        "en": "1900"
      },
      {
        "letter": "D",
        "hi": "1910",
        "en": "1910"
      }
    ],
    "correct": "B",
    "exp_hi": "डाकघर अधिनियम 1898 में बना।",
    "exp_en": "Post Office Act was enacted in 1898.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत के संविधान में कुल कितने अनुच्छेद हैं?",
    "q_en": "How many articles in Indian Constitution?",
    "options": [
      {
        "letter": "A",
        "hi": "395",
        "en": "395"
      },
      {
        "letter": "B",
        "hi": "448",
        "en": "448"
      },
      {
        "letter": "C",
        "hi": "470",
        "en": "470"
      },
      {
        "letter": "D",
        "hi": "500",
        "en": "500"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत के संविधान में वर्तमान में 448 अनुच्छेद हैं।",
    "exp_en": "Indian Constitution currently has 448 articles.",
    "exam_tag": "CTET 2024",
    "class": "कक्षा 9"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में पहली महिला राष्ट्रपति कौन थीं?",
    "q_en": "First woman President of India?",
    "options": [
      {
        "letter": "A",
        "hi": "सरोजिनी नायडू",
        "en": "Sarojini Naidu"
      },
      {
        "letter": "B",
        "hi": "इंदिरा गांधी",
        "en": "Indira Gandhi"
      },
      {
        "letter": "C",
        "hi": "प्रतिभा पाटिल",
        "en": "Pratibha Patil"
      },
      {
        "letter": "D",
        "hi": "सुषमा स्वराज",
        "en": "Sushma Swaraj"
      }
    ],
    "correct": "C",
    "exp_hi": "प्रतिभा पाटिल भारत की पहली महिला राष्ट्रपति थीं (2007-2012)।",
    "exp_en": "Pratibha Patil was India's first woman President (2007-2012).",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 10"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'सूचना आयोग' (CIC) की स्थापना कब हुई?",
    "q_en": "When was CIC established in India?",
    "options": [
      {
        "letter": "A",
        "hi": "2003",
        "en": "2003"
      },
      {
        "letter": "B",
        "hi": "2005",
        "en": "2005"
      },
      {
        "letter": "C",
        "hi": "2007",
        "en": "2007"
      },
      {
        "letter": "D",
        "hi": "2009",
        "en": "2009"
      }
    ],
    "correct": "B",
    "exp_hi": "CIC (Central Information Commission) 2005 में RTI Act के तहत स्थापित हुआ।",
    "exp_en": "CIC was established in 2005 under RTI Act.",
    "exam_tag": "Railway 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'केंद्रीय सतर्कता आयोग' (CVC) कब स्थापित हुआ?",
    "q_en": "When was CVC established in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1960",
        "en": "1960"
      },
      {
        "letter": "B",
        "hi": "1964",
        "en": "1964"
      },
      {
        "letter": "C",
        "hi": "1970",
        "en": "1970"
      },
      {
        "letter": "D",
        "hi": "1975",
        "en": "1975"
      }
    ],
    "correct": "B",
    "exp_hi": "CVC की स्थापना 1964 में हुई।",
    "exp_en": "CVC was established in 1964.",
    "exam_tag": "CTET 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "polity",
    "q_hi": "भारत में 'लोकायुक्त' का गठन किस राज्य में पहले हुआ?",
    "q_en": "In which state was Lokayukta first established?",
    "options": [
      {
        "letter": "A",
        "hi": "महाराष्ट्र",
        "en": "Maharashtra"
      },
      {
        "letter": "B",
        "hi": "राजस्थान",
        "en": "Rajasthan"
      },
      {
        "letter": "C",
        "hi": "महाराष्ट्र (1971)",
        "en": "Maharashtra (1971)"
      },
      {
        "letter": "D",
        "hi": "ओडिशा",
        "en": "Odisha"
      }
    ],
    "correct": "C",
    "exp_hi": "महाराष्ट्र में 1971 में पहली बार लोकायुक्त का गठन हुआ।",
    "exp_en": "Maharashtra established Lokayukta first in 1971.",
    "exam_tag": "Railway 2024",
    "class": "कक्षा 9"
  },
  {
    "subject": "economics",
    "q_hi": "MUDRA योजना किसके लिए है?",
    "q_en": "MUDRA scheme is for?",
    "options": [
      {
        "letter": "A",
        "hi": "बड़े उद्योग",
        "en": "Large industries"
      },
      {
        "letter": "B",
        "hi": "सूक्ष्म एवं लघु उद्यम",
        "en": "Micro and small enterprises"
      },
      {
        "letter": "C",
        "hi": "कृषि",
        "en": "Agriculture"
      },
      {
        "letter": "D",
        "hi": "निर्यात",
        "en": "Exports"
      }
    ],
    "correct": "B",
    "exp_hi": "MUDRA सूक्ष्म उद्यमों के लिए ऋण देती है।",
    "exp_en": "MUDRA provides loans to micro and small enterprises.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में आयकर कब शुरू हुआ?",
    "q_en": "When did Income Tax start in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1860",
        "en": "1860"
      },
      {
        "letter": "B",
        "hi": "1880",
        "en": "1880"
      },
      {
        "letter": "C",
        "hi": "1900",
        "en": "1900"
      },
      {
        "letter": "D",
        "hi": "1922",
        "en": "1922"
      }
    ],
    "correct": "A",
    "exp_hi": "भारत में आयकर 1860 में लागू हुआ।",
    "exp_en": "Income Tax was introduced in India in 1860.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में खाद्य सुरक्षा अधिनियम कब लागू हुआ?",
    "q_en": "When was Food Security Act implemented?",
    "options": [
      {
        "letter": "A",
        "hi": "2011",
        "en": "2011"
      },
      {
        "letter": "B",
        "hi": "2013",
        "en": "2013"
      },
      {
        "letter": "C",
        "hi": "2015",
        "en": "2015"
      },
      {
        "letter": "D",
        "hi": "2017",
        "en": "2017"
      }
    ],
    "correct": "B",
    "exp_hi": "राष्ट्रीय खाद्य सुरक्षा अधिनियम 2013 में लागू हुआ।",
    "exp_en": "National Food Security Act was implemented in 2013.",
    "exam_tag": "CTET 2022",
    "class": "कक्षา 10"
  },
  {
    "subject": "economics",
    "q_hi": "भारत का विदेश व्यापार सबसे ज्यादा किस देश से?",
    "q_en": "India's largest trading partner?",
    "options": [
      {
        "letter": "A",
        "hi": "अमेरिका",
        "en": "USA"
      },
      {
        "letter": "B",
        "hi": "चीन",
        "en": "China"
      },
      {
        "letter": "C",
        "hi": "UAE",
        "en": "UAE"
      },
      {
        "letter": "D",
        "hi": "रूस",
        "en": "Russia"
      }
    ],
    "correct": "B",
    "exp_hi": "चीन भारत का सबसे बड़ा व्यापारिक साझेदार है।",
    "exp_en": "China is India's largest trading partner.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "जन धन योजना कब शुरू हुई?",
    "q_en": "When did Jan Dhan Yojana start?",
    "options": [
      {
        "letter": "A",
        "hi": "2013",
        "en": "2013"
      },
      {
        "letter": "B",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "C",
        "hi": "2015",
        "en": "2015"
      },
      {
        "letter": "D",
        "hi": "2016",
        "en": "2016"
      }
    ],
    "correct": "B",
    "exp_hi": "जन धन योजना 28 अगस्त 2014 को शुरू हुई।",
    "exp_en": "Jan Dhan Yojana started on 28 August 2014.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "SEBI की स्थापना कब हुई?",
    "q_en": "When was SEBI established?",
    "options": [
      {
        "letter": "A",
        "hi": "1988",
        "en": "1988"
      },
      {
        "letter": "B",
        "hi": "1990",
        "en": "1990"
      },
      {
        "letter": "C",
        "hi": "1992",
        "en": "1992"
      },
      {
        "letter": "D",
        "hi": "1994",
        "en": "1994"
      }
    ],
    "correct": "C",
    "exp_hi": "SEBI की स्थापना 1992 में हुई।",
    "exp_en": "SEBI was established in 1992.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "नोटबंदी कब हुई?",
    "q_en": "When was demonetization?",
    "options": [
      {
        "letter": "A",
        "hi": "8 नवंबर 2015",
        "en": "8 November 2015"
      },
      {
        "letter": "B",
        "hi": "8 नवंबर 2016",
        "en": "8 November 2016"
      },
      {
        "letter": "C",
        "hi": "8 दिसंबर 2016",
        "en": "8 December 2016"
      },
      {
        "letter": "D",
        "hi": "8 नवंबर 2017",
        "en": "8 November 2017"
      }
    ],
    "correct": "B",
    "exp_hi": "नोटबंदी 8 नवंबर 2016 को हुई।",
    "exp_en": "Demonetization happened on 8 November 2016.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में आर्थिक उदारीकरण कब हुआ?",
    "q_en": "When did economic liberalization happen?",
    "options": [
      {
        "letter": "A",
        "hi": "1989",
        "en": "1989"
      },
      {
        "letter": "B",
        "hi": "1991",
        "en": "1991"
      },
      {
        "letter": "C",
        "hi": "1993",
        "en": "1993"
      },
      {
        "letter": "D",
        "hi": "1995",
        "en": "1995"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत में आर्थिक उदारीकरण 1991 में हुआ।",
    "exp_en": "Economic liberalization happened in 1991.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "GNP का पूरा नाम?",
    "q_en": "Full form of GNP?",
    "options": [
      {
        "letter": "A",
        "hi": "Gross National Product",
        "en": "Gross National Product"
      },
      {
        "letter": "B",
        "hi": "General National Product",
        "en": "General National Product"
      },
      {
        "letter": "C",
        "hi": "Global National Product",
        "en": "Global National Product"
      },
      {
        "letter": "D",
        "hi": "Gross Net Product",
        "en": "Gross Net Product"
      }
    ],
    "correct": "A",
    "exp_hi": "GNP यानी सकल राष्ट्रीय उत्पाद।",
    "exp_en": "GNP stands for Gross National Product.",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में बजट कब पेश होता है?",
    "q_en": "When is Union Budget presented?",
    "options": [
      {
        "letter": "A",
        "hi": "1 जनवरी",
        "en": "1 January"
      },
      {
        "letter": "B",
        "hi": "1 फरवरी",
        "en": "1 February"
      },
      {
        "letter": "C",
        "hi": "1 मार्च",
        "en": "1 March"
      },
      {
        "letter": "D",
        "hi": "1 अप्रैल",
        "en": "1 April"
      }
    ],
    "correct": "B",
    "exp_hi": "2017 से बजट 1 फरवरी को पेश होता है।",
    "exp_en": "Since 2017, Budget is presented on 1 February.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में मुद्रास्फीति मापने का आधार?",
    "q_en": "Basis of measuring inflation in India?",
    "options": [
      {
        "letter": "A",
        "hi": "WPI",
        "en": "WPI"
      },
      {
        "letter": "B",
        "hi": "CPI",
        "en": "CPI"
      },
      {
        "letter": "C",
        "hi": "GDP deflator",
        "en": "GDP deflator"
      },
      {
        "letter": "D",
        "hi": "सभी",
        "en": "All"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत में CPI मुद्रास्फीति मापने का मुख्य आधार है।",
    "exp_en": "CPI is the main basis for measuring inflation in India.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "PLI स्कीम किससे संबंधित है?",
    "q_en": "PLI scheme is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "कृषि",
        "en": "Agriculture"
      },
      {
        "letter": "B",
        "hi": "उत्पादन को बढ़ावा",
        "en": "Boost manufacturing"
      },
      {
        "letter": "C",
        "hi": "बैंकिंग",
        "en": "Banking"
      },
      {
        "letter": "D",
        "hi": "शिक्षा",
        "en": "Education"
      }
    ],
    "correct": "B",
    "exp_hi": "PLI (Production Linked Incentive) उत्पादन को बढ़ावा देने के लिए है।",
    "exp_en": "PLI is to boost manufacturing.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में बैंकों का राष्ट्रीयकरण कब हुआ?",
    "q_en": "When were banks nationalised in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1965",
        "en": "1965"
      },
      {
        "letter": "B",
        "hi": "1969",
        "en": "1969"
      },
      {
        "letter": "C",
        "hi": "1975",
        "en": "1975"
      },
      {
        "letter": "D",
        "hi": "1980",
        "en": "1980"
      }
    ],
    "correct": "B",
    "exp_hi": "पहली बार 14 बैंकों का राष्ट्रीयकरण 1969 में इंदिरा गांधी ने किया।",
    "exp_en": "First nationalisation of 14 banks was done by Indira Gandhi in 1969.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में IT उद्योग का केंद्र?",
    "q_en": "IT hub of India?",
    "options": [
      {
        "letter": "A",
        "hi": "मुंबई",
        "en": "Mumbai"
      },
      {
        "letter": "B",
        "hi": "दिल्ली",
        "en": "Delhi"
      },
      {
        "letter": "C",
        "hi": "बेंगलुरु",
        "en": "Bengaluru"
      },
      {
        "letter": "D",
        "hi": "हैदराबाद",
        "en": "Hyderabad"
      }
    ],
    "correct": "C",
    "exp_hi": "बेंगलुरु को भारत की सिलिकॉन वैली कहते हैं।",
    "exp_en": "Bengaluru is called Silicon Valley of India.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "NSE का पूरा नाम?",
    "q_en": "Full form of NSE?",
    "options": [
      {
        "letter": "A",
        "hi": "National Stock Exchange",
        "en": "National Stock Exchange"
      },
      {
        "letter": "B",
        "hi": "New Stock Exchange",
        "en": "New Stock Exchange"
      },
      {
        "letter": "C",
        "hi": "North Stock Exchange",
        "en": "North Stock Exchange"
      },
      {
        "letter": "D",
        "hi": "Normal Stock Exchange",
        "en": "Normal Stock Exchange"
      }
    ],
    "correct": "A",
    "exp_hi": "NSE यानी National Stock Exchange।",
    "exp_en": "NSE stands for National Stock Exchange.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में पंचवर्षीय योजनाएं कब बंद हुईं?",
    "q_en": "When were Five Year Plans discontinued in India?",
    "options": [
      {
        "letter": "A",
        "hi": "2012",
        "en": "2012"
      },
      {
        "letter": "B",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "C",
        "hi": "2017",
        "en": "2017"
      },
      {
        "letter": "D",
        "hi": "2019",
        "en": "2019"
      }
    ],
    "correct": "C",
    "exp_hi": "12वीं पंचवर्षीय योजना (2012-17) के बाद पंचवर्षीय योजनाएं बंद हो गईं।",
    "exp_en": "Five Year Plans ended after 12th Plan (2012-17).",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत की मुद्रा का नाम?",
    "q_en": "Name of India's currency?",
    "options": [
      {
        "letter": "A",
        "hi": "टका",
        "en": "Taka"
      },
      {
        "letter": "B",
        "hi": "रुपया",
        "en": "Rupee"
      },
      {
        "letter": "C",
        "hi": "दीनार",
        "en": "Dinar"
      },
      {
        "letter": "D",
        "hi": "रियाल",
        "en": "Riyal"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत की मुद्रा रुपया है।",
    "exp_en": "India's currency is Rupee.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में डिजिटल रुपया कब शुरू हुआ?",
    "q_en": "When did Digital Rupee start in India?",
    "options": [
      {
        "letter": "A",
        "hi": "2021",
        "en": "2021"
      },
      {
        "letter": "B",
        "hi": "2022",
        "en": "2022"
      },
      {
        "letter": "C",
        "hi": "2023",
        "en": "2023"
      },
      {
        "letter": "D",
        "hi": "2024",
        "en": "2024"
      }
    ],
    "correct": "B",
    "exp_hi": "RBI ने 2022 में डिजिटल रुपया (e-Rupee) लॉन्च किया।",
    "exp_en": "RBI launched Digital Rupee (e-Rupee) in 2022.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में GST के कितने स्लैब हैं?",
    "q_en": "How many GST slabs in India?",
    "options": [
      {
        "letter": "A",
        "hi": "3",
        "en": "3"
      },
      {
        "letter": "B",
        "hi": "4",
        "en": "4"
      },
      {
        "letter": "C",
        "hi": "5",
        "en": "5"
      },
      {
        "letter": "D",
        "hi": "6",
        "en": "6"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत में GST के 4 मुख्य स्लैब हैं - 5%, 12%, 18%, 28%।",
    "exp_en": "India has 4 main GST slabs - 5%, 12%, 18%, 28%.",
    "exam_tag": "Railway 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "IMF का मुख्यालय कहाँ है?",
    "q_en": "HQ of IMF?",
    "options": [
      {
        "letter": "A",
        "hi": "न्यूयॉर्क",
        "en": "New York"
      },
      {
        "letter": "B",
        "hi": "वाशिंगटन D.C.",
        "en": "Washington D.C."
      },
      {
        "letter": "C",
        "hi": "लंदन",
        "en": "London"
      },
      {
        "letter": "D",
        "hi": "जिनेवा",
        "en": "Geneva"
      }
    ],
    "correct": "B",
    "exp_hi": "IMF का मुख्यालय वाशिंगटन D.C. में है।",
    "exp_en": "IMF headquarters is in Washington D.C.",
    "exam_tag": "SSC 2018",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "विश्व बैंक का मुख्यालय?",
    "q_en": "HQ of World Bank?",
    "options": [
      {
        "letter": "A",
        "hi": "न्यूयॉर्क",
        "en": "New York"
      },
      {
        "letter": "B",
        "hi": "वाशिंगटन D.C.",
        "en": "Washington D.C."
      },
      {
        "letter": "C",
        "hi": "लंदन",
        "en": "London"
      },
      {
        "letter": "D",
        "hi": "जिनेवा",
        "en": "Geneva"
      }
    ],
    "correct": "B",
    "exp_hi": "विश्व बैंक का मुख्यालय वाशिंगटन D.C. में है।",
    "exp_en": "World Bank headquarters is in Washington D.C.",
    "exam_tag": "Railway 2018",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "WTO का मुख्यालय कहाँ है?",
    "q_en": "HQ of WTO?",
    "options": [
      {
        "letter": "A",
        "hi": "न्यूयॉर्क",
        "en": "New York"
      },
      {
        "letter": "B",
        "hi": "वाशिंगटन D.C.",
        "en": "Washington D.C."
      },
      {
        "letter": "C",
        "hi": "जिनेवा",
        "en": "Geneva"
      },
      {
        "letter": "D",
        "hi": "पेरिस",
        "en": "Paris"
      }
    ],
    "correct": "C",
    "exp_hi": "WTO का मुख्यालय जिनेवा में है।",
    "exp_en": "WTO headquarters is in Geneva.",
    "exam_tag": "UPSC 2017",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत का वित्त वर्ष कब से कब तक?",
    "q_en": "India's financial year?",
    "options": [
      {
        "letter": "A",
        "hi": "जनवरी-दिसंबर",
        "en": "January-December"
      },
      {
        "letter": "B",
        "hi": "अप्रैल-मार्च",
        "en": "April-March"
      },
      {
        "letter": "C",
        "hi": "अक्टूबर-सितंबर",
        "en": "October-September"
      },
      {
        "letter": "D",
        "hi": "जुलाई-जून",
        "en": "July-June"
      }
    ],
    "correct": "B",
    "exp_hi": "भारत का वित्त वर्ष 1 अप्रैल से 31 मार्च तक होता है।",
    "exp_en": "India's financial year is from 1 April to 31 March.",
    "exam_tag": "SSC 2017",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "BSE का पूरा नाम?",
    "q_en": "Full form of BSE?",
    "options": [
      {
        "letter": "A",
        "hi": "Bombay Stock Exchange",
        "en": "Bombay Stock Exchange"
      },
      {
        "letter": "B",
        "hi": "Bengal Stock Exchange",
        "en": "Bengal Stock Exchange"
      },
      {
        "letter": "C",
        "hi": "Basic Stock Exchange",
        "en": "Basic Stock Exchange"
      },
      {
        "letter": "D",
        "hi": "Bharat Stock Exchange",
        "en": "Bharat Stock Exchange"
      }
    ],
    "correct": "A",
    "exp_hi": "BSE यानी Bombay Stock Exchange।",
    "exp_en": "BSE stands for Bombay Stock Exchange.",
    "exam_tag": "Railway 2017",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "FDI का पूरा नाम?",
    "q_en": "Full form of FDI?",
    "options": [
      {
        "letter": "A",
        "hi": "Foreign Direct Investment",
        "en": "Foreign Direct Investment"
      },
      {
        "letter": "B",
        "hi": "Federal Direct Income",
        "en": "Federal Direct Income"
      },
      {
        "letter": "C",
        "hi": "Foreign Domestic Income",
        "en": "Foreign Domestic Income"
      },
      {
        "letter": "D",
        "hi": "Finance Development Index",
        "en": "Finance Development Index"
      }
    ],
    "correct": "A",
    "exp_hi": "FDI यानी प्रत्यक्ष विदेशी निवेश।",
    "exp_en": "FDI stands for Foreign Direct Investment.",
    "exam_tag": "UPSC 2018",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में पहला बैंक कौन सा था?",
    "q_en": "First bank established in India?",
    "options": [
      {
        "letter": "A",
        "hi": "Bank of Bengal",
        "en": "Bank of Bengal"
      },
      {
        "letter": "B",
        "hi": "Bank of Bombay",
        "en": "Bank of Bombay"
      },
      {
        "letter": "C",
        "hi": "Bank of Hindustan",
        "en": "Bank of Hindustan"
      },
      {
        "letter": "D",
        "hi": "SBI",
        "en": "SBI"
      }
    ],
    "correct": "C",
    "exp_hi": "Bank of Hindustan भारत का पहला बैंक था (1770)।",
    "exp_en": "Bank of Hindustan was India's first bank (1770).",
    "exam_tag": "SSC 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में LPG नीति कब शुरू हुई?",
    "q_en": "When did LPG policy start in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1989",
        "en": "1989"
      },
      {
        "letter": "B",
        "hi": "1991",
        "en": "1991"
      },
      {
        "letter": "C",
        "hi": "1993",
        "en": "1993"
      },
      {
        "letter": "D",
        "hi": "1995",
        "en": "1995"
      }
    ],
    "correct": "B",
    "exp_hi": "LPG (Liberalization, Privatization, Globalization) नीति 1991 में शुरू हुई।",
    "exp_en": "LPG (Liberalization, Privatization, Globalization) policy started in 1991.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में मनरेगा कब शुरू हुआ?",
    "q_en": "When did MGNREGA start in India?",
    "options": [
      {
        "letter": "A",
        "hi": "2004",
        "en": "2004"
      },
      {
        "letter": "B",
        "hi": "2005",
        "en": "2005"
      },
      {
        "letter": "C",
        "hi": "2006",
        "en": "2006"
      },
      {
        "letter": "D",
        "hi": "2007",
        "en": "2007"
      }
    ],
    "correct": "C",
    "exp_hi": "MGNREGA 2 फरवरी 2006 को शुरू हुआ।",
    "exp_en": "MGNREGA started on 2 February 2006.",
    "exam_tag": "UPSC 2019",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "LIC की स्थापना कब हुई?",
    "q_en": "When was LIC established?",
    "options": [
      {
        "letter": "A",
        "hi": "1950",
        "en": "1950"
      },
      {
        "letter": "B",
        "hi": "1956",
        "en": "1956"
      },
      {
        "letter": "C",
        "hi": "1960",
        "en": "1960"
      },
      {
        "letter": "D",
        "hi": "1965",
        "en": "1965"
      }
    ],
    "correct": "B",
    "exp_hi": "LIC की स्थापना 1 सितंबर 1956 को हुई।",
    "exp_en": "LIC was established on 1 September 1956.",
    "exam_tag": "SSC 2020",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में PM किसान योजना कब शुरू हुई?",
    "q_en": "When did PM Kisan Yojana start?",
    "options": [
      {
        "letter": "A",
        "hi": "2018",
        "en": "2018"
      },
      {
        "letter": "B",
        "hi": "2019",
        "en": "2019"
      },
      {
        "letter": "C",
        "hi": "2020",
        "en": "2020"
      },
      {
        "letter": "D",
        "hi": "2021",
        "en": "2021"
      }
    ],
    "correct": "B",
    "exp_hi": "PM किसान सम्मान निधि योजना फरवरी 2019 में शुरू हुई।",
    "exp_en": "PM Kisan Samman Nidhi Yojana started in February 2019.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में राष्ट्रीय आय की गणना कौन करता है?",
    "q_en": "Who calculates national income in India?",
    "options": [
      {
        "letter": "A",
        "hi": "RBI",
        "en": "RBI"
      },
      {
        "letter": "B",
        "hi": "CSO/NSO",
        "en": "CSO/NSO"
      },
      {
        "letter": "C",
        "hi": "SEBI",
        "en": "SEBI"
      },
      {
        "letter": "D",
        "hi": "NITI Aayog",
        "en": "NITI Aayog"
      }
    ],
    "correct": "B",
    "exp_hi": "CSO/NSO (Central Statistics Office) राष्ट्रीय आय की गणना करता है।",
    "exp_en": "CSO/NSO (Central Statistics Office) calculates national income.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में वस्तु एवं सेवा कर (GST) कितने प्रकार का है?",
    "q_en": "How many types of GST in India?",
    "options": [
      {
        "letter": "A",
        "hi": "2",
        "en": "2"
      },
      {
        "letter": "B",
        "hi": "3",
        "en": "3"
      },
      {
        "letter": "C",
        "hi": "4",
        "en": "4"
      },
      {
        "letter": "D",
        "hi": "5",
        "en": "5"
      }
    ],
    "correct": "B",
    "exp_hi": "GST 3 प्रकार का है - CGST, SGST, IGST।",
    "exp_en": "GST is of 3 types - CGST, SGST, IGST.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में सबसे बड़ी बीमा कंपनी?",
    "q_en": "Largest insurance company in India?",
    "options": [
      {
        "letter": "A",
        "hi": "New India Assurance",
        "en": "New India Assurance"
      },
      {
        "letter": "B",
        "hi": "LIC",
        "en": "LIC"
      },
      {
        "letter": "C",
        "hi": "ICICI Lombard",
        "en": "ICICI Lombard"
      },
      {
        "letter": "D",
        "hi": "Bajaj Allianz",
        "en": "Bajaj Allianz"
      }
    ],
    "correct": "B",
    "exp_hi": "LIC भारत की सबसे बड़ी बीमा कंपनी है।",
    "exp_en": "LIC is India's largest insurance company.",
    "exam_tag": "Railway 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में निर्यात को बढ़ावा देने वाली संस्था?",
    "q_en": "Export promotion body in India?",
    "options": [
      {
        "letter": "A",
        "hi": "SEBI",
        "en": "SEBI"
      },
      {
        "letter": "B",
        "hi": "EXIM Bank",
        "en": "EXIM Bank"
      },
      {
        "letter": "C",
        "hi": "RBI",
        "en": "RBI"
      },
      {
        "letter": "D",
        "hi": "NABARD",
        "en": "NABARD"
      }
    ],
    "correct": "B",
    "exp_hi": "EXIM Bank भारत में निर्यात-आयात को बढ़ावा देती है।",
    "exp_en": "EXIM Bank promotes exports-imports in India.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'मेक इन इंडिया' अभियान कब शुरू हुआ?",
    "q_en": "When did 'Make in India' campaign start?",
    "options": [
      {
        "letter": "A",
        "hi": "2013",
        "en": "2013"
      },
      {
        "letter": "B",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "C",
        "hi": "2015",
        "en": "2015"
      },
      {
        "letter": "D",
        "hi": "2016",
        "en": "2016"
      }
    ],
    "correct": "B",
    "exp_hi": "'मेक इन इंडिया' 25 सितंबर 2014 को शुरू हुआ।",
    "exp_en": "'Make in India' started on 25 September 2014.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'स्टार्टअप इंडिया' कब शुरू हुआ?",
    "q_en": "When did 'Startup India' start?",
    "options": [
      {
        "letter": "A",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "B",
        "hi": "2015",
        "en": "2015"
      },
      {
        "letter": "C",
        "hi": "2016",
        "en": "2016"
      },
      {
        "letter": "D",
        "hi": "2017",
        "en": "2017"
      }
    ],
    "correct": "C",
    "exp_hi": "'स्टार्टअप इंडिया' 16 जनवरी 2016 को शुरू हुआ।",
    "exp_en": "'Startup India' started on 16 January 2016.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'डिजिटल इंडिया' अभियान कब शुरू हुआ?",
    "q_en": "When did 'Digital India' start?",
    "options": [
      {
        "letter": "A",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "B",
        "hi": "2015",
        "en": "2015"
      },
      {
        "letter": "C",
        "hi": "2016",
        "en": "2016"
      },
      {
        "letter": "D",
        "hi": "2017",
        "en": "2017"
      }
    ],
    "correct": "B",
    "exp_hi": "'डिजिटल इंडिया' 1 जुलाई 2015 को शुरू हुआ।",
    "exp_en": "'Digital India' started on 1 July 2015.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में आयुष्मान भारत योजना कब शुरू हुई?",
    "q_en": "When did Ayushman Bharat start?",
    "options": [
      {
        "letter": "A",
        "hi": "2017",
        "en": "2017"
      },
      {
        "letter": "B",
        "hi": "2018",
        "en": "2018"
      },
      {
        "letter": "C",
        "hi": "2019",
        "en": "2019"
      },
      {
        "letter": "D",
        "hi": "2020",
        "en": "2020"
      }
    ],
    "correct": "B",
    "exp_hi": "आयुष्मान भारत योजना 23 सितंबर 2018 को शुरू हुई।",
    "exp_en": "Ayushman Bharat started on 23 September 2018.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'उज्ज्वला योजना' किससे संबंधित है?",
    "q_en": "Ujjwala Yojana is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "बिजली",
        "en": "Electricity"
      },
      {
        "letter": "B",
        "hi": "LPG गैस",
        "en": "LPG gas"
      },
      {
        "letter": "C",
        "hi": "पानी",
        "en": "Water"
      },
      {
        "letter": "D",
        "hi": "शिक्षा",
        "en": "Education"
      }
    ],
    "correct": "B",
    "exp_hi": "उज्ज्वला योजना BPL परिवारों को मुफ्त LPG कनेक्शन देती है।",
    "exp_en": "Ujjwala Yojana provides free LPG connections to BPL families.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में PMGSY किससे संबंधित है?",
    "q_en": "PMGSY is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "ग्रामीण सड़क",
        "en": "Rural roads"
      },
      {
        "letter": "B",
        "hi": "ग्रामीण विद्युत",
        "en": "Rural electricity"
      },
      {
        "letter": "C",
        "hi": "ग्रामीण जल",
        "en": "Rural water"
      },
      {
        "letter": "D",
        "hi": "ग्रामीण आवास",
        "en": "Rural housing"
      }
    ],
    "correct": "A",
    "exp_hi": "PMGSY (प्रधानमंत्री ग्राम सड़क योजना) ग्रामीण सड़क से संबंधित है।",
    "exp_en": "PMGSY (PM Gram Sadak Yojana) is related to rural roads.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'स्वच्छ भारत मिशन' कब शुरू हुआ?",
    "q_en": "When did Swachh Bharat Mission start?",
    "options": [
      {
        "letter": "A",
        "hi": "2013",
        "en": "2013"
      },
      {
        "letter": "B",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "C",
        "hi": "2015",
        "en": "2015"
      },
      {
        "letter": "D",
        "hi": "2016",
        "en": "2016"
      }
    ],
    "correct": "B",
    "exp_hi": "स्वच्छ भारत मिशन 2 अक्टूबर 2014 को शुरू हुआ।",
    "exp_en": "Swachh Bharat Mission started on 2 October 2014.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'PM आवास योजना' कब शुरू हुई?",
    "q_en": "When did PM Awas Yojana start?",
    "options": [
      {
        "letter": "A",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "B",
        "hi": "2015",
        "en": "2015"
      },
      {
        "letter": "C",
        "hi": "2016",
        "en": "2016"
      },
      {
        "letter": "D",
        "hi": "2017",
        "en": "2017"
      }
    ],
    "correct": "B",
    "exp_hi": "PM आवास योजना 25 जून 2015 को शुरू हुई।",
    "exp_en": "PM Awas Yojana started on 25 June 2015.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में सोने का आयात सबसे अधिक कहाँ से होता है?",
    "q_en": "India imports most gold from?",
    "options": [
      {
        "letter": "A",
        "hi": "अमेरिका",
        "en": "USA"
      },
      {
        "letter": "B",
        "hi": "रूस",
        "en": "Russia"
      },
      {
        "letter": "C",
        "hi": "UAE",
        "en": "UAE"
      },
      {
        "letter": "D",
        "hi": "स्विट्जरलैंड",
        "en": "Switzerland"
      }
    ],
    "correct": "D",
    "exp_hi": "भारत स्विट्जरलैंड से सबसे अधिक सोना आयात करता है।",
    "exp_en": "India imports most gold from Switzerland.",
    "exam_tag": "Railway 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'PM-KISAN' योजना में किसानों को कितनी राशि मिलती है?",
    "q_en": "How much do farmers get under PM-KISAN scheme?",
    "options": [
      {
        "letter": "A",
        "hi": "₹4000 प्रति वर्ष",
        "en": "₹4000 per year"
      },
      {
        "letter": "B",
        "hi": "₹6000 प्रति वर्ष",
        "en": "₹6000 per year"
      },
      {
        "letter": "C",
        "hi": "₹8000 प्रति वर्ष",
        "en": "₹8000 per year"
      },
      {
        "letter": "D",
        "hi": "₹10000 प्रति वर्ष",
        "en": "₹10000 per year"
      }
    ],
    "correct": "B",
    "exp_hi": "PM-KISAN में किसानों को ₹6000 प्रति वर्ष (₹2000 की 3 किस्तों में) मिलते हैं।",
    "exp_en": "PM-KISAN provides ₹6000 per year (in 3 installments of ₹2000).",
    "exam_tag": "CTET 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'गरीबी रेखा' कौन निर्धारित करता है?",
    "q_en": "Who determines poverty line in India?",
    "options": [
      {
        "letter": "A",
        "hi": "RBI",
        "en": "RBI"
      },
      {
        "letter": "B",
        "hi": "NITI Aayog",
        "en": "NITI Aayog"
      },
      {
        "letter": "C",
        "hi": "संसद",
        "en": "Parliament"
      },
      {
        "letter": "D",
        "hi": "वित्त मंत्रालय",
        "en": "Finance Ministry"
      }
    ],
    "correct": "B",
    "exp_hi": "NITI Aayog गरीबी रेखा निर्धारित करता है।",
    "exp_en": "NITI Aayog determines poverty line in India.",
    "exam_tag": "CTET 2024",
    "class": "कक्षा 9"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'मुद्रा' का निर्गमन कौन करता है?",
    "q_en": "Who issues currency in India?",
    "options": [
      {
        "letter": "A",
        "hi": "SBI",
        "en": "SBI"
      },
      {
        "letter": "B",
        "hi": "वित्त मंत्रालय",
        "en": "Finance Ministry"
      },
      {
        "letter": "C",
        "hi": "RBI",
        "en": "RBI"
      },
      {
        "letter": "D",
        "hi": "SEBI",
        "en": "SEBI"
      }
    ],
    "correct": "C",
    "exp_hi": "RBI भारत में मुद्रा (नोट) निर्गमित करता है।",
    "exp_en": "RBI issues currency (notes) in India.",
    "exam_tag": "Railway 2024",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'राजकोषीय घाटा' क्या है?",
    "q_en": "What is fiscal deficit in India?",
    "options": [
      {
        "letter": "A",
        "hi": "आयात - निर्यात",
        "en": "Import - Export"
      },
      {
        "letter": "B",
        "hi": "सरकारी व्यय - सरकारी आय",
        "en": "Govt expenditure - Govt income"
      },
      {
        "letter": "C",
        "hi": "GDP - GNP",
        "en": "GDP - GNP"
      },
      {
        "letter": "D",
        "hi": "मुद्रास्फीति - अपस्फीति",
        "en": "Inflation - Deflation"
      }
    ],
    "correct": "B",
    "exp_hi": "राजकोषीय घाटा = सरकारी कुल व्यय - सरकारी कुल आय।",
    "exp_en": "Fiscal deficit = Total govt expenditure - Total govt income.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'बालिका समृद्धि योजना' किससे संबंधित है?",
    "q_en": "Balika Samridhi Yojana is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "बालिकाओं की शिक्षा",
        "en": "Education of girls"
      },
      {
        "letter": "B",
        "hi": "बालिकाओं का स्वास्थ्य",
        "en": "Health of girls"
      },
      {
        "letter": "C",
        "hi": "बालिकाओं की वित्तीय सहायता",
        "en": "Financial support to girls"
      },
      {
        "letter": "D",
        "hi": "बालिकाओं का रोजगार",
        "en": "Employment of girls"
      }
    ],
    "correct": "C",
    "exp_hi": "बालिका समृद्धि योजना बालिकाओं को जन्म से लेकर शिक्षा तक वित्तीय सहायता देती है।",
    "exp_en": "Balika Samridhi Yojana provides financial support to girls from birth to education.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 9"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'सुकन्या समृद्धि योजना' कब शुरू हुई?",
    "q_en": "When did Sukanya Samridhi Yojana start?",
    "options": [
      {
        "letter": "A",
        "hi": "2013",
        "en": "2013"
      },
      {
        "letter": "B",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "C",
        "hi": "2015",
        "en": "2015"
      },
      {
        "letter": "D",
        "hi": "2016",
        "en": "2016"
      }
    ],
    "correct": "C",
    "exp_hi": "सुकन्या समृद्धि योजना 22 जनवरी 2015 को शुरू हुई।",
    "exp_en": "Sukanya Samridhi Yojana started on 22 January 2015.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "'मिश्रित अर्थव्यवस्था' का अर्थ?",
    "q_en": "What is 'Mixed Economy'?",
    "options": [
      {
        "letter": "A",
        "hi": "केवल सरकारी",
        "en": "Only government"
      },
      {
        "letter": "B",
        "hi": "केवल निजी",
        "en": "Only private"
      },
      {
        "letter": "C",
        "hi": "सरकारी और निजी दोनों",
        "en": "Both public and private"
      },
      {
        "letter": "D",
        "hi": "विदेशी नियंत्रण",
        "en": "Foreign control"
      }
    ],
    "correct": "C",
    "exp_hi": "मिश्रित अर्थव्यवस्था में सरकारी और निजी दोनों क्षेत्र होते हैं।",
    "exp_en": "Mixed economy has both public and private sectors.",
    "exam_tag": "CTET 2020",
    "class": "कक्षा 9"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'सोने का कड़ा' योजना किससे संबंधित है?",
    "q_en": "Gold Monetization Scheme in India is for?",
    "options": [
      {
        "letter": "A",
        "hi": "सोना निर्यात",
        "en": "Gold export"
      },
      {
        "letter": "B",
        "hi": "घर में रखे सोने को बैंक में जमा करना",
        "en": "Depositing gold at home in banks"
      },
      {
        "letter": "C",
        "hi": "सोना खरीदना",
        "en": "Buying gold"
      },
      {
        "letter": "D",
        "hi": "सोना आयात",
        "en": "Gold import"
      }
    ],
    "correct": "B",
    "exp_hi": "Gold Monetization Scheme में घर या मंदिर में रखे सोने को बैंक में जमा किया जाता है।",
    "exp_en": "Gold Monetization Scheme allows depositing idle gold in banks.",
    "exam_tag": "SSC 2021",
    "class": "कक्षา 10"
  },
  {
    "subject": "economics",
    "q_hi": "'राजस्व घाटा' क्या होता है?",
    "q_en": "What is Revenue Deficit?",
    "options": [
      {
        "letter": "A",
        "hi": "राजस्व प्राप्ति - राजस्व व्यय",
        "en": "Revenue receipts - Revenue expenditure"
      },
      {
        "letter": "B",
        "hi": "राजस्व व्यय - राजस्व प्राप्ति",
        "en": "Revenue expenditure - Revenue receipts"
      },
      {
        "letter": "C",
        "hi": "पूंजी प्राप्ति - पूंजी व्यय",
        "en": "Capital receipts - Capital expenditure"
      },
      {
        "letter": "D",
        "hi": "कुल आय - कुल व्यय",
        "en": "Total income - Total expenditure"
      }
    ],
    "correct": "B",
    "exp_hi": "राजस्व घाटा = राजस्व व्यय - राजस्व प्राप्ति।",
    "exp_en": "Revenue Deficit = Revenue Expenditure - Revenue Receipts.",
    "exam_tag": "Railway 2019",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "'नेट टैक्स रिसीट्स' किसमें आती हैं?",
    "q_en": "Net Tax Receipts come under?",
    "options": [
      {
        "letter": "A",
        "hi": "पूंजी प्राप्ति",
        "en": "Capital receipts"
      },
      {
        "letter": "B",
        "hi": "राजस्व प्राप्ति",
        "en": "Revenue receipts"
      },
      {
        "letter": "C",
        "hi": "ऋण",
        "en": "Debt"
      },
      {
        "letter": "D",
        "hi": "अनुदान",
        "en": "Grant"
      }
    ],
    "correct": "B",
    "exp_hi": "कर राजस्व प्राप्तियों में आता है।",
    "exp_en": "Tax comes under revenue receipts.",
    "exam_tag": "UPSC 2020",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'राष्ट्रीय ग्रामीण रोजगार गारंटी' कितने दिन का रोजगार देती है?",
    "q_en": "MGNREGA guarantees how many days of employment?",
    "options": [
      {
        "letter": "A",
        "hi": "50 दिन",
        "en": "50 days"
      },
      {
        "letter": "B",
        "hi": "75 दिन",
        "en": "75 days"
      },
      {
        "letter": "C",
        "hi": "100 दिन",
        "en": "100 days"
      },
      {
        "letter": "D",
        "hi": "150 दिन",
        "en": "150 days"
      }
    ],
    "correct": "C",
    "exp_hi": "MGNREGA प्रत्येक ग्रामीण परिवार को 100 दिन का रोजगार देती है।",
    "exp_en": "MGNREGA guarantees 100 days of employment per rural household.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में PLI स्कीम में कितने क्षेत्र शामिल हैं?",
    "q_en": "How many sectors under PLI scheme?",
    "options": [
      {
        "letter": "A",
        "hi": "10",
        "en": "10"
      },
      {
        "letter": "B",
        "hi": "14",
        "en": "14"
      },
      {
        "letter": "C",
        "hi": "16",
        "en": "16"
      },
      {
        "letter": "D",
        "hi": "20",
        "en": "20"
      }
    ],
    "correct": "B",
    "exp_hi": "PLI स्कीम में 14 क्षेत्र शामिल हैं।",
    "exp_en": "PLI scheme covers 14 sectors.",
    "exam_tag": "Railway 2020",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'महंगाई भत्ता' (DA) किसे मिलता है?",
    "q_en": "Who gets Dearness Allowance (DA) in India?",
    "options": [
      {
        "letter": "A",
        "hi": "किसानों को",
        "en": "Farmers"
      },
      {
        "letter": "B",
        "hi": "सरकारी कर्मचारियों को",
        "en": "Govt employees"
      },
      {
        "letter": "C",
        "hi": "उद्योगपतियों को",
        "en": "Industrialists"
      },
      {
        "letter": "D",
        "hi": "सभी को",
        "en": "Everyone"
      }
    ],
    "correct": "B",
    "exp_hi": "महंगाई भत्ता सरकारी कर्मचारियों और पेंशनधारियों को मिलता है।",
    "exp_en": "Dearness Allowance is given to government employees and pensioners.",
    "exam_tag": "UPSC 2021",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'NPA' (Non-Performing Assets) क्या है?",
    "q_en": "What is NPA (Non-Performing Assets)?",
    "options": [
      {
        "letter": "A",
        "hi": "बैंक की सम्पत्ति",
        "en": "Bank's property"
      },
      {
        "letter": "B",
        "hi": "डूबा हुआ कर्ज",
        "en": "Bad loans"
      },
      {
        "letter": "C",
        "hi": "विदेशी निवेश",
        "en": "Foreign investment"
      },
      {
        "letter": "D",
        "hi": "सरकारी बॉन्ड",
        "en": "Government bonds"
      }
    ],
    "correct": "B",
    "exp_hi": "NPA वे ऋण हैं जिनकी वसूली 90 दिनों से अधिक समय से नहीं हुई।",
    "exp_en": "NPA are loans where recovery hasn't happened for 90+ days.",
    "exam_tag": "SSC 2021",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "'मुद्रा स्फीति' (Inflation) का मुख्य कारण?",
    "q_en": "Main cause of Inflation?",
    "options": [
      {
        "letter": "A",
        "hi": "उत्पादन में कमी",
        "en": "Fall in production"
      },
      {
        "letter": "B",
        "hi": "मुद्रा आपूर्ति में वृद्धि",
        "en": "Increase in money supply"
      },
      {
        "letter": "C",
        "hi": "निर्यात में वृद्धि",
        "en": "Rise in exports"
      },
      {
        "letter": "D",
        "hi": "B और A दोनों",
        "en": "Both A and B"
      }
    ],
    "correct": "D",
    "exp_hi": "मुद्रास्फीति के मुख्य कारण हैं - उत्पादन में कमी और मुद्रा आपूर्ति में वृद्धि।",
    "exp_en": "Main causes of inflation - fall in production and rise in money supply.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'GST परिषद' कब बनी?",
    "q_en": "When was GST Council formed?",
    "options": [
      {
        "letter": "A",
        "hi": "2015",
        "en": "2015"
      },
      {
        "letter": "B",
        "hi": "2016",
        "en": "2016"
      },
      {
        "letter": "C",
        "hi": "2017",
        "en": "2017"
      },
      {
        "letter": "D",
        "hi": "2018",
        "en": "2018"
      }
    ],
    "correct": "B",
    "exp_hi": "GST परिषद 12 सितंबर 2016 को बनी।",
    "exp_en": "GST Council was formed on 12 September 2016.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "'राष्ट्रीय आय' को मापने के कितने तरीके हैं?",
    "q_en": "How many methods to measure National Income?",
    "options": [
      {
        "letter": "A",
        "hi": "2",
        "en": "2"
      },
      {
        "letter": "B",
        "hi": "3",
        "en": "3"
      },
      {
        "letter": "C",
        "hi": "4",
        "en": "4"
      },
      {
        "letter": "D",
        "hi": "5",
        "en": "5"
      }
    ],
    "correct": "B",
    "exp_hi": "राष्ट्रीय आय मापने के 3 तरीके हैं - उत्पाद, आय और व्यय विधि।",
    "exp_en": "National Income is measured by 3 methods - Product, Income and Expenditure.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'SBI' की स्थापना कब हुई?",
    "q_en": "When was SBI established?",
    "options": [
      {
        "letter": "A",
        "hi": "1948",
        "en": "1948"
      },
      {
        "letter": "B",
        "hi": "1955",
        "en": "1955"
      },
      {
        "letter": "C",
        "hi": "1960",
        "en": "1960"
      },
      {
        "letter": "D",
        "hi": "1969",
        "en": "1969"
      }
    ],
    "correct": "B",
    "exp_hi": "SBI की स्थापना 1 जुलाई 1955 को हुई।",
    "exp_en": "SBI was established on 1 July 1955.",
    "exam_tag": "Railway 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'आर्थिक सर्वेक्षण' कब जारी होता है?",
    "q_en": "When is Economic Survey released in India?",
    "options": [
      {
        "letter": "A",
        "hi": "बजट से पहले",
        "en": "Before Budget"
      },
      {
        "letter": "B",
        "hi": "बजट के बाद",
        "en": "After Budget"
      },
      {
        "letter": "C",
        "hi": "बजट के साथ",
        "en": "With Budget"
      },
      {
        "letter": "D",
        "hi": "मार्च में",
        "en": "In March"
      }
    ],
    "correct": "A",
    "exp_hi": "आर्थिक सर्वेक्षण हर वर्ष बजट से एक दिन पहले जारी होता है।",
    "exp_en": "Economic Survey is released one day before Budget every year.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 9"
  },
  {
    "subject": "economics",
    "q_hi": "'IRDAI' किससे संबंधित है?",
    "q_en": "IRDAI is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "बैंकिंग",
        "en": "Banking"
      },
      {
        "letter": "B",
        "hi": "बीमा",
        "en": "Insurance"
      },
      {
        "letter": "C",
        "hi": "पूंजी बाजार",
        "en": "Capital market"
      },
      {
        "letter": "D",
        "hi": "विदेश व्यापार",
        "en": "Foreign trade"
      }
    ],
    "correct": "B",
    "exp_hi": "IRDAI (Insurance Regulatory and Development Authority of India) बीमा क्षेत्र को नियंत्रित करती है।",
    "exp_en": "IRDAI regulates the insurance sector.",
    "exam_tag": "SSC 2022",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में सबसे अधिक कमाई किस क्षेत्र से होती है?",
    "q_en": "Which sector earns maximum in India?",
    "options": [
      {
        "letter": "A",
        "hi": "कृषि",
        "en": "Agriculture"
      },
      {
        "letter": "B",
        "hi": "उद्योग",
        "en": "Industry"
      },
      {
        "letter": "C",
        "hi": "सेवा",
        "en": "Services"
      },
      {
        "letter": "D",
        "hi": "खनन",
        "en": "Mining"
      }
    ],
    "correct": "C",
    "exp_hi": "सेवा क्षेत्र भारत की GDP में सर्वाधिक योगदान देता है।",
    "exp_en": "Service sector contributes most to India's GDP.",
    "exam_tag": "CTET 2022",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'मॉनेटरी पॉलिसी' कमेटी (MPC) कब बनी?",
    "q_en": "When was Monetary Policy Committee (MPC) formed?",
    "options": [
      {
        "letter": "A",
        "hi": "2014",
        "en": "2014"
      },
      {
        "letter": "B",
        "hi": "2016",
        "en": "2016"
      },
      {
        "letter": "C",
        "hi": "2018",
        "en": "2018"
      },
      {
        "letter": "D",
        "hi": "2020",
        "en": "2020"
      }
    ],
    "correct": "B",
    "exp_hi": "MPC का गठन 2016 में हुआ।",
    "exp_en": "MPC was formed in 2016.",
    "exam_tag": "UPSC 2022",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'RuPay Card' किसने लॉन्च किया?",
    "q_en": "Who launched RuPay Card in India?",
    "options": [
      {
        "letter": "A",
        "hi": "RBI",
        "en": "RBI"
      },
      {
        "letter": "B",
        "hi": "SBI",
        "en": "SBI"
      },
      {
        "letter": "C",
        "hi": "NPCI",
        "en": "NPCI"
      },
      {
        "letter": "D",
        "hi": "SEBI",
        "en": "SEBI"
      }
    ],
    "correct": "C",
    "exp_hi": "NPCI (National Payments Corporation of India) ने RuPay Card लॉन्च किया।",
    "exp_en": "NPCI launched RuPay Card in India.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 9"
  },
  {
    "subject": "economics",
    "q_hi": "'वस्तु विनिमय' (Barter) प्रणाली की मुख्य समस्या?",
    "q_en": "Main problem of Barter system?",
    "options": [
      {
        "letter": "A",
        "hi": "भारी वस्तुएं",
        "en": "Heavy goods"
      },
      {
        "letter": "B",
        "hi": "आवश्यकताओं का दोहरा संयोग",
        "en": "Double coincidence of wants"
      },
      {
        "letter": "C",
        "hi": "दूरी की समस्या",
        "en": "Distance problem"
      },
      {
        "letter": "D",
        "hi": "समय की बर्बादी",
        "en": "Waste of time"
      }
    ],
    "correct": "B",
    "exp_hi": "वस्तु विनिमय की मुख्य समस्या 'आवश्यकताओं का दोहरा संयोग' है।",
    "exp_en": "Main problem of Barter is 'Double Coincidence of Wants'.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'FEMA' कब लागू हुआ?",
    "q_en": "When was FEMA implemented in India?",
    "options": [
      {
        "letter": "A",
        "hi": "1998",
        "en": "1998"
      },
      {
        "letter": "B",
        "hi": "1999",
        "en": "1999"
      },
      {
        "letter": "C",
        "hi": "2000",
        "en": "2000"
      },
      {
        "letter": "D",
        "hi": "2001",
        "en": "2001"
      }
    ],
    "correct": "C",
    "exp_hi": "FEMA (Foreign Exchange Management Act) 2000 में लागू हुआ।",
    "exp_en": "FEMA (Foreign Exchange Management Act) was implemented in 2000.",
    "exam_tag": "UPSC 2023",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "'PMVVY' (Pradhan Mantri Vaya Vandana Yojana) किनके लिए है?",
    "q_en": "PMVVY is for which group?",
    "options": [
      {
        "letter": "A",
        "hi": "बच्चों के लिए",
        "en": "Children"
      },
      {
        "letter": "B",
        "hi": "किसानों के लिए",
        "en": "Farmers"
      },
      {
        "letter": "C",
        "hi": "वरिष्ठ नागरिकों के लिए",
        "en": "Senior citizens"
      },
      {
        "letter": "D",
        "hi": "महिलाओं के लिए",
        "en": "Women"
      }
    ],
    "correct": "C",
    "exp_hi": "PMVVY 60 वर्ष से ऊपर के वरिष्ठ नागरिकों के लिए पेंशन योजना है।",
    "exp_en": "PMVVY is a pension scheme for senior citizens above 60 years.",
    "exam_tag": "SSC 2023",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "'बैंक दर' (Bank Rate) किसे कहते हैं?",
    "q_en": "What is Bank Rate?",
    "options": [
      {
        "letter": "A",
        "hi": "बैंकों द्वारा ब्याज दर",
        "en": "Interest rate charged by banks"
      },
      {
        "letter": "B",
        "hi": "RBI द्वारा बैंकों को उधार देने की दर",
        "en": "Rate at which RBI lends to banks"
      },
      {
        "letter": "C",
        "hi": "विदेशी मुद्रा दर",
        "en": "Foreign exchange rate"
      },
      {
        "letter": "D",
        "hi": "मुद्रास्फीति दर",
        "en": "Inflation rate"
      }
    ],
    "correct": "B",
    "exp_hi": "बैंक दर वह दर है जिस पर RBI बैंकों को ऋण देता है।",
    "exp_en": "Bank Rate is the rate at which RBI lends to banks.",
    "exam_tag": "CTET 2023",
    "class": "कक्षा 9"
  },
  {
    "subject": "economics",
    "q_hi": "'CRR' (Cash Reserve Ratio) का अर्थ?",
    "q_en": "What is CRR (Cash Reserve Ratio)?",
    "options": [
      {
        "letter": "A",
        "hi": "बैंकों को RBI के पास रखी नकदी",
        "en": "Cash banks keep with RBI"
      },
      {
        "letter": "B",
        "hi": "सरकारी बॉन्ड",
        "en": "Government bonds"
      },
      {
        "letter": "C",
        "hi": "विदेशी मुद्रा भंडार",
        "en": "Foreign exchange reserve"
      },
      {
        "letter": "D",
        "hi": "बैंक का मुनाफा",
        "en": "Bank profit"
      }
    ],
    "correct": "A",
    "exp_hi": "CRR वह अनुपात है जो बैंकों को अपनी जमाराशि का RBI के पास रखना होता है।",
    "exp_en": "CRR is the ratio of deposits banks must keep with RBI.",
    "exam_tag": "Railway 2023",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "'SLR' (Statutory Liquidity Ratio) क्या है?",
    "q_en": "What is SLR (Statutory Liquidity Ratio)?",
    "options": [
      {
        "letter": "A",
        "hi": "बैंकों को सरकारी प्रतिभूतियों में रखना",
        "en": "Banks must keep in govt securities"
      },
      {
        "letter": "B",
        "hi": "RBI के पास नकदी",
        "en": "Cash with RBI"
      },
      {
        "letter": "C",
        "hi": "विदेशी निवेश",
        "en": "Foreign investment"
      },
      {
        "letter": "D",
        "hi": "बैंक का मुनाफा",
        "en": "Bank profit"
      }
    ],
    "correct": "A",
    "exp_hi": "SLR वह अनुपात है जो बैंकों को सरकारी प्रतिभूतियों में रखना होता है।",
    "exp_en": "SLR is ratio banks must maintain in government securities.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 11"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'MSME' का पूरा नाम?",
    "q_en": "Full form of MSME in India?",
    "options": [
      {
        "letter": "A",
        "hi": "Micro, Small and Medium Enterprises",
        "en": "Micro, Small and Medium Enterprises"
      },
      {
        "letter": "B",
        "hi": "Major, Small and Medium Enterprises",
        "en": "Major, Small and Medium Enterprises"
      },
      {
        "letter": "C",
        "hi": "Micro, Standard and Major Enterprises",
        "en": "Micro, Standard and Major Enterprises"
      },
      {
        "letter": "D",
        "hi": "Modern, Small and Medium Enterprises",
        "en": "Modern, Small and Medium Enterprises"
      }
    ],
    "correct": "A",
    "exp_hi": "MSME का अर्थ Micro, Small and Medium Enterprises है।",
    "exp_en": "MSME stands for Micro, Small and Medium Enterprises.",
    "exam_tag": "UPSC 2024",
    "class": "कक्षा 12"
  },
  {
    "subject": "economics",
    "q_hi": "'FPI' (Foreign Portfolio Investment) क्या है?",
    "q_en": "What is FPI?",
    "options": [
      {
        "letter": "A",
        "hi": "विदेशी प्रत्यक्ष निवेश",
        "en": "Foreign Direct Investment"
      },
      {
        "letter": "B",
        "hi": "विदेशी शेयर बाजार निवेश",
        "en": "Foreign stock market investment"
      },
      {
        "letter": "C",
        "hi": "सरकारी निवेश",
        "en": "Government investment"
      },
      {
        "letter": "D",
        "hi": "बैंक जमा",
        "en": "Bank deposits"
      }
    ],
    "correct": "B",
    "exp_hi": "FPI विदेशी निवेशकों द्वारा भारतीय शेयर बाजार में किया गया निवेश है।",
    "exp_en": "FPI is investment by foreign investors in Indian stock markets.",
    "exam_tag": "SSC 2024",
    "class": "कक्षा 9"
  },
  {
    "subject": "economics",
    "q_hi": "भारत में 'PMEGP' योजना किससे संबंधित है?",
    "q_en": "PMEGP scheme is related to?",
    "options": [
      {
        "letter": "A",
        "hi": "कृषि",
        "en": "Agriculture"
      },
      {
        "letter": "B",
        "hi": "लघु उद्योग रोजगार",
        "en": "Small industry employment"
      },
      {
        "letter": "C",
        "hi": "आवास",
        "en": "Housing"
      },
      {
        "letter": "D",
        "hi": "शिक्षा",
        "en": "Education"
      }
    ],
    "correct": "B",
    "exp_hi": "PMEGP (Prime Minister's Employment Generation Programme) लघु उद्योगों के लिए है।",
    "exp_en": "PMEGP is for small industry employment generation.",
    "exam_tag": "CTET 2024",
    "class": "कक्षा 10"
  },
  {
    "subject": "economics",
    "q_hi": "'RBI का REPO दर' क्या है?",
    "q_en": "What is RBI's REPO Rate?",
    "options": [
      {
        "letter": "A",
        "hi": "बैंकों द्वारा ग्राहकों को ब्याज",
        "en": "Interest by banks to customers"
      },
      {
        "letter": "B",
        "hi": "RBI द्वारा बैंकों को अल्पकालिक ऋण दर",
        "en": "Short-term lending rate by RBI to banks"
      },
      {
        "letter": "C",
        "hi": "विदेशी मुद्रा दर",
        "en": "Foreign exchange rate"
      },
      {
        "letter": "D",
        "hi": "मुद्रास्फीति दर",
        "en": "Inflation rate"
      }
    ],
    "correct": "B",
    "exp_hi": "REPO दर वह दर है जिस पर RBI बैंकों को अल्पकालिक ऋण देता है।",
    "exp_en": "REPO Rate is the rate at which RBI gives short-term loans to banks.",
    "exam_tag": "Railway 2024",
    "class": "कक्षा 11"
  }
]

SUBJECTS = {
    "history": "इतिहास",
    "geography": "भूगोल", 
    "economics": "अर्थशास्त्र",
    "polity": "राजनीति",
    "mixed": "मिश्रित"
}

def get_next_question(user_id, subject):
    """No-repeat: track seen questions per user per subject, reset when all done"""
    state = user_states.setdefault(user_id, {})
    
    # Get pool based on subject
    if subject == "mixed":
        pool = QUESTIONS
    else:
        pool = [q for q in QUESTIONS if q["subject"] == subject]
    
    if not pool:
        pool = QUESTIONS
    
    # Get seen set for this subject
    seen_key = f"seen_{subject}"
    seen = state.get(seen_key, set())
    
    # Get unseen questions
    pool_indices = set(range(len(pool)))
    unseen = pool_indices - seen
    
    # If all seen, reset
    if not unseen:
        seen = set()
        unseen = pool_indices
        state[seen_key] = seen
    
    # Pick random from unseen
    idx = random.choice(list(unseen))
    seen.add(idx)
    state[seen_key] = seen
    
    return pool[idx]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {"subject": "history", "score": 0, "total": 0, "streak": 0}
    
    total = len(QUESTIONS)
    keyboard = [
        [InlineKeyboardButton("🎯 Mini App में खेलें", web_app={"url": MINI_APP_URL})],
        [InlineKeyboardButton("⚔️ इतिहास", callback_data="sub_history"), InlineKeyboardButton("🌍 भूगोल", callback_data="sub_geography")],
        [InlineKeyboardButton("📈 अर्थशास्त्र", callback_data="sub_economics"), InlineKeyboardButton("🏛️ राजनीति", callback_data="sub_polity")],
        [InlineKeyboardButton("🎲 मिश्रित", callback_data="sub_mixed")],
        [InlineKeyboardButton("🚀 Quiz शुरू करें!", callback_data="start_quiz")]
    ]
    await update.message.reply_text(
        f"🎯 *NCERT Quiz Bot में स्वागत है!*\n\n"
        f"📚 {total}+ MCQs | इतिहास | भूगोल | अर्थशास्त्र | राजनीति\n"
        f"🎓 UPSC | SSC | Railway | CTET\n"
        f"✅ No-Repeat System - सभी MCQ होने तक repeat नहीं!\n\n"
        f"विषय चुनें 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if user_id not in user_states:
        user_states[user_id] = {"subject": "history", "score": 0, "total": 0, "streak": 0}
    state = user_states[user_id]

    if data.startswith("sub_"):
        state["subject"] = data[4:]
        sub_name = SUBJECTS.get(state["subject"], "")
        
        # Count available questions for this subject
        if state["subject"] == "mixed":
            total_sub = len(QUESTIONS)
        else:
            total_sub = len([q for q in QUESTIONS if q["subject"] == state["subject"]])
        
        seen_key = f"seen_{state['subject']}"
        seen_count = len(state.get(seen_key, set()))
        remaining = total_sub - seen_count
        
        await query.edit_message_text(
            f"✅ विषय: *{sub_name}*\n"
            f"📊 कुल प्रश्न: {total_sub}\n"
            f"🔄 बाकी: {remaining} प्रश्न\n\n"
            f"तैयार हैं?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🚀 Quiz शुरू करें!", callback_data="start_quiz")
            ]])
        )

    elif data == "start_quiz":
        await send_question(query.message.chat_id, context, user_id)

    elif data.startswith("ans_"):
        parts = data.split("_")
        selected = parts[1]
        correct = parts[2]
        state["total"] = state.get("total", 0) + 1

        if selected == correct:
            state["score"] = state.get("score", 0) + 1
            state["streak"] = state.get("streak", 0) + 1
            result = f"✅ *सही! Correct!* 🎉\n🔥 Streak: {state['streak']}"
        else:
            state["streak"] = 0
            result = f"❌ *गलत! Wrong!*\n✅ सही उत्तर: *{correct}*"

        exp = context.user_data.get(f"{user_id}_exp", {})
        exp_text = ""
        if exp:
            exp_text = f"\n\n💡 *व्याख्या:*\n{exp.get('hi', '')}\n_{exp.get('en', '')}_"

        keyboard = [
            [InlineKeyboardButton("➡️ अगला प्रश्न", callback_data="next_q")],
            [InlineKeyboardButton("📊 Score", callback_data="show_score"),
             InlineKeyboardButton("🔄 विषय बदलें", callback_data="change_sub")]
        ]
        await query.edit_message_text(
            result + exp_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "next_q":
        await send_question(query.message.chat_id, context, user_id)

    elif data == "show_score":
        total = state.get("total", 0)
        score = state.get("score", 0)
        pct = round((score / total) * 100) if total > 0 else 0
        emoji = "🏆" if pct >= 80 else "👍" if pct >= 60 else "📚"
        
        sub = state.get("subject", "mixed")
        seen_key = f"seen_{sub}"
        if sub == "mixed":
            total_sub = len(QUESTIONS)
        else:
            total_sub = len([q for q in QUESTIONS if q["subject"] == sub])
        seen_count = len(state.get(seen_key, set()))
        
        await query.edit_message_text(
            f"{emoji} *आपका Score*\n\n"
            f"✅ सही: {score}/{total}\n"
            f"📊 प्रतिशत: {pct}%\n"
            f"🔥 Streak: {state.get('streak', 0)}\n\n"
            f"📚 देखे गए: {seen_count}/{total_sub} प्रश्न",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("➡️ अगला", callback_data="next_q"),
                InlineKeyboardButton("🏠 Menu", callback_data="change_sub")
            ]])
        )

    elif data == "change_sub":
        keyboard = [
            [InlineKeyboardButton("⚔️ इतिहास", callback_data="sub_history"),
             InlineKeyboardButton("🌍 भूगोल", callback_data="sub_geography")],
            [InlineKeyboardButton("📈 अर्थशास्त्र", callback_data="sub_economics"),
             InlineKeyboardButton("🏛️ राजनीति", callback_data="sub_polity")],
            [InlineKeyboardButton("🎲 मिश्रित", callback_data="sub_mixed")],
            [InlineKeyboardButton("🎯 Mini App", web_app={"url": MINI_APP_URL})]
        ]
        await query.edit_message_text("विषय चुनें 👇", reply_markup=InlineKeyboardMarkup(keyboard))


async def send_question(chat_id, context, user_id):
    state = user_states.get(user_id, {"subject": "mixed"})
    subject = state.get("subject", "mixed")
    
    q = get_next_question(user_id, subject)
    
    # Save explanation for later
    context.user_data[f"{user_id}_exp"] = {
        "hi": q.get("exp_hi", ""),
        "en": q.get("exp_en", "")
    }
    
    correct = q.get("correct", "A")
    keyboard = []
    for opt in q.get("options", []):
        keyboard.append([InlineKeyboardButton(
            opt["letter"] + ". " + opt["hi"],
            callback_data=f"ans_{opt['letter']}_{correct}"
        )])

    # Show progress
    sub = subject
    seen_key = f"seen_{sub}"
    if sub == "mixed":
        total_sub = len(QUESTIONS)
    else:
        total_sub = len([q2 for q2 in QUESTIONS if q2["subject"] == sub])
    seen_count = len(state.get(seen_key, set()))

    msg = (
        f"📌 *{q.get('class', '')} | {SUBJECTS.get(subject, '')}*\n"
        f"🏷️ _{q.get('exam_tag', '')}_\n"
        f"📊 {seen_count}/{total_sub}\n\n"
        f"❓ *{q.get('q_hi', '')}*\n\n"
        f"_{q.get('q_en', '')}_\n\n"
        f"उत्तर चुनें 👇"
    )
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=msg,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def main():
    print(f"Bot shuru ho raha hai... {len(QUESTIONS)} MCQs loaded!")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot chalu hai!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
