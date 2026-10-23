# Rotina diária do Instagram @3tapbrasil (sessão "Posts diários no Instagram", ambiente IG_TOKEN)

Cinco horários por dia, horário de Brasília. Em cada um: `cd /mnt/project-files/marketing/instagram-auto && node publicar.mjs <turno>`

| Horário | Turno  | O que sai          |
|---------|--------|--------------------|
| 09h37   | manha  | 1 foto + 1 story   |
| 11h47   | reel1  | 1 reel             |
| 14h07   | tarde  | 1 foto + 1 story   |
| 16h47   | reel2  | 1 reel             |
| 19h37   | noite  | 1 foto + 1 story   |

Total por dia: no máximo 3 fotos, 3 stories e 2 reels (o script conta no próprio perfil e para no limite).

Antes de publicar, o script lê o perfil e pula o que repetiria: mesma imagem, legenda parecida com post recente,
ou a mesma profissão nas últimas 24 h (essa só é adiada). `node publicar.mjs <turno> --teste` mostra o que sairia.
A fila.json é só a ordem de preferência; o script pega o próximo item que passa nas verificações.
Se aparecer "nada novo na fila", falta conteúdo: avisar o thread "Instagram e anúncios do CHAMA".
Nunca imprimir, copiar ou gravar o token. Se der erro, não repetir; relatar em uma linha.
