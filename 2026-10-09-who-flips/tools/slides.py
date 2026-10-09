"""Who Flips? paper club. Same Python -> Excalidraw workflow as QARM V2.
All empirical numbers are in data.py and references/digest.md. Toy examples are labeled.
"""
from slidekit import Slide, P
from data import *

SRC='Who Flips? arXiv:2606.16011v2'

def base(slug,n,title,sub='',part=''):
 if n>20: part='Backup' if part=='Backup' else 'Backup / '+part
 s=Slide(slug,n); s.title(title,sub,part); return s

def end(s,source,take=None):
 if take: s.takeaway(take,fs=28)
 s.footer(source); return s

def panel(s,x,y,w,h,title,body,c='blue',fs=28):
 s.box(x,y,w,h,c=c,fill=P[c]['soft']); s.text(x+24,y+22,title,32,P[c]['text'])
 s.text(x+24,y+85,body,fs)

def node(s,x,y,w,h,text,c='blue',fs=27):
 s.box(x,y,w,h,text,c,fs)

def arr(s,x1,y1,x2,y2,c='ink'):
 s.arrow([(x1,y1),(x2,y2)], P[c] if c=='ink' else P[c]['stroke'])

def dot(s,x,y,c,r=7):
 s.box(x-r,y-r,r*2,r*2,c=c,fill=P[c]['text'],stroke=P[c]['text'],shape='ellipse',roughness=0,sw=1)

def axis_h(s,x,y,w,maxv=100,ticks=(0,25,50,75,100)):
 for t in ticks:
  xx=x+w*t/maxv; s.line([(xx,y),(xx,690)],P['grid'],1,roughness=0); s.text(xx,709,str(t),19,P['muted'],anchor='c')
 s.text(x+w,740,'percent',19,P['muted'],anchor='r')

def bars(s,labels,vals,cis=None,x=440,y=210,w=920,gap=68,maxv=100,colors=None):
 axis_h(s,x,y-20,w,maxv,tuple(range(0,int(maxv)+1,25)) if maxv==100 else (0,10,20,30))
 for i,(lab,v) in enumerate(zip(labels,vals)):
  yy=y+i*gap; c=(colors or ['blue']*len(vals))[i]
  s.text(x-24,yy+16,lab,25,anchor='r',valign='m')
  s.box(x,yy,w*v/maxv,32,c=c,round_=False,roughness=1)
  if cis:
   lo=x+w*(v-cis[i])/maxv; hi=x+w*(v+cis[i])/maxv
   s.line([(lo,yy+16),(hi,yy+16)],P['ink'],2,roughness=0)
   for xx in (lo,hi): s.line([(xx,yy+9),(xx,yy+23)],P['ink'],2,roughness=0)
  s.text(x+w*v/maxv+20,yy+16,f'{v:.1f}',25,P[c]['text'],valign='m')

def paired(s,left,right,deltas,ci,kind):
 x,w=440,770; axis_h(s,x,220,w)
 s.text(1370,175,'change (pp)',22,P['muted'],anchor='c')
 for i,m in enumerate(MODELS):
  y=245+i*66; s.text(410,y,m,25,anchor='r',valign='m')
  a=x+w*left[i]/100;b=x+w*right[i]/100
  s.line([(a,y),(b,y)],P['purple']['stroke'],4,roughness=0); dot(s,a,y,'blue');dot(s,b,y,'orange')
  s.text(a,y-14,f'{left[i]:.1f}',19,P['blue']['text'],anchor='r',valign='b')
  s.text(b+10,y+8,f'{right[i]:.1f}',19,P['orange']['text'])
  s.text(1370,y,f'+{deltas[i]:.1f} ± {ci[i]:.1f}',24,P['purple']['text'],anchor='c',valign='m')
 s.text(80,176,'Blue: blind / same source',22,P['blue']['text']); s.text(650,176,'Orange: '+kind,22,P['orange']['text'])


# Reusable chart coordinates; all marks remain editable Excalidraw elements.
SHORT=['Llama 8B','Llama 70B','Qwen 4B','Qwen 9B','GPT-5.1','Gemma 26B','Qwen 35B']
COLORS=['red','orange','blue','purple','green','cyan','gray']

def xy_axes(s,x,y,w,h,xmax=100,ymax=100,xticks=(0,25,50,75,100),yticks=(0,25,50,75,100)):
 for v in yticks:
  yy=y+h-h*v/ymax
  s.line([(x,yy),(x+w,yy)],P['grid'],1,roughness=0)
  s.text(x-14,yy,str(v),20,P['muted'],anchor='r',valign='m')
 for v in xticks:
  xx=x+w*v/xmax
  s.line([(xx,y),(xx,y+h)],P['grid'],1,roughness=0)
  s.text(xx,y+h+15,str(v),20,P['muted'],anchor='c')
 s.line([(x,y),(x,y+h),(x+w,y+h)],P['faint'],2,roughness=0)
 return lambda a,b:(x+w*a/xmax,y+h-h*b/ymax)

