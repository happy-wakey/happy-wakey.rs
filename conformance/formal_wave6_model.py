#!/usr/bin/env python3
from itertools import product

DISARMED, ARMED, FIRED = range(3)
EVENTS = ("arm", "disarm", "tick_due", "tick_early", "noop")


def step(state, event):
    if event == "arm" and state == DISARMED:
        return ARMED, 0
    if event == "disarm" and state == ARMED:
        return DISARMED, 0
    if event == "tick_due" and state == ARMED:
        return FIRED, 1
    if event == "tick_early" and state == ARMED:
        return ARMED, 0
    if event == "noop":
        return state, 0
    return None


reached_fired = False
rejected_illegal = False
for events in product(EVENTS, repeat=5):
    state = DISARMED
    effects = 0
    history = [state]
    legal = True
    for event in events:
        result = step(state, event)
        if result is None:
            rejected_illegal = True
            legal = False
            break
        state, emitted = result
        effects += emitted
        history.append(state)
        assert effects <= 1, "alarm emitted more than one firing effect"
    if not legal:
        continue
    if FIRED in history:
        reached_fired = True
        i = history.index(FIRED)
        assert effects == 1, "fired state was reached without exactly one effect"
        assert all(s == FIRED for s in history[i:]), "fired alarm reopened"

assert reached_fired, "fired state is unreachable"
assert rejected_illegal, "model never exercised an illegal alarm transition"
print("alarm exactly-once transition-system model: ok")
