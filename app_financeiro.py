import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Simulador Financeiro", layout="wide")
st.title("💸 Simulador Financeiro Interativo")

# Criando as duas abas que você pediu
aba_dividas, aba_lucros = st.tabs(["Controle de Dívidas", "Simulador de Investimentos"])

# ==========================================
# ABA 1: CONTROLE DE DÍVIDAS (Amortização)
# ==========================================
with aba_dividas:
    st.header("Sistema de Amortização de Dívidas")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        X_divida = st.number_input("Montante da Dívida (X) - R$", min_value=0.0, value=10000.0, step=100.0)
    with col2:
        Y_juros_divida = st.number_input("Juros Embutido (Y) - % ao mês", min_value=0.0, value=2.0, step=0.1) / 100
    with col3:
        Z_meses_divida = st.number_input("Período (Z) - Meses", min_value=1, value=12, step=1)
        
    valor_deducao_extra = st.number_input("Valor extra para deduzir por mês (Amortização Extra) - R$", min_value=0.0, value=0.0, step=50.0)

    if st.button("Calcular Dívida"):
        # Cálculo da parcela (Sistema Price)
        if Y_juros_divida > 0:
            parcela = X_divida * (Y_juros_divida * (1 + Y_juros_divida)**Z_meses_divida) / ((1 + Y_juros_divida)**Z_meses_divida - 1)
        else:
            parcela = X_divida / Z_meses_divida
            
        saldo_devedor = X_divida
        dados_amortizacao = []
        
        for mes in range(1, int(Z_meses_divida) + 1):
            juros_mes = saldo_devedor * Y_juros_divida
            amortizacao_mes = parcela - juros_mes + valor_deducao_extra
            
            # Garante que não vamos pagar mais do que devemos no último mês
            if amortizacao_mes > saldo_devedor:
                amortizacao_mes = saldo_devedor
                parcela = amortizacao_mes + juros_mes - valor_deducao_extra
                
            saldo_devedor -= amortizacao_mes
            
            dados_amortizacao.append({
                "Mês": mes,
                "Valor da Parcela (R$)": round(parcela + valor_deducao_extra, 2),
                "Juros Pagos (R$)": round(juros_mes, 2),
                "Valor Real Deduzido (R$)": round(amortizacao_mes, 2),
                "Saldo Devedor (R$)": round(max(0, saldo_devedor), 2)
            })
            
            if saldo_devedor <= 0:
                break
                
        df_dividas = pd.DataFrame(dados_amortizacao)
        st.dataframe(df_dividas, use_container_width=True)

# ==========================================
# ABA 2: SIMULADOR DE LUCRO / INVESTIMENTO
# ==========================================
with aba_lucros:
    st.header("Evolução de Patrimônio")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        X_investimento = st.number_input("Montante Inicial (X) - R$", min_value=0.0, value=1000.0, step=100.0)
    with col2:
        Y_juros_lucro = st.number_input("Rendimento Mensal (Y) - %", min_value=0.0, value=1.0, step=0.1) / 100
    with col3:
        Z_meses_lucro = st.number_input("Tempo de Investimento (Z) - Meses", min_value=1, value=12, step=1)
        
    aporte_mensal = st.number_input("Aporte Mensal - R$", min_value=0.0, value=100.0, step=50.0)

    if st.button("Calcular Rendimento"):
        saldo_acumulado = X_investimento
        dados_lucro = []
        
        for mes in range(1, int(Z_meses_lucro) + 1):
            rendimento_mes = saldo_acumulado * Y_juros_lucro
            saldo_acumulado += rendimento_mes + aporte_mensal
            
            dados_lucro.append({
                "Mês": mes,
                "Aporte do Mês (R$)": aporte_mensal,
                "Juros Ganhos (R$)": round(rendimento_mes, 2),
                "Patrimônio Total (R$)": round(saldo_acumulado, 2)
            })
            
        df_lucro = pd.DataFrame(dados_lucro)
        st.dataframe(df_lucro, use_container_width=True)