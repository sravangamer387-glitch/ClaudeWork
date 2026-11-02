#!/bin/bash
# Build PDFs of every manufacturing manual into manuals/pdf/ (pandoc -> HTML -> headless Chromium)

cd "$(dirname "$0")"; mkdir -p pdf html
cat > /tmp/style.css <<'CSS'
body{font-family:Arial,Helvetica,sans-serif;font-size:10.5pt;line-height:1.4;max-width:190mm;margin:auto;color:#111}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:9pt}td,th{border:1px solid #999;padding:3px 5px;vertical-align:top}th{background:#eee}
code,pre{font-family:Consolas,monospace;font-size:9pt;background:#f4f4f4}pre{padding:6px;white-space:pre-wrap}blockquote{border-left:4px solid #c00;margin:8px 0;padding:4px 10px;background:#fff4f4}h1{border-bottom:2px solid #333}
CSS
list=$(ls STANDARD_PROCEDURES.md README.md ORDERING_GUIDE.md ../costing/BOM_COSTS.md ../costing/CONFIDENCE.md ../costing/SIGNOFF.md ../costing/GATEKEEPER_AUDIT.md ../costing/DESIGN_REVIEW_LOG.md; for f in ../*/*/MANUFACTURING_MANUAL.md ../*/MANUFACTURING_MANUAL.md ../*/*/*/MANUFACTURING_MANUAL.md ../*/*/ORDERING.md ../*/ORDERING.md ../*/*/*/ORDERING.md; do [ -f "$f" ] && echo "$f"; done)
for f in $list; do
  n=$(echo "$f" | sed 's#^\.\./##; s#/MANUFACTURING_MANUAL.md##; s#/ORDERING.md#_ORDERING#; s#/#_#g; s#\.md$##'); [ "$f" = "STANDARD_PROCEDURES.md" ] && n=STANDARD_PROCEDURES; [ "$f" = "README.md" ] && n=INDEX
  pandoc "$f" -f gfm -t html5 -s --metadata title="$n" -c /tmp/style.css --self-contained -o html/$n.html 2>/dev/null
done
cat > /tmp/topdf.js <<'JS'
const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const dir=process.argv[2]; const out=process.argv[3];
 for (const f of fs.readdirSync(dir)) { if(!f.endsWith('.html')) continue; await p.goto('file://'+path.resolve(dir,f)); await p.pdf({path:path.join(out,f.replace('.html','.pdf')),format:'A4',margin:{top:'15mm',bottom:'15mm',left:'12mm',right:'12mm'},printBackground:true}); }
 await b.close(); })();
JS
NODE_PATH=$(npm root -g) node /tmp/topdf.js html pdf
ls pdf | wc -l