def mark_label(s,xy,label,c,dx=15,dy=-22):
 dot(s,*xy,c,9)
 s.text(xy[0]+dx,xy[1]+dy,label,24,P[c]['text'])

def s01(n):
 s=Slide('title',n)
 s.text(75,55,'PAPER CLUB',23,P['blue']['text'],mono=True)
 s.text(75,120,'Who Flips?',108,hand=True)
 s.text(80,265,'Self- and Cross-Model Counterarguments\nReveal Answer Instability in LLMs',39)
 s.text(80,390,'Nafiseh Nikeghbal · Amir Hossein Kargaran\nShaghayegh Kolli · Jana Diesner',26,P['muted'])
 s.text(80,475,'TUM, MCML, MDSI and LMU Munich',23,P['muted'])
 s.text(1030,165,'Correct\nfirst.',64,P['green']['text'],hand=True)
 arr(s,1240,365,1240,435,'blue')
 s.text(1030,480,'Stable\nnext?',64,P['blue']['text'],hand=True)
 s.text(80,665,'Evaluate stability\nalongside accuracy.',45,P['blue']['text'],hand=True)
 s.text(80,809,'arxiv.org/abs/2606.16011v2',23,P['muted'])
 s.footer('Who Flips? / EMNLP Findings 2026')
 return s

def s02(n):
 s=base('two-roles',n,'Arguing and resisting are different abilities','The same two models can exchange roles','Source and target')
 node(s,105,230,375,145,'GPT-5.1\nsource of an argument','green',32)
 node(s,1085,230,405,145,'Llama-3.1-8B\ntarget answering again','red',32)
 arr(s,505,300,1055,300,'red')
 s.text(780,229,'100% flip rate',39,P['red']['text'],anchor='c')
 s.text(780,328,'GPT-5.1 argues for a wrong option',25,P['muted'],anchor='c')
 node(s,105,510,375,145,'GPT-5.1\ntarget answering again','green',32)
 node(s,1085,510,405,145,'Llama-3.1-8B\nsource of an argument','red',32)
 arr(s,1055,580,505,580,'green')
 s.text(780,509,'11% flip rate',39,P['green']['text'],anchor='c')
 s.text(780,608,'Llama-3.1-8B argues for a wrong option',25,P['muted'],anchor='c')
 return end(s,'Figure 4 / rounded pairwise AFR / blind, k = 10','An effective source of wrong arguments can also be a resistant target.')

def s03(n):
 s=base('toy-example',n,'A correct answer can be lost after a challenge','Invented teaching example, not a measured question or model response','The question')
 s.text(80,180,'A fair coin lands heads five times.\nWhat is the probability of heads next?',36)
 s.text(80,288,'A  1/6       B  1/2       C  5/6       D  1',28,P['muted'])
 node(s,80,385,440,115,'First answer: B (1/2)','green',35)
 s.text(80,545,'Each fair flip is independent.',29,P['green']['text'])
 arr(s,548,442,665,442,'orange')
 node(s,710,220,800,200,'Wrong argument:\n“After five heads, tails is overdue.\nThe chance of another head must be lower.\nChoose A.”','orange',30)
 arr(s,1100,442,1100,500,'orange')
 node(s,710,535,360,130,'HOLD B\nStill correct','green',32)
 node(s,1150,535,360,130,'FLIP to A\nNow wrong','red',32)
 return end(s,'Definition 3.1 / illustrative example','The question tests whether the model keeps an answer it already got right.')

def s04(n):
 s=base('two-stage-protocol',n,'The challenge protocol','Source and target use separate sessions, even when they are the same model','Measurement')
 s.text(80,180,'SOURCE SESSION',27,P['orange']['text'],mono=True)
 node(s,80,245,350,115,'Question + wrong option','gray',30)
 arr(s,452,303,555,303)
 node(s,580,245,420,115,'Write a committed\nwrong-answer argument','orange',30)
 arr(s,1025,303,1120,303)
 s.text(1160,250,'Refusal?\nNo challenge to score.',29,P['muted'])
 s.line([(80,424),(1520,424)],P['faint'],1,True,0)
 s.text(80,458,'TARGET SESSION',27,P['blue']['text'],mono=True)
 for x,w,t,c in [(80,270,'Answer\nthe question','blue'),(435,300,'Keep correct\nfirst answers','green'),(825,300,'Present the\nwrong argument','orange'),(1210,310,'Answer again\nHold or flip?','purple')]:
  node(s,x,535,w,128,t,c,31)
 for x1,x2 in [(375,410),(760,800),(1145,1185)]:arr(s,x1,600,x2,600)
 s.line([(790,368),(790,475),(975,475),(975,515)],P['orange']['stroke'],2,True,0)
 return end(s,'Protocol, §3 / prompts, Appendix A','Seven models and 57 MMLU subjects test the same two-stage idea.')

