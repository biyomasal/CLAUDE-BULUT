"""Content for the 55 MEB biyoloji kazanımları (9, 10, 11. sınıf) – one reel each."""

R = []


def add(id_, style, hook, close, sub=None, **kw):
    R.append(dict(id=id_, grade=int(id_.split(".")[0]), style=style, hook=hook, close=close, sub=sub, **kw))


# ------------------------------------------------------------------ 9. sınıf
add("9.1.1", "rank", "HAYATINI DEĞİŞTİREN\n3 BİYOLOJİ KEŞFİ", "Dönüm noktaları\nhayatımızı değiştirdi",
    sub="Sen hangisini seçerdin?",
    items=[("Antibiyotik · 1928", "Alexander Fleming: penisilin bakterileri öldürür"),
           ("DNA çift sarmal · 1953", "Franklin, Watson, Crick: kalıtımın molekülü"),
           ("CRISPR-Cas · 2012", "Doudna ve Charpentier: genleri düzenleme")])
add("9.1.2", "chat", "BİLİM HİÇ\nDEĞİŞMEZ Mİ?", "Bilim bir kanıt\nve sorgulama işidir",
    msgs=[("L", "Bilim insanları bir şeyi kanıtlayınca hep doğru mu kalır?"),
          ("R", "Hayır! Bilimsel bilgi geçicidir: yeni kanıt gelirse güncellenir."),
          ("L", "Peki bilim neye dayanır?"),
          ("R", "Gözlem, deney ve kanıta. Hayal gücü de bilimin parçasıdır.")])
add("9.1.3", "swipe", "BU ARAŞTIRMA\nETİK Mİ?", "Bilim dürüstlükle\nbüyür", labels=("ETİK", "ETİK DEĞİL"),
    items=[(True, "Katılımcıdan izin almak.", "Gönüllü onam bilim etiğidir."),
           (False, "Verileri istediğin gibi değiştirmek.", "Veri sahteciliği etik dışıdır."),
           (True, "Kaynakları belirtmek.", "Başkasının emeğine saygı gösterilir."),
           (False, "Başkasının sonucunu kendi sonucun gibi sunmak.", "Aşırma (intihal) etik dışıdır.")])
add("9.1.4", "quiz", "VİRÜS CANLI MI\nCANSIZ MI?", "Virüsler canlı mı?\nBilim hâlâ tartışıyor",
    q="Virüsler neden net şekilde canlı sayılmaz?",
    opts=["Çok küçük oldukları için", "Hücresel yapıları yok, tek başına üreyemezler",
          "Hareket edemedikleri için", "Besin tüketmedikleri için"], ok=1,
    expl="Konak hücre olmadan üreyemezler, kendi metabolizmaları yoktur.")
add("9.1.5", "stats", "SU VE MİNERALLER\nNEDEN ŞART?", "Su ve mineraller\nyaşamın temeli",
    items=[dict(pre="~%", val=65, label="Yetişkin vücudunun yaklaşık su oranı"),
           dict(val=4.18, dec=2, label="Suyun öz ısısı (J/g·°C): vücut ısısını dengeler"),
           dict(pre="~%", val=99, label="Vücuttaki kalsiyumun yaklaşık yüzdesi kemik ve dişlerde")])
add("9.1.6", "flip", "ORGANİK MOLEKÜLLERİN\nYAPI TAŞLARI NE?", "Küçük yapı taşları,\nbüyük moleküller",
    labels=("MOLEKÜL", "YAPI TAŞI"),
    cards=[("Karbohidrat", "Monosakkarit (glikoz gibi)"), ("Protein", "Amino asit"),
           ("Lipit", "Gliserol + yağ asidi"), ("Nükleik asit", "Nükleotit")])
add("9.1.7", "lab", "BESİNDE NİŞASTA\nVAR MI?", "Ayraçlarla besinin\nyapısını keşfet", kind="lab_color",
    title="Lugol çözeltisi deneyi", colors=[(255, 228, 150), (250, 200, 90), (60, 50, 130)],
    steps=[("Hazırlık", "Besin örneğine biraz su ekle"), ("Ayraç", "Lugol çözeltisi damlat"),
           ("Sonuç", "Mavi-siyah renk: nişasta var!")])
