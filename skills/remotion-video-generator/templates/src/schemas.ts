/**
 * [INPUT]: zod for validation
 * [OUTPUT]: All Zod schemas for props validation
 * [POS]: Schema layer — validates all template props at runtime
 * [PROTOCOL]: Update this header on changes, then check AGENTS.md
 */

import { z } from 'zod';

// ============================================================
// MEDIA SCHEMAS
// ============================================================

export const MediaItemSchema = z.object({
  type: z.enum(['image', 'video', 'svg', 'lottie']),
  src: z.string(),
  alt: z.string().optional(),
  fit: z.enum(['cover', 'contain', 'fill']).optional(),
});

export const MetricItemSchema = z.object({
  label: z.string().max(60),
  value: z.union([z.string(), z.number()]),
  prefix: z.string().optional(),
  suffix: z.string().optional(),
  trend: z.enum(['up', 'down', 'neutral']).optional(),
});

// ============================================================
// SCENE SCHEMAS
// ============================================================

export const TransitionSchema = z.object({
  type: z.enum([
    'wipe-left', 'wipe-right', 'wipe-up', 'wipe-down',
    'dissolve', 'dissolve-scale',
    'curtain-horizontal', 'curtain-vertical',
    'slide-left', 'slide-right',
    'zoom-in', 'zoom-out',
    'liquid-morph',
    'iris-open', 'iris-close',
  ]),
  durationInFrames: z.number().min(5).max(60).default(20),
  easing: z.string().optional(),
});

export const BackgroundSchema = z.object({
  type: z.enum(['solid', 'gradient', 'mesh', 'image', 'video']),
  value: z.union([z.string(), z.array(z.string())]),
  opacity: z.number().min(0).max(1).optional(),
});

export const SceneContentSchema = z.object({
  headline: z.string().max(80).optional(),
  subheadline: z.string().max(160).optional(),
  body: z.string().max(500).optional(),
  bullets: z.array(z.string().max(120)).max(8).optional(),
  media: z.array(MediaItemSchema).optional(),
  metrics: z.array(MetricItemSchema).max(6).optional(),
  cta: z.object({
    label: z.string().max(40),
    url: z.string().url().optional(),
  }).optional(),
  code: z.object({
    language: z.string(),
    snippet: z.string(),
  }).optional(),
});

export const SceneSchema = z.object({
  id: z.string(),
  type: z.enum([
    'title', 'split', 'showcase', 'list', 'quote', 'data',
    'media', 'cta', 'logo-wall', 'comparison', 'timeline',
    'code', 'blank',
  ]),
  durationInFrames: z.number().min(15).max(900),
  content: SceneContentSchema,
  transition: TransitionSchema.optional(),
  background: BackgroundSchema.optional(),
});

// ============================================================
// THEME SCHEMAS
// ============================================================

export const ColorTokensSchema = z.object({
  bg: z.string(),
  bgAlt: z.string(),
  fg: z.string(),
  fgMuted: z.string(),
  accent: z.string(),
  accentFg: z.string(),
  surface: z.string(),
  border: z.string(),
  gradient: z.tuple([z.string(), z.string()]).optional(),
});

export const TypographyTokensSchema = z.object({
  displayFamily: z.string(),
  headlineFamily: z.string(),
  bodyFamily: z.string(),
  monoFamily: z.string(),
  scale: z.number().min(0.5).max(2.0).default(1.0),
});

export const MotionTokensSchema = z.object({
  defaultSpring: z.string(),
  staggerDelay: z.number().min(1).max(20).default(5),
  transitionType: TransitionSchema.shape.type,
  transitionDuration: z.number().min(5).max(60).default(20),
});

export const ThemeSchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  colors: ColorTokensSchema,
  typography: TypographyTokensSchema,
  spacing: z.object({ base: z.number(), scale: z.number() }),
  radius: z.number(),
  grain: z.boolean(),
  motion: MotionTokensSchema,
});

// ============================================================
// TEMPLATE PROPS SCHEMA
// ============================================================

export const BaseTemplateSchema = z.object({
  theme: ThemeSchema,
  scenes: z.array(SceneSchema).min(1).max(12),
  fps: z.number().min(24).max(60).default(30),
});

// ============================================================
// RENDER CONFIG SCHEMA
// ============================================================

export const RenderConfigSchema = z.object({
  codec: z.enum(['h264', 'h265', 'vp8', 'vp9', 'prores']),
  crf: z.number().min(0).max(51),
  pixelFormat: z.enum(['yuv420p', 'yuv444p']),
  audioBitrate: z.string().optional(),
  numberOfGifLoops: z.number().nullable().optional(),
  everyNthFrame: z.number().min(1).optional(),
});
