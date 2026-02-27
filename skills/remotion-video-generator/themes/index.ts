/**
 * [INPUT]: ThemeConfig from ./types
 * [OUTPUT]: 10 brand themes + theme registry
 * [POS]: Theme system — visual identity tokens for all templates
 * [PROTOCOL]: Update this header on changes, then check AGENTS.md
 */

import { ThemeConfig } from './types';

// ============================================================
// SHARED TYPOGRAPHY — Geist / Satoshi / Outfit stack
// ============================================================

const BASE_TYPOGRAPHY = {
  displayFamily: 'Geist',
  headlineFamily: 'Satoshi',
  bodyFamily: 'Outfit',
  monoFamily: 'Geist Mono',
  scale: 1.0,
};

// ============================================================
// 1. CORPORATE BLUE — Professional, trustworthy
// ============================================================

export const corporateBlue: ThemeConfig = {
  id: 'corporate-blue',
  name: 'Corporate Blue',
  description: 'Professional and trustworthy — enterprise presentations, investor decks',
  colors: {
    bg: '#0f172a',        // Slate-900
    bgAlt: '#1e293b',     // Slate-800
    fg: '#f1f5f9',        // Slate-100
    fgMuted: '#94a3b8',   // Slate-400
    accent: '#3b82f6',    // Blue-500
    accentFg: '#ffffff',
    surface: '#1e293b',
    border: '#334155',    // Slate-700
  },
  typography: BASE_TYPOGRAPHY,
  spacing: { base: 8, scale: 1.5 },
  radius: 12,
  grain: false,
  motion: {
    defaultSpring: 'STANDARD',
    staggerDelay: 5,
    transitionType: 'dissolve',
    transitionDuration: 20,
  },
};

// ============================================================
// 2. STARTUP GRADIENT — Modern, energetic
// ============================================================

export const startupGradient: ThemeConfig = {
  id: 'startup-gradient',
  name: 'Startup Gradient',
  description: 'Modern and energetic — product launches, SaaS demos',
  colors: {
    bg: '#09090b',        // Zinc-950
    bgAlt: '#18181b',     // Zinc-900
    fg: '#fafafa',        // Zinc-50
    fgMuted: '#a1a1aa',   // Zinc-400
    accent: '#34d399',    // Emerald-400
    accentFg: '#022c22',
    surface: '#18181b',
    border: '#27272a',    // Zinc-800
    gradient: ['#34d399', '#22d3ee'], // Emerald→Cyan
  },
  typography: BASE_TYPOGRAPHY,
  spacing: { base: 8, scale: 1.5 },
  radius: 16,
  grain: true,
  motion: {
    defaultSpring: 'SNAPPY',
    staggerDelay: 4,
    transitionType: 'slide-left',
    transitionDuration: 18,
  },
};

// ============================================================
// 3. LUXURY GOLD — Premium, exclusive
// ============================================================

export const luxuryGold: ThemeConfig = {
  id: 'luxury-gold',
  name: 'Luxury Gold',
  description: 'Premium and exclusive — high-end products, luxury brands',
  colors: {
    bg: '#0a0a0a',        // Neutral-950
    bgAlt: '#171717',     // Neutral-900
    fg: '#fafafa',
    fgMuted: '#a3a3a3',   // Neutral-400
    accent: '#fbbf24',    // Amber-400
    accentFg: '#451a03',
    surface: '#171717',
    border: '#262626',    // Neutral-800
  },
  typography: { ...BASE_TYPOGRAPHY, scale: 1.1 },
  spacing: { base: 10, scale: 1.618 },
  radius: 8,
  grain: true,
  motion: {
    defaultSpring: 'CINEMATIC',
    staggerDelay: 6,
    transitionType: 'dissolve-scale',
    transitionDuration: 25,
  },
};

// ============================================================
// 4. DARK TECH — Minimal, developer-focused
// ============================================================

export const darkTech: ThemeConfig = {
  id: 'dark-tech',
  name: 'Dark Tech',
  description: 'Minimal and developer-focused — dev tools, API products, technical content',
  colors: {
    bg: '#09090b',        // Zinc-950
    bgAlt: '#18181b',     // Zinc-900
    fg: '#e4e4e7',        // Zinc-200
    fgMuted: '#71717a',   // Zinc-500
    accent: '#a1a1aa',    // Zinc-400
    accentFg: '#09090b',
    surface: '#18181b',
    border: '#27272a',    // Zinc-800
  },
  typography: { ...BASE_TYPOGRAPHY, scale: 0.95 },
  spacing: { base: 8, scale: 1.5 },
  radius: 8,
  grain: true,
  motion: {
    defaultSpring: 'STANDARD',
    staggerDelay: 4,
    transitionType: 'wipe-right',
    transitionDuration: 15,
  },
};

// ============================================================
// 5. MINIMAL WHITE — Clean, editorial
// ============================================================

export const minimalWhite: ThemeConfig = {
  id: 'minimal-white',
  name: 'Minimal White',
  description: 'Clean and editorial — content marketing, brand stories',
  colors: {
    bg: '#ffffff',
    bgAlt: '#f4f4f5',     // Zinc-100
    fg: '#18181b',        // Zinc-900
    fgMuted: '#71717a',   // Zinc-500
    accent: '#18181b',    // Zinc-900
    accentFg: '#ffffff',
    surface: '#f4f4f5',
    border: '#e4e4e7',    // Zinc-200
  },
  typography: BASE_TYPOGRAPHY,
  spacing: { base: 10, scale: 1.618 },
  radius: 12,
  grain: false,
  motion: {
    defaultSpring: 'GENTLE',
    staggerDelay: 6,
    transitionType: 'dissolve',
    transitionDuration: 22,
  },
};

