# -*- coding: utf-8 -*-
"""All text content for the Desi Games Studio in English (en), Hindi (hi) and Telugu (te).
Hindi and Telugu were written by me and MUST be reviewed by native speakers before printing."""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
CRICKET_TABLE = json.load(open(os.path.join(HERE, "cricket_table.json")))   # [shot][delivery] -> six faces

NAMES = {
    "title": {"en": "Cricket Dhamaka", "hi": "क्रिकेट धमाका", "te": "క్రికెట్ ధమాకా"},
    "shots": {"en": ["Defend", "Drive", "Slog"], "hi": ["बचाव", "ड्राइव", "स्लॉग"], "te": ["రక్షణ", "డ్రైవ్", "స్లాగ్"]},
    "deliv": {"en": ["Yorker", "Bouncer", "Spin"], "hi": ["यॉर्कर", "बाउंसर", "स्पिन"], "te": ["యార్కర్", "బౌన్సర్", "స్పిన్"]},
    "shot_word": {"en": "SHOT", "hi": "शॉट", "te": "షాట్"},
    "deliv_word": {"en": "DELIVERY", "hi": "गेंद", "te": "బంతి"},
    "table_title": {"en": "Result table (roll a d6)", "hi": "रिज़ल्ट टेबल (पासा फेंकें)", "te": "ఫలిత పట్టిక (పాచిక వేయండి)"},
    "table_note": {"en": "Row = batter's shot, column = bowler's delivery. Die face 1-6 = left to right. W = OUT.",
                   "hi": "पंक्ति = शॉट, स्तंभ = गेंद। पासे का अंक 1-6 = बाएँ से दाएँ। W = आउट।",
                   "te": "వరుస = షాట్, నిలువు వరుస = బంతి. పాచిక సంఖ్య 1-6 = ఎడమ నుండి కుడికి. W = అవుట్."},
}

