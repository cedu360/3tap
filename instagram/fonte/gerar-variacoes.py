# Gera os posts do feed em 3 moldes alternativos (claro, laranja, cartão) para o perfil não repetir o mesmo visual.
# Uso: python3 gerar-variacoes.py   -> imagens/post-XX-v.jpg e atualiza fila.json a partir de 27/10
import json, os
from PIL import Image, ImageDraw, ImageFont
AQUI = os.path.dirname(os.path.abspath(__file__)); MK = os.path.dirname(AQUI)
FOTOS = os.path.join(MK, "profissoes-runway", "original"); KIT = os.path.join(MK, "logo-3tap", "final", "kit")
F_B = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"; F_R = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
W, H = 1080, 1350
NAVY, LARANJA, CREME, BRANCO = (16, 20, 31), (255, 106, 0), (250, 245, 236), (255, 255, 255)
def logo(var):
    l = Image.open(os.path.join(KIT, f"logo-horizontal-{var}-clicou-chegou.png")).convert("RGBA")
    l = l.crop(l.getbbox()); l.thumbnail((300, 110), Image.LANCZOS); return l
LOGO_ESC, LOGO_CLA = logo("escuro"), logo("claro")
def foto(nome, w, h):
    f = Image.open(os.path.join(FOTOS, nome + ".png")).convert("RGB"); s = max(w / f.width, h / f.height)
    f = f.resize((int(f.width * s) + 1, int(f.height * s) + 1), Image.LANCZOS)
    x, y = (f.width - w) // 2, (f.height - h) // 2; return f.crop((x, y, x + w, y + h))
def arred(img, r):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *img.size), r, fill=255); return m
def titulo(d, linhas, x, y, maxw, cor, tam=84):
    f = ImageFont.truetype(F_B, tam)
    while max(d.textlength(l, font=f) for l in linhas) > maxw: tam -= 4; f = ImageFont.truetype(F_B, tam)
    for l in linhas: d.text((x, y), l, font=f, fill=cor); y += tam + 12
    return y
def claro(p):
    c = Image.new("RGB", (W, H), CREME); ft = foto(p["imagem"], W - 120, 760); c.paste(ft, (60, 60), arred(ft, 40))
    d = ImageDraw.Draw(c); y = titulo(d, p["titulo"].split("\n"), 70, 870, W - 140, NAVY)
    d.rounded_rectangle((70, y + 20, 400, y + 92), 36, fill=LARANJA)
    d.text((235, y + 56), "Link na bio", font=ImageFont.truetype(F_B, 34), fill=BRANCO, anchor="mm")
    c.paste(LOGO_CLA, (W - LOGO_CLA.width - 60, H - LOGO_CLA.height - 50), LOGO_CLA); return c
def laranja(p):
    c = Image.new("RGB", (W, H), LARANJA); d = ImageDraw.Draw(c)
    f = ImageFont.truetype(F_B, 112); linhas = [""]
    for w in p["titulo"].replace("\n", " ").split():
        t = (linhas[-1] + " " + w).strip()
        if d.textlength(t, font=f) > W - 140 and linhas[-1]: linhas.append(w)
        else: linhas[-1] = t
    titulo(d, linhas, 70, 90, W - 140, BRANCO, 112)
    ft = foto(p["imagem"], 760, 760); c.paste(ft, (W - 760, H - 760), arred(ft, 60))
    d.text((70, H - 120), "3tapbrasil.com", font=ImageFont.truetype(F_R, 36), fill=BRANCO); return c
def cartao(p):
    c = foto(p["imagem"], W, H); d = ImageDraw.Draw(c)
    d.rounded_rectangle((50, H - 470, W - 50, H - 50), 40, fill=BRANCO)
    titulo(d, p["titulo"].split("\n"), 100, H - 420, W - 200, NAVY, 78)
    d.rounded_rectangle((100, H - 150, 220, H - 138), 6, fill=LARANJA)
    c.paste(LOGO_CLA, (W - LOGO_CLA.width - 100, H - LOGO_CLA.height - 90), LOGO_CLA); return c
MOLDES = [claro, laranja, cartao]
posts = {p["arquivo"]: p for p in json.load(open(os.path.join(AQUI, "posts.json")))}
fila = json.load(open(os.path.join(AQUI, "fila.json"))); k = 0
for it in fila:
    p = posts.get(it["arquivo"])
    if it["tipo"] != "FEED" or it["dia"] < "2026-10-27" or not p or p["imagem"].startswith("kit:"): continue
    novo = it["arquivo"].replace(".jpg", "-v.jpg")
    MOLDES[k % 3](p).save(os.path.join(AQUI, "imagens", novo), "JPEG", quality=88); it["arquivo"] = novo; k += 1
json.dump(fila, open(os.path.join(AQUI, "fila.json"), "w"), ensure_ascii=False, indent=1)
print(k, "posts em moldes novos")
