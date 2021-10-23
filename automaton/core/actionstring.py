from dataclasses import dataclass
from string import Formatter
from typing import List, Union

from automaton.core.peripheral import Peripheral

from ..core import Button, Input, Key


@dataclass
class KeyCombo:
    keys: List[Input]
    state: str


@dataclass
class ActionString:
    actions: List[Union[str, KeyCombo]]

    @staticmethod
    def parse(string: str) -> "ActionString":
        actions: List[Union[str, KeyCombo]] = []
        for literal, field, _, _ in Formatter().parse(string):
            if literal and not field:
                actions.append(literal)
            elif literal:
                actions.append(literal)

            if field:
                data = field.split(" ")
                key_combo, state = (
                    data[0] if len(data) >= 1 else "",
                    data[1] if len(data) == 2 else "tap",
                )

                def lookup_input(key: str) -> Input:
                    for k in [*Key, *Button]:
                        if k.name.lower() == key.lower():
                            return k
                    return Key.Reserved

                keys: List[Input] = list(map(lookup_input, key_combo.split("+")))
                actions.append(KeyCombo(keys, state.lower()))
        return ActionString(actions)

    def execute(self, device: Peripheral):
        method = {
            "up": device.release,
            "down": device.press,
            "tap": device.tap,
        }
        for action in self.actions:
            if isinstance(action, str):
                device.type_unicode(action)
            else:
                method[action.state](*action.keys)
