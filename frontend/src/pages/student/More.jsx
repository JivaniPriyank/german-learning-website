import Icon from "../../components/Icon";
import { useSignOut } from "../../components/Layout";
import { PageHead, RowLink } from "../../components/ui";
import { useTitle } from "../../lib/hooks";
import { useSession } from "../../lib/session";

export default function More() {
  useTitle("More");
  const { user } = useSession();
  const signOut = useSignOut();
  return (
    <>
      <PageHead title="More" />
      <ul className="list">
        {user.is_teacher ? (
          <>
            <RowLink to="/teacher/students" icon="users" title="Students" />
            <RowLink to="/teacher/content" icon="edit" title="Content" sub="Lektionen, words, exam practice" />
            <RowLink to="/teacher/classes" icon="classes" title="Classes" />
            <RowLink to="/teacher/videos" icon="upload" title="My videos" />
            <RowLink to="/lektionen" icon="lektionen" title="Meine Lektionen" sub="Mark Lektionen as taught; see the student pages" />
            <RowLink to="/exams" icon="exam" title="Exam practice" />
            <RowLink to="/speaking" icon="speaking" title="Speaking" sub="The student page" />
          </>
        ) : (
          <RowLink to="/progress" icon="progress" title="Progress" />
        )}
        <RowLink to="/videos" icon="videos" title="Videos" />
        <RowLink to="/account" icon="account" title="Your account" sub={user.email} />
      </ul>
      <button className="btn btn-secondary btn-block mt-5" type="button" onClick={signOut}><Icon name="out" />Sign out</button>
    </>
  );
}