// ============================================================
// 6. VIBRANT POP — Bold, attention-grabbing
// ============================================================

export const vibrantPop: ThemeConfig = {
  id: 'vibrant-pop',
  name: 'Vibrant Pop',
  description: 'Bold and attention-grabbing — social ads, event promos',
  colors: {
    bg: '#fafafa',        // Zinc-50
    bgAlt: '#f4f4f5',
    fg: '#18181b',
    fgMuted: '#52525b',   // Zinc-600
    accent: '#f43f5e',    // Rose-500
    accentFg: '#ffffff',
    surface: '#ffffff',
    border: '#e4e4e7',
  },
  typography: { ...BASE_TYPOGRAPHY, scale: 1.05 },
  spacing: { base: 8, scale: 1.5 },
  radius: 20,
  grain: false,
  motion: {
    defaultSpring: 'BOUNCE',
    staggerDelay: 3,
    transitionType: 'slide-right',
    transitionDuration: 15,
  },
};

// ============================================================
// 7. RETRO WAVE — Nostalgic, creative
// ============================================================

export const retroWave: ThemeConfig = {
  id: 'retro-wave',
  name: 'Retro Wave',
  description: 'Nostalgic and creative — music, entertainment, creative agencies',
  colors: {
    bg: '#1e1b4b',        // Indigo-950
    bgAlt: '#312e81',     // Indigo-900
    fg: '#e0e7ff',        // Indigo-100
    fgMuted: '#a5b4fc',   // Indigo-300
    accent: '#e879f9',    // Fuchsia-400
    accentFg: '#1e1b4b',
    surface: '#312e81',
    border: '#3730a3',    // Indigo-800
    gradient: ['#e879f9', '#fb923c'], // Fuchsia→Orange
  },
  typography: BASE_TYPOGRAPHY,
  spacing: { base: 8, scale: 1.5 },
  radius: 16,
  grain: true,
  motion: {
    defaultSpring: 'DRAMATIC',
    staggerDelay: 4,
    transitionType: 'curtain-horizontal',
    transitionDuration: 20,
  },
};

// ============================================================
// 8. NATURE GREEN — Organic, sustainable
// ============================================================

export const natureGreen: ThemeConfig = {
  id: 'nature-green',
  name: 'Nature Green',
  description: 'Organic and sustainable — eco brands, wellness, health',
  colors: {
    bg: '#0c0a09',        // Stone-950
    bgAlt: '#1c1917',     // Stone-900
    fg: '#fafaf9',        // Stone-50
    fgMuted: '#a8a29e',   // Stone-400
    accent: '#10b981',    // Emerald-500
    accentFg: '#022c22',
    surface: '#1c1917',
    border: '#292524',    // Stone-800
  },
  typography: BASE_TYPOGRAPHY,
  spacing: { base: 10, scale: 1.5 },
  radius: 12,
  grain: false,
  motion: {
    defaultSpring: 'GENTLE',
    staggerDelay: 6,
    transitionType: 'dissolve',
    transitionDuration: 25,
  },
};

// ============================================================
// 9. WARM EARTH — Approachable, grounded
// ============================================================

export const warmEarth: ThemeConfig = {
  id: 'warm-earth',
  name: 'Warm Earth',
  description: 'Approachable and grounded — community, education, non-profit',
  colors: {
    bg: '#1c1917',        // Stone-900
    bgAlt: '#292524',     // Stone-800
    fg: '#fafaf9',
    fgMuted: '#a8a29e',
    accent: '#f97316',    // Orange-500
    accentFg: '#431407',
    surface: '#292524',
    border: '#44403c',    // Stone-700
  },
  typography: BASE_TYPOGRAPHY,
  spacing: { base: 8, scale: 1.5 },
  radius: 14,
  grain: false,
  motion: {
    defaultSpring: 'STANDARD',
    staggerDelay: 5,
    transitionType: 'wipe-up',
    transitionDuration: 20,
  },
};

// ============================================================
// 10. ARCTIC FROST — Cool, precise, clinical
// ============================================================

export const arcticFrost: ThemeConfig = {
  id: 'arctic-frost',
  name: 'Arctic Frost',
  description: 'Cool and precise — fintech, healthcare, data platforms',
  colors: {
    bg: '#f8fafc',        // Slate-50
    bgAlt: '#f1f5f9',     // Slate-100
    fg: '#0f172a',        // Slate-900
    fgMuted: '#64748b',   // Slate-500
    accent: '#0ea5e9',    // Sky-500
    accentFg: '#ffffff',
    surface: '#ffffff',
    border: '#e2e8f0',    // Slate-200
  },
  typography: { ...BASE_TYPOGRAPHY, scale: 0.95 },
  spacing: { base: 8, scale: 1.5 },
  radius: 10,
  grain: false,
  motion: {
    defaultSpring: 'SNAPPY',
    staggerDelay: 4,
    transitionType: 'wipe-right',
    transitionDuration: 16,
  },
};

// ============================================================
// THEME REGISTRY
// ============================================================

export const THEMES: Record<string, ThemeConfig> = {
  'corporate-blue': corporateBlue,
  'startup-gradient': startupGradient,
  'luxury-gold': luxuryGold,
  'dark-tech': darkTech,
  'minimal-white': minimalWhite,
  'vibrant-pop': vibrantPop,
  'retro-wave': retroWave,
  'nature-green': natureGreen,
  'warm-earth': warmEarth,
  'arctic-frost': arcticFrost,
};

export function getTheme(id: string): ThemeConfig {
  const theme = THEMES[id];
  if (!theme) throw new Error(`Theme "${id}" not found. Available: ${Object.keys(THEMES).join(', ')}`);
  return theme;
}

export const DEFAULT_THEME = darkTech;