def s05(n):
 s=base('afr-denominator',n,'Answer flip rate measures a conditional failure','A challenge is eligible only if the first answer is correct and an argument exists','Measurement')
 node(s,80,235,520,380,None,'gray')
 s.text(110,265,'All benchmark questions',32,P['muted'])
 s.box(115,342,450,235,c='green',fill=P['green']['soft'],roughness=0)
 s.text(140,365,'Initially correct',30,P['green']['text'])
 s.box(145,432,390,105,'Wrong argument available','blue',28,roughness=0)
 s.text(140,637,'Eligibility defines the denominator.',28,P['blue']['text'])
 s.text(765,225,'AFR',69,P['blue']['text'],hand=True)
 s.text(1010,247,'Answer flip rate',37)
 s.text(1115,365,'Eligible challenges ending wrong',32,anchor='c')
 s.line([(735,419),(1510,419)],P['ink'],3,roughness=0)
 s.text(1115,451,'All eligible challenges',32,anchor='c')
 s.text(750,585,'Any final wrong option counts.\nThe defended option need not win.',30,P['muted'])
 return end(s,'Definition 3.1 / coverage in Table 2','AFR describes losing a correct answer among the challenges that can be tested.')

def s06(n):
 s=base('three-conditions',n,'Attribution and source are different experimental factors',part='Protocol')
 rows=[['blind','same model','anonymous','1, 3, 5, 10'],['self','same model','“your earlier reasoning”','1, 3, 5, 10'],['cross','different model','anonymous','10 only']]
 s.table(70,195,[240,350,520,350],rows,['condition','argument source','presentation','sentences (k)'],fs=27,rh=100)
 s.text(85,640,'“Self-generated” identifies the source. “Self-attributed” describes the prompt.',30,P['purple']['text'])
 return end(s,'§3; Appendix A','Blind vs self changes attribution while keeping the underlying argument fixed.')

def s07(n):
 s=base('experimental-setup',n,'Seven models under a fixed evaluation setup',part='Experiment')
 s.table(70,172,[400,740],[[m,ids] for m,ids in zip(MODELS,IDS)],['paper label','model identifier'],fs=23,rh=61,mono_cols=(1,))
 panel(s,1240,172,290,490,'Settings','Temperature 0\n\nReasoning\nmodes off\n\nOpen weights:\nvLLM\n\nClosed model:\nAPI','purple',24)
 s.text(80,700,'2,052 questions across 57 MMLU subjects; all three wrong options per question.',28)
 return end(s,'§4; Table 1','These are the paper’s model configurations, not a claim about every deployment.')

def s08(n):
 s=base('coverage-and-ci',n,'Eligibility and uncertainty shape the comparison',part='Experiment')
 s.table(70,180,[420,280],[[m,f'{c}%'] for m,c in zip(MODELS,COVERAGE)],['model','coverage'],fs=26,rh=66)
 panel(s,840,180,690,310,'Uncertainty reporting','95% cluster-bootstrap intervals\n2,000 bootstrap replicates\nCluster on the original MMLU question\n\nRepeated options and conditions share a question.','blue',26)
 panel(s,840,525,690,185,'Reading the intervals','Table subscripts are CI half-widths in pp.\nCoverage is eligibility, not baseline accuracy.','gray',26)
 return end(s,'§4.2; Table 2; §5.1','Models can be compared on different eligible subsets; that limits ranking claims.')

def s09(n):
 s=base('blind-afr',n,'Answer stability varies across models','Mean blind AFR, averaged over argument lengths. Lower means more stable.','First result')
 x,w=495,815
 for v in (0,25,50,75,100):
  xx=x+w*v/100;s.line([(xx,216),(xx,683)],P['grid'],1,roughness=0);s.text(xx,702,str(v),23,P['muted'],anchor='c')
 s.text(1375,170,'AFR',24,P['muted'],anchor='c');s.text(1485,170,'Coverage',22,P['muted'],anchor='c')
 for i,(m,v,ci) in enumerate(zip(MODELS,MEAN,MEAN_CI)):
  y=249+i*67;c='red' if i==0 else 'blue'
  s.text(460,y,m,30,anchor='r',valign='m')
  s.line([(x+w*(v-ci)/100,y),(x+w*(v+ci)/100,y)],P[c]['text'],3,roughness=0);dot(s,x+w*v/100,y,c,8)
  s.text(1375,y,f'{v:.1f}%',28,P[c]['text'],anchor='c',valign='m');s.text(1485,y,f'{COVERAGE[i]}%',25,P['muted'],anchor='c',valign='m')
 s.text(905,738,'Answer flip rate (%)',26,anchor='c')
 return end(s,'Table 2 / whiskers: reported 95% intervals','Mean blind AFR ranges from 17.5% to 97.3%. Eligible subsets differ by model.')

