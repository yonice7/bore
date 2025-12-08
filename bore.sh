#!/bin/bash

# Comando para mostrar qué día es hoy según el calendario bore
# Uso: ./bore

# Archivo JSON con las fechas bore
JSON_FILE="$(dirname "$0")/6025.json"

# Verificar que existe el archivo
if [[ ! -f "$JSON_FILE" ]]; then
    echo "❌ Error: No se encuentra el archivo 6025.json"
    exit 1
fi

# Obtener fecha y hora actual
NOW=$(date +"%Y-%m-%d %H:%M:%S")
ISO_DATE=$(date +"%Y-%m-%d")
CURRENT_HOUR=$(date +"%H")

# Calcular fecha para lookup en bore (después de las 18h = día siguiente)
if [[ $CURRENT_HOUR -ge 18 ]]; then
    LOOKUP_DATE=$(date -v+1d +"%Y-%m-%d")
    echo "📅 Fecha actual según Bore (después del atardecer):"
else
    LOOKUP_DATE=$ISO_DATE
    echo "📅 Fecha actual según Bore:"
fi

# Buscar entrada en el calendario
ENTRY=$(jq -r --arg date "$LOOKUP_DATE" '.[$date] // empty' "$JSON_FILE" 2>/dev/null || echo "")

if [[ -z "$ENTRY" || "$ENTRY" == "null" ]]; then
    # Si no encuentra la fecha bore, probar con la fecha civil
    ENTRY=$(jq -r --arg date "$ISO_DATE" '.[$date] // empty' "$JSON_FILE" 2>/dev/null || echo "")
    if [[ -z "$ENTRY" || "$ENTRY" == "null" ]]; then
        echo "❌ No se encontró información para la fecha $LOOKUP_DATE (bore) ni $ISO_DATE (civil)"
        exit 1
    fi
fi

# Extraer campos del JSON
BORE=$(echo "$ENTRY" | jq -r '.bore // "Unknown"' 2>/dev/null || echo "Unknown")
YEHUDIM=$(echo "$ENTRY" | jq -r '.yehudim // "Unknown"' 2>/dev/null || echo "Unknown")
EVENT=$(echo "$ENTRY" | jq -r '.event // empty' 2>/dev/null || echo "")
NOTE=$(echo "$ENTRY" | jq -r '.note // empty' 2>/dev/null || echo "")
MOON=$(echo "$ENTRY" | jq -r '.moon // empty' 2>/dev/null || echo "")
AVIV=$(echo "$ENTRY" | jq -r '.aviv // empty' 2>/dev/null || echo "")

# Mostrar información
echo "   Bore: $BORE"
echo "   Yehudim: $YEHUDIM"
echo "   Gregorian: $(date +"%A %d %B %Y")"

# Campos opcionales
[[ -n "$EVENT" ]] && echo "   🎉 Evento: $EVENT"
[[ -n "$NOTE" ]] && echo "   📝 Nota: $NOTE"
[[ -n "$MOON" ]] && echo "   🌙 Luna: $MOON"
[[ -n "$AVIV" ]] && echo "   🌾 Aviv: $AVIV"

exit 0