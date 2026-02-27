# Remotion Video Generator — Technical Specification

> SPEC.md — The engineering blueprint for production-ready programmatic video generation.

## 1. System Overview

### Purpose
A ClawHub-installable skill that enables AI agents to generate complete, render-ready Remotion video compositions. The skill provides 20+ templates, 8+ themes, AI generation prompts, and a Gamma-like webapp editor — all enforcing taste-skill design principles.

### Design Philosophy
- **Spring-first animation:** Every motion uses physics-based springs, never linear easing
- **Asymmetric composition:** DESIGN_VARIANCE 8 — offset grids, split screens, massive whitespace
- **Breathing space:** VISUAL_DENSITY 4 — gallery-mode elegance, generous padding
- **Fluid motion:** MOTION_INTENSITY 6 — perpetual micro-interactions, staggered reveals
- **Zero AI slop:** No Inter, no purple glow, no centered heroes, no 3-column cards

## 2. Core Dependencies

```json
{
  "remotion": "^4.0.0",
  "@remotion/cli": "^4.0.0",
  "@remotion/player": "^4.0.0",
  "@remotion/lambda": "^4.0.0",
  "@remotion/tailwind": "^4.0.0",
  "zod": "^3.22.0",
  "@phosphor-icons/react": "^2.1.0",
  "tailwindcss": "^4.0.0"
}
```

### Font Stack (Mandatory)
```
Display/Headlines: Geist (800, tracking: -0.04em)
Subtitles/Labels:  Satoshi (600, tracking: -0.02em)
Body text:         Outfit (400, line-height: 1.6)
Data/Code:         Geist Mono (500, tabular-nums)
```

### Banned Dependencies
- `inter` font — generic AI aesthetic
- `framer-motion` — use Remotion's native `spring()` / `interpolate()`
- `animate.css` — no CSS keyframe libraries
- `lottie-react` — use native SVG animation via Remotion

## 3. Animation Engine Specification

### 3.1 Spring Configurations

```typescript
// ============================================================
// SPRING PRESETS — The physics backbone of all motion
// ============================================================

export const SPRING = {
  // Smooth entrance for text blocks, panels
  GENTLE: { damping: 14, stiffness: 80, mass: 1.0 },

  // Default UI element animation
  STANDARD: { damping: 12, stiffness: 100, mass: 0.8 },

  // Buttons, badges, quick reveals
  SNAPPY: { damping: 15, stiffness: 200, mass: 0.5 },

  // Hero entrances, dramatic reveals
  DRAMATIC: { damping: 8, stiffness: 80, mass: 1.2 },

  // Bouncy overshoot for playful elements
  BOUNCE: { damping: 6, stiffness: 120, mass: 0.6 },

  // Slow, cinematic drift
  CINEMATIC: { damping: 20, stiffness: 40, mass: 1.5 },
} as const;
```

### 3.2 Interpolation Patterns

```typescript
// ============================================================
// EASING CURVES — For interpolate() when springs don't fit
// ============================================================

import { Easing } from 'remotion';

export const EASE = {
  // Smooth deceleration (entrances)
  OUT_EXPO: Easing.out(Easing.exp),

  // Smooth acceleration (exits)
  IN_EXPO: Easing.in(Easing.exp),

  // Symmetric smooth (transitions)
  IN_OUT_CUBIC: Easing.inOut(Easing.cubic),

  // Dramatic slow-start (cinematic)
  IN_OUT_QUART: Easing.inOut(Easing.quad),
} as const;
```

### 3.3 Stagger System

```typescript
// ============================================================
// STAGGER — Sequential reveal orchestration
// ============================================================

export function staggeredSpring(
  frame: number,
  fps: number,
  index: number,
  config: {
    delayPerItem?: number;  // frames between each item (default: 5)
    spring?: SpringConfig;  // spring preset (default: STANDARD)
  } = {}
): number {
  const { delayPerItem = 5, spring: springConfig = SPRING.STANDARD } = config;
  const offset = frame - index * delayPerItem;
  if (offset < 0) return 0;
  return spring({ frame: offset, fps, config: springConfig });
}

// Usage: elements.map((el, i) => {
//   const progress = staggeredSpring(frame, fps, i, { delayPerItem: 4 });
//   return <div style={{ opacity: progress, transform: `translateY(${(1-progress)*30}px)` }} />
// })
```

