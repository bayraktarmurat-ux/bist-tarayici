import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import requests
import os
import warnings
warnings.filterwarnings("ignore")

TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

PORTFOY      = 950000
RISK_YUZDESI = 1.0
ATR_PERIYOT  = 14
ATR_KATSAYI  = 1.5
RR_KATSAYI   = 3.0
EMA_TOLERANS = 2.0
STOK_ESIK    = 20

HISSELER = [
    "ACSEL","ADEL","ADESE","AGESA","AGHOL","AGROT","AGYO","AHGAZ","AKBNK",
    "AKCNS","AKFGY","AKFYE","AKGRT","AKSA","AKSEN","AKSGY","AKSUE","ALARK",
    "ALBRK","ALCAR","ALCTL","ALFAS","ALGYO","ALKA","ALKIM","ALKLC","ALTNY",
    "ALVES","ANELE","ANGEN","ANHYT","ANSGR","ARASE","ARCLK","ARDYZ","ARENA",
    "ARSAN","ARTMS","ARZUM","ASELS","ASGYO","ASTOR","ASUZU","ATAGY","ATAKP",
    "ATATP","ATEKS","ATLAS","ATSYH","AVGYO","AVHOL","AVOD","AVPGY","AVTUR",
    "AYCES","AYDEM","AYEN","AYES","AYGAZ","AZTEK","BAGFS","BAKAB","BALAT",
    "BANVT","BARMA","BASCM","BASGZ","BAYRK","BERA","BEYAZ","BFREN","BIMAS",
    "BIOEN","BMSCH","BMSTL","BNTAS","BOBET","BORLS","BORSK","BOSSA","BRISA",
    "BRKO","BRKSN","BRKVY","BRLSM","BRMEN","BRSAN","BRYAT","BSOKE","BTCIM",
    "BUCIM","BURCE","BURVA","BVSAN","BYDNR","CANTE","CASA","CEMAS","CEMTS",
    "CEOEM","CIMSA","CLEBI","CMBTN","CMENT","CONSE","COSMO","CRDFA","CRFSA",
    "CUSAN","CVKMD","CWENE","DAGI","DAPGM","DARDL","DCTTR","DENGE","DERHL",
    "DESA","DESPC","DEVA","DGATE","DGGYO","DGNMO","DITAS","DMSAS","DNISI",
    "DOAS","DOCO","DOFER","DOGUB","DOHOL","DOKTA","DURDO","DYOBY","DZGYO",
    "ECILC","ECZYT","EDATA","EDIP","EGEGY","EGGUB","EGPRO","EGSER","EKGYO",
    "EKIZ","EKOS","EKSUN","ELITE","EMKEL","EMNIS","ENERY","ENJSA","ENKAI",
    "ENSRI","ENTRA","EPLAS","ERBOS","ERCB","ESCAR","ESCOM","ESEN","ETILR",
    "ETYAT","EUHOL","EUPWR","EUREN","EUYO","FADE","FENER","FLAP","FMIZP",
    "FONET","FORMT","FORTE","FROTO","FZLGY","GARAN","GARFA","GEDIK","GEDZA",
    "GENIL","GENTS","GEREL","GESAN","GIPTA","GLBMD","GLCVY","GLDTR","GLRYH",
    "GLYHO","GMTAS","GOKNR","GOLTS","GOODY","GOZDE","GRSEL","GSDDE","GSDHO",
    "GSRAY","GUBRF","GWIND","GZNMI","HALKB","HATEK","HDFGS","HEDEF","HEKTS",
    "HKTM","HLGYO","HOROZ","HRKET","HTTBT","HUBVC","HUNER","HURGZ","ICBCT",
    "ICUGS","IDGYO","IEYHO","IHAAS","IHEVA","IHGZT","IHLAS","IHLGM","IHYAY",
    "IMASM","INDES","INFO","INGRM","INTEM","INVEO","INVES","ISATR","ISBIR",
    "ISCTR","ISDMR","ISFIN","ISGSY","ISGYO","ISYAT","IZENR","IZFAS","IZINV",
    "IZMDC","JANTS","KAPLM","KAREL","KARSN","KARTN","KATMR","KAYSE","KCAER",
    "KCHOL","KERVN","KFEIN","KGYO","KIMMR","KLGYO","KLKIM","KLMSN","KLNMA",
    "KLRHO","KLSYN","KMPUR","KNFRT","KOCMT","KONKA","KONTR","KONYA","KOPOL",
    "KORDS","KOTON","KRDMA","KRDMB","KRDMD","KRPLS","KRSTL","KRTEK","KRVGD",
    "KSTUR","KTLEV","KUTPO","KUVVA","KUYAS","KZBGY","KZGYO","LIDER","LIDFA",
    "LILAK","LKMNH","LMKDC","LOGO","LRSHO","MAALT","MACKO","MAGEN","MAKIM",
    "MAKTK","MANAS","MARBL","MARKA","MARTI","MEDTR","MEGAP","MEGMT","MEKAG",
    "MERCN","MERIT","MERKO","METRO","MGROS","MHRGY","MIATK","MNDRS","MNDTR",
    "MOBTL","MOGAN","MPARK","MRGYO","MRSHL","MSGYO","MTRKS","NATEN","NETAS",
    "NIBAS","NTHOL","NUGYO","NUHCM","OBAMS","OBASE","ODAS","ODINE","OFSYM",
    "ONCSM","ONRYT","ORCAY","ORGE","ORMA","OSMEN","OSTIM","OTKAR","OTTO",
    "OYAKC","OYAYO","OYLUM","OYYAT","OZGYO","OZKGY","OZRDN","OZSUB","PAGYO",
    "PAMEL","PAPIL","PARSN","PASEU","PATEK","PCILT","PEKGY","PENGD","PENTA",
    "PETKM","PETUN","PGSUS","PINSU","PKART","PKENT","PLTUR","PNLSN","POLTK",
    "PRDGS","PRZMA","PSDTC","PSGYO","QUAGR","RALYH","RAYSG","RCRAFT","REEDER",
    "RGYAS","RNPOL","RODRG","ROYAL","RTALB","RUBNS","RYGYO","RYSAS","SAFKR",
    "SAHOL","SAMAT","SANEL","SANFM","SANKO","SARKY","SASA","SAYAS","SDTTR",
    "SEGMN","SEKFK","SEKUR","SELEC","SELGD","SELVA","SEYKM","SILVR","SISE",
    "SKBNK","SKTAS","SMART","SMRTG","SNGYO","SNKRN","SODSN","SOKM","SONME",
    "SRVGY","SUMAS","SUNTK","SURGY","SUWEN","TABGD","TACTR","TALGO","TATGD",
    "TAVHL","TBORG","TCELL","TDGYO","TEKTU","TEZOL","TGSAS","THYAO","TKFEN",
    "TKNSA","TLMAN","TMPOL","TMSN","TNZTP","TOASO","TPVIO","TRGYO","TRILC",
    "TSGYO","TSKB","TSPOR","TTKOM","TTRAK","TUCLK","TUKAS","TUPRS","TURGG",
    "TURSG","UFUK","ULAS","ULKER","ULUFA","ULUSE","ULUUN","UMPAS","UNLU",
    "UNTRD","USAK","USDTR","UTPYA","UZERB","VAKBN","VAKFN","VAKKO","VANGD",
    "VBTYZ","VERTU","VERUS","VESBE","VKFYO","VKGYO","VRGYO","WINTL","WNKMD",
    "YATAS","YAYLA","YGYO","YIGIT","YKBNK","YKSLN","YMSTU","YNBIO","YONGA",
    "YOYVO","YTKYO","YUKSEL","YYAPI","ZEDUR","ZRGYO","ZYFGY",
]

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
        # MultiIndex düzelt
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df[["Open","High","Low","Close","Volume"]].copy()
        # Sütunlar hala DataFrame ise Series'e çevir
        for col in ["Open","High","Low","Close","Volume"]:
            if isinstance(df[col], pd.DataFrame):
                df[col] = df[col].iloc[:, 0]
        df = df.dropna()
        if len(df) < 60:
            return None
        return df
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

