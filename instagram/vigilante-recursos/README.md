# Vigilante de recursos · @tu_usuario

Corre en GitHub Actions cada 30 min. Revisa a quien comentó la palabra clave y recibió el
mensaje de "sígueme" de Zernio; si ya tocó "Ya te sigo ✅" o pasó 1 hora, le manda el recurso.
Si Meta lo acepta, publica la respuesta pública; si lo rechaza (no te sigue), reintenta hasta 23 h.

- Agregar un video nuevo: un bloque más en `recursos.json`.
- Probar sin enviar nada: `python3 vigilante.py --seco` (en la Mac toma la llave del Llavero).
- La llave de Zernio vive en el secreto `ZERNIO_API_KEY` del repo.
