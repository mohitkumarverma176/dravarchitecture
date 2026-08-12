# Drav Architecture — Full UI/UX Revamp Plan

## Design Direction
**Dark & Dramatic Architecture Firm** — inspired by Zaha Hadid Architects, Foster + Partners, BIG (Bjarke Ingels Group)

| Property | Value |
|---|---|
| Primary BG | `#0a0a0a` |
| Surface | `#111111` |
| Surface Elevated | `#1a1a1a` |
| Border | `rgba(255,255,255,0.08)` |
| Text Primary | `#f5f4f0` |
| Text Muted | `rgba(245,244,240,0.45)` |
| Accent | `#fc5404` (orange) |
| Display Font | Cormorant Garamond 300/400/600/italic |
| UI Font | Inter 300/400/500/600/700 |

---

## Libraries
| Library | Source | Purpose |
|---|---|---|
| GSAP 3 | CDN | Premium animations, timeline sequencing |
| ScrollTrigger | CDN (GSAP plugin) | Scroll-driven animations, parallax |
| Bootstrap 5 | existing local | Grid layout only |
| TinySlider | existing local | Hero image slider, testimonial slider |
| AOS | existing local | Fallback scroll reveals |
| GLightbox | existing local | Video lightbox |

---

## Files to Rewrite

| File | Status | Notes |
|---|---|---|
| `static/css/drav-custom.css` | [ ] | Complete rewrite — new dark design system |
| `templates/base.html` | [ ] | GSAP CDN, preloader revamp, new nav (transparent→solid), custom cursor |
| `templates/footer.html` | [ ] | Deep dark, architectural grid layout |
| `templates/index.html` | [ ] | Ken Burns hero slider, all sections redesigned |
| `templates/about.html` | [ ] | Parallax hero, pull-quote, team cards, process timeline |
| `templates/services.html` | [ ] | Full-width alternating service rows, animated process |
| `templates/projects.html` | [ ] | Dark masonry grid, wipe-reveal on scroll |
| `templates/contact.html` | [ ] | Split dark/light layout |
| `templates/project-single.html` | [ ] | Dark editorial single project page |
| `templates/single.html` | [ ] | Dark editorial article page |
| `static/js/custom.js` | [ ] | GSAP init, hero slider, custom cursor, scroll animations |

---

## Page-by-Page Specification

### 1. `drav-custom.css` — Design System
```
:root variables — all new dark tokens
Body defaults — dark bg, warm white text
Typography — display / ui / eyebrow / section-heading / display-heading
Preloader — fullscreen dark with DA logo spin
Custom cursor — small orange dot + large follower ring
Navigation — transparent overlay → solid #111 on scroll, 80px height
Hero — fullscreen (100vh), Ken Burns on each slide
Stats bar — dark strip, large Cormorant numbers
Sections — dark alternating: #0a0a0a / #111111
Cards — sharp corners, dark surface, orange left-border hover
Project grid — 1px gap, wipe-reveal on scroll
Testimonials — dark card, large quote marks, readable body text
CTA banner — full-bleed orange gradient overlay
Forms — dark fields, orange focus ring
Footer — #0a0a0a, architectural column grid
```

### 2. `base.html`
- Add GSAP 3 + ScrollTrigger via CDN (before closing `</body>`)
- Custom cursor HTML: `<div id="cursor-dot"></div><div id="cursor-ring"></div>`
- Preloader: replace Bootstrap spinner with animated `DA` logotype + line reveal
- Nav: add `id="site-nav"` for JS scroll detection; logo becomes wordmark with orange dot
- Mobile nav: full-screen overlay with large stacked links

### 3. `index.html` — Homepage
**Hero:**
- `<div class="hero-slider">` with 3 slides (img_2, img_3, img_5)
- Each slide: `<div class="hero-slide">` with Ken Burns CSS animation (`scale 1.0 → 1.08` over 8s)
- Crossfade transition between slides (TinySlider `mode: 'carousel'`, `speed: 1200`)
- Headline: large split-line text with GSAP stagger reveal from bottom
- CTA buttons fade up after headline
- Scroll indicator: animated vertical line + "scroll" text