add("9.1.8", "bars", "ISI ARTARSA ENZİMLERE\nNE OLUR?", "Enzimler en iyi\nuygun sıcaklıkta çalışır",
    title="Enzim aktivitesi ve sıcaklık", note="Örnek veri · aktivite %",
    bars=[("10°C", 25), ("25°C", 60), ("37°C", 100), ("50°C", 45), ("70°C", 5)], hi=2,
    punch="Aşırı ısı enzimi bozar (denatürasyon)")
add("9.2.1", "diagram", "HÜCRENİN İÇİNDE\nNELER VAR?", "Her organelin\nbir görevi var", center="HÜCRE",
    parts=[("Çekirdek", "Kalıtım bilgisini yönetir"), ("Mitokondri", "ATP üretir: enerji santrali"),
           ("Ribozom", "Protein sentezler"), ("Hücre zarı", "Madde geçişini kontrol eder")])
add("9.2.2", "sorter", "ATP HARCAYAN MI,\nHARCAMAYAN MI?", "Madde geçişi:\nenerjili mi, enerjisiz mi?",
    bins=["PASİF\n(ATP yok)", "AKTİF\n(ATP var)"],
    items=[("Difüzyon", 0), ("Aktif taşıma", 1), ("Ozmoz", 0), ("Endositoz", 1),
           ("Kolaylaştırılmış difüzyon", 0), ("Ekzositoz", 1)])
add("9.2.3", "versus", "PATATES DİLİMİ TUZLU\nSUDA NE OLUR?", "Ozmoz: su, seyrelikten\nderişiğe geçer",
    sides=("SAF SU", "TUZLU SU"),
    rows=[("Su hücreye girer", "Su hücreden çıkar"), ("Dilim şişer, sertleşir", "Dilim büzülür, yumuşar"),
          ("Ortam seyreltik", "Ortam derişik")])
add("9.2.4", "flow", "CANLILAR NASIL\nGRUPLANIR?", "Küçükten büyüğe\nsınıflandırma",
    steps=[("Tür", "Üreyip verimli döl verebilen bireyler"), ("Cins", "Birbirine yakın türler"),
           ("Familya", "Yakın cinslerin grubu"), ("Âlem", "En geniş sınıflandırma basamağı")])
add("9.2.5", "quiz", "3 ÜST ÂLEM:\nHANGİSİ ÇEKİRDEKLİ?", "Bacteria, Archaea,\nEukarya",
    q="Üç üst âlem sisteminde çekirdekli hücrelere sahip olan hangisidir?",
    opts=["Bacteria", "Archaea", "Eukarya", "Hiçbiri"], ok=2,
    expl="Eukarya: çekirdekli ve zarlı organelli hücreler.")
add("9.2.6", "stats", "TÜRKİYE BİYOÇEŞİTLİLİKTE\nNEREDE?", "Zengin biyoçeşitlilik,\nkorunması gereken miras",
    items=[dict(pre="~", val=12000, label="Doğal yetişen bitki taksonu (yaklaşık)"),
           dict(pre="~%", val=30, label="Bunların yaklaşık üçte biri endemik (sadece Türkiye'de)"),
           dict(static="3", label="Biyocoğrafik bölge: Avrupa-Sibirya, Akdeniz, İran-Turan")])

# ----------------------------------------------------------------- 10. sınıf
add("10.1.1", "reveal", "ENERJİ OLMADAN\nYAŞAM OLUR MU?", "Yaşamak enerji\ngerektirir!",
    facts=["Uyurken bile kalp, solunum ve beyin çalışır; enerji harcarsın.",
           "Beyin vücut ağırlığının yaklaşık %2’sidir ama enerjinin yaklaşık %20’sini kullanır.",
           "Çoğu ekosistemde enerjinin kaynağı Güneş’tir."])
