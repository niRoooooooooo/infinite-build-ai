# Demo Flow

**Project:** Contextual Ad Intelligence Engine (Bangladesh-focused)
**Format:** Live demo (or recorded)
**Total time:** ~5 minutes (with cut-to-time markers)
**Audience:** Hackathon judges
**This document:** Demo choreography only — clicks, screens, transitions. No scripted dialogue.

---

## Pre-Demo Setup (Before Going Live)

### Browser tabs ready
- **Tab 1:** Interface B — Brand Grid page (`/brand`)
- **Tab 2:** Interface A — Consumer Feed page (`/consumer`)
- Keep both tabs loaded and ready

### Persona pre-selected in Tab 2
- Active persona: **Rafi** (22, Dhaka, student)

### Brand pre-selected in Tab 1
- Default to grid view, with **Pran** block visible

### Pre-staged elements
- A test product image file ready to upload (e.g., new flavor of juice or snack)
- All pre-loaded brands have full data (kits, products, performance)
- 1000+ seeded conversion events already in the database
- The optimization cycle result for one brand pre-cached for instant response

### Browser settings
- Zoom level: 100% (or 110% if room is large)
- Notifications disabled
- Bookmarks bar hidden
- Use full screen mode

### Backup ready
- Screenshot of every key screen saved locally
- Pre-recorded 30-second video of the optimization cycle running (in case the live cycle fails)
- Pre-rendered ad images for each persona-brand pair (in case generation API hangs)

---

## Act 1 — Opening Hook (30 seconds)

**Goal:** Show what the system *does* in the first 10 seconds.

### Screen: Interface B → Pran brand detail page → Generate Ad panel

### Sequence:

1. Start on Pran's brand detail page (Interface B)
2. Scroll to the "Generate ad now" panel
3. Select **Rafi** (22, Dhaka, student) + select a Pran product (e.g., Mango Juice)
4. Click **Generate ad**
5. Ad appears in ~3 seconds — playful GIF/image with Banglish copy, hot-weather reference
6. **Pause for 2 seconds** — let judges absorb the ad
7. Without explanation, change persona to **Nusrat** (28, Chittagong, professional)
8. Same product (Mango Juice). Click **Generate ad** again
9. New ad appears — completely different visual, different copy style, different tone
10. **Pause for 3 seconds** — the contrast is the message

### What judges see:
- Two completely different ads for the same product
- No further explanation needed in the first 30 seconds

### Cut-to-time marker:
- If running over: skip the second ad generation. The first ad alone with mention of "for a different user it would be different" suffices.

### Backup:
- If generation hangs: pre-rendered ads for both personas ready as image files. Drop them in via the "show pre-rendered" toggle (build this as a hidden dev feature).

---

## Act 2 — Behind the System: Interface B Tour (45 seconds)

**Goal:** Show the brand-side architecture. Establish the multi-tenant story.

### Screen: Interface B → Brand Grid → Brand Detail

### Sequence:

1. Navigate back to **Brand Grid page**
2. **Pause for 3 seconds** — let judges scan the 5 brand cards
3. Hover over each brand briefly (not clicking) — Pran, Daraz, Foodpanda, bKash, local brand
4. Click into **Pran's block** to expand to detail page
5. Brief tour of the three sections:
   - **Identity section** (5 sec) — Show logo, tagline, voice description, brand colors
   - **Products section** (10 sec) — Show 4 products with images. Hover one to show "Generate ad" button
   - **Performance section** (15 sec) — Highlight the headline number: **"89 customers acquired this week"**. Then point to top-performing ad and segment breakdown

### What judges see:
- Multiple brands using the system
- Each brand has structured data: identity, products, performance
- Attribution-first metric ("customers acquired") not vanity metrics

### Cut-to-time marker:
- If running over: skip Daraz/Foodpanda/bKash hover. Go straight from grid to Pran detail.

