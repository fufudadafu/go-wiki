import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const html=fs.readFileSync(path.join(root,'dist/index.html'),'utf8');
const dataText=html.match(/<script id="content-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const code=html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
new vm.Script(code);
assert(!/<script[^>]+src=/.test(html));
assert(!/<link[^>]+rel=["']stylesheet/.test(html));
assert(!/https?:\/\/[^"']+\.(?:js|css)["']/.test(html));
const elements=new Map(),listeners={document:{},window:{}};
function el(id){
 if(!elements.has(id))elements.set(id,{id,innerHTML:'',textContent:'',value:'',style:{},hidden:false,disabled:false,attrs:{},
  addEventListener(name,fn){this[name]=fn;},setAttribute(k,v){this.attrs[k]=v;}});
 return elements.get(id);
}
el('content-data').textContent=dataText;
const document={
 getElementById:el,querySelectorAll(){return [];},
 addEventListener(name,fn){listeners.document[name]=fn;},
 createElement(){return {click(){}};},documentElement:{outerHTML:html}
};
const location={hash:'#lesson/0'};
const sandbox={document,location,console,Blob,URL,setTimeout,window:{addEventListener(name,fn){listeners.window[name]=fn;},scrollTo(){}}};
vm.createContext(sandbox);vm.runInContext(code,sandbox);
let rendered=0;
for(let i=0;i<16;i++){
 location.hash='#lesson/'+i;listeners.window.hashchange();
 const out=el('slide-content').innerHTML;
 assert(out.includes('<h1'),String(i));assert(!out.includes('undefined'),String(i));
 assert.equal(el('slidejump').value,i);
 assert.equal(el('previous').disabled,i===0);assert.equal(el('next').disabled,i===15);
 rendered++;
}
function clickAction(name){
 listeners.document.click({target:{closest(selector){return selector==='[data-action]'?{dataset:{action:name}}:null;}}});
}
for(const [i,action] of [[3,'liberty'],[5,'capture'],[6,'legal'],[7,'ko'],[10,'score']]){
 location.hash='#lesson/'+i;listeners.window.hashchange();
 const before=el('slide-content').innerHTML;clickAction(action);
 assert.notEqual(el('slide-content').innerHTML,before,action);
}
for(const [i,q,a] of [[11,1,1],[12,2,0],[13,3,0]]){
 location.hash='#lesson/'+i;listeners.window.hashchange();
 listeners.document.click({target:{closest(s){return s==='[data-answer]'?{dataset:{answer:q+':'+a}}:null;}}});
 assert(el('slide-content').innerHTML.includes('答對了'),String(q));
}
const data=JSON.parse(dataText);
for(const p of data.wiki){
 location.hash='#wiki/'+p.key;listeners.window.hashchange();
 assert(el('wiki-article').innerHTML.includes(p.title),p.key);
 for(const m of p.html.matchAll(/data-route="wiki\/([^"]+)"/g))assert(data.wiki.some(x=>x.key===m[1]),m[1]);
}
location.hash='#process';listeners.window.hashchange();
assert(el('process-content').innerHTML.includes('來源整合'));
location.hash='#lesson/2';listeners.window.hashchange();
listeners.document.keydown({key:'ArrowRight',target:{tagName:'BODY'},preventDefault(){}});
assert.equal(location.hash,'lesson/3');
listeners.window.hashchange();
el('slidejump').change({target:{value:'10'}});assert.equal(location.hash,'lesson/10');
const result={checked_at:new Date().toISOString(),javascript_syntax:'passed',rendered_lesson_pages:rendered,
 checked_diagram_actions:5,checked_quiz_answers:3,rendered_wiki_pages:data.wiki.length,
 internal_wiki_routes:'passed',keyboard_and_select_handlers:'passed',offline_external_dependencies:0,
 limitation:'使用 Node VM 與最小 DOM 替身檢查程式及組合結果；沒有執行真實瀏覽器排版、點擊或手機實機測試。'};
fs.writeFileSync(path.join(root,'reports/html_validation.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
