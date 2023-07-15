import re


class ProblemJSON:
    """class representing the problem json standard as mentionned in [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807)"""

    @staticmethod
    def build(
        typ: str, title: str, detail: str, status: int, context: dict | None
    ) -> dict:
        """function to generate dict from parameters"""
        return {
            "type": typ,
            "title": title,
            "detail": detail,
            "status": status,
            "context": context if context else {},
        }


EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""


def check_mail(email: str) -> bool:
    """checks if email is valid"""
    if re.fullmatch(EMAIL_REGEX, email):
        return True
    else:
        return False
