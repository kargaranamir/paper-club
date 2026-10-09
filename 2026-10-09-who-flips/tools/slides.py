"""Who Flips? paper club. Same Python -> Excalidraw workflow as QARM V2.
All empirical numbers are in data.py and references/digest.md. Toy examples are labeled.
"""
from slidekit import Slide, P
from data import *

SRC='Who Flips? arXiv:2606.16011v2'

def base(slug,n,title,sub='',part=''):
 s=Slide(slug,n); s.title(title,sub,part); return s

def end(s,source,take=None):
 if take: s.takeaway(take,fs=26)
 s.footer(SRC+' | '+source); return s

def panel(s,x,y,w,h,title,body,c='blue',fs=28):
 s.box(x,y,w,h,c=c,fill=P[c]['soft']); s.text(x+24,y+22,title,32,P[c]['text'])
 s.text(x+24,y+85,body,fs)

def node(s,x,y,w,h,text,c='blue',fs=27):
 s.box(x,y,w,h,text,c,fs)

def arr(s,x1,y1,x2,y2,c='ink'):
 s.arrow([(x1,y1),(x2,y2)], P[c] if c=='ink' else P[c]['stroke'])

def dot(s,x,y,c,r=7):
 s.box(x-r,y-r,r*2,r*2,c=c,shape='ellipse',roughness=0,sw=1)

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

def s01(n):
 s=Slide('title',n);s.text(70,90,'PAPER CLUB  /  9 OCTOBER 2026',21,P['muted'])
 s.text(70,150,'Who Flips?',88)
 s.text(72,272,'Self- and Cross-Model Counterarguments Reveal\nAnswer Instability in LLMs',38)
 s.text(72,390,'Paper authors and affiliations: see the linked arXiv paper',24,P['muted'])
 s.text(72,435,'TUM, MCML, MDSI and LMU Munich',22,P['muted'])
 s.text(72,488,'arXiv:2606.16011v2  /  30 August 2026  /  EMNLP Findings 2026',22,P['muted'],mono=True)
 node(s,72,600,340,94,'Initially correct','green',31);arr(s,427,647,530,647)
 node(s,545,600,440,94,'Plausible wrong argument','orange',29);arr(s,999,647,1100,647)
 node(s,1115,600,410,94,'Still correct?','purple',32)
 s.text(72,740,'Accuracy measures the first answer. Stability tests what happens next.',29,P['blue']['text'])
 return end(s,'Paper title, abstract and protocol; original explanatory drawings')

def s02(n):
 s=base('one-slide',n,'The paper in one slide')
 panel(s,70,168,460,550,'Question','When a model knows the\ncorrect answer, can a wrong\nargument make it change?\n\nTest only initially correct\nanswers after successful\nargument generation.','orange')
 panel(s,567,168,460,550,'Experiment','7 models, 57 MMLU subjects\n2,052 questions\n\nVary argument length,\nself-attribution and the\nmodel that wrote the\nwrong argument.','blue')
 panel(s,1064,168,466,550,'Main results','17.5% to 97.3% mean\nblind answer flip rate\n\n+7.1 pp mean effect of\nself-attribution\n\nMaxFlip: up to +23.6 pp','purple')
 return end(s,'§§3–5; Tables 2, 3 and 7','Answer stability adds a different measurement alongside accuracy.')

def s03(n):
 s=base('toy-example',n,'A correct answer can be lost after a challenge','Illustrative example for teaching; not a measured paper example','Protocol')
 node(s,70,190,620,140,'Which is prime?\nA: 9     B: 11     C: 15     D: 21','gray',31)
 node(s,70,390,620,110,'Initial answer: B (11)','green',32)
 arr(s,380,337,380,376)
 panel(s,825,190,700,260,'Wrong-option argument','“9 is odd, and odd numbers are prime.\nTherefore A is correct.”\n\nThe premise does not justify the claim.','orange',28)
 arr(s,700,445,810,445)
 node(s,825,520,315,120,'Hold: B\nstill correct','green');node(s,1210,520,315,120,'Flip: A\nnow wrong','red')
 s.text(80,590,'An answer change counts as a flip\nif the final option is any wrong option.',28,P['purple']['text'])
 return end(s,'Protocol definition; toy question and argument written for this deck','Good revision requires checking the argument, not just accepting its conclusion.')

