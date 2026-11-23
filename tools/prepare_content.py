import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-11-23"
if any((ROOT/"raw"/("S0"+str(i)+".json")).exists() for i in range(1,6)):
    raise SystemExit("來源紀錄已存在。此工具僅用於初次建立；請依 AGENTS.md 重新讀取來源並建立新版本。重建 HTML 請用 tools/build.py。")
SOURCES = [
 dict(id="S01",title="囲碁ってなあに？",label="圍棋是什麼？",org="日本棋院",language="日文",
      url="https://www.nihonkiin.or.jp/teach/gakkouigo/aboutigo.html",
      sections=["囲碁のルール","終局"],version="頁面未標明規則版本",
      points=["以黑白棋輪流落在交叉點，建立對局的基本認識。","提子、不能落子的位置與劫都有入門圖例。"],
      note="此頁終局示範以空點與提子處理，標為數目法資料；不把它當作本簡報的數子計算依據。",
      quote="囲碁は黒から順番に線と線の交差点に打ちます。"),
 dict(id="S02",title="囲碁の基本：囲碁ゲームの２大要素",label="氣與提子",org="日本棋院",language="日文",
      url="https://www.nihonkiin.or.jp/teach/lesson/school/youso.html",
      sections=["呼吸点","呼吸点を封じられると石は生きられない"],version="頁面未標明規則版本",
      points=["棋子上下左右的相鄰空點是氣，斜角不列入。","同一塊棋的氣全部被占滿時，整塊棋一起移除。"],
      note="只抽取氣與提子的解釋。此頁另含日式提子計分敘述，保留規則標記。",
      quote="石の呼吸点は石の置かれた場所のナナメではなく、十字の線上にあります。"),
 dict(id="S03",title="囲碁の基本：石を打てない所",label="合法落子與禁入點",org="日本棋院",language="日文",
      url="https://www.nihonkiin.or.jp/teach/lesson/school/kinshi.html",
      sections=["石を打てる所、打てない所"],version="頁面未標明規則版本",
      points=["判斷落子是否合法時，必須考慮提子之後的棋盤。","若能先提走對方無氣的棋，落點原本被包圍也可能合法。"],
      note="不能簡化成『四周都是對手的棋就不能下』；練習題會檢查提子的例外。",
      quote="相手の石を取り上げることができる"),
 dict(id="S04",title="How to Play",label="9 路盤入門、眼與劫",org="英國圍棋協會",language="英文",
      url="https://www.britgo.org/intro/intro2.html",
      sections=["Strings","Life and death and the concept of eyes","The ko rule","Seki","Komi"],
      version="頁面最後更新標示 2017-10-26",
      points=["以九路盤示範連接、眼、劫與雙活，適合安排入門順序。","兩個分開的真眼可保障同一塊棋存活；雙活提醒我們不能把無兩眼一律當死棋。"],
      note="主文採數目計分並含 AGA 終局程序；這些設定不直接混入數子例題。其 7.5 貼目敘述也不視為所有棋盤通用。",
      quote="We recommend that beginners learn the basics on a 9 by 9 board"),
 dict(id="S05",title="American Go Association Rules - Short Version",label="終局與數子法定義",org="AGA 制定，英國圍棋協會轉載",language="英文",
      url="https://www.britgo.org/rules/agashort.html",
      sections=["9) Ending the Game","12) Counting"],version="1991 年 4 月版；轉載頁標示 2017-11-29 更新",
      points=["面積計分把盤上活子與所圍空點相加，已提走的棋子不再另加分。","連續停一手後，仍需確認死活；存在爭議時要按所採規則處理。"],
      note="僅引用面積計分的定義及終局基本觀念。舊版 5.5 貼目、停一手交子、白最後行棋等屬該版本設定，不冒充完整中國規則。",
      quote="Prisoners are ignored.")
]