**Stats Bar:** Dark strip, numbers use Cormorant Garamond, count-up on scroll

**About Intro:** Dark section, large image right with parallax scroll, text left

**Services Accordion:** Dark background, numbered rows, expands to show image + description

**Projects Grid:** `g-1` tight grid, dark bg, cards reveal with upward wipe on scroll (GSAP)

**Testimonials:** Dark cards, orange quote marks, TinySlider center mode

**CTA:** Full-bleed background with diagonal orange gradient line accent

### 4. `about.html`
**Hero:** Full-bleed with parallax image, large headline reveal

**Philosophy:** Large pull-quote block (Cormorant italic, 2.5rem) on dark bg with orange left border

**Why Us:** 3 dark feature cards, icon + heading + text, orange border bottom on hover

**Stats:** Same dark stats bar

**Process:** Horizontal numbered steps with connecting orange line that draws on scroll (GSAP)

**Team:** 4 cards, portrait images (3/4 ratio), grayscale → color on hover, name + role slide up

**CTA:** Same CTA banner pattern

### 5. `services.html`
**Hero:** Inner page hero, full-bleed

**Services:** Full-width alternating rows:
- Odd: Image left (40%), text right (55%)
- Even: Text left (55%), image right (40%)
- Reveal with GSAP slide-in from sides on scroll

**Process:** 5 numbered steps, horizontal on desktop, orange line connector animates in

**Testimonials:** 3 dark cards, slider

**CTA:** Banner

### 6. `projects.html`
**Header:** Minimal — title + filter buttons (pill style, dark)

**Grid:** Asymmetric 2-col + 3-col rows for visual interest. Cards reveal with curtain-wipe (clip-path `inset(100% 0 0 0)` → `inset(0% 0 0 0)` on scroll)

**Each card:** Image fills frame, overlay gradient always present (subtle), text slides up on hover

**Commitment section:** Dark bg, 3 feature points

**CTA:** Banner

### 7. `contact.html`
**Layout:** True split — left panel dark `#111` (contact info), right panel slightly lighter `#1a1a1a` (form)

**Left panel:** Phone, email, locations, WhatsApp — styled vertically with icon dots

**Right panel:** Form with dark inputs, orange focus outline, submit button full-width

### 8. `project-single.html`
- Dark hero with project image + parallax
- Project meta row (location, category, services, status) — dark strip
- Content split: large image + text
- Related projects grid (dark)
- Testimonials slider
- CTA banner

### 9. `single.html`
- Dark hero with article title
- Article content: dark bg, warm white text, orange blockquote left-border
- Sidebar: dark cards with orange accent links
- CTA banner

### 10. `custom.js` — GSAP Animations
```javascript
// 1. Preloader — fade out with DA reveal
// 2. Custom cursor — dot + ring follow mouse
// 3. Nav scroll — add .scrolled class after 80px
// 4. Hero slider — TinySlider with Ken Burns per slide
// 5. GSAP hero headline — SplitText-style stagger reveal
// 6. GSAP scroll reveals — all [data-reveal] elements
// 7. Parallax images — GSAP ScrollTrigger scrub
// 8. Process line draw — SVG path or width animation
// 9. Stats counter — IntersectionObserver (keep existing logic)
// 10. Project filter — keep existing logic
```

---

## Implementation Order
1. `drav-custom.css` — design system first (all pages depend on this)
2. `base.html` — shell (nav, cursor, preloader, GSAP CDN)
3. `custom.js` — animations
4. `footer.html`
5. `index.html` — most complex page
6. `about.html`
7. `services.html`
8. `projects.html`
9. `contact.html`
10. `project-single.html`
11. `single.html`

---

## What Does NOT Change
- All **content** (text, project names, testimonials, locations, email, phone)
- `app.py` routes — untouched
- Static images — same files
- Flask/Jinja2 template inheritance pattern
- Bootstrap 5 grid system (still used for layout)
- Existing JS libraries (TinySlider, AOS, GLightbox, counter.js)
- Deployment files (Dockerfile, docker-compose.yml)