### 3.4 Scene Transition Engine

```typescript
// ============================================================
// TRANSITIONS — Scene-to-scene motion vocabulary
// ============================================================

export type TransitionType =
  | 'wipe-left' | 'wipe-right' | 'wipe-up' | 'wipe-down'
  | 'dissolve' | 'dissolve-scale'
  | 'curtain-horizontal' | 'curtain-vertical'
  | 'slide-left' | 'slide-right'
  | 'zoom-in' | 'zoom-out'
  | 'liquid-morph'
  | 'iris-open' | 'iris-close';

export interface SceneTransition {
  type: TransitionType;
  durationInFrames: number;  // 15-30 frames typical
  easing?: keyof typeof EASE;
}

// Every scene boundary MUST have a transition.
// Default: 'dissolve' at 20 frames if unspecified.
```

## 4. Template Specification

### 4.1 Template Interface

```typescript
// ============================================================
// TEMPLATE CONTRACT — Every template implements this
// ============================================================

export interface TemplateDefinition {
  id: string;                          // kebab-case unique ID
  name: string;                        // Human-readable name
  description: string;                 // One-line purpose
  category: TemplateCategory;
  aspectRatios: AspectRatio[];         // Supported ratios
  defaultDuration: number;             // Seconds
  minScenes: number;
  maxScenes: number;
  schema: z.ZodType;                   // Props validation
  component: React.FC<TemplateProps>;  // Remotion composition
  thumbnail: string;                   // Preview image path
}

export type TemplateCategory =
  | 'b2b-saas'
  | 'social-ads'
  | 'product'
  | 'corporate'
  | 'creative'
  | 'education'
  | 'events';

export type AspectRatio =
  | '16:9' | '9:16' | '1:1' | '4:5' | '4:3';
```

### 4.2 Scene Structure

```typescript
// ============================================================
// SCENE — The atomic unit of video content
// ============================================================

export interface Scene {
  id: string;
  type: SceneType;
  durationInFrames: number;
  content: SceneContent;
  transition?: SceneTransition;
  background?: BackgroundConfig;
  animation?: AnimationOverride;
}

export type SceneType =
  | 'title'           // Big headline + optional subtitle
  | 'split'           // Two-column content
  | 'showcase'        // Product/feature highlight
  | 'list'            // Staggered bullet points
  | 'quote'           // Testimonial or pull quote
  | 'data'            // Charts, metrics, numbers
  | 'media'           // Full-bleed image or video
  | 'cta'             // Call-to-action closer
  | 'logo-wall'       // Partner/client logos
  | 'comparison'      // Before/after or A vs B
  | 'timeline'        // Sequential events
  | 'code'            // Code snippet with syntax highlight
  | 'blank';          // Custom/freeform

export interface SceneContent {
  headline?: string;
  subheadline?: string;
  body?: string;
  bullets?: string[];
  media?: MediaItem[];
  metrics?: MetricItem[];
  cta?: { label: string; url?: string };
}
```

### 4.3 Template Catalog (22 Templates)

