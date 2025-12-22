from sqlalchemy import text
from sqlalchemy.orm import Session


def create_content(db: Session, title: str | None, body: str):
    query = text("""
        insert into contents (title, body)
        values (:title, :body)
        returning id, title, body, created_at
    """)

    result = db.execute(query, {"title": title, "body": body})
    row = result.fetchone()
    db.commit()

    return row


def get_content(db: Session, content_id: str):
    query = text("""
        select id, title, body, created_at
        from contents
        where id = :id
    """)

    result = db.execute(query, {"id": content_id})
    return result.fetchone()


def list_contents(db: Session):
    query = text("""
        select id, title, body, created_at
        from contents
        order by created_at desc
    """)

    result = db.execute(query)
    return result.fetchall()
