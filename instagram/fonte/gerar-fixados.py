# 2 posts para fixar (fixado-*.jpg, 1080x1350) e o story do destaque Dúvidas.
import os, importlib.util
from PIL import Image, ImageDraw
AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("gm", os.path.join(AQUI, "gerar-midias.py")); gm = importlib.util.module_from_spec(spec); spec.loader.exec_module(gm)
emb = Image.open(os.path.join(gm.KIT, "emblema.png")).convert("RGBA")

def arte(W, H, titulo, itens, rodape, saida, y0, tamt=92, passo=104):
    c = Image.new("RGB", (W, H), gm.FUNDO); d = ImageDraw.Draw(c)
    e = emb.copy(); e.thumbnail((380, 290), Image.LANCZOS); c.paste(e, ((W - e.width) // 2, y0), e)
    y = y0 + e.height + 50
    for l in titulo.split("\n"):
        f, _ = gm.caber(d, [l], gm.BOLD, tamt, W - 120); d.text((W // 2, y), l, font=f, fill="white", anchor="mm"); y += tamt + 14
    d.rounded_rectangle((W // 2 - 70, y, W // 2 + 70, y + 12), 6, fill=gm.LARANJA); y += 70
    for it in itens:
        d.ellipse((100, y + 14, 126, y + 40), fill=gm.LARANJA); f, _ = gm.caber(d, [it], gm.MED, 48, W - 230); d.text((156, y), it, font=f, fill=(230, 233, 240)); y += passo
    d.rounded_rectangle((W // 2 - 260, H - 190, W // 2 + 260, H - 85), 52, fill=gm.LARANJA)
    d.text((W // 2, H - 137), rodape, font=gm.fonte(gm.BOLD, 46), fill="white", anchor="mm")
    c.save(os.path.join(gm.SAIDA, saida), "JPEG", quality=90)

arte(1080, 1350, "Contrate com\nconfiança", ["Avaliações só de quem contratou", "Pagamento pelo app, registrado no pedido", "Seu número fica privado", "Reportar problema direto no app"], "Link na bio", "fixado-confianca.jpg", 70)
arte(1080, 1350, "Seja prestador\nno 3Tap", ["Cadastro grátis", "Seus preços, seu raio, sua agenda", "Pedidos de clientes perto de você", "Sua reputação é seu maior ativo"], "Link na bio", "fixado-prestador.jpg", 70)
arte(1080, 1920, "Dúvidas", ["Quanto custa? Cadastro grátis", "Preço aparece antes de contratar", "Funciona em qualquer cidade", "Conversa só pelo chat do app", "Deu problema? Reporte no pedido"], "Link na bio", "destaque-duvidas.jpg", 380, 110, 130)
print("ok")