| # | ID | Category | Scenes | Ratios | Description |
|---|-----|----------|--------|--------|-------------|
| 1 | `b2b-showcase` | b2b-saas | 4-8 | 16:9, 1:1 | Enterprise product demo with feature callouts |
| 2 | `saas-demo` | b2b-saas | 5-10 | 16:9 | Screen recording style with UI highlights |
| 3 | `feature-highlight` | b2b-saas | 3-6 | 16:9, 1:1 | Single feature deep-dive with motion graphics |
| 4 | `case-study` | b2b-saas | 4-7 | 16:9 | Client success story with metrics |
| 5 | `social-story` | social-ads | 3-6 | 9:16 | Instagram/TikTok story format |
| 6 | `social-feed` | social-ads | 2-4 | 1:1, 4:5 | Feed-optimized square/portrait |
| 7 | `social-carousel` | social-ads | 4-8 | 1:1 | Multi-slide carousel animation |
| 8 | `tiktok-ad` | social-ads | 3-5 | 9:16 | Fast-paced vertical with text overlays |
| 9 | `product-launch` | product | 5-8 | 16:9, 9:16 | Dramatic reveal with countdown |
| 10 | `product-tour` | product | 4-8 | 16:9 | Guided walkthrough with callouts |
| 11 | `unboxing-reveal` | product | 3-6 | 16:9, 9:16 | Physical product reveal sequence |
| 12 | `company-intro` | corporate | 4-6 | 16:9 | Brand story with values and mission |
| 13 | `team-showcase` | corporate | 3-8 | 16:9 | Team member spotlights |
| 14 | `quarterly-report` | corporate | 5-10 | 16:9 | Data-driven business update |
| 15 | `investor-deck` | corporate | 6-12 | 16:9 | Pitch deck as animated video |
| 16 | `kinetic-typography` | creative | 3-8 | 16:9, 1:1 | Text-as-hero motion piece |
| 17 | `data-visualization` | creative | 4-8 | 16:9 | Animated charts and infographics |
| 18 | `countdown-timer` | creative | 1-3 | 16:9, 1:1, 9:16 | Event countdown with urgency |
| 19 | `explainer-motion` | education | 5-10 | 16:9 | Concept explanation with diagrams |
| 20 | `tutorial-walkthrough` | education | 4-8 | 16:9 | Step-by-step instructional |
| 21 | `comparison-split` | education | 3-6 | 16:9 | Side-by-side A vs B analysis |
| 22 | `event-promo` | events | 3-6 | 16:9, 9:16 | Event announcement with details |

## 5. Theme Specification

### 5.1 Theme Interface

```typescript
// ============================================================
// THEME — Visual identity tokens for video rendering
// ============================================================

export interface ThemeConfig {
  id: string;
  name: string;
  description: string;
  colors: ColorTokens;
  typography: TypographyTokens;
  spacing: SpacingTokens;
  radius: number;
  grain: boolean;           // Film grain overlay
  motion: MotionTokens;
}

export interface ColorTokens {
  bg: string;               // Primary background
  bgAlt: string;            // Secondary background
  fg: string;               // Primary text
  fgMuted: string;          // Secondary text
  accent: string;           // Single accent color
  accentFg: string;         // Text on accent
  surface: string;          // Card/panel surface
  border: string;           // Subtle borders
  gradient?: [string, string]; // Optional gradient pair
}

export interface TypographyTokens {
  displayFamily: string;
  headlineFamily: string;
  bodyFamily: string;
  monoFamily: string;
  scale: number;            // Base multiplier (1.0 = default)
}

export interface MotionTokens {
  defaultSpring: keyof typeof SPRING;
  staggerDelay: number;     // Frames between stagger items
  transitionType: TransitionType;
  transitionDuration: number;
}
```

### 5.2 Theme Catalog (10 Themes)

| # | ID | Base | Accent | Vibe |
|---|-----|------|--------|------|
| 1 | `corporate-blue` | Slate-950 | Blue-500 | Professional, trustworthy |
| 2 | `startup-gradient` | Zinc-950 | Emerald-400→Cyan-400 | Modern, energetic |
| 3 | `luxury-gold` | Neutral-950 | Amber-400 | Premium, exclusive |
| 4 | `dark-tech` | Zinc-950 | Zinc-400 | Minimal, developer-focused |
| 5 | `minimal-white` | White | Zinc-900 | Clean, editorial |
| 6 | `vibrant-pop` | Zinc-50 | Rose-500 | Bold, attention-grabbing |
| 7 | `retro-wave` | Indigo-950 | Fuchsia-400→Orange-400 | Nostalgic, creative |
| 8 | `nature-green` | Stone-950 | Emerald-500 | Organic, sustainable |
| 9 | `warm-earth` | Stone-900 | Orange-500 | Approachable, grounded |
| 10 | `arctic-frost` | Slate-50 | Sky-500 | Cool, precise, clinical |

## 6. Webapp Editor Specification

### 6.1 Architecture

