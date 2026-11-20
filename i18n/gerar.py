"""Gera en/index.html e es/index.html a partir do index.html (português) e de i18n/textos.py.
O index.html continua sendo o original; as cópias em inglês e espanhol nunca são editadas à mão."""
import re,sys,html as H
import os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from textos import T
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')+'/'
src=open(R+'index.html').read()
REDIR='''<script>(function(){try{if(/bot|crawl|spider|slurp|lighthouse|preview/i.test(navigator.userAgent))return;if(/[?&]lang=/.test(location.search))return;var l=((navigator.languages&&navigator.languages[0])||navigator.language||'pt').toLowerCase();var w=l.indexOf('pt')===0?'':(l.indexOf('es')===0?'es/':'en/');if(w!=='%s')location.replace('/'+w+location.hash);}catch(e){}})();</script>
<link rel="alternate" hreflang="pt-BR" href="https://3tapbrasil.com/">
<link rel="alternate" hreflang="en" href="https://3tapbrasil.com/en/">
<link rel="alternate" hreflang="es" href="https://3tapbrasil.com/es/">
<link rel="alternate" hreflang="x-default" href="https://3tapbrasil.com/en/">'''
def head_insert(s,cur):
    s=re.sub(r'<script>\(function\(\)\{try\{if\(/bot.*?</script>\n(<link rel="alternate".*?\n){4}','',s,flags=re.S)
    return s.replace('<meta charset="utf-8">','<meta charset="utf-8">\n'+(REDIR%cur),1)
pt=head_insert(src,'')
open(R+'index.html','w').write(pt)
miss=set()
def tr(s,k,cur,lang):
    d={}
    for row in T: d[row[0]]=row[k]
    # sort by length desc
    keys=sorted(d,key=len,reverse=True)
    def esc_variants(t): return {t, H.escape(t,quote=False), t.replace('“','&ldquo;').replace('”','&rdquo;')}
    # text nodes
    def rep_text(m):
        pre,txt,post=m.group(1),m.group(2),m.group(3)
        raw=H.unescape(txt)
        if raw in d: return pre+H.escape(d[raw],quote=False)+post
        if '<' not in txt and ('“' in raw):
            parts=re.split('([“”])',raw); out=[]
            for p in parts:
                st=p.strip()
                if st and any(c.isalpha() for c in st):
                    if st in d: out.append(p.replace(st,d[st]))
                    else: miss.add(st); out.append(p)
                else: out.append(p)
            return pre+H.escape(''.join(out),quote=False).replace('“','&ldquo;').replace('”','&rdquo;')+post
        if any(c.isalpha() for c in raw) and 'function' not in raw and 'var ' not in raw: miss.add(raw)
        return m.group(0)
    s=re.sub(r'(>\s*)([^<>]*?[^\s<>][^<>]*?)(\s*<)',rep_text,s)
    def rep_attr(m):
        a,v=m.group(1),m.group(2); raw=H.unescape(v)
        if raw in d: return f'{a}="{H.escape(d[raw])}"'
        return m.group(0)
    s=re.sub(r'\b(alt|aria-label|placeholder|title|content)="([^"]*)"',rep_attr,s)
    for p in ['Na App Store','Para Android','Tocar o vídeo','Pausar o vídeo']:
        s=s.replace("'"+p+"'","'"+d[p]+"'")
    s=s.replace('<html lang="pt-BR">',f'<html lang="{lang}">')
    s=s.replace('<link rel="canonical" href="https://3tapbrasil.com/">',f'<link rel="canonical" href="https://3tapbrasil.com/{cur}">')
    s=s.replace('<meta property="og:url" content="https://3tapbrasil.com/">',f'<meta property="og:url" content="https://3tapbrasil.com/{cur}">')
    s=head_insert(s,cur)
    # relative paths -> ../
    def rel(m):
        a,v=m.group(1),m.group(2)
        if re.match(r'(https?:|mailto:|#|/|data:|tel:)',v) or v=='' : return m.group(0)
        return f'{a}="../{v}"'
    s=re.sub(r'\b(src|href|poster|srcset)="([^"]*)"',rel,s)
    for n in ['explorar-cidade','explorar-produtos','empresa','agendar']: s=s.replace(f'img/telas/{n}.webp',f'img/telas/'+lang+f'/{n}.webp')
    s=s.replace('url(img/','url(../img/').replace("'android/3tap.apk'","'../android/3tap.apk'")
    return s
for k,cur,lang in [(1,'en/','en'),(2,'es/','es')]:
    import os; os.makedirs(R+cur,exist_ok=True)
    open(R+cur+'index.html','w').write(tr(src,k,cur,lang))
skip={'Tap','3Tap','3Tap Shop','Pro','Premium','Shop','App Store (iPhone)','Android (APK)','3tap.apk','cedu@3tapbrasil.com','Instagram @3tapbrasil','Cookies','website','summary_large_image','R$ 59,90','R$ 119,90','R$ 129,90','R$ 249,90','R$ 399,90','R$ 252,00','width=device-width, initial-scale=1, viewport-fit=cover','Pix'}
faltam=sorted(m for m in miss if m not in skip and 'r.top' not in m)
print('Textos sem tradução:' if faltam else 'Tudo traduzido.', faltam or '')
