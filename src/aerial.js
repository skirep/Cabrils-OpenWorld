import * as THREE from 'three';
import {heightAt} from './geo.js';

// OSM uses the same local equirectangular projection. WMS 1.1.1 EPSG:4326
// uses longitude,latitude order; V=1 is north on a TextureLoader image.
export function projectLonLat(lon,lat,origin=[2.369,41.527]){
  return [(lon-origin[0])*111320*Math.cos(origin[1]*Math.PI/180),-(lat-origin[1])*111320];
}
export function aerialBounds(bbox,origin){const [west,south,east,north]=bbox;const [minX,maxZ]=projectLonLat(west,south,origin),[maxX,minZ]=projectLonLat(east,north,origin);return {minX,minZ,maxX,maxZ};}
export function aerialUV(x,z,b){return [(x-b.minX)/(b.maxX-b.minX),1-(z-b.minZ)/(b.maxZ-b.minZ)];}
export async function loadAerial(renderer,origin){
  const r=await fetch(import.meta.env.BASE_URL+'aerial/manifest.json');if(!r.ok)throw Error('No es troba la informació de l’ortofoto');
  const metadata=await r.json(),texture=await new THREE.TextureLoader().loadAsync(import.meta.env.BASE_URL+'aerial/'+metadata.file);
  // Bound GPU allocation on devices with smaller texture limits.
  const max=Math.min(4096,renderer.capabilities.maxTextureSize);
  if(texture.image.width>max){const c=document.createElement('canvas');c.width=c.height=max;c.getContext('2d').drawImage(texture.image,0,0,max,max);texture.image=c;texture.needsUpdate=true;}
  texture.colorSpace=THREE.SRGBColorSpace;texture.wrapS=texture.wrapT=THREE.ClampToEdgeWrapping;texture.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
  return {metadata,bounds:aerialBounds(metadata.bbox,origin),texture,roof:new THREE.MeshStandardMaterial({map:texture,roughness:.95,side:THREE.DoubleSide})};
}
export function createAerialTerrain(scene,aerial){const b=aerial.bounds,width=b.maxX-b.minX,depth=b.maxZ-b.minZ;
  const g=new THREE.PlaneGeometry(width,depth,80,80);g.rotateX(-Math.PI/2);g.translate((b.minX+b.maxX)/2,0,(b.minZ+b.maxZ)/2);
  const p=g.attributes.position,uv=g.attributes.uv;for(let i=0;i<p.count;i++){const x=p.getX(i),z=p.getZ(i),q=aerialUV(x,z,b);p.setY(i,heightAt(x,z)-.12);uv.setXY(i,...q);}g.computeVertexNormals();
  const mesh=new THREE.Mesh(g,new THREE.MeshStandardMaterial({map:aerial.texture,roughness:1,side:THREE.DoubleSide}));mesh.receiveShadow=true;scene.add(mesh);return mesh;
}
