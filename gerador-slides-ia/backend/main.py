from firebase_functions import https_fn, options
from firebase_admin import initialize_app, firestore
import google.generativeai as genai
import json

# Inicializa o Firebase Admin
initialize_app()

def get_db():
    return firestore.client()

@https_fn.on_call(memory=options.MemoryOption.GB_1)
def gerarSlidesIA(req: https_fn.CallableRequest):
    """
    Gera conteúdo para slides a partir de um texto bruto usando o modelo Gemini.
    """
    data = req.data
    rascunho = data.get('rascunho')
    qtd_slides = data.get('qtdSlides', 5)

    if not rascunho:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, 
            message="Texto bruto não fornecido."
        )

    try:
        # Busca chave de API do Firestore (ajuste conforme seu esquema)
        db = get_db()
        keys_doc = db.collection('system').document('api_keys').get()
        
        if not keys_doc.exists:
            # Caso não exista no banco, tenta buscar de variável de ambiente
            import os
            GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
        else:
            GEMINI_API_KEY = keys_doc.to_dict().get('gemini_api_key')

        if not GEMINI_API_KEY:
            raise https_fn.HttpsError(
                code=https_fn.FunctionsErrorCode.FAILED_PRECONDITION, 
                message="Chave Gemini não configurada."
            )

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash-lite")

        system_instruction = f"""
        Atue como Especialista em Design de Apresentações Profissionais.
        Sua tarefa é transformar o texto bruto fornecido em uma estrutura de apresentação de slides premium.
        
        Regras de Negócio:
        1. Gere EXATAMENTE {qtd_slides} slides.
        2. Use layouts variados: 'capa' (apenas no primeiro), 'titulo_e_conteudo', 'somente_titulo'.
        3. Tópicos: Use frases curtas, impactantes e diretas. No máximo 4 tópicos por slide. 
        4. O campo 'topicos' deve ser SEMPRE uma lista de strings.
        5. Prompt de Imagem: Forneça um prompt em INGLÊS detalhado para cada slide, focado em imagens corporativas e modernas.
        6. Tom de voz: Profissional, executivo e inspirador.

        Retorne APENAS um objeto JSON seguindo este esquema:
        {{
          "slides": [
            {{
              "numero": 1,
              "layout": "capa",
              "titulo": "Título",
              "topicos": ["Subtítulo"],
              "prompt_imagem": "Professional background..."
            }}
          ]
        }}
        """

        response = model.generate_content([
            system_instruction,
            f"Texto Bruto para Processar:\n{rascunho}"
        ], generation_config={"response_mime_type": "application/json"})

        text_response = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text_response)

    except Exception as e:
        print(f"Erro ao gerar slides: {str(e)}")
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INTERNAL, message=str(e))