def s04(n):
 s=base('two-stage-protocol',n,'Two stages keep generation and challenge separate',part='Protocol')
 s.text(70,175,'Stage I: source model, isolated session',31,P['orange']['text'])
 node(s,70,240,360,130,'Question + wrong option\n+ requested length k','gray')
 arr(s,445,305,515,305);node(s,530,240,370,130,'Generate a committed\nwrong-answer argument','orange')
 arr(s,915,305,985,305);node(s,1000,240,530,130,'Argument exists?\nRefusal excludes this attempt','gray')
 s.text(70,442,'Stage II: target model, fresh session',31,P['blue']['text'])
 for x,w,t,c in [(70,310,'Answer original\nquestion','blue'),(450,310,'Keep only\ncorrect answers','green'),(830,310,'Show Stage I\nargument','orange'),(1210,320,'Answer again\nand score','purple')]: node(s,x,510,w,135,t,c)
 for x in (392,772,1152): arr(s,x,578,x+45,578)
 return end(s,'§3 and Appendix A','The source generates the challenge before the target is evaluated.')

def s05(n):
 s=base('afr-denominator',n,'Answer flip rate has a conditional denominator',part='Protocol')
 s.text(110,204,'AFR =',54,P['purple']['text'])
 s.text(875,207,'eligible challenges ending in a wrong answer',33,anchor='c')
 s.line([(360,260),(1430,260)],P['ink'],2)
 s.text(875,287,'initially correct answer + available wrong argument',31,anchor='c')
 panel(s,70,390,700,300,'What AFR answers','Of the eligible challenges, how often\ndid the model lose a correct answer?\n\nA flip need not choose the defended option.','purple',28)
 panel(s,825,390,700,300,'What AFR leaves out','Initially incorrect answers\nRefused generation attempts\n\nIt is not the final error rate on all MMLU.','gray',28)
 return end(s,'Definition 3.1','Report coverage together with AFR so the tested population stays visible.')

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
 s=base('blind-afr',n,'Mean blind flip rates span almost 80 percentage points','Average over k = 1, 3, 5, 10; lower means more stable','Results')
 bars(s,MODELS,MEAN,MEAN_CI,colors=['red','orange','orange','purple','blue','blue','green'])
 return end(s,'Table 2; whiskers show reported 95% CI','Even the most stable model here flips on 17.5% of eligible challenges.')

def s10(n):
 s=base('argument-length',n,'Longer arguments have model-dependent effects',part='Results')
 rows=[[m]+[f'{v:.1f}' for v in a]+[f'{a[-1]-a[0]:+.1f}'] for m,a in zip(MODELS,AFR)]
 s.table(70,178,[430,170,170,170,170,350],rows,['blind AFR (%)','k = 1','k = 3','k = 5','k = 10','k10 minus k1 (pp)'],fs=25,rh=62)
 s.text(85,717,'Across-model means: 48.4, 47.3, 48.5, 50.2%. The average hides opposite trends.',25,P['muted'])
 return end(s,'Table 2; all per-cell CIs in references/digest.md','Qwen 4B and 9B increase most; the paper reports no significant downward trends.')

def s11(n):
 s=base('model-scale',n,'Size tracks stability within Qwen, but not across families',part='Results')
 s.text(75,172,'Qwen3.5 family: mean blind AFR (%)',29,P['blue']['text'])
 s.grouped_bars(140,245,750,410,['4B','9B','35B'],[[64.3,39.3,17.5]],0,100,[0,25,50,75,100],['blue'],values=True,fs=25)
 panel(s,1000,220,530,370,'Across families','Llama-3.3-70B: 75.8%\nQwen3.5-9B: 39.3%\n\nParameter count alone\ndoes not order these\nmodels by stability.','orange',28)
 return end(s,'Table 2; §5.1','This comparison is descriptive: model families differ in more than size.')

def s12(n):
 s=base('self-attribution',n,'Calling it “your earlier reasoning” increases flips','Same items, same argument; only attribution changes','Results')
 paired(s,MEAN,SELF,SAD,SAD_CI,'self-attributed')
 return end(s,'Table 3; change ± reported 95% CI half-width','Mean self-attribution delta: +7.1 pp. Qwen3.5-4B shifts by +18.7 pp.')

