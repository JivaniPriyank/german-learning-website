import { Suspense } from "react";
import { Link, NavLink, Navigate, Outlet, useLocation, useNavigate } from "react-router-dom";
import Icon, { BrandMark } from "./Icon";
import { Skeleton } from "./ui";
import { api } from "../lib/api";
import { useSession } from "../lib/session";
import { useToast } from "./Toasts";
import { useTeacherLiveUpdates } from "../lib/live";

export function Brand() {
  const { user } = useSession();
  return (
    <Link className="brand" to={user ? (user.is_teacher ? "/teacher" : "/today") : "/"}>
      <BrandMark /><span className="brand-text"><span>The German Lab</span><span className="brand-by">by Sneha</span></span>
    </Link>
  );
}

export function useSignOut() {
  const { setSession } = useSession();
  const navigate = useNavigate();
  const toast = useToast();
  return async () => {
    try {
      setSession(await api("/sign-out/", { method: "POST" }));
      navigate("/");
    } catch (e) {
      toast(e.message, "error");
    }
  };
}

function LevelSwitch() {
  const { user, levels, current_level, setSession } = useSession();
  const toast = useToast();
  const navigate = useNavigate();
  if (!levels || !levels.length) return null;
  if (levels.length === 1) {
    // A student whose course is A1 only sees A1: there's nothing to switch to.
    return (
      <div className="level-switch level-only" title={`Your level: ${levels[0].name}`}>
        <span aria-label={`Your level: ${levels[0].code} ${levels[0].name}`}>{levels[0].code}</span>
      </div>
    );
  }
  const choose = async (code) => {
    if (code === current_level?.code) return;
    try {
      const data = await api("/level/", { method: "POST", body: { level: code } });
      setSession(data);
      // A1 and A2 are separate courses: switching always starts on the home page.
      navigate(user.is_teacher ? "/teacher" : "/today");
      toast(`You're now studying ${data.current_level.code} (${data.current_level.name}).`);
    } catch (e) {
      toast(e.message, "error");
    }
  };
  return (
    <div className="level-switch" role="group" aria-label="Level you're studying">
      {levels.map((lv) => (
        <button key={lv.code} type="button" title={lv.name} aria-pressed={lv.code === current_level?.code} onClick={() => choose(lv.code)}>
          {lv.code}
        </button>
      ))}
    </div>
  );
}

function Count({ n, label }) {
  if (!n) return null;
  return <span className="count" aria-label={label ? `${n} ${label}` : undefined}>{n}</span>;
}

const STUDENT_MORE = ["/videos", "/progress", "/account", "/more", "/grammar", "/practice"];
const TEACHER_MORE = ["/teacher/students", "/teacher/content", "/teacher/classes", "/teacher/videos", "/videos", "/account", "/more",
  "/lektionen", "/sections", "/exams", "/speaking", "/words", "/practice", "/grammar"];

