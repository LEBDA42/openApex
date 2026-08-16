"""OpenApex — open training-intelligence engine for endurance sports.

A library, not a platform: parse activity files, compute documented
training-load metrics, model fitness/fatigue/form. Embed it anywhere.
"""

from openapex.io import read_fit
from openapex.models import (
    Activity,
    ActivityStreams,
    AthleteProfile,
    MissingProfileData,
    MissingStreamData,
    Sport,
)

__version__ = "0.1.0.dev0"

__all__ = [
    "Activity",
    "ActivityStreams",
    "AthleteProfile",
    "MissingProfileData",
    "MissingStreamData",
    "Sport",
    "__version__",
    "read_fit",
]
