# Monta fila.json: 10 dias a partir de 23/10/2026; manhã foto+story, tarde foto+reel, noite foto+story+reel.
import json, os, datetime
from conteudo_extra import POST31, REELS
AQUI = os.path.dirname(os.path.abspath(__file__))
leg = json.load(open(os.path.join(AQUI, "legendas.json"))) + [POST31[2]]
inicio = datetime.date(2026, 10, 23); fila = []; f = 2; r = 1; s = 1
for d in range(10):
    dia = (inicio + datetime.timedelta(d)).isoformat()
    for turno, tipos in (("manha", "FS"), ("tarde", "FR"), ("noite", "FSR")):
        for t in tipos:
            if t == "F": fila.append({"dia": dia, "turno": turno, "tipo": "FEED", "arquivo": f"post-{f:02d}.jpg", "legenda": leg[f - 1]}); f += 1
            if t == "S": fila.append({"dia": dia, "turno": turno, "tipo": "STORIES", "arquivo": f"story-{s:02d}.jpg"}); s += 1
            if t == "R": fila.append({"dia": dia, "turno": turno, "tipo": "REELS", "arquivo": f"reel-{r:02d}.mp4", "legenda": REELS[r - 1][3]}); r += 1
json.dump(fila, open(os.path.join(AQUI, "fila.json"), "w"), ensure_ascii=False, indent=1)
print(len(fila), "itens até", fila[-1]["dia"])
