const fs = require('fs');
const path = require('path');
const vm = require('vm');

console.log("==========================================================");
console.log("=== Starting 100-Pass Deep DOM & Script Simulation Audit ===");
console.log("==========================================================");

const indexPath = path.join(__dirname, '..', 'index.html');
const htmlSource = fs.readFileSync(indexPath, 'utf8');

const scriptMatch = htmlSource.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) {
    console.error("❌ No script tag found in index.html!");
    process.exit(1);
}
const jsCode = scriptMatch[1];

let passCount = 0;
let failCount = 0;

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
                    value: '',
                    className: '',
                    style: {},
                    listeners: {},
                    disabled: false,
                    children: [],
                    addEventListener(event, fn) {
                        this.listeners[event] = fn;
                    },
                    click() {
                        if (this.listeners['click']) this.listeners['click']({ target: this });
                    },
                    setAttribute(k, v) { this[k] = v; },
                    getAttribute(k) { return this[k] || null; },
                    appendChild(c) {
                        if (!this.children) this.children = [];
                        this.children.push(c);
                    },
                    querySelectorAll() { return []; },
                    querySelector() { return null; },
                    classList: {
                        add() {},
                        remove() {},
                        toggle() {},
                        contains() { return false; }
                    },
                    scrollIntoView() {}
                };
            }
            return elements[id];
        }

        // Pre-initialize DOM elements
        [
            'slide-stage', 'current-slide-num', 'total-slide-num', 'progress-bar',
            'header-title', 'module-badge', 'btn-prev', 'btn-next', 'btn-toc',
            'btn-notes', 'btn-help', 'btn-fullscreen', 'theme-select',
            'animation-select', 'jump-input', 'btn-jump', 'notes-drawer',
            'close-notes', 'notes-content', 'toc-drawer', 'close-toc',
            'toc-list', 'toc-search', 'help-modal', 'close-help'
        ].forEach(id => getOrCreateElement(id));

        const docListeners = {};
        const stateToUse = i % 3 === 0 ? 'complete' : (i % 3 === 1 ? 'interactive' : 'loading');
        
        const mockDocument = {
            readyState: stateToUse,
            body: getOrCreateElement('body', 'body'),
            documentElement: getOrCreateElement('html', 'html'),
            getElementById(id) {
                return getOrCreateElement(id);
            },
            createElement(tag) {
                return getOrCreateElement('elem_' + Math.random(), tag);
            },
            addEventListener(event, fn) {
                docListeners[event] = fn;
            },
            fullscreenElement: null,
            exitFullscreen() {}
        };

        const sandbox = {
            window: {
                slidesData: null,
                localStorage: {
                    getItem() { return 'theme-dark'; },
                    setItem() {}
                }
            },
            document: mockDocument,
            localStorage: {
                getItem() { return 'theme-dark'; },
                setItem() {}
            },
            console: { log() {}, warn() {}, error(e) { console.error("Sandbox Error:", e); } },
            setTimeout: (fn) => fn(),
            setInterval: () => {},
            clearInterval: () => {}
        };

        sandbox.global = sandbox;
        sandbox.window.window = sandbox.window;
        sandbox.window.document = mockDocument;

        const context = vm.createContext(sandbox);
        vm.runInContext(jsCode, context);

        // If readyState was loading, fire DOMContentLoaded
        if (stateToUse === 'loading' && docListeners['DOMContentLoaded']) {
            docListeners['DOMContentLoaded']();
        }

        const stage = elements['slide-stage'];
        const title = elements['header-title'];
        const num = elements['current-slide-num'];
        const totalNum = elements['total-slide-num'];

        if (!stage || !stage.innerHTML || stage.innerHTML.trim() === '') {
            throw new Error(`Pass ${i}: #slide-stage innerHTML is empty! (readyState: ${stateToUse})`);
        }
        if (!title || !title.textContent || title.textContent.trim() === '') {
            throw new Error(`Pass ${i}: #header-title textContent is empty!`);
        }
        if (!num || num.textContent.toString() !== '1') {
            throw new Error(`Pass ${i}: #current-slide-num is ${num ? num.textContent : 'undefined'}, expected 1`);
        }
        if (!totalNum || totalNum.textContent.toString() !== '500') {
            throw new Error(`Pass ${i}: #total-slide-num is ${totalNum ? totalNum.textContent : 'undefined'}, expected 500`);
        }

        // Test Next Navigation
        const btnNext = elements['btn-next'];
        if (btnNext) btnNext.click();
        if (num.textContent.toString() !== '2') {
            throw new Error(`Pass ${i}: Click next failed to advance to Slide 2 (got ${num.textContent})`);
        }

        // Test Prev Navigation
        const btnPrev = elements['btn-prev'];
        if (btnPrev) btnPrev.click();
        if (num.textContent.toString() !== '1') {
            throw new Error(`Pass ${i}: Click prev failed to return to Slide 1 (got ${num.textContent})`);
        }

        passCount++;
        if (i % 10 === 0 || i === 100) {
            console.log(`[Pass ${i}/100] ✅ State: ${stateToUse.padEnd(11)} | Slide 1: "${title.textContent.trim()}" | Total: ${totalNum.textContent} slides`);
        }
    } catch(err) {
        failCount++;
        console.error(`[Pass ${i}/100] ❌ Failure:`, err.message);
    }
}

console.log("\n==========================================================");
console.log(`🎉 100-Pass DOM Simulation Result: ${passCount} Passed, ${failCount} Failed.`);
console.log("==========================================================");

if (failCount > 0) {
    process.exit(1);
}
