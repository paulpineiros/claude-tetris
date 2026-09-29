---
name: clima
description: Da el clima actual de una ciudad usando la API gratuita de Open-Meteo (sin API key). Por defecto consulta Quito, Ecuador si no se especifica ciudad. Úsala cuando el usuario pregunte "qué clima hace", "cómo está el clima en X", o pida el pronóstico/temperatura de un lugar.
---

# Clima

Consulta el clima actual de cualquier ciudad. Si el usuario no especifica ciudad, usa Quito, Ecuador por defecto.

## Uso

Ejecuta el script con la ciudad como argumento (opcional):

```bash
python3 .claude/skills/clima/scripts/clima.py "Quito, Ecuador"
python3 .claude/skills/clima/scripts/clima.py "Madrid, España"
python3 .claude/skills/clima/scripts/clima.py           # usa Quito por defecto
```

El script geocodifica la ciudad y devuelve: condición, temperatura, sensación térmica, humedad y viento. No requiere API key (usa open-meteo.com).

Reporta el resultado al usuario de forma clara y concisa, en español.
