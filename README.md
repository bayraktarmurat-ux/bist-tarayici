# BIST Sinyal Tarayıcı

MACD Histogram Dönüşü stratejisi ile BIST hisselerini tarayan sistem.

## Strateji
- **Endeks Filtresi**: BIST100 > EMA200 olduğunda aktif
- **Trend**: EMA20 > EMA50 > EMA100 > EMA200
- **Giriş**: MACD histogram negatiften pozitife döndüğünde
- **Stop**: ATR × 1.5
- **Hedef**: R:R 1:3
- **Risk**: Portföyün %1'i

## Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `bist_streamlit.py` | Web arayüzü — günlük tarayıcı |
| `bist_tarayici.py` | Komut satırı tarayıcı |
| `bist_telegram_bot.py` | Telegram otomatik bildirim |
| `bist_backtest_ui.py` | Streamlit backtest arayüzü |

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

### Web Tarayıcı
```bash
streamlit run bist_streamlit.py
```

### Komut Satırı
```bash
python bist_tarayici.py
```

### Backtest
```bash
streamlit run bist_backtest_ui.py
```

## GitHub Actions (Otomatik Telegram)
`.github/workflows/bist_bot.yml` dosyası her hafta içi saat 17:00 UTC (20:00 TR) çalışır.

Repo → Settings → Secrets → Actions:
- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID`

## Gereksinimler
- Python 3.10+
- `pip install -r requirements.txt`
