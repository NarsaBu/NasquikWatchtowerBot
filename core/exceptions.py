class WatchtowerBotError(Exception):
    """Bot common exception"""
    pass

class UnauthorizedError(WatchtowerBotError):
    """Unauthorized user attempted access"""
    pass

class InvalidScopeError(WatchtowerBotError):
    """Invalid scope name for update"""
    pass

class DockerCommandError(WatchtowerBotError):
    """Error processing Docker-command"""
    pass