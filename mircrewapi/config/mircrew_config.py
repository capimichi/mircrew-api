import os
from dataclasses import dataclass


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing env var: {name}")
    return value


@dataclass(frozen=True)
class MirCrewConfig:
    username: str
    password: str

    @classmethod
    def from_env(cls) -> "MirCrewConfig":
        return cls(
            username=_get_required_env("MIRCREW_USERNAME"),
            password=_get_required_env("MIRCREW_PASSWORD"),
        )
