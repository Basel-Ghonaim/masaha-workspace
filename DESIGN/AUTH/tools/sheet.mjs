// sheet — a contact sheet of captures, as one HTML page shot by shoot.mjs: node sheet.mjs <dir> <prefix> <out.html> [cols]
import { readdirSync, writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { join } from 'node:path';
const [dir, prefix, out, cols = '7'] = process.argv.slice(2);
const files = readdirSync(dir).filter((f) => f.startsWith(prefix) && f.endsWith('.png')).sort();
const cells = files.map((f) => `<figure><figcaption>${f.replace('.png', '')}</figcaption><img src="${pathToFileURL(join(dir, f)).href}"></figure>`).join('');
writeFileSync(out, `<!doctype html><meta charset=utf-8><style>body{margin:0;padding:12px;background:#ddd;font:12px system-ui}main{display:grid;grid-template-columns:repeat(${cols},1fr);gap:10px;align-items:start}figure{margin:0}img{width:100%;display:block;background:#fff}figcaption{padding:2px 0}</style><main>${cells}</main>`);
console.log(files.length);
