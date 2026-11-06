import asyncio,base64,sys
from playwright.async_api import async_playwright
JS=r"""
([S,scale,ring])=>{const c=document.createElement('canvas');c.width=c.height=S;const x=c.getContext('2d');const k=S/1024;x.scale(k,k);
let g=x.createRadialGradient(512,512,60,512,512,760);g.addColorStop(0,'#1a2a46');g.addColorStop(.55,'#0c1526');g.addColorStop(1,'#050911');
x.fillStyle=g;x.fillRect(0,0,1024,1024);
x.fillStyle='rgba(150,180,220,.10)';for(let i=32;i<1024;i+=64)for(let j=32;j<1024;j+=64){x.beginPath();x.arc(i,j,4,0,7);x.fill()}
x.save();x.translate(512,512);x.scale(scale,scale);x.translate(-512,-512);
const T=[['#ff5a4e',[[-40,650],[262,650],[262,512],[512,512]]],
         ['#b46cff',[[374,-40],[374,262],[512,262],[512,512]]],
         ['#3fa9ff',[[1064,374],[762,374],[762,512],[512,512]]],
         ['#3ddc84',[[650,1064],[650,762],[512,762],[512,512]]]];
x.lineCap='round';x.lineJoin='round';
const path=p=>{x.beginPath();x.moveTo(...p[0]);for(const q of p.slice(1))x.lineTo(...q)};
for(const [col,p] of T){path(p);x.save();x.translate(0,10);x.lineWidth=100;x.strokeStyle='rgba(0,0,0,.4)';x.stroke();x.restore()}
for(const [col,p] of T){path(p);x.lineWidth=90;x.strokeStyle='#c99a62';x.stroke()}
for(const [col,p] of T){x.save();x.shadowColor=col;x.shadowBlur=70;path(p);x.lineWidth=56;x.strokeStyle=col;x.stroke();x.restore();
  path(p);x.lineWidth=56;x.strokeStyle=col;x.stroke();
  path(p);x.setLineDash([24,44]);x.lineDashOffset=10;x.lineWidth=16;x.strokeStyle='rgba(255,255,255,.88)';x.stroke();x.setLineDash([])}
// solder pads on the elbows
for(const [col,p] of T){const [a,b]=p[1];x.beginPath();x.arc(a,b,52,0,7);x.fillStyle='#ffd9b0';x.fill();x.beginPath();x.arc(a,b,21,0,7);x.fillStyle='#0c1526';x.fill()}
// bulb: warm halo, machined bezel, white-hot lens with a rainbow rim (all colours together make white)
const R=218;g=x.createRadialGradient(512,512,R*.5,512,512,R*2.1);g.addColorStop(0,'rgba(255,240,215,.8)');g.addColorStop(.45,'rgba(255,200,150,.2)');g.addColorStop(1,'rgba(255,180,120,0)');
x.fillStyle=g;x.beginPath();x.arc(512,512,R*2.1,0,7);x.fill();
x.save();x.shadowColor='rgba(0,0,0,.6)';x.shadowBlur=50;x.shadowOffsetY=16;x.beginPath();x.arc(512,512,R,0,7);x.fillStyle='#2a3036';x.fill();x.restore();
let m=x.createLinearGradient(0,512-R,0,512+R);m.addColorStop(0,'#f6f8fa');m.addColorStop(.45,'#aab3bb');m.addColorStop(1,'#4f5860');x.beginPath();x.arc(512,512,R,0,7);x.fillStyle=m;x.fill();
x.beginPath();x.arc(512,512,R*.87,0,7);x.fillStyle='#1d242b';x.fill();
const cg=x.createConicGradient(-Math.PI*.75,512,512);[['#ff5a4e',0],['#b46cff',.25],['#3fa9ff',.5],['#3ddc84',.75],['#ff5a4e',1]].forEach(([c,o])=>cg.addColorStop(o,c));
x.beginPath();x.arc(512,512,R*.8,0,7);x.fillStyle=cg;x.fill();
g=x.createRadialGradient(512,512,0,512,512,R*.8);g.addColorStop(0,'#ffffff');g.addColorStop(.36,'rgba(255,252,242,.96)');g.addColorStop(.66,'rgba(255,246,230,.35)');g.addColorStop(.9,'rgba(255,240,220,0)');
x.beginPath();x.arc(512,512,R*.8,0,7);x.fillStyle=g;x.fill();
const q=x.createRadialGradient(512-R*.3,512-R*.36,R*.03,512,512,R*.8);q.addColorStop(0,'rgba(255,255,255,.7)');q.addColorStop(.35,'rgba(255,255,255,.05)');q.addColorStop(1,'rgba(0,0,0,.12)');
x.beginPath();x.arc(512,512,R*.8,0,7);x.fillStyle=q;x.fill();
x.beginPath();x.ellipse(512-R*.28,512-R*.38,R*.22,R*.11,-.5,0,7);x.fillStyle='rgba(255,255,255,.75)';x.fill();
x.restore();
if(ring){x.lineWidth=0}
return c.toDataURL('image/png').split(',')[1]}
"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page();await pg.set_content('<body></body>')
        for name,S,sc in [('icon-1024.png',1024,1),('icon-maskable-1024.png',1024,.8),('pfp-1080.png',1080,.92)]:
            open(name,'wb').write(base64.b64decode(await pg.evaluate(JS,[S,sc,0])))
        await b.close()
asyncio.run(main())