add("10.1.2", "flow", "BİTKİLER IŞIKTAN\nNASIL BESİN YAPAR?", "Fotosentez:\nyaşamın enerji kaynağı",
    steps=[("Işık", "Klorofil ışık enerjisini soğurur"), ("Su + CO₂", "Köklerden su, yapraklardan CO₂ girer"),
           ("Kloroplast", "Işık enerjisi kimyasal enerjiye dönüşür"),
           ("Glikoz + O₂", "Besin üretilir, oksijen açığa çıkar")])
add("10.1.3", "lab", "BİTKİ IŞIKTA NEDEN\nKABARCIK ÇIKARIR?", "Işık şiddeti fotosentez\nhızını etkiler", kind="bubbles",
    title="Fotosentez deneyi (su bitkisi)", colors=[(160, 220, 255), (160, 220, 255), (160, 220, 255)],
    rates=[0.15, 1.0, 0.3],
    steps=[("Hazırlık", "Su bitkisi + su, bir kapta"), ("Işığa yaklaştır", "Kabarcık (O₂) sayısı artar"),
           ("Işığı uzaklaştır", "Kabarcık sayısı azalır")])
add("10.1.4", "riddle", "GÜNEŞSİZ BESİN\nÜRETEN VAR MI?", "Işıksız ortamlarda\nbile yaşam var", answer="KEMOSENTEZ",
    clues=["Güneş ışığı olmadan besin üretirim.", "Enerjiyi inorganik maddelerin yükseltgenmesinden alırım.",
           "Bazı bakteriler bunu yapar."])
add("10.1.5", "sorter", "SİNDİRİM SİSTEMİ\nTAMAMLANMIŞ MI?", "Sindirim sistemi\nbasitten karmaşığa",
    bins=["TAMAMLANMAMIŞ\n(tek delik)", "TAMAMLANMIŞ\n(ağız + anüs)"],
    items=[("Hidra", 0), ("İnsan", 1), ("Planarya", 0), ("Yağmur solucanı", 1), ("Deniz anemonu", 0), ("Kuş", 1)])
add("10.1.6", "flow", "YEDİĞİN YEMEK ENERJİYE\nNASIL DÖNÜŞÜR?", "Sindir, emil, taşı,\nenerji elde et",
    steps=[("Ağız", "Besin parçalanır, nişasta sindirimi başlar"), ("Mide", "Protein sindirimi başlar"),
           ("İnce bağırsak", "Sindirim biter, besinler emilir"), ("Kan", "Besinler hücrelere taşınır")])
add("10.1.7", "swipe", "HÜCRESEL SOLUNUM\nHAKKINDA DOĞRU MU?", "Solunum: besinden\nATP elde etme", labels=("DOĞRU", "YANLIŞ"),
    items=[(True, "Hücresel solunumun büyük kısmı mitokondride olur.", "Krebs ve ETS mitokondride gerçekleşir."),
           (False, "Sadece hayvanlar hücresel solunum yapar.", "Bitkiler de hücresel solunum yapar."),
           (True, "Oksijenli solunumda CO₂ ve H₂O açığa çıkar.", "Glikoz oksijenle yıkılır."),
           (False, "Glikoliz oksijen gerektirir.", "Glikoliz sitoplazmada, oksijensiz gerçekleşir.")])
add("10.1.8", "versus", "HANGİ BESİN\nDAHA ÇOK ENERJİ VERİR?", "Hedef hep aynı:\nATP", sides=("KARBOHİDRAT", "YAĞ"),
    rows=[("1 g ≈ 4 kcal", "1 g ≈ 9 kcal"), ("Hızlı enerji kaynağı", "Uzun süreli enerji deposu"),
          ("Önce kullanılır", "Karbohidrat azalınca kullanılır")])
add("10.1.9", "lab", "MAYA BALONU\nNASIL ŞİŞİRİR?", "Oksijensiz de\nenerji elde edilir", kind="balloon",
    title="Fermantasyon deneyi", colors=[(255, 230, 160), (250, 214, 120), (245, 205, 100)], balloon=[0.05, 0.4, 1.0],
    steps=[("Karışım", "Ilık su + şeker + maya"), ("Balon", "Şişenin ağzına balon tak"),
           ("Sonuç", "Fermantasyonla CO₂ çıkar, balon şişer")])
