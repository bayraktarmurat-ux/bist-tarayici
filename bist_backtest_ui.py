import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, date
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── HİSSE LİSTELERİ ──────────────────────────────────────────────────────────
TOP50 = {
    "POLTK","BMSTL","LIDER","AVTUR","MOBTL","ISCTR","DOAS","TRCAS","CMBTN","ISBTR",
    "LUKSK","DOHOL","DOCO","VBTYZ","MERIT","TEHOL","VAKKO","ALGYO","FRIGO","BMSCH",
    "HEDEF","ETILR","ASELS","ESCOM","AKSA","ULUUN","GRTHO","OYAKC","FMIZP","RYSAS",
    "KARSN","SMRVA","BRYAT","YAPRK","NETAS","SELEC","SAFKR","CELHA","ECILC","BURCE",
    "GLCVY","EGEEN","ACSEL","KUYAS","RYGYO","INDES","MAGEN","AKSEN","ARCLK","YYAPI",
}

BIST_HISSELER = [
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

st.set_page_config(
    page_title="BIST Backtest",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #1e2433;
        border: 1px solid #2d3548;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
    }
    .metric-label { font-size: 12px; color: #8b95a8; margin-bottom: 4px; }
    .metric-value { font-size: 24px; font-weight: 700; }
    .metric-pos { color: #22c55e; }
    .metric-neg { color: #ef4444; }
    .metric-neu { color: #94a3b8; }
    .islem-row { padding: 6px 0; border-bottom: 1px solid #1e2433; font-size: 13px; }
    .badge { padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 600; }
    .badge-hedef { background: #14532d; color: #22c55e; }
    .badge-stop  { background: #450a0a; color: #ef4444; }
    .badge-acik  { background: #1e3a5f; color: #60a5fa; }
    section[data-testid="stSidebar"] { background: #0f1117; }
</style>
""", unsafe_allow_html=True)

# ─── YARDIMCI FONKSİYONLAR ────────────────────────────────────────────────────
def squeeze(s):
    if hasattr(s, "squeeze"):
        return s.squeeze()
    return s

def ema(seri, periyot):
    return squeeze(seri).ewm(span=periyot, adjust=False).mean()

def atr_hesapla(df, periyot=14):
    c = squeeze(df["Close"])
    h = squeeze(df["High"])
    l = squeeze(df["Low"])
    hl = h - l
    hc = (h - c.shift(1)).abs()
    lc = (l - c.shift(1)).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return tr.ewm(span=periyot, adjust=False).mean()

def stokastik_hesapla(df, k=5, d=3, smooth=3):
    c = squeeze(df["Close"])
    h = squeeze(df["High"])
    l = squeeze(df["Low"])
    ll    = l.rolling(k).min()
    hh    = h.rolling(k).max()
    k_raw = 100 * (c - ll) / (hh - ll + 1e-9)
    k_sm  = k_raw.rolling(smooth).mean()
    d_sm  = k_sm.rolling(d).mean()
    return k_sm, d_sm

def veri_cek(ticker, bas, bit):
    try:
        df = yf.download(ticker + ".IS",
                         start=str(bas),
                         end=str(bit),
                         interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 50:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df[["Open","High","Low","Close","Volume"]].dropna()
        for col in df.columns:
            df[col] = squeeze(df[col])
        df.index = df.index.tz_localize(None)
        return df
    except Exception:
        return None

def endeks_filtre_olustur(bas, bit):
    try:
        df = yf.download("XU100.IS",
                         start=(bas - pd.DateOffset(years=1)).strftime("%Y-%m-%d"),
                         end=bit.strftime("%Y-%m-%d"),
                         interval="1d", progress=False, auto_adjust=True)
        if df.empty:
            return {}
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.index = df.index.tz_localize(None)
        df["EMA200"] = squeeze(df["Close"]).ewm(span=200, adjust=False).mean()
        df.dropna(subset=["EMA200"], inplace=True)
        return {row.Index.date(): float(row.Close) > float(row.EMA200)
                for row in df.itertuples()}
    except Exception:
        return {}

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
st.sidebar.title("⚙️ Backtest Ayarları")

st.sidebar.markdown("### 📌 Hisse")
tum_hisseler = st.sidebar.checkbox("Tüm Hisseleri Tara", value=False)

if tum_hisseler:
    st.sidebar.info("Tüm BIST hisseleri taranacak.\nSonuçlar getiriye göre sıralanır.")
    hisse_input = "ALL"
else:
    hisse_input = st.sidebar.text_input(
        "Hisse Kodu (örn: THYAO, POLTK)",
        value="THYAO",
        placeholder="BIST hisse kodu girin"
    ).upper().strip()

st.sidebar.markdown("### 📅 Tarih Aralığı")
col1, col2 = st.sidebar.columns(2)
bas_tarih = col1.date_input("Başlangıç", value=date(2020, 1, 1),
                             min_value=date(2010, 1, 1), max_value=date.today())
bit_tarih = col2.date_input("Bitiş", value=date.today(),
                             min_value=date(2010, 1, 1), max_value=date.today())

st.sidebar.markdown("### 💰 Sermaye & Risk")
portfoy    = st.sidebar.number_input("Portföy (TL)", min_value=10000,
                                      max_value=100_000_000, value=1_000_000, step=10000)
risk_yuzde = st.sidebar.slider("Risk % (işlem başına)", 0.5, 5.0, 1.0, 0.5)

st.sidebar.markdown("### 📐 R:R & Stop")
rr_kat  = st.sidebar.select_slider("R:R Katsayısı",
           options=[1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0], value=3.0)
atr_kat = st.sidebar.slider("ATR Katsayısı (Stop)", 0.5, 3.0, 1.5, 0.5)
atr_per = st.sidebar.slider("ATR Periyodu", 7, 21, 14, 1)

st.sidebar.markdown("### 📉 Stokastik")
stok_esik = st.sidebar.slider("Stokastik Eşik", 10, 40, 20, 5)

st.sidebar.markdown("### 🔍 Filtreler")
endeks_aktif = st.sidebar.checkbox("Endeks Filtresi (BIST100 > EMA200)", value=True)

# ─── BAŞLIK ───────────────────────────────────────────────────────────────────
st.title("📊 BIST Backtest")
if tum_hisseler:
    st.caption(f"Mod: Tüm Hisseler | Strateji: EMA Dokunuşu + Stokastik | R:R 1:{rr_kat:.0f} | Stop ATR×{atr_kat}")
else:
    st.caption(f"Mod: Tekil Hisse | Strateji: EMA Dokunuşu + Stokastik | R:R 1:{rr_kat:.0f} | Stop ATR×{atr_kat}")

# ─── BACKTEST BUTONU ──────────────────────────────────────────────────────────
if st.button("🚀 Backtest Çalıştır", use_container_width=True, type="primary"):
    if not hisse_input:
        st.error("Lütfen bir hisse kodu girin.")
        st.stop()

    bas_ts  = pd.Timestamp(bas_tarih)
    bit_ts  = pd.Timestamp(bit_tarih)
    veri_bas = bas_ts - pd.DateOffset(years=1)
    veri_bit = bit_ts + pd.DateOffset(days=2)

    # Endeks filtresi (her iki mod için de hazırla)
    endeks_f = {}
    if endeks_aktif:
        with st.spinner("Endeks verisi indiriliyor..."):
            endeks_f = endeks_filtre_olustur(bas_ts, veri_bit)

    # ── ÇOKLU HİSSE MODU ──────────────────────────────────────────────────────
    if tum_hisseler:
        ozet_listesi = []
        progress = st.progress(0, text="Tarama başlıyor...")
        toplam_h = len(BIST_HISSELER)

        for hi, sembol in enumerate(BIST_HISSELER):
            progress.progress((hi + 1) / toplam_h,
                               text=f"Taraniyor: {sembol} ({hi+1}/{toplam_h})")
            df_raw = veri_cek(sembol, veri_bas.to_pydatetime().date(),
                              veri_bit.to_pydatetime().date())
            if df_raw is None:
                continue
            try:
                df = df_raw.copy()
                df["EMA20"]  = ema(df["Close"], 20)
                df["EMA50"]  = ema(df["Close"], 50)
                df["EMA100"] = ema(df["Close"], 100)
                df["EMA200"] = ema(df["Close"], 200)
                df["ATR"]    = atr_hesapla(df, atr_per)
                df["K"], df["D"] = stokastik_hesapla(df)
                df.dropna(subset=["EMA200","K","D","ATR"], inplace=True)
                if len(df) < 10:
                    continue

                portfoy_s = portfoy
                islemler  = []
                for i in range(1, len(df)):
                    son    = df.iloc[i]
                    onceki = df.iloc[i - 1]
                    if son.name < bas_ts or son.name > bit_ts:
                        continue
                    if endeks_aktif and not endeks_f.get(son.name.date(), True):
                        continue
                    if not (float(son["EMA20"]) > float(son["EMA50"]) >
                            float(son["EMA100"]) > float(son["EMA200"])):
                        continue
                    if not (float(onceki["K"]) < float(onceki["D"]) and
                            float(son["K"]) > float(son["D"]) and
                            float(son["K"]) < stok_esik):
                        continue
                    low_v  = float(son["Low"])
                    high_v = float(son["High"])
                    ema_destek = None
                    for col_n in ["EMA20","EMA50","EMA100","EMA200"]:
                        ev = float(son[col_n])
                        if low_v <= ev <= high_v:
                            ema_destek = col_n
                            break
                    if ema_destek is None:
                        continue
                    giris  = float(son["Close"])
                    atr_v  = float(son["ATR"])
                    stop   = giris - atr_v * atr_kat
                    hedef  = giris + (giris - stop) * rr_kat
                    stop_m = giris - stop
                    if stop_m <= 0:
                        continue
                    lot  = max(1, int(portfoy_s * (risk_yuzde / 100) / stop_m))
                    sonuc = "acik"; cikis = None; kaz = 0.0
                    for j in range(i + 1, min(i + 60, len(df))):
                        if float(df.iloc[j]["Low"]) <= stop:
                            sonuc = "stop";  cikis = stop;  kaz = (stop  - giris) * lot; break
                        if float(df.iloc[j]["High"]) >= hedef:
                            sonuc = "hedef"; cikis = hedef; kaz = (hedef - giris) * lot; break
                    if cikis is None:
                        cikis = float(df.iloc[min(i + 59, len(df) - 1)]["Close"])
                        kaz   = (cikis - giris) * lot
                    portfoy_s += kaz
                    islemler.append({"sonuc": sonuc, "kaz": kaz})

                if not islemler:
                    continue
                df_i    = pd.DataFrame(islemler)
                tamam   = df_i[df_i["sonuc"] != "acik"]
                kazanan = df_i[df_i["sonuc"] == "hedef"]
                kaybeden= df_i[df_i["sonuc"] == "stop"]
                t       = len(tamam)
                if t == 0:
                    continue
                ort_k = kazanan["kaz"].mean() if len(kazanan) > 0 else 0
                ort_z = kaybeden["kaz"].mean() if len(kaybeden) > 0 else 0
                kf    = abs(ort_k / ort_z) if ort_z != 0 else float("inf")
                ozet_listesi.append({
                    "Hisse"      : sembol,
                    "★"          : "★" if sembol in TOP50 else "",
                    "İşlem"      : t,
                    "Kazanan"    : len(kazanan),
                    "Kaybeden"   : len(kaybeden),
                    "Win Rate%"  : round(len(kazanan) / t * 100, 1),
                    "Getiri%"    : round((portfoy_s - portfoy) / portfoy * 100, 1),
                    "K/Z (TL)"   : round(df_i["kaz"].sum(), 0),
                    "Kar Faktörü": round(kf, 2) if kf < 999 else float("inf"),
                })
            except Exception:
                continue

        progress.empty()
        st.session_state["mod"]          = "coklu"
        st.session_state["ozet_listesi"] = ozet_listesi
        st.session_state["portfoy"]      = portfoy

    # ── TEKİL HİSSE MODU ──────────────────────────────────────────────────────
    else:
        if not hisse_input:
            st.error("Lütfen bir hisse kodu girin.")
            st.stop()

        with st.spinner(f"{hisse_input} verisi indiriliyor..."):
            df_raw = veri_cek(hisse_input,
                              veri_bas.to_pydatetime().date(),
                              veri_bit.to_pydatetime().date())

        if df_raw is None:
            st.error(f"❌ {hisse_input}.IS için veri alınamadı. Hisse kodunu kontrol edin.")
            st.stop()

        with st.spinner("İndikatörler hesaplanıyor..."):
            df = df_raw.copy()
            df["EMA20"]  = ema(df["Close"], 20)
            df["EMA50"]  = ema(df["Close"], 50)
            df["EMA100"] = ema(df["Close"], 100)
            df["EMA200"] = ema(df["Close"], 200)
            df["ATR"]    = atr_hesapla(df, atr_per)
            df["K"], df["D"] = stokastik_hesapla(df)
            df.dropna(subset=["EMA200","K","D","ATR"], inplace=True)

        with st.spinner("Sinyaller taranıyor..."):
            islemler  = []
            portfoy_s = portfoy

        for i in range(1, len(df)):
            son    = df.iloc[i]
            onceki = df.iloc[i - 1]

            if son.name < bas_ts or son.name > bit_ts:
                continue
            if endeks_aktif and not endeks_f.get(son.name.date(), True):
                continue

            # Trend
            if not (float(son["EMA20"]) > float(son["EMA50"]) >
                    float(son["EMA100"]) > float(son["EMA200"])):
                continue

            # Stokastik
            if not (float(onceki["K"]) < float(onceki["D"]) and
                    float(son["K"])    > float(son["D"])    and
                    float(son["K"])    < stok_esik):
                continue

            # EMA dokunuşu
            low_v  = float(son["Low"])
            high_v = float(son["High"])
            ema_destek = None
            for col, label in [("EMA20","EMA20"),("EMA50","EMA50"),
                                ("EMA100","EMA100"),("EMA200","EMA200")]:
                ev = float(son[col])
                if low_v <= ev <= high_v:
                    ema_destek = label
                    break
            if ema_destek is None:
                continue

            giris  = float(son["Close"])
            atr_v  = float(son["ATR"])
            stop   = giris - atr_v * atr_kat
            hedef  = giris + (giris - stop) * rr_kat
            stop_m = giris - stop
            if stop_m <= 0:
                continue

            lot  = max(1, int(portfoy_s * (risk_yuzde / 100) / stop_m))
            sonuc = "acik"
            cikis = None
            kaz   = 0.0

            for j in range(i + 1, min(i + 60, len(df))):
                if float(df.iloc[j]["Low"]) <= stop:
                    sonuc = "stop";  cikis = stop;  kaz = (stop  - giris) * lot; break
                if float(df.iloc[j]["High"]) >= hedef:
                    sonuc = "hedef"; cikis = hedef; kaz = (hedef - giris) * lot; break
            if cikis is None:
                cikis = float(df.iloc[min(i + 59, len(df) - 1)]["Close"])
                kaz   = (cikis - giris) * lot

            portfoy_s += kaz
            islemler.append({
                "Tarih"    : son.name,
                "Giris"    : round(giris, 2),
                "Stop"     : round(stop,  2),
                "Hedef"    : round(hedef, 2),
                "Cikis"    : round(cikis, 2),
                "Sonuc"    : sonuc,
                "KZ_TL"    : round(kaz, 0),
                "Portfoy"  : round(portfoy_s, 0),
                "EMA"      : ema_destek,
                "K"        : round(float(son["K"]), 1),
                "Lot"      : lot,
            })

        st.session_state["mod"]       = "tekil"
        st.session_state["islemler"]  = islemler
        st.session_state["portfoy_s"] = portfoy_s
        st.session_state["df"]        = df
        st.session_state["hisse"]     = hisse_input
        st.session_state["portfoy"]   = portfoy
        st.session_state["bas_ts"]    = bas_ts
        st.session_state["bit_ts"]    = bit_ts
        st.session_state["rr_kat"]    = rr_kat

# ─── SONUÇLAR — ÇOKLU MOD ─────────────────────────────────────────────────────
if st.session_state.get("mod") == "coklu" and "ozet_listesi" in st.session_state:
    ozet_listesi = st.session_state["ozet_listesi"]
    portfoy0     = st.session_state["portfoy"]

    st.markdown("### Tüm Hisseler Backtest Sonuçları")

    if not ozet_listesi:
        st.warning("Bu dönemde sinyal üreten hisse bulunamadı.")
        st.stop()

    df_oz = pd.DataFrame(ozet_listesi).sort_values("Getiri%", ascending=False)
    poz   = len(df_oz[df_oz["Getiri%"] > 0])
    kf_f  = df_oz[df_oz["Kar Faktörü"] < 999]["Kar Faktörü"]

    c1,c2,c3,c4,c5 = st.columns(5)
    for col, lbl, val, renk in [
        (c1, "Sinyal Hisse",   str(len(df_oz)),                "metric-neu"),
        (c2, "Pozitif Getiri", f"{poz} (%{round(poz/len(df_oz)*100)})", "metric-pos"),
        (c3, "Ort. Getiri",    f"{df_oz['Getiri%'].mean():+.1f}%", "metric-pos" if df_oz['Getiri%'].mean()>=0 else "metric-neg"),
        (c4, "Ort. Win Rate",  f"{df_oz['Win Rate%'].mean():.1f}%", "metric-neu"),
        (c5, "Ort. Kar Fak.",  f"{kf_f.mean():.2f}",           "metric-neu"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{lbl}</div>
            <div class="metric-value {renk}">{val}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # Tablo
    st.dataframe(
        df_oz,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Getiri%"    : st.column_config.NumberColumn("Getiri%",    format="%.1f%%"),
            "Win Rate%"  : st.column_config.NumberColumn("Win Rate%",  format="%.1f%%"),
            "K/Z (TL)"   : st.column_config.NumberColumn("K/Z (TL)",  format="%,.0f"),
            "Kar Faktörü": st.column_config.NumberColumn("Kar Faktörü",format="%.2f"),
        }
    )

    csv = df_oz.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ CSV İndir", data=csv,
        file_name=f"bist_coklu_backtest_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv")

    st.caption("⚠️ Bu analiz yatırım tavsiyesi değildir.")

# ─── SONUÇLAR — TEKİL MOD ─────────────────────────────────────────────────────
elif st.session_state.get("mod") == "tekil" and "islemler" in st.session_state:
    islemler  = st.session_state["islemler"]
    portfoy_s = st.session_state["portfoy_s"]
    df        = st.session_state["df"]
    hisse     = st.session_state["hisse"]
    portfoy0  = st.session_state["portfoy"]
    bas_ts    = st.session_state["bas_ts"]
    bit_ts    = st.session_state["bit_ts"]
    rr_k      = st.session_state["rr_kat"]

    st.markdown(f"### {hisse} Backtest Sonuçları")

    if not islemler:
        st.warning("Bu dönemde kriterlere uyan sinyal bulunamadı.")
        st.stop()

    df_i     = pd.DataFrame(islemler)
    tamam    = df_i[df_i["Sonuc"] != "acik"]
    kazanan  = df_i[df_i["Sonuc"] == "hedef"]
    kaybeden = df_i[df_i["Sonuc"] == "stop"]
    toplam   = len(tamam)
    getiri   = (portfoy_s - portfoy0) / portfoy0 * 100
    win_rate = len(kazanan) / toplam * 100 if toplam > 0 else 0
    ort_k    = kazanan["KZ_TL"].mean() if len(kazanan) > 0 else 0
    ort_z    = kaybeden["KZ_TL"].mean() if len(kaybeden) > 0 else 0
    kar_fak  = abs(ort_k / ort_z) if ort_z != 0 else float("inf")
    toplam_kz= df_i["KZ_TL"].sum()

    # Metrik kartları
    g_renk = "metric-pos" if getiri >= 0 else "metric-neg"
    k_renk = "metric-pos" if toplam_kz >= 0 else "metric-neg"

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    for col, lbl, val, renk in [
        (c1, "Başlangıç",      f"{portfoy0:,.0f} TL",   "metric-neu"),
        (c2, "Bitiş",          f"{portfoy_s:,.0f} TL",  g_renk),
        (c3, "Toplam K/Z",     f"{toplam_kz:+,.0f} TL", k_renk),
        (c4, "Getiri",         f"{getiri:+.1f}%",        g_renk),
        (c5, "Win Rate",       f"{win_rate:.1f}%",       "metric-neu"),
        (c6, "Kar Faktörü",    f"{kar_fak:.2f}" if kar_fak < 999 else "∞", "metric-neu"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{lbl}</div>
            <div class="metric-value {renk}">{val}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    c7,c8,c9 = st.columns(3)
    for col, lbl, val, renk in [
        (c7, "Toplam İşlem",   str(toplam),             "metric-neu"),
        (c8, "Kazanan (Hedef)",f"{len(kazanan)}",        "metric-pos"),
        (c9, "Kaybeden (Stop)",f"{len(kaybeden)}",       "metric-neg"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{lbl}</div>
            <div class="metric-value {renk}">{val}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Portföy eğrisi + fiyat grafiği
    tab1, tab2, tab3 = st.tabs(["📈 Fiyat Grafiği", "💰 Portföy Eğrisi", "📋 İşlem Listesi"])

    with tab1:
        df_grafik = df[(df.index >= bas_ts) & (df.index <= bit_ts)].copy()
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.7, 0.3], vertical_spacing=0.04)

        fig.add_trace(go.Candlestick(
            x=df_grafik.index,
            open=df_grafik["Open"], high=df_grafik["High"],
            low=df_grafik["Low"],   close=df_grafik["Close"],
            name="Fiyat",
            increasing_line_color="#22c55e",
            decreasing_line_color="#ef4444",
        ), row=1, col=1)

        for col_n, renk, gw in [
            ("EMA20","#38bdf8",1), ("EMA50","#f59e0b",1),
            ("EMA100","#a78bfa",2), ("EMA200","#f472b6",2)
        ]:
            fig.add_trace(go.Scatter(
                x=df_grafik.index, y=df_grafik[col_n],
                name=col_n, line=dict(color=renk, width=gw)
            ), row=1, col=1)

        # İşlem noktaları
        for ist in islemler:
            renk  = "#22c55e" if ist["Sonuc"] == "hedef" else "#ef4444" if ist["Sonuc"] == "stop" else "#60a5fa"
            sembol = "triangle-up" if ist["Sonuc"] != "stop" else "triangle-down"
            fig.add_trace(go.Scatter(
                x=[ist["Tarih"]], y=[ist["Giris"] * 0.985],
                mode="markers",
                marker=dict(symbol=sembol, size=10, color=renk),
                name=ist["Sonuc"], showlegend=False,
                hovertext=f"{ist['Sonuc'].upper()} | Giriş:{ist['Giris']} Çıkış:{ist['Cikis']} K/Z:{ist['KZ_TL']:+,.0f}TL",
                hoverinfo="text"
            ), row=1, col=1)

        # Stokastik
        fig.add_trace(go.Scatter(
            x=df_grafik.index, y=df_grafik["K"],
            name="%K", line=dict(color="#38bdf8", width=1.5)
        ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=df_grafik.index, y=df_grafik["D"],
            name="%D", line=dict(color="#f59e0b", width=1.5)
        ), row=2, col=1)
        fig.add_hline(y=stok_esik, line_dash="dot", line_color="#64748b", row=2, col=1)
        fig.add_hline(y=80, line_dash="dot", line_color="#64748b", row=2, col=1)

        fig.update_layout(
            template="plotly_dark", paper_bgcolor="#0d0f14",
            plot_bgcolor="#0d0f14", height=600, showlegend=True,
            xaxis_rangeslider_visible=False,
            margin=dict(l=10, r=10, t=30, b=10),
            font=dict(family="Consolas", size=11),
        )
        fig.update_yaxes(gridcolor="#1e293b")
        fig.update_xaxes(gridcolor="#1e293b")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        portfoy_ser = [portfoy0] + df_i["Portfoy"].tolist()
        tarih_ser   = [bas_ts] + [r["Tarih"] for _, r in df_i.iterrows()]

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=tarih_ser, y=portfoy_ser,
            fill="tonexty", line=dict(color="#38bdf8", width=2),
            name="Portföy"
        ))
        fig2.add_hline(y=portfoy0, line_dash="dash",
                       line_color="#64748b", line_width=1)

        # Renk dolgu
        fig2.add_trace(go.Scatter(
            x=tarih_ser, y=[portfoy0] * len(tarih_ser),
            fill=None, line=dict(color="rgba(0,0,0,0)"),
            showlegend=False
        ))

        fig2.update_layout(
            template="plotly_dark", paper_bgcolor="#0d0f14",
            plot_bgcolor="#0d0f14", height=400,
            margin=dict(l=10, r=10, t=30, b=10),
            yaxis=dict(gridcolor="#1e293b",
                       tickformat=",.0f",
                       ticksuffix=" TL"),
            xaxis=dict(gridcolor="#1e293b"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        df_goster = df_i.copy()
        df_goster["Tarih"] = df_goster["Tarih"].dt.strftime("%d.%m.%Y")
        df_goster["K/Z (TL)"] = df_goster["KZ_TL"].apply(lambda x: f"{x:+,.0f}")
        df_goster["Portföy"]  = df_goster["Portfoy"].apply(lambda x: f"{x:,.0f}")
        df_goster["Sonuç"]    = df_goster["Sonuc"].map(
            {"hedef": "✅ Hedef", "stop": "❌ Stop", "acik": "⏳ Açık"})

        st.dataframe(
            df_goster[["Tarih","Giris","Stop","Hedef","Cikis","Sonuç",
                        "K/Z (TL)","Portföy","EMA","K","Lot"]],
            use_container_width=True,
            hide_index=True
        )

        csv = df_goster.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ CSV İndir", data=csv,
            file_name=f"{hisse}_backtest_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    st.markdown("---")
    st.caption("⚠️ Bu analiz yatırım tavsiyesi değildir.")
