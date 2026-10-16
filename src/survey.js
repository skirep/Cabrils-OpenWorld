import * as THREE from 'three';
import {setTerrain} from './terrain.js';
import {aerialUV} from './aerial.js';
export async function readGzipAsset(path){const response=await fetch(import.meta.env.BASE_URL+path);if(!response.ok)throw Error('No es troba '+path);return new Response(response.body.pipeThrough(new DecompressionStream('gzip'))).json();}
export async function loadSurvey(map){const [terrain,survey]=await Promise.all([readGzipAsset('data/terrain.json.gz'),readGzipAsset('data/survey-buildings.json.gz')]);if(survey.origin.some((n,i)=>Math.abs(n-map.origin[i])>1e-8))throw Error('Origen cartogràfic incompatible');setTerrain(terrain);map.buildings=survey.buildings;map.survey=survey;map.terrain=terrain;
// Short segments conform roads and curbs to the measured hills, not endpoint chords.
for(const road of map.roads){const points=[road.points[0]];for(let i=1;i<road.points.length;i++){const a=road.points[i-1],b=road.points[i],count=Math.max(1,Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1])/6));for(let j=1;j<=count;j++)points.push([a[0]+(b[0]-a[0])*j/count,a[1]+(b[1]-a[1])*j/count]);}road.points=points;}
return survey;}
export function createSurveyMeshes(scene,buildings,mats,aerial){
 const cells=new Map(),photoRoofs=[];
 const facade=mats.plaster.clone();facade.color.setHex(0xf5f0e6);facade.side=THREE.DoubleSide;
 function batch(key,material){if(!cells.has(key))cells.set(key,{positions:[],uvs:[],material});return cells.get(key);}
 for(const b of buildings){const v=b.vertices,indices=b.faces,center=b.points.reduce((p,q)=>[p[0]+q[0]/b.points.length,p[1]+q[1]/b.points.length],[0,0]),cell=`${Math.floor(center[0]/180)},${Math.floor(center[1]/180)}`;
  for(let f=0;f<indices.length;f+=3){const points=indices.slice(f,f+3).map(i=>new THREE.Vector3(...v.slice(i*3,i*3+3))),normal=new THREE.Vector3().subVectors(points[1],points[0]).cross(new THREE.Vector3().subVectors(points[2],points[0]));if(normal.lengthSq()<1e-10)continue;normal.normalize();
   if(normal.y<-.7)continue; // Bottom caps are underground, never photographic roof surfaces.
   const roof=normal.y>.35,photo=roof&&aerial&&points.every(p=>p.x>=aerial.bounds.minX&&p.x<=aerial.bounds.maxX&&p.z>=aerial.bounds.minZ&&p.z<=aerial.bounds.maxZ),key=(photo?'photo':roof?'roof':'wall')+cell,batchData=batch(key,photo?aerial.roof:roof?mats.roof:facade);
   for(const p of points){batchData.positions.push(p.x,p.y,p.z);batchData.uvs.push(...(photo?aerialUV(p.x,p.z,aerial.bounds):roof?[p.x/2.5,p.z/2.5]:[Math.abs(normal.x)>.6?p.z/3:p.x/3,p.y/3]));}
  }
 }
 for(const [key,b] of cells){const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(b.positions,3));geometry.setAttribute('uv',new THREE.Float32BufferAttribute(b.uvs,2));geometry.computeVertexNormals();geometry.computeBoundingSphere();const mesh=new THREE.Mesh(geometry,b.material);mesh.castShadow=true;mesh.receiveShadow=true;mesh.userData.surveyed=true;scene.add(mesh);if(key.startsWith('photo')){const photo=geometry.attributes.uv,material=photo.clone(),p=geometry.attributes.position;for(let i=0;i<p.count;i++)material.setXY(i,p.getX(i)/2.5,p.getZ(i)/2.5);photoRoofs.push({mesh,photo,material});}}
 return {setAerial(enabled){for(const r of photoRoofs){r.mesh.material=enabled?aerial.roof:mats.roof;r.mesh.geometry.setAttribute('uv',enabled?r.photo:r.material);}}};
}
