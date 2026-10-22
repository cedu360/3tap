# Gera post-31, stories (story-NN.jpg, 1080x1920) e reels (reel-NN.mp4, 1080x1920, ~9 s, áudio mudo).
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
from conteudo_extra import POST31, STORIES, REELS
AQUI = os.path.dirname(os.path.abspath(__file__)); MK = os.path.dirname(AQUI)
FOTOS = os.path.join(MK, "profissoes-runway", "original"); KIT = os.path.join(MK, "logo-3tap", "final", "kit")
BOLD = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"; MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
FUNDO = (16, 20, 31); LARANJA = (255, 106, 0)
SAIDA = os.path.join(AQUI, "imagens"); os.makedirs(SAIDA, exist_ok=True)
logo = Image.open(os.path.join(KIT, "logo-horizontal-escuro-clicou-chegou.png")).convert("RGBA"); logo = logo.crop(logo.getbbox())

def fonte(path, tam): return ImageFont.truetype(path, tam)
def caber(d, linhas, path, tam, larg):
    f = fonte(path, tam)
    while max(d.textlength(l, font=f) for l in linhas) > larg: tam -= 4; f = fonte(path, tam)
    return f, tam
def degrade(c, y0, y1):
    W, H = c.size; g = Image.new("L", (1, H))
    for y in range(H): g.putpixel((0, y), 0 if y < y0 else min(255, int((y - y0) / (y1 - y0) * 255)))
    return Image.composite(Image.new("RGB", (W, H), FUNDO), c, g.resize((W, H)))
def fundo_vertical(foto):
    f = Image.open(os.path.join(FOTOS, foto + ".png")).convert("RGB").resize((1350, 1350), Image.LANCZOS).crop((135, 0, 1215, 1350))
    c = Image.new("RGB", (1080, 1920), FUNDO); c.paste(f, (0, 0)); return degrade(c, 900, 1350)
def por_logo(c, larg, y):
    l = logo.copy(); l.thumbnail((larg, 400), Image.LANCZOS); c.paste(l, ((c.width - l.width) // 2, y), l)

def story(foto, grande, pequena):
    c = fundo_vertical(foto); d = ImageDraw.Draw(c); linhas = grande.split("\n")
    f, tam = caber(d, linhas, BOLD, 130, 940); y = 1180
    for l in linhas: d.text((70, y), l, font=f, fill="white"); y += tam + 16
    fp = fonte(MED, 46); d.text((70, y + 20), pequena, font=fp, fill=(205, 210, 222))
    d.rounded_rectangle((70, 1690, 520, 1790), 50, fill=LARANJA); d.text((295, 1740), "Link na bio", font=fonte(BOLD, 44), fill="white", anchor="mm")
    l = logo.copy(); l.thumbnail((300, 120), Image.LANCZOS); c.paste(l, (1080 - l.width - 60, 1690 + (100 - l.height) // 2), l)
    return c

def reel(i, foto, gancho, frase, tmp):
    base = fundo_vertical(foto); base.save(f"{tmp}/bg.png")
    for nome, txt, y, tamb in (("t1", gancho, 1250, 120), ("t2", frase, 1420, 78)):
        o = Image.new("RGBA", (1080, 1920)); d = ImageDraw.Draw(o)
        f, _ = caber(d, [txt], BOLD, tamb, 960); d.text((60, y), txt, font=f, fill="white" if nome == "t1" else (255, 178, 31))
        o.save(f"{tmp}/{nome}.png")
    fim = Image.new("RGB", (1080, 1920), FUNDO); por_logo(fim, 820, 700)
    ImageDraw.Draw(fim).text((540, 1150), "Link na bio", font=fonte(BOLD, 64), fill=LARANJA, anchor="mm"); fim.save(f"{tmp}/fim.png")
    out = os.path.join(SAIDA, f"reel-{i:02d}.mp4")
    filtro = ("[0:v]scale=1188:-1,zoompan=z='1+0.0016*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=210:s=1080x1920:fps=30[bg];"
              "[bg][1:v]overlay=enable='gte(t,0.6)'[a];[a][2:v]overlay=enable='gte(t,2.6)'[b];"
              "[b]trim=duration=7,setpts=PTS-STARTPTS,format=yuv420p[v1];[3:v]trim=duration=2,setpts=PTS-STARTPTS,fade=in:0:10,format=yuv420p[v2];"
              "[v1][v2]concat=n=2:v=1:a=0[v]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", f"{tmp}/bg.png", "-loop", "1", "-i", f"{tmp}/t1.png",
        "-loop", "1", "-i", f"{tmp}/t2.png", "-loop", "1", "-framerate", "30", "-i", f"{tmp}/fim.png",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", filtro, "-map", "[v]", "-map", "4:a",
        "-t", "9", "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-r", "30", "-c:a", "aac", "-b:a", "64k", "-shortest",
        "-movflags", "+faststart", out], check=True)

if __name__ == "__main__":
    tmp = sys.argv[1] if len(sys.argv) > 1 else "/tmp/reels"; os.makedirs(tmp, exist_ok=True)
    foto, tit, leg = POST31
    # post 31 no mesmo estilo dos outros
    src = open(os.path.join(AQUI, "gerar-imagens.py")).read().split("posts = json.load")[0]
    ns = {"__file__": os.path.join(AQUI, "gerar-imagens.py")}; exec(src, ns); ns["post"]({"imagem": foto, "titulo": tit}).save(os.path.join(SAIDA, "post-31.jpg"), "JPEG", quality=88)
    for i, s in enumerate(STORIES, 1): story(*s).save(os.path.join(SAIDA, f"story-{i:02d}.jpg"), "JPEG", quality=88)
    for i, r in enumerate(REELS, 1): reel(i, r[0], r[1], r[2], tmp)
    print("ok")
