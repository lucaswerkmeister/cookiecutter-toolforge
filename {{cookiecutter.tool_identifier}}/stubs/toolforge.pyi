from typing import Any, Optional


def set_user_agent(tool: str, url: Optional[str] = None, email: Optional[str] = None) -> str: ...


# catch-all for any unstubbed attributes
def __getattr__(name) -> Any: ...
