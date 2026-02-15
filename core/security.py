import re
from typing import List


class SecurityService:

    SCOPE_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')

    @staticmethod
    def validate_scope(scope: str, allowed_scopes: List[str]) -> bool:
        if not scope or not SecurityService.SCOPE_PATTERN.match(scope):
            return False
        return scope in allowed_scopes

    @staticmethod
    def escape_markdown_v2(text: str) -> str:
        if not text:
            return text
        chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in chars:
            text = text.replace(char, f'\\{char}')
        return text.replace('\\', '\\\\')