from abc import ABC, abstractmethod

from .. import core
from .context import Context


class Action(ABC):
    """Represents an action that can be emitted, and can determine when to emit.

        This is an abstract base class for representing actions. Actions are events
    that are emitted when a certain set of conditions are met. Each action has
    a different condition which is determined by `should_emit(context)`.
        Once it is decided that an action should be emit, the `emit()` function
    can be called with the device to emit the action from and the `Context` to
    use when emitting."""

    @abstractmethod
    def emit(self, device: core.Peripheral, context: Context) -> None:
        """Using the device and context, perform a series of actions.

        Args:
            device (core.Peripheral): The device on which the actions will be performed.
            context (Context): The context that caused the action to be emitted."""
        pass

    def should_emit(self, context: Context) -> core.EmissionState:
        """Determines using context whether to emit, not emit, or emit without suppression.

        Args:
            context (Context): The context that may cause an action to be emitted.

        Returns:
            core.EmissionState: An enum that represents one of three states. To Emit, Not Emit or Emit without suppresion of keys."""
        return core.EmissionState.Emit
