# Gera artes de anúncio (feed 1080x1350 e story 1080x1920): foto da profissão, celular com a tela real do app,
# gancho forte e botão "Acesse grátis". Uso: python3 gerar-anuncios.py  -> imagens/anuncio-*.jpg e story-anuncio-*.jpg
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQUI = os.path.dirname(os.path.abspath(__file__)); MK = os.path.dirname(AQUI)
FOTOS = os.path.join(MK, "profissoes-runway", "original")
TELAS = os.environ.get("TELAS_APP", "/home/user/3tap/img/app")
KIT = os.path.join(MK, "logo-3tap", "final", "kit")
F = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
SAIDA = os.path.join(AQUI, "imagens")
LARANJA, AMARELO, BRANCO, NAVY = (255, 106, 0), (255, 178, 31), (255, 255, 255), (16, 20, 31)
FUNDOS = [((16, 20, 31), (40, 24, 12)), ((255, 106, 0), (200, 50, 0)), ((14, 60, 72), (8, 24, 40)), ((48, 22, 86), (16, 20, 31))]

def fonte(peso, t): return ImageFont.truetype(F % peso, t)
def degrade(w, h, a, b):
    g = Image.new("RGB", (1, h))
    for y in range(h): g.putpixel((0, y), tuple(int(a[i] + (b[i] - a[i]) * y / h) for i in range(3)))
    return g.resize((w, h))
def foto(nome, w, h):
    f = Image.open(os.path.join(FOTOS, nome + ".png")).convert("RGB"); s = max(w / f.width, h / f.height)
    f = f.resize((int(f.width * s) + 1, int(f.height * s) + 1), Image.LANCZOS)
    x, y = (f.width - w) // 2, (f.height - h) // 3; return f.crop((x, y, x + w, y + h))
