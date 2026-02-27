/**
 * [INPUT]: Receives JSON payload with text/voice from webapp UI; depends on external TTS endpoint env vars.
 * [OUTPUT]: Returns audio bytes when provider succeeds, or JSON error payload on failure.
 * [POS]: webapp/src/app/api/tts backend adapter; keeps browser free of provider credentials.
 * [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
 */
import { NextRequest, NextResponse } from "next/server";

type Body = {
  text?: string;
  voice?: string;
};

function jsonError(error: string, status = 400) {
  return NextResponse.json({ ok: false, error }, { status });
}

export async function POST(req: NextRequest) {
  let body: Body;

  try {
    body = (await req.json()) as Body;
  } catch {
    return jsonError("Invalid JSON body.");
  }

  const text = (body.text || "").trim();
  const voice = (body.voice || "alloy").trim();

  if (!text) {
    return jsonError("text is required.");
  }

  const endpoint = process.env.TTS_ENDPOINT;
  const apiKey = process.env.TTS_API_KEY;

  if (!endpoint || !apiKey) {
    return jsonError(
      "TTS backend is not configured. Set TTS_ENDPOINT and TTS_API_KEY.",
      501,
    );
  }

  try {
    const upstream = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        text,
        voice,
        format: "mp3",
      }),
      cache: "no-store",
    });

    if (!upstream.ok) {
      const errText = await upstream.text();
      return jsonError(`Upstream TTS failed: ${upstream.status} ${errText}`, 502);
    }

    const contentType = upstream.headers.get("content-type") || "audio/mpeg";

    if (contentType.includes("application/json")) {
      const payload = await upstream.json().catch(() => ({}));
      return jsonError(payload?.error || "Upstream returned JSON instead of audio.", 502);
    }

    const bytes = await upstream.arrayBuffer();
    return new NextResponse(bytes, {
      status: 200,
      headers: {
        "Content-Type": contentType,
        "Cache-Control": "no-store",
      },
    });
  } catch (error) {
    const reason = error instanceof Error ? error.message : "Unknown upstream error";
    return jsonError(`TTS request failed: ${reason}`, 502);
  }
}
