"""Prepare a bounded ICGC 2024 IFC building snapshot and real MET5 terrain.
Dependencies: pip install ifcopenshell pyproj shapely numpy
python scripts/import_survey.py --cache /tmp/cabrils-ifc --dem /tmp/cabrils-dem2
IFC files: ICGC RTT, six 1:5000 sheets, CC BY 4.0. Never synthesize buildings.
"""
import argparse,pathlib,json,gzip,hashlib,datetime,math,collections
import numpy as np
from pyproj import Transformer
import ifcopenshell,ifcopenshell.geom
from shapely.geometry import Polygon,box
from shapely.ops import unary_union
ROOT=pathlib.Path(__file__).resolve().parents[1]
ORIGIN=[2.369,41.527];BBOX=[2.349,41.515,2.391,41.543]
TO_LONLAT=Transformer.from_crs(25831,4326,always_xy=True)
TO_UTM=Transformer.from_crs(4326,25831,always_xy=True)
SCALE=111320*math.cos(math.radians(ORIGIN[1]))
def local(lon,lat):return ((lon-ORIGIN[0])*SCALE,-(lat-ORIGIN[1])*111320)
def encode(path,value):
 raw=json.dumps(value,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode();path.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--cache',type=pathlib.Path,required=True);parser.add_argument('--dem',type=pathlib.Path,required=True);args=parser.parse_args();out=ROOT/'public/data';out.mkdir(exist_ok=True)
 # WCS ArcGrid records row 0 at north; resample in the exact game projection.
 lines=args.dem.read_text().splitlines();header={k.lower():float(v) for k,v in (l.split() for l in lines[:6])};raw=np.loadtxt(lines[6:]);ncol,nrow=int(header['ncols']),int(header['nrows']);assert raw.shape==(nrow,ncol)
 xmin=header['xllcorner']+header['cellsize']/2;ymax=header['yllcorner']+(nrow-.5)*header['cellsize'];step=header['cellsize']
 def elevation(e,n):
  x=np.clip((e-xmin)/step,0,ncol-1);y=np.clip((ymax-n)/step,0,nrow-1);i=np.floor(x).astype(int);j=np.floor(y).astype(int);u=x-i;v=y-j
  return raw[j,i]*(1-u)*(1-v)+raw[j,np.minimum(i+1,ncol-1)]*u*(1-v)+raw[np.minimum(j+1,nrow-1),i]*(1-u)*v+raw[np.minimum(j+1,nrow-1),np.minimum(i+1,ncol-1)]*u*v
 offset=round(float(elevation(*TO_UTM.transform(*ORIGIN))),2)
 minx,minz=-2300,-2400;maxx,maxz=2400,2100;spacing=10;cols=int((maxx-minx)/spacing)+1;rows=int((maxz-minz)/spacing)+1
 xx,zz=np.meshgrid(np.arange(cols)*spacing+minx,np.arange(rows)*spacing+minz);ee,nn=TO_UTM.transform(xx/SCALE+ORIGIN[0],ORIGIN[1]-zz/111320);grid=elevation(ee,nn)-offset
 assert np.isfinite(grid).all() and grid.min()>-500 and grid.max()<1500
 terrain={'origin':ORIGIN,'bounds':[minx,minz,maxx,maxz],'cols':cols,'rows':rows,'spacing':spacing,'verticalOffset':offset,'source':'ICGC MET5 via WCS; 5 m source model exported at 10 m sampling','data':np.round(grid,2).ravel().tolist()}
 terrainhash=encode(out/'terrain.json.gz',terrain);print('TERRAIN',grid.shape,'absolute altitudes',round(float(grid.min()+offset),1),round(float(grid.max()+offset),1),flush=True)
 settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
 region=box(*BBOX);buildings=[];seen=set();sources=[];kinds=collections.Counter();errors=[]
 for tile in ['293118','293119','293120','294118','294119','294120']:
  p=args.cache/f'topografia-territorial-v1r0-full{tile}-2024.ifc';assert p.exists(),p
  sources.append({'tile':tile,'url':'https://datacloud.icgc.cat/datacloud/topografia-territorial/ifc/'+p.name.replace('.ifc','.zip'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
  f=ifcopenshell.open(str(p));count=0
  for e in f.by_type('IfcBuildingElementProxy'):
   if e.Name not in {'edi','ind','hiv','dip','esm','esg','tor','cas'}:continue
   try:
    geom=ifcopenshell.geom.create_shape(settings,e);verts=np.array(geom.geometry.verts).reshape(-1,3);faces=np.array(geom.geometry.faces).reshape(-1,3)
    if len(faces)==0:continue
    lons,lats=TO_LONLAT.transform(verts[:,0],verts[:,1]);geo=box(float(min(lons)),float(min(lats)),float(max(lons)),float(max(lats)))
    if not region.intersects(geo):continue
    xs=(lons-ORIGIN[0])*SCALE;zs=-(lats-ORIGIN[1])*111320;ys=verts[:,2]-offset;v=np.round(np.column_stack([xs,ys,zs]),2)
    # Horizontal projection of nonvertical faces gives all solid footprints,
    # preserving separate components and courtyard rings. No convex hull.
    triangles=[]
    for face in faces:
     tri=Polygon([(v[i,0],v[i,2]) for i in face])
     if tri.area>.001:triangles.append(tri)
    foot=unary_union(triangles);parts=[foot] if foot.geom_type=='Polygon' else list(foot.geoms)
    digest=hashlib.sha256(np.array(sorted(map(tuple,v.tolist()))).tobytes()).hexdigest()
    if digest in seen:continue
    seen.add(digest)
    rings=[{'points':np.round(p.exterior.coords,2).tolist(),'holes':[np.round(h.coords,2).tolist() for h in p.interiors]} for p in parts if p.area>.5]
    if not rings:continue
    buildings.append({'id':e.GlobalId,'kind':e.Name,'name':'','tile':tile,'source':'ICGC RTT 2024','height':round(float(ys.max()-ys.min()),2),'base':round(float(ys.min()),2),'points':rings[0]['points'],'holes':rings[0]['holes'],'footprints':rings,'vertices':v.ravel().tolist(),'faces':faces.ravel().tolist()})
    count+=1;kinds[e.Name]+=1
   except Exception as ex:errors.append({'tile':tile,'id':e.GlobalId,'error':str(ex)[:160]})
  print('IFC',tile,count,'buildings; total',len(buildings),flush=True);del f
 assert len(buildings)>2000,(len(buildings),errors[:5])
 payload={'origin':ORIGIN,'bbox':BBOX,'year':2024,'provider':'Institut Cartogràfic i Geològic de Catalunya','license':'CC-BY-4.0','buildings':buildings}
 buildhash=encode(out/'survey-buildings.json.gz',payload)
 manifest={'product':'ICGC Referencial Topogràfic Territorial 2024, IFC 3D','license':'CC-BY-4.0','licenseUrl':'https://creativecommons.org/licenses/by/4.0/','attribution':'Edificis i elevacions © ICGC, CC BY 4.0 (adaptats)','prepared':datetime.datetime.now(datetime.timezone.utc).isoformat(),'origin':ORIGIN,'bbox':BBOX,'buildings':len(buildings),'kinds':dict(kinds),'sources':sources,'terrain':{'request':'https://geoserveis.icgc.cat/icc_mdt/wcs/service?SERVICE=WCS&VERSION=1.0.0&REQUEST=GetCoverage&COVERAGE=met&CRS=EPSG:25831&BBOX=445088,4595361,449878,4599990&RESX=10&RESY=10&FORMAT=ARCGRID','samplingMeters':10,'verticalOffset':offset,'sha256':terrainhash},'buildingSha256':buildhash,'skippedErrors':errors,'limitations':'Official 1:5000 surveyed volumes, not facade photogrammetry. Roof geometry retained from IFC, which includes flat extrusions; no invented pitched roofs. Snapshot 2024, not a claim of present-day centimetre accuracy. Facade materials are illustrative.'}
 (out/'survey-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print('DONE',len(buildings),'errors',len(errors),flush=True)
if __name__=='__main__':main()
