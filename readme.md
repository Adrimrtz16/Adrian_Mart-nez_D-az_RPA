# 🚀 Quick Start Guide - RPA Agent
 
Guía rápida para poner en marcha el sistema en 5 minutos.
 
---
 
## ⚡ Instalación Rápida
 
### 1. Clonar o descargar proyecto
 
```bash
cd ADRIAN_MARTINEZ_DIAZ_RPA
```
 
### 2. Crear archivo .env
 
```bash
cat > .env << EOF
MODEL_NAME=gpt-4-turbo
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-your-actual-key-here
EOF
```
 
O manualmente en tu editor favorito.
 
### 3. Instalar dependencias
 
```bash
pip install -r requirements.txt
```
 
O con `uv` (más rápido):
 
```bash
uv pip install -r requirements.txt
```
 
---
 
## 🎯 Los 3 Comandos (Orden Crítico)
 
### Terminal 1: Indexar ChromaDB
 
```bash
python index_procedures.py
```
 
**Salida esperada:**
 
```
Cargando variables de entorno...
Cargando workflows...
Indexando: alta_producto_v1.workflow.json
Indexando: baja_producto_v1.workflow.json
Indexando: actualizar_stock_v1.workflow.json
Creando embeddings...
Eliminando índice anterior (si existe)...
Creando ChromaDB persistente...
 
✔ 3 procedimientos indexados correctamente
✔ Base guardada en: /Users/adrian/project/rag/chroma_db
```
 
**Si ves esto:** ✅ Comando 1 exitoso. Pasa a Comando 2.
 
---
 
### Terminal 2: Levantar Web Server
 
```bash
cd web_form
python server.py
```
 
**Salida esperada:**
 
```
✔ Formulario disponible en http://localhost:8080/index.html
  Pulsa Ctrl+C para detener el servidor.
```
 
**Manténen abierto** y abre Terminal 3.
 
---
 
### Terminal 3: Ejecutar API o CLI
 
#### Opción A: API HTTP (Recomendado para Testing)
 
```bash
fastapi run api.py
```
 
O con Uvicorn explícito:
 
```bash
uvicorn api.py:app --reload --host 0.0.0.0 --port 8000
```
 
**Salida esperada:**
 
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
 
**Accede a:** http://localhost:8000/docs
 
---
 
#### Opción B: CLI Interactiva
 
```bash
python agent/app.py
```
 
**Salida esperada:**
 
```
Agente iniciado. Escribe 'exit' para salir.
 
Tú: 
```
 
---
 
## 📝 Ejemplos de Uso por Caso
 
### Caso 1: Alta de Producto (Completo)
 
#### CLI:
 
```
Tú: Dar de alta un producto llamado Camiseta Negra a 24.99 euros, 100 unidades, categoría camisetas
 
[Agente busca...]
[Agente extrae...]
[Runner abre navegador...]
[Runner ejecuta steps...]
 
Agente: ✔ Producto registrado correctamente. Duración: 2.34s
```
 
#### API HTTP:
 
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Alta de Camiseta Negra a 24.99€, 100 unidades, camisetas"
  }'
```
 
**Response:**
 
```json
{
  "response": "✔ Producto registrado correctamente. Duración: 2.34s"
}
```
 
---
 
### Caso 2: Actualizar Stock
 
#### CLI:
 
```
Tú: Cambiar el stock del producto Pantalón Azul a 50 unidades
 
[Runner ejecuta...]
 
Agente: ✔ Stock actualizado correctamente. Duración: 1.82s
```
 
#### API HTTP:
 
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Modificar stock de Pantalón Azul a 50"
  }'
```
 
---
 
### Caso 3: Eliminar Producto
 
#### CLI:
 
```
Tú: Quiero eliminar el producto Sudadera Roja
 
[Runner ejecuta click + espera confirmación...]
 
Agente: ✔ Producto eliminado correctamente. Duración: 1.56s
```
 
#### API HTTP:
 
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Borrar producto Sudadera Roja"
  }'
```
 
---
 
### Caso 4: Parámetro Incompleto (Loop)
 
#### CLI:
 
```
Tú: Alta de producto Pantalón Gris a 55 euros
 
Agente: Necesito más información.
        ¿Cuántas unidades en stock?
        ¿Qué categoría? (camisetas, sudaderas, pantalones, accesorios)
 
