# Gera anúncios novos sozinho quando a fila está acabando, com o Gemini (chave grátis em GEMINI_API_KEY).
# O Gemini (plano grátis) escreve o gancho e os pontos. A foto vem do banco kit/fotos, com corte, zoom e espelhamento sorteados
# para não repetir a mesma imagem; o plano grátis não gera imagens (GEMINI_MODELO_IMAGEM liga isso num plano pago).
# O script monta feed (1080x1350) e story (1080x1920) no visual do 3Tap e põe na fila.json já aprovados.
# Uso: python3 gerar.py [--teste]    (--teste gera sem chamar o Gemini e sem mexer na fila)
import base64, io, json, os, random, sys, time, urllib.request
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(AQUI, "kit")
TELAS = os.path.join(os.path.dirname(AQUI), "img", "app")
CHAVE = os.environ.get("GEMINI_API_KEY", "")
MODELOS_TEXTO = os.environ.get("GEMINI_MODELO_TEXTO", "gemini-3.5-flash-lite,gemini-flash-lite-latest").split(",")
MODELOS_IMAGEM = [m for m in os.environ.get("GEMINI_MODELO_IMAGEM", "").split(",") if m]
MINIMO = int(os.environ.get("IG_FILA_MINIMA", 4))  # gera quando sobram menos fotos novas que isso
POR_VEZ = int(os.environ.get("IG_GERAR_POR_VEZ", 2))
TESTE = "--teste" in sys.argv

LARANJA, AMARELO, BRANCO, NAVY = (255, 106, 0), (255, 178, 31), (255, 255, 255), (16, 20, 31)
FUNDOS = [((16, 20, 31), (40, 24, 12)), ((255, 106, 0), (200, 50, 0)), ((14, 60, 72), (8, 24, 40)), ((48, 22, 86), (16, 20, 31))]
TELAS_APP = ["buscar", "inicio", "chat", "servico", "perfil", "acompanhar", "video", "prestador"]
PROFISSOES = {  # foto do banco: (nome no anúncio, hashtag)
  "eletricista": ("Eletricista", "#Eletricista"), "encanador": ("Encanador", "#Encanador"), "limpeza": ("Diarista", "#Diarista"),
  "pedreiro": ("Pedreiro", "#Pedreiro"), "pintor": ("Pintor", "#Pintor"), "montador-de-moveis": ("Montador de móveis", "#MontadorDeMoveis"),
  "tecnico-ar-condicionado": ("Técnico de ar-condicionado", "#ArCondicionado"), "manicure": ("Manicure", "#Manicure"),
  "jardineiro": ("Jardineiro", "#Jardinagem"), "frete-e-carreto": ("Frete e carreto", "#Frete"), "marido-de-aluguel": ("Marido de aluguel", "#MaridoDeAluguel"),
  "tecnico-de-celular": ("Técnico de celular", "#TecnicoDeCelular"), "desentupidor": ("Desentupidora", "#Desentupidora"),
  "dedetizacao": ("Dedetização", "#Dedetizacao"), "cuidador-de-idosos": ("Cuidador de idosos", "#CuidadorDeIdosos"), "mecanico": ("Mecânico", "#Mecanico"),
  "limpeza-de-piscina": ("Limpeza de piscina", "#Piscina"), "tecnico-de-informatica": ("Técnico de informática", "#Informatica"),
  "cabeleireiro": ("Cabeleireiro", "#Cabeleireiro"), "vidraceiro": ("Vidraceiro", "#Vidraceiro"), "passeador-de-caes": ("Passeador de cães", "#PasseadorDeCaes"),
  "aulas-particulares": ("Aulas particulares", "#AulasParticulares"), "lavagem-de-estofados": ("Lavagem de estofados", "#LavagemDeEstofados"),
  "serralheiro": ("Serralheiro", "#Serralheiro"), "babysitter": ("Babá", "#Baba"), "churrasqueiro": ("Churrasqueiro", "#Churrasqueiro"),
  "costureira": ("Costureira", "#Costureira"), "cozinheira": ("Cozinheira", "#Cozinheira"), "fotografo": ("Fotógrafo", "#Fotografo"),
  "garcom": ("Garçom", "#Garcom"), "instalacao-de-tv": ("Instalação de TV", "#InstalacaoDeTV"), "lavagem-de-carro": ("Lavagem de carro", "#LavaJato"),
  "marceneiro": ("Marceneiro", "#Marceneiro"), "passadeira": ("Passadeira", "#Passadeira"), "personal-trainer": ("Personal trainer", "#PersonalTrainer"),
  "soldador": ("Soldador", "#Soldador"), "automotivo": ("Serviços automotivos", "#Automotivo"), "instalador": ("Instalador", "#Instalador"),
}
RESERVA = [  # textos usados se o Gemini não responder
  ("{p} perto de você, em 3 toques.", "3 toques.", ["Nota de quem contratou", "Preço antes de chamar", "Tudo pelo app"]),
  ("Precisa de {p}? Clicou, chegou.", "Clicou, chegou.", ["Profissional perto", "Conversa no app", "Avaliação real"]),
]

