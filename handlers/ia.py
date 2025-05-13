"""
Manejadores para comandos relacionados con IA y OpenAI
"""

import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    CallbackQueryHandler,
    ConversationHandler
)

from utils.openai import (
    generate_response, 
    analyze_coffee_data, 
    generate_coffee_recommendation,
    optimize_coffee_pricing
)
from utils.db import get_all_records
from config import COMPRAS_FILE, PROCESO_FILE, VENTAS_FILE, GASTOS_FILE, openai_configured

# Estados para la conversación
AWAIT_QUESTION, AWAIT_PREFERENCES, AWAIT_OPTIMIZATION_DATA = range(3)

# Configuración de logging
logger = logging.getLogger(__name__)

async def ia_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Manejador para el comando /ia - Muestra opciones de IA"""
    if not openai_configured:
        await update.message.reply_text(
            "⚠️ La integración con OpenAI no está configurada. "
            "Por favor configura OPENAI_API_KEY en las variables de entorno."
        )
        return ConversationHandler.END
    
    keyboard = [
        [InlineKeyboardButton("💬 Consulta IA", callback_data="ia_consulta")],
        [InlineKeyboardButton("📊 Análisis de datos", callback_data="ia_analisis")],
        [InlineKeyboardButton("☕ Recomendación de café", callback_data="ia_recomendacion")],
        [InlineKeyboardButton("💰 Optimización de precios", callback_data="ia_precios")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="ia_cancelar")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 *Asistente de IA para café*\n\n"
        "Selecciona una opción para utilizar las capacidades de IA:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return AWAIT_QUESTION

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja los callbacks de los botones de opciones de IA"""
    query = update.callback_query
    await query.answer()
    
    choice = query.data
    
    if choice == "ia_cancelar":
        await query.edit_message_text("Operación cancelada.")
        return ConversationHandler.END
    
    elif choice == "ia_consulta":
        await query.edit_message_text(
            "💬 *Consulta de IA*\n\n"
            "Escribe tu pregunta sobre café, procesamiento, ventas o cualquier "
            "tema relacionado con la industria del café:",
            parse_mode="Markdown"
        )
        context.user_data["ia_mode"] = "consulta"
        return AWAIT_QUESTION
    
    elif choice == "ia_analisis":
        await query.edit_message_text(
            "📊 *Análisis de datos*\n\n"
            "Estoy analizando tus datos de café...",
            parse_mode="Markdown"
        )
        
        # Recopilar datos para análisis
        try:
            compras = get_all_records(COMPRAS_FILE)
            procesos = get_all_records(PROCESO_FILE)
            ventas = get_all_records(VENTAS_FILE)
            gastos = get_all_records(GASTOS_FILE)
            
            data = {
                "compras": compras[-50:] if len(compras) > 50 else compras,  # Últimas 50 compras
                "procesos": procesos[-50:] if len(procesos) > 50 else procesos,
                "ventas": ventas[-50:] if len(ventas) > 50 else ventas,
                "gastos": gastos[-50:] if len(gastos) > 50 else gastos
            }
            
            # Generar análisis
            analysis = analyze_coffee_data(data)
            
            await query.edit_message_text(
                f"📊 *Análisis de datos*\n\n{analysis}",
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error al analizar datos: {e}")
            await query.edit_message_text(
                f"Lo siento, ocurrió un error al analizar los datos: {str(e)}"
            )
        
        return ConversationHandler.END
    
    elif choice == "ia_recomendacion":
        await query.edit_message_text(
            "☕ *Recomendación de café*\n\n"
            "Para ayudarte con una recomendación personalizada, por favor describe "
            "tus preferencias de café. Puedes incluir:\n"
            "- Nivel de acidez preferido\n"
            "- Intensidad deseada\n"
            "- Notas de sabor favoritas\n"
            "- Método de preparación\n"
            "- Cualquier otra preferencia relevante",
            parse_mode="Markdown"
        )
        context.user_data["ia_mode"] = "recomendacion"
        return AWAIT_PREFERENCES
    
    elif choice == "ia_precios":
        await query.edit_message_text(
            "💰 *Optimización de precios*\n\n"
            "Para ayudarte a optimizar tus precios, necesito información sobre "
            "tus productos de café y sus precios actuales. Por favor, proporciona "
            "los detalles en formato de lista:\n\n"
            "Producto: [nombre]\n"
            "Precio actual: [precio]\n"
            "Costo: [costo]\n"
            "Margen deseado: [porcentaje]\n\n"
            "Repite este formato para cada producto.",
            parse_mode="Markdown"
        )
        context.user_data["ia_mode"] = "precios"
        return AWAIT_OPTIMIZATION_DATA
    
    return ConversationHandler.END

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja una pregunta del usuario para la IA"""
    user_question = update.message.text
    
    await update.message.reply_text("🤔 Procesando tu consulta...")
    
    # Sistema de prompts específicos para café
    system_prompt = """
    Eres un experto en la industria del café con conocimientos profundos sobre 
    cultivo, procesamiento, tostado, preparación y comercialización de café.
    Proporciona respuestas detalladas, precisas y orientadas a la práctica.
    Incluye referencias a mejores prácticas de la industria cuando sea relevante.
    """
    
    try:
        response = generate_response(user_question, system_prompt)
        
        await update.message.reply_text(
            f"☕ *Respuesta:*\n\n{response}",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error al generar respuesta: {e}")
        await update.message.reply_text(
            f"Lo siento, ocurrió un error al procesar tu consulta: {str(e)}"
        )
    
    # Preguntar si quiere hacer otra consulta
    keyboard = [
        [InlineKeyboardButton("Nueva consulta", callback_data="ia_consulta")],
        [InlineKeyboardButton("Terminar", callback_data="ia_cancelar")]
    ]
    
    await update.message.reply_text(
        "¿Deseas hacer otra consulta?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return AWAIT_QUESTION

async def handle_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja las preferencias del usuario para recomendaciones de café"""
    preferences_text = update.message.text
    
    await update.message.reply_text("☕ Analizando tus preferencias...")
    
    # Convertir texto a formato de diccionario
    preferences = {
        "preferencias_usuario": preferences_text,
        "contexto": "Negocio de café buscando recomendaciones para ofrecer a clientes"
    }
    
    try:
        recommendations = generate_coffee_recommendation(preferences)
        
        await update.message.reply_text(
            f"☕ *Recomendaciones personalizadas:*\n\n{recommendations}",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error al generar recomendaciones: {e}")
        await update.message.reply_text(
            f"Lo siento, ocurrió un error al generar recomendaciones: {str(e)}"
        )
    
    return ConversationHandler.END

async def handle_optimization_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja los datos de optimización de precios"""
    pricing_data_text = update.message.text
    
    await update.message.reply_text("💰 Analizando datos de precios...")
    
    # Intentar estructurar los datos del texto
    try:
        # Conversión básica (podría mejorarse con regex para una estructura más precisa)
        lines = pricing_data_text.split('\n')
        products = []
        current_product = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("Producto:"):
                if current_product and "producto" in current_product:
                    products.append(current_product)
                current_product = {}
                current_product["producto"] = line.replace("Producto:", "").strip()
            elif line.startswith("Precio actual:"):
                try:
                    current_product["precio_actual"] = float(line.replace("Precio actual:", "").strip())
                except ValueError:
                    pass
            elif line.startswith("Costo:"):
                try:
                    current_product["costo"] = float(line.replace("Costo:", "").strip())
                except ValueError:
                    pass
            elif line.startswith("Margen deseado:"):
                try:
                    current_product["margen"] = float(line.replace("Margen deseado:", "").replace("%", "").strip())
                except ValueError:
                    pass
        
        # Añadir el último producto
        if current_product and "producto" in current_product:
            products.append(current_product)
        
        # Si no hay productos, lanzar excepción
        if not products:
            raise ValueError("No se pudieron extraer datos de productos del texto proporcionado")
            
        # Obtener recomendaciones de precios
        pricing_data = {"productos": products}
        optimization_result = optimize_coffee_pricing(pricing_data)
        
        # Formatear respuesta
        response = "💰 *Precios optimizados recomendados:*\n\n"
        
        if "error" in optimization_result:
            raise ValueError(optimization_result["error"])
            
        # Verificar si es una lista o un objeto
        items = optimization_result
        if not isinstance(optimization_result, list):
            items = [optimization_result]
            
        for item in items:
            response += f"*{item.get('producto', 'Producto')}*\n"
            response += f"📈 Precio actual: ${item.get('precio_actual', 'N/A')}\n"
            response += f"✅ Precio recomendado: ${item.get('precio_recomendado', 'N/A')}\n"
            response += f"📝 Justificación: {item.get('justificacion', 'No disponible')}\n\n"
        
        await update.message.reply_text(response, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Error en la optimización de precios: {e}")
        await update.message.reply_text(
            f"Lo siento, ocurrió un error al procesar los datos de precios: {str(e)}\n\n"
            "Por favor, asegúrate de seguir el formato especificado."
        )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela la conversación"""
    await update.message.reply_text("Operación cancelada.")
    return ConversationHandler.END

def register_ia_handlers(application):
    """Registra los manejadores relacionados con IA"""
    
    # Verificar si OpenAI está configurado
    if not openai_configured:
        logger.warning("OpenAI no está configurado. Las funcionalidades de IA estarán limitadas.")
    
    # Crear un manejador de conversación para IA
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("ia", ia_command)],
        states={
            AWAIT_QUESTION: [
                CallbackQueryHandler(button_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)
            ],
            AWAIT_PREFERENCES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_preferences)
            ],
            AWAIT_OPTIMIZATION_DATA: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_optimization_data)
            ],
        },
        fallbacks=[CommandHandler("cancelar", cancel)]
    )
    
    application.add_handler(conv_handler)
