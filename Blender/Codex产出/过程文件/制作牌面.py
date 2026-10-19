from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json
O=Path(__file__).resolve().parents[1]
W,H=2400,1900
F='/System/Library/Fonts/Hiragino Sans GB.ttc'
E='/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf'
cream='#F6E9C9'; red='#A72D2B'; edge='#66342C'; gold='#C29B52'
# Original artwork. All colour and light layers share this exact canvas.
outline=[('M',160,430),('Q',160,275,315,275),('L',655,275),('Q',1120,-35,1585,275),('L',1925,275),('Q',2080,275,2080,430),('L',2080,1140),('L',2360,1420),('L',2080,1700),('L',2080,1740),('Q',2080,1810,2010,1810),('L',315,1810),('Q',160,1810,160,1655),('Z',)]
def path(im,seq,fill,stroke=None,sw=1):
 pts=[]
 for item in seq:
  if item[0] in ['M','L']: pts.append(tuple(item[1:]))
  elif item[0]=='C':
   p0=pts[-1]; x1,y1,x2,y2,x3,y3=item[1:]
   for j in range(1,65):
    t=j/64;u=1-t
    pts.append((u**3*p0[0]+3*u*u*t*x1+3*u*t*t*x2+t**3*x3,u**3*p0[1]+3*u*u*t*y1+3*u*t*t*y2+t**3*y3))
  elif item[0]=='Z': pts.append(pts[0])
 d=ImageDraw.Draw(im)
 if fill:d.polygon(pts,fill=fill)
 if stroke:
  d.line(pts,fill=stroke,width=sw,joint='curve')
  for x,y in pts: d.ellipse((round(x-sw/2),round(y-sw/2),round(x+sw/2),round(y+sw/2)),fill=stroke)
# Cubic curves give the raised crown its streamlined 1950s silhouette.
P=[('M',150,430),('C',150,330,210,275,315,275),('L',650,275),('C',920,55,1320,55,1590,275),('L',1925,275),('C',2030,275,2090,330,2090,430),('L',2090,1130),('L',2370,1410),('L',2090,1690),('L',2090,1720),('C',2090,1780,2050,1810,1990,1810),('L',315,1810),('C',210,1810,150,1750,150,1650),('Z',)]
A=[('M',225,1180),('L',1840,1180),('L',1840,1010),('L',2235,1410),('L',1840,1740),('L',1840,1600),('L',225,1600),('Z',)]
def fit_text(im,t,box,font,color,index=0,stroke=0):
 font=ImageFont.truetype(font,600,index=index); bb=font.getbbox(t,stroke_width=stroke)
 m=Image.new('RGBA',(bb[2]-bb[0]+12,bb[3]-bb[1]+12));d=ImageDraw.Draw(m);d.text((6-bb[0],6-bb[1]),t,font=font,fill=color,stroke_width=stroke,stroke_fill=color)
 bw,bh=box[2]-box[0],box[3]-box[1]; scale=min(bw/m.width,bh/m.height)
 m=m.resize((round(m.width*scale),round(m.height*scale)),Image.Resampling.LANCZOS)
 im.alpha_composite(m,(round((box[0]+box[2]-m.width)/2),round((box[1]+box[3]-m.height)/2)))
def star(d,x,y,r,color):
 d.polygon([(x,y-r),(x+r*.18,y-r*.18),(x+r,y),(x+r*.18,y+r*.18),(x,y+r),(x-r*.18,y+r*.18),(x-r,y),(x-r*.18,y-r*.18)],fill=color)
bulbs=[(1955,1250),(2045,1330),(2135,1410),(2045,1490),(1955,1570)]
for mode in ['A','B']:
 main=Image.new('RGBA',(W,H)); isA=mode=='A'; bg=cream if isA else red; ink=red if isA else cream
 path(main,P,bg,edge,18)
 # inset rim follows original silhouette by scaling around its centre
 rim=[]
 for s in P:
  rim.append(tuple([s[0]]+[round(1200+(v-1200)*.954) if i%2==0 else round(950+(v-950)*.943) for i,v in enumerate(s[1:])]))
 path(main,rim,None,ink,18)
 d=ImageDraw.Draw(main);star(d,1120,300,92,ink)
 for x1,x2 in [(390,850),(1390,1850)]:
  d.rounded_rectangle((x1,309,x2,325),radius=8,fill=ink)
  d.rounded_rectangle((x1+90,351,x2-40,361),radius=5,fill=ink)
 # The three large Chinese glyphs dominate the sign at a 200 px display width.
 fit_text(main,'收银台',(320,485,1910,1040),F,ink,2,5)
 path(main,A,red if isA else cream)
 fit_text(main,'CHECKOUT',(335,1245,1740,1510),E,cream if isA else red)
 d=ImageDraw.Draw(main)
 # Lamps only on the directional chevron; keep main title crisp and unlit.
 for x,y in bulbs:
  d.ellipse((x-38,y-38,x+38,y+38),fill=edge)
  d.ellipse((x-28,y-28,x+28,y+28),fill=gold)
  d.ellipse((x-20,y-20,x+20,y+20),fill='#EAD7AA')
 name='A_奶油搪瓷箭头' if isA else 'B_樱桃红复古箭头'
 main.save(O/(name+'_正面.png'))
 light=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(light)
 for x,y in bulbs:ld.ellipse((x-20,y-20,x+20,y+20),fill='#FFF2C9')
 light.save(O/(name+'_发光层.png'))
 # Proof, only: matching registered layer preview, no baked halo in deliverables.
 lit=Image.alpha_composite(main,light);lit.save(O/'过程文件'/(name+'_对位核对.png'))
 small=main.resize((200,158),Image.Resampling.LANCZOS)
 proof=Image.new('RGB',(300,258),'#D8D5CE');proof.paste(small,(50,50),small)
 proof.save(O/'过程文件'/(name+'_200px可读性.png'))
(O/'过程文件'/'灯泡坐标.json').write_text(json.dumps({'canvas':[W,H],'centres':bulbs,'emitter_radius':20,'outline':P},ensure_ascii=False,indent=2))
