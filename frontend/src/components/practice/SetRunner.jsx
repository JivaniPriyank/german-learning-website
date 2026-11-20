import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import Icon from "../Icon";
import { PageHead } from "../ui";
import { accepted, ClockFace } from "../lesson/Blocks";
import { canSpeak, germanVoice, onVoicesChanged, say, stopSpeaking } from "../../lib/speech";

// One runner for every practice set (Lektion sets and exam practice).
// Kinds: "choice", "blanks", "tf" (with a reading text), "listen_type".
// Modes: "practice" shows right or wrong after every answer; "exam" has a timer and shows the result at the end.

export const PASS = 60; // about 60% passes the real A1 exam

export function readMode() {
  try { return localStorage.getItem("gl-exam-mode") === "exam" ? "exam" : "practice"; } catch { return "practice"; }
}
export function saveMode(mode) {
  try { localStorage.setItem("gl-exam-mode", mode); } catch { /* private window: this visit only */ }
}

export function ModeSwitch({ mode, onChange }) {
  return (
    <div className="ex-mode-wrap">
      <div className="ex-mode" role="group" aria-label="How to practise">
        <button type="button" aria-pressed={mode === "practice"} onClick={() => onChange("practice")}><b>Üben</b><span>Right or wrong after every answer</span></button>
        <button type="button" aria-pressed={mode === "exam"} onClick={() => onChange("exam")}><b>Prüfung</b><span>With a timer, result at the end</span></button>
      </div>
      <p className={`ex-mode-hint ${mode === "exam" ? "is-exam" : ""}`} role="status">
        {mode === "exam"
          ? <><Icon name="clock" /><span><b>Prüfung (exam mode):</b> a timer runs and you see no corrections while you answer. Hand in at the end to see your score and every correction. Test yourself like in the real exam.</span></>
          : <><Icon name="check" /><span><b>Üben (practice mode):</b> after every answer you see straight away if it's right, with the correct answer and why. No time limit. Best for revising after class.</span></>}
      </p>
    </div>
  );
}

export const formatSeconds = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;

export function BestBadge({ best }) {
  if (best == null) return null;
  return <span className={`badge ${best >= PASS ? "badge-good" : "badge-bad"}`}>best {best}%</span>;
}

export function VoiceNote() {
  const [voice, setVoice] = useState(() => germanVoice());
  useEffect(() => onVoicesChanged(() => setVoice(germanVoice())), []);
  if (!canSpeak) return <p className="ex-voice is-warn">This browser can't play the audio.</p>;
  if (voice) return <p className="ex-voice">German voice: {voice.name}</p>;
  return (
    <p className="ex-voice is-warn">
      No German voice on this device yet, so the audio may sound English. On a Mac: System Settings → Accessibility → Spoken
      Content → System voice → Manage Voices → German. On Windows: Settings → Time &amp; language → Speech → Add voices → Deutsch.
    </p>
  );
}

function isRight(kind, item, given) {
  if (given === null || given === undefined || given === "") return false;
  if (kind === "blanks" || kind === "listen_type") return accepted(String(given), String(item.answer));
  return given === item.answer;
}
const firstAnswer = (a) => String(a).split("|")[0];
function shown(kind, item, v) {
  if (v === null || v === undefined || v === "") return "–";
  if (kind === "choice") return item.options[v];
  if (kind === "tf") return v ? "richtig" : "falsch";
  return String(v);
}
function rightAnswer(kind, item) {
  if (kind === "choice") return item.options[item.answer];
  if (kind === "tf") return item.answer ? "richtig" : "falsch";
  return firstAnswer(item.answer);
}
function questionText(kind, item) {
  if (kind === "blanks") return `${item.before || ""} ___ ${item.after || ""}`.trim();
  if (kind === "listen_type") return "Listen and write";
  if (item.clock) return item.prompt || `Clock: ${item.clock}`;
  return item.prompt || "Listen and choose";
}

function Timer({ seconds }) {
  return (
    <span className={`badge badge-royal ex-timer${seconds <= 30 ? " is-low" : ""}`} role="timer" aria-label="Time left">
      {Math.floor(seconds / 60)}:{String(seconds % 60).padStart(2, "0")} left
    </span>
  );
}

function PlayButton({ text, disabled, onPlay, big }) {
  if (!canSpeak) return null;
  return (
    <button className={big ? "lsn-play" : "lsn-play-small"} type="button" aria-label="Listen" aria-disabled={disabled}
      onClick={() => { if (!disabled) { onPlay?.(); say(text); } }}>
      <Icon name="play" />
    </button>
  );
}

// ---------------- one question ----------------
function Question({ kind, item, i, value, checked, exam, playsLeft, onPlay, onChange, onCheck }) {
  const done = !exam && checked;
  const ok = done && isRight(kind, item, value);
  const feedback = done && (
    <div className={`lsn-feedback ${ok ? "is-right" : "is-wrong"}`} role="status">
      <b>{ok ? "Richtig!" : "Not quite."}</b>{" "}
      {!ok && (kind === "blanks" || kind === "listen_type") && <>It's <b lang="de">{rightAnswer(kind, item)}</b>. </>}
      {item.explain}
    </div>
  );
  const audioLimit = exam && playsLeft != null;

  if (kind === "choice") {
    const long = item.options.some((o) => String(o).length > 14);
    return (
      <div className="lk-q">
        <div className="lsn-question">
          {item.clock && <ClockFace h={+item.clock.slice(0, 2)} m={+item.clock.slice(3, 5)} size={120} />}
          {item.say && <PlayButton big={!item.prompt} text={item.say} disabled={audioLimit && playsLeft <= 0} onPlay={onPlay} />}
          <div className="ex-question">
            <p className="lsn-prompt" lang="de">{i + 1}. {item.prompt || (item.clock ? "Wie spät ist es?" : "Listen and choose.")}</p>
            {audioLimit && <span className="small muted">You can listen {playsLeft} more time{playsLeft === 1 ? "" : "s"}.</span>}
          </div>
        </div>
        <div className={`lsn-options${long ? " lsn-options-col" : ""}`} lang="de">
          {item.options.map((o, j) => {
            const cls = done ? (j === item.answer ? "is-right" : j === value ? "is-wrong" : "") : j === value ? "is-picked" : "";
            return (
              <button key={j} type="button" className={`lsn-option ${cls}`} aria-disabled={done} aria-pressed={j === value}
                onClick={() => { if (done) return; onChange(j); if (!exam) onCheck(); }}>
                {long && <span className="ex-key" aria-hidden="true">{"abcdef"[j]}</span>}{o}
              </button>
            );
          })}
        </div>
        {feedback}
      </div>
    );
  }

  if (kind === "tf") {
    return (
      <div className={`lk-q ex-tf${done ? (ok ? " is-right" : " is-wrong") : ""}`}>
        <div className="ex-tf-row">
          <span lang="de">{i + 1}. {item.prompt}</span>
          <span className="chips" role="group" aria-label={`Satz ${i + 1}`}>
            {[true, false].map((v) => (
              <button key={String(v)} className="chip" type="button" aria-pressed={value === v} aria-disabled={done}
                onClick={() => { if (done) return; onChange(v); if (!exam) onCheck(); }}>{v ? "richtig" : "falsch"}</button>
            ))}
          </span>
        </div>
        {feedback}
      </div>
    );
  }

  // blanks and listen_type: type the answer
  const input = (
    <input type="text" lang="de" autoComplete="off" autoCapitalize="off" spellCheck={false}
      aria-label={kind === "blanks" ? `Sentence ${i + 1}: the missing word` : `Question ${i + 1}: what you heard`}
      className={done ? (ok ? "is-right" : "is-wrong") : ""}
      value={value ?? ""} readOnly={done} onChange={(e) => onChange(e.target.value)} />
  );
  return (
    <div className="lk-q">
      <form className={`lsn-blank-line${done ? (ok ? " is-right" : " is-wrong") : ""}`} noValidate
        onSubmit={(e) => { e.preventDefault(); if (!exam && String(value ?? "").trim()) onCheck(); }}>
        {kind === "listen_type" ? (
          <>
            <span className="ex-num">{i + 1}.</span>
            <PlayButton text={item.say} disabled={audioLimit && playsLeft <= 0} onPlay={onPlay} />
            {input}
          </>
        ) : (
          <>
            <span lang="de">{i + 1}. {item.before}</span>{input}<span lang="de">{item.after}</span>
            {item.hint && <span className="lk-hint" lang="de">{item.hint}</span>}
          </>
        )}
        {!exam && !done && <button className="btn btn-secondary btn-small" type="submit">Check</button>}
        {done && ok && <span className="lsn-mark-right"><Icon name="check" label="Right" /></span>}
      </form>
      {done && (!ok || item.explain) && feedback}
    </div>
  );
}

// ---------------- the worked example at the top ----------------
const HOW = {
  blanks: "Type the missing word in the box, then press Check (or Enter).",
  choice: "Click the right answer.",
  tf: "Read the text, then click richtig (true) or falsch (false) for each sentence.",
  listen_type: "Press play, listen, then type what you hear and press Check.",
};

function ExampleBox({ kind, item }) {
  const howListen = kind === "choice" && item.say ? "Press play, listen, then click the right answer." : HOW[kind];
  let body;
  if (kind === "blanks") {
    body = (
      <p className="ex-example-line" lang="de">
        {item.before} <span className="ex-filled">{firstAnswer(item.answer)}</span> {item.after}
      </p>
    );
  } else if (kind === "listen_type") {
    body = (
      <div className="ex-example-line">
        <PlayButton text={item.say} />
        <span className="ex-filled" lang="de">{firstAnswer(item.answer)}</span>
      </div>
    );
  } else if (kind === "tf") {
    body = (
      <div className="ex-tf-row">
        <span lang="de">{item.prompt}</span>
        <span className="chips">
          {[true, false].map((v) => <span key={String(v)} className={`chip ${v === item.answer ? "ex-chip-right" : ""}`}>{v ? "richtig" : "falsch"}</span>)}
        </span>
      </div>
    );
  } else {
    body = (
      <>
        <div className="lsn-question">
          {item.clock && <ClockFace h={+item.clock.slice(0, 2)} m={+item.clock.slice(3, 5)} size={96} />}
          {item.say && <PlayButton text={item.say} />}
          {item.prompt && <p className="lsn-prompt" lang="de">{item.prompt}</p>}
        </div>
        <div className="lsn-options" lang="de">
          {item.options.map((o, j) => <span key={j} className={`lsn-option ex-option-static ${j === item.answer ? "is-right" : ""}`}>{o}</span>)}
        </div>
      </>
    );
  }
  return (
    <div className="ex-example">
      <p className="ex-example-head"><b>Beispiel</b> · {howListen}</p>
      {body}
      {item.explain && <p className="ex-example-why">{item.explain}</p>}
    </div>
  );
}

// ---------------- the runner ----------------
export default function SetRunner({ title, crumb, intro, kind, text, items, example, seconds, maxPlays, onSave, lang = "de" }) {
  const [mode, setMode] = useState(readMode);
  const exam = mode === "exam";
  const n = items.length;
  const blank = () => items.map(() => null);
  const [values, setValues] = useState(blank);
  const [checked, setChecked] = useState(() => items.map(() => false));
  const [plays, setPlays] = useState(() => items.map(() => 0));
  const [left, setLeft] = useState(seconds);
  const [result, setResult] = useState(null);
  const valuesRef = useRef(values);
  valuesRef.current = values;

  const finish = async () => {
    stopSpeaking();
    const given = valuesRef.current;
    const right = items.filter((it, i) => isRight(kind, it, given[i])).length;
    setResult({ right, given, best: null });
    window.scrollTo(0, 0);
    try {
      const best = await onSave(right, exam);
      setResult((r) => r && { ...r, best });
    } catch { /* the result still shows; it just isn't saved */ }
  };

  useEffect(() => {
    if (!exam || result) return undefined;
    const t = setInterval(() => setLeft((s) => s - 1), 1000);
    return () => clearInterval(t);
  }, [exam, result]);
  useEffect(() => { if (exam && left <= 0 && !result) finish(); }); // time's up: hand in
  useEffect(() => () => stopSpeaking(), []);

  const again = () => {
    setValues(blank()); setChecked(items.map(() => false)); setPlays(items.map(() => 0));
    setLeft(seconds); setResult(null); window.scrollTo(0, 0);
  };
  const switchMode = () => {
    const m = exam ? "practice" : "exam";
    saveMode(m); setMode(m); stopSpeaking(); again();
  };

  if (result) {
    const { right, given, best } = result;
    const pct = Math.round((right / n) * 100);
    return (
      <>
        <PageHead crumb={crumb} title={title} lang={lang} />
        <div className={`lsn-done${right === n ? " is-perfect" : ""}`}>
          <span>
            <b>{right === n ? "Perfekt!" : pct >= PASS ? "Gut gemacht!" : "Keep practising."}</b> {right} of {n} right · {pct}%.
            {best != null && best > pct ? ` Your best: ${best}%.` : ""}
          </span>
          <button className="btn btn-secondary btn-small" type="button" onClick={again}><Icon name="again" />Try again</button>
        </div>
        <section className="section">
          <h2>Your answers</h2>
          <ul className="list ex-review">
            {items.map((it, i) => {
              const ok = isRight(kind, it, given[i]);
              return (
                <li className="row" key={i}>
                  <span className="row-main">
                    <span className="row-title" lang="de">{i + 1}. {questionText(kind, it)}</span>
                    <span className="row-sub" lang="de">
                      Your answer: {shown(kind, it, given[i])}{!ok && <> · Right: <b>{rightAnswer(kind, it)}</b></>}
                      {it.explain ? ` · ${it.explain}` : ""}
                    </span>
                  </span>
                  <span className="row-end"><span className={`badge ${ok ? "badge-good" : "badge-bad"}`}>{ok ? "Right" : "Wrong"}</span></span>
                </li>
              );
            })}
          </ul>
        </section>
        <div className="ex-actions"><Link className="btn btn-primary" to={crumb.to}>Done</Link></div>
      </>
    );
  }

  const answered = values.filter((v) => v !== null && v !== "").length;
  const ready = exam ? answered === n : checked.every(Boolean);
  const hasAudio = kind === "listen_type" || items.some((it) => it.say);
  return (
    <>
      <PageHead crumb={crumb} title={title} lang={lang} actions={exam ? <Timer seconds={Math.max(0, left)} /> : null}>
        {intro && <p className="muted" lang="de">{intro}</p>}
      </PageHead>
      <div className={`ex-mode-bar ${exam ? "is-exam" : ""}`}>
        <Icon name={exam ? "clock" : "check"} />
        <span>{exam
          ? <><b>Prüfung:</b> {formatSeconds(seconds)} for {n} questions. Corrections come after you hand in.</>
          : <><b>Üben:</b> you see right or wrong after every answer.</>}</span>
        <button className="btn btn-quiet btn-small" type="button" onClick={switchMode}>
          {exam ? "Switch to Üben" : "Switch to Prüfung"}
        </button>
      </div>
      <section className="panel">
        <div className="lsn-block lsn-exercise">
          {hasAudio && <VoiceNote />}
          {text && <div className="ex-text paper" lang="de">{text}</div>}
          {example && <ExampleBox kind={kind} item={example} />}
          {example && <p className="ex-now">Now you:</p>}
          {items.map((it, i) => (
            <Question key={i} kind={kind} item={it} i={i} value={values[i]} checked={checked[i]} exam={exam}
              playsLeft={maxPlays ? maxPlays - plays[i] : null}
              onPlay={() => setPlays((p) => p.map((x, j) => (j === i ? x + 1 : x)))}
              onChange={(v) => setValues((a) => a.map((x, j) => (j === i ? v : x)))}
              onCheck={() => setChecked((c) => c.map((x, j) => (j === i ? true : x)))} />
          ))}
          <div className="ex-actions">
            <span className="muted small">{exam ? `${answered} of ${n} answered` : `${checked.filter(Boolean).length} of ${n} checked`}</span>
            <button className="btn btn-primary btn-small" type="button" aria-disabled={!ready} onClick={() => ready && finish()}>
              {exam ? "Hand in" : "See result"}<Icon name="chevron" />
            </button>
          </div>
        </div>
      </section>
    </>
  );
}