### Visual emphasis:
- The "89 customers acquired this week" number should be visually large and prominent. This is the business value in 3 words.

---

## Act 3 — Live Product Upload (60 seconds)

**Goal:** Prove the system is real, not faked. Show the brand-side workflow.

### Screen: Interface B → Pran → Products section → Upload Form

### Sequence:

1. Click **+ Add product** tile in Pran's products grid
2. Upload form opens
3. Fill the form (have these values pre-memorized):
   - **Name:** "Pran Lemon-Mint Cooler" (or whatever fits your test image)
   - **Category:** Beverage
   - **Description:** "New summer drink, refreshing citrus-mint blend, perfect for hot afternoons"
   - **Image:** Click upload, select the pre-staged test image
4. Image preview appears
5. Click **Add product**
6. Form closes — new product card appears in the grid with the uploaded image
7. **Pause for 2 seconds** — confirm to judges this is real
8. Click **Generate ad** on the new product card
9. Pick persona: **Rafi**
10. Wait ~5 seconds for generation
11. Ad appears — uses the uploaded product image, generates contextual copy
12. Open the **Why this ad?** panel below the generated ad
13. Show the reasoning: format, style, tone, mode, confidence

### What judges see:
- A new product enters the system live
- The system immediately generates an ad for it
- The ad uses the actual uploaded image
- The system explains its creative choices

### Cut-to-time marker:
- If running over: skip the "Why this ad?" panel expansion. Just show the generated ad.

### Backup:
- If image upload fails: have a backup product already prepared in the database, "find" it instead and generate the ad from it.
- If generation hangs: pre-rendered ad for the test product, drop in via dev toggle.

### Critical practice point:
- Practice this upload 10+ times before demo. The form filling should be smooth, no typos. Image file location memorized.

---

## Act 4 — The Consumer View: Interface A (45 seconds)

**Goal:** Show what the user actually sees. Make the ad placement believable.

### Screen: Tab switch to Interface A → Feed page

### Sequence:

1. Switch to **Interface A** tab
2. Confirm active persona is **Rafi** (shown in header)
3. **Pause for 2 seconds** — let judges see the feed format
4. Scroll down through the feed slowly
5. Pass an organic content card, an organic content card
6. Reach a **sponsored Pran ad** (the same brand from earlier)
7. **Pause** — point out the "Sponsored" tag, the brand logo, the native feel
8. Click the ad's **Take the offer** button
9. Button changes to "Offer claimed" confirmation
10. Scroll a bit further — show another sponsored ad from a different brand (Daraz or Foodpanda) appearing naturally in the feed

### What judges see:
- Sponsored ads embedded naturally in feed, not as banners
- Native styling (sponsored looks like organic, with honest "Sponsored" tag)
- Click-to-convert interaction is simple and direct
- Multiple brands compete for slots in one user's feed

### Cut-to-time marker:
- If running over: skip the second brand ad. Just demonstrate one Take-the-offer click.

### Backup:
- If feed doesn't load: have screenshots of the feed ready as static images.

---

## Act 5 — The Attribution Loop (30 seconds)

**Goal:** Prove the system is wired end-to-end. Click in A → updates in B.

### Screen: Tab switch back to Interface B → Pran's performance section

### Sequence:

1. Switch back to **Interface B** tab
2. The Pran brand detail page should still be open
3. **Pause for 2 seconds** — let the performance section refresh (polling)
4. Point to the "customers acquired" counter: it has incremented (89 → 90)
5. Point to the Top Ads list: the ad Rafi just took is now listed (or its conversion rate increased)
6. Briefly explain: "Rafi just became a customer. The system knows which ad brought him."

### What judges see:
- Direct cause-and-effect: click in one interface, see the impact in another
- The attribution story is concrete, not abstract
- "Customer acquired through ad" is a measured outcome, not a guess

### Cut-to-time marker:
- This act is short already — don't cut.

