import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ─── SAYFA AYARLARI ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BIST Sinyal Tarayıcı",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── HİSSE LİSTESİ ────────────────────────────────────────────────────────────
HISSELER = [
    "ACSEL","ADEL","ADESE","ADFAS","ADGYO","ADNAC","AFYON","AGESA","AGHOL",
    "AGROT","AGYO","AHGAZ","AKBNK","AKCNS","AKFGY","AKFYE","AKGRT","AKISP",
    "AKKGZ","AKSA","AKSEN","AKSGY","AKSUE","AKTIF","ALARK","ALBRK","ALCAR",
    "ALCTL","ALFAS","ALGYO","ALKA","ALKIM","ALKLC","ALMAD","ALTNY","ALVES",
    "ANELE","ANGEN","ANHYT","ANSGR","ANTGZ","ARASE","ARCLK","ARDYZ","ARENA",
    "ARSAN","ARTMS","ARZUM","ASCEL","ASELS","ASGYO","ASTOR","ASUZU","ATAGY",
    "ATAKP","ATATP","ATEKS","ATLAS","ATSYH","AVGYO","AVHOL","AVOD","AVPGY",
    "AVTUR","AYCES","AYDEM","AYEN","AYES","AYGAZ","AZTEK","BAGFS","BAKAB",
    "BALAT","BANVT","BARMA","BASCM","BASGZ","BAYRK","BERA","BEYAZ","BFREN",
    "BIMAS","BIOEN","BIOTK","BITKN","BKMEZ","BMSCH","BMSTL","BNTAS","BOBET",
    "BORLS","BORSK","BOSSA","BRISA","BRKO","BRKSN","BRKVY","BRLSM","BRMEN",
    "BRSAN","BRYAT","BSOKE","BTCIM","BUCIM","BURCE","BURVA","BVSAN","BYDNR",
    "CANTE","CASA","CEMAS","CEMTS","CEOEM","CIMSA","CLEBI","CLNKL","CMBTN",
    "CMENT","COKAS","CONSE","COSMO","CRDFA","CRFSA","CUSAN","CVKMD","CWENE",
    "DAGI","DAPGM","DARDL","DASTY","DCTTR","DENGE","DERHL","DESA","DESPC",
    "DEVA","DGATE","DGGYO","DGNMO","DITAS","DJIST","DMSAS","DNISI","DOAS",
    "DOBUR","DOCO","DOFER","DOGUB","DOHOL","DOKTA","DURDO","DYOBY","DZGYO",
    "ECILC","ECZYT","EDATA","EDIP","EGEGY","EGGUB","EGPRO","EGSER","EKGYO",
    "EKIZ","EKOS","EKSUN","ELITE","EMKEL","EMNIS","ENERY","ENJSA","ENKAI",
    "ENSRI","ENTRA","EPLAS","ERBOS","ERCB","ERGLI","ESCAR","ESCOM","ESEN",
    "ETILR","ETYAT","EUHOL","EUPWR","EUREN","EUYO","EVYAP","FADE","FENER",
    "FLAP","FMIZP","FONET","FORMT","FORTE","FROTO","FZLGY","GARAN","GARFA",
    "GEDIK","GEDZA","GENIL","GENTS","GEREL","GESAN","GIPTA","GLBMD","GLCVY",
    "GLDTR","GLRYH","GLYHO","GMTAS","GOKNR","GOLTS","GOODY","GOZDE","GRSEL",
    "GRTRK","GSDDE","GSDHO","GSRAY","GUBRF","GWIND","GZNMI","HALKB","HATEK",
    "HDFGS","HEDEF","HEKTS","HKTM","HLGYO","HOROZ","HRKET","HTTBT","HUBVC",
    "HUNER","HURGZ","ICBCT","ICUGS","IDEAS","IDGYO","IDOSA","IEYHO","IHAAS",
    "IHEVA","IHGZT","IHLAS","IHLGM","IHYAY","IMASM","INDES","INFO","INGRM",
    "INTEM","INVEO","INVES","IPEKE","ISATR","ISBIR","ISCTR","ISDMR","ISFIN",
    "ISGSY","ISGYO","ISHOL","ISYAT","ITFAQ","IZENR","IZFAS","IZINV","IZMDC",
    "JANTS","KAPLM","KAREL","KARSN","KARTN","KATMR","KAYSE","KCAER","KCHOL",
    "KCGYO","KERVN","KERVT","KFEIN","KGYO","KIMMR","KLGYO","KLKIM","KLMSN",
    "KLNMA","KLRHO","KLSYN","KMPUR","KNFRT","KOCMT","KONKA","KONTR","KONYA",
    "KOPOL","KORDS","KOTON","KPHOL","KRDMA","KRDMB","KRDMD","KRPLS","KRSTL",
    "KRTEK","KRVGD","KSTUR","KTLEV","KUTPO","KUVVA","KUYAS","KZBGY","KZGYO",
    "LIDER","LIDFA","LILAK","LKMNH","LMKDC","LOGO","LRSHO","LYKHO","MAALT",
    "MACKO","MAGEN","MAKIM","MAKTK","MANAS","MARBL","MARKA","MARTI","MAVKG",
    "MEDTR","MEGAP","MEGMT","MEKAG","MERCN","MERIT","MERKO","METRO","METUR",
    "MGROS","MHRGY","MIATK","MIPAZ","MNDRS","MNDTR","MOBTL","MOGAN","MPARK",
    "MRGYO","MRSHL","MSGYO","MTRKS","MTSN","NATEN","NBVMD","NETAS","NIBAS",
    "NILYT","NKELU","NTHOL","NTTUR","NUGYO","NUHCM","OBAMS","OBASE","ODAS",
    "ODINE","OFSYM","OKANT","ONCSM","ONRYT","ORCAY","ORGE","ORMA","OSMEN",
    "OSTIM","OTKAR","OTTO","OYAKC","OYAYO","OYLUM","OYYAT","OZGYO","OZKGY",
    "OZRDN","OZSUB","PAGYO","PAMEL","PAPIL","PARSN","PASEU","PATEK","PCILT",
    "PEGYO","PEKGY","PENGD","PENTA","PETKM","PETUN","PGSUS","PINSU","PKART",
    "PKENT","PLTUR","PNLSN","POLTK","POLYP","POPSH","PRDGS","PRZMA","PSDTC",
    "PSGYO","PTOFS","QUAGR","RALYH","RAYSG","RCRAFT","REEDER","RGYAS","RNPOL",
    "RODRG","ROYAL","RTALB","RUBNS","RYGYO","RYSAS","SAFKR","SAHOL","SAMAT",
    "SANEL","SANFM","SANKO","SARKY","SASA","SAYAS","SDTTR","SEGMN","SEKFK",
    "SEKUR","SELEC","SELGD","SELVA","SEYKM","SILVR","SISE","SKBNK","SKTAS",
    "SMART","SMRTG","SNGYO","SNKRN","SODSN","SOKM","SONME","SRVGY","SUMAS",
    "SUNTK","SURGY","SUWEN","TABGD","TACTR","TALGO","TATGD","TAVHL","TBORG",
    "TCELL","TDGYO","TEKTU","텍ST","TEZOL","TGSAS","THYAO","TKFEN","TKNSA",
    "TLMAN","TMPOL","TMSN","TNZTP","TOASO","TPVIO","TRGYO","TRILC","TSGYO",
    "TSKB","TSPOR","TTKOM","TTRAK","TUCLK","TUKAS","TUPRS","TURGG","TURSG",
    "UFUK","ULAS","ULKER","ULUFA","ULUSE","ULUUN","UMPAS","UNLU","UNTRD",
    "USAK","USDTR","UTPYA","UZERB","VAKBN","VAKFN","VAKKO","VANGD","VBTYZ",
    "VERTU","VERUS","VESBE","VKFYO","VKGYO","VRGYO","WINTL","WNKMD","YATAS",
    "YAYLA","YGYO","YIGIT","YKBNK","YKSLN","YMSTU","YNBIO","YONGA","YOYVO",
    "YTKYO","YUKSEL","YYAPI","ZEDUR","ZRGYO","ZYFGY",
]
# ─── YARDIMCI FONKSİYONLAR ────────────────────────────────────────────────────
def ema(seri, periyot):
    return seri.ewm(span=periyot, adjust=False).mean()