def telegram_gonder(mesaj):
    url  = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=data, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print("Telegram hatasi:", e)
        return False

def main():
    print("Tarama basliyor:", datetime.now().strftime("%Y-%m-%d %H:%M"))
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
    tarih = datetime.now().strftime("%d.%m.%Y")

    if len(sinyaller) == 0:
        mesaj  = "<b>📈 BIST Sinyal Tarayici</b>\n"
        mesaj += "<b>" + tarih + "</b>\n\n"
        mesaj += "Bugun sinyal bulunamadi."
        telegram_gonder(mesaj)
        print("Sinyal yok.")
        return

    baslik  = "<b>📈 BIST Sinyal Tarayici — " + tarih + "</b>\n"
    baslik += "<b>" + str(len(sinyaller)) + " sinyal bulundu</b>\n"
    baslik += "Portfoy: " + str(PORTFOY) + " TL | Risk: %" + str(RISK_YUZDESI) + "\n"
    baslik += "━━━━━━━━━━━━━━━━━━━━"
    telegram_gonder(baslik)

    for s in sinyaller:
        mesaj  = "<b>" + s["hisse"] + "</b> | " + s["destek"] + "\n"
        mesaj += "Fiyat: <b>" + str(s["kapanis"]) + "</b> TL\n"
        mesaj += "Stop: " + str(s["stop"]) + " | Hedef: " + str(s["hedef"]) + "\n"
        mesaj += "Lot: " + str(s["lot"]) + " | Giris: " + str(s["giris_tl"]) + " TL\n"
        mesaj += "Risk: " + str(s["risk_tl"]) + " TL | %K: " + str(s["k"])
        telegram_gonder(mesaj)
        print("Sinyal:", s["hisse"])

    print("Tamamlandi. Toplam sinyal:", len(sinyaller))

if __name__ == "__main__":
    main()
