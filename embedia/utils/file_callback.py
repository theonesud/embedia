import json
import os
import sqlite3
from typing import Optional

from embedia.schema.pubsub import Event
from embedia.utils.pubsub import subscribe_event

home = os.path.expanduser('~')
os.makedirs(f'{home}/.embedia', exist_ok=True)
conn = sqlite3.connect(f'{home}/.embedia/backup.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS backup (
            TIMESTAMP TEXT, EVENT TEXT, ID INT, DATA TEXT)""")


def file_callback(event_type: Event, id: int, timestamp: str, data: Optional[dict] = None):
    if not data:
        data = {}
    cur.execute("INSERT INTO backup VALUES (?, ?, ?, ?)",
                (timestamp, event_type, id, json.dumps(data)))
    conn.commit()


def setup_file_callback():
    subscribe_event(Event.LLMEnd, file_callback)
    subscribe_event(Event.ChatLLMInit, file_callback)
    subscribe_event(Event.ChatLLMEnd, file_callback)
    subscribe_event(Event.ToolEnd, file_callback)
    subscribe_event(Event.AgentStep, file_callback)
    subscribe_event(Event.AgentEnd, file_callback)