PAGES = [
("board","棋盤與落子",["S01","S04","S05"],"""## 基本概念
棋子下在線與線的交叉點。一般平手對局由黑先白後，輪到自己可以在合法空點落一子，也可以停一手。落下的棋子留在原處，直到被提走。

## 教學範圍
本教學以 9 路盤示範，共有 81 個交叉點。19 路盤有 361 個交叉點。本課不使用讓子局。

## 閱讀連結
先看[氣與連接](liberties.md)，再看[打吃與提子](capture.md)。
"""),
("liberties","氣與連接",["S02","S04","S05"],"""## 定義
上下左右相鄰的同色棋子形成同一塊棋。這塊棋相鄰的空交叉點集合，就是它的氣。

## 數氣方法
找出整塊棋，檢查每顆棋子的四個相鄰點，把重複空點只算一次。斜角既不是直接連接，也不直接提供氣。

## 常見誤解
不能直接把每顆棋子的氣相加，因為它們可能共用同一口氣。邊角交叉點的相鄰方向較少。

## 閱讀連結
接著看[打吃與提子](capture.md)與[合法落子](legal.md)。
"""),
("capture","打吃與提子",["S02","S04","S05"],"""## 基本判斷
一塊棋只剩一口氣，稱為打吃。對手占住最後一口氣後，這塊棋失去所有氣，便整塊提離棋盤。

## 與勝負的關係
提子可以幫助保護自己的棋與取得空間。本課採用的面積計分，不把提走的棋子再額外加分。

## 閱讀連結
提子可能改變落子的合法性，請看[合法落子](legal.md)；勝負請看[數子法](scoring.md)。
"""),
("legal","合法落子與禁入點",["S03","S05"],"""## 判斷順序
先確認交叉點沒有棋子，再假設放下自己的棋，先提走因此無氣的對方棋塊。之後自己的棋塊仍須有氣，並且符合劫的限制。

## 提子的例外
一個空點即使四周都是對方棋子，落子若能提走對方棋子並取得氣，仍可能合法。不能只看落子前的外觀。

## 本課邊界
本課禁止自殺，僅用簡單劫展示不能立即提回。其他規則系統的自殺與全局重複判定不展開。

## 閱讀連結
搭配[打吃與提子](capture.md)與[劫](ko.md)閱讀。
"""),
("ko","劫與立即提回限制",["S01","S04","S05"],"""## 簡單劫
有些局面中，一方提走一顆棋子後，對方若立刻提回，就會回到剛才的盤面。簡單劫的限制阻止這種立即反覆。

## 教學用法
用同一局面的提子前後圖比較，不把每一次提子都叫作劫。若對方沒有補劫，之後是否可提回，仍取決於局面與所採規則。

## 版本邊界
AGA 舊版還有全局重複盤面與輪次的規定。本課的局部示範與驗證程式只檢查簡單劫，並不是完整比賽規則引擎。

## 閱讀連結
返回[合法落子](legal.md)。
"""),
("eyes","眼與簡單活棋",["S04"],"""## 眼的概念
眼是棋塊內部保留的空間。真眼與假眼需要根據周圍連接判斷，不能只憑看見一個空點就斷定。

## 本課示範
示範同一塊相連棋具有兩個分開真眼的情況。對手無法藉正常合法落子同時填滿兩眼，因此這塊棋可以存活。

## 不可過度推論
不能由此推論沒有兩眼就一定死；雙活是重要例外。本課只提示雙活存在，不教複雜判斷。

## 閱讀連結
接著看[終局](ending.md)。
"""),
("ending","停一手與終局",["S04","S05"],"""## 終局流程
當雙方認為沒有需要繼續下的地方，可以停一手。連續停一手通常表示進入終局確認，而不是略過死活判定直接算分。

## 確認死活
雙方先確認剩餘棋子的死活，移除同意的死子，再計分。有爭議時依採用規則續弈或處理，不能由程式憑外觀任意刪子。

## 本課範例
數子例題預先給定雙方已確認無死子，因此只計算明確的活子與單方所圍空點。此例不教 AGA 停一手交子等完整程序。

## 閱讀連結
閱讀[數子法](scoring.md)。
"""),
("scoring","數子法與貼目",["S05","S01","S04"],"""## 本課採用的定義
面積計分把盤上活子數與己方所圍空點數相加。共同相鄰黑白兩色的中立空點不屬於任一方。提走的棋子不再另外加分。

## 教學例題設定
採 9 路盤、不讓子、白貼 6.5 分。這是清楚標示的教學設定，並非宣稱所有 9 路比賽都用相同貼目。
自編終局中，黑活子 43、黑空點 2，白活子 34、白空點 2；雙方已確認無死子與中立點。黑得 45，白加貼目後得 42.5，黑勝 2.5 分。

## 來源差異
S01 與 S04 的主要終局範例採數目思路。S05 同時定義面積與地域兩種計分，且其 1991 版貼目為 5.5。本課僅取 S05 的面積定義，不把這些參數混作單一官方規則。

## 閱讀連結
返回[終局](ending.md)，或查[術語表](glossary.md)。
"""),
("glossary","入門術語表",["S01","S02","S03","S04","S05"],"""## 中英日對照
氣：liberty，呼吸点。
打吃：atari，アタリ。
提子：capture，石を取る。
眼：eye，眼。
劫：ko，コウ。
停一手：pass，パス。
數子法：area counting，盤上活子與空點都計入。
數目法：territory counting，處理地域及俘子；細節依規則而異。

## 使用原則
不同語言詞彙先統一再整合，不把所有規則差異都當翻譯問題。

## 閱讀連結
從[棋盤與落子](board.md)開始。
""")
]