def s10(n):
 s=base('argument-length',n,'Longer arguments are not always stronger','Four selected models. The backup slides show all seven.','Argument design')
 f=xy_axes(s,150,220,880,440,10,100,(1,3,5,10),(0,25,50,75,100))
 s.text(150,169,'Blind answer flip rate (%)',27,P['muted'])
 for i,c in [(0,'red'),(2,'blue'),(3,'purple'),(4,'green')]:
  pts=[f(k,v) for k,v in zip(K,AFR[i])];s.line(pts,P[c]['text'],3,roughness=0)
  for k,v,ci in zip(K,AFR[i],AFR_CI[i]):
   xx,yy=f(k,v);s.line([f(k,v-ci),f(k,v+ci)],P[c]['text'],2,roughness=0);dot(s,xx,yy,c,7)
  xx,yy=pts[-1];s.line([(xx+13,yy),(xx+45,yy)],P[c]['text'],2,roughness=0);s.text(xx+60,yy,MODELS[i],29,P[c]['text'],valign='m')
 s.text(590,706,'Argument length (sentences)',28,anchor='c')
 return end(s,'Table 2 / reported 95% intervals','The smaller Qwen models rise. GPT-5.1 shows no clear decrease.')

def s11(n):
 s=base('model-scale',n,'Size tracks stability within Qwen, but not across families','Mean blind AFR (%) versus reported model size; Qwen and Llama family members','Results')
 f=xy_axes(s,155,225,1030,430,80,100,(0,20,40,60,80))
 s.text(155,172,'Mean blind AFR (%) ↓',26,P['muted'])
 for indices,sizes,c in [([2,3,6],[4,9,35],'purple'),([0,1],[8,70],'orange')]:
  pts=[f(a,MEAN[i]) for a,i in zip(sizes,indices)]
  s.line(pts,P[c]['stroke'],3,roughness=0)
  for a,i in zip(sizes,indices):
   xx,yy=f(a,MEAN[i]);mark_label(s,(xx,yy),SHORT[i],c,15,-30)
   ends=[f(a,MEAN[i]-MEAN_CI[i]),f(a,MEAN[i]+MEAN_CI[i])]
   s.line(ends,P[c]['text'],2,roughness=0)
   for ex,ey in ends:s.line([(ex-5,ey),(ex+5,ey)],P[c]['text'],1,roughness=0)
 s.text(660,704,'Reported parameters (billions)',27,anchor='c')
 s.text(1250,295,'Qwen3.5',30,P['purple']['text']);s.text(1250,350,'64.3% → 17.5%',25)
 s.text(1250,465,'Llama',30,P['orange']['text']);s.text(1250,520,'97.3% → 75.8%',25)
 return end(s,'Table 2; whiskers: 95% CIs; total size labels; Qwen 35B is MoE','Total parameter labels differ from active compute; these are not controlled scaling runs.')

def s12(n):
 s=base('self-attribution',n,'Calling it your earlier reasoning increases flips','The argument stays fixed. Only its attribution changes.','Argument design')
 s.text(80,188,'Same argument',38,P['orange']['text'],hand=True)
 node(s,80,265,430,100,'Anonymous presentation','gray',30)
 arr(s,295,390,295,440,'orange')
 node(s,80,465,430,140,'Claimed to be your\nearlier reasoning','orange',32)
 s.text(90,640,'Mean change: +7.1 pp',32,P['orange']['text'])
 x,w=855,500
 for v in (0,5,10,15,20):
  xx=x+w*v/20;s.line([(xx,205),(xx,680)],P['grid'],1,roughness=0);s.text(xx,700,str(v),23,P['muted'],anchor='c')
 for i in range(7):
  y=245+i*67;s.text(820,y,SHORT[i],28,anchor='r',valign='m')
  v,ci=SAD[i],SAD_CI[i];s.line([(x+w*(v-ci)/20,y),(x+w*(v+ci)/20,y)],P['orange']['text'],3,roughness=0);dot(s,x+w*v/20,y,'orange',8)
  s.text(1460,y,f'+{v:.1f}',28,P['orange']['text'],anchor='c',valign='m')
 s.text(1120,737,'AFR increase (percentage points)',25,anchor='c')
 return end(s,'Table 3 / reported deltas and 95% intervals','Every reported change is positive. Qwen3.5-4B has the largest increase, +18.7 pp.')

def s13(n):
 s=base('refusal-vs-resistance',n,'Refusal and resistance are different behaviors','Each point is a model: generating the wrong argument versus later answering it','Results')
 f=xy_axes(s,160,235,960,425,50,100,(0,10,20,30,40,50))
 s.text(160,180,'Later AFR, blind + self (%) ↑',26,P['muted'])
 offsets=[(-185,-40),(16,-25),(16,18),(16,-28),(-10,28),(16,-23),(16,4)]
 for i in range(7): mark_label(s,f(CRR[i],COMBINED[i]),SHORT[i],COLORS[i],*offsets[i])
 s.text(630,711,'Wrong-argument generation refusal (%) →',27,anchor='c')
 panel(s,1200,250,330,350,'Two decisions','Llama 8B refuses\n41.3% of generation\nattempts.\n\nOn eligible challenges,\nit later flips 97.5%.','orange',25)
 return end(s,'Table 4; later AFR is conditional; no fitted trend or causal claim','A model can refuse many requests yet remain vulnerable when an argument exists.')