def s13(n):
 s=base('refusal-vs-resistance',n,'Refusing to write a wrong argument differs from resisting it',part='Results')
 s.table(70,175,[430,340,300,390],[[m,f'{a:.1f}%',f'{b:+.1f} pp',f'{c:.1f}%'] for m,a,b,c in zip(MODELS,CRR,RSS,COMBINED)],['model','generation refusal','refusal selectivity','later AFR (blind + self)'],fs=24,rh=64)
 s.text(80,728,'Selectivity = refusal on initially correct items minus refusal on initially incorrect items.',24,P['muted'])
 return end(s,'Table 4; §5.3','Llama-3.1-8B: 41.3% refusal yet 97.5% AFR. These measure distinct behaviors.')

def s14(n):
 s=base('linguistic-correlates',n,'Language differs between held and flipped answers','Descriptive associations from lexical features, not causal explanations','Results')
 panel(s,70,185,700,480,'After the challenge','Held answers: more resistance phrases\n\nFlipped answers: about 6x as many\ncapitulation markers\n\nHeld responses are longer:\nabout 1,800 vs 1,150 characters.','blue',29)
 panel(s,830,185,700,480,'Before the challenge','Later flips associate with:\n\nMore baseline hedging\nLonger baseline responses\n\nHigher confidence in the wrong argument\ndoes not straightforwardly predict flips.','orange',27)
 s.text(80,703,'Manually curated lexicons; case-insensitive substring matching.',25,P['muted'])
 return end(s,'§5.4; Figure 2; Appendix B','Response markers partly describe the outcome; they do not establish why it happened.')

def s15(n):
 s=base('subject-domains',n,'Instability also varies by subject','Selected subjects; averages pool models, lengths and attribution conditions','Results')
 bars(s,[v[0] for v in SUBJECTS],[v[1] for v in SUBJECTS],[v[2] for v in SUBJECTS],x=490,w=860,gap=75,colors=['orange']*3+['green']*3)
 return end(s,'Table 5; selected extremes; whiskers: reported 95% CI','Moral disputes: 80.8%. Elementary mathematics: 20.9%. Causes remain untested.')

def s16(n):
 s=base('cross-matrix',n,'Who writes the argument, and who is challenged?','Blind, k = 10. Rows = source, columns = target. Values rounded as in Figure 4.','Cross-model results')
 short=['GPT\n5.1','Gemma\n26B','Llama\n8B','Llama\n70B','Qwen\n35B','Qwen\n4B','Qwen\n9B']
 x,y,cw,rh=335,255,166,65
 for j,m in enumerate(short): s.text(x+(j+.5)*cw,179,m,24,anchor='c')
 for i,m in enumerate(MATRIX_MODELS):
  s.text(x-20,y+i*rh+rh/2,m,23,anchor='r',valign='m')
  for j,v in enumerate(MATRIX[i]):
   c='gray' if i==j else ('green' if v<30 else 'yellow' if v<60 else 'orange' if v<85 else 'red')
   s.box(x+j*cw,y+i*rh,cw-6,rh-6,f'{v}%',c,26,round_=False,roughness=0,sw=1)
 return end(s,'Figure 4; diagonal: same source, off-diagonal: cross source','Many sources can destabilize the same vulnerable target, but source effects remain.')

def s17(n):
 s=base('cross-vs-same',n,'A different source does not increase flips on average','Compare same-source blind AFR with mean cross-source AFR at k = 10','Cross-model results')
 rows=[[m,f'{a[-1]:.1f}',f'{c:.1f}',f'{d:+.1f} ± {ci:.1f}'] for m,a,c,d,ci in zip(MODELS,AFR,CROSS,CROSS_DELTA,CROSS_CI)]
 s.table(70,190,[460,320,320,360],rows,['target','same source (%)','cross source (%)','change (pp), 95% CI'],fs=26,rh=66)
 return end(s,'Table 6; averages over the other six source models','Mean change: -1.6 pp. Opposing target-specific effects disappear in that average.')