def atr_hesapla(df, periyot=14):
    hl = df["High"] - df["Low"]
    hc = (df["High"] - df["Close"].shift(1)).abs()
    lc = (df["Low"] - df["Close"].shift(1)).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return tr.ewm(span=periyot, adjust=False).mean()

def stokastik_hesapla(df, k=5, d=3, smooth=3):
    ll = df["Low"].rolling(k).min()
    hh = df["High"].rolling(k).max()
    k_raw = 100 * (df["Close"] - ll) / (hh - ll + 1e-9)
    k_sm  = k_raw.rolling(smooth).mean()
    d_sm  = k_sm.rolling(d).mean()
    return k_sm, d_sm

def veri_cek(ticker, gun=300):
    try:
        df = yf.download(ticker + ".IS", period=f"{gun}d",
                         interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 60:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df[["Open","High","Low","Close","Volume"]].dropna()
        return df
    except Exception:
        return None

def sinyal_tara(df, params):
    tolerans   = params["ema_tolerans"] / 100
    stok_esik  = params["stok_esik"]
    atr_per    = params["atr_periyot"]
    atr_kat    = params["atr_katsayi"]
    rr         = params["rr_katsayi"]

    df = df.copy()
    df["EMA20"]  = ema(df["Close"], 20)
    df["EMA50"]  = ema(df["Close"], 50)
    df["EMA100"] = ema(df["Close"], 100)
    df["EMA200"] = ema(df["Close"], 200)
    df["ATR"]    = atr_hesapla(df, atr_per)
    df["K"], df["D"] = stokastik_hesapla(df)

    son  = df.iloc[-1]
    once = df.iloc[-2]
    kapanis = float(son["Close"])

    # EMA sırası kontrolü
    if not (son["EMA20"] > son["EMA50"] > son["EMA100"] > son["EMA200"]):
        return None

    # Stokastik kesişim
    if not (float(once["K"]) < float(once["D"]) and
            float(son["K"]) > float(son["D"]) and
            float(son["K"]) < stok_esik):
        return None

    # EMA destek kontrolü
    ema_destek = None
    for col in ["EMA20","EMA50","EMA100","EMA200"]:
        ema_val = float(son[col])
        if abs(kapanis - ema_val) / ema_val <= tolerans:
            ema_destek = col
            break
    if ema_destek is None:
        return None

    atr_val = float(son["ATR"])
    stop    = round(kapanis - atr_kat * atr_val, 2)
    hedef   = round(kapanis + rr * atr_kat * atr_val, 2)

    return {
        "Son Kapanis": round(kapanis, 2),
        "EMA Destek":  ema_destek,
        "K":           round(float(son["K"]), 2),
        "D":           round(float(son["D"]), 2),
        "Stop":        stop,
        "Hedef":       hedef,
        "ATR":         round(atr_val, 2),
    }
# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
st.sidebar.title("⚙️ Ayarlar")

portfoy = st.sidebar.number_input(
    "Portföy (TL)", min_value=10000, max_value=10000000,
    value=950000, step=10000
)
risk_yuzde = st.sidebar.slider(
    "Risk %", min_value=0.5, max_value=5.0, value=1.0, step=0.5
)
rr_katsayi = st.sidebar.slider(
    "R:R Katsayısı", min_value=1.0, max_value=5.0, value=3.0, step=0.5
)
atr_katsayi = st.sidebar.slider(
    "ATR Katsayısı", min_value=0.5, max_value=3.0, value=1.5, step=0.5
)
atr_periyot = st.sidebar.slider(
    "ATR Periyodu", min_value=7, max_value=21, value=14, step=1
)
ema_tolerans = st.sidebar.slider(
    "EMA Tolerans %", min_value=0.5, max_value=5.0, value=2.0, step=0.5
)
stok_esik = st.sidebar.slider(
    "Stokastik Eşik", min_value=10, max_value=40, value=20, step=5
)

params = {
    "ema_tolerans": ema_tolerans,
    "stok_esik":    stok_esik,
    "atr_periyot":  atr_periyot,
    "atr_katsayi":  atr_katsayi,
    "rr_katsayi":   rr_katsayi,
}

# ─── ANA SAYFA ────────────────────────────────────────────────────────────────
st.title("📈 BIST Sinyal Tarayıcı")
st.caption("EMA20>50>100>200 + Stokastik Kesişim + EMA Destek")

if st.button("🔍 Tara", use_container_width=True, type="primary"):
    risk_tl = portfoy * risk_yuzde / 100
    sinyaller = []
    hatalar   = []

    progress = st.progress(0, text="Tarama başlıyor...")
    toplam = len(HISSELER)

    for i, hisse in enumerate(HISSELER):
        progress.progress((i + 1) / toplam,
                          text=f"Taraniyor: {hisse} ({i+1}/{toplam})")
        df = veri_cek(hisse)
        if df is None:
            hatalar.append(hisse)
            continue
        sonuc = sinyal_tara(df, params)
        if sonuc is None:
            continue

        kapanis = sonuc["Son Kapanis"]
        stop    = sonuc["Stop"]
        risk_hisse = kapanis - stop
        if risk_hisse <= 0:
            continue
        lot        = int(risk_tl / risk_hisse)
        giris_tl   = round(lot * kapanis, 2)

        sinyaller.append({
            "Hisse":       hisse,
            "Kapanis":     kapanis,
            "EMA Destek":  sonuc["EMA Destek"],
            "%K":          sonuc["K"],
            "%D":          sonuc["D"],
            "Stop":        stop,
            "Hedef":       sonuc["Hedef"],
            "ATR":         sonuc["ATR"],
            "Lot":         lot,
            "Giris TL":    giris_tl,
            "Risk TL":     round(risk_tl, 2),
        })

    progress.empty()
    st.session_state["sinyaller"] = sinyaller
    st.session_state["hatalar"]   = hatalar
    st.session_state["tarih"]     = datetime.now().strftime("%d.%m.%Y %H:%M")
# ─── SONUÇLAR ─────────────────────────────────────────────────────────────────
if "sinyaller" in st.session_state:
    sinyaller = st.session_state["sinyaller"]
    tarih     = st.session_state["tarih"]
    hatalar   = st.session_state.get("hatalar", [])

    st.markdown(f"### Tarama Sonuçları — {tarih}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Sinyal Sayısı",  len(sinyaller))
    col2.metric("Taranan Hisse",  len(HISSELER))
    col3.metric("Veri Hatası",    len(hatalar))

    if len(sinyaller) == 0:
        st.warning("Bugün sinyal bulunamadı.")
    else:
        df_sonuc = pd.DataFrame(sinyaller).sort_values("%K")
        st.dataframe(df_sonuc, use_container_width=True, hide_index=True)

        # CSV indir
        csv = df_sonuc.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="⬇️ CSV İndir",
            data=csv,
            file_name="bist_sinyaller_" + datetime.now().strftime("%Y%m%d_%H%M") + ".csv",
            mime="text/csv",
        )

        st.markdown("---")
        st.markdown("### 📊 Grafik")

        secili = st.selectbox(
            "Hisse seçin:", [r["Hisse"] for r in sinyaller]
        )

        df_grafik = veri_cek(secili, gun=150)
        if df_grafik is not None:
            df_grafik["EMA20"]  = ema(df_grafik["Close"], 20)
            df_grafik["EMA50"]  = ema(df_grafik["Close"], 50)
            df_grafik["EMA100"] = ema(df_grafik["Close"], 100)
            df_grafik["EMA200"] = ema(df_grafik["Close"], 200)
            df_grafik["K"], df_grafik["D"] = stokastik_hesapla(df_grafik)

            secili_sinyal = next(r for r in sinyaller if r["Hisse"] == secili)

            fig = make_subplots(
                rows=2, cols=1, shared_xaxes=True,
                row_heights=[0.7, 0.3], vertical_spacing=0.04
            )

            # Mum grafik
            fig.add_trace(go.Candlestick(
                x=df_grafik.index,
                open=df_grafik["Open"], high=df_grafik["High"],
                low=df_grafik["Low"],   close=df_grafik["Close"],
                name="Fiyat",
                increasing_line_color="#22c55e",
                decreasing_line_color="#ef4444",
            ), row=1, col=1)

            # EMA çizgileri
            for col_name, renk, genislik in [
                ("EMA20","#38bdf8",1.5), ("EMA50","#f59e0b",1.5),
                ("EMA100","#a78bfa",1),  ("EMA200","#f472b6",1),
            ]:
                fig.add_trace(go.Scatter(
                    x=df_grafik.index, y=df_grafik[col_name],
                    name=col_name, line=dict(color=renk, width=genislik)
                ), row=1, col=1)

            # Stop ve hedef çizgileri
            son_tarih  = df_grafik.index[-1]
            bitis      = son_tarih + timedelta(days=15)
            for seviye, renk, isim in [
                (secili_sinyal["Stop"],  "#ef4444", "Stop"),
                (secili_sinyal["Hedef"], "#22c55e", "Hedef"),
            ]:
                fig.add_shape(type="line",
                    x0=son_tarih, x1=bitis, y0=seviye, y1=seviye,
                    line=dict(color=renk, width=1.5, dash="dash"),
                    row=1, col=1)
                fig.add_annotation(
                    x=bitis, y=seviye, text=isim + " " + str(seviye),
                    showarrow=False, font=dict(color=renk, size=11),
                    xanchor="left", row=1, col=1)

            # Stokastik
            fig.add_trace(go.Scatter(
                x=df_grafik.index, y=df_grafik["K"],
                name="%K", line=dict(color="#38bdf8", width=1.5)
            ), row=2, col=1)
            fig.add_trace(go.Scatter(
                x=df_grafik.index, y=df_grafik["D"],
                name="%D", line=dict(color="#f59e0b", width=1.5)
            ), row=2, col=1)
            fig.add_hline(y=20, line_dash="dot",
                          line_color="#64748b", row=2, col=1)
            fig.add_hline(y=80, line_dash="dot",
                          line_color="#64748b", row=2, col=1)

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0d0f14",
                plot_bgcolor="#0d0f14",
                height=650,
                showlegend=True,
                xaxis_rangeslider_visible=False,
                margin=dict(l=10, r=80, t=30, b=10),
                font=dict(family="Consolas", size=11),
            )
            fig.update_yaxes(gridcolor="#1e293b")
            fig.update_xaxes(gridcolor="#1e293b")

            st.plotly_chart(fig, use_container_width=True)
