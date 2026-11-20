import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import Icon from "../../components/Icon";
import { Async, Empty, PageHead } from "../../components/ui";
import { api } from "../../lib/api";
import { useApi, useLevelKey, useTitle } from "../../lib/hooks";
import SetRunner, { BestBadge, ModeSwitch, readMode, saveMode } from "../../components/practice/SetRunner";

const MODULE_ICONS = { hoeren: "headphones", lesen: "book", schreiben: "pencil", sprechen: "chat" };
// ---------------- /exams ----------------
export function ExamsHome() {
  useTitle("Exam practice");
  const state = useApi("/exams/", [useLevelKey()]);
  const [mode, setMode] = useState(readMode);
  const pick = (m) => { setMode(m); saveMode(m); };
  return (
    <Async state={state}>
      {({ level, exams }) => (
        <>
          <PageHead title="Exam practice">
            <p className="muted">Practise every part of the {level?.code} exam the way it really looks, with our own texts and audio.</p>
          </PageHead>
          {exams.length === 0 ? (
            <Empty title="No exam practice yet">Your teacher is still preparing exam practice for this level.</Empty>
          ) : (
            <>
              <ModeSwitch mode={mode} onChange={pick} />
              {exams.map((ex) => (
                <section className="section" key={ex.id}>
                  <div className="ex-exam-head"><h2>{ex.name}</h2>{ex.sub && <span className="muted small">{ex.sub}</span>}</div>
                  <ul className="list">
                    {ex.modules.map((m) => {
                      const tried = m.parts.filter((p) => p.best != null);
                      const best = tried.length ? Math.round(tried.reduce((a, p) => a + p.best, 0) / tried.length) : null;
                      return (
                        <li key={m.key}>
                          <Link className="row" to={`/exams/${ex.id}/${m.key}`}>
                            <Icon name={MODULE_ICONS[m.key]} />
                            <span className="row-main">
                              <span className="row-title" lang="de">{m.name}</span>
                              <span className="row-sub">
                                Teil {m.teile.join(", ")} · {m.parts.length} practice set{m.parts.length === 1 ? "" : "s"} · real exam about {m.minutes} min
                              </span>
                            </span>
                            <span className="row-end"><BestBadge best={best} /><span className="chev"><Icon name="chevron" /></span></span>
                          </Link>
                        </li>
                      );
                    })}
                  </ul>
                </section>
              ))}
            </>
          )}
        </>
      )}
    </Async>
  );
}

// ---------------- /exams/:exam/:module ----------------
export function ExamModule() {
  const { exam, module } = useParams();
  const state = useApi("/exams/", [useLevelKey()]);
  const ex = state.data?.exams.find((e) => e.id === exam);
  const m = ex?.modules.find((x) => x.key === module);
  useTitle(m ? `${m.name} · ${ex.name}` : "Exam practice");
  const mode = readMode();
  return (
    <Async state={state}>
      {() => !m ? (
        <Empty title="Nothing here" action={<Link className="btn btn-primary" to="/exams">Back to exam practice</Link>}>
          This part has no practice sets at your level.
        </Empty>
      ) : (
        <>
          <PageHead crumb={{ to: "/exams", label: "Exam practice" }} title={m.name} lang="de">
            <p className="muted">{ex.name} · {mode === "exam" ? "Prüfung: with a timer, result at the end" : "Üben: right or wrong after every answer"}</p>
          </PageHead>
          <ul className="list">
            {m.parts.map((p) => (
              <li key={p.id}>
                <Link className="row" to={`/exams/parts/${p.id}`}>
                  <span className="row-main">
                    <span className="row-title" lang="de">Teil {p.teil}: {p.title}</span>
                    <span className="row-sub">
                      {p.questions} {p.kind === "tf" ? "sentences · richtig oder falsch" : "questions · a, b oder c"} · {p.minutes} min in exam mode
                      {!p.is_published && " · Draft (only you see it)"}
                    </span>
                  </span>
                  <span className="row-end"><BestBadge best={p.best} /><span className="chev"><Icon name="chevron" /></span></span>
                </Link>
              </li>
            ))}
          </ul>
        </>
      )}
    </Async>
  );
}

// ---------------- /exams/parts/:id ----------------
export function ExamPart() {
  const { id } = useParams();
  const state = useApi(`/exams/parts/${id}/`);
  useTitle(state.data ? `${state.data.part.module_name} Teil ${state.data.part.teil}` : "Exam practice");
  return (
    <Async state={state}>
      {({ part }) => {
        // Exam parts use the same runner as the Lektion sets: "listen" is a choice with audio.
        const kind = part.kind === "listen" ? "choice" : "tf";
        const items = part.items.map((it) => (kind === "choice"
          ? { prompt: it.q, say: it.audio, options: it.options, answer: it.answer, explain: it.explain }
          : { prompt: it.q, answer: it.answer, explain: it.explain }));
        const ex = part.example;
        const example = !ex ? null : kind === "choice"
          ? { prompt: ex.q, say: ex.audio, options: ex.options, answer: ex.answer, explain: ex.explain }
          : { prompt: ex.q, answer: ex.answer, explain: ex.explain };
        const save = async (score, timed) => {
          const res = await api(`/exams/parts/${part.id}/result/`, { method: "POST", body: { score, timed } });
          return res.best == null ? null : Math.round((res.best * 100) / res.total);
        };
        return (
          <SetRunner key={part.id} title={`Teil ${part.teil}: ${part.title}`} crumb={{ to: `/exams/${part.exam}/${part.module}`, label: part.module_name }}
            intro={part.instructions} kind={kind} text={part.text} items={items} example={example} seconds={part.minutes * 60}
            maxPlays={kind === "choice" ? 2 : null} onSave={save} />
        );
      }}
    </Async>
  );
}