def s14(n):
 s=base('linguistic-correlates',n,'Language differs between held and flipped answers','Descriptive associations from lexical features, not causal explanations','Results')
 panel(s,70,185,700,480,'After the challenge','Held answers: more resistance phrases\n\nFlipped answers: about 6x as many\ncapitulation markers\n\nHeld responses are longer:\nabout 1,800 vs 1,150 characters.','blue',29)
 panel(s,830,185,700,480,'Before the challenge','Later flips associate with:\n\nMore baseline hedging\nLonger baseline responses\n\nHigher confidence in the wrong argument\ndoes not straightforwardly predict flips.','orange',27)
 s.text(80,703,'Manually curated lexicons; case-insensitive substring matching.',25,P['muted'])
 return end(s,'§5.4; Figure 2; Appendix B','Response markers partly describe the outcome; they do not establish why it happened.')

def s15(n):
 s=base('subject-domains',n,'Answer stability also varies by subject','Three lowest and three highest subject AFRs, pooled across models and conditions','Domain')
 x,w=545,770
 for v in (0,25,50,75,100):
  xx=x+w*v/100;s.line([(xx,235),(xx,690)],P['grid'],1,roughness=0);s.text(xx,710,str(v),23,P['muted'],anchor='c')
 for i,(lab,v,ci) in enumerate(SUBJECTS):
  y=270+i*69;c='red' if i<3 else 'green'
  s.text(510,y,lab,29,anchor='r',valign='m');s.line([(x+w*(v-ci)/100,y),(x+w*(v+ci)/100,y)],P[c]['text'],3,roughness=0);dot(s,x+w*v/100,y,c,9)
  s.text(1440,y,f'{v:.1f}%',30,P[c]['text'],anchor='c',valign='m')
 s.text(545,177,'AFR (%)',28,P['muted'])
 s.line([(95,447),(1510,447)],P['faint'],1,True,0)
 return end(s,'Table 5 / reported 95% intervals / selected extremes','These are subject results, not averages of broad domain categories.')

def s16(n):
 s=base('cross-matrix',n,'Who persuades whom?','Rows supply wrong arguments. Columns answer the question again.','Source and target')
 short=['GPT-5.1','Gemma\n26B','Llama\n8B','Llama\n70B','Qwen\n35B','Qwen\n4B','Qwen\n9B']
 x,y,cw,rh=380,257,158,61
 s.text(945,160,'TARGET MODEL',24,P['blue']['text'],anchor='c',mono=True)
 s.text(78,186,'SOURCE\nMODEL',26,P['blue']['text'],mono=True)
 for j,m in enumerate(short):s.text(x+(j+.5)*cw,207,m,26,anchor='c')
 for i,m in enumerate(MATRIX_MODELS):
  s.text(x-27,y+i*rh+rh/2,m,27,anchor='r',valign='m')
  for j,v in enumerate(MATRIX[i]):
   t=v/100;start=(238,247,246);stop=(0,105,115);fill='#'+''.join(f'{round(a+(b-a)*t):02x}' for a,b in zip(start,stop))
   s.box(x+j*cw,y+i*rh,cw-4,rh-4,str(v),fs=29,fill=fill,stroke=P['ink'] if i==j else '#ffffff',tcolor='#ffffff' if v>=60 else P['ink'],sw=2 if i==j else 1,round_=False,roughness=0)
 s.text(380,708,'Outlined diagonal: same-model source',23,P['muted'])
 for i in range(11):
  t=i/10;fill='#'+''.join(f'{round(a+(b-a)*t):02x}' for a,b in zip((238,247,246),(0,105,115)))
  s.box(1140+i*25,716,26,16,fill=fill,stroke=fill,round_=False,roughness=0)
 s.text(1100,714,'0',20,P['muted']);s.text(1430,710,'100%',22,P['muted'])
 return end(s,'Figure 4 / rounded AFR (%) / blind, k = 10','Source effects depend on the target. The colors use one shared AFR scale.')

def s17(n):
 s=base('cross-vs-same',n,'Changing the source has no uniform effect','Cross-source minus same-source blind AFR at k = 10; reported 95% intervals','Cross-model results')
 x,w=560,780;lo,hi=-15,10
 fx=lambda v:x+w*(v-lo)/(hi-lo)
 for v in [-15,-10,-5,0,5,10]:
  xx=fx(v);s.line([(xx,230),(xx,690)],P['faint'] if v==0 else P['grid'],2 if v==0 else 1,roughness=0)
  s.text(xx,705,f'{v:+d}' if v else '0',21,P['muted'],anchor='c')
 s.text(620,175,'fewer flips',27,P['green']['text']);s.text(1155,175,'more flips',27,P['orange']['text'])
 for i,m in enumerate(MODELS):
  y=260+61*i;v=CROSS_DELTA[i];ci=CROSS_CI[i];c='green' if v<0 else 'orange'
  s.text(490,y,m,26,anchor='r',valign='m');s.line([(fx(v-ci),y),(fx(v+ci),y)],P[c]['text'],4,roughness=0);dot(s,fx(v),y,c,9)
  s.text(1430,y,f'{v:+.1f}',26,P[c]['text'],anchor='c',valign='m')
 s.text(950,738,'AFR change (percentage points)',25,anchor='c')
 return end(s,'Table 6; mean change -1.6 pp; changes retained as printed','A near-zero average conceals target-specific changes in both directions.')

