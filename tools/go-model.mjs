// Only verifies authored teaching positions. This is not a full tournament engine.
export const size=9;
export function empty(){return Array.from({length:size},()=>Array(size).fill(0));}
export function position(black=[],white=[]){
 const b=empty();
 for(const [x,y] of black)b[y][x]=1;
 for(const [x,y] of white){if(b[y][x])throw Error('overlap');b[y][x]=2;}
 return b;
}
export function adjacent(x,y){return [[x-1,y],[x+1,y],[x,y-1],[x,y+1]].filter(([a,b])=>a>=0&&a<size&&b>=0&&b<size);}
export function group(board,x,y){
 const color=board[y][x],stones=[],liberties=new Set(),seen=new Set(),todo=[[x,y]];
 if(!color)return {stones,liberties};
 while(todo.length){
  const [a,b]=todo.pop(),key=a+','+b;
  if(seen.has(key))continue;
  seen.add(key);stones.push([a,b]);
  for(const [c,d] of adjacent(a,b)){
   if(board[d][c]===0)liberties.add(c+','+d);
   else if(board[d][c]===color&&!seen.has(c+','+d))todo.push([c,d]);
  }
 }
 return {stones,liberties};
}
export function move(board,color,x,y,prior=null){
 if(x<0||x>=size||y<0||y>=size||board[y][x])return {legal:false,reason:'occupied'};
 const next=board.map(r=>r.slice());next[y][x]=color;let captured=[];
 for(const [a,b] of adjacent(x,y)){
  if(next[b][a]===3-color){
   const g=group(next,a,b);
   if(!g.liberties.size){captured.push(...g.stones);for(const [c,d] of g.stones)next[d][c]=0;}
  }
 }
 if(!group(next,x,y).liberties.size)return {legal:false,reason:'suicide'};
 if(prior&&JSON.stringify(next)===JSON.stringify(prior))return {legal:false,reason:'ko'};
 return {legal:true,board:next,captured};
}
export function area(board){
 let stones={1:0,2:0},territory={1:0,2:0},neutral=0;const seen=new Set();
 for(let y=0;y<size;y++)for(let x=0;x<size;x++){
  if(board[y][x]){stones[board[y][x]]++;continue;}
  if(seen.has(x+','+y))continue;
  const stack=[[x,y]],region=[],boundary=new Set();
  while(stack.length){
   const [a,b]=stack.pop(),key=a+','+b;if(seen.has(key))continue;
   seen.add(key);region.push([a,b]);
   for(const [c,d] of adjacent(a,b)){
    if(board[d][c])boundary.add(board[d][c]);else if(!seen.has(c+','+d))stack.push([c,d]);
   }
  }
  if(boundary.size===1)territory[[...boundary][0]]+=region.length;else neutral+=region.length;
 }
 return {stones,territory,neutral,black:stones[1]+territory[1],white:stones[2]+territory[2]};
}
export function fixtures(){
 const chain=position([[3,4],[4,4]],[[3,3],[4,3],[2,4]]);
 const capture=position([[4,3],[3,4],[5,4]],[[4,4]]);
 const suicide=position([],[[4,3],[3,4],[5,4],[4,5]]);
 const exception=position([[3,3],[5,3],[4,2]],[[4,3],[3,4],[5,4],[4,5]]);
 const ko=position([[4,3],[3,4],[5,4]],[[4,4],[3,5],[5,5],[4,6]]);
 const eyeBlack=[];
 for(let x=2;x<=6;x++){eyeBlack.push([x,3],[x,5]);}
 eyeBlack.push([2,4],[4,4],[6,4]);
 const eyes=position(eyeBlack,[]);
 const scoring=empty();
 for(let y=0;y<size;y++)for(let x=0;x<size;x++)scoring[y][x]=x<5?1:2;
 for(const [x,y] of [[1,2],[1,6],[7,2],[7,6]])scoring[y][x]=0;
 return {chain,capture,suicide,exception,ko,eyes,scoring};
}
