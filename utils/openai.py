"""
Utilidades para interactuar con la API de OpenAI
"""

import logging
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

# Inicializar cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuración de logging
logger = logging.getLogger(__name__)

def generate_response(prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
    """
    Genera una respuesta usando OpenAI
    
    Args:
        prompt: El mensaje del usuario
        system_prompt: Mensaje de sistema para dirigir el comportamiento del modelo
        temperature: Controla la aleatoriedad de las respuestas (0-1)
        
    Returns:
        Respuesta generada por OpenAI
    """
    try:
        messages = []
        
        # Agregar mensaje de sistema si está disponible
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        # Agregar mensaje del usuario
        messages.append({"role": "user", "content": prompt})
        
        # Llamar a la API de OpenAI
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        logger.error(f"Error al generar respuesta con OpenAI: {e}")
        return f"Lo siento, no pude generar una respuesta en este momento. Error: {str(e)}"

def analyze_coffee_data(data: Dict[str, Any]) -> str:
    """
    Analiza datos de café usando OpenAI
    
    Args:
        data: Diccionario con datos de café
        
    Returns:
        Análisis del café
    """
    try:
        system_prompt = """
        Eres un experto en la industria del café que analiza datos de operaciones de café.
        Proporciona información valiosa y recomendaciones basadas en los datos proporcionados.
        Enfócate en identificar tendencias, áreas de mejora y oportunidades de optimización.
        """
        
        prompt = f"""
        Por favor, analiza los siguientes datos de operaciones de café:
        {json.dumps(data, indent=2, ensure_ascii=False)}
        
        Proporciona:
        1. Un resumen de los principales hallazgos
        2. Tendencias identificadas
        3. Áreas de mejora
        4. Recomendaciones específicas
        """
        
        return generate_response(prompt, system_prompt, temperature=0.3)
    
    except Exception as e:
        logger.error(f"Error al analizar datos de café: {e}")
        return f"Lo siento, no pude analizar los datos en este momento. Error: {str(e)}"

def generate_coffee_recommendation(preferences: Dict[str, Any]) -> str:
    """
    Genera recomendaciones de café basadas en preferencias
    
    Args:
        preferences: Diccionario con preferencias de café
        
    Returns:
        Recomendación de café
    """
    system_prompt = """
    Eres un barista experto y catador de café. Tu trabajo es recomendar tipos de café, métodos de
    procesamiento y preparación basados en las preferencias del usuario. Sé específico y
    detallado en tus recomendaciones.
    """
    
    prompt = f"""
    Con base en las siguientes preferencias de café:
    {json.dumps(preferences, indent=2, ensure_ascii=False)}
    
    Por favor, recomienda:
    1. Los tipos de café más adecuados
    2. Métodos de procesamiento recomendados
    3. Sugerencias para la preparación
    4. Posibles maridajes
    """
    
    return generate_response(prompt, system_prompt, temperature=0.6)

def optimize_coffee_pricing(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Optimiza precios de café usando IA
    
    Args:
        data: Datos históricos y actuales de precios y costos
        
    Returns:
        Recomendaciones de precios optimizados
    """
    system_prompt = """
    Eres un analista de datos especializado en la optimización de precios para productos de café.
    Tu objetivo es maximizar la rentabilidad manteniendo precios competitivos.
    Proporciona recomendaciones específicas con valores numéricos precisos.
    """
    
    prompt = f"""
    Analiza los siguientes datos de precios y costos de café:
    {json.dumps(data, indent=2, ensure_ascii=False)}
    
    Proporciona recomendaciones detalladas de precios optimizados para cada tipo de café
    y presentación. Incluye el precio recomendado y la justificación para cada uno.
    Devuelve tus recomendaciones en formato JSON con la estructura: 
    {{"producto": "nombre", "precio_actual": x, "precio_recomendado": y, "justificacion": "razón"}}
    """
    
    response = generate_response(prompt, system_prompt, temperature=0.2)
    
    try:
        # Intentar extraer JSON de la respuesta
        # Buscar contenido entre tres backticks si está en ese formato
        if "```json" in response and "```" in response.split("```json", 1)[1]:
            json_str = response.split("```json", 1)[1].split("```", 1)[0].strip()
        elif "```" in response and "```" in response.split("```", 1)[1]:
            json_str = response.split("```", 1)[1].split("```", 1)[0].strip()
        else:
            json_str = response
            
        return json.loads(json_str)
    except Exception as e:
        logger.error(f"Error al parsear JSON de respuesta de OpenAI: {e}")
        return {"error": str(e), "raw_response": response}
