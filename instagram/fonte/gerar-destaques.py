# 4 stories para os destaques do perfil (destaque-*.jpg, 1080x1920).
import os, importlib.util
from PIL import Image, ImageDraw
AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("gm", os.path.join(AQUI, "gerar-midias.py")); gm = importlib.util.module_from_spec(spec); spec.loader.exec_module(gm)
D = [
 ("como-funciona", "Como funciona", ["Conte o que você precisa", "Veja quem está perto e disponível", "Converse e combine pelo chat", "Contrate e acompanhe", "Conclua e avalie"]),
 ("profissionais", "Profissionais", ["Eletricista, encanador, diarista", "Pedreiro, pintor, manicure", "Montador, jardineiro, técnicos", "Em qualquer cidade, perto de você", "Nota de quem contratou de verdade"]),
 ("seguranca", "Segurança", ["Avaliações só de quem contratou", "Tudo registrado no pedido", "Seu número fica privado", "Reportar problema pelo app", "Perfil claro e honesto"]),
 ("seja-prestador", "Seja prestador", ["Cadastro grátis", "Seus preços, seu raio, sua agenda", "Pedidos de clientes perto de você", "Sem pagar para aparecer", "Sua reputação é seu maior ativo"]),
]
emb = Image.open(os.path.join(gm.KIT, "emblema.png")).convert("RGBA"); emb.thumbnail((520, 400), Image.LANCZOS)
for slug, titulo, itens in D:
    c = Image.new("RGB", (1080, 1920), gm.FUNDO); d = ImageDraw.Draw(c)
    c.paste(emb, ((1080 - emb.width) // 2, 230), emb)
    d.text((540, 760), titulo, font=gm.fonte(gm.BOLD, 104), fill="white", anchor="mm")
    d.rounded_rectangle((470, 840, 610, 852), 6, fill=gm.LARANJA)
    y = 960
    for it in itens:
        d.ellipse((110, y + 14, 138, y + 42), fill=gm.LARANJA); d.text((170, y), it, font=gm.fonte(gm.MED, 52), fill=(230, 233, 240)); y += 118
    d.rounded_rectangle((290, 1640, 790, 1750), 55, fill=gm.LARANJA); d.text((540, 1695), "Link na bio", font=gm.fonte(gm.BOLD, 50), fill="white", anchor="mm")
    d.text((540, 1820), "3tapbrasil.com", font=gm.fonte(gm.MED, 42), fill=(160, 168, 185), anchor="mm")
    c.save(os.path.join(gm.SAIDA, f"destaque-{slug}.jpg"), "JPEG", quality=90)
print("ok")
