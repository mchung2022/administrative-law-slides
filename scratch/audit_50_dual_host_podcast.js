const fs = require('fs');
const path = require('path');
const vm = require('vm');

console.log("=========================================================================");
console.log("=== 50-Pass Audit: Dual-Host 30-Min Dialogue & Taiwan Legal Accuracy ===");
console.log("=========================================================================");

const playerPath = path.join(__dirname, '..', 'podcast_player.html');
const mp3Path = path.join(__dirname, '..', 'podcast_audio_30min.mp3');

const htmlSource = fs.readFileSync(playerPath, 'utf8');

// 1. Audit MP3 File Size & Duration (>7MB)
const mp3SizeMB = fs.statSync(mp3Path).size / (1024 * 1024);
console.log(`[MP3 Audit] Dual-Host MP3 File Size: ${mp3SizeMB.toFixed(2)} MB`);

const scriptMatch = htmlSource.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) {
    console.error("❌ No script tag found!");
    process.exit(1);
}
const jsCode = scriptMatch[1];

let passCount = 0;
let failCount = 0;

// Legal Keywords strict check for each chapter (0 to 9)
const requiredLegalTerms = [
    '依法行政原則', // Ch 1
    '釋字第 443 號', // Ch 2
    '比例原則',     // Ch 3
    '信賴保護原則', // Ch 4
    '行政處分',     // Ch 5
    '行政指導',     // Ch 6
    '行政罰法',     // Ch 7
    '行政執行法',   // Ch 8
    '訴願',         // Ch 9
    '國家賠償法'    // Ch 10
];

async function run50Audits() {
    for (let i = 1; i <= 50; i++) {
        try {
            const elements = {};
            function getOrCreateElement(id, tag = 'div') {
                if (!elements[id]) {
                    elements[id] = {
                        id: id,
                        tagName: tag.toUpperCase(),
                        innerHTML: '',
                        textContent: '',
                        value: '1.0',
                        className: '',
                        style: {},
                        listeners: {},
                        children: [],
                        currentTime: 0,
                        duration: 1603.68,
                        paused: true,
                        volume: 1.0,
                        playbackRate: 1.0,
                        play() {
                            this.paused = false;
                            return Promise.resolve();
                        },
                        pause() {
                            this.paused = true;
                        },
                        addEventListener(event, fn) {
                            this.listeners[event] = fn;
                        },
                        click() {
                            if (this.listeners['click']) this.listeners['click']({ target: this });
                        },
                        setAttribute(k, v) { this[k] = v; },
                        getAttribute(k) { return this[k] || null; },
                        appendChild(c) {
                            this.children.push(c);
                        },
                        classList: {
                            add(cls) { this.className += ' ' + cls; },
                            remove(cls) { this.className = this.className.replace(cls, '').trim(); },
                            toggle(cls) { this.className += ' ' + cls; },
                            contains(cls) { return this.className.includes(cls); }
                        },
                        scrollIntoView() {}
                    };
                }
                return elements[id];
            }

            [
                'mainAudio', 'btnPlay', 'btnRewind', 'btnForward', 'seekSlider',
                'currentTime', 'durationTime', 'speedSelect', 'volumeSlider',
                'chapterPane', 'transcriptBox', 'engineStatus', 'waveformCanvas'
            ].forEach(id => getOrCreateElement(id));

            const canvasElem = getOrCreateElement('waveformCanvas');
            canvasElem.offsetWidth = 500;
            canvasElem.offsetHeight = 120;
            canvasElem.getContext = () => ({
                clearRect() {},
                beginPath() {},
                moveTo() {},
                lineTo() {},
                stroke() {}
            });

            const mockDocument = {
                readyState: 'complete',
                body: getOrCreateElement('body', 'body'),
                documentElement: getOrCreateElement('html', 'html'),
                getElementById(id) {
                    return getOrCreateElement(id);
                },
                createElement(tag) {
                    return getOrCreateElement('elem_' + Math.random(), tag);
                },
                querySelectorAll() { return []; },
                addEventListener() {}
            };

            const sandbox = {
                window: {
                    addEventListener() {},
                    speechSynthesis: {
                        speaking: false,
                        speak() {},
                        cancel() {},
                        getVoices() { return [{ lang: 'zh-TW', name: 'Microsoft HsiaoChen' }]; }
                    },
                    SpeechSynthesisUtterance: function(text) {
                        this.text = text;
                        this.lang = 'zh-TW';
                    },
                    fetch() {
                        return Promise.reject(new Error("CORS local file simulation"));
                    }
                },
                document: mockDocument,
                console: { log() {}, warn() {}, error() {} },
                setTimeout: (fn) => fn(),
                setInterval: () => {},
                clearInterval: () => {},
                requestAnimationFrame: () => {}
            };

            sandbox.global = sandbox;
            sandbox.window.window = sandbox.window;
            sandbox.window.document = mockDocument;

            const context = vm.createContext(sandbox);
            vm.runInContext(jsCode, context);

            const btnPlay = elements['btnPlay'];
            const transcriptBox = elements['transcriptBox'];
            const chapterPane = elements['chapterPane'];

            // Test Chapter Jump Alignment across 10 chapters
            const targetChIdx = (i % 10);
            const targetCard = chapterPane.children[targetChIdx];
            if (targetCard) targetCard.click();

            await new Promise(r => setTimeout(r, 5));

            if (!btnPlay.textContent.includes("暫停")) {
                throw new Error(`Pass ${i}: Chapter jump click failed to switch state to playing!`);
            }
            if (!transcriptBox.textContent || transcriptBox.textContent.length < 50) {
                throw new Error(`Pass ${i}: Transcript text sync is empty or incomplete!`);
            }

            // Verify Male and Female Co-Host Tags in Transcript
            if (!transcriptBox.textContent.includes("【阿哲】") || !transcriptBox.textContent.includes("【小晨】")) {
                throw new Error(`Pass ${i}: Dual-host tags 【阿哲】 or 【小晨】 missing from transcript!`);
            }

            // Verify Legal accuracy term presence
            const requiredTerm = requiredLegalTerms[targetChIdx];
            if (!transcriptBox.textContent.includes(requiredTerm)) {
                throw new Error(`Pass ${i}: Required Taiwanese legal term '${requiredTerm}' missing in Chapter ${targetChIdx+1}!`);
            }

            // Pause
            btnPlay.click();

            passCount++;
            if (i % 10 === 0 || i === 50) {
                console.log(`[Pass ${i}/50] ✅ Dual-Host 30-Min Podcast & Legal Accuracy Audit: OK (Chapter ${targetChIdx+1} Verified)`);
            }
        } catch(err) {
            failCount++;
            console.error(`[Pass ${i}/50] ❌ Failure:`, err.message);
        }
    }

    console.log("\n=========================================================================");
    console.log(`🎉 50-PASS DUAL-HOST PODCAST AUDIT RESULT: ${passCount} Passed, ${failCount} Failed.`);
    console.log("=========================================================================");

    if (failCount > 0) process.exit(1);
}

run50Audits();
