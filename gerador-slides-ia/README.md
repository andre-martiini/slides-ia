# Gerador de Slides IA

Módulo independente para geração de apresentações profissionais a partir de texto bruto, utilizando IA (Google Gemini) e exportação para PowerPoint (PPTX).

## 🚀 Estrutura do Módulo

- **`frontend/`**: Componentes React (TSX) e lógica de interface.
  - `SlidesTool.tsx`: Componente principal.
  - `AutoExpandingTextarea.tsx`: Utilitário de UI.
  - **Dependências**: React, Firebase (Callable Functions), PPTXGenJS, Tailwind CSS.
- **`backend/`**: Lógica de processamento (Cloud Functions).
  - `main.py`: Função Python que orquestra o Google Gemini.
  - **Dependências**: `firebase-functions`, `firebase-admin`, `google-generativeai`.

## 🛠️ Configuração

### Backend (Firebase Functions)
1. Certifique-se de ter uma conta no Firebase e o `firebase-tools` instalado.
2. Configure sua chave do Google Gemini no Firestore no caminho `system/api_keys` (campo `gemini_api_key`) ou como variável de ambiente `GEMINI_API_KEY`.
3. O modelo utilizado é o `gemini-2.5-flash-lite`.

### Frontend
1. Importe o `SlidesTool` em seu projeto React.
2. Certifique-se de que o Tailwind CSS e as animações base (conforme `index.html` original) estejam configurados.
3. Passe a instância do Firebase Functions para o componente via prop `functionsInstance`.

## 📦 Dependências Externas
- [PPTXGenJS](https://gitbrent.github.io/PptxGenJS/): Para geração dos arquivos .pptx.
- [Google Generative AI](https://ai.google.dev/): Para o processamento de linguagem natural.
- [Firebase Cloud Functions](https://firebase.google.com/docs/functions): Para o backend serverless.

## 🎨 Estética
O design utiliza uma paleta escura premium baseada em `slate-900` com accents em `orange-500`, focado em legibilidade e modernidade.
