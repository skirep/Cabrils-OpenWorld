import * as THREE from 'three';

// Assets are bundled locally: no third-party requests or runtime hotlinking.
export async function loadVillageMaterials(renderer){
  const loader=new THREE.TextureLoader(),anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
  const load=async(name,color=false)=>{const t=await loader.loadAsync(import.meta.env.BASE_URL+'textures/'+name+'.webp');t.wrapS=t.wrapT=THREE.RepeatWrapping;t.anisotropy=anisotropy;if(color)t.colorSpace=THREE.SRGBColorSpace;return t;};
  const pairs=await Promise.all(['plaster','roof','stone','asphalt','cobble','soil','pavement'].map(async key=>[key,await Promise.all([load(key+'-diff',true),load(key+'-normal')])]));
  const maps=Object.fromEntries(pairs);
  const make=(key,roughness,strength=.4)=>new THREE.MeshStandardMaterial({map:maps[key][0].clone(),normalMap:maps[key][1].clone(),normalScale:new THREE.Vector2(strength,strength),roughness,side:THREE.DoubleSide});
  const facadeMaps=await Promise.all([0,1,2].map(i=>load('facade-'+i,true)));
  const facades=facadeMaps.map(map=>new THREE.MeshStandardMaterial({map,normalMap:maps.plaster[1],normalScale:new THREE.Vector2(.16,.16),roughness:.94,side:THREE.DoubleSide}));
  return {road:make('asphalt',.95,.35),grass:make('soil',1,.35),wall:facades[0],facades,
    roof:make('roof',.89,.75),stone:make('stone',.96,.6),paving:make('cobble',.97,.5),
    pavement:make('pavement',.95,.3),dirt:make('soil',1,.4),
    line:new THREE.MeshStandardMaterial({color:0xd4cfb9,roughness:1,side:THREE.DoubleSide})};
}