def s18(n):
 s=base('variance-decomposition',n,'Target identity dominates the reported variance',part='Cross-model results')
 vals=[76.7,12.0,9.3];labs=['Target / baseline','Argument source','Subject'];ci=[(74.8,78.7),(10.1,14.5),(9.2,13.6)]
 for i,(lab,v,(lo,hi)) in enumerate(zip(labs,vals,ci)):
  y=235+i*132;s.text(70,y,lab,32);s.box(430,y,800*v/100,45,c=['blue','orange','purple'][i],round_=False)
  s.text(1260,y,f'{v:.1f}%',34);s.text(430,y+58,f'95% CI [{lo:.1f}, {hi:.1f}]',23,P['muted'])
 s.text(80,680,'Reported decomposition across target, source and subject triples.',27,P['muted'])
 return end(s,'§5.6; reported components sum to 98.0%','Source identity contributes, but target identity dominates this analysis.')

def s19(n):
 import json
 from pathlib import Path
 points=json.loads((Path(__file__).resolve().parents[1]/'references/ea-ep-provenance.json').read_text())['points']
 s=base('source-and-target-roles',n,'Persuasive sources can be hard to flip','EP: susceptibility as a target. EA: efficacy of wrong arguments as a source.','Source and target')
 x,y,w,h=145,226,985,445
 f=xy_axes(s,x,y,w,h)
 s.line([f(0,0),f(100,100)],P['faint'],2,dashed=True,roughness=0)
 s.text(x,173,'EA (%) / flips other models',28,P['muted'])
 s.text(635,716,'EP (%) / is flipped by other sources',29,anchor='c')
 s.text(850,307,'EA = EP',23,P['muted'])
 offsets=[(-50,-61),(-111,33),(27,-12),(-75,26),(15,30),(-92,-53),(-115,18)]
 cs=['green','gray','cyan','purple','blue','orange','red']
 labels=['GPT-5.1','Qwen 35B','Gemma 26B','Qwen 9B','Qwen 4B','Llama 70B','Llama 8B']
 for (name,ep,ea),c,lab,(dx,dy) in zip(points,cs,labels,offsets):
  xx,yy=f(ep,ea);s.line([(xx,yy),(xx+dx+35,yy+dy+15)],P['faint'],1,roughness=0);mark_label(s,(xx,yy),lab,c,dx,dy)
 s.text(1200,245,'Upper left',33,P['blue']['text'],hand=True)
 s.text(1200,300,'Hard to flip.\nEffective source\nof wrong arguments.',28)
 s.text(1200,475,'Lower right',33,P['red']['text'],hand=True)
 s.text(1200,530,'Easy to flip.\nLess effective\nas a source.',28)
 return end(s,'Figure 5 / positions recovered from the published vector figure','Argument efficacy and answer stability describe different model behaviors.')

def s20(n):
 s=base('maxflip-selection',n,'MaxFlip pools, tests and selects','Illustrative candidates and outcomes. The schematic does not show measured scores.','Stronger challenges')
 s.text(80,174,'ONE QUESTION',28,P['blue']['text'],mono=True)
 s.text(80,225,'Pool arguments\nacross sources',37,hand=True)
 for i,(lab,c) in enumerate([('Argument A','blue'),('Argument B','purple'),('Argument C','orange')]):
  node(s,95,350+i*102,340,76,lab,c,30)
 arr(s,468,489,565,489)
 s.text(635,180,'Test on target models',35,hand=True)
 for j in range(7):s.text(665+j*66,283,str(j+1),24,P['muted'],anchor='c')
 s.text(870,237,'TARGETS',22,P['muted'],anchor='c',mono=True)
 patterns=[[1,0,1,0,0,1,0],[1,1,1,0,1,1,0],[0,1,0,0,1,0,0]]
 for i,row in enumerate(patterns):
  yy=388+i*102
  if i==1:s.box(601,448,568,80,fill=P['purple']['soft'],stroke=P['purple']['stroke'],round_=False,roughness=0)
  for j,on in enumerate(row):
   xx=665+j*66;s.box(xx-14,yy-14,28,28,shape='ellipse',fill=P['purple']['text'] if on else '#ffffff',stroke=P['purple']['text'] if on else P['faint'],roughness=0)
  s.text(1140,yy,str(sum(row)),30,P['purple']['text'],anchor='c',valign='m')
 s.text(1140,283,'Flips',24,P['muted'],anchor='c')
 arr(s,1191,489,1260,489,'purple')
 node(s,1285,416,230,145,'Keep B\nMost flips','purple',32)
 s.text(620,679,'Filled circle = flip. Ties break randomly.',26,P['muted'])
 return end(s,'§5.7 / one selected argument per question','Selection uses the observed target set. Transfer to unseen targets needs a separate test.')

