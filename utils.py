class ProblemJSON:
    """class representing the problem json standard as mentionned in [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807)"""

    @staticmethod
    def build(typ: str, detail: str, status: int, context: dict | None) -> dict:
        """function to generate dict from parameters"""
        return {
            "type": typ,
            "detail": detail,
            "status": status,
            "context": context if context else {},
        }
