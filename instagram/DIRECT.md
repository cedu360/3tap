# Robô do direct (instagram/direct.mjs)

Responde no direct quem comenta um post ou responde um story da @3tapbrasil:
1. "Oi! Que bom te ver por aqui 😊 Você trabalha com o quê?" (em comentário, também responde no post "Te chamei no direct! 😉")
2. Depois da resposta: convite para seguir e se cadastrar grátis no 3Tap. Depois fica quieto; a conversa segue com o Carlos.

Nunca escreve para quem só visualizou (a API oficial não permite). Textos em `TEXTO` no arquivo.

## Ligar (uma vez)
1. Railway: novo serviço a partir do repo cedu360/3tap, comando `node instagram/direct.mjs`, com domínio público.
   Variáveis: IG_DM_TOKEN, IG_APP_SECRET (chave secreta do app 3tap-IG), IG_VERIFY (palavra qualquer).
   Para guardar o passo de cada pessoa entre reinícios, volume montado e IG_DM_ESTADO=/data/direct-estado.json.
2. IG_DM_TOKEN: gerar no painel do app (Instagram > Configuração da API com login do Instagram > Gerar token)
   com as permissões instagram_business_basic, instagram_business_manage_messages e instagram_business_manage_comments.
   O serviço renova o token sozinho todo dia enquanto estiver ligado.
3. Webhooks no mesmo painel: URL `https://<domínio do serviço>/`, token de verificação = IG_VERIFY;
   assinar os campos `messages` e `comments`.
4. Para funcionar com qualquer pessoa (não só contas de teste do app): Análise do app pedindo acesso avançado a
   instagram_business_manage_messages e instagram_business_manage_comments, com vídeo mostrando o robô respondendo.
   Enquanto não for aprovado, só responde a contas com função no app.
5. Teste: comentar num post com outra conta; deve chegar o direct.
