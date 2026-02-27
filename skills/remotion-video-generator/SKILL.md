---
name: remotion-video-generator
description: Production-ready Remotion video generator. Creates programmatic videos with premium motion design, taste-skill UI principles, and 20+ templates. Supports B2B showcases, social ads, product launches, explainers, and more. Outputs render-ready Remotion compositions with Spring physics, staggered orchestration, and cinematic transitions.
---

# Remotion Video Generator

## 1. ACTIVE BASELINE CONFIGURATION

* DESIGN_VARIANCE: 8 (Artsy, asymmetric compositions)
* MOTION_INTENSITY: 6 (Fluid spring animations, perpetual micro-interactions)
* VISUAL_DENSITY: 4 (Breathing space, gallery-mode elegance)

**AI Instruction:** These values are the strict baseline for ALL video generations. Adapt dynamically based on user prompts. Use these as global variables driving Sections 3-8.

## 2. WHEN TO INVOKE THIS SKILL

Trigger on ANY of these patterns:
- "Create a video", "Generate a video", "Make a video"
- "Remotion", "programmatic video", "video template"
- "Product demo video", "social media video", "explainer video"
- "B2B video", "SaaS demo", "launch video", "promo video"
- "Video ad", "YouTube intro", "TikTok video", "Reels"
- "Animate this", "turn this into a video"
- "Video from data", "dynamic video", "personalized video"

## 3. CORE ARCHITECTURE

### Tech Stack
- **Runtime:** Remotion v4+ (React-based video framework)
- **Animation:** Remotion `spring()`, `interpolate()`, `useCurrentFrame()`
- **Styling:** Tailwind CSS v4 (within Remotion compositions)
- **Typography:** Geist / Satoshi / Outfit (NEVER Inter)
- **Icons:** @phosphor-icons/react (NEVER emoji)
- **Media:** Sharp for image processing, FFmpeg for encoding

### Project Structure
```
src/
  compositions/        # Video compositions (one per template)
  components/          # Reusable animated components
    typography/        # Text reveal, kinetic type, scramble
    transitions/       # Wipe, dissolve, curtain, liquid
    layouts/           # Split, bento, asymmetric, stack
    media/             # Image sequences, video overlays
    shapes/            # Animated SVG, particles, mesh gradients
  hooks/               # useAnimatedValue, useStagger, useParallax
  themes/              # Color + typography + spacing tokens
  lib/                 # Utilities, easing functions, math helpers
  Root.tsx             # Composition registry
  index.ts             # Entry point
remotion.config.ts     # Remotion configuration
```

### Composition Schema (Every Template MUST Export)
```typescript
interface VideoComposition {
  id: string;
  component: React.FC<VideoProps>;
  width: number;           // Default: 1920
  height: number;          // Default: 1080
  fps: number;             // Default: 30
  durationInFrames: number;
  defaultProps: VideoProps;
  schema: z.ZodType;       // Zod validation for props
}

interface VideoProps {
  theme: ThemeConfig;
  content: ContentBlock[];
  settings: RenderSettings;
}
```

## 4. ANIMATION SYSTEM (Spring-First)

### Mandatory Spring Physics
ALL animations MUST use Remotion's `spring()` with premium configs:

```typescript
// Standard entrance
spring({ frame, fps, config: { damping: 12, stiffness: 100, mass: 0.8 } })

// Snappy UI element
spring({ frame, fps, config: { damping: 15, stiffness: 200, mass: 0.5 } })

// Heavy/dramatic entrance
spring({ frame, fps, config: { damping: 8, stiffness: 80, mass: 1.2 } })

// Overshoot bounce
spring({ frame, fps, config: { damping: 6, stiffness: 120, mass: 0.6, overshootClamping: false } })
```

### BANNED Animation Patterns
- NO linear easing (`Easing.linear`) for UI elements
- NO `setTimeout` or `setInterval` — use frame-based timing
- NO CSS `@keyframes` — use Remotion's `interpolate()`
- NO opacity-only fades as primary transitions
- NO instant cuts between scenes (always transition)

### Staggered Orchestration
```typescript
// Stagger children by frame offset
const stagger = (index: number, delayPerItem: number = 5) => {
  const offset = frame - index * delayPerItem;
  return spring({ frame: Math.max(0, offset), fps, config: SPRING_SNAPPY });
};
```

### Scene Transition System
Every template MUST use scene transitions from this palette:
- **Wipe:** Directional mask reveal (left, right, up, down, diagonal)
- **Dissolve:** Cross-fade with scale shift
- **Curtain:** Split-screen parting
- **Liquid:** SVG filter displacement morph
- **Zoom:** Scale from element to full-frame
- **Slide:** Physics-based slide with overshoot

## 5. DESIGN ENGINEERING (Taste-Skill Enforced)

### Typography Rules
- Display: `fontFamily: 'Geist', fontSize: 72, fontWeight: 800, letterSpacing: -2`
- Headline: `fontFamily: 'Satoshi', fontSize: 48, fontWeight: 700, letterSpacing: -1`
- Body: `fontFamily: 'Outfit', fontSize: 24, fontWeight: 400, lineHeight: 1.6`
- Mono/Data: `fontFamily: 'Geist Mono', fontSize: 20, fontWeight: 500`

