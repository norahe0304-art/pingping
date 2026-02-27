/**
 * [INPUT]: None (root type definitions)
 * [OUTPUT]: All shared types for the Remotion video generator
 * [POS]: Core type system — every other module depends on this
 * [PROTOCOL]: Update this header on changes, then check AGENTS.md
 */

import { z } from 'zod';

// ============================================================
// ASPECT RATIOS
// ============================================================

export type AspectRatio = '16:9' | '9:16' | '1:1' | '4:5' | '4:3';

export const ASPECT_DIMENSIONS: Record<AspectRatio, { width: number; height: number }> = {
  '16:9': { width: 1920, height: 1080 },
  '9:16': { width: 1080, height: 1920 },
  '1:1': { width: 1080, height: 1080 },
  '4:5': { width: 1080, height: 1350 },
  '4:3': { width: 1440, height: 1080 },
};

// ============================================================
// SCENE TYPES
// ============================================================

export type SceneType =
  | 'title'
  | 'split'
  | 'showcase'
  | 'list'
  | 'quote'
  | 'data'
  | 'media'
  | 'cta'
  | 'logo-wall'
  | 'comparison'
  | 'timeline'
  | 'code'
  | 'blank';

export type TransitionType =
  | 'wipe-left' | 'wipe-right' | 'wipe-up' | 'wipe-down'
  | 'dissolve' | 'dissolve-scale'
  | 'curtain-horizontal' | 'curtain-vertical'
  | 'slide-left' | 'slide-right'
  | 'zoom-in' | 'zoom-out'
  | 'liquid-morph'
  | 'iris-open' | 'iris-close';

// ============================================================
// MEDIA
// ============================================================

export interface MediaItem {
  type: 'image' | 'video' | 'svg' | 'lottie';
  src: string;
  alt?: string;
  fit?: 'cover' | 'contain' | 'fill';
}

export interface MetricItem {
  label: string;
  value: string | number;
  prefix?: string;
  suffix?: string;
  trend?: 'up' | 'down' | 'neutral';
}

// ============================================================
// SCENE
// ============================================================

export interface SceneTransition {
  type: TransitionType;
  durationInFrames: number;
  easing?: string;
}

export interface BackgroundConfig {
  type: 'solid' | 'gradient' | 'mesh' | 'image' | 'video';
  value: string | string[];
  opacity?: number;
}

export interface SceneContent {
  headline?: string;
  subheadline?: string;
  body?: string;
  bullets?: string[];
  media?: MediaItem[];
  metrics?: MetricItem[];
  cta?: { label: string; url?: string };
  code?: { language: string; snippet: string };
}

export interface Scene {
  id: string;
  type: SceneType;
  durationInFrames: number;
  content: SceneContent;
  transition?: SceneTransition;
  background?: BackgroundConfig;
}

// ============================================================
// THEME
// ============================================================

export interface ColorTokens {
  bg: string;
  bgAlt: string;
  fg: string;
  fgMuted: string;
  accent: string;
  accentFg: string;
  surface: string;
  border: string;
  gradient?: [string, string];
}

export interface FontConfig {
  family: string;
  weight: number;
  letterSpacing: number;
  lineHeight: number;
}

export interface TypographyTokens {
  displayFamily: string;
  headlineFamily: string;
  bodyFamily: string;
  monoFamily: string;
  scale: number;
}

export interface SpacingTokens {
  base: number;
  scale: number;
}

export interface MotionTokens {
  defaultSpring: string;
  staggerDelay: number;
  transitionType: TransitionType;
  transitionDuration: number;
}

export interface ThemeConfig {
  id: string;
  name: string;
  description: string;
  colors: ColorTokens;
  typography: TypographyTokens;
  spacing: SpacingTokens;
  radius: number;
  grain: boolean;
  motion: MotionTokens;
}

// ============================================================
// TEMPLATE
// ============================================================

export type TemplateCategory =
  | 'b2b-saas'
  | 'social-ads'
  | 'product'
  | 'corporate'
  | 'creative'
  | 'education'
  | 'events';

export interface TemplateProps {
  theme: ThemeConfig;
  scenes: Scene[];
  fps?: number;
}

export interface TemplateDefinition {
  id: string;
  name: string;
  description: string;
  category: TemplateCategory;
  aspectRatios: AspectRatio[];
  defaultDuration: number;
  minScenes: number;
  maxScenes: number;
  schema: z.ZodType;
  component: React.FC<TemplateProps>;
  thumbnail?: string;
}

// ============================================================
// RENDER
// ============================================================

export interface RenderConfig {
  codec: 'h264' | 'h265' | 'vp8' | 'vp9' | 'prores';
  crf: number;
  pixelFormat: 'yuv420p' | 'yuv444p';
  audioBitrate?: string;
  numberOfGifLoops?: number | null;
  everyNthFrame?: number;
}

export const RENDER_PRESETS = {
  'web-optimized': { codec: 'h264' as const, crf: 23, pixelFormat: 'yuv420p' as const },
  'high-quality': { codec: 'h264' as const, crf: 18, pixelFormat: 'yuv420p' as const },
  'professional': { codec: 'prores' as const, crf: 0, pixelFormat: 'yuv444p' as const },
  'social-media': { codec: 'h264' as const, crf: 20, pixelFormat: 'yuv420p' as const },
} as const;