### Backup:
- If polling doesn't update fast enough: manually click a "Refresh" button (have one ready in the UI).
- Worst case: have a screenshot of the "after" state ready to show.

---

## Act 6 — The Intelligence: Optimization Cycle (60 seconds — THE CLIMAX)

**Goal:** Show that the system learns. This is your biggest wow moment.

### Screen: Interface B → Pran brand detail page → Optimization section

### Sequence:

1. Scroll to the **Optimization** section on Pran's detail page
2. Show the **Run weekly optimization cycle** button
3. **Pause for 2 seconds** — set up the moment
4. Click the button
5. Progress indicator runs through 4 steps:
   - "Extracting user patterns..."
   - "Aggregating insights..."
   - "Reshaping libraries..."
   - "Generating recommendations..."
6. Results panel appears: "Analyzed 1,247 events. Updated 5 user profiles. Generated 12 recommendations."
7. **Pause for 3 seconds** — let judges see what happened
8. Scroll to recommendations: show 2-3 plain-language recommendations (e.g., "Generate more GIF + joke combos for young Dhaka users")
9. Now demonstrate the learning visually:
10. Scroll back to **Generate ad now** panel
11. Same Rafi + same Pran product as before
12. Click **Generate ad**
13. New ad appears — visibly different from the Act 1 ad
14. Open **Why this ad?** panel
15. Show that the system now references learned patterns: "Top performer for this user. Confidence 78% based on 23 prior interactions."
16. **Pause for 3 seconds** — the contrast with Act 1's ad is the message

### What judges see:
- The system runs an optimization cycle live
- Concrete output (events processed, profiles updated)
- The next generated ad is informed by what was learned
- The system can explain its choices

### Cut-to-time marker:
- If running over: skip the recommendations scroll. Go straight from cycle complete → generate next ad.

### Backup:
- The cycle result is pre-cached so the button click feels instant.
- If the post-cycle ad generation hangs: pre-rendered post-optimization ad ready.

### Critical messaging point:
- This act answers Track 5's judging criteria. Make sure the "the system gets smarter" moment lands clearly.

---

## Act 7 — Closing: Persona Contrast + Future (30 seconds)

**Goal:** Final differentiation moment + forward-looking pitch beat.

### Screen: Interface A → Persona switcher → Feed

### Sequence:

1. Switch to **Interface A** tab
2. Click persona switcher → change to **Nusrat** (28, Chittagong, professional)
3. Feed refreshes — visibly different ads appear
4. **Pause for 3 seconds** — same brands, completely different ads for a different person
5. Scroll briefly to show 2-3 different ads
6. **Don't click anything** — let the visual contrast with Rafi's feed do the work
7. Optional: switch one more time to a third persona (Karim, 45) for a 3-way contrast
8. End on the feed view — leave the visual on screen as the closing image

### What judges see:
- The system serves wildly different ads to different people
- Bangladesh-specific intelligence is visible (city, language, age-appropriate)
- The product is real and works for any persona

### Cut-to-time marker:
- If running over: skip the third persona. Two contrasts (Rafi → Nusrat) suffice.

### Closing visual:
- End with a different-persona feed on screen. Don't navigate back to dashboards or "thank you" slides.

---

## Total Timeline

| Act | Duration | Cumulative |
|---|---|---|
| 1 — Opening Hook | 30s | 0:30 |
| 2 — Interface B Tour | 45s | 1:15 |
| 3 — Live Product Upload | 60s | 2:15 |
| 4 — Consumer View | 45s | 3:00 |
| 5 — Attribution Loop | 30s | 3:30 |
| 6 — Optimization Cycle (climax) | 60s | 4:30 |
| 7 — Closing Contrast | 30s | 5:00 |

**Total: 5:00 minutes**

### If you only have 3 minutes (compressed version):
- Cut Act 4 (Consumer View) to 20 seconds
- Cut Act 5 (Attribution Loop) entirely
- Cut Act 7 down to 15 seconds
- New total: ~3:00