RULES = {
 "cricket": {
  "en": ["Cricket Dhamaka - 2 players, age 8+, 15 minutes. You need: the card sets, a d6 (die), pen and paper.",
         "Each player has 3 Shot cards (Defend, Drive, Slog) and 3 Delivery cards (Yorker, Bouncer, Spin).",
         "An innings is 12 balls (2 overs) or 2 wickets, whichever comes first.",
         "Each ball: the batter secretly picks a Shot card and the bowler a Delivery card. Reveal together.",
         "Roll the die. Find the row (shot) and column (delivery) in the Result table and read the face that matches the die.",
         "W means OUT. Any number is runs. Add runs to the score sheet.",
         "After the innings swap roles. More runs wins. A tie is settled by a super over: 1 over, 1 wicket."],
  "hi": ["क्रिकेट धमाका - 2 खिलाड़ी, 8+ वर्ष, 15 मिनट। चाहिए: कार्ड सेट, एक पासा, कागज़ और पेन।",
         "हर खिलाड़ी के पास 3 शॉट कार्ड (बचाव, ड्राइव, स्लॉग) और 3 गेंद कार्ड (यॉर्कर, बाउंसर, स्पिन) हैं।",
         "एक पारी = 12 गेंदें (2 ओवर) या 2 विकेट, जो पहले हो।",
         "हर गेंद पर बल्लेबाज़ चुपचाप एक शॉट कार्ड और गेंदबाज़ एक गेंद कार्ड चुनता है। दोनों साथ में दिखाएँ।",
         "पासा फेंकें। रिज़ल्ट टेबल में शॉट की पंक्ति और गेंद का स्तंभ देखें और पासे के अंक वाला नतीजा पढ़ें।",
         "W का मतलब आउट। संख्या का मतलब रन। रन स्कोर शीट में जोड़ें।",
         "पारी के बाद भूमिकाएँ बदलें। ज़्यादा रन वाला जीतता है। बराबरी पर सुपर ओवर: 1 ओवर, 1 विकेट।"],
  "te": ["క్రికెట్ ధమాకా - 2 ఆటగాళ్లు, 8+ ఏళ్లు, 15 నిమిషాలు. కావలసినవి: కార్డుల సెట్, ఒక పాచిక, కాగితం, పెన్.",
         "ప్రతి ఆటగాడికి 3 షాట్ కార్డులు (రక్షణ, డ్రైవ్, స్లాగ్), 3 బంతి కార్డులు (యార్కర్, బౌన్సర్, స్పిన్) ఉంటాయి.",
         "ఒక ఇన్నింగ్స్ = 12 బంతులు (2 ఓవర్లు) లేదా 2 వికెట్లు, ఏది ముందైతే అది.",
         "ప్రతి బంతికి బ్యాటర్ ఒక షాట్ కార్డును, బౌలర్ ఒక బంతి కార్డును రహస్యంగా ఎంచుకోవాలి. ఇద్దరూ ఒకేసారి చూపించాలి.",
         "పాచిక వేయండి. ఫలిత పట్టికలో షాట్ వరుస, బంతి నిలువు వరుస చూసి, పాచిక సంఖ్యకు సరిపోయే ఫలితం చదవండి.",
         "W అంటే అవుట్. సంఖ్య అంటే పరుగులు. పరుగులను స్కోరు షీట్‌లో కలపండి.",
         "ఇన్నింగ్స్ తర్వాత పాత్రలు మార్చుకోండి. ఎక్కువ పరుగులు చేసినవారు గెలుస్తారు. సమమైతే సూపర్ ఓవర్: 1 ఓవర్, 1 వికెట్."],
 },
 "ganit": {
  "en": ["Ganit Ladder - 2 to 4 players, age 8+, 20-30 minutes. You need: the board, a token each, a d6, the Table cards.",
         "Everyone starts off the board. Roll the die and move that many squares. Ladders take you up, snakes take you down.",
         "You must roll the exact number to land on 100.",
         "If you land on a ? square, take a Table card and answer. The answer is printed upside down on the card; another player checks it.",
         "Correct answer: roll again (you may chain more ? squares). Wrong answer: go back 4 squares (never below 1).",
         "The first player to reach 100 wins."],
  "hi": ["गणित सीढ़ी - 2 से 4 खिलाड़ी, 8+ वर्ष, 20-30 मिनट। चाहिए: बोर्ड, हर खिलाड़ी की एक गोटी, पासा, पहाड़ा कार्ड।",
         "सब बोर्ड के बाहर से शुरू करते हैं। पासा फेंकें और उतने खाने चलें। सीढ़ी ऊपर ले जाती है, साँप नीचे ले आता है।",
         "100 पर पहुँचने के लिए ठीक उतना ही अंक आना चाहिए।",
         "अगर आप ? वाले खाने पर आएँ तो एक पहाड़ा कार्ड लेकर जवाब दें। जवाब कार्ड पर उल्टा छपा है; दूसरा खिलाड़ी जाँचेगा।",
         "सही जवाब: दोबारा पासा फेंकें (और ? खाने आएँ तो फिर से)। गलत जवाब: 4 खाने पीछे जाएँ (1 से नीचे नहीं)।",
         "100 पर सबसे पहले पहुँचने वाला जीतता है।"],
  "te": ["గణిత నిచ్చెన - 2 నుండి 4 ఆటగాళ్లు, 8+ ఏళ్లు, 20-30 నిమిషాలు. కావలసినవి: బోర్డు, ఒక్కొక్కరికి ఒక పావు, పాచిక, ఎక్కాల కార్డులు.",
         "అందరూ బోర్డు బయట నుండి మొదలుపెడతారు. పాచిక వేసి అన్ని గడులు ముందుకు వెళ్లండి. నిచ్చెన పైకి, పాము కిందికి తీసుకెళ్తాయి.",
         "100కు చేరాలంటే సరిగ్గా అంత సంఖ్య రావాలి.",
         "? గడిపై ఆగితే ఒక ఎక్కాల కార్డు తీసి జవాబు చెప్పండి. జవాబు కార్డుపై తలకిందులుగా ముద్రించి ఉంటుంది; మరొకరు సరిచూస్తారు.",
         "సరైన జవాబు: మళ్ళీ పాచిక వేయండి (మరో ? గడి వస్తే మళ్ళీ). తప్పు జవాబు: 4 గడులు వెనక్కి (1 కంటే తక్కువ కాదు).",
         "100కు ముందుగా చేరినవారు గెలుస్తారు."],
 },
 "yatra": {
  "en": ["India Yatra - 2 to 6 players, age 8+, 20 minutes. You need: the question cards.",
         "Shuffle the cards. On your turn another player reads the question and the three choices A, B, C.",
         "Say your answer. The correct answer is printed upside down at the bottom of the card.",
         "Correct: you keep the card (1 point). Wrong: the next player may try the same card to steal the point.",
         "The first player with 10 cards wins."],
  "hi": ["इंडिया यात्रा - 2 से 6 खिलाड़ी, 8+ वर्ष, 20 मिनट। चाहिए: सवाल कार्ड।",
         "कार्ड फेंटें। आपकी बारी पर कोई दूसरा खिलाड़ी सवाल और तीन विकल्प A, B, C पढ़ता है।",
         "अपना जवाब बताएँ। सही जवाब कार्ड के नीचे उल्टा छपा है।",
         "सही: कार्ड आपका (1 अंक)। गलत: अगला खिलाड़ी वही कार्ड आज़माकर अंक ले सकता है।",
         "सबसे पहले 10 कार्ड जीतने वाला विजेता है।"],
  "te": ["ఇండియా యాత్ర - 2 నుండి 6 ఆటగాళ్లు, 8+ ఏళ్లు, 20 నిమిషాలు. కావలసినవి: ప్రశ్నల కార్డులు.",
         "కార్డులను కలపండి. మీ వంతులో మరొకరు ప్రశ్న, A, B, C మూడు ఎంపికలు చదువుతారు.",
         "మీ జవాబు చెప్పండి. సరైన జవాబు కార్డు అడుగున తలకిందులుగా ముద్రించి ఉంటుంది.",
         "సరైనది: కార్డు మీది (1 పాయింట్). తప్పు: తదుపరి ఆటగాడు అదే కార్డు ప్రయత్నించి పాయింట్ తీసుకోవచ్చు.",
         "ముందుగా 10 కార్డులు గెలిచినవారు విజేత."],
 },
 "mandi": {
  "en": ["Sabzi Mandi - 2 to 4 players, age 7+, 25 minutes. You need: Item cards, Money cards, a till tray, paper for scores.",
         "One player is the shopkeeper. The shopkeeper's till starts with: Rs 20 x1, Rs 10 x3, Rs 5 x6, Rs 2 x10, Rs 1 x12.",
         "A customer draws 1 to 3 Item cards (add the prices; the total may not exceed Rs 45) and pays with the smallest note that covers the bill (Rs 5, 10, 20 or 50).",
         "The shopkeeper gives the exact change from the till. If that is impossible, the shopkeeper may ask the bank to break ONE note ('chhutta') once per sale.",
         "Correct change: shopkeeper +2 points. Wrong change: the customer who spots it gets +1 and the shopkeeper -1.",
         "After 12 sales swap shopkeeper. Most points wins."],
  "hi": ["सब्ज़ी मंडी - 2 से 4 खिलाड़ी, 7+ वर्ष, 25 मिनट। चाहिए: सामान कार्ड, पैसे कार्ड, गल्ला ट्रे, स्कोर के लिए कागज़।",
         "एक खिलाड़ी दुकानदार बनता है। गल्ले में शुरू में: 20 रु x1, 10 रु x3, 5 रु x6, 2 रु x10, 1 रु x12।",
         "ग्राहक 1 से 3 सामान कार्ड लेता है (दाम जोड़ें; कुल 45 रु से ज़्यादा नहीं) और बिल से बड़ा सबसे छोटा नोट (5, 10, 20 या 50 रु) देता है।",
         "दुकानदार गल्ले से ठीक-ठीक बाकी पैसे लौटाता है। अगर नहीं हो सके तो हर बिक्री में एक बार बैंक से एक नोट तुड़वा (छुट्टा) सकता है।",
         "सही बाकी: दुकानदार +2 अंक। गलत बाकी: जो ग्राहक गलती पकड़े उसे +1 और दुकानदार को -1।",
         "12 बिक्री के बाद दुकानदार बदलें। सबसे ज़्यादा अंक वाला जीतता है।"],
  "te": ["కూరగాయల మార్కెట్ - 2 నుండి 4 ఆటగాళ్లు, 7+ ఏళ్లు, 25 నిమిషాలు. కావలసినవి: వస్తువుల కార్డులు, డబ్బు కార్డులు, గల్లా ట్రే, స్కోరు కాగితం.",
         "ఒక ఆటగాడు దుకాణదారుడు. గల్లాలో మొదట: 20 రూ x1, 10 రూ x3, 5 రూ x6, 2 రూ x10, 1 రూ x12.",
         "కస్టమర్ 1 నుండి 3 వస్తువుల కార్డులు తీసుకుంటాడు (ధరలు కూడండి; మొత్తం 45 రూ మించకూడదు), బిల్లును మించిన అతి చిన్న నోటు (5, 10, 20 లేదా 50 రూ) ఇస్తాడు.",
         "దుకాణదారుడు గల్లా నుండి సరిగ్గా మిగిలిన చిల్లర ఇవ్వాలి. సాధ్యం కాకపోతే, ప్రతి అమ్మకానికి ఒకసారి బ్యాంకు నుండి ఒక నోటును చిల్లరగా మార్చుకోవచ్చు.",
         "సరైన చిల్లర: దుకాణదారుడికి +2 పాయింట్లు. తప్పు చిల్లర: పట్టుకున్న కస్టమర్‌కు +1, దుకాణదారుడికి -1.",
         "12 అమ్మకాల తర్వాత దుకాణదారుడిని మార్చండి. ఎక్కువ పాయింట్లు వచ్చినవారు గెలుస్తారు."],
 },
}

