import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, date
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
                         start=bas.strftime("%Y-%m-%d"),
                         end=bit.strftime("%Y-%m-%d"),
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
st.title("📊 BIST Tekil Hisse Backtest")
st.caption(f"Strateji: EMA Dokunuşu + Stokastik Kesişim | R:R 1:{rr_kat:.0f} | Stop ATR×{atr_kat}")

# ─── BACKTEST BUTONU ──────────────────────────────────────────────────────────
if st.button("🚀 Backtest Çalıştır", use_container_width=True, type="primary"):
    if not hisse_input:
        st.error("Lütfen bir hisse kodu girin.")
        st.stop()

    bas_ts  = pd.Timestamp(bas_tarih)
    bit_ts  = pd.Timestamp(bit_tarih)

    with st.spinner(f"{hisse_input} verisi indiriliyor..."):
        # EMA200 için 1 yıl önceden başla
        veri_bas = bas_ts - pd.DateOffset(years=1)
        df_raw = veri_cek(hisse_input, veri_bas, bit_ts + pd.DateOffset(days=1))

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

        # Endeks filtresi
        endeks_f = {}
        if endeks_aktif:
            endeks_f = endeks_filtre_olustur(bas_ts, bit_ts + pd.DateOffset(days=1))

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

    st.session_state["islemler"]  = islemler
    st.session_state["portfoy_s"] = portfoy_s
    st.session_state["df"]        = df
    st.session_state["hisse"]     = hisse_input
    st.session_state["portfoy"]   = portfoy
    st.session_state["bas_ts"]    = bas_ts
    st.session_state["bit_ts"]    = bit_ts
    st.session_state["rr_kat"]    = rr_kat

# ─── SONUÇLAR ─────────────────────────────────────────────────────────────────
if "islemler" in st.session_state:
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
