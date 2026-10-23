from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, tempfile
DAYS=[
("2026-10-26","Fundamentos da Auditoria","OBJECTIVO","RISCO","CONTROLO","Primeiro compreende o processo"),
("2026-10-27","Auditoria vs Compliance","AVALIAR","CUMPRIR","COMPROVAR","Funções distintas e complementares"),
("2026-10-28","Riscos empresariais","IDENTIFICAR","AVALIAR","RESPONDER","Risco não significa problema certo"),
("2026-10-29","Segregação de funções","AUTORIZAR","EXECUTAR","REVER","Uma pessoa não deve controlar tudo"),
("2026-10-30","Fraudes e prevenção","CONFERIR","INVESTIGAR","REGISTAR","Nem todo erro é fraude"),
("2026-10-31","Evidências e documentos","DOCUMENTO","REGISTO","CONFIRMAÇÃO","Opiniões não substituem provas"),
("2026-11-01","Competências do auditor","ANALISAR","DOCUMENTAR","COMUNICAR","Aprende a fazer boas perguntas"),
("2026-11-02","Caixa e pagamentos","APROVAR","REGISTAR","CONCILIAR","Caixa certo exige comprovativos"),
("2026-11-03","Inventário e existências","RECEBER","CONTAR","CONFERIR","O sistema coincide com o stock?"),
("2026-11-04","Erros de gestão","PLANEAR","REGISTAR","REVER","Decidir sem dados cria riscos"),
("2026-11-05","Ética profissional","RESPEITO","SIGILO","OBJECTIVIDADE","Informação exige responsabilidade"),
("2026-11-06","Relatórios de auditoria","FACTO","EVIDÊNCIA","RECOMENDAÇÃO","O relatório deve ser claro"),
("2026-11-07","Aprendizagem em auditoria","CONCEITO","PRÁTICA","REVISÃO","Ninguém começa sabendo tudo"),
("2026-11-08","Melhoria contínua","OBSERVAR","AJUSTAR","MEDIR","Um processo pode melhorar"),
("2026-11-09","Dúvidas sobre auditoria","RISCO","CONTROLO","PROCESSO","Auditoria não é só fraude"),
("2026-11-10","Escolher uma formação","PROGRAMA","PREÇO","CONDIÇÕES","Confirma a oferta antes de pagar"),
("2026-11-11","Revisão da campanha","RISCO","CONTROLO","EVIDÊNCIA","Transforma ideias em prática")
]
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUT=Path("assets/nc7_v25")
OUT.mkdir(parents=True,exist_ok=True)
def ff(size,b=False): return ImageFont.truetype(BOLD if b else FONT,size)
def lines(d,text,font,width):
 out=[];s=""
 for word in text.split():
  new=(s+" "+word).strip()
  if d.textbbox((0,0),new,font=font)[2]>width and s: out.append(s);s=word
  else:s=new
 if s:out.append(s)
 return out
def art(date,head,detail,tag,portrait=False,style=0):
 w,h=(540,960) if portrait else (1080,1080)
 cols=[("#091626","#122d41","#77e5cb"),("#10172a","#302442","#f0c98b"),("#082135","#1b4150","#a1ddff")]
 top,bottom,accent=cols[style%3]
 ca=tuple(int(top[i:i+2],16) for i in (1,3,5))
 cb=tuple(int(bottom[i:i+2],16) for i in (1,3,5))
 strip=Image.new("RGB",(1,h));px=strip.load()
 for yy in range(h):
  k=yy/h*.85;px[0,yy]=tuple(int(ca[i]*(1-k)+cb[i]*k) for i in range(3))
 im=strip.resize((w,h));d=ImageDraw.Draw(im)
 s=w/1080;p=int(75*s);y0=int(85*s)
 d.rounded_rectangle((p,y0,p+int(160*s),y0+int(9*s)),radius=4,fill=accent)
 for z in range(5):
  r=int((220+75*z)*s);x=w-int(30*s);y=int(360*s)
  d.ellipse((x-r,y-r,x+r,y+r),outline=accent,width=max(1,int(2*s)))
 d.text((p,y0+int(30*s)),"NÚCLEO CONTROLO 7",font=ff(int(30*s),True),fill="white")
 d.text((p,y0+int(82*s)),"AUDITORIA · CONTROLO · RISCO",font=ff(int(18*s)),fill="#c6dce2")
 yy=int(h*.31)
 font=ff(int(65*s),True)
 for line in lines(d,head,font,w-2*p)[:5]:
  d.text((p,yy),line,font=font,fill="white");yy+=int(83*s)
 yy+=int(20*s)
 d.rounded_rectangle((p,yy,w-p,yy+max(3,int(8*s))),radius=3,fill=accent)
 yy+=int(50*s)
 font=ff(int(34*s))
 for line in lines(d,detail,font,w-2*p)[:6]:
  d.text((p,yy),line,font=font,fill="#d1e4ed");yy+=int(51*s)
 d.text((p,h-int(125*s)),date+"  /  JORNADA PLANETÁRIA",font=ff(int(20*s)),fill=accent)
 d.text((p,h-int(82*s)),tag,font=ff(int(21*s),True),fill="white")
 return im
for day,theme,a,b,c,hook in DAYS:
 images=[("0900",hook,a+"  /  "+b+"  /  "+c,"CONCEITO"),
         ("1400",b+" + "+c,theme+": o que verificar?","CHECKLIST"),
         ("2030","APRENDE "+theme.upper(),"Consulta o programa e as condições na legenda.","FORMAÇÃO • AFILIADO")]
 for style,(time,h,detail,tag) in enumerate(images):
  path=OUT/(day+"_"+time+".png")
  if not path.exists():art(day,h,detail,tag,style=style).save(path,optimize=True)
 reels=[("1115",hook,a+" → "+b,"Pratica e aprende"),
        ("1600","3 IDEIAS SOBRE "+theme.upper(),a+" • "+b+" • "+c,"Segue o Núcleo Controlo 7"),
        ("2200","QUERES APRENDER AUDITORIA?",theme,"Vê o link de afiliado na legenda")]
 for style,(time,h1,h2,h3) in enumerate(reels):
  path=OUT/(day+"_"+time+".mp4")
  if path.exists():continue
  with tempfile.TemporaryDirectory() as td:
   ins=[]
   for j,title in enumerate((h1,h2,h3)):
    frame=Path(td)/(str(j)+".png")
    art(day,title,("EXEMPLO EDUCATIVO","CONHECIMENTO PROFISSIONAL","ACOMPANHA A PÁGINA")[j],str(j+1)+" / 3",True,style+j).save(frame)
    ins+=["-loop","1","-t","3","-i",str(frame)]
   cmd=["ffmpeg","-hide_banner","-loglevel","error","-y",*ins,"-f","lavfi","-t","9","-i","anullsrc=r=44100:cl=stereo",
        "-filter_complex","[0:v]fps=10,format=yuv420p[v0];[1:v]fps=10,format=yuv420p[v1];[2:v]fps=10,format=yuv420p[v2];[v0][v1][v2]concat=n=3:v=1:a=0[v]",
        "-map","[v]","-map","3:a","-c:v","libx264","-preset","ultrafast","-crf","24","-pix_fmt","yuv420p","-r","10","-c:a","aac","-b:a","48k","-movflags","+faststart",str(path)]
   subprocess.run(cmd,check=True,timeout=90)
 print(day,"OK",flush=True)
