#!/usr/bin/env python3
"""Vigilante de recursos de @tu_usuario (corre en GitHub Actions cada 30 min).

Zernio manda el mensaje de "sígueme" a quien comenta la palabra clave, pero a veces no
entrega el recurso después. Este script revisa a esas personas y, si ya tocaron
"Ya te sigo ✅" o ya pasó ESPERA_MIN desde su comentario, intenta mandarles el recurso.
Si Meta lo rechaza (normalmente
porque no te sigue), no hace nada y lo vuelve a intentar en la siguiente vuelta.

No guarda estado: antes de enviar revisa la conversación, así que nunca manda dos veces.

Uso:  python3 vigilante.py          (envía de verdad)
      python3 vigilante.py --seco   (solo dice qué haría)
"""
import json
import os

import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://zernio.com/api/v1"
ESPERA_MIN = int(os.environ.get("ESPERA_MIN", "60"))
SECO = "--seco" in sys.argv
VENTANA = timedelta(hours=23)  # Meta no deja escribir después de 24 h


def llave():
    if os.environ.get("ZERNIO_API_KEY"):
        return os.environ["ZERNIO_API_KEY"]
    return subprocess.run(["security", "find-generic-password", "-s", "zernio-api-key", "-w"],
                          capture_output=True, text=True).stdout.strip()


KEY = llave()


def api(metodo, ruta, cuerpo=None, extra=None):
    cabeceras = {"Authorization": "Bearer " + KEY, "Content-Type": "application/json"}
    cabeceras.update(extra or {})
    datos = json.dumps(cuerpo, ensure_ascii=False).encode() if cuerpo is not None else None
    req = urllib.request.Request(API + ruta, data=datos, method=metodo, headers=cabeceras)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.load(e)
        except ValueError:
            return e.code, {"error": str(e)}


def fecha(texto):
    return datetime.fromisoformat(texto.replace("Z", "+00:00"))


def revisar(rec, ahora):
    _, res = api("GET", f"/comment-automations/{rec['automationId']}/logs?status=gated&limit=200")
    for log in res.get("logs", []):
        quien = log.get("commenterUsername") or log.get("commenterId")
        creado = fecha(log["createdAt"])
        edad = ahora - creado
        if edad > VENTANA:
            continue
        conv = log["commenterId"]
        _, m = api("GET", f"/inbox/conversations/{conv}/messages?accountId={rec['accountId']}&limit=50&sortOrder=desc")
        msgs = m.get("messages", [])
        if any(x.get("direction") == "outgoing" and (x.get("message") or "").strip() == rec["dmMessage"]
               for x in msgs):
            continue  # ya tiene el recurso
        toco = any(x.get("direction") == "incoming" and fecha(x["createdAt"]) > creado for x in msgs)
        if not toco and edad < timedelta(minutes=ESPERA_MIN):
            print(f"· @{quien}: esperando ({int(edad.total_seconds() // 60)} min)")
            continue
        motivo = "tocó el botón" if toco else f"pasaron {int(edad.total_seconds() // 60)} min"
        if SECO:
            print(f"· @{quien}: le mandaría el recurso ({motivo})")
            continue
        st, r = api("POST", f"/inbox/conversations/{conv}/messages", {
            "accountId": rec["accountId"], "message": rec["dmMessage"],
            "buttons": [{"type": "url", "title": rec["boton"], "url": rec["url"]}]})
        if st >= 300:
            print(f"✗ @{quien}: Meta no dejó enviar ({motivo}): {str(r.get('error'))[:120]}")
            continue
        # La respuesta pública ya la publica Zernio al mandar el DM (publicReplyPolicy=always).
        print(f"✓ @{quien}: recurso enviado ({motivo})")


def main():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "recursos.json")) as f:
        recursos = json.load(f)
    ahora = datetime.now(timezone.utc)
    for rec in recursos:
        if rec.get("activo", True):
            print(f"== {rec['nombre']}")
            revisar(rec, ahora)


if __name__ == "__main__":
    main()
