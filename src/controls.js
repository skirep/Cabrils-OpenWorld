// Standard Gamepad mapping plus two independent multi-touch sticks.
export function deadzone(x=0,y=0,threshold=.16){
  if(!Number.isFinite(x)||!Number.isFinite(y))return {x:0,y:0};
  const length=Math.hypot(x,y);if(length<=threshold)return {x:0,y:0};
  const amount=Math.min(1,(length-threshold)/(1-threshold));return {x:x/length*amount,y:y/length*amount};
}
export function readGamepad(pad){
  if(!pad?.connected||pad.mapping!=='standard')return null;
  const value=i=>Math.max(0,Math.min(1,pad.buttons[i]?.value||0));
  return {left:deadzone(pad.axes[0],pad.axes[1]),right:deadzone(pad.axes[2],pad.axes[3]),accelerate:value(7),reverse:value(6),run:value(0)>.5,brake:value(1)>.5,interact:value(3)>.5,map:value(8)>.5,pause:value(9)>.5,camera:value(2)>.5,route:value(5)>.5,recover:value(4)>.5};
}
export class Controls{
  constructor(actions){this.actions=actions;this.left={x:0,y:0};this.right={x:0,y:0};this.previous={};this.resets=[];this.pad=null;this.bindStick('moveStick','left');this.bindStick('lookStick','right');}
  bindStick(id,key){const el=document.getElementById(id),knob=el.querySelector('.stick-knob');let pointer=null;
    const reset=()=>{pointer=null;this[key]={x:0,y:0};knob.style.transform='translate(0px,0px)';el.classList.remove('active');};this.resets.push(reset);
    const update=e=>{const r=el.getBoundingClientRect(),radius=r.width*.34,x=(e.clientX-r.left-r.width/2)/radius,y=(e.clientY-r.top-r.height/2)/radius,length=Math.max(1,Math.hypot(x,y));this[key]=deadzone(x/length,y/length,.08);knob.style.transform=`translate(${x/length*radius}px,${y/length*radius}px)`;};
    el.addEventListener('pointerdown',e=>{if(pointer!==null||!this.actions.active())return;e.preventDefault();pointer=e.pointerId;el.setPointerCapture(pointer);el.classList.add('active');update(e);});
    el.addEventListener('pointermove',e=>{if(e.pointerId===pointer){e.preventDefault();update(e);}});
    for(const name of ['pointerup','pointercancel','lostpointercapture'])el.addEventListener(name,e=>{if(e.pointerId===pointer)reset();});
  }
  reset(){this.resets.forEach(fn=>fn());}
  poll(){const pads=Array.from(navigator.getGamepads?.()||[]);this.pad=pads.find(p=>p?.connected&&p.mapping==='standard')||null;const state=readGamepad(this.pad);for(const action of ['interact','pause','map','camera','run','route','recover']){const pressed=!!state?.[action];if(pressed&&!this.previous[action])(action==='run'?this.actions.start:this.actions[action])?.();this.previous[action]=pressed;}return state;}
  sample(pad){const strongest=(a,b)=>Math.abs(a)>Math.abs(b||0)?a:(b||0);return {x:strongest(this.left.x,pad?.left.x),y:strongest(this.left.y,pad?.left.y),lookX:strongest(this.right.x,pad?.right.x),lookY:strongest(this.right.y,pad?.right.y),accelerate:pad?.accelerate||0,reverse:pad?.reverse||0,run:pad?.run||false,brake:pad?.brake||false};}
}
