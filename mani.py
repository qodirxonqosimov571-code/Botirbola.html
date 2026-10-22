
<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NEON RUNNER</title>
<style>
*{box-sizing:border-box}
body{
 margin:0;background:#070b18;color:white;
 font-family:Arial,sans-serif;text-align:center;
 overflow:hidden;touch-action:manipulation
}
h1{color:#00f7ff;text-shadow:0 0 18px #00f7ff;margin:18px 0 5px}
.info{display:flex;justify-content:center;gap:25px;margin:14px;font-size:17px}
canvas{
 display:block;width:min(94vw,420px);height:auto;
 aspect-ratio:360/500;margin:auto;
 border:2px solid #00f7ff;border-radius:14px;
 background:#101a35;box-shadow:0 0 22px #00f7ff33;
 touch-action:manipulation
}
button{
 background:#00f7ff;color:#06101c;border:0;border-radius:12px;
 padding:13px 25px;font-size:17px;font-weight:bold;margin:12px;
 cursor:pointer
}
p{color:#b7c9e8;font-size:14px}
</style>
</head>
<body>
<h1>⚡ NEON RUNNER</h1>
<p>Tangalarni yig‘ • To‘siqlardan qoch!</p>
<div class="info">
 <span>🪙 <b id="score">0</b></span>
 <span>🏆 <b id="best">0</b></span>
</div>
<canvas id="game" width="360" height="500"></canvas>
<button id="start">▶ O‘YINNI BOSHLASH</button>
<p>⬅ ➡ Harakatlanish: ekranning chap yoki o‘ng tomonini bos.</p>

<script>
const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");
const scoreEl=document.getElementById("score");
const bestEl=document.getElementById("best");
const startBtn=document.getElementById("start");

let player,items,score,best,playing,frame,speed;
best=Number(localStorage.getItem("neonBest")||0);
bestEl.textContent=best;

function reset(){
 player={x:180,y:425,w:30,h:30};
 items=[];score=0;frame=0;speed=3;playing=true;
 scoreEl.textContent=score;
 startBtn.textContent="↻ QAYTA BOSHLASH";
}

function spawn(){
 const coin=Math.random()<0.58;
 items.push({
  x:20+Math.random()*320,y:-25,
  r:coin?10:15,coin,
  color:coin?"#ffd700":"#ff3864"
 });
}

function drawPlayer(){
 ctx.save();
 ctx.shadowBlur=18;ctx.shadowColor="#00f7ff";
 ctx.fillStyle="#00f7ff";
 ctx.fillRect(player.x-player.w/2,player.y-player.h/2,
              player.w,player.h);
 ctx.fillStyle="#ffffff";
 ctx.fillRect(player.x-7,player.y-5,5,5);
 ctx.fillRect(player.x+3,player.y-5,5,5);
 ctx.restore();
}

function drawItem(item){
 ctx.save();
 ctx.shadowBlur=15;ctx.shadowColor=item.color;
 ctx.fillStyle=item.color;
 if(item.coin){
  ctx.beginPath();
  ctx.arc(item.x,item.y,item.r,0,Math.PI*2);
  ctx.fill();
  ctx.fillStyle="#7c5200";
  ctx.font="bold 13px Arial";
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("$",item.x,item.y);
 }else{
  ctx.fillRect(item.x-item.r,item.y-item.r,
               item.r*2,item.r*2);
 }
 ctx.restore();
}

function endGame(){
 playing=false;
 startBtn.textContent="↻ QAYTA O‘YNASH";
}

function update(){
 if(!playing)return;
 frame++;
 if(frame%42===0)spawn();
 speed=3+Math.min(score/12,5);

 ctx.clearRect(0,0,360,500);
 ctx.strokeStyle="#24365b";ctx.lineWidth=1;
 for(let y=(frame*2)%40;y<500;y+=40){
  ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(360,y);ctx.stroke();
 }

 for(let i=items.length-1;i>=0;i--){
  const item=items[i];
  item.y+=speed;
  drawItem(item);
  const hit=Math.abs(item.x-player.x)<item.r+player.w/2-3
         &&Math.abs(item.y-player.y)<item.r+player.h/2-3;

  if(hit){
   if(item.coin){
    score+=1;
    scoreEl.textContent=score;
    if(score>best){
     best=score;bestEl.textContent=best;
     localStorage.setItem("neonBest",best);
    }
    items.splice(i,1);
    continue;
   }else{
    endGame();
   }
  }
  if(item.y>530)items.splice(i,1);
 }

 drawPlayer();

 if(!playing){
  ctx.fillStyle="#000b";
  ctx.fillRect(0,0,360,500);
  ctx.textAlign="center";
  ctx.fillStyle="#ff3864";
  ctx.font="bold 32px Arial";
  ctx.fillText("O‘YIN TUGADI!",180,220);
  ctx.fillStyle="white";
  ctx.font="20px Arial";
  ctx.fillText("Tangalar: "+score,180,260);
  ctx.font="15px Arial";
  ctx.fillText("Qayta boshlash uchun tugmani bosing",180,300);
  return;
 }
 requestAnimationFrame(update);
}

function move(x){
 if(!playing)return;
 player.x=Math.max(18,Math.min(342,x));
}

canvas.addEventListener("pointerdown",e=>{
 const rect=canvas.getBoundingClientRect();
 const x=(e.clientX-rect.left)*360/rect.width;
 move(x);
});

document.addEventListener("keydown",e=>{
 if(e.key==="ArrowLeft"||e.key==="a")move(player.x-28);
 if(e.key==="ArrowRight"||e.key==="d")move(player.x+28);
});

startBtn.addEventListener("click",()=>{
 reset();
 update();
});

ctx.fillStyle="#00f7ff";
ctx.textAlign="center";
ctx.font="bold 22px Arial";
ctx.fillText("TAYYORMISAN?",180,220);
ctx.fillStyle="white";
ctx.font="16px Arial";
ctx.fillText("Boshlash tugmasini bosing!",180,260);
</script>
</body>
</html>
