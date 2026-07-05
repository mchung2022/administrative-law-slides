const fs = require('fs');
const path = require('path');
const vm = require('vm');

console.log("=========================================================================");
console.log("=== 100-Pass Deep Audit & Simulation for Podcast Player & Audio Engine ===");
console.log("=========================================================================");

const playerPath = path.join(__dirname, '..', 'podcast_player.html');
const htmlSource = fs.readFileSync(playerPath, 'utf8');

const scriptMatch = htmlSource.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) {
    console.error("❌ No script tag found in podcast_player.html!");
    process.exit(1);
}
const jsCode = scriptMatch[1];

let passCount = 0;
let failCount = 0;

async function run100Audits() {
    for (let i = 1; i <= 100; i++) {
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
                        duration: 1800,
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
                        getVoices() { return [{ lang: 'zh-TW', name: 'Microsoft Hanhan' }]; }
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
            const engineStatus = elements['engineStatus'];
            const transcriptBox = elements['transcriptBox'];

            // 1. Simulate Play Click
            btnPlay.click();

            // Wait for promise resolution microtask
            await new Promise(r => setTimeout(r, 10));

            if (!btnPlay.textContent.includes("暫停")) {
                throw new Error(`Pass ${i}: Click play button failed to toggle state to pause!`);
            }
            if (!engineStatus.textContent || engineStatus.textContent.trim() === '') {
                throw new Error(`Pass ${i}: Engine status indicator is empty!`);
            }
            if (!transcriptBox.textContent || transcriptBox.textContent.trim() === '') {
                throw new Error(`Pass ${i}: Transcript box text is empty!`);
            }

            // 2. Simulate Pause Click
            btnPlay.click();
            if (!btnPlay.textContent.includes("播放")) {
                throw new Error(`Pass ${i}: Click pause failed to return state to play!`);
            }

            passCount++;
            if (i % 10 === 0 || i === 100) {
                console.log(`[Pass ${i}/100] ✅ Play Click Simulation: OK | Engine Status: "${engineStatus.textContent.trim().slice(0, 30)}..."`);
            }
        } catch(err) {
            failCount++;
            console.error(`[Pass ${i}/100] ❌ Failure:`, err.message);
        }
    }

    console.log("\n=========================================================================");
    console.log(`🎉 100-PASS PODCAST PLAYER AUDIT RESULT: ${passCount} Passed, ${failCount} Failed.`);
    console.log("=========================================================================");

    if (failCount > 0) {
        process.exit(1);
    }
}

run100Audits();
