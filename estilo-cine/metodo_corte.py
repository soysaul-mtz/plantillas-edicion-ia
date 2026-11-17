"""Corte de un tutorial "cámara + pantalla" (formato Metodología): toma los tramos elegidos de la cámara,
quita las pausas internas y saca el mismo tramo de la grabación de pantalla, sincronizado por audio.

Uso: python3 estilo-cine/metodo_corte.py proyectos/<n>
Lee proyectos/<n>/metodo.json:
  { "camara": "...C8260.MP4", "pantalla": "...mov", "words": "corte/words.json",
    "tramos": [[a, b], [a, b, "sin", c, d], ...],   # tiempos de la cámara; "sin" quita [c, d] dentro del tramo
    "recorte": {"w": 2600, "cx": 0.5, "y": 100} }    # recorte de la cámara 4K para el panel de arriba (1080x768)
  "recorte": {"vertical": true, "vf": "crop=…,scale=1080:1920"}  # filtro propio para llegar a 1080x1920 (toma horizontal o 3:4)
Escribe corte/cam.mov (1080x768 + audio), corte/scr.mov (1920x1080) y corte/mapa.json.
Con "perfil": "4k" y recorte vertical, además escribe corte/cam_4k.mov (2160x3840, sin audio) con exactamente los mismos
cortes: se edita todo sobre cam.mov (copia ligera) y cam_4k.mov solo se usa en el render final (prep4k.py).
"""
import sys, os, json, subprocess
import numpy as np

