"""Escaletas de los anuncios del webinar de Jorge (seminario "De emprendedor a empresario digital"), en formato cine.json.
Cada línea de texto consume, en orden, las palabras de voz/palabras.json ("oye|se_ve" cambia lo que se lee).
"""

INVITA = {"dia": "JUEVES", "hora": "8 PM", "titulo": "Clase en vivo", "sub": "Gratis · jueves 8:00 pm"}
inv = lambda en, flecha=None, fin=999: {**INVITA, "en": en, "fin": fin, **({"flecha": flecha} if flecha else {})}

VIDEOS = {}

# ---------- IMG_2040: "La IA te quita la hoja en blanco" ----------
VIDEOS["2040"] = {"abajo_oscuro": True, "cortesFx": False, "escenas": [
    # Jorge enseña el celular: acercamiento a la mano y el chat corriendo DENTRO de la pantalla (rastreada cuadro por cuadro,
    # tel/quads_final.json); antes era una interfaz a pantalla completa (Saúl, 5 nov)
    {"visual": "celularIA", "tema": "oscuro",
     "tel": {"escribe1": 1.9, "envia1": 3.35, "ideas": 4.7, "escribe2": 6.75, "envia2": 7.75, "guion": 8.0,
             "mensaje1": "Tengo una taquería y quiero vender más con redes. ¿Qué videos hago?",
             "ideasLista": ["Así preparamos el pastor desde las 6 am", "Tu orden lista en 60 segundos", "El taco que más piden",
                            "Clientes probando su primer bocado", "Martes de 2x1: cómo llegar"],
             "mensaje2": "Escríbeme el guion del video 1 y el texto del anuncio.",
             "guionTexto": ["Gancho: «Son las 6 am y el trompo ya está girando…»", "Escena 1: el taquero cortando el pastor.",
                            "Escena 2: el primer cliente probando su taco.", "Anuncio: ¿Antojo de pastor? 🌮 Hoy 2x1."]},
     "grupos": [
         {"y": .775, "lineas": ["-Mira esto,", "le digo que|qué negocio tengo"]},
         {"y": .775, "lineas": ["-y que|qué es lo que", "quiero hacer."]},
         {"y": .775, "lineas": ["-y aquí están", "5 ideas de contenido."]},
         {"y": .775, "lineas": ["-ahora le pido", "el guion del primero"]},
         {"y": .775, "lineas": ["-y el texto para", "el anuncio."]}]},
    {"visual": "persona", "tema": "claro",
     "grupos": [
         {"y": .2, "lineas": ["-Esto no reemplaza lo que", "tu|tú ya sabes de tu negocio."]}]},
    {"visual": "persona", "tema": "claro", "hoja": {"en": 12.79, "llena": 13.81, "fin": 17.04},
     "grupos": [
         {"y": .2, "lineas": ["-te quita la", "*hoja en blanco"]},
         {"y": .2, "lineas": ["-y lo que falta es", "saber que|qué hacer con esto"]}]},
    {"visual": "persona", "tema": "claro",
     "chips": {"items": [{"en": 17.58, "icono": "📲", "texto": "Publicarlo"}, {"en": 18.68, "icono": "📣", "texto": "Convertirlo en anuncio"},
                         {"en": 21.09, "icono": "🎯", "texto": "A quién mostrárselo"}], "junta": 21.61, "fin": 22.04},
     "grupos": [
         {"y": .2, "lineas": ["-como|cómo", "publicarlo,"]},
         {"y": .2, "lineas": ["-como|cómo convertirlo", "en anuncio"]},
         {"y": .2, "lineas": ["-pero sobre todo", "a quien|quién mostrárselo"]}]},
    {"visual": "persona", "tema": "claro", "invita": inv(24.4),
     "grupos": [
         {"y": .76, "lineas": ["-y esto es justo", "lo que te enseño"]},
         {"y": .76, "lineas": ["-en una clase", "totalmente de Gravity's|gratis_este"]},
         {"y": .76, "lineas": ["-jueves", "8 de la noche"]}]},
    {"visual": "persona", "tema": "claro", "invita": inv(24.4),
     "chips": {"items": [{"en": 29.3, "icono": "📱", "texto": "Redes sociales"}, {"en": 30.69, "icono": "🤖", "texto": "Inteligencia artificial"},
                         {"en": 33.17, "icono": "🧠", "texto": "Mentalidad correcta"}], "junta": 35.4, "fin": 35.79},
     "grupos": [
         {"y": .76, "lineas": ["-donde vamos a", "aprender"]},
         {"y": .76, "lineas": ["-de redes sociales,", "de inteligencia artificial,"]},
         {"y": .76, "lineas": ["-pero sobre todo, cuál es", "la mentalidad correcta"]},
         {"y": .76, "lineas": ["-para tener un", "negocio en línea."]}]},
    {"visual": "persona", "tema": "claro", "textoTema": "oscuro", "invita": inv(24.4, flecha=37.92),
     "grupos": [
         {"y": .66, "lineas": ["-Para inscribirte", "lo único que tienes que hacer"]},
         {"y": .66, "lineas": ["-es darle clic en el botón", "que está aquí abajo."]}]},
]}

