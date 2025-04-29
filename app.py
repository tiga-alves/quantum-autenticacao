import streamlit as st
import boto3
import io
import re
from difflib import SequenceMatcher
import uuid  # Adicionar esta importação no topo do arquivo

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

def similar(a, b):
    # Função para comparar similaridade entre strings
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

selfie_file = st.file_uploader("📸 Envie sua Selfie", type=["jpg", "jpeg", "png"])
doc_file = st.file_uploader("🪪 Envie o Documento com Foto", type=["jpg", "jpeg", "png"])
comprovante_file = st.file_uploader("📄 Envie o Comprovante de Residência", type=["pdf"])

if selfie_file and doc_file and comprovante_file:
    st.image(selfie_file, width=250, caption="Selfie")
    st.image(doc_file, width=250, caption="Documento")

    rekognition = boto3.client("rekognition", region_name="us-east-1")
    textract = boto3.client("textract", region_name="us-east-1")

    # Leitura das imagens
    selfie_bytes = selfie_file.read()
    doc_bytes = doc_file.read()
    comprovante_bytes = comprovante_file.read()

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
            
            # --- Extração de Texto do Documento ---
            with st.spinner("📄 Extraindo texto do documento..."):
                response = textract.detect_document_text(Document={'Bytes': doc_bytes})
                st.subheader("📝 Informações do Documento:")
                
                # Extract text lines do documento
                lines = [block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE']
                
                # Find nome and CPF
                nome_doc = ""
                cpf = ""
                
                for i, line in enumerate(lines):
                    if line.upper() == "NOME" and i + 1 < len(lines):
                        nome_doc = lines[i + 1]
                    elif line.upper() == "CPF" and i + 1 < len(lines):
                        cpf = lines[i + 1]
                
                # Display the information in the styled container
                container_html = f"""
                    <div class="doc-info">
                        <p><strong>Nome:</strong> {nome_doc}</p>
                        <p><strong>CPF:</strong> {cpf}</p>
                    </div>
                """
                st.markdown(container_html, unsafe_allow_html=True)

            # --- Extração de Texto do Comprovante ---
            with st.spinner("📄 Extraindo texto do comprovante de residência..."):
                try:
                    # Criar cliente S3
                    s3 = boto3.client('s3')
                    bucket_name = 'projeto-validacao'
                    
                    # Gerar um nome único para o arquivo
                    file_key = f'temp/{uuid.uuid4()}.pdf'
                    
                    # Upload do arquivo para S3
                    s3.put_object(
                        Bucket=bucket_name,
                        Key=file_key,
                        Body=comprovante_bytes
                    )

                    # Iniciar o job de processamento do PDF
                    response_start = textract.start_document_text_detection(
                        DocumentLocation={
                            'S3Object': {
                                'Bucket': bucket_name,
                                'Name': file_key
                            }
                        }
                    )
                    job_id = response_start['JobId']

                    # Aguardar o processamento
                    import time
                    status = 'IN_PROGRESS'
                    while status == 'IN_PROGRESS':
                        response_get = textract.get_document_text_detection(JobId=job_id)
                        status = response_get['JobStatus']
                        if status == 'IN_PROGRESS':
                            time.sleep(1)

                    # Deletar o arquivo do S3 após o processamento
                    s3.delete_object(Bucket=bucket_name, Key=file_key)

                    # Processar os resultados
                    if status == 'SUCCEEDED':
                        st.subheader("📝 Informações do Comprovante:")
                        
                        # Extrair todas as linhas de texto
                        lines_comprovante = []
                        for item in response_get['Blocks']:
                            if item['BlockType'] == 'LINE':
                                lines_comprovante.append(item['Text'])
                        
                        texto_completo = " ".join(lines_comprovante)
                        
                        # Procurar por endereço no comprovante
                        endereco = ""
                        for i, line in enumerate(lines_comprovante):
                            if "ENDEREÇO" in line.upper() or "RUA" in line.upper() or "AVENIDA" in line.upper():
                                endereco = line
                                # Tenta pegar mais linhas do endereço
                                if i + 1 < len(lines_comprovante):
                                    endereco += f" {lines_comprovante[i + 1]}"

                        # Verificar se o nome do documento está presente no comprovante
                        nome_encontrado = nome_doc.strip() in texto_completo

                        # Display the information in the styled container
                        container_html = f"""
                            <div class="doc-info">
                                <p><strong>Endereço:</strong> {endereco}</p>
                            </div>
                        """
                        st.markdown(container_html, unsafe_allow_html=True)

                        # Mostrar resultado da validação do nome
                        if nome_encontrado:
                            st.success("✅ Nome do documento encontrado no comprovante de residência!")
                        else:
                            st.error("❌ Nome do documento não encontrado no comprovante de residência!")
                    else:
                        st.error(f"❌ Erro ao processar o PDF: {status}")

                except Exception as e:
                    st.error(f"❌ Erro ao processar o comprovante: {str(e)}")
                    
        else:
            st.error("❌ Rostos não correspondem!")
