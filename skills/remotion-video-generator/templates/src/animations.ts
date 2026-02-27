/**
 * [INPUT]: None (root animation constants)
 * [OUTPUT]: SPRING presets, EASE curves, staggeredSpring(), useAnimatedValue()
 * [POS]: Animation engine — the physics backbone of all motion
 * [PROTOCOL]: Update this header on changes, then check AGENTS.md
 */

import { spring, interpolate, Easing, SpringConfig } from 'remotion';

// ============================================================
// SPRING PRESETS — Physics backbone of all motion
// ============================================================

export const SPRING = {
  GENTLE: { damping: 14, stiffness: 80, mass: 1.0 } as SpringConfig,
  STANDARD: { damping: 12, stiffness: 100, mass: 0.8 } as SpringConfig,
  SNAPPY: { damping: 15, stiffness: 200, mass: 0.5 } as SpringConfig,
  DRAMATIC: { damping: 8, stiffness: 80, mass: 1.2 } as SpringConfig,
  BOUNCE: { damping: 6, stiffness: 120, mass: 0.6 } as SpringConfig,
  CINEMATIC: { damping: 20, stiffness: 40, mass: 1.5 } as SpringConfig,
} as const;

// ============================================================
// EASING CURVES — For interpolate() when springs don't fit
// ============================================================

export const EASE = {
  OUT_EXPO: Easing.out(Easing.exp),
  IN_EXPO: Easing.in(Easing.exp),
  IN_OUT_CUBIC: Easing.inOut(Easing.cubic),
  IN_OUT_QUART: Easing.inOut(Easing.quad),
} as const;

// ============================================================
// STAGGER — Sequential reveal orchestration
// ============================================================

export function staggeredSpring(
  frame: number,
  fps: number,
  index: number,
  config: {
    delayPerItem?: number;
    spring?: SpringConfig;
  } = {}
): number {
  const { delayPerItem = 5, spring: springConfig = SPRING.STANDARD } = config;
  const offset = frame - index * delayPerItem;
  if (offset < 0) return 0;
  return spring({ frame: offset, fps, config: springConfig });
}

// ============================================================
// ANIMATED VALUE — Spring-driven single value
// ============================================================

export function animatedValue(
  frame: number,
  fps: number,
  delay: number = 0,
  config: SpringConfig = SPRING.STANDARD
): number {
  const offset = frame - delay;
  if (offset < 0) return 0;
  return spring({ frame: offset, fps, config });
}

// ============================================================
// SCENE TIMING — Frame math utilities
// ============================================================

export function sceneTiming(
  frame: number,
  sceneStart: number,
  sceneDuration: number
): { localFrame: number; progress: number; isActive: boolean } {
  const localFrame = frame - sceneStart;
  const progress = Math.min(1, Math.max(0, localFrame / sceneDuration));
  const isActive = localFrame >= 0 && localFrame < sceneDuration;
  return { localFrame, progress, isActive };
}

export function calculateSceneStarts(
  scenes: { durationInFrames: number }[]
): number[] {
  const starts: number[] = [];
  let current = 0;
  for (const scene of scenes) {
    starts.push(current);
    current += scene.durationInFrames;
  }
  return starts;
}

// ============================================================
// INTERPOLATION HELPERS
// ============================================================

export function fadeIn(frame: number, start: number = 0, duration: number = 15): number {
  return interpolate(frame, [start, start + duration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: EASE.OUT_EXPO,
  });
}

export function fadeOut(frame: number, start: number, duration: number = 15): number {
  return interpolate(frame, [start, start + duration], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: EASE.IN_EXPO,
  });
}

export function slideIn(
  frame: number,
  fps: number,
  delay: number = 0,
  distance: number = 40,
  config: SpringConfig = SPRING.STANDARD
): { opacity: number; translateY: number } {
  const progress = animatedValue(frame, fps, delay, config);
  return {
    opacity: progress,
    translateY: (1 - progress) * distance,
  };
}

export function scaleIn(
  frame: number,
  fps: number,
  delay: number = 0,
  config: SpringConfig = SPRING.SNAPPY
): { opacity: number; scale: number } {
  const progress = animatedValue(frame, fps, delay, config);
  return {
    opacity: progress,
    scale: interpolate(progress, [0, 1], [0.85, 1]),
  };
}