export function AppLayout() {
  const { user, counts } = useSession();
  const { pathname } = useLocation();
  const signOut = useSignOut();
  const t = user.is_teacher;
  useTeacherLiveUpdates(t);
  const moreActive = (t ? TEACHER_MORE : STUDENT_MORE).some((p) => pathname === p || pathname.startsWith(p + "/"));
  // A Lektion's pages (/sections/…) and its word flashcards belong to Meine Lektionen.
  const inLektion = pathname.startsWith("/sections/") || pathname.startsWith("/words/");

  return (
    <div className="shell">
      <a className="skip-link" href="#main">Skip to content</a>
      <aside className="sidebar" aria-label="Main menu">
        <Brand />
        <LevelSwitch />
        <nav className="nav">
          {t ? (
            <>
              <NavLink to="/teacher" end><Icon name="today" />Home</NavLink>
              <span className="nav-sep" aria-hidden="true" />
              <NavLink to="/teacher/requests"><Icon name="inbox" />Access requests<Count n={counts.pending_requests} label="waiting" /></NavLink>
              <NavLink to="/teacher/speaking"><Icon name="speaking" />Speaking answers<Count n={counts.speaking_waiting} label="waiting" /></NavLink>
              <NavLink to="/teacher/writing"><Icon name="writing" />Writing answers<Count n={counts.writing_waiting} label="waiting" /></NavLink>
              <NavLink to="/teacher/students"><Icon name="users" />Students</NavLink>
              <NavLink to="/teacher/classes"><Icon name="classes" />Classes</NavLink>
              <NavLink to="/teacher/videos"><Icon name="upload" />My videos</NavLink>
              <NavLink to="/teacher/content"><Icon name="edit" />Content</NavLink>
              <span className="nav-label">Student view</span>
            </>
          ) : (
            <>
              <NavLink to="/today"><Icon name="today" />Home</NavLink>
              <span className="nav-sep" aria-hidden="true" />
            </>
          )}
          <Link to="/lektionen" aria-current={pathname === "/lektionen" || inLektion ? "page" : undefined}><Icon name="lektionen" />Meine Lektionen</Link>
          <NavLink to="/exams"><Icon name="exam" />Exam practice</NavLink>
          <NavLink to="/speaking"><Icon name="speaking" />Speaking</NavLink>
          <NavLink to="/videos"><Icon name="videos" />Videos</NavLink>
          {!t && <NavLink to="/progress"><Icon name="progress" />Progress</NavLink>}
        </nav>
        <div className="sidebar-foot">
          <Link className="who" to="/account">
            <span className="avatar" aria-hidden="true">{(user.full_name || "?")[0].toUpperCase()}</span>
            <span><b>{user.full_name}</b><br /><span className="muted small">{t ? "Teacher" : user.classroom?.name || "Student"}</span></span>
          </Link>
          <button className="btn btn-quiet btn-small" type="button" onClick={signOut}><Icon name="out" />Sign out</button>
        </div>
      </aside>

      <div>
        <header className="topbar"><Brand /><LevelSwitch /></header>
        <main className="main" id="main"><Suspense fallback={<Skeleton />}><Outlet /></Suspense></main>
      </div>

      <nav className="tabbar" aria-label="Main menu">
        {t ? (
          <>
            <NavLink className="tab" to="/teacher" end><Icon name="today" />Home</NavLink>
            <NavLink className="tab" to="/teacher/requests"><Icon name="inbox" />Requests<Count n={counts.pending_requests} /></NavLink>
            <NavLink className="tab" to="/teacher/speaking"><Icon name="speaking" />Speaking<Count n={counts.speaking_waiting} /></NavLink>
            <NavLink className="tab" to="/teacher/writing"><Icon name="writing" />Writing<Count n={counts.writing_waiting} /></NavLink>
          </>
        ) : (
          <>
            <NavLink className="tab" to="/today"><Icon name="today" />Home</NavLink>
            <Link className="tab" to="/lektionen" aria-current={pathname === "/lektionen" || inLektion ? "page" : undefined}><Icon name="lektionen" />Lektionen</Link>
            <NavLink className="tab" to="/exams"><Icon name="exam" />Exams</NavLink>
            <NavLink className="tab" to="/speaking"><Icon name="speaking" />Speaking</NavLink>
          </>
        )}
        <Link className="tab" to="/more" aria-current={moreActive ? "page" : undefined}><Icon name="more" />More</Link>
      </nav>
    </div>
  );
}

export function PublicLayout() {
  const { user } = useSession();
  const signOut = useSignOut();
  return (
    <div className="public">
      <a className="skip-link" href="#main">Skip to content</a>
      <header className="public-top">
        <Brand />
        <nav aria-label="Account">
          {user ? (
            <button className="btn btn-quiet btn-small" type="button" onClick={signOut}>Sign out</button>
          ) : (
            <>
              <Link className="btn btn-quiet btn-small" to="/sign-in">Sign in</Link>
              <Link className="btn btn-primary btn-small" to="/join">Request access</Link>
            </>
          )}
        </nav>
      </header>
      <main className="contents" id="main"><Outlet /></main>
      <footer className="public-foot">German practice between lessons, for A1 and A2 learners.</footer>
    </div>
  );
}

// ---------- access rules (the server checks them too) ----------
export function RequireApproved() {
  const { user } = useSession();
  const location = useLocation();
  if (!user) return <Navigate to={`/sign-in?next=${encodeURIComponent(location.pathname)}`} replace />;
  if (user.status !== "approved") return <Navigate to="/waiting" replace />;
  return <Outlet />;
}

export function RequireTeacher() {
  const { user } = useSession();
  if (!user?.is_teacher) {
    return (
      <div className="error-page">
        <div className="code" aria-hidden="true">403</div>
        <h1>This page is for the teacher</h1>
        <p className="lead error-lead">Your account can't open it. Go back to your own pages from the menu.</p>
        <Link className="btn btn-primary" to="/today">Go to Today</Link>
      </div>
    );
  }
  return <Outlet />;
}

export function GuestOnly() {
  const { user } = useSession();
  if (user) return <Navigate to={user.status !== "approved" ? "/waiting" : user.is_teacher ? "/teacher" : "/today"} replace />;
  return <Outlet />;
}
