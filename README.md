# 圍棋入門教室

以五篇已閱讀來源建立 LLM Wiki，再從 Wiki 編排十六頁繁體中文教學 HTML 簡報。
適用完全新手，使用 9 路盤，含三題盤面練習。面積計分示範另列白貼 6.5 為教學設定。

## GitHub Pages 網站

預定儲存庫名稱為 go-wiki。上傳完成後，在 Settings、Pages 的 Build and deployment 選擇 Deploy from a branch，選 main 與 / (root)，再儲存。
啟用並完成發布後，網站網址為 https://fufudadafu.github.io/go-wiki/ 。
本專案的入口 index.html 已準備完成，並包含 .nojekyll，適合從根目錄直接發布。

## 開始使用

解壓縮後開啟 go-beginner.html，或開啟 dist/index.html。
頁面包含「教學簡報」「知識 Wiki」「流程與反思」三個區域。
簡報可用上一頁／下一頁、頁面選單及鍵盤左右鍵操作。
所有程式、盤面與文字均在單一 HTML 中，不需要安裝套件或 API 金鑰。

## 作業內容對照

| 作業要求 | 檔案或位置 |
| --- | --- |
| 先討論後生成 | 原對話、reports/assignment.md 的討論紀錄 |
| ingest 至少五篇 | raw/S01.json 至 S05.json、wiki/sources/ |
| 可維護 Wiki | wiki/index.md、wiki/concepts/、AGENTS.md |
| 教學 HTML 簡報 | go-beginner.html、dist/index.html |
| loop / graph | HTML 的流程與反思、reports/workflow.mmd |
| 實際反思 | reports/assignment.md |
| 來源與檢查 | wiki/synthesis.md、reports/validation.json、reports/html_validation.json |

raw 保存來源網址與有限摘錄等閱讀紀錄，不包含完整原文。外文圖例沒有直接拷貝，所有盤面均為自編示意。
來源 S05 是 1991 版 AGA 簡明規則，僅取其面積計分等基本定義，不代表所有現行比賽都採同樣貼目或程序。
GitHub 專案入口為本資料夾的 index.html；若儲存庫已啟用 GitHub Pages，可以直接透過資料夾網址開啟。go-beginner.html 也可下載離線使用。

## 重建與檢查

需要 Node.js 及 Python 3，不需要額外依賴。

    node tools/check_go.mjs
    python3 tools/build.py
    node tools/check_html.mjs

build.py 將已整理的 Wiki 與內容重建為 HTML，不會自動呼叫 LLM 或取得新資料。
prepare_content.py 是本次初次整理的紀錄工具，已執行完成，會拒絕覆蓋現有來源閱讀紀錄。
後續新增來源請先實際讀取正文，依 AGENTS.md 更新相關概念與來源，再重建 HTML。

## 驗證範圍

已做棋盤運算、答案、內部連結、內嵌 JavaScript 語法與最小 DOM 導航檢查。
未做真實瀏覽器排版、實際點擊與手機視覺測試。此程式只驗證教學局面，不是完整比賽規則引擎。