Tú: 60 unidades, pantalones
 
[Runner ejecuta...]
 
Agente: ✔ Procedimiento completado. Duración: 2.51s
```
 
---
 
## 🔍 Inspeccionar Trazas Detalladas
 
### Habilitar Debug Logging
 
En terminal 3 (antes de ejecutar API/CLI):
 
```bash
# Opción A: Variable de entorno
export PYTHONUNBUFFERED=1
 
# Opción B: Agregar en tu script de inicio
python -u agent/app.py  # -u = unbuffered
```
 
### Ver Trazas en API
 
En la terminal donde corre `fastapi run api.py`, verás logs como:
 
```
INFO:     127.0.0.1:57820 "POST /chat HTTP/1.1" 200 OK
```
 
Para más detalles, añade a `api.py`:
 
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
 
---
 
## 🐛 Troubleshooting
 
### Error 1: `FileNotFoundError: rag/chroma_db`
 
```
FileNotFoundError: [Errno 2] No such file or directory: 'rag/chroma_db'
```
 
**Causa:** No ejecutaste `python index_procedures.py`
 
**Solución:**
 
```bash
# En NUEVA terminal
python index_procedures.py
 
# Espera a que termine (✔ 3 procedimientos indexados)
```
 
---
 
### Error 2: `ConnectionRefusedError: [Errno 111] Connection refused`
 
```
ConnectionRefusedError: [Errno 111] Connection refused
```
 
**Causa:** `server.py` no está corriendo
 
**Solución:**
 
```bash
# Abre una segunda terminal
cd web_form
python server.py
 
# Verifica: http://localhost:8080
```
 
---
 
### Error 3: `OPENAI_API_KEY not found`
 
```
KeyError: 'OPENAI_API_KEY'
```
 
**Causa:** Archivo `.env` no existe o está incorrecto
 
**Solución:**
 
```bash
# Crear .env en raíz del proyecto
cat > .env << EOF
MODEL_NAME=gpt-4-turbo
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-your-actual-key-here
EOF
 
# Verifica que está en la carpeta correcta
ls -la .env
```
 
---
 
### Error 4: `Timeout waiting for element`
 
```
TimeoutError: Timeout waiting for ... to be visible
```
 
**Causa:** Selector CSS incorrecto o página no cargó
 
**Solución:**
 
```python
# En runner.py, aumentar timeout
locator.wait_for(
    state="visible",
    timeout=20000  # Aumentar de 10000 a 20000
)
```
 
O revisar selectores en `index.html`:
 
```bash
# Inspeccionar en navegador (F12)
# Verificar que los selectores CSS coincidan:
# - #nombre      ✓
# - #precio      ✓
# - #stock       ✓
# - #categoria   ✓
# - #btn_guardar ✓
# - #toast       ✓
```
 
---
 
### Error 5: `Model not found`
 
```
openai.error.InvalidRequestError: The model 'gpt-4-turbo' does not exist
```
 
**Causa:** Modelo especificado no disponible o credenciales inválidas
 
**Solución:**
 
```bash
# Opción A: Usar modelo más disponible
# En .env
MODEL_NAME=gpt-4o  # o gpt-3.5-turbo
 
# Opción B: Usar LLM local
# En .env
MODEL_NAME=llama2
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=ollama
 
# Requiere Ollama corriendo:
# ollama run llama2
```
 
---
 
### Error 6: `No se encontraron workflows`
 
```
Exception: No se encontraron workflows en /procedures
```
 
**Causa:** Archivos `.workflow.json` no están en carpeta `procedures/`
 
**Solución:**
 
```bash
# Verifica la estructura
ls -la procedures/
# Debería mostrar:
# - alta_producto_v1.workflow.json
# - baja_producto_v1.workflow.json
# - actualizar_stock_v1.workflow.json
 
