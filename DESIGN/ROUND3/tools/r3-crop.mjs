// r3-crop — cuts an issue's capture out of a pack frame (no dependency: a small PNG reader and writer
// over node:zlib). Optionally draws a red box around the defect so the capture shows where to look.
// Usage:
//   node r3-crop.mjs <frame.png> <out.png> <x> <y> <w> <h> [--mark x,y,w,h] [--scale 2]
// x, y, w, h are in the frame's own pixels (the facts JSON gives element positions; a full.png's y is
// the page's). --mark is in the same pixels and must lie inside the crop. --scale enlarges small crops.
// e.g. node r3-crop.mjs ..\pack\PU\frames\PU-03-390-ar-light.full.png ..\shots\issues\R3-PU-007.png 0 1200 390 300 --mark 16,1260,120,44
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import { inflateSync, deflateSync } from 'node:zlib';

const [src, out, ...rest] = process.argv.slice(2);
const nums = rest.filter((a) => /^-?\d+$/.test(a)).map(Number);
const opt = (n) => { const i = rest.indexOf('--' + n); return i >= 0 ? rest[i + 1] : null; };
if (!src || !out || nums.length < 4) { console.error('usage: node r3-crop.mjs <frame.png> <out.png> <x> <y> <w> <h> [--mark x,y,w,h] [--scale 2]'); process.exit(2); }

const buf = readFileSync(src);
let pos = 8, W = 0, H = 0, depth = 0, ctype = 0, interlace = 0; const idat = [];
while (pos < buf.length) {
  const len = buf.readUInt32BE(pos); const type = buf.toString('ascii', pos + 4, pos + 8); const data = buf.subarray(pos + 8, pos + 8 + len);
  if (type === 'IHDR') { W = data.readUInt32BE(0); H = data.readUInt32BE(4); depth = data[8]; ctype = data[9]; interlace = data[12]; }
  else if (type === 'IDAT') idat.push(data);
  else if (type === 'IEND') break;
  pos += 12 + len;
}
if (depth !== 8 || interlace || ![2, 6].includes(ctype)) { console.error(`unsupported PNG (depth ${depth}, colour type ${ctype}, interlace ${interlace})`); process.exit(1); }
const bpp = ctype === 6 ? 4 : 3, stride = W * bpp;
const raw = inflateSync(Buffer.concat(idat));
const px = Buffer.alloc(H * stride);
for (let y = 0; y < H; y++) {
  const f = raw[y * (stride + 1)], line = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1));
  const prev = y ? px.subarray((y - 1) * stride, y * stride) : Buffer.alloc(stride), cur = px.subarray(y * stride, (y + 1) * stride);
  for (let i = 0; i < stride; i++) {
    const a = i >= bpp ? cur[i - bpp] : 0, b = prev[i], c = i >= bpp ? prev[i - bpp] : 0;
    let v = line[i];
    if (f === 1) v += a; else if (f === 2) v += b; else if (f === 3) v += (a + b) >> 1;
    else if (f === 4) { const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c); v += pa <= pb && pa <= pc ? a : pb <= pc ? b : c; }
    cur[i] = v & 255;
  }
}
let [x, y, w, h] = nums;
x = Math.max(0, Math.min(x, W - 1)); y = Math.max(0, Math.min(y, H - 1)); w = Math.min(w, W - x); h = Math.min(h, H - y);
const scale = Math.max(1, Math.min(4, Number(opt('scale') || 1)));
const OW = w * scale, OH = h * scale;
const outPx = Buffer.alloc(OW * OH * 4);
for (let j = 0; j < OH; j++) for (let i = 0; i < OW; i++) {
  const s = ((y + Math.floor(j / scale)) * W + (x + Math.floor(i / scale))) * bpp, d = (j * OW + i) * 4;
  outPx[d] = px[s]; outPx[d + 1] = px[s + 1]; outPx[d + 2] = px[s + 2]; outPx[d + 3] = bpp === 4 ? px[s + 3] : 255;
}
const mark = opt('mark');
if (mark) {
  const [mx, my, mw, mh] = mark.split(',').map(Number);
  const L = (mx - x) * scale, T = (my - y) * scale, R = (mx - x + mw) * scale, B = (my - y + mh) * scale, t = 3;
  const put = (i, j) => { if (i < 0 || j < 0 || i >= OW || j >= OH) return; const d = (j * OW + i) * 4; outPx[d] = 230; outPx[d + 1] = 0; outPx[d + 2] = 0; outPx[d + 3] = 255; };
  for (let i = L - t; i <= R + t; i++) for (let k = 0; k < t; k++) { put(i, T - t + k); put(i, B + k); }
  for (let j = T - t; j <= B + t; j++) for (let k = 0; k < t; k++) { put(L - t + k, j); put(R + k, j); }
}
const rows = Buffer.alloc(OH * (OW * 4 + 1));
for (let j = 0; j < OH; j++) { rows[j * (OW * 4 + 1)] = 0; outPx.copy(rows, j * (OW * 4 + 1) + 1, j * OW * 4, (j + 1) * OW * 4); }
const crcTable = Array.from({ length: 256 }, (_, n) => { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; return c >>> 0; });
const crc = (b) => { let c = 0xffffffff; for (const v of b) c = crcTable[(c ^ v) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
const chunk = (type, data) => { const l = Buffer.alloc(4); l.writeUInt32BE(data.length); const td = Buffer.concat([Buffer.from(type, 'ascii'), data]); const c = Buffer.alloc(4); c.writeUInt32BE(crc(td)); return Buffer.concat([l, td, c]); };
const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(OW, 0); ihdr.writeUInt32BE(OH, 4); ihdr[8] = 8; ihdr[9] = 6;
mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ihdr), chunk('IDAT', deflateSync(rows)), chunk('IEND', Buffer.alloc(0))]));
console.log(`${out}: ${OW}x${OH} from ${src} (${x},${y} ${w}x${h})${mark ? ' marked' : ''}`);
