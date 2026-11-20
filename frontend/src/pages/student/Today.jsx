import { Link, Navigate, useSearchParams } from "react-router-dom";
import Icon from "../../components/Icon";
import { Async, Empty, Meter, RowLink } from "../../components/ui";
import { useApi, useLevelKey, useTitle } from "../../lib/hooks";
import { formatDate, plural } from "../../lib/speech";
import { useSession } from "../../lib/session";

// The student's home: carry on with the newest Lektion, see the teacher's comments.
export default function Today() {
  useTitle("Today");
  const { user } = useSession();
  const [params] = useSearchParams();
  const levelKey = useLevelKey();
  const asTeacher = user.is_teacher && !params.get("as_student");
  const state = useApi(asTeacher ? null : "/lektionen/", [levelKey]);
  if (asTeacher) return <Navigate to="/teacher" replace />;

  return (
    <Async state={state}>
      {({ level, lektionen, streak, feedback, new_videos }) => {
        const taught = lektionen.filter((x) => x.is_taught);
        const current = taught[taught.length - 1];
        const unfinished = taught.find((x) => x.sets && x.sets_done < x.sets);
        return (
          <>
            <div className="greeting">
              <h1>Hallo, {user.first_name}!</h1>
              <p className="muted">
                {streak ? `${plural(streak, "day")} in a row. Keep it going.` : `Revise your ${level?.code || ""} Lektionen here after class. A few minutes a day is enough.`}
              </p>
            </div>

            {current ? (
              <section className="focus-card paper">
                <div>
                  <h2 lang="de">{current.title}</h2>
                  <p>Your newest Lektion from class: {current.sets_done} of {current.sets} practice sets done.</p>
                  {current.sets > 0 && <Meter good percent={Math.round((current.sets_done / current.sets) * 100)} label={`${current.sets_done} of ${current.sets} practice sets done`} />}
                </div>
                <div className="actions"><Link className="btn btn-primary" to={`/sections/${current.id}`}>{current.sets_done ? "Carry on" : "Start practising"}</Link></div>
              </section>
            ) : (
              <Empty title="Nothing to revise yet">Your first Lektion opens here after it has been taught in class.</Empty>
            )}

            {feedback.length > 0 && (
              <section className="section">
                <div className="section-head"><h2>Comments from your teacher</h2></div>
                <ul className="list">
                  {feedback.map((f) => (
                    <li key={f.id}>
                      <Link className="row" to={`/sections/${f.section}?tab=schreiben`}>
                        <Icon name="writing" />
                        <span className="row-main">
                          <span className="row-title" lang="de">{f.task}</span>
                          <span className="row-sub">“{f.feedback}” · {formatDate(f.checked_at)}</span>
                        </span>
                        <span className="row-end"><span className="chev"><Icon name="chevron" /></span></span>
                      </Link>
                    </li>
                  ))}
                </ul>
              </section>
            )}

            <section className="section">
              <h2 className="visually-hidden">Go to</h2>
              <div className="quick">
                <Link to="/lektionen"><Icon name="lektionen" />Meine Lektionen<span>{taught.length} {taught.length === 1 ? "Lektion" : "Lektionen"} open</span></Link>
                <Link to="/exams"><Icon name="exam" />Exam practice<span>Goethe and telc format</span></Link>
                <Link to="/speaking"><Icon name="speaking" />Speaking<span>Record exam answers</span></Link>
                {unfinished && unfinished !== current
                  ? <Link to={`/sections/${unfinished.id}`}><Icon name="practice" />Not finished<span lang="de">{unfinished.title.split(":")[0]}</span></Link>
                  : <Link to="/progress"><Icon name="progress" />Progress<span>Your practice days</span></Link>}
              </div>
            </section>

            {new_videos.length > 0 && (
              <section className="section">
                <div className="section-head"><h2>New from your teacher</h2><Link to="/videos">All videos</Link></div>
                <ul className="list">
                  {new_videos.map((v) => <RowLink key={v.id} to={`/videos/${v.id}`} icon="videos" title={v.title} sub="Not watched yet" />)}
                </ul>
              </section>
            )}
          </>
        );
      }}
    </Async>
  );
}