# ---------- IMG_2038: "No necesitas haber nacido con un celular en la mano" ----------
VIDEOS["2038"] = {"cortesFx": False, "escenas": [  # Saúl 5 nov: menos transiciones, solo entrar/salir de redes + IA
    {"visual": "persona", "tema": "claro", "golpe": 0.98,
     "pregunta": {"en": 3.29, "fin": 6.75, "texto": "Jorge, eso de las redes sociales ya no es para mí 😩", "y": 1180},
     "grupos": [
         {"y": .16, "lineas": ["-Mucha gente de", "40, 50 años"]},
         {"y": .16, "lineas": ["-me dice, Jorge,", "eso de las redes sociales"]},
         {"y": .16, "lineas": ["-ya no es", "para mí."]}]},
    {"visual": "persona", "tema": "claro",
     "chips": {"items": [{"en": 15.62, "icono": "🤝", "texto": "Persona a persona"}, {"en": 17.52, "icono": "🗣️", "texto": "Referidos"},
                         {"en": 18.52, "icono": "🥂", "texto": "Networking"}, {"en": 19.34, "icono": "⭐", "texto": "Recomendación"}], "junta": 19.91, "fin": 20.23},
     "grupos": [
         {"y": .16, "lineas": ["-A ver, yo no empecé", "con redes sociales,"]},
         {"y": .16, "lineas": ["-yo tengo", "*7 empresas"]},
         {"y": .16, "lineas": ["-y hasta antes de construir", "redes sociales,"]},
         {"y": .16, "lineas": ["-todo lo que sabía", "a través de las ventas era"]},
         {"y": .16, "lineas": ["-persona", "a persona,"]},
         {"y": .16, "lineas": ["-referidos,", "networking, recomendación."]}]},
    {"visual": "redesIA", "tema": "oscuro", "trans": "zoom",
     "red": {"redes": 21.22, "ia": 22.0, "pauta": 23.38, "auto": 23.88},
     "grupos": [
         {"y": .7, "lineas": ["-Lo que tiene que ver con", "redes, inteligencia artificial,"]},
         {"y": .7, "lineas": ["-pauta,", "automatización,"]}]},
    {"visual": "persona", "tema": "claro", "trans": "zoom",
     "grupos": [{"y": .76, "lineas": ["-son competencias que aprendí", "*ya de adulto."]}]},
    {"visual": "persona", "tema": "claro",
     "grupos": [
         {"y": .76, "lineas": ["-Y déjame decirte una cosa", "con mucho respeto"]},
         {"y": .76, "lineas": ["-si estás viendo", "este video:"]},
         {"y": .76, "lineas": ["-No se necesita", "haber nacido"]},
         {"y": .76, "lineas": ["-con un", "celular en la mano."]}]},
    {"visual": "persona", "tema": "claro",
     "chips": {"items": [{"en": 36.4, "icono": "🧑‍🏫", "texto": "Un mentor"}, {"en": 38.32, "icono": "🔢", "texto": "En el orden correcto"}],
               "junta": 39.13, "fin": 39.45, "alterna": False},
     "grupos": [
         {"y": .16, "lineas": ["-Se necesita que", "una persona,"]},
         {"y": .16, "lineas": ["-un mentor,", "te explique"]},
         {"y": .16, "lineas": ["-en el", "*orden correcto."]}]},
    {"visual": "persona", "tema": "claro",
     "versus": {"en": 39.7, "b": 43.54, "fin": 45.13, "a": "Tu experiencia", "bTexto": "Usar una app"},
     "grupos": [
         {"y": .16, "lineas": ["-La experiencia que", "tú hoy ya tienes"]},
         {"y": .16, "lineas": ["-en tu negocio", "*vale más"]},
         {"y": .16, "lineas": ["-que saber utilizar", "una aplicación."]}]},
    {"visual": "persona", "tema": "claro", "invita": inv(46.66),
     "grupos": [
         {"y": .76, "lineas": ["-Pero aún así,", "este próximo jueves"]},
         {"y": .76, "lineas": ["-a las", "8 de la noche,"]},
         {"y": .76, "lineas": ["-te quiero invitar", "a una clase en vivo"]}]},
    {"visual": "persona", "tema": "claro", "invita": inv(46.66),
     "chips": {"items": [{"en": 52.22, "icono": "📱", "texto": "Redes sociales"}, {"en": 52.7, "icono": "🤖", "texto": "Inteligencia artificial"},
                         {"en": 53.3, "icono": "🎯", "texto": "Pauta"}, {"en": 53.6, "icono": "⚙️", "texto": "Automatización"}], "junta": 54.86, "fin": 55.3},
     "grupos": [
         {"y": .76, "lineas": ["-donde vas a aprender", "a utilizar todas"]},
         {"y": .76, "lineas": ["-estas herramientas", "y mucho más."]}]},
    {"visual": "persona", "tema": "claro", "textoTema": "oscuro", "invita": inv(46.66, flecha=57.82),
     "grupos": [
         {"y": .66, "lineas": ["-Para registrarte,", "lo único que tienes que hacer"]},
         {"y": .66, "lineas": ["-es darle clic en el botón", "que está aquí abajo."]}]},
]}

