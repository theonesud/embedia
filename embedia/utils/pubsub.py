from typing import Dict, Optional

subscribers = {}


def publish_event(event_type: str, data: Optional[Dict] = {}):
    if event_type not in subscribers.keys():
        return
    for callback in subscribers[event_type]:
        callback(data)


def subscribe_event(event_type: str, callback):
    if event_type not in subscribers.keys():
        subscribers[event_type] = [callback]
    else:
        subscribers[event_type].append(callback)
