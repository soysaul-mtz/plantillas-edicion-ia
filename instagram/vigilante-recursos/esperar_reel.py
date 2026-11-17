#!/usr/bin/env python3
"""Espera a que Saúl publique un reel nuevo en @tu_usuario y le crea la automatización de Zernio.

Uso:  python3 esperar_reel.py <palabra> "<nombre>" [horas]
Copia el mensaje, botón, candado de "sígueme" y respuestas públicas de la automatización del
reel VIDEO, cambiando solo la palabra clave y el reel. Al crearla, la agrega a recursos.json
para que el vigilante de GitHub también la cuide.
"""
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vigilante import api, fecha  # noqa: E402  (reusa la llave y el cliente)

# IDs de tu cuenta de Zernio: cuenta.json junto a este archivo (ver cuenta.ejemplo.json) o variables de entorno
_C = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cuenta.json"))) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cuenta.json")) else {}
A = os.environ.get("ZERNIO_ACCOUNT_ID") or _C.get("accountId")
PROFILE = os.environ.get("ZERNIO_PROFILE_ID") or _C.get("profileId")
BASE = os.environ.get("ZERNIO_AUTOMATIZACION_BASE") or _C.get("automatizacionBase")  # automatización existente que sirve de plantilla
RECURSOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recursos.json")

palabra, nombre = sys.argv[1], sys.argv[2]
horas = float(sys.argv[3]) if len(sys.argv) > 3 else 6
inicio = datetime.now(timezone.utc) - timedelta(minutes=2)
fin = time.time() + horas * 3600

print(f"Esperando un reel nuevo publicado después de {inicio:%H:%M} UTC…", flush=True)
reel = None
while time.time() < fin and not reel:
    st, r = api("GET", f"/inbox/comments?accountId={A}&limit=5")
    for p in r.get("data", []) if st < 300 else []:
        if p.get("createdTime") and fecha(p["createdTime"]) > inicio:
            reel = p
            break
    if not reel:
        time.sleep(60)

if not reel:
    sys.exit("No apareció ningún reel nuevo en el tiempo de espera.")

print(f"REEL DETECTADO: {reel['permalink']} · {reel['createdTime']}", flush=True)
print("Texto:", (reel.get("content") or "")[:160].replace("\n", " "), flush=True)

_, b = api("GET", f"/comment-automations/{BASE}")
b = b.get("automation", b)
cuerpo = {
    "profileId": PROFILE, "accountId": A, "name": nombre, "trigger": "comment",
    "platformPostId": reel["id"], "postTitle": (reel.get("content") or nombre)[:80],
    "keywords": [palabra], "matchMode": "word",
    "dmMessage": b["dmMessage"], "buttons": b["buttons"],
    "audience": {"followerStatus": "follower", "whenUnknown": "verify"},
    "followGate": b["followGate"],
    "commentReply": b["commentReply"], "commentReplyVariations": b.get("commentReplyVariations", []),
    "publicReplyPolicy": "after_dm", "isActive": True,
}
st, r = api("POST", "/comment-automations", cuerpo)
if st >= 300:
    sys.exit(f"No se pudo crear la automatización: {r}")
nueva = r["automation"]
print(f"AUTOMATIZACIÓN ACTIVA: {nueva['id']} · palabra '{palabra}'", flush=True)

with open(RECURSOS) as f:
    recursos = json.load(f)
base = recursos[0]
recursos.append({**base, "nombre": nombre, "automationId": nueva["id"], "postId": reel["id"],
                 "reel": reel["permalink"]})
with open(RECURSOS, "w") as f:
    json.dump(recursos, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("Agregada a recursos.json", flush=True)
