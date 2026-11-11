import streamlit as st
import pandas as pd
import json
import yfinance as yf
from pathlib import Path

st.set_page_config(page_title="R1 Screener", page_icon="chart_with_downwards_trend", layout="wide")

APP_DIR = Path(__file__).parent

@st.cache_data(ttl=300)
def load_screener():
    with open(APP_DIR / "last_screener.json") as f:
        return json.load(f)

data = load_screener()
regime = data.get("regime", {})
signals = data.get("signals", [])

st.sidebar.title("R1 Screener")
st.sidebar.markdown("**Regimen:** " + str(regime.get("regime", "?")))
st.sidebar.markdown("**Senales:** " + str(len(signals)))
st.sidebar.markdown("---")
st.sidebar.warning("DSR 0.76. Edge podria ser ruido. Paper trading 3 meses obligatorio.")

st.title("R1 Screener - Mean Reversion en Bear Market")

if regime.get("regime") == "BEAR":
    st.success("REGIMEN: BEAR - R1 operable")
else:
    st.error("REGIMEN: BULL - NO OPERAR. R1 solo funciona en bear.")

tab1, tab2, tab3, tab4 = st.tabs(["Senales", "Detalle", "Paper Trading", "Info"])

with tab1:
    st.header("Senales R1 hoy (ordenadas por score ponderado)")
    if not signals:
        st.warning("No hay senales R1 hoy. Normal - R1 requiere condiciones extremas.")
    else:
        df_sig = pd.DataFrame([{
            "Ticker": s["ticker"],
            "Score": s.get("weighted_score", 0),
            "Fuerza": str(s.get("n_strong", 0)) + "/" + str(s.get("n_total", 5)),
            "Precio": "$" + str(round(s["price"], 2)),
        } for s in signals])
        df_sig = df_sig.sort_values("Score", ascending=False)
        st.dataframe(df_sig, use_container_width=True, hide_index=True)

with tab2:
    st.header("Detalle por ticker")
    if signals:
        ticker_sel = st.selectbox("Ticker", [s["ticker"] for s in signals])
        sel = next(s for s in signals if s["ticker"] == ticker_sel)
        st.metric("Score Ponderado", sel.get("weighted_score", 0))
        if "conditions" in sel:
            for c in sel["conditions"]:
                icon = "verde" if c.get("strong") else "amarillo"
                st.markdown("**" + c["feature"] + "**: " + str(round(c["value"], 4)) + " (umbral " + str(round(c["threshold"], 4)) + ") - " + icon)

with tab3:
    st.header("Paper Trading")
    st.info("Registra cada trade manualmente. Edita paper_trading.json en el repo.")
    hist_file = APP_DIR / "paper_trading.json"
    if hist_file.exists():
        with open(hist_file) as f:
            history = json.load(f)
        if history:
            st.dataframe(pd.DataFrame(history), use_container_width=True)
        else:
            st.info("Sin trades registrados aun.")
    else:
        st.info("Crea paper_trading.json con [] para empezar.")

with tab4:
    st.header("Sobre R1")
    st.markdown("### Regla R1")
    st.markdown("- ret_5 < P33: caida corto plazo")
    st.markdown("- ret_252 < P33: caida largo plazo")
    st.markdown("- macd_hist > P67: momentum mejorando")
    st.markdown("- dist_ma_20 < P33: precio bajo su MA20")
    st.markdown("- atr_norm > P67: volatilidad alta")
    st.markdown("### Rendimiento historico")
    st.markdown("- Bear: hit 66.5%, +2.387% por trade, Sharpe 1.40")
    st.markdown("- Bull: hit 49.9%, +0.108% por trade, Sharpe 0.10")
    st.markdown("### Advertencias")
    st.markdown("- DSR 0.76: podria ser ruido de multiple testing")
    st.markdown("- Solo bear: no operar si SPY > MA200")
    st.markdown("- Paper trading 3 meses obligatorio antes de dinero real")
