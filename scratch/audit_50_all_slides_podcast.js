const fs = require('fs');
const path = require('path');
const vm = require('vm');

console.log("=========================================================================");
console.log("=== 50-Pass Audit: Module 7-10 Slide Podcast & Speech TTS Feature ===");
console.log("=========================================================================");

const slidesDataPath = path.join(__dirname, '..', 'js', 'slidesData.js');
const slidesCode = fs.readFileSync(slidesDataPath, 'utf8');

const sandbox = {
    window: {},
    console: { log() {}, error() {} }
};
vm.createContext(sandbox);
vm.runInContext(slidesCode, sandbox);

const slides = sandbox.window.slidesData;

let passCount = 0;
let failCount = 0;

for (let i = 1; i <= 50; i++) {
    try {
        // Sample slides across Module 7 (301-350), Module 8 (351-400), Module 9 (401-450), Module 10 (451-500)
        const targetSid = 300 + ((i * 4) % 200) + 1; // 301 to 500
        const slide = slides.find(s => s.id === targetSid);
        
        if (!slide) {
            throw new Error(`Pass ${i}: Slide ID ${targetSid} not found in slidesData!`);
        }
        
        if (!slide.podcastScript || typeof slide.podcastScript !== 'string' || slide.podcastScript.length < 50) {
            throw new Error(`Pass ${i}: Slide ${targetSid} in Module 7-10 has invalid or missing podcastScript!`);
        }
        
        passCount++;
        if (i % 10 === 0 || i === 50) {
            console.log(`[Pass ${i}/50] ✅ Module 7-10 Slide Podcast Audit: OK (Slide ${slide.id} [${slide.module}] Has ${slide.podcastScript.length} Chars Podcast Script)`);
        }
    } catch (err) {
        failCount++;
        console.error(`[Pass ${i}/50] ❌ Failure:`, err.message);
    }
}

console.log("\n=========================================================================");
console.log(`🎉 50-PASS MODULE 7-10 PODCAST AUDIT RESULT: ${passCount} Passed, ${failCount} Failed.`);
console.log("=========================================================================");

if (failCount > 0) process.exit(1);
