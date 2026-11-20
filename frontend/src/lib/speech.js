// Pronunciation with the device's German voice. If the device has no German voice, the
// browser would read German words with an English accent, so we look for a real German one.
const synth = typeof window !== "undefined" ? window.speechSynthesis : null;

// Voices that sound natural, best first (macOS, Chrome, Windows/Edge names).
const GOOD_VOICES = [/anna/i, /petra/i, /markus/i, /yannick/i, /helena/i, /google deutsch/i, /katja/i, /conrad/i, /hedda/i, /stefan/i];

export function germanVoice() {
  if (!synth) return null;
  // Asked again every time: Safari and Chrome load their voice list late.
  const voices = synth.getVoices().filter((v) => /^de([-_]|$)/i.test(v.lang));
  for (const re of GOOD_VOICES) {
    const v = voices.find((x) => re.test(x.name));
    if (v) return v;
  }
  return voices.find((v) => v.localService) || voices[0] || null;
}

// Call fn when the browser has (re)loaded its voices; returns a function that stops listening.
export function onVoicesChanged(fn) {
  if (!synth || !synth.addEventListener) return () => {};
  synth.addEventListener("voiceschanged", fn);
  return () => synth.removeEventListener("voiceschanged", fn);
}

export const canSpeak = !!synth;

export function say(text) {
  if (!synth || !text) return;
  synth.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "de-DE";
  u.rate = 0.9;
  const voice = germanVoice();
  if (voice) u.voice = voice;
  synth.speak(u);
}

export function stopSpeaking() {
  if (synth) synth.cancel();
}

export function formatTime(totalSeconds) {
  const s = Math.max(0, Math.floor(totalSeconds));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

export function formatDate(iso, withTime = false) {
  if (!iso) return "";
  const d = new Date(iso);
  const opts = { day: "numeric", month: "short", year: "numeric" };
  if (withTime) Object.assign(opts, { hour: "2-digit", minute: "2-digit" });
  return d.toLocaleString("en-GB", opts);
}

export function plural(n, word, many) {
  return `${n} ${n === 1 ? word : many || word + "s"}`;
}
