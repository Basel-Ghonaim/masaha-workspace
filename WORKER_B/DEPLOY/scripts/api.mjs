// The function as Vercel runs it, locally: the root api/index.js (the API's built function.ts) on a
// plain Node http server, port 3321, with app-b's apps/api/.env (masaha_b_dev). Run with
// node --env-file=C:/dev/masaha/app-b/apps/api/.env api.mjs
import { createServer } from 'node:http';

const { default: handler } = await import('file:///C:/dev/masaha/app-b/api/index.js');
createServer(handler).listen(3321, () => console.log(`function on 3321, pid ${process.pid}`));
