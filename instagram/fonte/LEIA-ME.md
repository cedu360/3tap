# Posts automáticos no Instagram @3tapbrasil

Mesmo resultado do ChatFyre, pelo caminho oficial: a API de publicação do Instagram (Instagram API com login do Instagram). Sem senha: a conta autoriza um app da Meta e gera um token.

## O que já está pronto
- `calendario.py` → `posts.json`: 30 posts (legenda + hashtags), alternando clientes e prestadores. Edite e rode de novo.
- `gerar-imagens.py` → `imagens/post-NN.jpg` (1080x1350): foto da profissão, título e logo 3Tap.
- As imagens estão no ar em https://3tapbrasil.com/instagram/post-NN.jpg (repositório cedu360/3tap, pasta `instagram/`). A API precisa delas num endereço público.
- `publicar.mjs`: publica o post do dia (ciclo de 30 dias a partir de 23/10/2026) e renova o token. Uso: `IG_TOKEN=... node publicar.mjs [n]`.

## O que só o Carlos faz (uma vez)
1. No app do Instagram: @3tapbrasil > Configurações > Tipo de conta > **Mudar para conta profissional > Empresa**.
2. Em developers.facebook.com: Criar app > caso de uso "Gerenciar mensagens e conteúdo no Instagram" > Configuração da API com login do Instagram > **Adicionar conta** (@3tapbrasil) > **Gerar token**.
3. Colar o token em Configurações do projeto > Ambiente, como variável secreta `IG_TOKEN` (nunca no chat).

Depois disso uma rotina diária roda `publicar.mjs` às 11h de Brasília.

## Cuidados
- O token vale 60 dias; o script renova a cada post. Se um dia falhar com token expirado, gerar outro no passo 2.
- Limite da Meta: 100 posts por dia (usamos 1).
- Post 14 ("Pagamento protegido") fala de um recurso que ainda é simulado no app: tirar ou adiar até os pagamentos reais.

## Novos posts feitos no ChatGPT ou Gemini
Cole este pedido lá e salve a resposta como `posts.json` nesta pasta (substitui o atual):

> Crie N posts para o Instagram do 3Tap, app que conecta clientes a profissionais autônomos perto de você (eletricista, diarista, encanador etc.). Slogan: "Clicou, chegou." Sem telefone nem WhatsApp. Alterne posts para clientes e para prestadores ("Sua reputação é seu maior ativo"). Responda só com JSON: uma lista de objetos {"n": número a partir de 1, "imagem": uma destas profissões: eletricista, limpeza, encanador, pedreiro, pintor, manicure, jardineiro, mecanico, cabeleireiro, marido-de-aluguel, montador-de-moveis, frete-e-carreto, babysitter, cuidador-de-idosos, "titulo": até 2 linhas curtas separadas por \n, "legenda": legenda com chamada "link na bio" e hashtags, "arquivo": "post-NN.jpg"}.

Depois rode `python3 gerar-imagens.py` e as imagens novas sobem para o site junto com o resto.
