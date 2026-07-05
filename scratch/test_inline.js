const fs = require('fs');
const path = require('path');
const vm = require('vm');

const indexPath = path.join(__dirname, '..', 'index.html');
const htmlSource = fs.readFileSync(indexPath, 'utf8');

const scriptMatch = htmlSource.match(/<script>([\s\S]*?)<\/script>/);
const jsCode = scriptMatch[1];

const elements = {};
function getOrCreateElement(id, tag = 'div') {
    if (!elements[id]) {
        elements[id] = {
            id: id,
            tagName: tag.toUpperCase(),
            innerHTML: '',
            textContent: '',
            style: {},
            listeners: {},
            classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
            addEventListener(e, fn) { this.listeners[e] = fn; },
            setAttribute(k, v) { this[k] = v; },
            getAttribute(k) { return this[k] || null; },
            appendChild(c) { if (!this.children) this.children = []; this.children.push(c); },
            querySelectorAll() { return []; },
            querySelector() { return null; },
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
    createElement(tag) { return getOrCreateElement('elem_' + Math.random(), tag); },
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

const ctx = vm.createContext(sandbox);

try {
    const script = new vm.Script(jsCode, { filename: 'inline.js' });
    script.runInContext(ctx);
    console.log('\n==================================================');
    console.log('🎉 Script execution finished with ZERO errors!');
    console.log('✅ slide-stage innerHTML length:', elements['slide-stage'].innerHTML.length);
    console.log('✅ header-title textContent:', elements['header-title'].textContent);
    console.log('✅ total-slide-num textContent:', elements['total-slide-num'].textContent);
    console.log('✅ current-slide-num textContent:', elements['current-slide-num'].textContent);
    console.log('==================================================');
} catch(err) {
    console.error('CRITICAL UNCAUGHT EXCEPTION:', err.message, err.stack);
}