def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding="utf-8")

log=["# 實際執行紀錄\n",f"- 日期：{TODAY}（Asia/Taipei）",
     "- 執行方式：本次對話中的 AI 實際開啟並讀取五個正文頁面，再手動編輯持久化檔案。沒有假設背景呼叫另一個 LLM API。",
     "- 討論階段：使用者先選定完全新手、9 路盤、繁體中文、數子法及三題盤面練習，並確認五個來源。"]
for s in SOURCES:
    receipt={k:v for k,v in s.items() if k!="quote"}
    receipt.update(accessed_on=TODAY,read_status="正文已透過網頁讀取工具確認",storage="保留網址、有限摘錄及整理紀錄，未保存完整原文",excerpt=s["quote"])
    write(ROOT/"raw"/(s["id"]+".json"),json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    md="# "+s["id"]+" "+s["label"]+"\n\n"
    md+="原題："+s["title"]+"\n\n機構："+s["org"]+"\n\n語言："+s["language"]+"\n\n"
    md+="版本："+s["version"]+"\n\n取得日期："+TODAY+"\n\n[原始網頁]("+s["url"]+")\n\n## 閱讀段落\n"
    md+="\n".join("- "+v for v in s["sections"])+"\n\n## 整理重點\n"
    md+="\n".join("- "+v for v in s["points"])+"\n\n## 適用範圍與檢查\n"+s["note"]+"\n"
    md+="\n## 相關概念\n"+"\n".join("- ["+p[1]+"](../concepts/"+p[0]+".md)" for p in PAGES if s["id"] in p[2])+"\n"
    write(ROOT/"wiki/sources"/(s["id"]+".md"),md)
    log.append("\n## ingest "+s["id"]+"\n- 讀取段落："+ "、".join(s["sections"])+"\n- 建立 raw/"+s["id"]+".json 與 wiki/sources/"+s["id"]+".md。\n- 檢查："+s["note"])
    write(ROOT/"wiki/index.md","# 圍棋 LLM Wiki\n\n## 已 ingest 來源\n"+"\n".join("- ["+x["id"]+" "+x["label"]+"](sources/"+x["id"]+".md)" for x in SOURCES if x["id"]<=s["id"])+"\n")
    write(ROOT/"wiki/log.md","\n".join(log)+"\n")

for slug,title,refs,body in PAGES:
    links="、".join("["+sid+"](../sources/"+sid+".md)" for sid in refs)
    write(ROOT/"wiki/concepts"/(slug+".md"),"# "+title+"\n\n來源："+links+"\n\n"+body)
index="# 圍棋 LLM Wiki\n\n對象：完全新手。示範棋盤：9 路。教學計分：面積計分，例題另外列出貼目。\n\n## 概念目錄\n"
index+="\n".join("- ["+p[1]+"](concepts/"+p[0]+".md)" for p in PAGES)
index+="\n\n## 五篇已 ingest 來源\n"+"\n".join("- ["+s["id"]+" "+s["label"]+"](sources/"+s["id"]+".md)" for s in SOURCES)
index+="\n\n## 維護紀錄\n- [實際執行紀錄](log.md)\n- [規則差異與使用邊界](synthesis.md)\n"
write(ROOT/"wiki/index.md",index)
synthesis="""# 規則差異與使用邊界

| 議題 | 觀察 | 本專案處理 |
| --- | --- | --- |
| 計分方法 | S01、S02 與 S04 含數目計分；S05 同時列出面積與地域計分 | 只用 S05 的面積定義製作數子例題 |
| 貼目與版本 | S05 是 1991 版，寫 5.5；S04 提到比賽常用 7.5，情境不同 | 教學題自行明列白貼 6.5，不宣稱通用 |
| 終局程序 | AGA 文本含停一手交子及白最後行棋 | 不把這些細節冒充中國規則；本課只教基本概念 |
| 活棋 | 兩眼是簡單可靠形狀，但 S04 另說明雙活 | 不寫成沒有兩眼一律死 |
| 劫的範圍 | S05 涉及全局重複盤面；簡報只展示局部簡單劫 | 檢查程式標示僅驗證教學例圖 |

## 整合方法
先讀來源卡，再把共通定義整合進概念頁。矛盾或版本差異先留在這一頁，經明確選擇才進入教學內容。
來源頁與概念頁互相連結，所有概念都有來源，後續新增資料時可找到受影響頁面。
"""
write(ROOT/"wiki/synthesis.md",synthesis)
log.append("\n## synthesis\n- 完成九篇交叉連結概念頁及規則差異表。\n- 內容整合共發現兩類主要問題：計分方法差異、貼目及版本設定差異。\n- 將規則分類與參數檢查放到 ingest 前，之後再進行概念整合與簡報大綱。\n- 所有棋盤例圖與數字均為本專案自編示意，並非職業棋譜。")
write(ROOT/"wiki/log.md","\n".join(log)+"\n")
write(ROOT/"raw/README.md","""# 來源層說明

五個 JSON 是逐篇閱讀的來源紀錄，保存原始網址、機構、版本、取得日期、讀取段落與有限摘錄。原文仍由原站提供，這裡未保存完整網頁或圖像。
S01 至 S05 每篇均實際開啟正文後才整理。重新 ingest 時要先重讀原網址，再保存新版本；不要把本次摘要冒充新讀到的全文。
本資料夾作為本次閱讀的固定輸入紀錄，整理與修正寫在 wiki 層。
""")
write(ROOT/"AGENTS.md","""# 圍棋 LLM Wiki 專案規則

## 目標
為完全新手維護繁體中文圍棋 Wiki，再以它製作 9 路盤教學 HTML 簡報。現有五篇來源已由本次對話讀取。

## 結構
- raw/：固定閱讀紀錄，不修改既有來源紀錄；重新讀取建立新版本。
- wiki/sources/：每篇資料一張摘要卡，必須有原始網址、機構、取得日期與規則版本。
- wiki/concepts/：跨來源整合的概念頁，保留來源連結及相關頁面。
- wiki/index.md：目錄；wiki/log.md：依序追加的操作紀錄。
- wiki/synthesis.md：來源差異與採用範圍。
- dist/index.html：可離線開啟的教學簡報與 Wiki 閱讀器。
- reports/：實際流程、查詢紀錄與驗證結果。

## ingest
先討論再生成。一次處理一篇：讀正文、檢查可讀性與規則版本、記錄 metadata、寫來源卡、更新概念與目錄、追加 log。失敗就停在來源節點重新取得，不能憑標題補寫內容。

## 查詢與生成
先查 index，再讀相關概念頁及必要來源卡。簡報的知識來源是 Wiki，內容缺口先補 Wiki。自編例題標為教學示意，與來源原例分開。

## 規則
面積計分採活子加空點，不另加提子。每個數值例題明列貼目。不可混用數目法。不能把 1991 版 AGA 的所有程序宣稱為完整中國規則。
氣取相鄰空點聯集。合法落子先提對手無氣棋，再判自己是否有氣。劫例圖驗證立即提回會重複盤面。兩眼示範不推論所有無兩眼的棋都死。

## 檢查
新增或修改盤面必須執行 node tools/check_go.mjs。
概念、來源連結、三題答案、計分與 HTML 語法都要檢查。實際未進行的瀏覽器操作不得寫成已通過。
""")

queries=[
 dict(question="初學者從哪裡開始？",pages=["board","liberties"],decision="先介紹交叉點與氣，使用 9 路盤。"),
 dict(question="四周都是對手棋子就不能下嗎？",pages=["legal","capture"],decision="先判斷能否提走對手棋，製作提子例外練習。"),
 dict(question="沒有兩眼就一定死嗎？",pages=["eyes"],decision="補上雙活提示，保留規則邊界。"),
 dict(question="計分是否還要加提子？",pages=["scoring","ending"],decision="本課面積計分不另加提子，例題明列白貼 6.5。")
]
write(ROOT/"reports/wiki_queries.json",json.dumps(queries,ensure_ascii=False,indent=2)+"\n")
data=dict(date=TODAY,sources=SOURCES,pages=[dict(slug=p[0],title=p[1],refs=p[2],markdown=p[3]) for p in PAGES],queries=queries)
write(ROOT/"content.json",json.dumps(data,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(dict(ingested=len(SOURCES),concept_pages=len(PAGES),source_receipts=5),ensure_ascii=False))