def s18(n):
 s=base('variance-decomposition',n,'Target susceptibility explains most reported variance',part='Cross-model results')
 vals=[76.7,12.0,9.3];labs=['Target / baseline','Argument source','Subject'];ci=[(74.8,78.7),(10.1,14.5),(9.2,13.6)]
 for i,(lab,v,(lo,hi)) in enumerate(zip(labs,vals,ci)):
  y=235+i*132;s.text(70,y,lab,32);s.box(430,y,800*v/100,45,c=['blue','orange','purple'][i],round_=False)
  s.text(1260,y,f'{v:.1f}%',34);s.text(430,y+58,f'95% CI [{lo:.1f}, {hi:.1f}]',23,P['muted'])
 s.text(80,680,'Reported decomposition across target, source and subject triples.',27,P['muted'])
 return end(s,'§5.6; reported components sum to 98.0%','Source identity contributes, but target identity dominates this analysis.')

def s19(n):
 s=base('source-and-target-roles',n,'Resistance and persuasive errors are separate roles',part='Cross-model results')
 panel(s,70,180,700,430,'EP: susceptibility as a target','Average a target column,\nexcluding the diagonal.\n\nHow often do other models’\narguments flip this target?\n\nLower EP means more resistance.','blue',30)
 panel(s,830,180,700,430,'EA: efficacy as a source','Average a source row,\nexcluding the diagonal.\n\nHow often does this source’s\nwrong argument flip other models?\n\nHigher EA means more effective errors.','orange',30)
 s.text(80,670,'Llama-3.1-8B: EP about 99%, EA about 24% (paper’s rounded summary).',28)
 return end(s,'Definition 5.3; §5.6; Figure 5','The strongest sources of wrong arguments can also be among the most stable targets.')

def s20(n):
 s=base('maxflip-selection',n,'MaxFlip selects a strong argument for each question',part='MaxFlip')
 node(s,70,220,340,180,'One question\n\nPool wrong arguments\nfrom source models','blue',27)
 arr(s,423,310,495,310);node(s,510,220,450,180,'Test candidates against\nthe target models\n\nCount how many flip','orange',27)
 arr(s,973,310,1045,310);node(s,1060,220,470,180,'Keep the argument that\nflips the most models\n\nBreak ties randomly','purple',27)
 s.text(100,488,'Repeat for each question',36,P['purple']['text'])
 panel(s,70,565,1460,155,'Evaluation question','Does a selected pool challenge models more than their own standard blind k = 10 arguments?','gray',27)
 return end(s,'§5.7; Table 7','Selection uses observed flips, so held-out targets are a useful next test of generalization.')

def s21(n):
 s=base('maxflip-results',n,'MaxFlip raises AFR most for models in the middle','Standard = same-source blind k = 10; changes and CIs as reported','MaxFlip')
 paired(s,[r[-1] for r in AFR],CURATED,GAIN,GAIN_CI,'MaxFlip')
 return end(s,'Table 7; change ± reported 95% CI half-width','Qwen3.5-9B: +23.6 pp. GPT-5.1: +2.4 pp, not statistically significant.')

def s22(n):
 s=base('maxflip-producers',n,'Stable targets often supply the selected wrong arguments','Producer shares as printed in Table 7; not renormalized','MaxFlip')
 idx=[4,5,6,2,1,3,0]
 bars(s,[MODELS[i] for i in idx],[PRODUCER[i] for i in idx],x=450,w=810,maxv=30,colors=['blue','blue','blue','orange','orange','orange','gray'])
 return end(s,'Table 7; published shares sum to 96.1%, not 100%; see audit','GPT-5.1 supplies 24.4% of the selected arguments; Llama-3.1-8B supplies 3.7%.')

def s23(n):
 s=base('controls-and-scope',n,'What the design controls, and what can still vary',part='Discussion')
 panel(s,70,180,700,500,'Controlled comparisons','Question, target and wrong option\nheld within-item\n\nBlind vs self uses the same argument\n\nTemperature and reasoning-mode setup\nheld fixed\n\nCross condition fixes k = 10','green',28)
 panel(s,830,180,700,500,'Remaining variation','Changing k regenerates the argument\n\nA different source changes content\nas well as source identity\n\nEligibility differs across models\n\nAttribution adds a persuasive cue','orange',28)
 return end(s,'§§3–4; reviewer interpretation distinguished in notes','The design isolates specific comparisons; it does not identify every causal mechanism.')