proy = sys.argv[1]
cfg = json.load(open(os.path.join(proy, 'metodo.json')))
# video HDR (iPhone en HLG/Dolby Vision, DJI en HLG): sin mapeo de tonos sale lavado y con color feo. Se pasa una vez a SDR Rec.709
# con bin/sdr (mapeo de tonos de macOS, lo mismo que hace CapCut al importar) y se corta de esa copia (5 nov 2026)
def a_sdr(src):
    tr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=color_transfer', '-of', 'csv=p=0', src],
                        capture_output=True, text=True).stdout.strip().strip(',')
    if tr not in ('arib-std-b67', 'smpte2084'): return src
    dst = os.path.join(proy, 'corte', '_sdr_' + os.path.splitext(os.path.basename(src))[0] + '.mov')
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True); print(f'HDR ({tr}) → Rec.709: {os.path.basename(src)}', flush=True)
        subprocess.run([os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bin', 'sdr'), src, dst], check=True)
    return dst
# copia de trabajo (6 nov 2026): un video VERTICAL más grande que 1080 (4K de celular o de cámara) se baja UNA vez a 1080x1920 al empezar
# (con el chip de video en Mac) y cada vuelta de `cortar` lee esa copia ligera en vez del 4K: leer 4K era el paso más lento (4.5 min con
# 3 min de crudo). El video final es 1080 de todos modos. Si además es HDR, el paso a color normal se hace en la misma pasada.
def copia_trabajo(src):
    import time
    s = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,color_transfer:stream_side_data=rotation',
                                   '-of', 'json', src], capture_output=True, text=True).stdout or '{}').get('streams', [{}])[0]
    w, h, tr = s.get('width', 0), s.get('height', 0), s.get('color_transfer', '')
    if any(abs(int(d.get('rotation', 0))) in (90, 270) for d in s.get('side_data_list', [])): w, h = h, w
    R0 = cfg.get('recorte', {}); hdr = tr in ('arib-std-b67', 'smpte2084')
    chico = bool(R0.get('vertical')) and not R0.get('vf') and cfg.get('perfil') != '4k' and h > w and min(w, h) > 1080
    if not hdr and not chico: return src
    dst = os.path.join(proy, 'corte', ('_trabajo1080_' if chico else '_sdr_') + os.path.splitext(os.path.basename(src))[0] + '.mov')
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src): return dst
    os.makedirs(os.path.dirname(dst), exist_ok=True); t0 = time.time()
    print(f"copia de trabajo: {os.path.basename(src)} {w}x{h}{' HDR → Rec.709' if hdr else ''}{' → 1080x1920 (una sola vez)' if chico else ''}", flush=True)
    if hdr: subprocess.run([os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bin', 'sdr'), src, dst] + (['1080', '1920'] if chico else []), check=True)
    else:
        mac = sys.platform == 'darwin'
        subprocess.run(['ffmpeg', '-v', 'error', '-y'] + (['-hwaccel', 'videotoolbox'] if mac else []) + ['-i', src, '-vf', 'scale=1080:1920:flags=lanczos'] +
                       (['-c:v', 'h264_videotoolbox', '-b:v', '25M'] if mac else ['-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast']) +
                       ['-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', dst + '.tmp.mov'], check=True)
        os.replace(dst + '.tmp.mov', dst)
    print(f"  lista en {time.time() - t0:.0f} s: el resto del corte lee la copia ligera", flush=True)
    return dst
cfg['camara'] = copia_trabajo(cfg['camara'])
words = json.load(open(os.path.join(proy, cfg.get('words', 'corte/words.json'))))
FPS = '24000/1001'
PAUSA, ANTES, DESPUES = .32, .08, .14


def lee_audio(f, ss=0, t=None, sr=8000):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', f] + (['-t', str(t)] if t else []) + ['-ac', '1', '-ar', str(sr), '-f', 's16le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.int16).astype(float)


# ---- desfase pantalla = cámara + lag (envolvente en todo el archivo y luego fino en 40 s) ----
def env(x):
    e = np.sqrt(np.convolve(x ** 2, np.ones(400) / 400, 'same'))[::80]
    e = np.log(e + 1); return (e - e.mean()) / e.std()

if not cfg.get('pantalla'):
    lag = 0
elif 'lag' in cfg:
    lag = cfg['lag']
else:
    ec, es = env(lee_audio(cfg['camara'])), env(lee_audio(cfg['pantalla']))
    n = len(ec) + len(es); c = np.fft.irfft(np.fft.rfft(es, n) * np.conj(np.fft.rfft(ec, n)), n)
    i = int(np.argmax(c)); lag = (i if i < n // 2 else i - n) / 100
    t0 = 60.0  # afinar a nivel de muestra
    a = lee_audio(cfg['camara'], t0, 40); b = lee_audio(cfg['pantalla'], t0 + lag - 1, 42)
    cc = np.correlate(b, a, 'valid'); lag = lag - 1 + int(np.argmax(cc)) / 8000
print(f'desfase pantalla = cámara {lag:+.3f} s')

# ---- tramos → subtramos sin pausas largas ----
piezas = []
for tr in cfg['tramos']:
    a, b = tr[0], tr[1]
    if 'entero' in tr: piezas.append([a, b, 'entero']); continue  # tramo de una sola pieza: no se parte en las pausas cortas (evita tomas de 0.2 s)
    quita = [(tr[i + 1], tr[i + 2]) for i in range(2, len(tr), 3) if tr[i] == 'sin']
    ws = [w for w in words if w['e'] > a + .1 and w['e'] <= b + .05 and not any(q0 <= w['s'] < q1 for q0, q1 in quita)]
    if not ws: continue
    ini = ws[0]
    for w0, w1 in zip(ws, ws[1:] + [None]):
        if w1 is None or w1['s'] - w0['e'] > PAUSA or any(w0['e'] <= q0 < w1['s'] + .01 for q0, _ in quita):
            fin = w0['e'] + DESPUES
            for q0, _ in quita:
                if w0['e'] <= q0 + .05: fin = min(fin, q0)
            if w1 is None: fin = min(max(fin, b) if b - w0['e'] < .35 else fin, b + .03)  # fin dado un poco después de la palabra: respetarlo (cola de la sílaba); nunca llevarse la que sigue
            ini_t = (a if ws[0]['s'] - a > .35 else max(a, ini['s'] - ANTES)) if ini is ws[0] else ini['s'] - ANTES  # si Whisper ubicó tarde la 1ª palabra, respetar el inicio dado
            piezas.append([ini_t, fin])
            ini = w1
# Whisper estira las palabras sobre los silencios: partir además por silencio real del audio (10 ms)
voz = lee_audio(cfg['camara'])
def parte(a, b):
    x = voz[int(a * 8000):int(b * 8000)]; h = 80
    e = 20 * np.log10(np.array([np.sqrt((x[i:i + h] ** 2).mean()) for i in range(0, len(x) - h, h)]) / 32768 + 1e-9)
    if not len(e): return [[a, b]]
    sil = e < np.percentile(e, 90) - 24; out, i0, i = [], 0, 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j < len(sil) and sil[j]: j += 1
            if (j - i) * .01 > PAUSA and i > 0 and j < len(sil):
                out.append([a + i0 * .01, a + i * .01 + DESPUES]); i0 = max(i0, j - int(ANTES / .01))
            i = j
        else: i += 1
    out.append([a + i0 * .01, b]); return out
piezas = [q for p in piezas for q in ([p[:2]] if len(p) > 2 else parte(*p))]
# AJUSTE FINO POR ENERGÍA (5 nov 2026): los tiempos de palabra de Whisper fallan por décimas y dejaban (1) silencio de 0.4–0.7 s al inicio de una toma y
# (2) finales de palabra truncados («ganadores» → «ganado»). Cada borde se corrige con el nivel REAL de la voz: el inicio sube hasta donde empieza el
# sonido (menos 0.10 s) y el final se alarga mientras la voz siga sonando (más 0.06 s de cola) o se recorta si ya hay silencio largo.
_e = 20 * np.log10(np.sqrt((voz[:len(voz) // 80 * 80].reshape(-1, 80) ** 2).mean(axis=1)) / 32768 + 1e-9)
_thr = max(np.percentile(_e, 90) - cfg.get('umbral_rel', 27), np.percentile(_e, 10) + 12)   # metodo.json › umbral_rel: dB bajo la voz fuerte que cuentan como silencio (27 por defecto; 22 = más estricto, quita también la respiración)
def _fr(t): return int(max(0, min(len(_e) - 1, round(t * 100))))
def afina(a, b, entero=False):
    i = _fr(a)
    if _e[i] < _thr:                                           # empieza en silencio: subir hasta el primer sonido (máx. 1.0 s)
        j = i
        while j < _fr(b) and j - i < 100 and _e[j] < _thr: j += 1
        if _e[min(len(_e) - 1, j)] >= _thr and (j - i) * .01 > .12: a = max(a, j * .01 - .10)
    else:                                                      # ya hay voz en el borde (palabra cortada): retroceder hasta un hueco (máx. 0.30 s)
        j = i
        while j > 0 and i - j < 30 and _e[j] >= _thr: j -= 1
        if _e[j] < _thr: a = max(0, min(a, j * .01 + .02))
    k = _fr(b)
    if _e[k] >= _thr:                                          # sigue sonando al final: alargar hasta que calle (máx. 0.40 s)
        j = k
        while j < len(_e) - 1 and j - k < 40 and _e[j] >= _thr: j += 1
        if _e[j] < _thr: b = max(b, j * .01 + .06)
    else:                                                      # silencio al final: recortar a la última voz + cola
        j = k
        while j > _fr(a) and _e[j] < _thr: j -= 1
        if (k - j) * .01 > .22: b = min(b, j * .01 + .14)
    return a, b
piezas = [list(afina(p[0], p[1])) for p in piezas]
# una toma corta (< 0.35 s) donde casi no hay voz es una toma fantasma (silencio, respiración): se elimina
def _hay_voz(a, b): return bool((_e[_fr(a):max(_fr(a) + 1, _fr(b))] >= _thr + 2).any())
_antes = len(piezas); piezas = [p for p in piezas if (p[1] - p[0]) >= .35 or _hay_voz(p[0], p[1])]
if len(piezas) < _antes: print(f'  quité {_antes - len(piezas)} toma(s) fantasma sin voz', flush=True)
# que no se encimen
for p, q in zip(piezas, piezas[1:]):
    if p[1] > q[0] and q[0] > p[0]: p[1] = q[0] = (p[1] + q[0]) / 2
tot = sum(b - a for a, b in piezas)
print(f'{len(piezas)} piezas · {tot:.1f} s')

R = cfg.get('recorte', {}); rw = R.get('w', 2600); ALTO = R.get('alto', 768); rh = round(rw * ALTO / 1080)
rx = round(3840 * R.get('cx', .5) - rw / 2); rx = max(0, min(3840 - rw, rx)); ry = R.get('y', 100)

def corta(src, salida, desfase, vf, con_audio, vf4=None):
    fc, ins = [], []
    for k, (a, b) in enumerate(piezas):
        fc.append(f'[0:v]trim={a + desfase:.4f}:{b + desfase:.4f},setpts=PTS-STARTPTS,fps={FPS}[v{k}]')
        if con_audio: fc.append(f'[0:a]atrim={a + desfase:.4f}:{b + desfase:.4f},asetpts=PTS-STARTPTS,aresample=48000[a{k}]')
        ins.append(f'[v{k}]' + (f'[a{k}]' if con_audio else ''))
    fc.append(''.join(ins) + f'concat=n={len(piezas)}:v=1:a={1 if con_audio else 0}' + ('[vc][a]' if con_audio else '[vc]'))
    fc.append(f'[vc]split=2[x][y];[x]{vf}[v];[y]{vf4}[v4]' if vf4 else f'[vc]{vf}[v]')
    f = os.path.join(proy, 'corte', '_fc.txt'); open(f, 'w').write(';\n'.join(fc))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', src, '-/filter_complex', f, '-map', '[v]'] + (['-map', '[a]', '-c:a', 'pcm_s16le'] if con_audio else []) + \
          ['-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', salida] + \
          (['-map', '[v4]', '-c:v', ('h264_videotoolbox' if sys.platform == 'darwin' else 'libx264'), '-b:v', '60M', '-pix_fmt', 'yuv420p', '-an', salida.replace('.mov', '_4k.mov')] if vf4 else [])
    subprocess.run(cmd, check=True)

os.makedirs(os.path.join(proy, 'corte'), exist_ok=True)
K4 = cfg.get('perfil') == '4k' and R.get('vertical')
if cfg.get('perfil') == '4k' and not R.get('vertical'): print('⚠ el perfil 4K solo aplica a cámara vertical (recorte.vertical); se corta en 1080')
corta(cfg['camara'], os.path.join(proy, 'corte', 'cam.mov'), 0, R['vf'] if R.get('vf') else 'scale=1080:1920' if R.get('vertical') else f'crop={rw}:{rh}:{rx}:{ry},scale=1080:{ALTO}', True,
      'scale=2160:3840:flags=lanczos' if K4 else None)
if cfg.get('pantalla'): corta(cfg['pantalla'], os.path.join(proy, 'corte', 'scr.mov'), lag, 'scale=1920:1080', False)
json.dump({'lag': lag, 'piezas': piezas}, open(os.path.join(proy, 'corte', 'mapa.json'), 'w'))
print('✓ corte/cam.mov + corte/scr.mov')
