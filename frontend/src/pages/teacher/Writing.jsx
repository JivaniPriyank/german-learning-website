import { useId, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import Icon from "../../components/Icon";
import { useToast } from "../../components/Toasts";
import { Async, Empty, PageHead } from "../../components/ui";
import { api } from "../../lib/api";
import { useApi, useTitle } from "../../lib/hooks";
import { useSession } from "../../lib/session";
import { formatDate } from "../../lib/speech";

// Writing answers from the Lektionen: read them, write a comment, mark them as checked.
export default function WritingInbox() {
  useTitle("Writing answers");
  const [params, setParams] = useSearchParams();
  const show = params.get("show") === "checked" ? "checked" : "waiting";
  const state = useApi(`/teacher/writing/?show=${show}`, [show]);
  const { refresh } = useSession();
  const done = (id) => {
    state.setData((d) => ({ ...d, answers: d.answers.filter((a) => a.id !== id), waiting: Math.max(0, d.waiting - 1) }));
    refresh?.();
  };
  return (
    <>
      <PageHead title="Writing answers">
        <p className="muted">Answers to the writing tasks of the Lektionen. Your comment appears under the student's answer.</p>
      </PageHead>
      <div className="content-tabs" role="tablist" aria-label="Which answers">
        <button type="button" role="tab" aria-selected={show === "waiting"} onClick={() => setParams({}, { replace: true })}>
          Waiting{state.data && <span className="tab-count">{state.data.waiting}</span>}
        </button>
        <button type="button" role="tab" aria-selected={show === "checked"} onClick={() => setParams({ show: "checked" }, { replace: true })}>Checked</button>
      </div>
      <Async state={state}>
        {({ answers }) => answers.length === 0 ? (
          <Empty title={show === "waiting" ? "Nothing to check" : "Nothing checked yet"}>
            {show === "waiting" ? "When a student sends a writing answer, it appears here." : "Answers you've checked appear here."}
          </Empty>
        ) : (
          answers.map((a) => <Answer key={a.id} a={a} onChecked={done} />)
        )}
      </Async>
    </>
  );
}

function Answer({ a, onChecked }) {
  const id = useId();
  const toast = useToast();
  const [feedback, setFeedback] = useState(a.feedback || "");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const checked = a.status === "checked";

  const save = async (e) => {
    e.preventDefault();
    if (busy) return;
    if (!feedback.trim()) { setError("Write a short comment for the student."); return; }
    setBusy(true);
    try {
      const res = await api(`/teacher/writing/${a.id}/`, { method: "POST", body: { feedback } });
      toast(res.message);
      onChecked(a.id);
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  };

  return (
    <section className="panel lk-task">
      <div className="lk-task-head">
        <div>
          <h3><Link to={`/teacher/students/${a.student.id}`}>{a.student.name}</Link></h3>
          <span className="lk-note"><span lang="de">{a.section.title}</span> · <span lang="de">{a.task.title}</span>{a.task.source && ` (${a.task.source})`}</span>
        </div>
        <span className="muted small">{checked ? `Checked ${formatDate(a.checked_at, true)}` : `Sent ${formatDate(a.submitted_at, true)}`}</span>
      </div>
      <p className="lk-prompt">{a.task.prompt}</p>
      <div className="lk-answer" lang="de">{a.text}</div>
      {checked ? (
        <div className="lk-comment"><b>Your comment:</b> {a.feedback}</div>
      ) : (
        <form className="lk-write" onSubmit={save} noValidate>
          <label htmlFor={id}>Your comment</label>
          <textarea id={id} rows={3} value={feedback} maxLength={5000} aria-invalid={!!error}
            placeholder="e.g. Sehr gut! Only one thing: Ich kaufe den Apfel (maskulin → den)."
            onChange={(e) => setFeedback(e.target.value)} />
          {error && <p className="error" role="alert">{error}</p>}
          <div className="ex-actions">
            <button className="btn btn-primary btn-small" type="submit" aria-disabled={busy}><Icon name="check" />{busy ? "Saving…" : "Mark as checked"}</button>
          </div>
        </form>
      )}
    </section>
  );
}
