# Skill Mapping — mobile prototype

Clickable iPhone prototype of [Skill Mapping](https://github.com/Learning-platfrom/SkillMapping). It covers finding expertise, requesting support, the request lifecycle on both sides, feedback, and keeping your profile and skills current.

**Live:** https://gbergengruen.github.io/skill-mapping-prototype/

`index.html` is fully self-contained: no build step, and it works offline.

## Kept in sync with the app

This mirrors `Learning-platfrom/SkillMapping` at commit `057c2d5`.

- **Branding:** "Skill Mapping", UNICEF cyan `#1cabe2`, the warm off-white background and the Network logo.
- **Options and statuses**, copied from `lib/constants.ts` and `components/status-badges.tsx`:
  - Support types
  - Preferred timings
  - Proficiency levels (Beginner → Expert)
  - Availability (Available / Limited / Unavailable, including the rule that an expert at their request limit shows as Limited)
  - Request statuses
- **Search** matches and sorts the way `searchExperts()` does. It has the same filters: All / Available or limited / Available now.
- **Request detail** has:
  - the 4-step progress bar;
  - "Cancel request" for the requester;
  - the expert's actions from `request-actions.tsx`, under My requests → *Requests to me*.
- **Feedback** has the same fields as `feedback-form.tsx`. **My profile** has the same fields as `profile-form.tsx` and `skill-manager.tsx`.
- **Skills:** only a sample of the UNICEF skills catalogue is included. The full catalogue stays in the app.

## Intentionally left out

- Sign-in and password flows
- Admin pages (Activity, Users)
- The editor-only Skills catalogue page
- The app-feedback page

The app uses DM Sans. The prototype uses the system font stack so it keeps working offline.

Two things are simulated:
- When the "autoAccept" prop is on, the expert accepts a new request after about 3.5 seconds.
- A dashed "Prototype: simulate…" button stands in for the expert marking a request as completed.

## Editing

The prototype is a bundled export. Its markup and logic live in `src/template.html`. Everything else inside `index.html` (runtime, React, fonts, iPhone frame) is packed assets and stays as it is.

```bash
python3 scripts/bundle.py unpack   # index.html -> src/template.html (only if index.html changed elsewhere)
# edit src/template.html
python3 scripts/bundle.py pack     # src/template.html -> index.html
python3 -m http.server 8000        # preview at http://localhost:8000
```

Commit both files and push to `main`. GitHub Pages republishes in a minute or two.
