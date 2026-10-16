import {test} from 'node:test';import assert from 'node:assert/strict';
import {projectLonLat,aerialBounds,aerialUV,createAerialTerrain} from '../src/aerial.js';
import * as THREE from 'three';
const bbox=[2.349,41.515,2.391,41.543],origin=[2.369,41.527];
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-6,`${a} != ${b}`);
test('orthophoto shares the local OSM coordinate projection and longitude/latitude axis order',()=>{const p=projectLonLat(...origin,origin);close(p[0],0);close(p[1],0);const b=aerialBounds(bbox,origin);assert.ok(b.minX<0&&b.maxX>0&&b.minZ<0&&b.maxZ>0);assert.ok(b.maxX-b.minX>3400&&b.maxX-b.minX<3600);assert.ok(b.maxZ-b.minZ>3100&&b.maxZ-b.minZ<3200);});
test('north is V=1, south is V=0, and corners are not mirrored or tiled',()=>{const b=aerialBounds(bbox,origin);for(const [x,z,u,v] of [[b.minX,b.minZ,0,1],[b.maxX,b.minZ,1,1],[b.minX,b.maxZ,0,0],[b.maxX,b.maxZ,1,0]]){const q=aerialUV(x,z,b);close(q[0],u);close(q[1],v);}});
test('aerial terrain has georeferenced continuous finite UVs',()=>{const scene=new THREE.Scene(),bounds=aerialBounds(bbox,origin),mesh=createAerialTerrain(scene,{bounds,texture:new THREE.Texture()});const uv=mesh.geometry.attributes.uv,p=mesh.geometry.attributes.position;assert.equal(scene.children.length,1);for(let i=0;i<uv.count;i++){assert.ok(Number.isFinite(p.getY(i)));const q=aerialUV(p.getX(i),p.getZ(i),bounds);assert.ok(Math.abs(uv.getX(i)-q[0])<1e-6);assert.ok(Math.abs(uv.getY(i)-q[1])<1e-6);}mesh.geometry.dispose();mesh.material.dispose();});