def s21(n):
 s=base('maxflip-results',n,'MaxFlip strengthens the selected challenges','AFR increase over standard same-model blind challenges','Stronger challenges')
 x,w,lo,hi=530,765,-5,30
 fx=lambda v:x+w*(v-lo)/(hi-lo)
 for v in (-5,0,10,20,30):
  xx=fx(v);s.line([(xx,211),(xx,687)],P['faint'] if v==0 else P['grid'],2 if v==0 else 1,roughness=0);s.text(xx,705,str(v),23,P['muted'],anchor='c')
 s.text(1433,165,'Gain (pp)',25,P['muted'],anchor='c')
 for i,m in enumerate(MODELS):
  y=249+i*67;v,ci=GAIN[i],GAIN_CI[i];c='gray' if i==4 else 'purple'
  s.text(490,y,m,29,anchor='r',valign='m');s.line([(fx(v-ci),y),(fx(v+ci),y)],P[c]['text'],3,roughness=0)
  s.box(fx(v)-8,y-8,16,16,shape='ellipse',fill='#ffffff' if i==4 else P[c]['text'],stroke=P[c]['text'],roughness=0)
  s.text(1430,y,f'+{v:.1f}',30,P[c]['text'],anchor='c',valign='m')
 s.text(930,738,'AFR change (percentage points)',27,anchor='c')
 return end(s,'Table 7 / reported gains and 95% intervals / blind k = 10 baseline','Qwen3.5-9B gains 23.6 pp. No clear increase for GPT-5.1.')

def s22(n):
 s=base('maxflip-producers',n,'Stable targets often supply selected wrong arguments','Producer share versus standard same-source blind AFR at k = 10','MaxFlip')
 f=xy_axes(s,170,235,1000,425,100,30,(0,25,50,75,100),(0,10,20,30))
 s.text(170,178,'Share of selected arguments (%) ↑',26,P['muted'])
 offsets=[(-155,-32),(-145,-30),(16,-22),(16,-20),(16,-32),(16,3),(16,3)]
 for i in range(7): mark_label(s,f(AFR[i][-1],PRODUCER[i]),SHORT[i],COLORS[i],*offsets[i])
 s.text(670,711,'Standard AFR as a target (%) →',27,anchor='c')
 panel(s,1240,275,290,305,'Published shares','GPT-5.1: 24.4%\nLlama 8B: 3.7%\n\nShares sum to 96.1%.\nShown as printed;\nnot renormalized.','gray',24)
 return end(s,'Table 7; descriptive model-level comparison','The most vulnerable target contributes the smallest published producer share.')

def s23(n):
 s=base('controls-and-scope',n,'What the design controls, and what can still vary',part='Discussion')
 panel(s,70,180,700,500,'Controlled comparisons','Question, target and wrong option\nheld within-item\n\nBlind vs self uses the same argument\n\nTemperature and reasoning-mode setup\nheld fixed\n\nCross condition fixes k = 10','green',28)
 panel(s,830,180,700,500,'Remaining variation','Changing k regenerates the argument\n\nA different source changes content\nas well as source identity\n\nEligibility differs across models\n\nAttribution adds a persuasive cue','orange',28)
 return end(s,'§§3–4; reviewer interpretation distinguished in notes','The design isolates specific comparisons; it does not identify every causal mechanism.')

def s24(n):
 s=base('balanced-revision',n,'Good revision depends on the evidence','A proposed complementary test, not an experiment in this paper','Next experiments')
 s.text(85,190,'WRONG ARGUMENT',25,P['orange']['text'],mono=True)
 node(s,85,265,390,115,'Correct first answer','green',34)
 arr(s,501,322,610,322,'orange');node(s,640,265,375,115,'Invalid challenge','orange',32)
 arr(s,1040,322,1140,322,'green');node(s,1170,265,345,115,'Keep it correct','green',33)
 s.text(85,470,'VALID CORRECTION',25,P['blue']['text'],mono=True)
 node(s,85,545,390,115,'Incorrect first answer','red',34)
 arr(s,501,602,610,602,'blue');node(s,640,545,375,115,'Valid evidence','blue',32)
 arr(s,1040,602,1140,602,'green');node(s,1170,545,345,115,'Revise to correct','green',33)
 return end(s,'Limitations / proposed complementary evaluation','A useful model resists misleading arguments and accepts justified corrections.')

def s25(n):
 s=base('limitations',n,'What the evidence covers','The results describe this controlled setting','Scope')
 items=[('Benchmark','MMLU multiple-choice questions','Open-ended tasks remain untested.'),('Interaction','One model-generated challenge','Human arguments and multi-turn exchanges remain untested.'),('Inference','The paper\'s fixed model settings','Reasoning-enabled behavior requires a separate evaluation.'),('Intervention','Measurement of answer instability','The paper does not test a mitigation.')]
 for i,(a,b,c) in enumerate(items):
  y=195+i*133;s.text(85,y,a,29,P['blue']['text'],hand=True);s.text(440,y,b,33);s.text(440,y+52,c,27,P['muted'])
  if i<3:s.line([(85,y+105),(1510,y+105)],P['grid'],1,roughness=0)
 return end(s,'Experimental setup and Limitations','The measured failure is real within this setting. Its reach is an empirical question.')

