import csv
import io
import os
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, inspect, Column, String, Float, Integer, Table, MetaData
from sqlalchemy import insert

from app.db import get_db, engine
from app.auth import get_current_user
from app import models
from app.rag import upsert_document
from app.utils import ollama_embed
from app.db import get_db

router = APIRouter()


def infer_column_type(samples: list[str]):
    """Infer SQL type from sample values."""
    if not samples:
        return String(500)
    non_null = [s for s in samples if s.strip()]
    if not non_null:
        return String(500)
    try:
        [float(s) for s in non_null]
        if all("." not in s for s in non_null):
            return Integer
        return Float
    except ValueError:
        return String(500)


def sanitize_column_name(name: str) -> str:
    """Make column name SQL-safe."""
    import re
    name = re.sub(r"[^\w]", "_", name.strip().lower())
    return name[:63] or "col"


def ensure_table(table_name: str, columns: dict, db: Session) -> Table:
    """Create table if it doesn't exist, or add missing columns."""
    metadata = MetaData()
    inspector = inspect(engine)

    if table_name in inspector.get_table_names():
        # Add any new columns
        existing = {c["name"] for c in inspector.get_columns(table_name)}
        for col_name, col_type in columns.items():
            if col_name not in existing:
                col_type_str = "TEXT" if isinstance(col_type, String) else str(col_type).upper()
                db.execute(text(f'ALTER TABLE "{table_name}" ADD COLUMN "{col_name}" {col_type_str}'))
        db.commit()
    else:
        # Create new table
        sa_columns = [Column("id", Integer, primary_key=True, autoincrement=True)]
        for col_name, col_type in columns.items():
            sa_columns.append(Column(col_name, col_type))
        table = Table(table_name, metadata, *sa_columns)
        metadata.create_all(engine)

    return Table(table_name, MetaData(bind=engine), autoload_with=engine)


@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    table_name: Optional[str] = None,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV files are supported")

    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))
    rows = list(reader)

    if not rows:
        raise HTTPException(400, "CSV file is empty")

    # Detect schema
    raw_columns = list(rows[0].keys())
    sanitized = {sanitize_column_name(c): c for c in raw_columns}

    # Sample up to 20 rows per column for type inference
    column_types = {}
    for safe_name, raw_name in sanitized.items():
        samples = [row[raw_name] for row in rows[:20] if row.get(raw_name)]
        column_types[safe_name] = infer_column_type(samples)

    # Determine table name
    if not table_name:
        table_name = sanitize_column_name(file.filename.replace(".csv", "")) or "imported_data"

    # Ensure table exists
    ensure_table(table_name, column_types, db)

    # Bulk insert (skip duplicates via ON CONFLICT DO NOTHING on id)
    inserted = 0
    skipped = 0
    embed_texts = []

    for row in rows:
        record = {}
        for safe_name, raw_name in sanitized.items():
            val = row.get(raw_name, "").strip()
            col_type = column_types[safe_name]
            if isinstance(col_type, Float) and val:
                try:
                    record[safe_name] = float(val)
                except ValueError:
                    record[safe_name] = None
            elif col_type == Integer and val:
                try:
                    record[safe_name] = int(val)
                except ValueError:
                    record[safe_name] = None
            else:
                record[safe_name] = val or None

        try:
            # db.execute(text(f'INSERT INTO "{table_name}" ({", ".join(f\'"{k}"\' for k in record)}) VALUES ({", ".join(f":{k}" for k in record)})'), record)
            columns = ", ".join(f'"{k}"' for k in record)
            values = ", ".join(f":{k}" for k in record)

            query = text(f'INSERT INTO "{table_name}" ({columns}) VALUES ({values})')

            db.execute(query, record)
            inserted += 1
            embed_texts.append(" ".join(str(v) for v in record.values() if v))
        except Exception:
            skipped += 1

    db.commit()

    # Index in Pinecone for semantic search
    for i, text_chunk in enumerate(embed_texts[:500]):  # cap at 500 per upload
        await upsert_document(
            f"{table_name}_row_{i}",
            text_chunk,
            {"source": table_name, "type": "product", "row": i},
        )

    return {
        "table": table_name,
        "columns": list(column_types.keys()),
        "inserted": inserted,
        "skipped": skipped,
        "total": len(rows),
    }
