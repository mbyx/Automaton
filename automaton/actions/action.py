from abc import ABC, abstractmethod
from ..core import Peripheral, EmissionState, Context

class Action(ABC):
    """Represents an action that can be emitted, and can determine when to emit."""

    @abstractmethod
    def emit(self, device: Peripheral, context: Context):
        """Using the device and context, perform a series of actions."""
        pass

    def should_emit(self, context: Context) -> EmissionState:
        """Determines using context whether to emit, not emit, or emit without suppression."""
        return EmissionState.Emit