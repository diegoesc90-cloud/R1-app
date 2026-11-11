# R1 Screener App

## Ejecutar localmente
Instala dependencias: pip install -r requirements.txt
Ejecuta: streamlit run app.py

## Desplegar en Streamlit Cloud
1. Sube esta carpeta a un repo publico de GitHub
2. Ve a share.streamlit.io
3. New app, selecciona el repo, main file: app.py
4. Deploy

## Configuracion
- last_screener.json: resultados del ultimo screener
- percentiles_train.json: percentiles P33/P67 del train (2010-2021)
- paper_trading.json: historial de trades

## Advertencias
- DSR 0.76: edge podria ser ruido de multiple testing
- Solo funciona en bear market (SPY < MA200)
- Paper trading 3 meses antes de dinero real