### Color Rules
- Max 1 accent color per video. Saturation < 80%.
- NO purple/neon AI aesthetic. Use Zinc/Slate bases + singular accent.
- Background: Never pure black (#000). Use off-black (Zinc-950) or deep navy.
- Text: Never pure white on dark. Use Zinc-100 or Slate-50.

### Layout Rules (DESIGN_VARIANCE: 8)
- NO centered-only compositions. Use asymmetric splits, offset grids.
- Text blocks: left-aligned or right-aligned with massive counter-space.
- Grid: Use fractional units (`2fr 1fr`, `3fr 2fr`) not equal columns.
- Safe zones: 80px margin from all edges for broadcast safety.

### Visual Rules
- NO stock photo aesthetic. Use geometric shapes, gradients, typography as hero.
- NO drop shadows on text. Use contrast, backdrop, or knockout instead.
- Grain/noise: Apply as a static overlay layer, never on animated elements.
- Glass effects: 1px inner border + subtle inner shadow for edge refraction.

## 6. TEMPLATE CATEGORIES

### Available Templates (20+)
See `templates/` directory. Each template is a self-contained composition:

| Category | Templates | Aspect Ratios |
|----------|-----------|---------------|
| B2B/SaaS | b2b-showcase, saas-demo, feature-highlight, case-study | 16:9, 1:1 |
| Social Ads | social-story, social-feed, social-carousel, tiktok-ad | 9:16, 1:1, 4:5 |
| Product | product-launch, product-tour, unboxing-reveal | 16:9, 9:16 |
| Corporate | company-intro, team-showcase, quarterly-report, investor-deck | 16:9 |
| Creative | kinetic-typography, data-visualization, countdown-timer | 16:9, 1:1 |
| Education | explainer-motion, tutorial-walkthrough, comparison-split | 16:9 |
| Events | event-promo, conference-opener, webinar-intro | 16:9, 9:16 |

### Template Props Schema (Universal)
```typescript
const BaseTemplateSchema = z.object({
  headline: z.string().max(80),
  subheadline: z.string().max(160).optional(),
  body: z.string().max(500).optional(),
  cta: z.string().max(40).optional(),
  media: z.array(MediaItemSchema).optional(),
  logo: z.string().url().optional(),
  theme: ThemeSchema,
  scenes: z.array(SceneSchema).min(1).max(12),
});
```

## 7. THEME SYSTEM

### Available Themes (8+)
See `themes/` directory. Each theme provides:

```typescript
interface ThemeConfig {
  name: string;
  colors: {
    background: string;
    foreground: string;
    accent: string;
    accentForeground: string;
    muted: string;
    mutedForeground: string;
    surface: string;
    border: string;
  };
  typography: {
    display: FontConfig;
    headline: FontConfig;
    body: FontConfig;
    mono: FontConfig;
  };
  spacing: { base: number; scale: number };
  radius: number;
  motion: {
    spring: SpringConfig;
    stagger: number;
    transitionStyle: 'wipe' | 'dissolve' | 'curtain' | 'slide';
  };
}
```

## 8. RENDER PIPELINE

### Output Formats
- **MP4** (H.264): Default, universal playback
- **WebM** (VP9): Web-optimized, smaller files
- **GIF**: Social preview, max 15s
- **PNG Sequence**: Post-production pipeline
- **ProRes**: Professional editing workflow

### Resolution Presets
- 4K: 3840x2160 @ 30fps
- 1080p: 1920x1080 @ 30fps
- 720p: 1280x720 @ 30fps
- Square: 1080x1080 @ 30fps
- Story: 1080x1920 @ 30fps
- TikTok: 1080x1920 @ 30fps

### Render Command
```bash
npx remotion render src/index.ts <CompositionId> out/video.mp4 \
  --props='{"theme":"dark-tech","headline":"Ship Faster"}' \
  --codec=h264 \
  --crf=18
```

## 9. WEBAPP EDITOR (Gamma-Like)

The `webapp/` directory contains a Next.js template for a visual video editor:

### Editor Features
- **Timeline:** Frame-accurate scene editor with drag-to-reorder
- **Preview:** Real-time Remotion Player with playback controls
- **Props Panel:** Dynamic form generated from Zod schemas
- **Theme Picker:** Visual theme switcher with live preview
- **Template Gallery:** Bento grid of available templates
- **Export:** Render queue with progress tracking

### Editor UI Rules (Taste-Skill Enforced)
- Font: Geist + Geist Mono
- Palette: Zinc base + single accent
- Layout: Asymmetric sidebar (280px left panel, fluid canvas, 320px right panel)
- Glass panels with inner border refraction
- Spring-physics for all panel transitions
- Skeleton shimmer loaders during render

## 10. GENERATION WORKFLOW

When a user requests a video:

1. **Parse Intent:** Identify template category, content, and tone
2. **Select Template:** Match to closest template from the 20+ available
3. **Apply Theme:** Select or generate theme matching brand/mood
4. **Structure Scenes:** Break content into 3-8 scenes with transitions
5. **Generate Code:** Output complete Remotion composition
6. **Validate:** Run Zod schema validation on all props
7. **Render Instructions:** Provide exact render command

### AI Prompt Structure
```
TEMPLATE: [selected-template]
THEME: [selected-theme]
SCENES: [scene-by-scene breakdown]
DURATION: [total seconds]
ASPECT: [ratio]
OUTPUT: [format]
```

## 11. PRE-FLIGHT CHECKLIST

Before outputting any video composition:
- [ ] Spring physics on ALL animated properties (no linear easing)
- [ ] Staggered entrance for multi-element scenes
- [ ] Scene transitions between every scene change
- [ ] Safe zones respected (80px margins)
- [ ] Typography hierarchy: Display > Headline > Body > Mono
- [ ] Max 1 accent color, saturation < 80%
- [ ] No Inter font, no emoji, no purple glow
- [ ] Asymmetric layouts (DESIGN_VARIANCE: 8)
- [ ] Frame-based timing only (no setTimeout/setInterval)
- [ ] Zod schema validates all props
- [ ] Render command provided with correct codec/CRF

[PROTOCOL]: Update this header on changes, then check AGENTS.md
