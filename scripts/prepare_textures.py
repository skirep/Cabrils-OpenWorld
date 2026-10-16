"""Prepare locally downloaded CC0 Poly Haven maps for the web.
Run: python3 scripts/prepare_textures.py /path/to/downloaded-maps
Expected source names: <asset>_diff.jpg and <asset>_normal.jpg.
Photographs of Cabrils are visual references only and are not redistributed.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageEnhance
import sys,json,hashlib
src=Path(sys.argv[1]);out=Path(__file__).resolve().parents[1]/'public/textures';out.mkdir(parents=True,exist_ok=True)
assets={'plaster':'plastered_wall','roof':'clay_roof_tiles_02','stone':'rustic_stone_wall_02','asphalt':'asphalt_02','cobble':'cobblestone_floor_03','soil':'brown_mud_leaves_01','pavement':'concrete_pavement'}
manifest=[]
for key,asset in assets.items():
 for kind in ['diff','normal']:
  source=src/f'{asset}_{kind}.jpg';im=Image.open(source).convert('RGB').resize((512,512),Image.Resampling.LANCZOS)
  name=f'{key}-{kind}.webp';im.save(out/name,'WEBP',quality=88 if kind=='normal' else 82,method=6)
  manifest.append({'file':name,'asset':asset,'source':f'https://dl.polyhaven.org/file/ph-assets/Textures/jpg/1k/{asset}/{asset}_{"nor_gl" if kind=="normal" else "diff"}_1k.jpg','page':f'https://polyhaven.com/a/{asset}','license':'CC0-1.0','original_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'size':512})
# A 7 x 6.4 m facade atlas: photographed plaster, original window/door artwork.
plaster=Image.open(src/'plastered_wall_diff.jpg').convert('L').resize((512,512),Image.Resampling.LANCZOS)
for idx,(low,high,shutter) in enumerate([('#d4d0c4','#fffdf6','#3e5149'),('#d1c4a8','#f8ecd0','#5c5147'),('#d1bda3','#efddc0','#484e4c')]):
 base=ImageOps.colorize(plaster,low,high);im=Image.new('RGB',(1024,1024))
 for y in range(0,1024,512):
  for x in range(0,1024,512):im.paste(base,(x,y))
 g=ImageDraw.Draw(im)
 # Two bays and two floors. Sills ~1m above each floor; narrow iron grilles.
 for row in range(2):
  for bay in range(2):
   x=bay*512+180;y=row*512+125
   g.rectangle((x-20,y-15,x+145,y+259),fill='#c5bda9')
   g.rectangle((x-15,y-15,x+140,y+250),fill='#e7dfce')
   g.rectangle((x,y,x+125,y+235),fill='#293b3d')
   g.rectangle((x+7,y+8,x+59,y+224),fill='#657875')
   g.polygon([(x+8,y+8),(x+58,y+8),(x+8,y+123)],fill='#91a09a')
   g.rectangle((x+65,y+8,x+117,y+224),fill='#4c605c')
   for side in [-1,1]:
    sx=x-58 if side==-1 else x+132
    g.rectangle((sx,y-2,sx+49,y+237),fill=shutter)
    for line in range(y+7,y+234,12):g.line((sx+4,line,sx+44,line),fill='#242f2b',width=2)
   g.rectangle((x-19,y+237,x+145,y+252),fill='#aaa28e')
   g.line((x-19,y+238,x+145,y+238),fill='#e7dfcc',width=3)
   if row==1:
    for bar in range(x+7,x+125,23):g.line((bar,y+112,bar,y+235),fill='#252e2c',width=3)
    g.line((x,y+149,x+125,y+149),fill='#252e2c',width=3)
 name=f'facade-{idx}.webp';im.save(out/name,'WEBP',quality=88,method=6)
 manifest.append({'file':name,'asset':'plastered_wall','page':'https://polyhaven.com/a/plastered_wall','license':'CC0-1.0 + original MIT artwork','derived':True,'size':1024})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('Prepared',len(manifest),'maps;',sum(f.stat().st_size for f in out.glob('*.webp')),'bytes')
