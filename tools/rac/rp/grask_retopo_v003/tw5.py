from PIL import Image, ImageDraw, ImageFont
D='/tmp/claude-0/rt/tw'; F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20); FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',28)
w=500; rows=[('RIGHT',['zsrc','zv2c','zv3c'],['zsrcw','zv2','zv3']),('LEFT',['zsrcL','zv2cL','zv3cL'],['zsrcwL','zv2L','zv3L'])]
cols=['v005 source (frozen)','v002 (submitted 2026-10-25)','v003 (this turn-in)']
S=Image.new('RGB',(20+3*(w+10),120+4*(w+40)+200),'white'); d=ImageDraw.Draw(S)
d.text((20,20),'Thumb web saddle: source vs v002 vs v003 (identical cameras, 5 cm field, thumb-side view)',fill='black',font=FB)
d.text((20,62),'v003 = v002 retopology corrected: quads relaxed along the frozen source surface. The anatomy (the hollow) is unchanged source.',fill=(40,40,40),font=F)
y=110
for side,clay,wire in rows:
    for tags,kind in ((clay,'clay'),(wire,'wire')):
        x=20
        for t,cn in zip(tags,cols):
            S.paste(Image.open('%s/%s_zz.png'%(D,t)).resize((w,w)),(x,y+30)); d.text((x,y),'%s hand  %s - %s'%(side,cn,kind),fill=(10,10,120),font=F); x+=w+10
        y+=w+40
for n in ['The hollow between thumb and index metacarpals is frozen v005 anatomy and is kept (left column).',
          'v002 shaded with faint rumples at the saddle (uneven quad spacing). v003 relaxes those quads on the source surface: the rumples are gone; a faint',
          'shading variation remains at the web-floor pole (right hand, lower centre). Deviation within 2.5 cm stays <= 0.8 mm (T-2). No source anatomy was edited.']:
    d.text((20,y),n,fill=(20,20,90),font=F); y+=40
S.save(D+'/TW5_thumb_web_v002_vs_v003.png'); print(S.size)
