import os
import google.generativeai as genai
from dotenv import load_dotenv 

# carregar arquivo .env
load_dotenv() 


# configurar a API 
def config_gemini_api():
    api_key = os.getenv("GEMINI_API_KEY") or input("Insira sua chave Gemini: ")
    if not api_key:
        print("Chave não fornecida. IA desativada.")
        return False
    
    try:
        genai.configure(api_key=api_key)
        print("API Gemini configurada.")
        return True
    
    except Exception as e:
        print(f"Erro ao configurar API: {e}")
        return False

gemini_configurada = config_gemini_api()

# sugestão de diagnóstico pela IA
def sugerir_diagnostico_ia():
    if not gemini_configurada:
        print("IA desativada.")
        return
    
    sintomas = input("\nDescreva os sintomas do pet: ")
    if not sintomas:
        print("Nenhum sintoma informado.")
        return
    print("Consultando IA...")
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Você é um assistente veterinário virtual. Sintomas: {sintomas}. 
Sugira possíveis causas e oriente procurar um veterinário."""
        response = model.generate_content(prompt)
        print("\n--- Sugestão da IA ---")
        print(response.text 
              if hasattr(response, 'text') 
              else "Resposta vazia.")
    
    except Exception as e:
        print(f"Erro na consulta IA: {e}")