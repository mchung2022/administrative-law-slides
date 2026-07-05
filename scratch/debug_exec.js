const fs = require('fs');
const path = require('path');
const vm = require('vm');

const indexPath = path.join(__dirname, '..', 'index.html');
const htmlSource = fs.readFileSync(indexPath, 'utf8');
const scriptMatch = htmlSource.match(/<script>([\s\S]*?)<\/script>/);
let jsCode = scriptMatch[1];

jsCode = jsCode.replace('function renderTOC() {', 'function renderTOC() { console.log("===> ENTERING renderTOC()"); if (!tocList) return;');
jsCode = jsCode.replace('function renderSlide(index) {', 'function renderSlide(index) { console.log("===> ENTERING renderSlide()", index);');

const mockDocument = {
    id: 'MY_MOCK_DOCUMENT_ID',
    readyState: 'complete',
    body: { style: {} },
    documentElement: { style: {} },
    getElementById(id) {
        console.log('✅ getElementById called for:', id);
        return {
            addEventListener() {},
            style: {},
            setAttribute() {},
            textContent: '',
            innerHTML: '',
            querySelectorAll() { return []; },
            querySelector() { return null; },
            classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } }
        };
    },
    createElement(tag) { return { addEventListener() {}, style: {} }; },
    addEventListener(e, fn) {}
};

const sandbox = {
    window: { localStorage: { getItem() { return 'theme-dark'; }, setItem() {} } },
    document: mockDocument,
    localStorage: { getItem() { return 'theme-dark'; }, setItem() {} },
    console: console,
    setTimeout: (fn) => fn()
};

sandbox.global = sandbox;
sandbox.window.window = sandbox.window;
sandbox.window.document = mockDocument;

const context = vm.createContext(sandbox);

try {
    vm.runInContext(jsCode, context);
} catch(err) {
    console.error("vm.runInContext EXCEPTION:", err.message, err.stack);
}
