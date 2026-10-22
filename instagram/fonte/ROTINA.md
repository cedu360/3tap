# Rotina diária do Instagram @3tapbrasil (para a sessão que roda no ambiente IG_TOKEN)

Ambiente: "IG_TOKEN" (env_01TzSEUs5TtDr2fzY4isgT9j), com a variável IG_TOKEN e rede liberada para graph.instagram.com.

Todo dia às 10h37 de Brasília (cron `CRON_TZ=America/Sao_Paulo 37 10 * * *`):
1. Copiar `publicar.mjs` e `legendas.json` desta pasta para $HOME/ig (se esta pasta não existir na sessão, os mesmos arquivos estão em github.com/cedu360/3tap, pasta instagram/).
2. `cd $HOME/ig && node publicar.mjs` (sem argumento). Publica o post do dia (ciclo de 30 desde 22/10/2026), no máximo 1 por dia, e renova o token.
3. Nunca imprimir, copiar ou gravar o token. Se der erro, não repetir; relatar o erro em uma linha.

As imagens já estão em https://3tapbrasil.com/instagram/post-01.jpg a post-30.jpg.
