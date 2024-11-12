# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from funcoes import obter_dados_criptomoeda, calcular_bandas_bollinger, calcular_rsi

# Configurações do Streamlit
st.set_page_config(page_title="Análise de Criptomoedas", layout="wide")

# Título do Aplicativo
st.title("Análise de Criptomoedas com Bandas de Bollinger e RSI")

# Input para o usuário inserir o símbolo da criptomoeda
simbolo = st.text_input("Digite o símbolo da criptomoeda (ex: bitcoin, ethereum):", value="bitcoin", max_chars=20)

# Botão para atualizar os dados
if st.button("Atualizar Dados"):
    intervalos = ['4h', 'daily']
    cores = {
        'Cotação': 'blue',
        'Banda Superior': 'green',
        'Banda Inferior': 'red'
    }
    
    for intervalo in intervalos:
        st.header(f"Gráficos de Intervalo {intervalo.upper()}")

        try:
            # Obter dados
            df = obter_dados_criptomoeda(simbolo, intervalo)
            
            # Gráfico de preços
            fig1, ax1 = plt.subplots(figsize=(14, 5))
            sns.lineplot(data=df, x=df.index, y='close', label="Cotação", color=cores['Cotação'], ax=ax1)
            ax1.set_title(f"{simbolo.capitalize()} - Preço de Fechamento ({intervalo.upper()})")
            ax1.set_xlabel("Data")
            ax1.set_ylabel("Preço (USD)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig1)

            # Calcular e exibir o gráfico com Bandas de Bollinger
            df_bb = calcular_bandas_bollinger(df.copy())
            fig2, ax2 = plt.subplots(figsize=(14, 5))
            sns.lineplot(data=df_bb, x=df_bb.index, y='close', label="Cotação", color=cores['Cotação'], ax=ax2)
            sns.lineplot(data=df_bb, x=df_bb.index, y='Upper Band', label="Banda Superior", color=cores['Banda Superior'], linestyle="--", ax=ax2)
            sns.lineplot(data=df_bb, x=df_bb.index, y='Lower Band', label="Banda Inferior", color=cores['Banda Inferior'], linestyle="--", ax=ax2)
            ax2.set_title(f"{simbolo.capitalize()} - Bandas de Bollinger ({intervalo.upper()})")
            ax2.set_xlabel("Data")
            ax2.set_ylabel("Preço (USD)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig2)

            # Calcular e exibir o gráfico de RSI
            df_rsi = calcular_rsi(df_bb.copy())
            fig3, ax3 = plt.subplots(figsize=(14, 3))
            sns.lineplot(data=df_rsi, x=df_rsi.index, y='RSI', color='purple', ax=ax3)
            ax3.axhline(70, linestyle="--", color="red", label="Sobrecompra (70)")
            ax3.axhline(30, linestyle="--", color="green", label="Sobrevenda (30)")
            ax3.set_title(f"{simbolo.capitalize()} - RSI ({intervalo.upper()})")
            ax3.set_xlabel("Data")
            ax3.set_ylabel("RSI")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig3)

            # Exibir valores absolutos do RSI e das bandas de Bollinger
            ultimo_valor = df_rsi.iloc[-1]
            tabela_resultados = pd.DataFrame({
                'Indicador': ['RSI', 'Banda Superior', 'Banda Inferior'],
                'Valor Atual': [
                    f"{ultimo_valor['RSI']:.2f}",
                    f"{ultimo_valor['Upper Band']:.2f}",
                    f"{ultimo_valor['Lower Band']:.2f}"
                ]
            })

            # Mostrar tabela abaixo dos gráficos
            st.subheader(f"Valores Absolutos - {intervalo.upper()}")
            st.table(tabela_resultados)

        except Exception as e:
            st.error(f"Erro ao obter dados para {simbolo.capitalize()}: {e}")
