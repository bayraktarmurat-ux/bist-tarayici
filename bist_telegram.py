import pandas as pd
import yfinance as yf
from datetime import datetime
import requests
import os
import warnings
warnings.filterwarnings("ignore")

# ─── TELEGRAM ─────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ─── STRATEJİ PARAMETRELERİ ───────────────────────────────────────────────────
PORTFOY        = 950_000
RISK_YUZDESI   = 1.0
ATR_PERIYOT    = 14
ATR_KATSAYI    = 1.5
RR_KATSAYI     = 3.0
ENDEKS_SEMBOL  = "XU100.IS"
MACD_HIZLI     = 12
MACD_YAVAS     = 26
MACD_SINYAL    = 9

# ─── EN BASARILI 50 HİSSE ─────────────────────────────────────────────────────
TOP50 = {
    "POLTK","BMSTL","LIDER","AVTUR","MOBTL","ISCTR","DOAS","TRCAS","CMBTN","ISBTR",
    "LUKSK","DOHOL","DOCO","VBTYZ","MERIT","TEHOL","VAKKO","ALGYO","FRIGO","BMSCH",
    "HEDEF","ETILR","ASELS","ESCOM","AKSA","ULUUN","GRTHO","OYAKC","FMIZP","RYSAS",
    "KARSN","SMRVA","BRYAT","YAPRK","NETAS","SELEC","SAFKR","CELHA","ECILC","BURCE",
    "GLCVY","EGEEN","ACSEL","KUYAS","RYGYO","INDES","MAGEN","AKSEN","ARCLK","YYAPI",
}

# ─── HİSSE LİSTESİ ────────────────────────────────────────────────────────────
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

# ─── YARDIMCI FONKSİYONLAR ────────────────────────────────────────────────────
def squeeze(s):
    if hasattr(s, "squeeze"):
        return s.squeeze()
    return s

def ema(seri, periyot):
    return squeeze(seri).ewm(span=periyot, adjust=False).mean()

def atr_hesapla(df, periyot=14):
    c  = squeeze(df["Close"])
    h  = squeeze(df["High"])
    l  = squeeze(df["Low"])
    hl = h - l
    hc = (h - c.shift(1)).abs()
    lc = (l - c.shift(1)).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return tr.ewm(span=periyot, adjust=False).mean()

def stokastik_hesapla(df, k=5, d=3, smooth=3):
    c     = squeeze(df["Close"])
    h     = squeeze(df["High"])
    l     = squeeze(df["Low"])
    ll    = l.rolling(k).min()
    hh    = h.rolling(k).max()
    k_raw = 100 * (c - ll) / (hh - ll + 1e-9)
    k_sm  = k_raw.rolling(smooth).mean()
    d_sm  = k_sm.rolling(d).mean()
    return k_sm, d_sm

def veri_cek(ticker, gun=300):
    try:
        df = yf.download(ticker + ".IS", period=str(gun) + "d",
                         interval="1d", progress=False, auto_adjust=True)
        if df is None or df.empty or len(df) < 60:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df[["Open","High","Low","Close","Volume"]].copy()
        for col in df.columns:
            df[col] = squeeze(df[col])
        df = df.dropna()
        if len(df) < 60:
            return None
        return df
    except Exception:
        return None

# ─── ENDEKS FİLTRESİ ──────────────────────────────────────────────────────────
def endeks_kontrol():
    try:
        df = yf.download(ENDEKS_SEMBOL, period="300d",
                         interval="1d", progress=False, auto_adjust=True)
        if df.empty:
            return None, None, None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df["EMA200"] = squeeze(df["Close"]).ewm(span=200, adjust=False).mean()
        df.dropna(subset=["EMA200"], inplace=True)
        son    = df.iloc[-1]
        kap    = float(son["Close"])
        e200   = float(son["EMA200"])
        fark   = (kap - e200) / e200 * 100
        return kap > e200, round(kap, 0), round(fark, 1)
    except Exception:
        return None, None, None

# ─── SİNYAL TARAMA (MACD STRATEJİSİ) ────────────────────────────────────────
def sinyal_tara(df):
    """
    Strateji: Trend (EMA20>50>100>200) + MACD histogram negatiften pozitife donus
    """
    df = df.copy()
    close = squeeze(df["Close"])
    df["EMA20"]  = ema(close, 20)
    df["EMA50"]  = ema(close, 50)
    df["EMA100"] = ema(close, 100)
    df["EMA200"] = ema(close, 200)
    df["ATR"]    = atr_hesapla(df, ATR_PERIYOT)

    # MACD
    ema_h          = close.ewm(span=MACD_HIZLI,  adjust=False).mean()
    ema_y          = close.ewm(span=MACD_YAVAS,  adjust=False).mean()
    df["MACD"]     = ema_h - ema_y
    df["MACD_SIG"] = df["MACD"].ewm(span=MACD_SINYAL, adjust=False).mean()
    df["MACD_HIS"] = df["MACD"] - df["MACD_SIG"]

    son  = df.iloc[-1]
    once = df.iloc[-2]

    # 1. Trend filtresi
    if not (float(son["EMA20"]) > float(son["EMA50"]) >
            float(son["EMA100"]) > float(son["EMA200"])):
        return None

    # 2. MACD histogram: negatiften pozitife dondü
    if not (float(once["MACD_HIS"]) < 0 and
            float(son["MACD_HIS"])   > 0):
        return None

    kapanis = float(son["Close"])
    atr_val = float(son["ATR"])
    stop    = round(kapanis - ATR_KATSAYI * atr_val, 2)
    hedef   = round(kapanis + (kapanis - stop) * RR_KATSAYI, 2)
    stop_p  = round((kapanis - stop) / kapanis * 100, 1)
    hedef_p = round((hedef - kapanis) / kapanis * 100, 1)

    return {
        "kapanis" : round(kapanis, 2),
        "macd_his": round(float(son["MACD_HIS"]), 4),
        "macd"    : round(float(son["MACD"]), 4),
        "stop"    : stop,
        "stop_p"  : stop_p,
        "hedef"   : hedef,
        "hedef_p" : hedef_p,
    }

