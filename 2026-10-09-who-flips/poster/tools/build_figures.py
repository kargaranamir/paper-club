"""Author native Excalidraw figures; published values are in data.py."""
from pathlib import Path
import json, os
from fontTools.ttLib import TTFont
from data import *
ROOT=Path(__file__).resolve().parents[1]
TEAL='#16130F';BLUE='#0078BF';SKY='#EBD8BD';AMBER='#B31C70';GOLD='#FFE14D';INK='#16130F';MUTED='#5B5347';GRID='#DED2BE';PALE='#E2F3E8';WHITE='#FFFAF0'
f=TTFont(os.environ.get('FIGURE_FONT', '/System/Library/Fonts/Supplemental/Arial.ttf'));cm=f.getBestCmap();hm=f['hmtx'];up=f['head'].unitsPerEm

def tw(t,sz):return max(sum(hm[cm.get(ord(c),'space')][0] for c in l)/up*sz for l in t.split('\n'))
class Fig:
 def __init__(self,name,w,h,bg=WHITE):
  self.name=name;self.w=w;self.h=h;self.e=[dict(type='cameraUpdate',x=0,y=0,width=1200,height=900)];self.k=0;self.rect(0,0,w,h,bg,'transparent',0)
 def add(self,**el):
  self.k+=1;el['id']=self.name+'-'+str(self.k);self.e.append(el)
 def rect(self,x,y,w,h,fill,stroke=GRID,sw=1,rough=0):self.add(type='rectangle',x=x,y=y,width=w,height=h,backgroundColor=fill,strokeColor=stroke,fillStyle='solid',strokeWidth=sw,roughness=rough)
 def text(self,x,y,t,sz=28,col=INK,anchor='l'):
  x-=tw(t,sz)*(0.5 if anchor=='c' else 1 if anchor=='r' else 0)
  self.add(type='text',x=x,y=y,text=t,fontSize=sz,fontFamily=2,strokeColor=col)
 def line(self,pts,col=GRID,sw=1,dashed=False,head=None,rough=0):
  x,y=pts[0];self.add(type='arrow' if head else 'line',x=x,y=y,width=max(a for a,b in pts)-min(a for a,b in pts),height=max(b for a,b in pts)-min(b for a,b in pts),points=[[a-x,b-y] for a,b in pts],strokeColor=col,strokeWidth=sw,strokeStyle='dashed' if dashed else 'solid',roughness=rough,endArrowhead=head,startArrowhead=None)
 def dot(self,x,y,col=BLUE,r=6,open=False):self.add(type='ellipse',x=x-r,y=y-r,width=r*2,height=r*2,strokeColor=col,backgroundColor='transparent' if open else col,strokeWidth=2,fillStyle='solid',roughness=0)
 def write(self):
  # Compact the two lower rows while preserving type size and round markers.
  # Baseline and length graphics remain identical to the preceding poster.
  scale={'cross-matrix':.90,'ea-ep':.85,'maxflip':.85,'pooling':.85}.get(self.name,1)
  if scale!=1:
   self.h*=scale
   for el in self.e:
    if el['type']=='cameraUpdate':continue
    if el['type']=='ellipse':el['y']=(el['y']+el['height']/2)*scale-el['height']/2
    else:
     el['y']*=scale
     if 'height' in el:el['height']*=scale
    if 'points' in el:el['points']=[[a,b*scale] for a,b in el['points']]
   # Include the final text line without clipping its font ascenders/descenders.
   extent=max(el['y']+el['fontSize']*1.25*len(el['text'].split('\n')) for el in self.e if el['type']=='text')
   self.h=max(self.h,extent+3)
   self.e[1]['height']=self.h
  (ROOT/'figures/src'/f'{self.name}.json').write_text(json.dumps(dict(width=self.w,height=self.h,elements=self.e)))
 def node(self,x,y,w,h,t,fill=PALE,col=TEAL):
  self.rect(x,y,w,h,fill,col,1.5,.5)
  for i,l in enumerate(t.split('\n')):self.text(x+w/2,y+h/2-17*len(t.split('\n'))+i*34,l,29,col,'c')

