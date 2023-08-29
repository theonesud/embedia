from typing import Dict, Optional
from embedia.schema.pubsub import Event

subscribers = {}


def publish_event(event_type: Event, data: Optional[Dict] = {}):
    if event_type not in subscribers.keys():
        return
    for callback in subscribers[event_type]:
        callback(data)


def subscribe_event(event_type: Event, callback):
    if event_type not in subscribers.keys():
        subscribers[event_type] = [callback]
    else:
        subscribers[event_type].append(callback)
