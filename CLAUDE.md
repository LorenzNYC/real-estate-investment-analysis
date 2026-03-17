# Real Estate Investment Analysis

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