add("10.1.10", "riddle", "HÜCRENİN ENERJİ\nPARASI NE?", "ATP: hücrenin\nenerji parası", answer="ATP",
    clues=["Adenin, riboz ve üç fosfattan oluşurum.", "Yüksek enerjili fosfat bağlarım var.",
           "Enerji verince ADP’ye dönüşürüm."])
add("10.2.1", "diagram", "EKOSİSTEMİ KİMLER\nOLUŞTURUR?", "Canlı ve cansız\nbileşenler birlikte çalışır",
    center="EKOSİSTEM",
    parts=[("Üretici", "Bitki, alg: besin üretir"), ("Tüketici", "Hayvanlar: hazır besin tüketir"),
           ("Ayrıştırıcı", "Mantar, bakteri: atıkları parçalar"), ("Cansız", "Su, ışık, toprak, sıcaklık")])
add("10.2.2", "flip", "TÜRLER ARASI İLİŞKİLERİ\nBİLİYOR MUSUN?", "Doğada her ilişkinin\nbir sonucu var", labels=("İLİŞKİ", "SONUÇ"),
    cards=[("Mutualizm", "İki tür de yararlanır (+/+)"), ("Parazitlik", "Parazit yararlanır, konak zarar görür"),
           ("Kommensalizm", "Biri yararlanır, diğeri etkilenmez"), ("Rekabet", "İki tür de zarar görür (−/−)")])
add("10.2.3", "bars", "NEDEN ASLAN SAYISI\nOTÇULLARDAN AZ?", "Enerji basamak\nbasamak azalır",
    title="Besin zincirinde enerji (örnek, kJ)", note="Her basamakta enerjinin yaklaşık %90’ı kaybolur",
    bars=[("Üretici", 1000), ("1. tüketici", 100), ("2. tüketici", 10)], hi=0,
    punch="Üst basamağa az enerji ulaşır")
add("10.2.4", "cycle", "KARBON ATOMU\nNEREDEN NEREYE?", "Madde döner,\nenerji akar", center="KARBON\nDÖNGÜSÜ",
    loop="karbon\ndöngüsü\nsürer",
    nodes=[("Atmosfer\nCO₂", "CO₂ havada bulunur"), ("Fotosentez", "Bitki CO₂’yi alır, besin yapar"),
           ("Besin\nzinciri", "Karbon hayvanlara geçer"), ("Solunum\n+ ayrışma", "CO₂ atmosfere geri döner")])
add("10.2.5", "rank", "SÜRDÜRÜLEBİLİRLİK\nİÇİN 3 KURAL", "Küçük adımlar,\nbüyük fark",
    items=[("Geri dönüştür", "Atığı yeniden hammaddeye çevir"), ("Yeniden kullan", "Ürünün ömrünü uzat"),
           ("Azalt", "En iyisi baştan az tüketmek")])
add("10.2.6", "swipe", "DOĞAYA ZARARLI MI,\nDOSTU MU?", "Seçimlerimiz\ngeleceği belirler", labels=("DOĞA DOSTU", "ZARARLI"),
    items=[(False, "Tek kullanımlık plastik", "Yüzyıllarca doğada kalabilir."),
           (True, "Ağaç dikmek", "Karbon tutar, yaşam alanı oluşturur."),
           (False, "Aşırı avlanma", "Türlerin nesli tükenebilir."),
           (True, "Toplu taşıma", "Karbon salımını azaltır.")])
add("10.2.7", "quiz", "EKOLOJİK AYAK İZİNİ\nNASIL KÜÇÜLTÜRSÜN?", "Ayak izin,\ngeleceğin izi",
    q="Hangisi ekolojik ayak izini küçültür?",
    opts=["Tek kullanımlık poşet kullanmak", "Gereksiz ışıkları açık bırakmak", "Toplu taşımayı tercih etmek",
          "Musluğu açık bırakmak"], ok=2, expl="Daha az enerji ve kaynak tüketimi = daha küçük ayak izi.")
