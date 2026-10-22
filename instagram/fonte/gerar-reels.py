# Reels de 30 s (1080x1920): gancho com foto (6 s), 3 telas do app com o passo do site (6 s cada), final com logo (6 s).
# Uso: python3 gerar-reels.py <pasta-temporária> [números...]
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
from conteudo_extra import REELS
import importlib.util
AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("gm", os.path.join(AQUI, "gerar-midias.py")); gm = importlib.util.module_from_spec(spec); spec.loader.exec_module(gm)
TELAS = os.environ.get("TELAS_APP", "/home/user/3tap/img/app")
CLIENTE = [("1 · Encontre", "Veja quem está perto e disponível", "buscar"),
           ("2 · Converse e combine", "Foto, vídeo e áudio no mesmo chat", "chat"),
           ("3 · Acompanhe", "Do primeiro toque à conclusão", "acompanhar")]
PRESTADOR = [("1 · Cadastre seus serviços", "Seus preços, seu raio, sua agenda", "prestador"),
             ("2 · Receba pedidos", "Clientes perto de você chamam pelo app", "servico"),
             ("3 · Construa sua reputação", "Avaliações de quem contratou de verdade", "perfil")]

def tela(titulo, sub, nome):
    c = gm.Image.new("RGB", (1080, 1920), gm.FUNDO); d = ImageDraw.Draw(c)
    ft, _ = gm.caber(d, [titulo], gm.BOLD, 76, 980); d.text((540, 170), titulo, font=ft, fill="white", anchor="mm")
    d.text((540, 265), sub, font=gm.fonte(gm.MED, 44), fill=(255, 178, 31), anchor="mm")
    s = Image.open(os.path.join(TELAS, nome + ".webp")).convert("RGB"); s = s.resize((int(s.width * 1380 / s.height), 1380), Image.LANCZOS)
    m = Image.new("L", s.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, s.width - 1, s.height - 1), 48, fill=255)
    x, y = (1080 - s.width) // 2, 380
    sombra = Image.new("RGBA", (1080, 1920)); ImageDraw.Draw(sombra).rounded_rectangle((x - 6, y - 6, x + s.width + 6, y + s.height + 6), 54, fill=(255, 106, 0, 120))
    c.paste(sombra.filter(ImageFilter.GaussianBlur(18)), (0, 0), sombra.filter(ImageFilter.GaussianBlur(18)))
    c.paste(s, (x, y), m); return c

def final():
    c = gm.Image.new("RGB", (1080, 1920), gm.FUNDO); gm.por_logo(c, 820, 560); d = ImageDraw.Draw(c)
    d.text((540, 1020), "Precisou de um profissional?", font=gm.fonte(gm.BOLD, 62), fill="white", anchor="mm")
    d.text((540, 1110), "3Tap.", font=gm.fonte(gm.BOLD, 62), fill=(255, 106, 0), anchor="mm")
    d.rounded_rectangle((290, 1300, 790, 1410), 55, fill=(255, 106, 0)); d.text((540, 1355), "Link na bio", font=gm.fonte(gm.BOLD, 50), fill="white", anchor="mm")
    d.text((540, 1500), "3tapbrasil.com", font=gm.fonte(gm.MED, 46), fill=(205, 210, 222), anchor="mm"); return c

def reel(i, foto, gancho, frase, legenda, tmp):
    gm.fundo_vertical(foto).save(f"{tmp}/bg.png")
    for nome, txt, y, tamb in (("t1", gancho, 1250, 120), ("t2", frase, 1420, 78)):
        o = Image.new("RGBA", (1080, 1920)); d = ImageDraw.Draw(o); f, _ = gm.caber(d, [txt], gm.BOLD, tamb, 960)
        d.text((60, y), txt, font=f, fill="white" if nome == "t1" else (255, 178, 31)); o.save(f"{tmp}/{nome}.png")
    passos = PRESTADOR if "#Prestador" in legenda else CLIENTE
    for k, p in enumerate(passos): tela(*p).save(f"{tmp}/s{k}.png")
    final().save(f"{tmp}/fim.png")
    ins = ["-loop", "1", "-i", f"{tmp}/bg.png", "-loop", "1", "-i", f"{tmp}/t1.png", "-loop", "1", "-i", f"{tmp}/t2.png"]
    for k in range(3): ins += ["-loop", "1", "-framerate", "30", "-i", f"{tmp}/s{k}.png"]
    ins += ["-loop", "1", "-framerate", "30", "-i", f"{tmp}/fim.png", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
    z = "zoompan=z='1+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=180:s=1080x1920:fps=30"
    f = (f"[0:v]scale=1188:-1,{z.replace('0.0008','0.0016')}[bg];[bg][1:v]overlay=enable='gte(t,0.5)'[a];[a][2:v]overlay=enable='gte(t,2.2)',trim=duration=6,setpts=PTS-STARTPTS,format=yuv420p[p0];")
    for k in range(3): f += f"[{3+k}:v]scale=1188:-1,{z},trim=duration=6,setpts=PTS-STARTPTS,fade=in:0:8,format=yuv420p[p{k+1}];"
    f += "[6:v]trim=duration=6,setpts=PTS-STARTPTS,fade=in:0:10,format=yuv420p[p4];[p0][p1][p2][p3][p4]concat=n=5:v=1:a=0[v]"
    out = os.path.join(gm.SAIDA, f"reel-{i:02d}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", f, "-map", "[v]", "-map", "7:a", "-t", "30",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-r", "30", "-c:a", "aac", "-b:a", "64k", "-shortest",
                    "-movflags", "+faststart", out], check=True)

if __name__ == "__main__":
    tmp = sys.argv[1]; os.makedirs(tmp, exist_ok=True)
    nums = [int(x) for x in sys.argv[2:]] or range(1, len(REELS) + 1)
    for i in nums: reel(i, *REELS[i - 1], tmp)
    print("ok", list(nums))
