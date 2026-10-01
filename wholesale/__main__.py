import argparse
import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from .engine import screen

def main():
    p = argparse.ArgumentParser(description='Screen sourced property leads; never sends messages or executes transactions.')
    p.add_argument('input', type=Path)
    p.add_argument('--buyers', type=Path)
    p.add_argument('--db', type=Path, default=Path('data/pipeline.sqlite'))
    p.add_argument('--output', type=Path, default=Path('data/screening.json'))
    a = p.parse_args()
    leads = json.loads(a.input.read_text())
    buyers = json.loads(a.buyers.read_text()) if a.buyers else []
    results = [screen(lead, buyers) for lead in leads]
    a.db.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(a.db) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, occurred_at TEXT, lead_id TEXT, input_sha256 TEXT, input_json TEXT, result_json TEXT)')
        for lead, result in zip(leads, results):
            raw = json.dumps({'lead':lead,'buyers':buyers}, sort_keys=True, allow_nan=False)
            conn.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)', (str(uuid.uuid4()), datetime.now(timezone.utc).isoformat(), lead['id'], hashlib.sha256(raw.encode()).hexdigest(), raw, json.dumps(result, allow_nan=False)))
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(results, indent=2, allow_nan=False)+'\n')
    print(json.dumps({'screened':len(results), 'owner_review':sum(r['status']=='READY_FOR_OWNER_REVIEW' for r in results), 'report':str(a.output), 'audit_db':str(a.db)}))

if __name__ == '__main__': main()
