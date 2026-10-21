// Checks that the demo accounts accept the .env's demo password; prints only the status codes.
import { OWNER, RECEPTION } from './common3.mjs';

for (const [who, account] of [['owner', OWNER], ['reception', RECEPTION]]) {
  const answer = await fetch('http://localhost:5320/api/v1/auth/login', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: account.email, password: account.password }),
  });
  console.log(who, answer.status);
}
