// The web as Vercel serves it, locally: apps/web/dist with exactly vercel.json's headers and
// rewrites, read from the file. Files first; /api/* forwarded to the API (the function on 3321, as
// Vercel rewrites it to the function); every other path falls back to index.html. Port 5321.
import { createReadStream, existsSync, readFileSync, statSync } from 'node:fs';
import { createServer, request } from 'node:http';
import { extname, join, normalize } from 'node:path';

const REPO = 'C:/dev/masaha/app-b';
const config = JSON.parse(readFileSync(`${REPO}/vercel.json`, 'utf8'));
const DIST = join(REPO, config.outputDirectory);
const API = { host: '127.0.0.1', port: 3321 };
const PORT = 5321;

// vercel.json's sources: path-to-regexp named wildcards (:path*) or raw regex groups.
const toRegExp = (source) => new RegExp(`^${source.replace(/:\w+\*/g, '.*')}$`);
const headerRules = config.headers.map((rule) => ({ test: toRegExp(rule.source), headers: rule.headers }));
const rewrites = config.rewrites.map((rule) => ({ test: toRegExp(rule.source), destination: rule.destination }));

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
};

createServer((req, res) => {
  const path = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  for (const rule of headerRules) {
    if (rule.test.test(path)) for (const { key, value } of rule.headers) res.setHeader(key, value);
  }
  const file = normalize(join(DIST, path));
  if (file.startsWith(DIST) && existsSync(file) && statSync(file).isFile()) {
    res.setHeader('Content-Type', TYPES[extname(file)] ?? 'application/octet-stream');
    createReadStream(file).pipe(res);
    return;
  }
  const rewrite = rewrites.find((rule) => rule.test.test(path));
  if (rewrite?.destination === '/api') {
    // The function sees the original path (Vercel's rewrite keeps it).
    const upstream = request(
      { ...API, method: req.method, path: req.url, headers: { ...req.headers, 'x-forwarded-for': '127.0.0.1' } },
      (answer) => {
        res.writeHead(answer.statusCode, answer.headers);
        answer.pipe(res);
      },
    );
    upstream.on('error', () => {
      res.statusCode = 502;
      res.end('API unreachable');
    });
    req.pipe(upstream);
    return;
  }
  if (rewrite?.destination === '/index.html') {
    res.setHeader('Content-Type', TYPES['.html']);
    createReadStream(join(DIST, 'index.html')).pipe(res);
    return;
  }
  res.statusCode = 404;
  res.end('Not found');
}).listen(PORT, () => console.log(`web on ${PORT}, pid ${process.pid}`));
