let terrain=null;
export function setTerrain(grid){
  if(!grid||grid.cols<2||grid.rows<2||grid.data.length!==grid.cols*grid.rows||grid.data.some(v=>!Number.isFinite(v)))throw Error('Model d’elevacions invàlid');
  terrain=grid;
}
export function terrainHeight(x,z,grid=terrain){
  if(!grid)return 0;
  const [west,north,east,south]=grid.bounds;
  const u=Math.max(0,Math.min(grid.cols-1,(x-west)/(east-west)*(grid.cols-1))),v=Math.max(0,Math.min(grid.rows-1,(z-north)/(south-north)*(grid.rows-1)));
  const i=Math.min(grid.cols-2,Math.floor(u)),j=Math.min(grid.rows-2,Math.floor(v)),a=u-i,b=v-j,k=j*grid.cols+i,d=grid.data;
  return d[k]*(1-a)*(1-b)+d[k+1]*a*(1-b)+d[k+grid.cols]*(1-a)*b+d[k+grid.cols+1]*a*b;
}