def fonte(peso, t): return ImageFont.truetype(os.path.join(KIT, f"Inter-{peso}.otf"), t)
def degrade(w, h, a, b):
    g = Image.new("RGB", (1, h))
    for y in range(h): g.putpixel((0, y), tuple(int(a[i] + (b[i] - a[i]) * y / h) for i in range(3)))
    return g.resize((w, h))
def recorte(f, w, h):
    s = max(w / f.width, h / f.height); f = f.resize((int(f.width * s) + 1, int(f.height * s) + 1), Image.LANCZOS)
    x, y = (f.width - w) // 2, (f.height - h) // 3; return f.crop((x, y, x + w, y + h))
def mascara(w, h):
    g = Image.new("L", (1, h))
    for y in range(h): g.putpixel((0, y), 255 if y < h * 0.55 else max(0, int(255 * (h - y) / (h * 0.45))))
    return g.resize((w, h))
def celular(tela, largura):
    t = Image.open(os.path.join(TELAS, tela + ".webp")).convert("RGB"); t = t.resize((largura, int(t.height * largura / t.width)), Image.LANCZOS)
    b = 16; c = Image.new("RGBA", (t.width + 2 * b, t.height + 2 * b), (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 56, fill=(10, 10, 14, 255))
    m = Image.new("L", t.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *t.size), 42, fill=255); c.paste(t, (b, b), m)
    s = Image.new("RGBA", (c.width + 120, c.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((60, 75, 60 + c.width, 75 + c.height), 56, fill=(0, 0, 0, 150))
    s = s.filter(ImageFilter.GaussianBlur(28)); s.paste(c, (60, 60), c); return s
def quebrar(d, texto, f, maxw):
    linhas = []
    for parte in texto.split("\n"):
        l = ""
        for w in parte.split():
            t = (l + " " + w).strip()
            if d.textlength(t, font=f) > maxw and l: linhas.append(l); l = w
            else: l = t
        linhas.append(l)
    return linhas
def escrever(d, texto, x, y, maxw, tam, cor, destaque=""):
    f = fonte("ExtraBold", tam); marcadas = set(destaque.split()); esp = d.textlength(" ", font=f)
    for l in quebrar(d, texto, f, maxw):
        xx = x
        for w in l.split(): d.text((xx, y), w, font=f, fill=AMARELO if w in marcadas else cor); xx += d.textlength(w, font=f) + esp
        y += int(tam * 1.12)
    return y
def check(d, x, y, texto, tam=34):
    d.ellipse((x, y + 4, x + 34, y + 38), fill=LARANJA); d.line((x + 9, y + 21, x + 15, y + 28, x + 26, y + 13), fill=BRANCO, width=5)
    d.text((x + 50, y), texto, font=fonte("SemiBold", tam), fill=BRANCO)
def botao(d, x, y, tam=40):
    f = fonte("ExtraBold", tam); w = d.textlength("Acesse grátis", font=f) + 140
    d.rounded_rectangle((x, y, x + w, y + tam + 44), (tam + 44) // 2, fill=AMARELO); d.text((x + 44, y + 20), "Acesse grátis", font=f, fill=NAVY)
    ax = x + w - 56; ay = y + (tam + 44) // 2
    d.line((ax - 16, ay, ax + 10, ay), fill=NAVY, width=6); d.line((ax, ay - 11, ax + 11, ay, ax, ay + 11), fill=NAVY, width=6)

def feed(a, foto, i):
    W, H = 1080, 1350; c = degrade(W, H, *FUNDOS[i % 4]).convert("RGBA")
    c.paste(recorte(foto, W, 620).convert("RGBA"), (0, 0), mascara(W, 620))
    v = Image.new("RGBA", (W, 620), (0, 0, 0, 70)); c.alpha_composite(v); d = ImageDraw.Draw(c)
    d.rounded_rectangle((60, 56, 60 + d.textlength(a["selo"], font=fonte("Bold", 30)) + 48, 112), 28, fill=LARANJA)
    d.text((84, 66), a["selo"], font=fonte("Bold", 30), fill=BRANCO)
    tam = 76
    while len(quebrar(d, a["gancho"], fonte("ExtraBold", tam), 540)) > 3: tam -= 6
    y = escrever(d, a["gancho"], 60, 380 + (76 - tam) * 2, 540, tam, BRANCO, a["destaque"])
    cel = celular(a["tela"], 360); c.alpha_composite(cel, (W - cel.width + 30, 470))
    y = max(y + 30, 720)
    for b in a["pontos"]: check(d, 60, y, b); y += 66
    botao(d, 60, y + 30); d.text((60, H - 90), "3tapbrasil.com", font=fonte("SemiBold", 32), fill=(230, 230, 235))
    c.alpha_composite(LOGO, (60, H - 200)); return c.convert("RGB")
def story(a, foto, i):
    W, H = 1080, 1920; c = degrade(W, H, *FUNDOS[(i + 1) % 4]).convert("RGBA")
    c.paste(recorte(foto, W, 900).convert("RGBA"), (0, 0), mascara(W, 900)); d = ImageDraw.Draw(c)
    y = escrever(d, a["gancho"], 70, 640, W - 140, 96, BRANCO, a["destaque"])
    cel = celular(a["tela"], 380); c.alpha_composite(cel, (W - cel.width + 50, y - 10)); yy = y + 50
    for b in a["pontos"]: check(d, 70, yy, b, 34); yy += 70
    botao(d, 70, yy + 30, 44); d.text((70, H - 170), "Link na bio · 3tapbrasil.com", font=fonte("SemiBold", 36), fill=BRANCO)
    return c.convert("RGB")

def gemini(modelo, corpo):
    r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
        data=json.dumps(corpo).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": CHAVE})
    return json.load(urllib.request.urlopen(r, timeout=90))
def textos(nome, usados):
    if CHAVE and not TESTE:
        for m in MODELOS_TEXTO:
          try:
            p = (f"Crie um anúncio curto para Instagram do 3Tap, app que encontra profissionais perto de você. Profissão: {nome}. "
                 "O gancho fala de um problema do dia a dia e da solução, como nestes exemplos: 'Chuveiro queimou? Resolve em 3 toques.', "
                 "'Vazamento não espera. Nem você.', 'Orçamento por vídeo, sem visita.', 'Tela quebrada não é o fim.'. "
                 "Responda só JSON: {\"gancho\": no máximo 45 caracteres, \"destaque\": as 1 a 3 últimas palavras do gancho, "
                 "\"pontos\": 3 vantagens de usar o app, no máximo 26 caracteres cada}. Português do Brasil com acentos corretos, sem emojis, "
                 "sem 'Clicou, chegou', sem prometer garantia nem dizer verificado, sem as palavras catálogo, baixe ou compre. "
                 f"Não repita estes ganchos: {'; '.join(usados[-20:])}")
            j = gemini(m.strip(), {"contents": [{"parts": [{"text": p}]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 1.1}})
            t = json.loads(next(x["text"] for x in j["candidates"][0]["content"]["parts"] if "text" in x))
            if len(t["gancho"]) <= 60 and len(t["pontos"]) == 3 and all(len(x) <= 32 for x in t["pontos"]): return t
            print("Texto do Gemini fora do tamanho")
          except Exception as e: print(f"Gemini (texto, {m}) falhou:", e)
        print("Usando texto de reserva")
    g, dst, pts = random.choice(RESERVA); return {"gancho": g.format(p=nome), "destaque": dst, "pontos": pts}
def foto_nova(nome, slug):
    if CHAVE and not TESTE:
        p = (f"Fotografia realista vertical de um(a) {nome.lower()} brasileiro(a) trabalhando em uma casa em Minas Gerais, luz natural, "
             "pessoa sorrindo, estilo foto profissional de anúncio, sem texto, sem logotipos.")
        for m in MODELOS_IMAGEM:
            try:
                j = gemini(m.strip(), {"contents": [{"parts": [{"text": p}]}], "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}})
                for parte in j["candidates"][0]["content"]["parts"]:
                    if "inlineData" in parte: return Image.open(io.BytesIO(base64.b64decode(parte["inlineData"]["data"]))).convert("RGB"), m
            except Exception as e: print(f"Gemini (imagem, {m}) falhou:", e)
    f = Image.open(os.path.join(KIT, "fotos", slug + ".jpg")).convert("RGB")
    if random.random() < 0.5: f = f.transpose(Image.FLIP_LEFT_RIGHT)
    z = random.uniform(1.0, 1.3); w, h = int(f.width / z), int(f.height / z)
    x, y = random.randint(0, f.width - w), random.randint(0, (f.height - h) // 2 + 1)
    return f.crop((x, y, x + w, y + h)), "banco"

if __name__ == "__main__":
    fila = json.load(open(os.path.join(AQUI, "fila.json")))
    estado = json.load(open(os.path.join(AQUI, "estado.json")))
    livres = [x for x in fila if x["tipo"] == "FEED" and x.get("aprovado") and (x["arquivo"] not in estado or str(estado[x["arquivo"]].get("pulado", "")).startswith("legenda"))]
    if len(livres) >= MINIMO and not TESTE: print(f"Fila com {len(livres)} fotos novas, nada a gerar"); sys.exit(0)
    LOGO = Image.open(os.path.join(KIT, "logo.png")).convert("RGBA"); LOGO.thumbnail((260, 96), Image.LANCZOS)
    usos = {s: sum(1 for x in fila if x.get("tema") == "#" + s) for s in PROFISSOES}
    escolhidas = sorted(PROFISSOES, key=lambda s: (usos[s], random.random()))[:POR_VEZ]
    usados = [x["legenda"].split("\n")[0] for x in fila if x.get("legenda")]
    dia = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
    novos = []
    for i, slug in enumerate(escolhidas):
        nome, tag = PROFISSOES[slug]
        t = textos(nome, usados); usados.append(t["gancho"])
        a = {**t, "selo": nome, "tela": random.choice(TELAS_APP)}
        img, origem = foto_nova(nome, slug)
        n = random.randrange(4)
        base = f"g-{slug}-{dia}"
        feed(a, img, n).save(os.path.join(AQUI, f"anuncio-{base}.jpg"), "JPEG", quality=88)
        story(a, img, n).save(os.path.join(AQUI, f"story-anuncio-{base}.jpg"), "JPEG", quality=88)
        leg = a["gancho"] + "\n\n" + "\n".join("✅ " + p for p in a["pontos"]) + f"\n\n👉 Acesse grátis: link na bio ou 3tapbrasil.com\n\n{tag} #3Tap #ClicouChegou"
        novos += [{"tipo": "FEED", "arquivo": f"anuncio-{base}.jpg", "legenda": leg, "tema": "#" + slug, "aprovado": True, "gerado": origem},
                  {"tipo": "STORIES", "arquivo": f"story-anuncio-{base}.jpg", "tema": "#" + slug, "aprovado": True, "gerado": origem}]
        print(f"Gerado {base}: {a['gancho']} (foto: {origem})")
        time.sleep(2)
    if not TESTE:
        with open(os.path.join(AQUI, "fila.json"), "w") as f: json.dump(fila + novos, f, ensure_ascii=False, indent=1)
