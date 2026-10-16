"""Download one bounded ICGC orthophoto snapshot; keep attribution/provenance.
Reproduction needs Python + Pillow. No Google imagery or runtime tile requests.
"""
import pathlib,urllib.request,urllib.parse,json,datetime,hashlib,io
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parents[1];out=ROOT/'public/aerial';out.mkdir(parents=True,exist_ok=True)
bbox=[2.349,41.515,2.391,41.543];size=4096
service='https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms'
p={'SERVICE':'WMS','VERSION':'1.1.1','REQUEST':'GetMap','LAYERS':'ortofoto_color_vigent','STYLES':'','SRS':'EPSG:4326','BBOX':','.join(map(str,bbox)),'WIDTH':size,'HEIGHT':size,'FORMAT':'image/jpeg'}
url=service+'?'+urllib.parse.urlencode(p)
print('Downloading Cabrils orthophoto',flush=True)
with urllib.request.urlopen(url,timeout=90) as response:
 raw=response.read();assert 'image' in response.headers.get('Content-Type',''),raw[:500]
im=Image.open(io.BytesIO(raw)).convert('RGB');assert im.size==(size,size)
buf=io.BytesIO();im.save(buf,'WEBP',quality=80,method=6);data=buf.getvalue();assert len(data)>10000
(out/'cabrils-ortho.webp').write_bytes(data)
meta={'provider':'Institut Cartogràfic i Geològic de Catalunya (ICGC)','title':'Ortofoto Territorial · Cabrils','layer':'ortofoto_color_vigent','bbox':bbox,'crs':'EPSG:4326','wmsVersion':'1.1.1','width':size,'height':size,'file':'cabrils-ortho.webp','source':url,'product':'https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Imatge/Ortofoto-Territorial','license':'CC-BY-4.0','licenseUrl':'https://creativecommons.org/licenses/by/4.0/','attribution':'Ortofoto © ICGC · CC BY 4.0','downloaded':datetime.datetime.now(datetime.timezone.utc).isoformat(),'flightDate':None,'changes':'Bounded WMS RGB export; re-encoded JPEG to WebP; mapped to approximate 3D terrain and roof footprints. No claim of exact facade or elevation reconstruction.','sha256':hashlib.sha256(data).hexdigest()}
(out/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
print('Saved',len(data),'bytes;',im.size,flush=True)
