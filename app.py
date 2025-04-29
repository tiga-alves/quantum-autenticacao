import streamlit as st
import boto3
import io
import re

st.set_page_config(page_title="Validação de Identidade", layout="centered")
st.title("🧠 Validação de Identidade com AWS")

# Add custom CSS no início para garantir que está disponível
st.markdown("""
    <style>
    .doc-info {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

selfie_file = st.file_uploader("📸 Envie sua Selfie", type=["jpg", "jpeg", "png"])
doc_file = st.file_uploader("🪪 Envie o Documento com Foto", type=["jpg", "jpeg", "png"])

if selfie_file and doc_file:
    st.image(selfie_file, width=250, caption="Selfie")
    st.image(doc_file, width=250, caption="Documento")

    rekognition = boto3.client("rekognition", region_name="us-east-1")
    textract = boto3.client("textract", region_name="us-east-1")

    # Leitura das imagens
    selfie_bytes = selfie_file.read()
    doc_bytes = doc_file.read()

    # --- Comparar Rostos ---
    with st.spinner("🔍 Comparando rostos..."):
        result = rekognition.compare_faces(
            SourceImage={'Bytes': selfie_bytes},
            TargetImage={'Bytes': doc_bytes},
            SimilarityThreshold=80
        )

        if result['FaceMatches']:
            similarity = result['FaceMatches'][0]['Similarity']
            st.success(f"✅ Mesma pessoa! Similaridade: {similarity:.2f}%")
            
            # --- Extração de Texto ---
            with st.spinner("📄 Extraindo texto do documento..."):
                response = textract.detect_document_text(Document={'Bytes': doc_bytes})
                st.subheader("📝 Informações do Documento:")
                
                # Extrair linhas de texto
                lines = [block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE']
                
                # Procurar por Nome e CPF
                nome = ""
                cpf = ""
                
                for i, line in enumerate(lines):
                    if line.upper() == "NOME" and i + 1 < len(lines):
                        nome = lines[i + 1]
                    elif line.upper() == "CPF" and i + 1 < len(lines):
                        cpf = lines[i + 1]
                
                # Mostrar informações do documento dentro de um container
                container_html = f"""
                    <div class="doc-info">
                        <p><strong>Nome:</strong> {nome}</p>
                        <p><strong>CPF:</strong> {cpf}</p>
                    </div>
                """
                st.markdown(container_html, unsafe_allow_html=True)
        else:
            st.error("❌ Rostos não correspondem!")