# ─── TELEGRAM ─────────────────────────────────────────────────────────────────
def telegram_gonder(mesaj):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram token/chat_id eksik!")
        return False
    url  = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=data, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print("Telegram hatasi:", e)
        return False

# ─── ANA FONKSİYON ────────────────────────────────────────────────────────────
def main():
    print("Tarama basliyor:", datetime.now().strftime("%Y-%m-%d %H:%M"))
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M")

    # Endeks kontrolu
    endeks_ok, xu100, xu_fark = endeks_kontrol()

    if endeks_ok is False:
        mesaj  = "<b>BIST Sinyal Tarayici - " + tarih + "</b>\n\n"
        mesaj += "BIST100 EMA200 altinda!\n"
        mesaj += "XU100: " + str(xu100) + " TL"
        if xu_fark is not None:
            mesaj += " (" + str(xu_fark) + "%)"
        mesaj += "\n\nStrateji bugun pasif, islem onerilmez."
        telegram_gonder(mesaj)
        print("Endeks pasif, islem yok.")
        return

    endeks_durum = ""
    if xu100 and xu_fark is not None:
        endeks_durum = "XU100: " + str(xu100) + " (" + ("+" if xu_fark >= 0 else "") + str(xu_fark) + "%)"

    # Hisse tarama
    risk_tl   = PORTFOY * RISK_YUZDESI / 100
    sinyaller = []

    for hisse in HISSELER:
        df = veri_cek(hisse)
        if df is None:
            continue
        try:
            sonuc = sinyal_tara(df)
        except Exception as e:
            print("Hata -", hisse, ":", e)
            continue
        if sonuc is None:
            continue

        risk_hisse = sonuc["kapanis"] - sonuc["stop"]
        if risk_hisse <= 0:
            continue
        lot      = max(1, int(risk_tl / risk_hisse))
        giris_tl = round(lot * sonuc["kapanis"], 0)
        top50    = hisse in TOP50

        sinyaller.append({
            "hisse"   : hisse,
            "top50"   : top50,
            "kapanis" : sonuc["kapanis"],
            "macd_his": sonuc["macd_his"],
            "macd"    : sonuc["macd"],
            "stop"    : sonuc["stop"],
            "stop_p"  : sonuc["stop_p"],
            "hedef"   : sonuc["hedef"],
            "hedef_p" : sonuc["hedef_p"],
            "lot"     : lot,
            "giris_tl": giris_tl,
            "risk_tl" : round(risk_tl, 0),
        })

    # Top50 once, sonra MACD_HIS buyukten kucuge sirala
    sinyaller.sort(key=lambda x: (not x["top50"], -x["macd_his"]))

    top50_count = sum(1 for s in sinyaller if s["top50"])

    # Sonuc yok
    if not sinyaller:
        mesaj  = "<b>BIST Sinyal Tarayici - " + tarih + "</b>\n"
        if endeks_durum:
            mesaj += endeks_durum + "\n"
        mesaj += "\nBugun sinyal bulunamadi."
        telegram_gonder(mesaj)
        print("Sinyal yok.")
        return

    # Baslik mesaji
    baslik  = "<b>BIST MACD Sinyal Tarayici - " + tarih + "</b>\n"
    if endeks_durum:
        baslik += endeks_durum + "\n"
    baslik += str(len(sinyaller)) + " sinyal"
    if top50_count > 0:
        baslik += " | " + str(top50_count) + " adet TOP50"
    baslik += "\nPortfoy: " + str(PORTFOY) + " TL | Risk: %" + str(RISK_YUZDESI) + " | R:R 1:" + str(RR_KATSAYI)
    baslik += "\n" + "─" * 22
    telegram_gonder(baslik)

    # Her sinyal icin mesaj
    for s in sinyaller:
        star  = " STAR " if s["top50"] else ""
        mesaj  = "<b>" + star + s["hisse"] + star + "</b>\n"
        mesaj += "Fiyat: <b>" + str(s["kapanis"]) + " TL</b>\n"
        mesaj += "MACD His: " + str(s["macd_his"]) + " (+ dondu)\n"
        mesaj += "Stop:  " + str(s["stop"]) + " (-%" + str(s["stop_p"]) + ")\n"
        mesaj += "Hedef: " + str(s["hedef"]) + " (+%" + str(s["hedef_p"]) + ")\n"
        mesaj += "R:R  : 1:" + str(RR_KATSAYI) + "\n"
        mesaj += "Lot:   " + str(s["lot"]) + " adet | " + str(int(s["giris_tl"])) + " TL\n"
        mesaj += "Risk:  " + str(int(s["risk_tl"])) + " TL"
        telegram_gonder(mesaj)
        print("Sinyal gonderildi:", s["hisse"], "| TOP50:" if s["top50"] else "")

    print("Tamamlandi. Toplam sinyal:", len(sinyaller))

if __name__ == "__main__":
    main()
