"""W5: SQLite 실패 주입으로 상태/감사의 원자성만 검증한다."""
import sqlite3

def atomic_review(connection: sqlite3.Connection, fail_audit: bool = False) -> None:
    """상태와 감사 행을 한 트랜잭션으로 저장한다.

    Args:
        connection: 실습용 SQLite 연결.
        fail_audit: 감사 기록 전에 오류를 주입할지 여부.
    Returns:
        None. 성공하면 두 변경을 커밋한다.
    Raises:
        RuntimeError: 실패 주입 시 발생하며 상태 변경도 롤백된다.
        sqlite3.Error: SQL 실행이 실패한 경우.
    """
    with connection:  # context manager는 예외 시 DB 변경을 롤백한다.
        connection.execute("UPDATE cases SET status = ? WHERE id = ?", ("APPROVED", 1))
        if fail_audit:
            raise RuntimeError("injected audit failure")
        connection.execute("INSERT INTO audit(case_id) VALUES (?)", (1,))

connection = sqlite3.connect(":memory:")
connection.executescript("CREATE TABLE cases(id INTEGER PRIMARY KEY, status TEXT);"
                         "CREATE TABLE audit(case_id INTEGER);"
                         "INSERT INTO cases VALUES(1, 'REVIEW_PENDING');")
try:
    atomic_review(connection, fail_audit=True)
except RuntimeError:
    pass
assert connection.execute("SELECT status FROM cases").fetchone()[0] == "REVIEW_PENDING"
assert connection.execute("SELECT count(*) FROM audit").fetchone()[0] == 0
atomic_review(connection)
assert connection.execute("SELECT count(*) FROM audit").fetchone()[0] == 1
connection.close()
print("W5 SQLite atomicity: passed; PostgreSQL/concurrency not validated")
