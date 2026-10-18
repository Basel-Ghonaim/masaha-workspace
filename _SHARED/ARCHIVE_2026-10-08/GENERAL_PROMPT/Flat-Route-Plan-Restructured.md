# Flat Route Reform — Commit-Staged Repair Plan

---

## Goal

Refactor nested API routes into flatter resource-oriented routes while keeping every commit internally consistent and verifiable.

---

## Scope

- Backend route / controller / service / repository changes.
- API contract and backend docs updates.
- **No** Prisma schema or migration changes.
- **No** active frontend implementation changes unless endpoint consumers already exist.

> **Breaking Change Notice:** This is a breaking API contract change — old nested routes should return `404` after the final backend reform.

---

## Key Repairs to Original Plan

- Do not change `app.ts` mounts before validators/controllers are compatible.
- Do not change follow route paths before moving follows to `/api/v1/follows`.
- Add `GET /tweets?author=username` **before** removing `GET /users/:username/tweets`.
- Treat documentation and API contract as part of the change, not an afterthought.
- Use stronger verification than `tsc` only.

---

## Final Execution Order

Execute the stages in the following order. Each commit is coherent — no stage depends on a later stage to make the server functional.

| # | Commit |
|---|--------|
| 1 | `refactor(comments): flatten comment routes` |
| 2 | `refactor(follows): mount follows as standalone resource` |
| 3 | `feat(tweets): support author-filtered tweet feed` |
| 4 | `refactor(users): remove user tweets endpoint` |
| 5 | `docs(api): document flat route reform` |
| 6 | `test(server): add flat route smoke coverage` *(optional, only if adding smoke coverage)* |

---

## Stage 1 — Flatten Comments Atomically

**Commit:** `refactor(comments): flatten comment routes`
**Covers original issues:** 1, 2, 3, 4, part of 8

### Files

- `server/src/modules/comments/comment.routes.ts`
- `server/src/modules/comments/comment.validator.ts`
- `server/src/modules/comments/comment.controller.ts`
- `server/src/modules/comments/comment.types.ts`
- `server/src/modules/comments/comment.service.ts`
- `server/src/modules/comments/comment.repository.ts`
- `server/src/app.ts`

### Changes

- Mount comments at `/api/v1/comments`.
- Remove `Router({ mergeParams: true })`.
- Change comment mutation params from `:commentId` to `:id`.
- Move `tweetId` to:
  - **query** for `GET /comments?tweetId=X`
  - **body** for `POST /comments`
- Update controller to stop reading `req.params.tweetId`.
- Remove `tweetId` from comment update/delete service signatures.
- Remove `owner.tweetId !== tweetId` check — flat update/delete routes no longer receive tweet context.
- Keep `tweetId` in comment response DTO and create/list logic.

### Final Routes After This Stage

```
GET    /api/v1/comments?tweetId=X
POST   /api/v1/comments
PATCH  /api/v1/comments/:id
DELETE /api/v1/comments/:id
```

### Verification

**Build check:**
```
npm run build --prefix server
```

**Manual checks:**

| Method | Endpoint | Body / Notes |
|--------|----------|--------------|
| `GET` | `/api/v1/comments?tweetId=1` | — |
| `POST` | `/api/v1/comments` | `{ "tweetId": 1, "body": "Nice" }` |
| `PATCH` | `/api/v1/comments/1` | `{ "body": "Updated" }` |
| `DELETE` | `/api/v1/comments/1` | — |
| `GET` | `/api/v1/tweets/1/comments` | **Must return `404`** |

---

## Stage 2 — Flatten Follow Routes Atomically

**Commit:** `refactor(follows): mount follows as standalone resource`
**Covers original issues:** 5, part of 8

### Files

- `server/src/modules/follows/follow.routes.ts`
- `server/src/modules/follows/follow.controller.ts` *(comments only if needed)*
- `server/src/app.ts`

### Changes

- Mount follows at `/api/v1/follows`.
- Remove `Router({ mergeParams: true })`.
- Change routes:
  - `POST /users/:username/follow` → `POST /follows/:username`
  - `DELETE /users/:username/follow` → `DELETE /follows/:username`
  - `GET /users/:username/followers` → `GET /follows/:username/followers`
  - `GET /users/:username/following` → `GET /follows/:username/following`
- Split app registration:
  - `/api/v1/users` → only gets `userRoutes`
  - `/api/v1/follows` → gets `followRoutes`

### Final Routes After This Stage

```
POST   /api/v1/follows/:username
DELETE /api/v1/follows/:username
GET    /api/v1/follows/:username/followers
GET    /api/v1/follows/:username/following
```

### Verification

**Build check:**
```
npm run build --prefix server
```

**Manual checks:**

| Method | Endpoint | Notes |
|--------|----------|-------|
| `POST` | `/api/v1/follows/basel` | — |
| `DELETE` | `/api/v1/follows/basel` | — |
| `GET` | `/api/v1/follows/basel/followers` | — |
| `GET` | `/api/v1/follows/basel/following` | — |
| `POST` | `/api/v1/users/basel/follow` | **Must return `404`** |

---

## Stage 3 — Add Author-Filtered Tweet Feed

**Commit:** `feat(tweets): support author-filtered tweet feed`
**Covers original issue:** 6

### Files