# ---------- IMG_2041: "El anuncio no es el primer paso" ----------
VIDEOS["2041"] = {"cortesFx": False, "abajo_oscuro": True, "escenas": [
    {"visual": "persona", "tema": "claro",
     "notifs": {"impulsar": 1.96, "monto": "$1,000 MXN", "cero": 11.5, "fin": 12.1,
                "items": [{"en": 8.06, "icono": "👍", "texto": "A 128 personas les gusta"}, {"en": 9.0, "icono": "💬", "texto": "¿Info?"},
                          {"en": 10.28, "icono": "💬", "texto": "¿Precio? Info por favor"}]},
     "grupos": [
         {"y": .76, "lineas": ["-Ya le pagaste a Facebook", "para impulsar una publicación"]},
         {"y": .76, "lineas": ["-para que la vea más gente", "tratando de vender más."]},
         {"y": .76, "lineas": ["-y lo único", "que te llegó fue"]},
         {"y": .76, "lineas": ["-likes, comentarios", "e información,"]},
         {"y": .76, "lineas": ["-pero", "*cero ventas."]}]},
    {"visual": "persona", "tema": "claro",
     "orden": {"en": 15.1, "tacha": 16.24, "swap": 17.82, "luz2": 24.76, "fin": 26.0, "uno": "ANUNCIO", "dos": "CONTENIDO"},
     "grupos": [
         {"y": .2, "lineas": ["-Te explico", "qué fue lo que pasó,"]},
         {"y": .2, "lineas": ["-presta", "mucha atención."]},
         {"y": .2, "lineas": ["-el anuncio no es", "el primer paso."]},
         {"y": .2, "lineas": ["-primero va", "*el contenido,"]},
         {"y": .2, "lineas": ["-algo que tú", "quieras comunicar."]},
         {"y": .2, "lineas": ["-y luego de tener", "un mensaje que compartir,"]},
         {"y": .2, "lineas": ["-entonces vienen", "los anuncios."]}]},
    {"visual": "persona", "tema": "claro",
     "embudo": {"fin": 35.6, "pasos": [{"en": 26.88, "icono": "📝", "texto": "Contenido"}, {"en": 27.78, "icono": "👥", "texto": "Audiencia"},
                                       {"en": 30.96, "icono": "📣", "texto": "Anuncios"}, {"en": 35.02, "icono": "💰", "texto": "Ventas"}]},
     "grupos": [
         {"y": .2, "lineas": ["-El contenido genera", "audiencias"]},
         {"y": .2, "lineas": ["-que ya te vio", "y ya le interesó."]},
         {"y": .2, "lineas": ["-y los anuncios sirven para", "convertir esa audiencia"]},
         {"y": .2, "lineas": ["-que ya creaste", "en ventas."]}]},
    {"visual": "persona", "tema": "claro", "trans": "zoom", "invita": inv(39.4),
     "grupos": [
         {"y": .76, "lineas": ["-Todo esto que", "te estoy contando"]},
         {"y": .76, "lineas": ["-te lo puedo enseñar en una", "clase a profundidad"]},
         {"y": .76, "lineas": ["-el próximo jueves", "en punto de las 8 de la noche."]}]},
    {"visual": "persona", "tema": "claro", "invita": inv(39.4),
     "chips": {"items": [{"en": 46.28, "icono": "🏆", "texto": "Anuncios ganadores"}, {"en": 47.74, "icono": "🧠", "texto": "Mentalidad"},
                         {"en": 49.1, "icono": "🤖", "texto": "Inteligencia artificial"}, {"en": 54.12, "icono": "💰", "texto": "Más ventas y dinero"}],
               "junta": 56.0, "fin": 56.4},
     "grupos": [
         {"y": .76, "lineas": ["-Vas a aprender cómo hacer", "anuncios ganadores,"]},
         {"y": .76, "lineas": ["-cuál es", "la mentalidad,"]},
         {"y": .76, "lineas": ["-cómo funciona la", "inteligencia artificial,"]},
         {"y": .76, "lineas": ["-pero sobre todo cómo esto", "lo puedes aplicar"]},
         {"y": .76, "lineas": ["-para generar más ventas", "y más dinero para tu negocio."]}]},
    {"visual": "persona", "tema": "claro", "textoTema": "oscuro", "invita": inv(39.4, flecha=60.26),
     "grupos": [
         {"y": .66, "lineas": ["-Inscríbete a esta clase", "y después me lo vas a agradecer."]},
         {"y": .66, "lineas": ["-que|Que dios|Dios", "te bendiga.|bendiga."]},
         {"y": .66, "lineas": ["-dale|Dale click|clic aquí.|aquí.", "allá|Allá nos vemos.|vemos."]}]},
]}