# Flow diagram: generation and answering occur in separate sessions.
s=Fig('protocol',740,600)
s.text(22,12,'1  GENERATE THE CHALLENGE',28,TEAL)
s.node(20,65,300,100,'Question +\nincorrect option')
s.line([(335,115),(395,115)],TEAL,2,head='arrow')
s.node(410,65,310,100,'Source argues for\nthe incorrect option','#FFF3D9',AMBER)
s.text(22,185,'Refusal → exclude this attempt',27,MUTED)
s.text(22,261,'2  TEST A FRESH SESSION',28,TEAL)
s.node(20,313,300,100,'Target answers\nthe original question')
s.line([(335,363),(395,363)],TEAL,2,head='arrow')
s.node(410,313,310,100,'Initially correct?\nShow the argument')
s.line([(565,425),(565,469)],TEAL,2,head='arrow')
s.node(410,480,310,92,'Answer again:\ncorrect / incorrect','#FFF3D9',AMBER)
s.text(22,470,'Keep only initially\ncorrect answers with\nan available argument.',27,MUTED)
s.write()

# Baseline: keep uncertainty and model-specific eligibility visible.
s=Fig('baseline',1060,670,WHITE)
x,w=370,475
for v in [0,25,50,75,100]:
 xx=x+w*v/100;s.line([(xx,75),(xx,555)],GRID,1);s.text(xx,575,str(v),29,MUTED,'c')
s.text(165,5,'TARGET MODEL',26,MUTED,'c');s.text(911,5,'AFR',25,MUTED,'c');s.text(1004,5,'Coverage',23,MUTED,'c')
for i,m in enumerate(MODELS):
 y=100+i*70;s.text(340,y-17,m,32,INK,'r');a=x+w*MEAN[i]/100;s.dot(a,y,BLUE,6)
 for xx in [x+w*(MEAN[i]-MEAN_CI[i])/100,x+w*(MEAN[i]+MEAN_CI[i])/100]:s.line([(xx,y-8),(xx,y+8)],BLUE,2)
 s.line([(x+w*(MEAN[i]-MEAN_CI[i])/100,y),(x+w*(MEAN[i]+MEAN_CI[i])/100,y)],BLUE,2)
 s.text(911,y-16,f'{MEAN[i]:.1f}',30,INK,'c');s.text(1004,y-17,f'{COVERAGE[i]}%',30,MUTED,'c')
s.text(607,627,'Mean blind AFR (%) · lower = more stable',30,INK,'c');s.write()

# Selected subject-domain results, transcribed from Table 5 rather than
# inferred broad-category averages. Both panels share a 0-100 percent scale.
s=Fig('domains',1760,218)
for offset,title,rows,col in [
 (0,'THREE LOWEST · STEM',[SUBJECTS[5],SUBJECTS[4],SUBJECTS[3]],'#0B765A'),
 (890,'THREE HIGHEST · HUMANITIES / SOCIAL SCI.',SUBJECTS[:3],AMBER)]:
 s.text(offset+12,0,title,25,col)
 xx,ww=offset+355,345
 for v in [0,50,100]:
  a=xx+ww*v/100;s.line([(a,43),(a,172)],GRID,1)
  s.text(a,184,str(v),26,MUTED,'c')
 for i,(label,afr,ci) in enumerate(rows):
  label={'Elementary mathematics':'Elementary math.','College mathematics':'College math.'}.get(label,label)
  yy=60+i*47
  s.text(offset+328,yy-16,label,30,INK,'r')
  a,b=xx+ww*(afr-ci)/100,xx+ww*(afr+ci)/100
  s.line([(a,yy),(b,yy)],col,2)
  for edge in [a,b]:s.line([(edge,yy-7),(edge,yy+7)],col,2)
  s.dot(xx+ww*afr/100,yy,col,6)
  s.text(offset+810,yy-16,f'{afr:.1f}%',30,col,'r')
s.write()

