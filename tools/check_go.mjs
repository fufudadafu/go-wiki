import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {position,group,move,area,fixtures} from './go-model.mjs';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
let checked=0;
function check(name,fn){fn();checked++;console.log('PASS '+name);}
const f=fixtures();
check('單子中央、邊、角的氣',()=>{
 assert.equal(group(position([[4,4]]),4,4).liberties.size,4);
 assert.equal(group(position([[0,4]]),0,4).liberties.size,3);
 assert.equal(group(position([[0,0]]),0,0).liberties.size,2);
});
check('斜向不連接，棋塊共用氣去重',()=>{
 assert.equal(group(position([[3,3],[4,4]]),3,3).stones.length,1);
 const shared=position([[3,3],[4,3],[3,4]]);
 assert.equal(group(shared,3,3).liberties.size,7);
});
check('練習一唯一答案為三口氣',()=>{
 assert.equal(group(f.chain,3,4).liberties.size,3);
});
check('練習二 A 點提走中央白子',()=>{
 const g=group(f.capture,4,4);assert.equal(g.liberties.size,1);
 assert(g.liberties.has('4,5'));
 const r=move(f.capture,1,4,5);assert(r.legal);assert.deepEqual(r.captured,[[4,4]]);assert.equal(r.board[4][4],0);
});
check('自殺禁止，提子例外必須先處理',()=>{
 assert.equal(move(f.suicide,1,4,4).reason,'suicide');
 const r=move(f.exception,1,4,4);assert(r.legal);assert.deepEqual(r.captured,[[4,3]]);
 assert.equal(group(r.board,4,4).liberties.size,1);
});
check('簡單劫立即提回會還原盤面',()=>{
 const r=move(f.ko,1,4,5);assert(r.legal);assert.equal(r.captured.length,1);
 assert.equal(move(r.board,2,4,4,f.ko).reason,'ko');
 assert.deepEqual(move(r.board,2,4,4).board,f.ko);
});
check('兩眼示意確實同一棋塊且兩眼不可直接落白',()=>{
 assert.equal(group(f.eyes,2,3).stones.length,13);
 assert.equal(move(f.eyes,2,3,4).reason,'suicide');
 assert.equal(move(f.eyes,2,5,4).reason,'suicide');
});
check('終局面積、貼目及總交叉點數',()=>{
 const s=area(f.scoring);assert.deepEqual(s.stones,{1:43,2:34});
 assert.deepEqual(s.territory,{1:2,2:2});assert.equal(s.neutral,0);
 assert.equal(s.black,45);assert.equal(s.white,36);
 assert.equal(s.black-s.white-6.5,2.5);
 assert.equal(s.black+s.white+s.neutral,81);
});
check('全部示意盤的棋塊均有氣，無重疊棋子',()=>{
 for(const b of Object.values(f))for(let y=0;y<9;y++)for(let x=0;x<9;x++)
  if(b[y][x])assert(group(b,x,y).liberties.size>0);
});
check('五篇來源與九篇概念均可追溯',()=>{
 const d=JSON.parse(fs.readFileSync(path.join(root,'content.json'),'utf8'));
 assert.equal(d.sources.length,5);assert.equal(d.pages.length,9);
 for(const p of d.pages){assert(p.refs.length);for(const id of p.refs)assert(d.sources.some(s=>s.id===id));}
 for(const s of d.sources)assert(fs.existsSync(path.join(root,'raw',s.id+'.json')));
});
check('Markdown 內部連結有效',()=>{
 function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]);}
 for(const file of walk(path.join(root,'wiki')).filter(f=>f.endsWith('.md'))){
  for(const m of fs.readFileSync(file,'utf8').matchAll(/\]\(([^)]+)\)/g)){
   if(/^https?:/.test(m[1])||m[1].startsWith('#'))continue;
   assert(fs.existsSync(path.resolve(path.dirname(file),m[1])),file+' '+m[1]);
  }
 }
});
const result={checked_at:new Date().toISOString(),passed:checked,failed:0,
 scope:'教學盤面、練習答案、簡單劫、面積計分與內部來源連結；非完整比賽規則引擎',
 browser_qa:'本環境沒有可用瀏覽器控制工具，未做視覺及真實點擊測試'};
fs.writeFileSync(path.join(root,'reports','validation.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));
