from __future__ import annotations

from typing import List, Optional
from pathlib import Path


class ASTKeyValue:
    def __init__(self):
        self.key: str | int = None
        self.value: [str, int, Path] = None

    def __str__(self):
        return f"{self.key}: {self.value}"

    def __eq__(self, other):
        return self.value == other


class ASTBlock:
    def __init__(self):
        self.children: List[ASTKeyValue] = []
        self.parent: Optional[ASTKeyValue] = None

    def __getitem__(self, item):
        return self.children[item]

    def __str__(self):
        children = ', '.join(str(x) for x in self.children)
        return f"{{{children}}}"