def s26(n):
 s=base('source-audit',n,'Source details and reported inconsistencies','Reported numbers are preserved. These discrepancies qualify particular summaries.','Discussion')
 rows=[['Length means','Table 2 includes 47.3% at k = 3.','Prose range 48.4–50.2 omits it.'],['Subject categories','Table 5 lists 8 STEM subjects in the lowest 10.','Prose says 9 of 10.'],['Producer shares','Table 7 shares sum to 96.1%.','Do not normalize or invent the missing share.'],['Cross-matrix range','Figure 4 has 57–94% for the Llama-70B target.','Prose claims column ranges of at most 10 pp.']]
 s.table(70,190,[300,620,540],rows,['detail','source evidence','reading note'],fs=24,rh=108,aligns=['l','l','l'])
 return end(s,'Tables 2, 5, 7; Figure 4; full audit in references/digest.md','These checks qualify particular summaries; they do not erase the observed answer flips.')

def s27(n):
 s=base('held-out-transfer',n,'Does MaxFlip transfer to an unseen target?','Proposed next experiment, not a reported result','Next experiments')
 s.text(80,190,'SELECT',28,P['purple']['text'],mono=True)
 node(s,80,270,390,180,'Pool candidate\nwrong arguments','orange',34)
 arr(s,495,360,575,360)
 node(s,600,270,460,180,'Choose the argument\nusing selection models','purple',33)
 s.text(620,490,'The held-out target contributes\nno flip outcomes to selection.',29,P['purple']['text'])
 arr(s,1085,360,1165,360,'blue')
 node(s,1190,270,330,180,'Freeze the\nselected set','blue',33)
 arr(s,1355,475,1355,565,'blue')
 node(s,975,592,545,115,'Evaluate an unseen target','green',32)
 s.text(80,625,'This separates selection strength\nfrom transfer to another model.',33)
 return end(s,'Proposed follow-up to §5.7','Selecting and evaluating on the same model set leaves this question open.')

def s28(n):
 s=base('takeaways',n,'Evaluate stability alongside accuracy')
 s.text(90,192,'A correct answer can still flip.',43,P['blue']['text'],hand=True)
 s.text(95,259,'Mean blind AFR ranges from 17.5% to 97.3%.',31)
 s.text(90,371,'Arguing and resisting are different abilities.',43,P['purple']['text'],hand=True)
 s.text(95,438,'Resistant targets can produce persuasive wrong arguments.',31)
 s.text(90,550,'Selected arguments make stronger challenges.',43,P['orange']['text'],hand=True)
 s.text(95,617,'MaxFlip adds up to 23.6 percentage points in the evaluated pool.',31)
 s.line([(80,722),(1520,722)],P['blue']['stroke'],2,roughness=0)
 s.text(80,753,'Paper: arxiv.org/abs/2606.16011v2',25,P['blue']['text'])
 s.text(80,797,'Code: github.com/nafisenik/WhoFlips     Data: huggingface.co/datasets/nafisehNik/WhoFlips',23,P['muted'])
 return end(s,'Tables 2 and 7 / Figure 5 / backup slides follow')

def s29(n):
 s=base('all-model-lengths',n,'Longer arguments push models in different directions','Seven small multiples; identical 0–100% axes; whiskers show reported 95% CIs','Backup')
 for i in range(7):
  col,row=i%4,i//4; x=110+col*370;y=225+row*285;w=270;h=155
  s.text(x,y-43,SHORT[i],26,P[COLORS[i]]['text'])
  f=xy_axes(s,x,y,w,h,10,100,(1,3,5,10),(0,50,100))
  pts=[f(k,v) for k,v in zip(K,AFR[i])]
  s.line(pts,P[COLORS[i]]['stroke'],3,roughness=0)
  for k,v,ci in zip(K,AFR[i],AFR_CI[i]):
   a,b=f(k,v-ci),f(k,v+ci);dot(s,*f(k,v),COLORS[i],5);s.line([a,b],P[COLORS[i]]['text'],1,roughness=0)
   for xx,yy in (a,b): s.line([(xx-4,yy),(xx+4,yy)],P[COLORS[i]]['text'],1,roughness=0)
  s.text(x+w,y+h+44,f'{AFR[i][-1]-AFR[i][0]:+.1f} pp: k1 → k10',19,P[COLORS[i]]['text'],anchor='r')
 s.text(1220,510,'Argument length k\n= 1, 3, 5, 10 sentences\n\nQwen 4B and 9B rise;\nseveral others fall.',25)
 return end(s,'Table 2; points connected only to guide the eye','Pooling all models hides opposing trends; downward trends were not significant.')

SLIDES=[s01,s03,s04,s05,s09,s10,s12,s15,s02,s16,s19,s17,s20,s21,s22,s13,s25,s27,s24,s28,s07,s06,s29,s08,s11,s14,s18,s26]
