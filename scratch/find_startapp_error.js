const fs = require('fs');
const path = require('path');
const vm = require('vm');

const indexPath = path.join(__dirname, '..', 'index.html');
const htmlSource = fs.readFileSync(indexPath, 'utf8');
const scriptMatch = htmlSource.match(/<script>([\s\S]*?)<\/script>/);
let jsCode = scriptMatch[1];

// Wrap body of startApp in try/catch block
jsCode = jsCode.replace('function startApp() {', 'function startApp() {\n  try {');
jsCode = jsCode.replace('if (document.readyState === \'loading\') {', '  } catch(err) {\n    console.error("CRITICAL EXCEPTION IN startApp:", err.message, err.stack);\n  }\nif (document.readyState === \'loading\') {');

const elements = {};
function getOrCreateElement(id) {
    if (!elements[id]) {
        elements[id] = {
            id: id,
            innerHTML: '',
            textContent: '',
            value: '',
            className: '',
            style: {},
            listeners: {},
            disabled: false,
            children: [],
            addEventListener(e, fn) { this.listeners[e] = fn; },
            click() { if (this.listeners['click']) this.listeners['click']({ target: this }); },
            setAttribute(k, v) { this[k] = v; },
            getAttribute(k) { return this[k] || null; },
            appendChild(c) { this.children.push(c); },
            querySelectorAll() { return []; },
            querySelector() { return null; },
            classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
            scrollIntoView() {}
        };
    }
    return elements[id];
}

const mockDocument = {
    readyState: 'complete',
    body: getOrCreateElement('body'),
    documentElement: getOrCreateElement('html'),
    getElementById(id) {
        return getOrCreateElement(id);
    },
    createElement(tag) { return getOrCreateElement('elem_' + Math.random()); },
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
    console.log("slide-stage innerHTML len:", elements['slide-stage'] ? elements['slide-stage'].innerHTML.length : 0);
} catch(err) {
    console.error("Outer Script Error:", err.message, err.stack);
}