# Attribution: pairs and a reported-delta column, no re-computation from rounded means.
s=Fig('attribution',1060,510)
x,w=375,460
for v in [0,25,50,75,100]:
 xx=x+w*v/100;s.line([(xx,60),(xx,424)]);s.text(xx,439,str(v),26,MUTED,'c')
s.dot(384,20,BLUE,6,True);s.text(400,3,'blind',27,BLUE);s.dot(548,20,AMBER);s.text(564,3,'self-attributed',27,AMBER);s.text(963,3,'Δ pp',28,MUTED,'c')
for i,m in enumerate(MODELS):
 y=76+i*54;s.text(343,y-16,m,29,INK,'r');a=x+w*MEAN[i]/100;b=x+w*SELF[i]/100
 s.line([(a,y),(b,y)],AMBER,3);s.dot(a,y,BLUE,7,True);s.dot(b,y,AMBER,7);s.text(963,y-16,f'+{SAD[i]:.1f}',29,AMBER,'c')
s.text(600,480,'Answer flip rate (%)',28,MUTED,'c');s.write()

# Length trajectories: four explicitly selected models with published pointwise CIs.
# Direct labels and different marker shapes identify series without a distant legend.
s=Fig('length',1060,510)
x,y,w,h=85,47,635,367
fx=lambda k:x+w*(k-1)/9
fy=lambda v:y+h*(1-v/100)
for v in [0,25,50,75,100]:
 yy=fy(v);s.line([(x,yy),(x+w,yy)],GRID,1);s.text(x-16,yy-15,str(v),27,MUTED,'r')
for k in K:
 xx=fx(k);s.line([(xx,y),(xx,y+h)],GRID,1);s.text(xx,y+h+13,str(k),27,MUTED,'c')
s.text(85,0,'Blind AFR (%)',28,MUTED)
styles=[(0,MUTED,'open'),(2,BLUE,'circle'),(3,'#8054BA','diamond'),(4,'#0B765A','square')]
for i,col,shape in styles:
 pts=[(fx(k),fy(v)) for k,v in zip(K,AFR[i])]
 s.line(pts,col,3,dashed=shape=='square')
 for k,v,ci in zip(K,AFR[i],AFR_CI[i]):
  xx=fx(k);a=fy(v-ci);b=fy(v+ci)
  s.line([(xx,a),(xx,b)],col,1.8)
  for yy in [a,b]:s.line([(xx-5,yy),(xx+5,yy)],col,1.5)
  yy=fy(v)
  if shape in ['circle','open']:s.dot(xx,yy,col,6,open=shape=='open')
  elif shape=='diamond':s.add(type='diamond',x=xx-8,y=yy-8,width=16,height=16,strokeColor=col,backgroundColor=col,fillStyle='solid',strokeWidth=1.5,roughness=0)
  else:s.rect(xx-6,yy-6,12,12,WHITE,col,2)
 ey=pts[-1][1]
 s.line([(x+w+12,ey),(750,ey)],col,1.5)
 s.text(765,ey-15,MODELS[i],27,col)
s.text(409,473,'Argument length (sentences)',29,MUTED,'c');s.write()

# MaxFlip effect sizes: zero line and a CI crossing it are visually explicit.
s=Fig('maxflip',1060,510)
x,w=380,500;lo,hi=-2,30;fx=lambda v:x+w*(v-lo)/(hi-lo)
for v in [0,10,20,30]:
 xx=fx(v);s.line([(xx,60),(xx,424)],MUTED if v==0 else GRID,1.8 if v==0 else 1);s.text(xx,439,str(v),26,MUTED,'c')
s.text(380,3,'Increase under selected challenges',28,AMBER);s.text(975,3,'Δ pp',28,MUTED,'c')
for i,m in enumerate(MODELS):
 y=76+i*54;s.text(347,y-16,m,29,INK,'r');a=fx(GAIN[i]-GAIN_CI[i]);b=fx(GAIN[i]+GAIN_CI[i]);s.line([(a,y),(b,y)],AMBER,3)
 for xx in (a,b):s.line([(xx,y-7),(xx,y+7)],AMBER,2)
 s.dot(fx(GAIN[i]),y,AMBER,7,open=i==4);s.text(975,y-16,f'+{GAIN[i]:.1f}',29,AMBER,'c')