```
webapp/
  app/
    layout.tsx              # Root layout (Geist font, Zinc palette)
    page.tsx                # Editor workspace
    api/
      render/route.ts       # Render queue API
      templates/route.ts    # Template listing API
  components/
    editor/
      Timeline.tsx          # Frame-accurate scene timeline
      Canvas.tsx            # Remotion Player wrapper
      PropsPanel.tsx        # Dynamic form from Zod schema
      ThemePicker.tsx       # Visual theme grid
      TemplateGallery.tsx   # Bento grid template browser
      ExportPanel.tsx       # Render settings + queue
    ui/
      GlassPanel.tsx        # Liquid glass container
      SpringButton.tsx      # Physics-based button
      SkeletonShimmer.tsx   # Loading placeholder
      BentoGrid.tsx         # Asymmetric grid layout
  lib/
    schemas.ts              # Shared Zod schemas
    themes.ts               # Theme registry
    templates.ts            # Template registry
  styles/
    globals.css             # Tailwind + custom properties
```

### 6.2 Editor Layout

```
+--[280px]--+--------[fluid]--------+--[320px]--+
|            |                       |            |
| Template   |                       | Props      |
| Gallery    |    Canvas / Preview   | Panel      |
|            |    (Remotion Player)  |            |
| Theme      |                       | Theme      |
| Picker     |                       | Picker     |
|            +-----------------------+            |
|            |      Timeline         | Export     |
|            |   (Scene strips)      | Panel      |
+------------+-----------------------+------------+
```

### 6.3 UI Component Specs

**GlassPanel:** `bg-white/5 backdrop-blur-xl border border-white/10 shadow-[inset_0_1px_0_rgba(255,255,255,0.1)] rounded-2xl`

**SpringButton:** Framer Motion `whileHover={{ scale: 1.02 }}` `whileTap={{ scale: 0.98 }}` with `transition={{ type: "spring", stiffness: 400, damping: 17 }}`

**SkeletonShimmer:** `animate-pulse bg-gradient-to-r from-zinc-800 via-zinc-700 to-zinc-800 bg-[length:200%_100%]`

**BentoGrid:** `grid grid-cols-3 gap-4` with items spanning `col-span-2`, `row-span-2` for asymmetry

## 7. Render Pipeline Specification

### 7.1 Render Configurations

```typescript
export interface RenderConfig {
  codec: 'h264' | 'h265' | 'vp8' | 'vp9' | 'prores';
  crf: number;              // 0-51, lower = better quality
  pixelFormat: 'yuv420p' | 'yuv444p';
  audioBitrate: string;     // e.g. '320k'
  numberOfGifLoops: number | null;
  everyNthFrame: number;    // 1 = all frames, 2 = half
}

export const RENDER_PRESETS = {
  'web-optimized': { codec: 'h264', crf: 23, pixelFormat: 'yuv420p' },
  'high-quality':  { codec: 'h264', crf: 18, pixelFormat: 'yuv420p' },
  'professional':  { codec: 'prores', crf: 0,  pixelFormat: 'yuv444p' },
  'social-media':  { codec: 'h264', crf: 20, pixelFormat: 'yuv420p' },
  'gif-preview':   { codec: 'gif',  crf: 0,  everyNthFrame: 2 },
} as const;
```

### 7.2 Lambda Rendering (Optional)

```typescript
// For serverless rendering at scale
import { renderMediaOnLambda } from '@remotion/lambda';

const render = await renderMediaOnLambda({
  region: 'us-east-1',
  functionName: 'remotion-render',
  composition: templateId,
  inputProps: validatedProps,
  codec: 'h264',
  imageFormat: 'jpeg',
  maxRetries: 2,
  privacy: 'public',
});
```

## 8. Quality Gates

### Mandatory Checks Before Render
1. All props pass Zod schema validation
2. Total duration > 2s and < 120s
3. Every scene has explicit durationInFrames
4. Every scene boundary has a transition
5. Font files are bundled (not external URLs)
6. Media assets are accessible and correct dimensions
7. No frame drops in preview (60fps target)

### Visual Quality Checks
1. Text never extends beyond safe zones (80px margins)
2. No text smaller than 18px at 1080p
3. Contrast ratio > 4.5:1 for all text
4. No pure black (#000) or pure white (#fff)
5. Accent color saturation < 80%
6. No orphaned single words on a line

[PROTOCOL]: Update this header on changes, then check AGENTS.md