# ---- India Yatra quiz: correct answer FIRST in each option list; render rotates it so A/B/C are balanced
YATRA = [
 (dict(en="What is the capital of India?", hi="भारत की राजधानी क्या है?", te="భారతదేశ రాజధాని ఏది?"),
  dict(en=["New Delhi", "Mumbai", "Kolkata"], hi=["नई दिल्ली", "मुंबई", "कोलकाता"], te=["న్యూఢిల్లీ", "ముంబై", "కోల్‌కతా"])),
 (dict(en="What is the capital of Telangana?", hi="तेलंगाना की राजधानी क्या है?", te="తెలంగాణ రాజధాని ఏది?"),
  dict(en=["Hyderabad", "Warangal", "Karimnagar"], hi=["हैदराबाद", "वारंगल", "करीमनगर"], te=["హైదరాబాద్", "వరంగల్", "కరీంనగర్"])),
 (dict(en="Which is India's national animal?", hi="भारत का राष्ट्रीय पशु कौन सा है?", te="భారతదేశ జాతీయ జంతువు ఏది?"),
  dict(en=["Tiger", "Lion", "Elephant"], hi=["बाघ", "शेर", "हाथी"], te=["పులి", "సింహం", "ఏనుగు"])),
 (dict(en="Which is India's national bird?", hi="भारत का राष्ट्रीय पक्षी कौन सा है?", te="భారతదేశ జాతీయ పక్షి ఏది?"),
  dict(en=["Peacock", "Parrot", "Sparrow"], hi=["मोर", "तोता", "गौरैया"], te=["నెమలి", "చిలుక", "పిచ్చుక"])),
 (dict(en="Which is India's national flower?", hi="भारत का राष्ट्रीय फूल कौन सा है?", te="భారతదేశ జాతీయ పుష్పం ఏది?"),
  dict(en=["Lotus", "Rose", "Marigold"], hi=["कमल", "गुलाब", "गेंदा"], te=["తామర", "గులాబీ", "బంతి"])),
 (dict(en="Which is India's national fruit?", hi="भारत का राष्ट्रीय फल कौन सा है?", te="భారతదేశ జాతీయ ఫలం ఏది?"),
  dict(en=["Mango", "Apple", "Banana"], hi=["आम", "सेब", "केला"], te=["మామిడి", "ఆపిల్", "అరటి"])),
 (dict(en="Which is India's national river?", hi="भारत की राष्ट्रीय नदी कौन सी है?", te="భారతదేశ జాతీయ నది ఏది?"),
  dict(en=["Ganga", "Yamuna", "Godavari"], hi=["गंगा", "यमुना", "गोदावरी"], te=["గంగ", "యమున", "గోదావరి"])),
 (dict(en="Which is the highest mountain peak in India?", hi="भारत की सबसे ऊँची पर्वत चोटी कौन सी है?", te="భారతదేశంలో ఎత్తైన పర్వత శిఖరం ఏది?"),
  dict(en=["Kanchenjunga", "Nanda Devi", "Anamudi"], hi=["कंचनजंगा", "नंदा देवी", "अनाईमुडी"], te=["కాంచనజంగ", "నందాదేవి", "ఆనైముడి"])),
 (dict(en="Which is the largest state of India by area?", hi="क्षेत्रफल में भारत का सबसे बड़ा राज्य कौन सा है?", te="విస్తీర్ణంలో భారతదేశంలో అతి పెద్ద రాష్ట్రం ఏది?"),
  dict(en=["Rajasthan", "Maharashtra", "Madhya Pradesh"], hi=["राजस्थान", "महाराष्ट्र", "मध्य प्रदेश"], te=["రాజస్థాన్", "మహారాష్ట్ర", "మధ్యప్రదేశ్"])),
 (dict(en="In which city is the Taj Mahal?", hi="ताजमहल किस शहर में है?", te="తాజ్ మహల్ ఏ నగరంలో ఉంది?"),
  dict(en=["Agra", "Jaipur", "Delhi"], hi=["आगरा", "जयपुर", "दिल्ली"], te=["ఆగ్రా", "జైపూర్", "ఢిల్లీ"])),
 (dict(en="In which city is the Charminar?", hi="चारमीनार किस शहर में है?", te="చార్మినార్ ఏ నగరంలో ఉంది?"),
  dict(en=["Hyderabad", "Chennai", "Bengaluru"], hi=["हैदराबाद", "चेन्नई", "बेंगलुरु"], te=["హైదరాబాద్", "చెన్నై", "బెంగళూరు"])),
 (dict(en="In which city is the Gateway of India?", hi="गेटवे ऑफ़ इंडिया किस शहर में है?", te="గేట్‌వే ఆఫ్ ఇండియా ఏ నగరంలో ఉంది?"),
  dict(en=["Mumbai", "Kolkata", "Goa"], hi=["मुंबई", "कोलकाता", "गोवा"], te=["ముంబై", "కోల్‌కతా", "గోవా"])),
 (dict(en="Which colour is at the top of the Indian flag?", hi="भारतीय झंडे में सबसे ऊपर कौन सा रंग है?", te="భారత జెండాలో పైన ఉండే రంగు ఏది?"),
  dict(en=["Saffron", "Green", "White"], hi=["केसरिया", "हरा", "सफ़ेद"], te=["కాషాయం", "ఆకుపచ్చ", "తెలుపు"])),
 (dict(en="Who is called the Father of the Nation?", hi="राष्ट्रपिता किसे कहा जाता है?", te="జాతిపిత అని ఎవరిని పిలుస్తారు?"),
  dict(en=["Mahatma Gandhi", "Jawaharlal Nehru", "B. R. Ambedkar"], hi=["महात्मा गांधी", "जवाहरलाल नेहरू", "बी. आर. अंबेडकर"], te=["మహాత్మా గాంధీ", "జవహర్‌లాల్ నెహ్రూ", "బి. ఆర్. అంబేద్కర్"])),
 (dict(en="When is Republic Day celebrated?", hi="गणतंत्र दिवस कब मनाया जाता है?", te="గణతంత్ర దినోత్సవం ఎప్పుడు జరుపుకుంటారు?"),
  dict(en=["26 January", "15 August", "2 October"], hi=["26 जनवरी", "15 अगस्त", "2 अक्टूबर"], te=["జనవరి 26", "ఆగస్టు 15", "అక్టోబర్ 2"])),
 (dict(en="When is Independence Day celebrated?", hi="स्वतंत्रता दिवस कब मनाया जाता है?", te="స్వాతంత్ర్య దినోత్సవం ఎప్పుడు జరుపుకుంటారు?"),
  dict(en=["15 August", "26 January", "14 November"], hi=["15 अगस्त", "26 जनवरी", "14 नवंबर"], te=["ఆగస్టు 15", "జనవరి 26", "నవంబర్ 14"])),
 (dict(en="Which planet is called the Red Planet?", hi="किस ग्रह को लाल ग्रह कहते हैं?", te="ఏ గ్రహాన్ని ఎర్ర గ్రహం అంటారు?"),
  dict(en=["Mars", "Venus", "Jupiter"], hi=["मंगल", "शुक्र", "बृहस्पति"], te=["అంగారకుడు", "శుక్రుడు", "గురుడు"])),
 (dict(en="What is Earth's natural satellite?", hi="पृथ्वी का प्राकृतिक उपग्रह कौन सा है?", te="భూమి సహజ ఉపగ్రహం ఏది?"),
  dict(en=["The Moon", "The Sun", "A comet"], hi=["चंद्रमा", "सूर्य", "धूमकेतु"], te=["చంద్రుడు", "సూర్యుడు", "తోకచుక్క"])),
 (dict(en="Which is the hardest natural substance?", hi="सबसे कठोर प्राकृतिक पदार्थ कौन सा है?", te="అత్యంత గట్టి సహజ పదార్థం ఏది?"),
  dict(en=["Diamond", "Gold", "Iron"], hi=["हीरा", "सोना", "लोहा"], te=["వజ్రం", "బంగారం", "ఇనుము"])),
 (dict(en="Which gas do we need to breathe to live?", hi="जीने के लिए हमें कौन सी गैस साँस में चाहिए?", te="బ్రతకడానికి మనం పీల్చవలసిన వాయువు ఏది?"),
  dict(en=["Oxygen", "Hydrogen", "Helium"], hi=["ऑक्सीजन", "हाइड्रोजन", "हीलियम"], te=["ఆక్సిజన్", "హైడ్రోజన్", "హీలియం"])),
 (dict(en="Which is the largest planet in our solar system?", hi="हमारे सौरमंडल का सबसे बड़ा ग्रह कौन सा है?", te="మన సౌర కుటుంబంలో అతి పెద్ద గ్రహం ఏది?"),
  dict(en=["Jupiter", "Earth", "Mars"], hi=["बृहस्पति", "पृथ्वी", "मंगल"], te=["గురుడు", "భూమి", "అంగారకుడు"])),
 (dict(en="Which is the fastest land animal?", hi="सबसे तेज़ दौड़ने वाला ज़मीनी जानवर कौन सा है?", te="అత్యంత వేగంగా పరుగెత్తే భూమి జంతువు ఏది?"),
  dict(en=["Cheetah", "Horse", "Deer"], hi=["चीता", "घोड़ा", "हिरण"], te=["చిరుత", "గుర్రం", "జింక"])),
 (dict(en="How many players of one team are on the field in cricket?", hi="क्रिकेट में एक टीम के कितने खिलाड़ी मैदान पर होते हैं?", te="క్రికెట్‌లో ఒక జట్టు నుండి మైదానంలో ఎంతమంది ఆటగాళ్లు ఉంటారు?"),
  dict(en=["11", "9", "12"], hi=["11", "9", "12"], te=["11", "9", "12"])),
 (dict(en="Which Indian mission landed near the Moon's south pole in 2023?", hi="2023 में चंद्रमा के दक्षिणी ध्रुव के पास कौन सा भारतीय मिशन उतरा?", te="2023లో చంద్రుని దక్షిణ ధ్రువం దగ్గర దిగిన భారత మిషన్ ఏది?"),
  dict(en=["Chandrayaan-3", "Mangalyaan", "Aryabhata"], hi=["चंद्रयान-3", "मंगलयान", "आर्यभट्ट"], te=["చంద్రయాన్-3", "మంగళయాన్", "ఆర్యభట్ట"])),
]

