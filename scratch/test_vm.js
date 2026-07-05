const fs = require('fs');
const path = require('path');
const vm = require('vm');

const indexPath = path.join(__dirname, '..', 'index.html');
const htmlSource = fs.readFileSync(indexPath, 'utf8');
const scriptMatch = htmlSource.match(/<script>([\s\S]*?)<\/script>/);
let jsCode = scriptMatch[1];

const mockDocument = {
    readyState: 'complete',
    body: { style: {} },
    documentElement: { style: {} },
    getElementById(id) {
        console.log('getElementById:', id);
        return { addEventListener() {}, style: {}, setAttribute() {} };
    },
    createElement(tag) { return { addEventListener() {}, style: {} }; },
    addEventListener(e, fn) {
        console.log('addEventListener:', e);
        if (e === 'DOMContentLoaded') fn();
    }
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

const ctx = vm.createContext(sandbox);
try {
    new vm.Script(jsCode);
    console.log("✅ Script parsed ok!");
    vm.runInContext(jsCode, ctx);
    console.log("✅ Script executed ok!");
} catch(e) {
    console.error("❌ ERROR:", e.message, e.stack);
}
