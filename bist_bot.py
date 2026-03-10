import os
import threading
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime
from flask import Flask, request, jsonify
import warnings
warnings.filterwarnings("ignore")

TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

PORTFOY      = 950000
RISK_YUZDESI = 1.0
ATR_PERIYOT  = 14
ATR_KATSAYI  = 1.5
RR_KATSAYI   = 2.5
EMA_TOLERANS = 2.0
STOK_ESIK    = 20

HISSELER = [
    "ACSEL","ADEL","ADESE","ADGYO","AFYON","AGHOL","AGESA","AGROT","AHSGY","AHGAZ",
    "AKYHO","AKENR","AKFGY","AKFIS","AKFYE","AKHAN","ATEKS","AKSGY","AKMGY","AKSA",
    "AKSEN","AKGRT","AKSUE","ALCAR","ALGYO","ALARK","ALBRK","ALCTL","ALFAS","ALKIM",
    "ALKA","AYCES","ALTNY","ALKLC","ALVES","ANSGR","AEFES","ANHYT","ASUZU","ANGEN",
    "ANELE","ARCLK","ARDYZ","ARENA","ARFYE","ARMGD","ARSAN","ARTMS","ARZUM","ASGYO",
    "ASELS","ASTOR","ATAGY","ATATR","ATAKP","AGYO","ATSYH","ATLAS","ATATP","AVOD",
    "AVGYO","AVTUR","AVHOL","AVPGY","AYDEM","AYEN","AYES","AYGAZ","AZTEK","A1CAP",
    "A1YEN","BAGFS","BAHKM","BAKAB","BALAT","BALSU","BNTAS","BANVT","BARMA","BASGZ",
    "BASCM","BEGYO","BTCIM","BSOKE","BYDNR","BAYRK","BERA","BRKSN","BESLR","BESTE",
    "BJKAS","BEYAZ","BIENY","BIGTK","BLCYT","BIMAS","BINBN","BIOEN","BRKVY","BRKO",
    "BIGEN","BRLSM","BRMEN","BIZIM","BLUME","BMSTL","BMSCH","BOBET","BORSK","BORLS",
    "BRSAN","BRYAT","BFREN","BOSSA","BRISA","BULGS","BURCE","BURVA","BUCIM","BVSAN",
    "BIGCH","CRFSA","CASA","CEMZY","CEOEM","CCOLA","CONSE","COSMO","CRDFA","CVKMD",
    "CWENE","CGCAM","CANTE","CATES","CLEBI","CELHA","CEMAS","CEMTS","CMBTN","CMENT",
    "CIMSA","CUSAN","DAGI","DAPGM","DARDL","DGATE","DCTTR","DMSAS","DENGE","DZGYO",
    "DERIM","DERHL","DESA","DESPC","DSTKF","DEVA","DNISI","DIRIT","DITAS","DMRGD",
    "DOCO","DOFRB","DOFER","DOHOL","DGNMO","ARASE","DOGUB","DGGYO","DOAS","DOKTA",
    "DURDO","DURKN","DUNYH","DYOBY","EBEBK","ECOGR","ECZYT","EDATA","EDIP","EFOR",
    "EGEEN","EGGUB","EGPRO","EGSER","EPLAS","EGEGY","ECILC","EKIZ","EKOS","EKSUN",
    "ELITE","EMKEL","EMNIS","EKGYO","EMPAE","ENDAE","ENJSA","ENERY","ENKAI","ENSRI",
    "ERBOS","ERCB","EREGL","KIMMR","ERSU","ESCAR","ESCOM","ESEN","ETILR","EUKYO",
    "EUYO","ETYAT","EUHOL","TEZOL","EUREN","EUPWR","EYGYO","FADE","FMIZP","FENER",
    "FLAP","FONET","FROTO","FORMT","FRMPL","FORTE","FRIGO","FZLGY","GWIND","GSRAY",
    "GARFA","GRNYO","GATEG","GEDIK","GEDZA","GLCVY","GENIL","GENTS","GENKM","GEREL",
    "GZNMI","GIPTA","GMTAS","GESAN","GLBMD","GLYHO","GOODY","GOKNR","GOLTS","GOZDE",
    "GRTHO","GSDDE","GSDHO","GUBRF","GLRYH","GLRMK","GUNDG","GRSEL","SAHOL","HLGYO",
    "HRKET","HATEK","HATSN","HDFGS","HEDEF","HEKTS","HKTM","HTTBT","HOROZ","HUBVC",
    "HUNER","HURGZ","ENTRA","ICBCT","ICUGS","INGRM","INVEO","INVES","ISKPL","IEYHO",
    "IDGYO","IHEVA","IHLGM","IHGZT","IHAAS","IHLAS","IHYAY","IMASM","INDES","INFO",
    "INTEK","INTEM","ISDMR","ISFIN","ISGYO","ISGSY","ISMEN","ISYAT","ISBIR","ISSEN",
    "IZINV","IZENR","IZMDC","IZFAS","JANTS","KFEIN","KLKIM","KLSER","KLYPV","KAPLM",
    "KRDMA","KRDMB","KRDMD","KAREL","KARSN","KRTEK","KARTN","KTLEV","KATMR","KAYSE",
    "KENT","KRVGD","KERVN","TCKRC","KZBGY","KLGYO","KLRHO","KMPUR","KLMSN","KCAER",
    "KCHOL","KOCMT","KLSYN","KNFRT","KONTR","KONYA","KONKA","KGYO","KORDS","KRPLS",
    "KOTON","KOPOL","KRGYO","KRSTL","KRONT","KSTUR","KUVVA","KUYAS","KBORU","KZGYO",
    "KUTPO","KTSKR","LIDER","LIDFA","LILAK","LMKDC","LINK","LOGO","LKMNH","LRSHO",
    "LUKSK","LYDHO","LYDYE","MACKO","MAKIM","MAKTK","MANAS","MAGEN","MARKA","MARMR",
    "MAALT","MRSHL","MRGYO","MARTI","MTRKS","MAVI","MZHLD","MEDTR","MEGMT","MEGAP",
    "MEKAG","MNDRS","MEPET","MERCN","MERIT","MERKO","METRO","MTRYO","MEYSU","MHRGY",
    "MIATK","MGROS","MSGYO","MPARK","MMCAS","MOBTL","MOGAN","MNDTR","MOPAS","EGEPO",
    "NATEN","NTGAZ","NTHOL","NETAS","NETCD","NIBAS","NUHCM","NUGYO","OBAMS","OBASE",
    "ODAS","ODINE","OFSYM","ONCSM","ONRYT","ORCAY","ORGE","ORMA","OSMEN","OSTIM",
    "OTKAR","OTTO","OYAKC","OYYAT","OYAYO","OYLUM","OZKGY","OZATD","OZGYO","OZRDN",
    "OZSUB","OZYSR","PAMEL","PNLSN","PAGYO","PAPIL","PRDGS","PRKME","PARSN","PASEU",
    "PSGYO","PAHOL","PATEK","PCILT","PGSUS","PEKGY","PENGD","PENTA","PSDTC","PETKM",
    "PKENT","PETUN","PINSU","PNSUT","PKART","PLTUR","POLHO","POLTK","PRZMA","RNPOL",
    "RALYH","RAYSG","REEDR","RYGYO","RYSAS","RODRG","ROYAL","RGYAS","RTALB","RUBNS",
    "RUZYE","SAFKR","SANEL","SNICA","SANFM","SANKO","SAMAT","SARKY","SASA","SVGYO",
    "SAYAS","SDTTR","SEGMN","SEKUR","SELEC","SELVA","SERNT","SRVGY","SEYKM","SILVR",
    "SNGYO","SKYLP","SMRTG","SMART","SODSN","SOKE","SKTAS","SONME","SNPAM","SUMAS",
    "SUNTK","SURGY","SUWEN","SMRVA","SEKFK","SEGYO","SKYMD","SKBNK","SOKM","TABGD",
    "TATGD","TATEN","TAVHL","TEKTU","TKFEN","TKNSA","TMPOL","TRHOL","TERA","TEHOL",
    "TGSAS","TOASO","TRGYO","TRMET","TRENJ","TLMAN","TSPOR","TDGYO","TSGYO","TUCLK",
    "TUKAS","TRCAS","TUREX","MARBL","TRILC","TCELL","TMSN","TUPRS","TRALT","THYAO",
    "PRKAB","TTKOM","TTRAK","TBORG","TURGG","GARAN","HALKB","ISATR","ISBTR","ISCTR",
    "ISKUR","KLNMA","TSKB","TURSG","SISE","VAKBN","UFUK","ULAS","ULUFA","ULUSE",
    "ULUUN","UMPAS","USAK","UCAYM","ULKER","UNLU","VAKFA","VAKFN","VKGYO","VKFYO",
    "VAKKO","VANGD","VBTYZ","VRGYO","VERUS","VERTU","VESBE","VESTL","VKING","VSNMD",
    "YKBNK","YAPRK","YATAS","YYLGD","YAYLA","YGGYO","YEOTK","YGYO","YYAPI","YESIL",
    "YBTAS","YIGIT","YONGA","YKSLN","YUNSA","ZGYO","ZEDUR","ZERGY","ZRGYO","ZOREN",
    "BINHO",
]