- `server/src/modules/tweets/tweet.validator.ts`
- `server/src/modules/tweets/tweet.routes.ts`
- `server/src/modules/tweets/tweet.controller.ts`
- `server/src/modules/tweets/tweet.types.ts`
- `server/src/modules/tweets/tweet.service.ts`
- `server/src/modules/tweets/tweet.repository.ts`

### Changes

- Add tweet-specific `feedQuerySchema`.
- Keep shared `cursorQuerySchema` unchanged.
- Add optional `author` query param.
- Update `GET /tweets` to support:
  - **Global feed:** `GET /tweets`
  - **Author tweets:** `GET /tweets?author=username`
- Add `getByAuthorUsername` to tweet service.
- Add `findAuthorIdByUsername` to tweet repository.
- Preserve `404 User not found` behavior when `author` username does not exist.
- Avoid self-reference inside `createTweetService`; use a local helper or call repository methods directly.

### Final Routes After This Stage

```
GET /api/v1/tweets
GET /api/v1/tweets?author=basel
```

### Verification

**Build check:**
```
npm run build --prefix server
```

**Manual checks:**

| Method | Endpoint | Notes |
|--------|----------|-------|
| `GET` | `/api/v1/tweets` | — |
| `GET` | `/api/v1/tweets?author=basel` | — |
| `GET` | `/api/v1/tweets?author=unknown_user` | **Must return `404`** |
| `GET` | `/api/v1/users/basel/tweets` | **Must still work in this stage** |

---

## Stage 4 — Remove User Tweets Endpoint

**Commit:** `refactor(users): remove user tweets endpoint`
**Covers original issue:** 7

### Files

- `server/src/modules/users/user.routes.ts`
- `server/src/modules/users/user.controller.ts`
- `server/src/modules/users/user.service.ts`
- `server/src/modules/users/user.types.ts`
- `server/src/modules/users/user.repository.ts`

### Changes

- Remove `GET /users/:username/tweets`.
- Remove `controller.getUserTweets`.
- Remove `service.getUserTweets`.
- Remove tweet service dependency from user service.
- Remove unused tweet-related imports.
- Remove `findIdByUsername` from user repository **only if nothing else uses it**.

### Final User Route

```
GET /api/v1/users/:username
```

### Replacement Route

```
GET /api/v1/tweets?author=:username
```

### Verification

**Build check:**
```
npm run build --prefix server
```

**Manual checks:**

| Method | Endpoint | Notes |
|--------|----------|-------|
| `GET` | `/api/v1/users/basel` | — |
| `GET` | `/api/v1/tweets?author=basel` | — |
| `GET` | `/api/v1/users/basel/tweets` | **Must return `404`** |

---

## Stage 5 — Sync API Contract and Docs

**Commit:** `docs(api): document flat route reform`
**Covers original issue:** 9

### Files

- `server/docs/api-contract.md`
- `server/docs/setup-log.md`
- `server/docs/issues.md`
- Any touched route/controller JSDoc comments

### Changes

- Update final endpoint map.
- Replace nested comments docs with flat comments docs.
- Replace user-scoped follow docs with `/follows`.
- Remove user tweets endpoint docs.
- Document `GET /tweets?author=username`.
- Add migration note: old nested routes intentionally return `404`.
- Fix rationale wording:
  - Do **not** say "RTK Query requires flat URLs."
  - Say "flat routes simplify client cache organization and resource ownership."

### Final Route Map

```
GET    /api/v1/tweets
GET    /api/v1/tweets?author=username
GET    /api/v1/tweets/:id
POST   /api/v1/tweets
PATCH  /api/v1/tweets/:id
DELETE /api/v1/tweets/:id
POST   /api/v1/tweets/:id/like

GET    /api/v1/comments?tweetId=X
POST   /api/v1/comments
PATCH  /api/v1/comments/:id
DELETE /api/v1/comments/:id

GET    /api/v1/users/:username

POST   /api/v1/follows/:username
DELETE /api/v1/follows/:username
GET    /api/v1/follows/:username/followers
GET    /api/v1/follows/:username/following
```

### Verification

**Build check:**
```
npm run build --prefix server
```

**Docs grep checks** *(none of these should remain as active API contract):*

```
/tweets/:tweetId/comments
/users/:username/tweets
/users/:username/follow
```

---

## Stage 6 — Final Route Reform Verification

**Commit:** *(optional — only if adding tests or a smoke script)*
**Suggested commit:** `test(server): add flat route smoke coverage`

### Required Verification Before Merge

**Build checks:**
```
npm run build --prefix server
npm run build
```

**Manual route checks — new flat routes (all must succeed):**

```
GET    /api/v1/tweets
GET    /api/v1/tweets?author=basel
GET    /api/v1/comments?tweetId=1
POST   /api/v1/comments
PATCH  /api/v1/comments/:id
DELETE /api/v1/comments/:id
POST   /api/v1/follows/basel
DELETE /api/v1/follows/basel
GET    /api/v1/follows/basel/followers
GET    /api/v1/follows/basel/following
```

**Old route checks (all must return `404`):**

| Old Route | Expected |
|-----------|----------|
| `GET    /api/v1/tweets/1/comments` | `404` |
| `POST   /api/v1/tweets/1/comments` | `404` |
| `PATCH  /api/v1/tweets/1/comments/1` | `404` |
| `DELETE /api/v1/tweets/1/comments/1` | `404` |
| `GET    /api/v1/users/basel/tweets` | `404` |
| `POST   /api/v1/users/basel/follow` | `404` |
| `DELETE /api/v1/users/basel/follow` | `404` |