# Si no existen, copiar desde uploads o crear
cp /mnt/user-data/uploads/*.workflow.json procedures/
```
 
---
 
### Error 7: `Playwright installation missing`
 
```
PlaywrightException: Chromium is not installed
```
 
**Causa:** Playwright no instaló navegadores
 
**Solución:**
 
```bash
# Instalar navegadores Playwright
playwright install
 
# O forzar en código
python -m playwright install chromium
```
 
---
 
## ✅ Verificación del Sistema
 
Ejecuta este script para verificar todo:
 
```bash
#!/bin/bash
 
echo "=== Verificación RPA Agent ==="
echo ""
 
echo "1. Verificar Python"
python --version
echo ""
 
echo "2. Verificar .env"
if [ -f .env ]; then
    echo "✓ .env existe"
    grep OPENAI_API_KEY .env | head -c 30
    echo "..."
else
    echo "✗ .env NO existe"
fi
echo ""
 
echo "3. Verificar procedimientos"
ls -1 procedures/*.workflow.json | wc -l
echo "   procedimientos encontrados"
echo ""
 
echo "4. Verificar ChromaDB"
if [ -d rag/chroma_db ]; then
    echo "✓ ChromaDB indexado"
    ls rag/chroma_db/
else
    echo "✗ ChromaDB NO indexado - ejecutar: python index_procedures.py"
fi
echo ""
 
echo "5. Verificar web_form"
if [ -f web_form/index.html ]; then
    echo "✓ index.html existe"
else
    echo "✗ index.html NO existe"
fi
echo ""
 
echo "=== Resumen ==="
echo "Próximos pasos:"
echo "  Terminal 1: python index_procedures.py"
echo "  Terminal 2: cd web_form && python server.py"
echo "  Terminal 3: fastapi run api.py"
```
 
Guarda como `verify.sh` y ejecuta:
 
```bash
chmod +x verify.sh
./verify.sh
```
 
---
 
## 📊 Monitoreo en Tiempo Real
 
### Ver trazas de agent en CLI
 
Edita `agent/app.py`:
 
```python
import logging
from langchain_core.callbacks import StdOutCallbackHandler
 
# Habilitar callbacks
print("\n[AGENT] Starting with detailed traces...\n")
 
# El agente ya imprime pero puedes agregar más
```
 
### Ver trazas de Playwright
 
Edita `agent/runner.py`:
 
```python
# Agregar en WorkflowRunner._execute_step:
 
print(f"[Step {i}] Type={step_type}")
print(f"  Target: {step.get('target')}")
print(f"  Value: {step.get('value', 'N/A')}")
```
 
### Ver trazas de API HTTP
 
En terminal donde corre fastapi:
 
```bash
# Ya verás logs automáticamente
# Para aún más detalle:
LOGLEVEL=DEBUG fastapi run api.py
```
 
---
 
## 🎮 Modo Headless vs Headed
 
### Ver Navegador Automatizado (Helpful para debugging)
 
En `agent/runner.py`, busca:
 
```python
browser = p.chromium.launch(
    headless=False  # ← Cambiar a False para ver navegador
)
```
 
**Resultado:** Se abre ventana del navegador y ves los clics/fills en tiempo real.
 
### Modo Headless (Rápido, production)
 
```python
browser = p.chromium.launch(
    headless=True  # ← Para invisible (más rápido)
)
```
 
---
 
## 🔄 Desarrollo Iterativo
 
### Después de cambios en code
 
```bash
# Si solo cambias Python (agent, tools, etc.)
# No necesitas re-indexar, solo reinicia terminal 3
 
# Si cambias un procedimiento JSON
python index_procedures.py  # Re-indexar
 
# Si cambias formulario HTML
# Servidor lo sirve automáticamente (refresh página)
```
 
---
 
## 📦 Estructura de Carpetas Esperada
 
```
ADRIAN_MARTINEZ_DIAZ_RPA/
├── .env                    ← CRÍTICO
├── .env.example
├── requirements.txt
├── README.md
├── index_procedures.py     ← Script 1
│
├── agent/
│   ├── __init__.py
│   ├── agent.py            ← Núcleo LangGraph
│   ├── app.py              ← CLI (Script 3B)
│   ├── tools.py            ← Tools
│   └── runner.py           ← Playwright
│
├── procedures/
│   ├── alta_producto_v1.workflow.json
│   ├── baja_producto_v1.workflow.json
│   └── actualizar_stock_v1.workflow.json
│
├── shared/
│   └── templating.py
│
├── rag/
│   └── chroma_db/          ← Generado automáticamente
│       ├── chroma.sqlite3
│       └── ...
│
├── web_form/
│   ├── index.html
│   └── server.py           ← Script 2
│
└── api.py                  ← Script 3A (FastAPI)
```
 
---
 
 