add("10.2.8", "diagram", "TÜRLERİ KORUMANIN\n4 YOLU", "Koruma hepimizin\nsorumluluğu", center="KORUMA",
    parts=[("Milli parklar", "Yaşam alanları korunur"), ("Gen bankaları", "Tohum ve genetik materyal saklanır"),
           ("Yasalar", "Avcılık ve ticaret sınırlanır"), ("Eğitim", "Bilinç ve katılım artar")])
add("10.2.9", "sorter", "ÇÖPÜ DOĞRU\nKUTUYA AT!", "Ayır, geri dönüştür,\ndünyayı koru",
    bins=["KÂĞIT\n(mavi)", "PLASTİK\n(sarı)", "CAM\n(yeşil)"],
    items=[("Gazete", 0), ("Pet şişe", 1), ("Kavanoz", 2), ("Karton kutu", 0), ("Deterjan şişesi", 1), ("Cam şişe", 2)])

# ----------------------------------------------------------------- 11. sınıf
add("11.1.1", "riddle", "CANLIDA TEPKİ\nOLUŞTURAN NEDİR?", "Uyaran → tepki:\nher canlıda ortak", answer="UYARAN",
    clues=["Çevreden gelen bir değişimdir.", "Canlıda tepki oluşturur.", "Işık, ses, dokunma, sıcaklık olabilir."])
add("11.1.2", "flip", "BİTKİLER NASIL\nKONUŞUR?", "Bitkiler de hormonla\nyönetilir", sub="Cevap: hormonlarla", labels=("HORMON", "GÖREV"),
    cards=[("Oksin", "Hücre uzaması, ışığa yönelme"), ("Giberellin", "Gövde uzaması ve çimlenme"),
           ("Sitokinin", "Hücre bölünmesini uyarır"), ("Etilen", "Meyvelerin olgunlaşması")])
add("11.1.3", "sorter", "UYARAN YÖNLÜ MÜ,\nYÖNSÜZ MÜ?", "Tropizma ve nasti:\nbitkilerin iki tepkisi",
    bins=["TROPİZMA\n(yöne bağlı)", "NASTİ\n(yöne bağlı değil)"],
    items=[("Işığa doğru eğilme", 0), ("Küsmeotu yaprağı kapanır", 1), ("Kökün yerçekimine uzanması", 0),
           ("Çiçeğin gece kapanması", 1), ("Köklerin suya yönelmesi", 0), ("Sinekkapan kapanması", 1)])
add("11.1.4", "lab", "BİTKİ IŞIĞA\nNASIL DÖNER?", "Işık yönü bitkinin\nbüyümesini yönlendirir", kind="plant",
    title="Yönelme deneyi", bend=[0.0, 0.5, 1.0],
    steps=[("Hazırlık", "Fideyi tek yönden ışık alacak şekilde koy"),
           ("Gözlem", "Gün geçtikçe gövde ışığa doğru eğilir"), ("Sonuç", "Fototropizma: ışığa yönelme")])
add("11.1.5", "sorter", "HANGİ DUYU\nHANGİ RESEPTÖR?", "Duyu organları\nçevreyi algılar",
    bins=["KEMORESEPTÖR\n(kimyasal)", "MEKANORESEPTÖR\n(basınç, ses)", "FOTORESEPTÖR\n(ışık)"],
    items=[("Dil: tat tomurcuğu", 0), ("Burun: koku", 0), ("İç kulak: ses", 1), ("Deri: basınç", 1),
           ("Göz: çubuk ve koni", 2), ("Retina", 2)])
add("11.1.6", "versus", "BEYNİ OLMAYAN CANLI\nTEPKİ VERİR Mİ?", "Sinir sistemi\nsadeden karmaşığa", sides=("HİDRA", "İNSAN"),
    rows=[("Ağsı sinir sistemi", "Merkezî + çevresel sinir sistemi"), ("Beyin yok", "Gelişmiş beyin"),
          ("Basit tepkiler", "Karmaşık tepkiler ve öğrenme")])
