# Stories, reels e o post 31 (10 dias a partir de 23/10/2026). Usado por gerar-midias.py e montar-fila.py.
C = "\n\n👉 Acesse o 3Tap: link na bio."
P = "\n\n👉 Cadastre-se como prestador: link na bio."
T = " #3Tap #ServiçosPertoDeVocê"
POST31 = ("soldador", "Solda, portão,\ngrade: resolvido.", "Soldador perto de você, com nota de quem já contratou e preço antes de chamar." + C + "\n\n#Soldador" + T)
# (foto, linha grande, linha pequena)
STORIES = [
 ("eletricista", "Precisou?\n3Tap.", "Profissionais perto de você em 3 toques"),
 ("limpeza", "Diarista\npra hoje?", "Veja quem está disponível agora"),
 ("pedreiro", "Prestador,\nvem pro 3Tap", "Cadastro grátis, pedidos perto de você"),
 ("encanador", "Vazou?\nChama.", "Encanador disponível agora"),
 ("manicure", "Agenda\nno app", "Escolha o dia e o horário"),
 ("pintor", "Nota real,\ncliente real", "Só avalia quem contratou"),
 ("jardineiro", "Orçamento\ncom foto", "Mande a foto pelo chat"),
 ("mecanico", "Seu preço,\nseu raio", "Prestador define tudo"),
 ("tecnico-ar-condicionado", "Calor?\n3Tap.", "Técnico de ar perto de você"),
 ("montador-de-moveis", "Móvel novo\nmontado hoje", "Disponível hoje ou agendado"),
 ("cuidador-de-idosos", "Confiança\nem primeiro", "Perfil e avaliações verificadas"),
 ("marido-de-aluguel", "Faz de tudo?\nTem cliente", "Receba pedidos perto de você"),
 ("frete-e-carreto", "Frete sem\ncomplicação", "Foto, preço e pronto"),
 ("cabeleireiro", "Verde = agora", "Amarelo = hoje · Azul = agendar"),
 ("dedetizacao", "Adeus,\nbaratas", "Dedetização agendada"),
 ("tecnico-de-informatica", "PC lento?", "Técnico de informática perto de você"),
 ("serralheiro", "Seu trabalho\naparece", "Sem pagar para aparecer"),
 ("lavagem-de-carro", "Carro limpo\nsem sair", "Lavagem no seu endereço"),
 ("passeador-de-caes", "Passeio\npro pet", "Passeador de cães perto de você"),
 ("churrasqueiro", "Churrasco\nno sábado?", "Churrasqueiro com agenda no app"),
]
# (foto, gancho, segunda frase, legenda)
REELS = [
 ("eletricista", "Chuveiro gelado?", "3 toques e chegou.", "Categoria, profissional, CHAMAR. Simples assim." + C + "\n\n#Eletricista" + T),
 ("pedreiro", "Prestador:", "sua reputação é seu maior ativo.", "Cada serviço concluído vira avaliação verificada no seu perfil." + P + "\n\n#Pedreiro #Prestador" + T),
 ("limpeza", "Casa limpa hoje?", "Diarista disponível agora.", "Combine tudo pelo chat do app, sem passar seu número." + C + "\n\n#Diarista" + T),
 ("encanador", "Vazamento?", "Encanador perto de você.", "Distância, nota e preço antes de chamar." + C + "\n\n#Encanador" + T),
 ("marido-de-aluguel", "Faz de tudo?", "O 3Tap te traz clientes.", "Cadastre seus serviços e seus preços." + P + "\n\n#MaridoDeAluguel #Prestador" + T),
 ("manicure", "Unha feita", "no horário que você escolher.", "Agenda da profissional direto no app." + C + "\n\n#Manicure" + T),
 ("pintor", "Pintura nova?", "Pintor com nota real.", "Só avalia quem contratou de verdade." + C + "\n\n#Pintor" + T),
 ("mecanico", "Mecânico?", "Você define preço e raio.", "O 3Tap leva os clientes até você." + P + "\n\n#Mecanico #Prestador" + T),
 ("jardineiro", "Quintal em dia", "com orçamento por foto.", "Mande a foto pelo chat e receba a proposta." + C + "\n\n#Jardinagem" + T),
 ("tecnico-ar-condicionado", "Ar parou?", "Técnico perto de você.", "Preço visível antes de contratar." + C + "\n\n#ArCondicionado" + T),
 ("serralheiro", "Trabalha bem?", "Sobe no ranking.", "Nota, avaliações e serviços concluídos, sem pagar para aparecer." + P + "\n\n#Serralheiro #Prestador" + T),
 ("montador-de-moveis", "Móvel novo?", "Montado hoje.", "Montador disponível hoje ou agendado." + C + "\n\n#MontadorDeMoveis" + T),
 ("cuidador-de-idosos", "Cuidado com", "quem você ama.", "Perfil completo e avaliações verificadas." + C + "\n\n#CuidadorDeIdosos" + T),
 ("frete-e-carreto", "Mudança?", "Frete com preço na hora.", "Foto do que vai levar e pronto." + C + "\n\n#Frete" + T),
 ("cabeleireiro", "Quer alguém já?", "Filtre por disponível agora.", "Verde é agora, amarelo é hoje, azul é agendar." + C + "\n\n#Cabeleireiro" + T),
 ("limpeza-de-piscina", "Autônomo?", "Seu negócio no bolso.", "Pedidos, conversa e agenda num lugar só." + P + "\n\n#Autônomo #Prestador" + T),
 ("desentupidor", "Pia entupida?", "Categoria, profissional, CHAMAR.", "Foto e detalhes você manda depois, pelo chat." + C + "\n\n#Desentupidora" + T),
 ("tecnico-de-celular", "Tela quebrada?", "Técnico perto de você.", "Distância e nota no card." + C + "\n\n#TecnicoDeCelular" + T),
 ("costureira", "Ajuste de roupa?", "Costureira perto de você.", "Avaliações verificadas de quem contratou." + C + "\n\n#Costureira" + T),
 ("instalacao-de-tv", "TV na parede?", "Hoje mesmo.", "Instalador disponível hoje, preço antes de contratar." + C + "\n\n#InstalacaoDeTV" + T),
]
