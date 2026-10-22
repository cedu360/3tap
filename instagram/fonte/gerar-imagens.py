# Gera as imagens 1080x1350 dos posts (foto da profissão + título + logo). Uso: python3 gerar-imagens.py
import json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQUI = os.path.dirname(os.path.abspath(__file__))
MK = os.path.dirname(AQUI)
FOTOS = os.path.join(MK, "profissoes-runway", "original")
KIT = os.path.join(MK, "logo-3tap", "final", "kit")
FONTE = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
W, H = 1080, 1350
FUNDO = (16, 20, 31)
SAIDA = os.path.join(AQUI, "imagens"); os.makedirs(SAIDA, exist_ok=True)
logo = Image.open(os.path.join(KIT, "logo-horizontal-escuro-clicou-chegou.png")).convert("RGBA")
logo = logo.crop(logo.getbbox()); logo.thumbnail((360, 130), Image.LANCZOS)

def post(p):
    img = p["imagem"]
    if img.startswith("kit:"):
        base = Image.open(os.path.join(KIT, f"instagram-post-1080-{img[4:]}.png")).convert("RGB")
        c = Image.new("RGB", (W, H), FUNDO); c.paste(base, (0, (H - 1080) // 2))
        return c
    foto = Image.open(os.path.join(FOTOS, img + ".png")).convert("RGB").resize((W, W), Image.LANCZOS)
    c = Image.new("RGB", (W, H), FUNDO); c.paste(foto, (0, 0))
    # degradê da foto para o fundo escuro
    g = Image.new("L", (1, H))
    for y in range(H):
        g.putpixel((0, y), 0 if y < 560 else min(255, int((y - 560) / 420 * 255)))
    c = Image.composite(Image.new("RGB", (W, H), FUNDO), c, g.resize((W, H)))
    d = ImageDraw.Draw(c)
    linhas = p["titulo"].split("\n")
    tam = 92
    f = ImageFont.truetype(FONTE, tam)
    while max(d.textlength(l, font=f) for l in linhas) > W - 140:
        tam -= 4; f = ImageFont.truetype(FONTE, tam)
    y = H - 250 - len(linhas) * (tam + 14)
    for l in linhas:
        d.text((70, y), l, font=f, fill=(255, 255, 255)); y += tam + 14
    d.rounded_rectangle((70, y + 18, 190, y + 30), 6, fill=(255, 106, 0))
    c.paste(logo, (W - logo.width - 60, H - logo.height - 50), logo)
    return c

posts = json.load(open(os.path.join(AQUI, "posts.json")))
for p in posts:
    post(p).save(os.path.join(SAIDA, p["arquivo"]), "JPEG", quality=88)
print(len(posts), "imagens em", SAIDA)