def celular(tela, largura):
    t = Image.open(os.path.join(TELAS, tela + ".webp")).convert("RGB")
    t = t.resize((largura, int(t.height * largura / t.width)), Image.LANCZOS)
    b = 16; c = Image.new("RGBA", (t.width + 2 * b, t.height + 2 * b), (0, 0, 0, 0))
    d = ImageDraw.Draw(c); d.rounded_rectangle((0, 0, c.width - 1, c.height - 1), 56, fill=(10, 10, 14, 255))
    m = Image.new("L", t.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *t.size), 42, fill=255)
    c.paste(t, (b, b), m)
    sombra = Image.new("RGBA", (c.width + 120, c.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle((60, 75, 60 + c.width, 75 + c.height), 56, fill=(0, 0, 0, 150))
    sombra = sombra.filter(ImageFilter.GaussianBlur(28)); sombra.paste(c, (60, 60), c)
    return sombra
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
def escrever(d, texto, x, y, maxw, tam, cor, peso="ExtraBold", destaque=None):
    f = fonte(peso, tam); marcadas = set((destaque or "").split()); esp = d.textlength(" ", font=f)
    for l in quebrar(d, texto, f, maxw):
        xx = x
        for w in l.split():
            d.text((xx, y), w, font=f, fill=AMARELO if w in marcadas else cor); xx += d.textlength(w, font=f) + esp
        y += int(tam * 1.12)
    return y
def check(d, x, y, texto, tam=34):
    d.ellipse((x, y + 4, x + 34, y + 38), fill=LARANJA)
    d.line((x + 9, y + 21, x + 15, y + 28, x + 26, y + 13), fill=BRANCO, width=5)
    d.text((x + 50, y), texto, font=fonte("SemiBold", tam), fill=BRANCO)
def botao(d, x, y, texto="Acesse grátis", tam=40):
    f = fonte("ExtraBold", tam); w = d.textlength(texto, font=f) + 140
    d.rounded_rectangle((x, y, x + w, y + tam + 44), (tam + 44) // 2, fill=AMARELO)
    d.text((x + 44, y + 20), texto, font=f, fill=NAVY)
    ax = x + w - 56; ay = y + (tam + 44) // 2
    d.line((ax - 16, ay, ax + 10, ay), fill=NAVY, width=6); d.line((ax, ay - 11, ax + 11, ay, ax, ay + 11), fill=NAVY, width=6)
    return y + tam + 44
logo = Image.open(os.path.join(KIT, "logo-horizontal-escuro-clicou-chegou.png")).convert("RGBA")
logo = logo.crop(logo.getbbox()); logo.thumbnail((260, 96), Image.LANCZOS)

def feed(a, i):
    W, H = 1080, 1350; c = degrade(W, H, *FUNDOS[i % len(FUNDOS)]).convert("RGBA")
    ft = foto(a["foto"], W, 620).convert("RGBA")
    c.paste(ft, (0, 0), _mascara(W, 620))
    sombra = Image.new("RGBA", (W, 620), (0, 0, 0, 0)); ImageDraw.Draw(sombra).rectangle((0, 0, W, 620), fill=(0, 0, 0, 70)); c.alpha_composite(sombra)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((60, 56, 60 + d.textlength(a["selo"], font=fonte("Bold", 30)) + 48, 112), 28, fill=LARANJA)
    d.text((84, 66), a["selo"], font=fonte("Bold", 30), fill=BRANCO)
    tam = 76
    while len(quebrar(d, a["gancho"], fonte("ExtraBold", tam), 540)) > 3: tam -= 6
    y = escrever(d, a["gancho"], 60, 380 + (76 - tam) * 2, 540, tam, BRANCO, destaque=a.get("destaque"))
    cel = celular(a["tela"], 360); c.alpha_composite(cel, (W - cel.width + 30, 470))
    y = max(y + 30, 720)
    for b in a["pontos"]: check(d, 60, y, b); y += 66
    botao(d, 60, y + 30)
    d.text((60, H - 90), "3tapbrasil.com", font=fonte("SemiBold", 32), fill=(230, 230, 235))
    c.alpha_composite(logo, (60, H - 200))
    return c.convert("RGB")
def _mascara(w, h):
    g = Image.new("L", (1, h))
    for y in range(h): g.putpixel((0, y), 255 if y < h * 0.55 else max(0, int(255 * (h - y) / (h * 0.45))))
    return g.resize((w, h))
def story(a, i):
    W, H = 1080, 1920; c = degrade(W, H, *FUNDOS[(i + 1) % len(FUNDOS)]).convert("RGBA")
    ft = foto(a["foto"], W, 900).convert("RGBA"); c.paste(ft, (0, 0), _mascara(W, 900))
    d = ImageDraw.Draw(c)
    y = escrever(d, a["gancho"], 70, 640, W - 140, 96, BRANCO, destaque=a.get("destaque"))
    cel = celular(a["tela"], 380); c.alpha_composite(cel, (W - cel.width + 50, y - 10))
    yy = y + 50
    for b in a["pontos"]: check(d, 70, yy, b, 34); yy += 70
    botao(d, 70, yy + 30, "Acesse grátis", 44)
    d.text((70, H - 170), "Link na bio · 3tapbrasil.com", font=fonte("SemiBold", 36), fill=BRANCO)
    return c.convert("RGB")

ANUNCIOS = [
  {"id": "eletricista", "foto": "eletricista", "tela": "buscar", "selo": "Eletricista perto de você", "gancho": "Chuveiro queimou? Resolve em 3 toques.", "destaque": "3 toques", "pontos": ["Nota de quem contratou", "Preço antes de chamar", "Disponível hoje"]},
  {"id": "diarista", "foto": "limpeza", "tela": "inicio", "selo": "Diarista e limpeza", "gancho": "Casa limpa sem ligar pra ninguém.", "destaque": "sem ligar", "pontos": ["Escolhe dia e hora", "Avaliações verificadas", "Tudo combinado no app"]},
  {"id": "encanador", "foto": "encanador", "tela": "chat", "selo": "Encanador agora", "gancho": "Vazamento não espera. Nem você.", "destaque": "Nem você.", "pontos": ["Manda foto pelo chat", "Recebe a proposta", "Acompanha a chegada"]},
  {"id": "prestador", "foto": "pedreiro", "tela": "prestador", "selo": "Para prestadores", "gancho": "Mais clientes perto de você. Cadastro grátis.", "destaque": "Cadastro grátis.", "pontos": ["Seus preços e sua agenda", "Pedidos no seu raio", "Sem pagar pra aparecer"]},
  {"id": "montador", "foto": "montador-de-moveis", "tela": "acompanhar", "selo": "Montador de móveis", "gancho": "Móvel novo montado hoje.", "destaque": "hoje.", "pontos": ["Vê a distância em km", "Acompanha a chegada", "Avalia no final"]},
  {"id": "ar", "foto": "tecnico-ar-condicionado", "tela": "servico", "selo": "Ar-condicionado", "gancho": "Calor chegou? Técnico chega antes.", "destaque": "chega antes.", "pontos": ["Instalação e limpeza", "Preço visível", "Nota real"]},
  {"id": "manicure", "foto": "manicure", "tela": "perfil", "selo": "Beleza em casa", "gancho": "Manicure na sua casa, no seu horário.", "destaque": "no seu horário.", "pontos": ["Perfis com avaliação", "Agenda no app", "Sem troca de número"]},
  {"id": "pintor", "foto": "pintor", "tela": "video", "selo": "Pintor", "gancho": "Orçamento por vídeo, sem visita.", "destaque": "sem visita.", "pontos": ["Mostra a parede na chamada", "Recebe o preço", "Agenda o dia"]},
  {"id": "jardineiro", "foto": "jardineiro", "tela": "buscar", "selo": "Jardinagem", "gancho": "Jardim em dia em 3 toques.", "destaque": "3 toques.", "pontos": ["Corte e poda", "Profissional perto", "Preço antes"]},
  {"id": "frete", "foto": "frete-e-carreto", "tela": "chat", "selo": "Frete e carreto", "gancho": "Mudança pequena? Frete hoje.", "destaque": "Frete hoje.", "pontos": ["Foto do que vai levar", "Proposta no chat", "Acompanha pelo app"]},
  {"id": "marido", "foto": "marido-de-aluguel", "tela": "inicio", "selo": "Marido de aluguel", "gancho": "Aquele conserto parado? Hoje sai.", "destaque": "Hoje sai.", "pontos": ["Pequenos reparos", "Quem está perto", "Avaliação real"]},
  {"id": "celular", "foto": "tecnico-de-celular", "tela": "servico", "selo": "Técnico de celular", "gancho": "Tela quebrada não é o fim.", "destaque": "não é o fim.", "pontos": ["Técnicos avaliados", "Preço na hora", "Perto de você"]},
]

if __name__ == "__main__":
    for i, a in enumerate(ANUNCIOS):
        feed(a, i).save(os.path.join(SAIDA, f"anuncio-{a['id']}.jpg"), "JPEG", quality=90)
        story(a, i).save(os.path.join(SAIDA, f"story-anuncio-{a['id']}.jpg"), "JPEG", quality=90)
    print(len(ANUNCIOS), "anúncios")
