# 🧠 Sistema de Validação de Identidade com AWS

## 📋 Sobre o Projeto
Este é um sistema de validação de identidade que utiliza serviços da AWS (Amazon Web Services) para comparar uma selfie com um documento de identificação com foto e extrair informações textuais do documento. O projeto foi desenvolvido usando Streamlit para criar uma interface web intuitiva e amigável.

## 🚀 Funcionalidades
- Upload de selfie e documento com foto
- Comparação facial usando AWS Rekognition
- Extração de texto do documento usando AWS Textract
- Interface web responsiva e amigável
- Suporte para diferentes formatos de imagem (JPG, JPEG, PNG)

## 🛠️ Tecnologias Utilizadas
- Python 3.x
- Streamlit
- AWS SDK (boto3)
- AWS Rekognition
- AWS Textract
- Pillow (PIL)

## ⚙️ Pré-requisitos
- Python 3.x instalado
- Conta AWS com acesso aos serviços Rekognition e Textract
- Credenciais AWS configuradas

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/validacao-identidade-aws.git
cd validacao-identidade-aws
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure suas credenciais AWS:
- Crie um arquivo `~/.aws/credentials` (Linux/Mac) ou `%UserProfile%\.aws\credentials` (Windows)
- Adicione suas credenciais:
```ini
[default]
aws_access_key_id = sua_access_key
aws_secret_access_key = sua_secret_key
```

## 🚀 Como Executar

1. Execute o aplicativo Streamlit:
```bash
streamlit run app.py
```

2. Acesse o aplicativo em seu navegador (geralmente em `http://localhost:8501`)

## 📝 Como Usar
1. Faça upload de uma selfie recente
2. Faça upload de um documento com foto (RG, CNH, etc.)
3. Aguarde a análise automática
4. Verifique o resultado da comparação facial e o texto extraído

## 🔒 Segurança
- As imagens são processadas em memória e não são armazenadas
- Utiliza conexão segura com AWS
- Requer autenticação AWS válida

## ⚠️ Limitações
- Tamanho máximo de arquivo: Determinado pelo Streamlit
- Formatos suportados: JPG, JPEG, PNG
- Requer conexão com internet
- Necessita de boa qualidade nas imagens para melhor precisão

## 💰 Custos
Este projeto utiliza serviços AWS que podem gerar custos:
- AWS Rekognition: Cobrado por imagem analisada
- AWS Textract: Cobrado por página processada
Consulte a [documentação AWS](https://aws.amazon.com/pricing/) para mais detalhes sobre preços.

## 🤝 Contribuindo
Contribuições são bem-vindas! Para contribuir:
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📧 Contato
Seu Nome - [@seutwitter](https://twitter.com/seutwitter) - email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/validacao-identidade-aws](https://github.com/seu-usuario/validacao-identidade-aws)