from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List


def create_content(
    db: Session,
    title: str | None,
    body: str,
    embedding: List[float],
):
    """
    Insert a content row with embedding vector.
    Day4: embedding is mock but schema is production-ready.
    """
    query = text("""
        insert into contents (title, body, embedding)
        values (:title, :body, :embedding)
        returning id, title, body, created_at
    """)

    result = db.execute(
        query,
        {
            "title": title,
            "body": body,
            "embedding": embedding,
        }
    )
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
    """
    List contents without embeddings.
    Embeddings are intentionally excluded to avoid
    large payloads and unnecessary data transfer.
    """
    query = text("""
        select id, title, body, created_at
        from contents
        order by created_at desc
    """)

    result = db.execute(query)
    return result.fetchall()

def semantic_search(
    db: Session,
    query_embedding: list[float],
    top_k: int,
):
    query = text("""
        select
            id,
            title,
            body,
            embedding <-> (:query_embedding)::vector as score
        from contents
        where embedding is not null
        order by embedding <-> (:query_embedding)::vector
        limit :top_k
    """)

    result = db.execute(
        query,
        {
            "query_embedding": query_embedding,
            "top_k": top_k,
        }
    )

    return result.fetchall()
