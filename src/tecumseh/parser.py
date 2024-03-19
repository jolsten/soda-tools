import fileinput
from typing import Any, Iterable, List, Optional


class InputParser:
    def __init__(
        self, files: Optional[Iterable[str]] = None, chunk_size: int = 1_000
    ) -> None:
        self.files = files

    def __iter__(self) -> List[Any]:
        for line in fileinput.input(self.files):
            yield line