### If you only have 2 minutes (extreme cut):
- Keep Act 1 (Opening Hook)
- Keep Act 3 (Product Upload) — compressed to 40s
- Keep Act 6 (Optimization Cycle) — the climax
- Total: ~1:50

---

## Demo Day Checklist

### 1 hour before demo
- [ ] Both browser tabs open and loaded
- [ ] Backend running and healthy (check all API endpoints)
- [ ] Database seeded with all events, brands, personas, ads
- [ ] Test product image file on the demo laptop's desktop
- [ ] Pre-cached optimization cycle result confirmed
- [ ] All backup screenshots saved locally
- [ ] Backup video of optimization cycle ready

### 15 minutes before demo
- [ ] Run through Acts 1, 3, and 6 once as a final test
- [ ] Confirm "customers acquired" counter resets if needed (start at a clean number)
- [ ] Browser zoom set correctly
- [ ] Full screen mode on
- [ ] Notifications off
- [ ] Battery plugged in
- [ ] Water nearby

### 1 minute before demo
- [ ] Both tabs open to their starting screens (Act 1 → Pran detail; Tab 2 → Feed with Rafi)
- [ ] Mouse positioned over the first click target
- [ ] Take one deep breath

---

## Risk Mitigation

### Top failure scenarios and responses

| What fails | Response |
|---|---|
| Image upload hangs | "Let me show this with a backup product already in the system" — switch to a pre-loaded product, continue |
| Ad generation API hangs (>10 sec) | "While the system processes, here's an example of what gets generated" — show pre-rendered ad |
| Optimization cycle fails | "We have the cycle output ready — let me walk you through what it produced" — switch to pre-recorded video or static result |
| Frontend crashes | Refresh the page, jump to the next act |
| Internet goes down | Switch to fully recorded demo video (have one ready) |

### Do not under any circumstances
- Apologize or explain the failure in detail — pivot smoothly and keep moving
- Mention "this is a hackathon MVP" defensively — the judges know
- Show error messages on screen — close them immediately

---

## What NOT to Demo

These exist in the system but waste time on stage:

- Detailed API/data source explanations (judges don't care)
- The brand registration form (slower than product upload, less impressive)
- Multiple persona switches beyond 2-3 (diminishing returns)
- The full dashboard breakdown (one headline number is enough)
- Privacy/ethical statement explanations (mention only if asked)
- The technical architecture diagram (show only if asked in Q&A)
- The full code structure or repo (irrelevant during demo)

---

## What to Have Ready for Q&A (Not in the Demo)

Judges often have 1-3 minutes of questions after demos. Anticipate:

| Question | Have ready |
|---|---|
| "How does this scale?" | One slide showing API + multi-tenant architecture |
| "What's the business model?" | One slide: per-brand SaaS subscription + per-conversion fee |
| "Who's the first customer?" | A specific named brand or category (e.g., "Bangladeshi food delivery apps") |
| "How is this different from Jasper/Persado?" | Three points: local context intelligence, conversion-tied learning, multi-channel native delivery |
| "How do you handle privacy?" | The privacy statement from Document 1, Section 7 — first-party data only, no inferred sensitive attributes |
| "What's next?" | V2 roadmap: dynamic placement in video content, brand bidding for ad slots, deeper integration with paid ad networks |

Have these as a small slide deck open in a third tab — don't open during the demo, open if needed in Q&A.

---

## Rehearsal Plan

### Day 3 (final day before submission)

**Rehearsal 1 (morning):** Full run-through. Time it. Note where it lags.
**Rehearsal 2 (midday):** Run-through with intentional disruptions — simulate API failures, force backup activations.
**Rehearsal 3 (afternoon):** Final timing pass. Confirm 5:00 total.
**Rehearsal 4 (evening):** One last walk-through. Don't change anything after this.

**Do not modify the demo flow on demo day.** Whatever works in rehearsal is what you ship.
