# Faz reels do @3tapbrasil com uma IA gratuita do PC (Gemini CLI ou Codex), sem gastar o Claude.
# Uso (PowerShell, na pasta do repositório 3tap):  .\instagram\fazer-reels.ps1 [-Quantos 4] [-IA gemini|codex]
# A IA cria os vídeos, põe na fila com "aprovado": false e para. O Carlos assiste e troca para true os que gostar,
# depois roda:  git add instagram; git commit -m "Reels novos"; git push   (o robô do GitHub publica sozinho)
param([int]$Quantos = 4, [string]$IA = "gemini")
$pedido = @"
Você está na pasta do site 3Tap (repositório cedu360/3tap). Crie $Quantos reels novos para o Instagram @3tapbrasil.
Regras:
- Vídeo MP4 vertical 1080x1920, 30 segundos, H.264 + AAC, usando ffmpeg (instale com 'winget install Gyan.FFmpeg' se faltar).
- Estrutura: gancho forte nos 3 primeiros segundos (problema do dia a dia: chuveiro queimou, vazamento, casa bagunçada,
  mudança, calor), depois 2 ou 3 telas reais do app de img/app/*.webp com movimento suave e uma legenda curta cada,
  e cartão final com o logo de marca/ e os textos "3Tap. Clicou, chegou." e "Link na bio · 3tapbrasil.com".
- Fotos de profissões: img/cat/*.webp. Se existir a pasta instagram/clipes/ com vídeos curtos (Runway, Meta AI), use-os no gancho.
- Cada reel com profissão diferente e visual diferente dos reels já em instagram/ (nada quase igual).
- Textos em português do Brasil. O 3Tap é para descobrir e contratar autônomos e pequenos prestadores perto de você;
  nunca diga "catálogo", "compre aqui" nem "baixe na loja" (o app ainda está em teste). Diga "Acesse grátis".
- Salve como instagram/reel-g-<profissão>-<AAAAMMDD>.mp4.
- Acrescente cada um no fim de instagram/fila.json neste formato, com "aprovado": false:
  {"tipo":"REELS","arquivo":"reel-g-....mp4","legenda":"<2 linhas + 👉 Acesse o 3Tap: link na bio. + 3 hashtags, uma com a profissão>","tema":"#<profissão>","aprovado":false}
- Não mexa em instagram/estado.json, não faça commit nem push. Ao terminar, liste os arquivos criados.
"@
git pull -q
if ($IA -eq "codex") { codex exec --full-auto $pedido } else { gemini --yolo -p $pedido }
Write-Host "`nPronto. Assista os reel-g-*.mp4 em instagram\, troque aprovado para true em instagram\fila.json nos que gostar e faça push."
