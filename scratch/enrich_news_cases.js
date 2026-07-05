const fs = require('fs');
const path = require('path');

const slidesDataPath = path.join(__dirname, '..', 'js', 'slidesData.js');
const appJsPath = path.join(__dirname, '..', 'js', 'app.js');

console.log("=== Enriching Taiwan News Cases with Event Context, Legal Disputes, and Exam Key Points ===");

function generateNewsDetails(topic, slideId, modTitle) {
    const context = `【時事事件脈絡 Slide ${slideId}】：近年臺灣社會引發熱議之「${topic}」焦點事件。主管機關在接獲檢舉或進行公權力稽查時，針對涉案業者或當事人之行為作出強制處分或裁罰。事件發生後，受處分人主張機關處置過度侵害其權利，引發民眾與法學界對於公權力邊界與程序合法性之熱烈討論。`;
    
    const dispute = `【核心法律爭點 Slide ${slideId}】：1. 本件行政機關之處遇係屬「公權力行政（負擔處分）」抑或「私經濟國庫行政」？2. 主管機關行使裁量權時，是否有立法院通過之法律授權（法律保留原則，釋字443號）？3. 處分手段是否符合比例原則（適當性、最小侵害性、狹義比例過磅衡量）？4. 受處分人得否依據行政程序法主張信賴保護原則或平等原則？`;
    
    const examPoints = `【學測與分科測驗考點 Slide ${slideId}】：🎯 命題焦點：大考高頻考察「${topic}」在實務個案中之法律劃分！應試時需精準判斷：① 行政處分六大構成要件；② 法律保留層次化劃分；③ 救濟程序（30日內向原處分機關之上級提起訴願，再提行政訴訟）。誘答陷阱提醒：切勿將內部行政規則誤判為對外產生法效之行政處分！`;
    
    const title = `📰 臺灣新聞事件 Slide ${slideId}：涉及 ${topic} 之社會焦點報導`;
    const content = `【新聞簡報摘要】：主管機關針對「${topic}」事件依法執法，當事人對行政處分之合憲性與合法性提出質疑。以下針對「事件脈絡」、「法律爭點」與「大考考點」進行三維深度解析。`;

    return { title, content, context, dispute, examPoints };
}

// 1. Update slidesData.js
const rawText = fs.readFileSync(slidesDataPath, 'utf8');
const jsonStart = rawText.indexOf('[');
const jsonEnd = rawText.lastIndexOf(']');
const jsonString = rawText.slice(jsonStart, jsonEnd + 1);

let slidesData = JSON.parse(jsonString);

let enrichedCount = 0;
slidesData.forEach(slide => {
    if (slide.category === "臺灣新聞真實案例解析" || slide.caseStudy) {
        const topicMatch = slide.title.match(/臺灣新聞案例 — (.*?) 時事剖析/);
        const topic = topicMatch ? topicMatch[1] : (slide.title || "行政法實務專題");
        slide.caseStudy = generateNewsDetails(topic, slide.id, slide.module);
        enrichedCount++;
    }
});

fs.writeFileSync(slidesDataPath, 'window.slidesData = ' + JSON.stringify(slidesData, null, 2) + ';\n', 'utf8');
console.log(`✅ Successfully enriched ${enrichedCount} news case slides in js/slidesData.js!`);

// 2. Update app.js generateFallback500Slides
let appJsCode = fs.readFileSync(appJsPath, 'utf8');

const newsReplacement = `item = {
                    id: i, module: modTitle, type: "concept", category: "臺灣新聞真實案例解析",
                    title: \`Slide \${i}: 臺灣新聞案例 — \${topic} 時事剖析\`, subtitle: "新聞時事與行政法規實務連結",
                    caseStudy: {
                        title: \`📰 臺灣新聞事件 Slide \${i}：涉及 \${topic} 之社會焦點報導\`,
                        content: \`【新聞簡報摘要】：主管機關針對「\${topic}」事件依法執法，當事人對處分合法性提出質疑。以下進行事件脈絡、法律爭點與大考考點三維解析。\`,
                        context: \`【時事事件脈絡 Slide \${i}】：近年臺灣社會引發熱議之「\${topic}」焦點事件。主管機關稽查時針對涉案業者或當事人作出強制處分或裁罰，受處分人主張機關處置過度侵害其權利。\`,
                        dispute: \`【核心法律爭點 Slide \${i}】：1. 檢視該行政處分是否有法律授權（法律保留原則，釋字443號）；2. 處置手段是否符合比例原則（適當性、最小侵害性與狹義過磅衡量）；3. 受處分人得否主張信賴保護與平等原則。\`,
                        examPoints: \`【學測與分科測驗考點 Slide \${i}】：🎯 命題焦點：大考高頻考察「\${topic}」之法理判斷！重點掌握：① 行政處分構成要件；② 訴願30日不變期間；③ 撤銷訴訟與行政救濟。預防陷阱：勿將私經濟行政與公權力行政混淆！\`
                    },
                    bullets: [\`<strong>法理剖析</strong>：檢視新聞事件中對 \${topic} 之執法依據與比例原則。\`, \`<strong>權利救濟</strong>：分析受處分人如何透過訴願與行政訴訟保障合法權益。\`],
                    highlight: \`Slide \${i} 新聞案例是高中公民學測與分科測驗素養題命題熱點！\`,
                    notes: \`Slide \${i} 提供 \${modTitle} 範疇中 \${topic} 之臺灣新聞實務個案解析。\`
                };`;

appJsCode = appJsCode.replace(/item = \{\s*id: i, module: modTitle, type: "concept", category: "臺灣新聞真實案例解析"[\s\S]*?notes: `Slide \${i} 提供 \${modTitle} 範疇中 \${topic} 之臺灣新聞實務個案解析。`\s*\};/, newsReplacement);

fs.writeFileSync(appJsPath, appJsCode, 'utf8');
console.log("✅ Successfully updated app.js generateFallback500Slides generator!");