def yatra_cards(lang):
    """Return [(question, [A,B,C], answer_letter)] with the correct option rotated through A/B/C."""
    out = []
    for i, (q, opts) in enumerate(YATRA):
        o = list(opts[lang]); k = i % 3
        correct = o[0]
        rest = o[1:]
        shuffled = rest[:k] + [correct] + rest[k:]
        out.append((q[lang], shuffled, "ABC"[k]))
    return out

# ---- Ganit Ladder table cards: 60 distinct products from tables 2-12
def table_cards(seed=11, n=60):
    rng = random.Random(seed)
    pairs = [(a, b) for a in range(2, 13) for b in range(2, 13) if a <= b and a * b >= 12]
    rng.shuffle(pairs)
    return [(f"{a} x {b} = ?", a * b) for a, b in pairs[:n]]

# ---- Sabzi Mandi items (price list matches sim_ganit_mandi.PRICES)
ITEMS = [  # price, en, hi, te, colour
 (3, "Green chilli", "हरी मिर्च", "పచ్చిమిర్చి", (46, 139, 87)),
 (4, "Coriander", "धनिया", "కొత్తిమీర", (60, 179, 113)),
 (6, "Lemon", "नींबू", "నిమ్మకాయ", (230, 200, 40)),
 (7, "Spinach", "पालक", "పాలకూర", (34, 139, 34)),
 (8, "Potato", "आलू", "బంగాళాదుంప", (181, 140, 90)),
 (9, "Carrot", "गाजर", "క్యారెట్", (237, 120, 30)),
 (12, "Tomato", "टमाटर", "టమాటా", (214, 48, 49)),
 (14, "Onion", "प्याज़", "ఉల్లిపాయ", (150, 70, 140)),
 (15, "Brinjal", "बैंगन", "వంకాయ", (88, 50, 120)),
 (18, "Okra", "भिंडी", "బెండకాయ", (107, 142, 35)),
 (22, "Cabbage", "पत्ता गोभी", "క్యాబేజీ", (140, 190, 90)),
 (25, "Cauliflower", "फूलगोभी", "కాలీఫ్లవర్", (200, 190, 150)),
]
MONEY = {1: 24, 2: 24, 5: 24, 10: 18, 20: 12, 50: 6}   # money cards to print (108 = 9 pages)
