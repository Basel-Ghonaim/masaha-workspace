# Start a new main-supervisor conversation

Open a new Claude Code conversation in `C:\dev\masaha\app` (Opus 5.5; the effort the owner picks) and paste:

```
Read C:\dev\masaha\workspace\HANDOFF.md whole, then C:\dev\masaha\workspace\BOARD.md, then C:\dev\masaha\workspace\REFACTOR_NOTES.md, then the 0_OWNER_DECISIONS.md of each active task: C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\, C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\, C:\dev\masaha\workspace\TASKS\IDENTITY\. You are the main supervisor; reply to me in plain Arabic with technical terms in English, never editing the repository unless I say so. Start from sections 2 and 2a: main = 40cb481d (#137); DIRECTORY_PROD's executor is building PR #138 in app; SPACE_PROFILE's prototype worker runs in app-design; the palette lab is in app-b; the women + evening task waits for #138's merge. Check each worktree's state yourself (git status, git log, gh pr list), give me a short state in Arabic, and ask which of the active tasks I want to follow first.
```