def s24(n):
 s=base('strengths',n,'Why this is a useful evaluation contribution',part='Discussion')
 for y,num,head,body,c in [(180,'1','A failure standard accuracy misses','An initially correct answer can still fail during the next exchange.','blue'),(360,'2','A reusable protocol with multiple controls','Length, attribution and source appear in one framework.','purple'),(540,'3','A released challenge resource','The protocol, records and MaxFlip support follow-up evaluation.','green')]:
  node(s,70,y,95,95,num,c,44);s.text(205,y+2,head,34,P[c]['text']);s.text(205,y+62,body,28)
 return end(s,'Introduction, conclusion and released resources','The contribution is measurement and characterization; the paper does not test a fix.')

def s25(n):
 s=base('limitations',n,'The results have a specific scope',part='Discussion')
 panel(s,70,180,700,510,'Limits stated by the authors','MMLU only\n\nOne challenge per exchange\n\nModel-generated English arguments\n\nNo tested mitigation\n\nNo incorrect-to-correct revision study','orange',29)
 panel(s,830,180,700,510,'Questions for follow-up','How do reasoning-enabled models behave?\n\nDoes MaxFlip transfer to unseen targets?\n\nCan a model resist bad evidence while\nstill accepting a valid correction?\n\nHow do rates change on a common\neligible subset?','purple',28)
 return end(s,'Limitations; right column: proposed follow-up experiments','Resistance to wrong arguments is valuable; blanket refusal to revise would not be enough.')

def s26(n):
 s=base('source-audit',n,'A few source details need careful reading','The deck uses table values and records discrepancies without silently correcting the paper.','Discussion')
 rows=[['Length means','Table 2 includes 47.3% at k = 3.','Prose range 48.4–50.2 omits it.'],['Subject categories','Table 5 lists 8 STEM subjects in the lowest 10.','Prose says 9 of 10.'],['Producer shares','Table 7 shares sum to 96.1%.','Do not normalize or invent the missing share.'],['Cross-matrix range','Figure 4 has 57–94% for the Llama-70B target.','Prose claims column ranges of at most 10 pp.']]
 s.table(70,190,[300,620,540],rows,['detail','source evidence','reading note'],fs=24,rh=108,aligns=['l','l','l'])
 return end(s,'Tables 2, 5, 7; Figure 4; full audit in references/digest.md','These checks qualify particular summaries; they do not erase the observed answer flips.')

def s27(n):
 s=base('discussion-questions',n,'What would make the next experiment more informative?',part='Discussion')
 for y,a,b in [(185,'Held-out transfer','Select MaxFlip without the evaluated target, then test that target.'),(330,'Balanced revision','Test correct-to-wrong and incorrect-to-correct changes together.'),(475,'Evidence checking','Compare baseline responses with explicit verification or tool access.'),(620,'Comparable populations','Report shared-subset AFR, coverage and per-subject uncertainty.')]:
  s.text(75,y,a,33,P['purple']['text']);s.text(75,y+55,b,29)
 return end(s,'Proposed discussion and follow-up work, not results from the paper')

def s28(n):
 s=base('takeaways',n,'Accuracy is only the start of the conversation')
 items=[('Correct first answers can be fragile.','Mean blind AFR spans 17.5% to 97.3% in this setup.','blue'),('The framing of an argument matters.','Self-attribution adds +7.1 pp on average.','orange'),('Source and target play different roles.','Target susceptibility dominates, while selected sources strengthen challenges.','purple'),('MaxFlip is a useful stress test.','Next: unseen targets, valid corrections and tested mitigations.','green')]
 for i,(h,b,c) in enumerate(items):
  y=160+i*138;s.box(70,y,1460,116,c=c,fill=P[c]['soft']);s.text(95,y+15,h,30,P[c]['text']);s.text(95,y+62,b,26)
 s.text(75,751,'Paper: arxiv.org/abs/2606.16011v2',23,P['blue']['text'])
 s.text(75,791,'Code: github.com/nafisenik/WhoFlips    Data: hf.co/datasets/nafisehNik/WhoFlips',22,P['muted'])
 return end(s,'Tables 2, 3, 7; §5.6; conclusion; proposed next steps clearly labeled')

SLIDES=[s01,s02,s03,s04,s05,s06,s07,s08,s09,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21,s22,s23,s24,s25,s26,s27,s28]
