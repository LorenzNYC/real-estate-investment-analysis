# CLAUDE.md — Project Rules & Invariants

Every change must pass enterprise-grade scrutiny. Prioritize correctness, security, observability, and maintainability over speed. If in doubt, ask for clarification or leave as-is. Never assume — verify.

## 1. Non-Negotiable Invariants

- Preserve all business logic exactly unless explicitly instructed to change. Do NOT "optimize" calculations, date handling, permission checks, or revenue-impacting flows.
- Authentication & Authorization: Every endpoint/action MUST use the existing auth system (NextAuth / tRPC middleware / Lucia). Never bypass, mock, or weaken checks. Always validate session/user ID server-side.
- Input Validation: Use Zod schemas on EVERY user input (forms, API params, query strings). Parse with safeParse() and throw AppError on failure. No raw string/number usage.
- Error Handling: Centralized AppError + errorToResponse mapper. NEVER return raw errors/stack traces to client. Log structured errors with context but mask sensitive data.
- Secrets: NEVER hardcode, log, or commit secrets. Use process.env + validation at startup.
- Dependencies: Only add packages after explicit approval. Prefer built-in / existing libs. Pin versions in package.json.

## 2. Architecture & Structure

- Folder structure: Follow T3 / feature-based layout (app/, features/, lib/, components/, server/, utils/). New features go in features/[feature]/ with route handlers, components, hooks, schema, and types.
- Separation of Concerns: Server code stays server-only. No client imports from server/. Use server actions or tRPC for data fetching/mutations.
- tRPC Procedures: Input Zod schema, output inferred type. Use ctx for auth/db. Throw TRPCError on failure (code + message).
- React Server Components: Default to RSC. Use "use client" only when needed (interactivity, hooks).
- State Management: Prefer React hooks / server components. No global stores unless scale demands it (then Zustand with clear boundaries).

## 3. Code Quality

- TypeScript strict mode. No `any`. Exhaustive switch/case. Prefer interfaces over types for public APIs.
- Naming: Functions verbNoun(), components PascalCase, utils camelCase.
- Formatting: Follow project .prettierrc and .eslintrc exactly — do not override.
- JSDoc on public APIs/hooks. Explain WHY for non-obvious logic. No redundant comments.
- Functions < 20 lines preferred. Extract helpers early.

## 4. Testing & Verification

- Before any change: Run existing tests + dev server smoke test.
- New features/endpoints: Add unit tests (Vitest) covering happy path + 3-5 edge cases.
- Critical paths (auth, payments, data mutations): Add integration tests.
- After refactor: Re-run ALL affected tests. Fix before commit.
- Goal: >80% coverage on new/changed code.
- Never mark a task complete without proving it works. Run tests, check logs, demonstrate correctness.

## 5. Security & Performance Checklist

- OWASP Top 10 mitigation: Input sanitization, CSP, rate limiting, secure headers.
- Never return full user objects, passwords, or tokens to client.
- Structured logging (pino), no PII. Levels: debug/info/warn/error.
- Avoid N+1 queries (use include/select). Cache where appropriate (React.cache / unstable_cache).
- Accessibility: ARIA, semantic HTML, keyboard nav.
- Tailwind mobile-first.

## 6. Workflow & Safety

- Commit often, small, atomic. Messages: feat: / fix: / refactor: / test:.
- Never force-push main.
- Before destructive ops (rm, git reset): Pause and confirm with user.
- If uncertainty > medium: Propose plan first, wait for approval.
- If something goes sideways during implementation, STOP and re-plan — don't keep pushing.
- For tasks touching 5+ files: suggest full test run before committing.
- Self-review: Before finalizing, re-read changed code against this file.

## 7. Workflow Orchestration

### Plan Mode
- Enter plan mode for tasks touching 5+ files or requiring architectural decisions.
- Write detailed specs upfront to reduce ambiguity.
- Use plan mode for verification steps, not just building.

### Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding.
- Point at logs, errors, failing tests — then resolve them.
- Zero context switching required from the user.

### Verification Before Done
- Diff behavior between main and your changes when relevant.
- Ask yourself: "Would a staff engineer approve this?"

### Demand Elegance (When It Matters)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: implement the clean solution instead.
- **Tiebreaker: Simplicity wins unless the hacky path creates tech debt.**

## 8. Core Principles

- **Simplicity First**: Make every change as simple as possible. Minimal code impact.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.

## 9. Boundaries

- Do NOT touch files marked `// @legacy-do-not-refactor` unless explicitly asked.
- Domain invariants: See docs/business-rules.md — preserve exactly.
- If conflict with this file: Prioritize this CLAUDE.md over general knowledge.

## 10. Self-Improvement Loop

- After ANY correction from the user: update `tasks/lessons.md` with the pattern.
- Write rules for yourself that prevent the same mistake.
- After major tasks: Suggest updates to this CLAUDE.md if rules were unclear or missing.

## gstack

Use gstack skills for development workflow. Available skills:

- `/plan-ceo-review` - Product/founder review of feature plans
- `/plan-eng-review` - Engineering architecture review
- `/plan-design-review` - Design audit (report only)
- `/design-consultation` - Full design system build
- `/review` - Pre-landing code review, auto-fixes obvious issues
- `/ship` - Run tests, push, open PR
- `/qa` - Browser-based QA testing (requires Chromium)
- `/qa-only` - QA report without code changes
- `/qa-design-review` - Design audit + fixes
- `/retro` - Weekly engineering retrospective
- `/document-release` - Update docs to match shipped changes

Note: Browser-based skills (/browse, /qa, /qa-design-review, /setup-browser-cookies) require Playwright Chromium to be installed. Run `cd .claude/skills/gstack && ./setup` if skills aren't working.

<!-- Last Updated: 2026-03-17 -->
