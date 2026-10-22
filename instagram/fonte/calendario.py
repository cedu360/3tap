# Calendário de 30 posts do @3tapbrasil. Gera posts.json (legendas) para o gerador de imagens e o publicador.
import json, os
H = "\n\n#3Tap #ServiçosPertoDeVocê #Autônomo #ProfissionalDeConfiança"
C = "\n\n👉 Acesse o 3Tap: link na bio."
P = "\n\n👉 Cadastre-se como prestador: link na bio."
posts = [
 ("kit:clicou-chegou", None, "Precisou de um profissional? 3Tap. Abriu, escolheu, chamou: profissionais perto de você em 3 toques."+C, "#Lançamento"),
 ("eletricista", "Tomada sem energia?\nChama um eletricista.", "Disjuntor caindo, tomada queimada, chuveiro que não esquenta. No 3Tap você vê quem está disponível agora perto de você, com nota real de quem contratou."+C, "#Eletricista"),
 ("limpeza", "Casa limpa\nsem ligar pra ninguém.", "Diarista para hoje ou agendada para o dia que você escolher. Combine tudo pelo chat do app, sem passar seu número."+C, "#Diarista #Limpeza"),
 ("pedreiro", "Sua reputação é\nseu maior ativo.", "Prestador: no 3Tap cada serviço concluído vira avaliação verificada no seu perfil. Quanto melhor seu trabalho, mais você aparece."+P, "#Pedreiro #Prestador"),
 ("encanador", "Vazamento não espera.", "Encanador disponível agora, perto de você. Você vê a distância, a nota e o preço antes de chamar."+C, "#Encanador"),
 ("kit:simples-e-agil", None, "Simples e ágil: encontre, converse, combine e contrate num pedido só. Fotos, vídeo, áudio e localização no mesmo chat."+C, "#ComoFunciona"),
 ("manicure", "Unha feita\nno seu horário.", "Escolha o dia e o horário na agenda da profissional e pronto. Sem troca de mensagens infinita."+C, "#Manicure #Beleza"),
 ("pintor", "Pintor com nota\nde quem contratou.", "No 3Tap só avalia quem contratou de verdade. Nota real, de cliente real."+C, "#Pintor #Reforma"),
 ("marido-de-aluguel", "Faz de tudo?\nO 3Tap te chama.", "Prateleira, chuveiro, cortina, pequenos reparos. Cadastre seus serviços e seus preços e receba pedidos de clientes perto de você."+P, "#MaridoDeAluguel #Prestador"),
 ("jardineiro", "Quintal em dia.", "Jardineiro para corte de grama, poda e manutenção. Peça orçamento com foto pelo chat e receba a proposta no app."+C, "#Jardinagem"),
 ("tecnico-ar-condicionado", "Ar-condicionado\nparou no calor?", "Técnico de ar-condicionado perto de você, com preço visível antes de contratar."+C, "#ArCondicionado"),
 ("montador-de-moveis", "Móvel novo,\nmontado hoje.", "Montador de móveis disponível hoje ou na data que você escolher."+C, "#MontadorDeMoveis"),
 ("cuidador-de-idosos", "Cuidado com\nquem você ama.", "Veja avaliações verificadas, serviços concluídos e o perfil completo antes de contratar um cuidador."+C, "#CuidadorDeIdosos"),
 ("instalador", "Pagamento protegido.", "No 3Tap o valor só vai para o profissional quando você confirma que o serviço foi feito. Deu problema? Você abre uma disputa pelo app."+C, "#PagamentoSeguro"),
 ("mecanico", "Mecânico perto\nde você.", "Prestador: você define seu preço, seu raio de atendimento e quando está disponível. O 3Tap leva os clientes até você."+P, "#Mecanico #Prestador"),
 ("frete-e-carreto", "Frete e carreto\nsem complicação.", "Mande foto do que vai levar pelo chat e receba o preço. Tudo registrado no pedido."+C, "#Frete #Mudança"),
 ("babysitter", "Babá de confiança.", "Perfil, avaliações de quem já contratou e conversa dentro do app. Confiança antes de tudo."+C, "#Baba"),
 ("dedetizacao", "Adeus, baratas.", "Dedetização agendada no dia e horário que você escolher."+C, "#Dedetizacao"),
 ("cabeleireiro", "Disponível agora:\nverde. Hoje: amarelo.", "No 3Tap a disponibilidade é real: verde é agora, amarelo é hoje, azul é agendar. Quer alguém já? Filtre por disponível agora."+C, "#Cabeleireiro"),
 ("tecnico-de-celular", "Celular quebrado?", "Técnico de celular perto de você, com distância e nota no card."+C, "#TecnicoDeCelular"),
 ("serralheiro", "Seu trabalho merece\nser encontrado.", "Sem pagar para aparecer: no 3Tap quem trabalha bem sobe no ranking por nota, avaliações e serviços concluídos."+P, "#Serralheiro #Prestador"),
 ("lavagem-de-estofados", "Sofá novo de novo.", "Lavagem de estofados com preço público antes de contratar: fixo, por unidade ou a partir de."+C, "#LavagemDeSofa"),
 ("personal-trainer", "Treino com\nhora marcada.", "Personal trainer com agenda no app: escolha o dia e o horário."+C, "#PersonalTrainer"),
 ("desentupidor", "Pia entupida?\n3 toques.", "Categoria, profissional, CHAMAR. Foto e detalhes você manda depois, pelo chat."+C, "#Desentupidora"),
 ("costureira", "Ajuste de roupa\nsem sair caçando.", "Costureira perto de você, com avaliações verificadas."+C, "#Costureira"),
 ("instalacao-de-tv", "TV na parede hoje.", "Instalador disponível hoje, com preço antes de contratar."+C, "#InstalacaoDeTV"),
 ("limpeza-de-piscina", "Autônomo? Seu\nnegócio no bolso.", "Pedidos, conversa, agenda e recebimento num lugar só. Cadastre-se grátis como prestador."+P, "#LimpezaDePiscina #Prestador"),
 ("fotografo", "Fotógrafo para\nseu evento.", "Peça orçamento com a data e receba a proposta pelo app."+C, "#Fotografo"),
 ("vidraceiro", "Vidro quebrado,\nresolvido.", "Vidraceiro perto de você, com foto do serviço no chat para orçar certo."+C, "#Vidraceiro"),
 ("kit:clicou-chegou", None, "Uma conta, dois papéis: você contrata e também pode oferecer seus serviços. Troca entre cliente e prestador com um toque."+C, "#3Tap"),
]
out = []
for i, (img, titulo, legenda, tags) in enumerate(posts, 1):
    out.append({"n": i, "imagem": img, "titulo": titulo, "legenda": legenda + "\n\n" + tags + " " + H.strip(), "arquivo": f"post-{i:02d}.jpg"})
here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here, "posts.json"), "w"), ensure_ascii=False, indent=1)
print(len(out), "posts")
