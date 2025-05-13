# Bot de Telegram para Gestión de Café con OpenAI

Un bot de Telegram completo para gestionar operaciones relacionadas con un negocio de café, desde la compra de café en cereza hasta la venta final, incluyendo procesamiento, control de gastos y análisis inteligente con IA.

![Café Bot](https://img.shields.io/badge/Bot-Telegram-0088cc)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenAI](https://img.shields.io/badge/IA-OpenAI-412991)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)

## 🚀 Características

- ☕ **Gestión de Compras**: Registro detallado de proveedores, cantidad, precio y calidad
- 🔄 **Procesamiento de Café**: Control del flujo desde cereza hasta producto final
- 💰 **Control de Gastos**: Registro categorizado de gastos operativos
- 💼 **Gestión de Ventas**: Registro de clientes, precios y cálculo de utilidades
- 📊 **Reportes Avanzados**: Diarios, semanales y mensuales
- 📦 **Control de Inventario**: Seguimiento del café disponible por estado
- 🤖 **Asistente IA**: Análisis, recomendaciones y respuestas inteligentes con OpenAI
- 📱 **Interfaz de Telegram**: Accesible desde cualquier dispositivo

## 📋 Requisitos

- Python 3.10 o superior
- Cuenta de Telegram
- Token de bot (obtenido a través de [@BotFather](https://t.me/botfather))
- API Key de OpenAI
- Bibliotecas de Python (ver `requirements.txt`)

## 🛠️ Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/sofiaqsy/openai-cafe-bot.git
cd openai-cafe-bot
```

2. **Crear un entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar las variables de entorno**:
   - Copia `.env.example` a `.env`
   - Edita `.env` y añade:
     - Tu token de bot de Telegram
     - Tu API Key de OpenAI
     - Configuración de Google Sheets (opcional)

5. **Ejecutar el bot**:
```bash
python bot.py
```

## 🤖 Uso

1. **Inicia una conversación** con tu bot en Telegram
2. Usa el comando `/start` para comenzar
3. Sigue las instrucciones para cada operación:
   - `/compra` - Registrar compra de café
   - `/proceso` - Registrar procesamiento
   - `/gasto` - Registrar gastos
   - `/venta` - Registrar venta
   - `/reporte` - Ver reportes
   - `/ia` - Acceder a las funcionalidades de IA

## 🧠 Funcionalidades de IA

El bot incluye un asistente inteligente con las siguientes capacidades:

- **Consultas generales**: Responde preguntas sobre café, procesamiento, mercado y mejores prácticas
- **Análisis de datos**: Analiza tus registros para identificar tendencias y oportunidades de mejora
- **Recomendaciones personalizadas**: Sugiere tipos de café y métodos de procesamiento según preferencias
- **Optimización de precios**: Recomienda precios óptimos basados en tus costos y márgenes

Para acceder a estas funciones, usa el comando `/ia` y selecciona la opción deseada.

## 📁 Estructura del Proyecto

```
openai-cafe-bot/
├── bot.py                 # Archivo principal
├── config.py              # Configuraciones
├── handlers/              # Manejadores de comandos
│   ├── compras.py
│   ├── proceso.py
│   ├── gastos.py
│   ├── ventas.py
│   ├── reportes.py
│   └── ia.py              # Manejador de funciones de IA
├── utils/                 # Utilidades
│   ├── db.py              # Manejo de CSV
│   ├── openai.py          # Integración con OpenAI
│   └── sheets.py          # Integración con Google Sheets
└── data/                  # Datos almacenados
    ├── compras.csv
    ├── proceso.csv
    ├── gastos.csv
    └── ventas.csv
```

## 🔄 Flujo de Trabajo

1. **Compra** → 2. **Procesamiento** → 3. **Venta**
   (Con registro de gastos y análisis de IA en cualquier momento)

## 📊 Reportes y Análisis

- **Reportes Básicos**: Histórico, diario, semanal y mensual
- **Análisis de IA**: Tendencias, predicciones y recomendaciones basadas en tus datos

## 🛡️ Control de Inventario

El sistema mantiene un control detallado del café:
- **Pendiente**: Café disponible para procesar
- **Procesado parcialmente**: Parte del lote procesado
- **Procesado completamente**: Lote agotado

## 🤝 Contribuir

Las contribuciones son bienvenidas. Si quieres mejorar este proyecto:
1. Haz un fork del repositorio
2. Crea una rama para tu función: `git checkout -b nueva-funcion`
3. Realiza tus cambios y haz commit: `git commit -m 'Añadir nueva función'`
4. Envía tus cambios: `git push origin nueva-funcion`
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 🙋 Soporte

Si tienes preguntas o problemas, abre un issue en este repositorio.

---

Desarrollado con ☕ y 💙, potenciado con 🧠 IA