app = Flask(__name__)
tarama_devam = False

def telegram_gonder(chat_id, mesaj):
    url  = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
    data = {"chat_id": chat_id, "text": mesaj, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("Telegram hatasi:", e)

def ema(seri, periyot):
    return seri.ewm(span=periyot, adjust=False).mean()

def atr_hesapla(df, periyot=14):
    hl = df["High"] - df["Low"]
    hc = (df["High"] - df["Close"].shift(1)).abs()
    lc = (df["Low"]  - df["Close"].shift(1)).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return tr.ewm(span=periyot, adjust=False).mean()

def stokastik_hesapla(df, k=5, d=3, smooth=3):
    ll    = df["Low"].rolling(k).min()
    hh    = df["High"].rolling(k).max()
    k_raw = 100 * (df["Close"] - ll) / (hh - ll + 1e-9)
    k_sm  = k_raw.rolling(smooth).mean()
    d_sm  = k_sm.rolling(d).mean()
    return k_sm, d_sm

def veri_cek(ticker, gun=300):
    try:
        df = yf.download(
            ticker + ".IS", period=str(gun) + "d",
            interval="1d", progress=False, auto_adjust=True
        )
        if df is None or df.empty or len(df) < 60:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df[["Open","High","Low","Close","Volume"]].copy()
        for col in ["Open","High","Low","Close","Volume"]:
            if isinstance(df[col], pd.DataFrame):
                df[col] = df[col].iloc[:, 0]
        df = df.dropna()
        return df if len(df) >= 60 else None
    except Exception:
        return None

def sinyal_tara(df):
    tolerans = EMA_TOLERANS / 100
    df = df.copy()
    close = df["Close"].squeeze()
    df["EMA20"]  = ema(close, 20)
    df["EMA50"]  = ema(close, 50)
    df["EMA100"] = ema(close, 100)
    df["EMA200"] = ema(close, 200)
    df["ATR"]    = atr_hesapla(df, ATR_PERIYOT)
    df["K"], df["D"] = stokastik_hesapla(df)

    son   = df.iloc[-1]
    once  = df.iloc[-2]
    kapanis = float(son["Close"])

    if not (son["EMA20"] > son["EMA50"] > son["EMA100"] > son["EMA200"]):
        return None
    if not (float(once["K"]) < float(once["D"]) and
            float(son["K"])  > float(son["D"])  and
            float(son["K"])  < STOK_ESIK):
        return None

    ema_destek = None
    for col in ["EMA20","EMA50","EMA100","EMA200"]:
        ema_val = float(son[col])
        if abs(kapanis - ema_val) / ema_val <= tolerans:
            ema_destek = col
            break
    if ema_destek is None:
        return None

    atr_val = float(son["ATR"])
    stop    = round(kapanis - ATR_KATSAYI * atr_val, 2)
    hedef   = round(kapanis + RR_KATSAYI * ATR_KATSAYI * atr_val, 2)
    return {
        "kapanis":    round(kapanis, 2),
        "ema_destek": ema_destek,
        "k":          round(float(son["K"]), 2),
        "stop":       stop,
        "hedef":      hedef,
    }

def tarama_yap(chat_id):
    global tarama_devam
    tarama_devam = True
    risk_tl   = PORTFOY * RISK_YUZDESI / 100
    sinyaller = []
    tarih     = datetime.now().strftime("%d.%m.%Y %H:%M")

    telegram_gonder(chat_id, "🔍 Tarama basliyor... (~3-4 dakika)")

    for hisse in HISSELER:
        df = veri_cek(hisse)
        if df is None:
            continue
        try:
            sonuc = sinyal_tara(df)
        except Exception:
            continue
        if sonuc is None:
            continue

        risk_hisse = sonuc["kapanis"] - sonuc["stop"]
        if risk_hisse <= 0:
            continue
        lot      = int(risk_tl / risk_hisse)
        giris_tl = round(lot * sonuc["kapanis"], 2)

        sinyaller.append({
            "hisse":    hisse,
            "kapanis":  sonuc["kapanis"],
            "destek":   sonuc["ema_destek"],
            "k":        sonuc["k"],
            "stop":     sonuc["stop"],
            "hedef":    sonuc["hedef"],
            "lot":      lot,
            "giris_tl": giris_tl,
            "risk_tl":  round(risk_tl, 2),
        })

    sinyaller.sort(key=lambda x: x["k"])

    if len(sinyaller) == 0:
        telegram_gonder(chat_id,
            "<b>📈 BIST Sinyal Tarayici — " + tarih + "</b>\n\nBugun sinyal bulunamadi.")
        tarama_devam = False
        return

    baslik  = "<b>📈 BIST Sinyal Tarayici — " + tarih + "</b>\n"
    baslik += "<b>" + str(len(sinyaller)) + " sinyal bulundu</b>\n"
    baslik += "Portfoy: " + str(PORTFOY) + " TL | Risk: %" + str(RISK_YUZDESI) + "\n"
    baslik += "━━━━━━━━━━━━━━━━━━━━"
    telegram_gonder(chat_id, baslik)

    for s in sinyaller:
        tv_link = "https://tr.tradingview.com/chart/?symbol=BIST:" + s["hisse"]
        mesaj  = "<b>" + s["hisse"] + "</b> | " + s["destek"] + "\n"
        mesaj += "Fiyat: <b>" + str(s["kapanis"]) + "</b> TL\n"
        mesaj += "Stop: " + str(s["stop"]) + " | Hedef: " + str(s["hedef"]) + "\n"
        mesaj += "Lot: " + str(s["lot"]) + " | Giris: " + str(s["giris_tl"]) + " TL\n"
        mesaj += "Risk: " + str(s["risk_tl"]) + " TL | %K: " + str(s["k"]) + "\n"
        mesaj += "<a href='" + tv_link + "'>📊 Grafik</a>"
        telegram_gonder(chat_id, mesaj)

    tarama_devam = False

@app.route("/webhook", methods=["POST"])
def webhook():
    global tarama_devam
    data = request.json
    if not data:
        return jsonify({"ok": True})

    message  = data.get("message", {})
    text     = message.get("text", "").strip().lower()
    chat_id  = str(message.get("chat", {}).get("id", ""))

    if text == "/tara":
        if tarama_devam:
            telegram_gonder(chat_id, "⏳ Tarama zaten devam ediyor, lutfen bekleyin.")
        else:
            t = threading.Thread(target=tarama_yap, args=(chat_id,), daemon=True)
            t.start()
    elif text == "/start":
        telegram_gonder(chat_id,
            "<b>BIST Sinyal Tarayici Bot</b>\n\n"
            "/tara — Anlik tarama baslat\n"
            "/yardim — Komutlar")
    elif text == "/yardim":
        telegram_gonder(chat_id,
            "<b>Komutlar:</b>\n"
            "/tara — Tum hisseleri tara, sinyalleri gonder\n"
            "/yardim — Bu mesaji goster")

    return jsonify({"ok": True})

@app.route("/", methods=["GET"])
def index():
    return "BIST Bot aktif!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
