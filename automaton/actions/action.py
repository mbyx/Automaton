from abc import ABC, abstractmethod

from .. import core
from .context import Context


class Action(ABC):
    """Represents an action that can be emitted, and can determine when to emit."""

    @abstractmethod
    def emit(self, device: core.Peripheral, context: Context) -> None:
        """Using the device and context, perform a series of actions."""
        pass

    def should_emit(self, context: Context) -> core.EmissionState:
        """Determines using context whether to emit, not emit, or emit without suppression."""
        return core.EmissionState.Emit
