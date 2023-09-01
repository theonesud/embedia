from typing import Optional
from embedia.schema.pubsub import Event
from datetime import datetime, timezone

subscribers = {}


def publish_event(event_type: Event, id: int, data: Optional[dict] = None):
    now = str(datetime.now(timezone.utc).astimezone().isoformat())
    if event_type not in subscribers.keys():
        return
    for callback in subscribers[event_type]:
        callback(event_type, id, now, data)


def subscribe_event(event_type: Event, callback):
    if event_type not in subscribers.keys():
        subscribers[event_type] = [callback]
    else:
        subscribers[event_type].append(callback)