s.text(633,480,'AFR change (percentage points)',28,MUTED,'c');s.write()

# Pairwise source-to-target structure: sequential palette with numeric cells.
s=Fig('cross-matrix',1080,510)
labels=['GPT-5.1','Gemma 26B','Llama 8B','Llama 70B','Qwen 35B','Qwen 4B','Qwen 9B']
x,y,cw,rh=305,105,99,44
s.text(665,0,'TARGET MODEL →',29,TEAL,'c');s.text(16,45,'SOURCE',27,TEAL);s.text(16,76,'MODEL ↓',27,TEAL)
for j,l in enumerate(labels):
 pieces=l.split(' ')
 if len(pieces)==1: pieces=[l]
 for k,p in enumerate(pieces):s.text(x+(j+.5)*cw,40+k*29,p,25,INK,'c')
for i,row in enumerate(MATRIX):
 s.text(x-20,y+i*rh+6,labels[i],28,INK,'r')
 for j,v in enumerate(row):
  t=v/100;a=(255,250,240);b=(0,120,191);rgb=tuple(round(aa+(bb-aa)*t) for aa,bb in zip(a,b));fill='#%02x%02x%02x'%rgb
  s.rect(x+j*cw,y+i*rh,cw-4,rh-4,fill,TEAL if i==j else 'transparent',2 if i==j else 0);s.text(x+(j+.5)*cw-2,y+i*rh+5,str(v),28,WHITE if v>63 else INK,'c')
s.text(305,440,'AFR (%)    ',27,MUTED)
for j in range(10):
 t=j/9;a=(255,250,240);b=(0,120,191);rgb=tuple(round(aa+(bb-aa)*t) for aa,bb in zip(a,b));s.rect(490+j*40,444,40,19,'#%02x%02x%02x'%rgb,'transparent',0)
s.text(484,474,'0',25,MUTED);s.text(885,474,'100',25,MUTED,'r');s.write()
# EA vs EP: preserve the original Figure 5 point locations, rather than
# recomputing them from Figure 4's rounded cells or substituting Table 6 means.
s=Fig('ea-ep',1060,510)
x,y,w,h=100,60,900,355
fx=lambda v:x+w*v/100
fy=lambda v:y+h*(1-v/100)
def triangle(pts,fill):
 xx,yy=pts[0]
 s.add(type='line',x=xx,y=yy,width=max(a for a,b in pts)-min(a for a,b in pts),height=max(b for a,b in pts)-min(b for a,b in pts),points=[[a-xx,b-yy] for a,b in pts],strokeColor='transparent',backgroundColor=fill,fillStyle='solid',strokeWidth=0,roughness=0)
triangle([(fx(0),fy(0)),(fx(0),fy(100)),(fx(100),fy(100)),(fx(0),fy(0))],'#E2F3E8')
triangle([(fx(0),fy(0)),(fx(100),fy(0)),(fx(100),fy(100)),(fx(0),fy(0))],'#FBE6EC')
for v in [0,25,50,75,100]:
 s.line([(fx(v),fy(0)),(fx(v),fy(100))],GRID,1)
 s.line([(fx(0),fy(v)),(fx(100),fy(v))],GRID,1)
 s.text(fx(v),430,str(v),27,MUTED,'c')
 s.text(79,fy(v)-15,str(v),27,MUTED,'r')
