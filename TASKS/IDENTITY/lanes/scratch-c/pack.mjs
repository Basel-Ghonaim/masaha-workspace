// Packs PNGs into an .ico: ICONDIR (reserved 0, type 1, count), a 16-byte ICONDIRENTRY per image
// (width, height, 0 colours, 0, planes 1, 32 bits, the PNG's size, its offset), then the PNGs.
//   node pack.mjs <out.ico> <a.png> [<b.png> …]
import { readFileSync, writeFileSync } from 'node:fs';

const [target, ...sources] = process.argv.slice(2);
const pngs = sources.map((path) => readFileSync(path));
const header = Buffer.alloc(6 + 16 * pngs.length);
header.writeUInt16LE(0, 0);
header.writeUInt16LE(1, 2);
header.writeUInt16LE(pngs.length, 4);
let offset = header.length;
pngs.forEach((png, index) => {
  if (png.toString('latin1', 12, 16) !== 'IHDR') throw new Error(`${sources[index]} is not a PNG`);
  const [width, height] = [png.readUInt32BE(16), png.readUInt32BE(20)];
  const entry = 6 + 16 * index;
  header.writeUInt8(width >= 256 ? 0 : width, entry);
  header.writeUInt8(height >= 256 ? 0 : height, entry + 1);
  header.writeUInt8(0, entry + 2);
  header.writeUInt8(0, entry + 3);
  header.writeUInt16LE(1, entry + 4);
  header.writeUInt16LE(32, entry + 6);
  header.writeUInt32LE(png.length, entry + 8);
  header.writeUInt32LE(offset, entry + 12);
  offset += png.length;
  console.log(`${sources[index]}: ${width} x ${height}, ${png.length} bytes`);
});
writeFileSync(target, Buffer.concat([header, ...pngs]));
console.log(`${target}: ${offset} bytes, ${pngs.length} images`);