add("11.1.7", "diagram", "VÜCUDUN KOMUTA\nMERKEZİ NERESİ?", "Beyin, omurilik, sinirler:\nbir ekip", center="SİNİR\nSİSTEMİ",
    parts=[("Beyin", "Merkezî: düşünme ve koordinasyon"), ("Omurilik", "Refleks merkezi, iletim yolu"),
           ("Sinirler", "Çevresel: bilgiyi taşır"), ("Nöron", "Sinir sisteminin yapı birimi")])
add("11.1.8", "flow", "ELİN SICAĞA DEĞİNCE\nNEDEN HEMEN ÇEKİLİR?", "Refleks: hızlı\nve istem dışı",
    steps=[("Reseptör", "Sıcağı algılar"), ("Duyu nöronu", "Bilgiyi omuriliğe taşır"),
           ("Omurilik", "Karar verir: beyin beklenmez"), ("Motor nöron", "Kas kasılır, elini çekersin")])
add("11.1.9", "myth", "KASLAR KEMİĞİ\nİTER Mİ?", "Hareket bir\ntakım işi",
    items=[("Kaslar kemikleri iter.", "Kaslar sadece kasılır, kemiği çeker."),
           ("Kas tek başına hareket sağlar.", "Kas, kemik ve eklem birlikte çalışır."),
           ("Biseps kasılırken triseps de kasılır.", "Biseps kasılırken triseps gevşer.")])
add("11.1.10", "cycle", "KAS KASILIRKEN\nİÇERİDE NE OLUR?", "ATP olmadan kas\ngevşeyemez", center="KAS\nKASILMASI",
    loop="döngü\ntekrarlanır",
    nodes=[("Kalsiyum\ngelir", "Miyozinin bağlanması mümkün olur"), ("Bağlanma", "Miyozin başları aktine tutunur"),
           ("Kayma", "Aktin kayar, kas kısalır"), ("ATP", "Bağ çözülür, kas gevşer")])
add("11.1.11", "versus", "AŞI BAĞIŞIKLIĞI\nNASIL EĞİTİR?", "Bağışıklık: vücudun\nsavunma ordusu",
    sides=("DOĞAL\nBAĞIŞIKLIK", "KAZANILMIŞ\nBAĞIŞIKLIK"),
    rows=[("Doğuştan vardır", "Hastalık ya da aşıyla kazanılır"),
          ("Her mikroba karşı genel savunma", "Belirli mikroba özgü savunma"),
          ("Deri, mide asidi, fagositler", "Antikor ve hafıza hücreleri")])
add("11.1.12", "myth", "ALERJİ BULAŞICI MI?", "Alerji: bağışıklığın\nyanlış alarmı",
    items=[("Alerji bulaşıcıdır.", "Alerji bulaşmaz; bağışıklığın aşırı tepkisidir."),
           ("Alerjenler zararlı mikroplardır.", "Çoğu alerjen zararsızdır: polen, toz gibi."),
           ("Alerjide histamin salınmaz.", "Histamin salınır: kaşıntı, akıntı, şişlik.")])
add("11.2.1", "stats", "İÇ DENGEN\nNE KADAR HASSAS?", "Homeostazi:\niç denge",
    items=[dict(val=37, suf=" °C", label="İç vücut sıcaklığı (yaklaşık)"),
           dict(val=7.4, dec=1, label="Kan pH’ı (7,35–7,45 aralığında tutulur)"),
           dict(static="70–100", label="Açlık kan şekeri (mg/dL)")])
add("11.2.2", "quiz", "SICAKTA TERLEMEK\nNEDEN GEREKLİ?", "Dengeyi korumak için\nçalışan vücut",
    q="Sıcak havada terlemenin amacı nedir?",
    opts=["Vücut sıcaklığını dengede tutmak", "Vücudu ısıtmak", "Kan basıncını artırmak", "Su kaybını artırmak"], ok=0,
    expl="Terin buharlaşması vücudu soğutur: negatif geri bildirim.")
