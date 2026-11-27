import streamlit as st
import re

st.set_page_config(page_title="Escudo Digital - Detector de Golpes", page_icon="🛡️")

st.title("🛡️ Escudo Digital: Detector de Golpes")
st.markdown("Cole abaixo uma mensagem suspeita recebida por **WhatsApp, SMS ou E-mail** para verificar se há risco de fraude.")

mensagem = st.text_area("Cole a mensagem aqui:", height=150, placeholder="Ex: Olá, seu CPF foi bloqueado! Acesse http://bit.ly para evitar multa.")

def analisar_mensagem(texto):
    pontuacao_risco = 0
    alertas = []
    texto_lower = texto.lower()

    gatilhos_urgencia = [
        r"urgente", r"bloquead[oa]", r"suspens[oa]", r"última chance",
        r"hoje", r"imediatamente", r"multa", r"cancelad[oa]", r"expira"
    ]
    for padrao in gatilhos_urgencia:
        if re.search(padrao, texto_lower):
            pontuacao_risco += 15
            alertas.append("⚠️ **Gatilho de Urgência/Medo:** A mensagem pressiona você a agir rápido sem pensar.")
            break

    iscas_financeiras = [
        r"pix", r"prêmio", r"ganhou", r"resgate", r"empréstimo",
        r"receita federal", r"serasa", r"spc", r"banco", r"fatura", r"boleto", r"brinde"
    ]
    for padrao in iscas_financeiras:
        if re.search(padrao, texto_lower):
            pontuacao_risco += 20
            alertas.append("💰 **Isca Financeira ou Institucional:** Menciona dinheiro, prêmios ou órgãos oficiais.")
            break

    dados_sensiveis = [
        r"senha", r"código", r"token", r"cpf", r"cartão", r"cvv", r"dados bancários"
    ]
    for padrao in dados_sensiveis:
        if re.search(padrao, texto_lower):
            pontuacao_risco += 30
            alertas.append("🔐 **Solicitação de Dados Sensíveis:** Empresas sérias nunca pedem senhas ou códigos por mensagem.")
            break

    urls = re.findall(r'(https?://[^\s]+|www\.[^\s]+)', texto_lower)
    encurtadores = ["bit.ly", "tinyurl", "is.gd", "t.co", "cutt.ly", "rb.gy", "shorturl"]
    dominios_oficiais_gov = [".gov.br"]

    if urls:
        pontuacao_risco += 15
        alertas.append(f"🔗 **Link Detectado ({len(urls)}):** Mensagens com links exigem atenção redobrada.")
        
        for url in urls:
            if not url.startswith("https://"):
                pontuacao_risco += 15
                alertas.append("🔓 **Conexão Insegura (Sem HTTPS):** O link não utiliza criptografia padrão.")
            
            if any(enc in url for enc in encurtadores):
                pontuacao_risco += 25
                alertas.append("🎭 **Link Encurtado:** O endereço verdadeiro está escondido, técnica comum em golpes.")
            
            if ("receita" in texto_lower or "gov" in texto_lower or "inss" in texto_lower) and not any(gov in url for gov in dominios_oficiais_gov):
                pontuacao_risco += 35
                alertas.append("🚨 **Falsificação de Órgão Público:** Cita o governo, mas o link NÃO termina em `.gov.br`.")

    return min(pontuacao_risco, 100), alertas

if st.button("Analisar Mensagem", type="primary"):
    if not mensagem.strip():
        st.warning("Por favor, cole uma mensagem antes de analisar.")
    else:
        risco, motivos = analisar_mensagem(mensagem)
        
        st.subheader("Resultado da Análise")
        st.progress(risco / 100)
        
        if risco >= 60:
            st.error(f"🚨 **ALTO RISCO DE GOLPE ({risco}%)** — Não clique em links nem responda!")
        elif risco >= 30:
            st.warning(f"⚠️ **RISCO MODERADO ({risco}%)** — Desconfie e confirme por um canal oficial.")
        else:
            st.success(f"✅ **BAIXO RISCO ({risco}%)** — Nenhum padrão óbvio de golpe encontrado, mas mantenha a atenção.")

        if motivos:
            st.markdown("### O que encontramos:")
            for m in motivos:
                st.markdown(f"- {m}")
        else:
            st.info("Não foram encontrados links suspeitos ou palavras-chave típicas de engenharia social.")

st.markdown("---")
st.caption("Projeto de Extensão Universitária (PEX III) - Ciência da Computação | Ferramenta educativa gratuita para a comunidade.")
