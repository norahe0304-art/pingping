/**
 * [INPUT]: Depends on browser fetch API and /api/tts endpoint.
 * [OUTPUT]: Exposes the main editor-like landing page and TTS test interaction.
 * [POS]: webapp/src/app primary UI entry; asymmetric bento layout aligned with taste-skill constraints.
 * [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
 */
"use client";

import { useMemo, useState } from "react";

type TtsState = "idle" | "loading" | "ok" | "error";

export default function HomePage() {
  const [script, setScript] = useState(
    "Create a crisp 20-second product launch video: problem, value, CTA.",
  );
  const [voice, setVoice] = useState("alloy");
  const [status, setStatus] = useState<TtsState>("idle");
  const [message, setMessage] = useState("");
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  const statusLabel = useMemo(() => {
    if (status === "loading") return "Generating preview...";
    if (status === "ok") return "Preview generated.";
    if (status === "error") return "Generation failed.";
    return "Ready";
  }, [status]);

  async function handleGenerate() {
    if (!script.trim()) {
      setStatus("error");
      setMessage("Script is empty.");
      return;
    }

    setStatus("loading");
    setMessage("");

    try {
      const res = await fetch("/api/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: script, voice }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ error: "Unknown error" }));
        throw new Error(err.error || `HTTP ${res.status}`);
      }

      const contentType = res.headers.get("content-type") || "";
      if (!contentType.includes("audio")) {
        const payload = await res.json().catch(() => ({}));
        throw new Error(payload.error || "TTS endpoint did not return audio.");
      }

      const blob = await res.blob();
      const nextUrl = URL.createObjectURL(blob);
      if (audioUrl) URL.revokeObjectURL(audioUrl);
      setAudioUrl(nextUrl);
      setStatus("ok");
      setMessage("Audio preview is ready.");
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof Error ? error.message : "Generation failed.");
    }
  }

  return (
    <main className="shell">
      <section className="hero panel">
        <p className="eyebrow">Remotion Generator</p>
        <h1>Design premium motion stories without a timeline drag hell.</h1>
        <p className="lede">
          Asymmetric layout, fluid spring motion, and production-first template flow.
          Draft your script, generate voice preview, then iterate scene blocks.
        </p>
        <div className="statusRow">
          <span className={`statusDot status-${status}`} />
          <span>{statusLabel}</span>
          {message ? <span className="statusMsg">{message}</span> : null}
        </div>
      </section>

      <section className="composer panel">
        <label htmlFor="script" className="fieldLabel">
          Script Draft
        </label>
        <textarea
          id="script"
          value={script}
          onChange={(e) => setScript(e.target.value)}
          rows={8}
          placeholder="Write your launch narrative..."
        />

        <div className="controls">
          <label htmlFor="voice">Voice</label>
          <select id="voice" value={voice} onChange={(e) => setVoice(e.target.value)}>
            <option value="alloy">Alloy</option>
            <option value="aria">Aria</option>
            <option value="verse">Verse</option>
          </select>
          <button onClick={handleGenerate} disabled={status === "loading"}>
            {status === "loading" ? "Generating..." : "Generate TTS Preview"}
          </button>
        </div>
      </section>

      <section className="preview panel">
        <h2>Audio Preview</h2>
        {audioUrl ? (
          <audio controls src={audioUrl} className="audio" />
        ) : (
          <p className="placeholder">No preview yet. Generate one from the script panel.</p>
        )}
      </section>

      <section className="insight panel">
        <h2>Execution Notes</h2>
        <ul>
          <li>Keep scenes under 4 seconds unless explanation demands longer pacing.</li>
          <li>Animate one dominant element per beat; avoid competing motion vectors.</li>
          <li>Use one accent color for CTA moments and keep background neutrals stable.</li>
        </ul>
      </section>
    </main>
  );
}
