import { useId, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import Icon from "../../components/Icon";
import { useToast } from "../../components/Toasts";
import SetRunner, { BestBadge, formatSeconds, ModeSwitch, readMode, saveMode } from "../../components/practice/SetRunner";
import { Async, Empty, PageHead } from "../../components/ui";
import { api } from "../../lib/api";
import { useApi, useLevelKey, useTitle } from "../../lib/hooks";
import { formatDate } from "../../lib/speech";
import { useSession } from "../../lib/session";

const SOURCE = {
  lesson: <span className="badge badge-royal">From the lesson</span>,
  extra: <span className="badge badge-note">Extra</span>,
  both: <><span className="badge badge-royal">From the lesson</span><span className="badge badge-note">+ Extra</span></>,
};
const KIND = { choice: "choose the answer", blanks: "type the missing word", tf: "richtig oder falsch", listen_type: "listen and write" };
const num = (title) => (title.match(/^Lektion\s+(\d+)/i) || [])[1];

// ---------------- /lektionen ----------------
export function LektionenList() {
  useTitle("Meine Lektionen");
  const { user } = useSession();
  const t = user.is_teacher;
  const state = useApi("/lektionen/", [useLevelKey()]);
  const toast = useToast();
  const [busy, setBusy] = useState(null);

  const toggle = async (row) => {
    if (busy) return;
    setBusy(row.id);
    try {
      const res = await api(`/teacher/lektionen/${row.id}/taught/`, { method: "POST", body: { taught: !row.is_taught } });
      state.setData((d) => ({ ...d, lektionen: d.lektionen.map((x) => (x.id === row.id ? { ...x, is_taught: res.is_taught, taught_at: res.taught_at } : x)) }));
      toast(res.message);
    } catch (e) {
      toast(e.message, "error");
    } finally {
      setBusy(null);
    }
  };

  return (
    <Async state={state}>
      {({ level, lektionen }) => (
        <>
          <PageHead title="Meine Lektionen">
            <p className="muted">
              {t ? "After the Zoom class, mark the Lektion as taught. Then your students can open it and practise."
                : "Revise what you learned in class. A new Lektion opens after it's been taught."}
            </p>
          </PageHead>
          {lektionen.length === 0 ? (
            <Empty title="No Lektionen yet">{t ? "Add Lektionen under Content → Your sections." : `Your teacher hasn't added any ${level?.code} Lektionen yet.`}</Empty>
          ) : (
            <ul className="list lk-list">
              {lektionen.map((x, i) => {
                const open = x.is_taught || t;
                const n = num(x.title) || "·";
                const pct = x.sets ? Math.round((x.sets_done / x.sets) * 100) : 0;
                const sub = x.is_taught || t
                  ? [x.sets && `${x.sets} practice sets`, x.words && `${x.words} words`, x.writing && `${x.writing} writing tasks`].filter(Boolean).join(" · ") || x.description
                  : "Opens after the class";
                const inner = (
                  <>
                    <span className="lk-num" aria-hidden="true">{n}</span>
                    <span className="row-main">
                      <span className="row-title" lang="de">{x.title}</span>
                      <span className="row-sub">{sub}{t && !x.is_visible ? " · hidden from students" : ""}</span>
                    </span>
                  </>
                );
                if (t) {
                  return (
                    <li key={x.id} className="row lk-teacher-row">
                      <Link className="lk-teacher-link" to={`/sections/${x.id}`}>{inner}</Link>
                      <span className="row-end">
                        {x.is_taught && x.taught_at && <span className="muted small lk-when">since {formatDate(x.taught_at)}</span>}
                        <button className={`btn btn-small ${x.is_taught ? "btn-secondary" : "btn-primary"}`} type="button"
                          aria-pressed={x.is_taught} aria-disabled={busy === x.id} onClick={() => toggle(x)}>
                          {x.is_taught ? <><Icon name="check" />Taught</> : "Mark as taught"}
                        </button>
                      </span>
                    </li>
                  );
                }
                return (
                  <li key={x.id}>
                    {open ? (
                      <Link className="row" to={`/sections/${x.id}`}>
                        {inner}
                        <span className="row-end">
                          {x.sets_done > 0
                            ? <span className="meter meter-mini meter-good" role="img" aria-label={`${x.sets_done} of ${x.sets} practice sets done`}><span style={{ width: `${pct}%` }} /></span>
                            : <span className="badge badge-royal">New</span>}
                          <span className="chev"><Icon name="chevron" /></span>
                        </span>
                      </Link>
                    ) : (
                      <div className="row lk-locked" aria-disabled="true">
                        {inner}
                        <span className="row-end"><span className="lk-lock"><Icon name="lock" />Not taught yet</span></span>
                      </div>
                    )}
                  </li>
                );
              })}
            </ul>
          )}
        </>
      )}
    </Async>
  );
}

// ---------------- /sections/:id ----------------
const TABS = [["uebungen", "Übungen"], ["regeln", "Regeln"], ["woerter", "Wörter"], ["schreiben", "Schreiben"]];

export function LektionPage() {
  const { id } = useParams();
  const [params, setParams] = useSearchParams();
  const tab = TABS.some(([k]) => k === params.get("tab")) ? params.get("tab") : "uebungen";
  const state = useApi(`/lektionen/${id}/`);
  useTitle(state.data?.section.title);
  const { user } = useSession();
  return (
    <Async state={state}>
      {(d) => {
        const counts = { uebungen: d.sets.length, regeln: d.pages.length, woerter: d.words.length, schreiben: d.writing.length };
        return (
          <>
            <PageHead crumb={{ to: "/lektionen", label: "Meine Lektionen" }} title={d.section.title} lang="de">
              {d.section.description && <p className="muted">{d.section.description}</p>}
              {user.is_teacher && !d.section.is_taught && <p className="badge badge-note">Not taught yet: students can't open it.</p>}
            </PageHead>
            {d.section.goals?.length > 0 && (
              <ul className="lk-goals" aria-label="What you learn">
                {d.section.goals.map((g, i) => <li key={i}><Icon name="check" /><span><b>{g.title}</b>{g.text && <span className="muted"> · {g.text}</span>}</span></li>)}
              </ul>
            )}
            <div className="content-tabs" role="tablist" aria-label="Parts of the Lektion">
              {TABS.map(([k, label]) => (
                <button key={k} type="button" role="tab" aria-selected={k === tab} onClick={() => setParams(k === "uebungen" ? {} : { tab: k }, { replace: true })}>
                  {label}<span className="tab-count">{counts[k]}</span>
                </button>
              ))}
            </div>
            {tab === "uebungen" && <SetsTab d={d} />}
            {tab === "regeln" && <RulesTab d={d} />}
            {tab === "woerter" && <WordsTab d={d} />}
            {tab === "schreiben" && <WritingTab d={d} setData={state.setData} />}
          </>
        );
      }}
    </Async>
  );
}

function SetsTab({ d }) {
  const [mode, setMode] = useState(readMode);
  if (!d.sets.length) return <Empty title="No practice sets yet">Your teacher is still preparing them.</Empty>;
  return (
    <>
      <ModeSwitch mode={mode} onChange={(m) => { setMode(m); saveMode(m); }} />
      <ul className="list">
        {d.sets.map((x) => (
          <li key={x.id}>
            <Link className="row lk-set" to={`/sections/${d.section.id}/sets/${x.id}`}>
              <span className="row-main">
                <span className="row-title"><span lang="de">{x.title}</span>{SOURCE[x.source]}</span>
                <span className="row-sub">
                  {x.questions} questions · {KIND[x.kind]} · {mode === "exam" ? `${formatSeconds(x.seconds)} min, result at the end` : "feedback after every answer"}
                  {!x.is_published && " · Draft (only you see it)"}
                </span>
              </span>
              <span className="row-end">
                <BestBadge best={x.best} />
                <span className={`badge ${mode === "exam" ? "badge-note" : "badge-royal"} ex-mode-badge`}>{mode === "exam" ? <><Icon name="clock" />Prüfung</> : "Üben"}</span>
                <span className="chev"><Icon name="chevron" /></span>
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </>
  );
}

function RulesTab({ d }) {
  if (!d.pages.length) return <Empty title="No rule pages yet">Your teacher is still preparing them.</Empty>;
  return (
    <ul className="list">
      {d.pages.map((p) => (
        <li key={p.id}>
          <Link className="row" to={`/sections/${d.section.id}/lessons/${p.id}`}>
            <Icon name="book" />
            <span className="row-main">
              <span className="row-title" lang="de">{p.title}</span>
              {p.summary && <span className="row-sub">{p.summary}{!p.is_published && " · Draft (only you see it)"}</span>}
            </span>
            <span className="row-end"><span className="chev"><Icon name="chevron" /></span></span>
          </Link>
        </li>
      ))}
    </ul>
  );
}

function WordRow({ w }) {
  return (
    <li>
      <b lang="de">{w.article && <span className={`art art-${w.article}`}>{w.article} </span>}{w.german}</b>
      <span className="muted">{w.english}</span>
      {w.extra && <span className="badge badge-note">Extra</span>}
    </li>
  );
}

function WordsTab({ d }) {
  if (!d.words.length) return <Empty title="No words yet">Your teacher is still preparing the word list.</Empty>;
  const lesson = d.words.filter((w) => !w.extra);
  const extra = d.words.filter((w) => w.extra);
  return (
    <>
      {d.topic && (
        <section className="focus-card paper lk-words-start">
          <div><h2>Practise all {d.words.length} words</h2><p>Flashcards: see the word, say it, check if you knew it. Words you miss come back sooner.</p></div>
          <Link className="btn btn-primary" to={`/words/${d.topic.level}/${d.topic.slug}/study`}>Start flashcards</Link>
        </section>
      )}
      <h2 className="lk-h2">From the lesson ({lesson.length})</h2>
      <ul className="lsn-card lsn-words lk-words">{lesson.map((w, i) => <WordRow key={i} w={w} />)}</ul>
      {extra.length > 0 && (
        <>
          <h2 className="lk-h2">Extra words for this topic ({extra.length})</h2>
          <ul className="lsn-card lsn-words lk-words">{extra.map((w, i) => <WordRow key={i} w={w} />)}</ul>
        </>
      )}
    </>
  );
}

function WritingTab({ d, setData }) {
  if (!d.writing.length) return <Empty title="No writing tasks yet">Your teacher is still preparing them.</Empty>;
  const update = (task) => setData((x) => ({ ...x, writing: x.writing.map((t) => (t.id === task.id ? task : t)) }));
  return (
    <>
      <p className="muted">Write your answer and send it. Your teacher checks it and writes a comment.</p>
      {d.writing.map((t) => <WritingTask key={t.id} task={t} onSaved={update} />)}
    </>
  );
}

function WritingTask({ task, onSaved }) {
  const id = useId();
  const toast = useToast();
  const a = task.answer;
  const [editing, setEditing] = useState(!a);
  const [text, setText] = useState(a?.text || "");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const send = async (e) => {
    e.preventDefault();
    if (busy) return;
    if (!text.trim()) { setError("Write your answer first."); return; }
    setBusy(true);
    try {
      const res = await api(`/writing/${task.id}/`, { method: "POST", body: { text } });
      onSaved(res.task);
      setEditing(false);
      setError("");
      toast(res.message);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="panel lk-task">
      <div className="lk-task-head">
        <div><h3 lang="de">{task.title}</h3>{task.source && <span className="lk-note">{task.source}</span>}</div>
        {a && !editing && (a.status === "checked"
          ? <span className="badge badge-good">Checked</span>
          : <span className="badge badge-royal">Sent · waiting for your teacher</span>)}
      </div>
      <p className="lk-prompt">{task.prompt}</p>
      {editing ? (
        <form className="lk-write" onSubmit={send} noValidate>
          <label className="visually-hidden" htmlFor={id}>Your answer</label>
          <textarea id={id} lang="de" rows={5} value={text} placeholder="Schreib hier …" maxLength={5000}
            aria-invalid={!!error} onChange={(e) => setText(e.target.value)} />
          {error && <p className="error" role="alert">{error}</p>}
          <div className="ex-actions">
            {a && <button className="btn btn-quiet btn-small" type="button" onClick={() => { setEditing(false); setText(a.text); setError(""); }}>Cancel</button>}
            <button className="btn btn-primary btn-small" type="submit" aria-disabled={busy}>{busy ? "Sending…" : a ? "Send again" : "Send to your teacher"}</button>
          </div>
        </form>
      ) : (
        <>
          <div className="lk-answer" lang="de">{a.text}</div>
          {a.status === "checked" && a.feedback && <div className="lk-comment"><b>Your teacher:</b> {a.feedback}</div>}
          <div className="ex-actions">
            <span className="muted small">Sent {formatDate(a.submitted_at, true)}</span>
            <button className="btn btn-secondary btn-small" type="button" onClick={() => setEditing(true)}><Icon name="pencil" />Change and send again</button>
          </div>
        </>
      )}
    </section>
  );
}

// ---------------- /sections/:sectionId/sets/:id ----------------
export function PracticeSetPage() {
  const { sectionId, id } = useParams();
  const state = useApi(`/practice-sets/${id}/`);
  useTitle(state.data?.set.title);
  return (
    <Async state={state}>
      {({ set, section }) => {
        const save = async (score, timed) => (await api(`/practice-sets/${set.id}/result/`, { method: "POST", body: { score, timed } })).best;
        return (
          <SetRunner key={set.id} title={set.title} crumb={{ to: `/sections/${sectionId || section.id}`, label: section.title }}
            intro={set.intro} kind={set.kind} text={set.text} items={set.items} example={set.example} seconds={set.seconds} onSave={save} />
        );
      }}
    </Async>
  );
}
