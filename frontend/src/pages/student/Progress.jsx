import { Link } from "react-router-dom";
import Icon from "../../components/Icon";
import { Async, Meter, PageHead } from "../../components/ui";
import { useApi, useLevelKey, useTitle } from "../../lib/hooks";
import { plural } from "../../lib/speech";

// Darker squares for days with more practice.
const shade = (n) => (n === 0 ? 0 : n <= 2 ? 1 : n <= 5 ? 2 : n <= 9 ? 3 : 4);
const dayLabel = (iso) => new Date(`${iso}T12:00:00`).toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" });

// The last 12 weeks: one column per week (Monday at the top), one square per day.
function ActivityCalendar({ days }) {
  const active = days.filter((d) => d.count > 0).length;
  const firstWeekday = (new Date(`${days[0].date}T12:00:00`).getDay() + 6) % 7; // Monday = 0
  return (
    <div className="calendar-wrap">
      <div className="calendar" role="img" aria-label={`Practised on ${active} of the last ${days.length} days`}>
        {Array.from({ length: firstWeekday }, (_, i) => <span key={`pad${i}`} className="cal-pad" />)}
        {days.map((d) => (
          <span key={d.date} className={`cal-day cal-${shade(d.count)}`}
            title={`${dayLabel(d.date)}: ${d.count ? plural(d.count, "thing") + " practised" : "no practice"}`} />
        ))}
      </div>
      <div className="calendar-legend" aria-hidden="true">
        <span>Less</span>{[0, 1, 2, 3, 4].map((n) => <span key={n} className={`cal-day cal-${n}`} />)}<span>More</span>
      </div>
      <p className="muted small mb-0">Practised on <b>{active}</b> of the last {days.length} days.</p>
    </div>
  );
}

// Progress through the Lektionen taught so far, and the days practised.
export default function Progress() {
  useTitle("Progress");
  const levelKey = useLevelKey();
  const state = useApi("/progress/", [levelKey]);
  const lek = useApi("/lektionen/", [levelKey]);
  return (
    <Async state={lek}>
      {({ level, lektionen, streak }) => {
        const taught = lektionen.filter((x) => x.is_taught);
        const sets = taught.reduce((a, x) => a + x.sets, 0);
        const done = taught.reduce((a, x) => a + x.sets_done, 0);
        return (
          <>
            <PageHead title={`Your ${level?.code || ""} progress`}>
              <p className="muted">{streak ? `${plural(streak, "day")} in a row. ` : ""}Every practice set you finish counts.</p>
            </PageHead>
            <div className="stats">
              <div className="stat"><b>{taught.length}<small className="stat-of"> / {lektionen.length}</small></b><span>Lektionen taught so far</span></div>
              <div className="stat"><b>{done}<small className="stat-of"> / {sets}</small></b><span>practice sets done</span></div>
              <div className="stat"><b>{streak || 0}</b><span>days in a row</span></div>
            </div>

            <section className="section">
              <h2>Lektionen</h2>
              {taught.length ? (
                <ul className="list">
                  {taught.map((x) => (
                    <li key={x.id}>
                      <Link className="row" to={`/sections/${x.id}`}>
                        <span className="row-main">
                          <span className="row-title" lang="de">{x.title}</span>
                          <span className="row-sub">{x.sets_done} of {x.sets} practice sets done</span>
                        </span>
                        <span className="row-end">
                          <Meter className="meter-mini" good percent={x.sets ? Math.round((x.sets_done / x.sets) * 100) : 0} label={`${x.sets_done} of ${x.sets} done`} />
                          <span className="chev"><Icon name="chevron" /></span>
                        </span>
                      </Link>
                    </li>
                  ))}
                </ul>
              ) : <p className="muted">Your first Lektion opens after it has been taught in class.</p>}
            </section>

            <Async state={state}>
              {({ calendar }) => (
                <section className="section">
                  <h2>Last 12 weeks</h2>
                  <ActivityCalendar days={calendar} />
                </section>
              )}
            </Async>
          </>
        );
      }}
    </Async>
  );
}
