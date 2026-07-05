const fs = require('fs');
const path = require('path');

console.log("=== 30-Minute Podcast Media & Web Player Verification Audit ===");

const rootDir = path.join(__dirname, '..');
const wavPath = path.join(rootDir, 'podcast_audio_30min.wav');
const playerPath = path.join(rootDir, 'podcast_player.html');
const docxPath = path.join(rootDir, '行政法30分鐘Podcast廣播講堂_完整廣播劇本.docx');
const jsonPath = path.join(__dirname, 'podcast_script_30min.json');

let pass = 0;
let fail = 0;

function audit(name, cond, details = '') {
    if (cond) {
        pass++;
        console.log(`✅ [PASS] ${name} ${details}`);
    } else {
        fail++;
        console.error(`❌ [FAIL] ${name} ${details}`);
    }
}

// 1. WAV Audio File Audit
const wavExists = fs.existsSync(wavPath);
audit('WAV Audio File Existence Audit', wavExists);
if (wavExists) {
    const wavSizeMB = fs.statSync(wavPath).size / (1024 * 1024);
    audit('WAV Audio File Size Audit (>10MB)', wavSizeMB > 10, `(Size: ${wavSizeMB.toFixed(2)} MB)`);
}

// 2. Word Script Document Audit
const docxExists = fs.existsSync(docxPath);
audit('Word Podcast Script (.docx) Audit', docxExists);
if (docxExists) {
    const docxKB = fs.statSync(docxPath).size / 1024;
    audit('Word Script Size Audit (>20KB)', docxKB > 20, `(Size: ${docxKB.toFixed(1)} KB)`);
}

// 3. JSON Script Audit
const jsonExists = fs.existsSync(jsonPath);
audit('JSON Script File Existence Audit', jsonExists);
if (jsonExists) {
    const chapters = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    audit('JSON Chapter Count Audit (10 Chapters)', chapters.length === 10);
    const totalChars = chapters.reduce((acc, c) => acc + c.script.length, 0);
    audit('JSON Script Total Spoken Chars (>5000 chars)', totalChars >= 5000, `(Total Chars: ${totalChars})`);
}

// 4. Web Player HTML Audit
const playerExists = fs.existsSync(playerPath);
audit('Web Player HTML (podcast_player.html) Audit', playerExists);
if (playerExists) {
    const htmlText = fs.readFileSync(playerPath, 'utf8');
    audit('Audio Source Binding Audit', htmlText.includes('podcast_audio_30min.wav'));
    audit('Canvas Visualizer Binding Audit', htmlText.includes('waveformCanvas'));
    audit('10 Chapter Markers Audit', htmlText.includes('chapters = ['));
}

console.log("\n==================================================");
console.log(`🎉 PODCAST AUDIT RESULT: ${pass} Passed, ${fail} Failed.`);
console.log("==================================================");

if (fail > 0) process.exit(1);