add("11.2.3", "versus", "TERMOSTAT MI,\nZİNCİR REAKSİYON MU?", "Çoğu denge\nnegatif geri bildirimle sağlanır",
    sides=("NEGATİF\nGERİ BİLDİRİM", "POZİTİF\nGERİ BİLDİRİM"),
    rows=[("Değişimi azaltır, dengeyi korur", "Değişimi artırır, uca götürür"),
          ("Örnek: kan şekeri, vücut ısısı", "Örnek: doğumda oksitosin, pıhtılaşma"),
          ("Çoğu homeostatik süreç", "Nadir ve kısa süreli")])
add("11.2.4", "chat", "VÜCUDUN TERMOSTATI\nKİM?", "Sinir sistemi iç\ndengeyi korur",
    msgs=[("L", "Sıcak havada vücut sıcaklığımı kim ayarlıyor?"), ("R", "Hipotalamus: beynin termostatı."),
          ("L", "Peki nasıl ayarlıyor?"), ("R", "Ter bezlerini ve damarları harekete geçirip vücudu soğutur.")])
add("11.2.5", "diagram", "HORMONLAR\nKİMİN EMRİNDE?", "Hormonlar iç dengeyi\nayarlar", center="ENDOKRİN",
    parts=[("Hipofiz", "Yönetici bez: diğer bezleri uyarır"), ("Pankreas", "İnsülin ve glukagon: kan şekeri"),
           ("Tiroit", "Metabolizma hızını ayarlar"), ("Böbreküstü", "Adrenalin: stres tepkisi")])
add("11.2.6", "cycle", "KALBİN HİÇ DURMAYAN\nYOLCULUĞU", "Dolaşım: iç dengenin\ntaşıyıcısı", center="KAN\nDOLAŞIMI",
    loop="dolaşım\nsürer",
    nodes=[("Kalp", "Kanı pompalar"), ("Atardamar", "Kanı organlara götürür"),
           ("Kılcal\ndamar", "Madde alışverişi burada olur"), ("Toplardamar", "Kanı kalbe döndürür")])
add("11.2.7", "bars", "KOŞARKEN NEDEN\nNEFES NEFESE KALIRSIN?", "Solunum kan pH’ını\ndengede tutar",
    title="Dakikadaki solunum sayısı (yaklaşık)", note="Örnek veri · yaklaşık değerler",
    bars=[("Dinlenme", 15), ("Yürüyüş", 22), ("Koşu", 40), ("Sprint", 55)], hi=3,
    punch="CO₂ artar → solunum hızlanır")
add("11.2.8", "flow", "BÖBREKLER KANI\nNASIL TEMİZLER?", "Nefron: iç dengenin\nfiltresi",
    steps=[("Süzülme", "Kan, glomerulusta süzülür"), ("Geri emilim", "Yararlı maddeler kana döner"),
           ("Salgılama", "Zararlı maddeler tübüle geçer"), ("İdrar", "Atıklar vücuttan atılır")])
add("11.2.9", "cycle", "KOŞARKEN TÜM SİSTEMLER\nBİRLİKTE ÇALIŞIR!", "Sistemler eş güdümlü\nçalışır", center="EŞ\nGÜDÜM",
    loop="denge\nsağlanır",
    nodes=[("Kas\nçalışır", "ATP harcanır, ısı ve CO₂ artar"), ("Solunum\nhızlanır", "Daha çok O₂ alınır"),
           ("Kalp\nhızlanır", "Kan hızla taşınır"), ("Terleme\n+ böbrek", "Isı ve su dengesi korunur")])
add("11.2.10", "quiz", "İNSÜLİN YETMEZSE\nNE OLUR?", "Denge bozulursa\nsağlık bozulur",
    q="İnsülin yetersizliğinde hangi sağlık sorunu görülür?",
    opts=["Anemi", "Diyabet (şeker hastalığı)", "Astım", "Alerji"], ok=1,
    expl="Kan şekeri dengelenemez: homeostazi bozulur.")

assert len(R) == 55, len(R)