s.line([(fx(0),fy(0)),(fx(100),fy(100))],MUTED,2,dashed=True)
s.text(100,0,'EA (%) · flips other models as a source',29,INK)
s.text(553,477,'EP (%) · is flipped by other sources',29,INK,'c')
s.text(142,80,'EA > EP',27,'#0B765A')
s.text(830,358,'EP > EA',27,AMBER)
# Direct labels, plus leader lines around the closely spaced upper-left trio.
label_specs={
 'GPT-5.1':(180,131,'c','#0B765A'),
 'Qwen3.5-35B':(194,245,'c','#8054BA'),
 'Gemma-4-26B':(431,173,'c',BLUE),
 'Qwen3.5-9B':(541,283,'c','#8054BA'),
 'Qwen3.5-4B':(661,198,'c',BLUE),
 'Llama-3.3-70B':(820,225,'c',MUTED),
 'Llama-3.1-8B':(982,291,'r',MUTED)}
for name,ep,ea in EA_EP_FIG5:
 xx,yy=fx(ep),fy(ea);tx,ty,anchor,col=label_specs[name]
 # Stop at the outside of each label rather than striking through its text.
 endpoints={'GPT-5.1':(219,168),'Qwen3.5-35B':(217,240),
  'Gemma-4-26B':(329,190),'Qwen3.5-9B':(531,278),
  'Qwen3.5-4B':(661,240),'Llama-3.3-70B':(839,266),
  'Llama-3.1-8B':(989,311)}
 s.line([(xx,yy),endpoints[name]],col,1.4)
 s.dot(xx,yy,col,9,open=name.startswith('Llama'))
 s.text(tx,ty,name,26,col,anchor)
s.write()

# MaxFlip is a per-question selection procedure, not a generated score example.
s=Fig('pooling',1060,510)
s.text(530,0,'ONE QUESTION · MANY SOURCE ARGUMENTS',27,MUTED,'c')
for i,(tx,fill) in enumerate([(68,'#D6F2DF'),(355,'#B7DDF5'),(642,'#FFB9DE')]):
 s.rect(tx+11,59,275,90,INK,INK,2)
 s.rect(tx,48,275,90,fill,INK,2)
 for yy,ww in [(69,199),(89,222),(109,160)]:s.line([(tx+24,yy),(tx+ww,yy)],INK,2)
 s.line([(tx+138,158),(530,212)],INK,2,head='arrow')
s.text(977,90,'…',38,INK,'c')
s.rect(178,220,704,112,'#E2F3E8',INK,3)
s.text(530,234,'Evaluate each candidate',36,INK,'c')
s.text(530,285,'Count how many target models flip',28,INK,'c')
s.line([(530,343),(530,382)],INK,3,head='arrow')
s.rect(139,401,800,80,INK,INK,2)
s.rect(130,392,800,80,GOLD,INK,3)
s.text(530,410,'KEEP THE ARGUMENT WITH THE MOST FLIPS',30,INK,'c')
s.text(530,482,'One selected challenge per question · random tie-breaking',25,MUTED,'c')
s.write()

# Original Excalidraw schematic: the mechanism, not an invented paper example.
s=Fig('mechanism',1800,242)
def frame(x,w):
 s.rect(x+7,17,w,217,INK,INK,3);s.rect(x,10,w,217,WHITE,INK,3)
frame(20,370);frame(500,570);frame(1180,580)
s.text(46,31,'01  FIRST ANSWER',29,INK)
s.rect(43,86,323,107,'#D6F2DF',INK,2)
s.text(204,106,'Correct',58,INK,'c')
s.line([(412,117),(472,117)],INK,5,head='arrow')
s.text(530,31,'02  COUNTERARGUMENT',29,INK)
s.text(785,78,'A plausible case for',42,INK,'c')
s.text(785,125,'a wrong option.',42,INK,'c')
s.text(785,187,'Refusal → no challenge',25,MUTED,'c')
s.line([(1093,117),(1152,117)],INK,5,head='arrow')
s.text(1210,31,'03  ANSWER AGAIN',29,INK)
s.rect(1205,91,245,104,'#D6F2DF',INK,2)
s.rect(1474,91,260,104,'#FFB9DE',INK,2)
s.text(1327,104,'HOLD',33,INK,'c');s.text(1327,149,'correct',32,INK,'c')
s.text(1604,104,'FLIP',33,INK,'c');s.text(1604,149,'any wrong',32,INK,'c')
s.write()
