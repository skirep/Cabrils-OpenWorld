"""Download and simplify real OpenStreetMap geometry. No invented fallback."""
import urllib.request, xml.etree.ElementTree as ET, json, math, pathlib, datetime, gzip
ROOT=pathlib.Path(__file__).resolve().parents[1]
BBOX=(2.349,41.515,2.391,41.543)
url='https://www.openstreetmap.org/api/0.6/map?bbox='+','.join(map(str,BBOX))
print('Downloading',url,flush=True)
raw=urllib.request.urlopen(url,timeout=90).read()
root=ET.fromstring(raw)
nodes={n.attrib['id']:(float(n.attrib['lon']),float(n.attrib['lat'])) for n in root.findall('node')}
origin=[2.369,41.527]
def point(p): return [round((p[0]-origin[0])*111320*math.cos(math.radians(origin[1])),2),round(-(p[1]-origin[1])*111320,2)]
roads=[]; buildings=[]; areas=[]; pois=[]
for w in root.findall('way'):
 tags={t.attrib['k']:t.attrib['v'] for t in w.findall('tag')}
 pts=[point(nodes[n.attrib['ref']]) for n in w.findall('nd') if n.attrib['ref'] in nodes]
 if len(pts)<2: continue
 if 'highway' in tags and tags['highway'] not in ['steps','construction','proposed']:
  roads.append({'id':w.attrib['id'],'name':tags.get('name',''),'kind':tags['highway'],'points':pts,'oneway':tags.get('oneway')=='yes'})
 if 'building' in tags and len(pts)>3 and pts[0]==pts[-1]:
  try: height=float(tags.get('height',float(tags.get('building:levels',2))*3.1))
  except: height=6.2
  buildings.append({'points':pts,'height':max(3,min(height,35)),'kind':tags['building'],'name':tags.get('name','')})
 if len(pts)>3 and pts[0]==pts[-1] and (tags.get('landuse') in ['forest','grass','meadow','vineyard','orchard'] or tags.get('natural') in ['wood','water'] or tags.get('leisure') in ['park','pitch','swimming_pool']):
  areas.append({'points':pts,'kind':tags.get('natural',tags.get('leisure',tags.get('landuse')))})
for n in root.findall('node'):
 tags={t.attrib['k']:t.attrib['v'] for t in n.findall('tag')}
 if tags.get('name') and (tags.get('amenity') or tags.get('tourism')):
  pois.append({'name':tags['name'],'point':point(nodes[n.attrib['id']]),'kind':tags.get('amenity',tags.get('tourism'))})
data={'origin':origin,'bbox':BBOX,'downloaded':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':url,'attribution':'© OpenStreetMap contributors · ODbL 1.0','roads':roads,'buildings':buildings,'areas':areas,'pois':pois}
out=ROOT/'public/data/cabrils.json.gz'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_bytes(gzip.compress(json.dumps(data,separators=(',',':'),ensure_ascii=False).encode(),compresslevel=9,mtime=0))
print({k:len(data[k]) for k in ['roads','buildings','areas','pois']})
