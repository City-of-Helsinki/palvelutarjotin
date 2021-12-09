from typing import List, Optional


def get_event_provider(event_json: dict, language: str = "fi") -> Optional[str]:
    """Return a provider name in preferred language from given event json.

    Args:
        event_json (dict): [description]
        language (str, optional): [description]. Defaults to "fi".

    Returns:
        Optional[str]: [description]
    """
    return event_json["provider"]["fi"] if event_json["provider"] else None


def get_event_keywords(event_json: dict, language: str = "fi") -> List[str]:
    """Return event keywords in a format that is supported by EnrolmentReport model.

    Args:
        event_json (dict): event json fetched from LinkedEvents API
        language (str, optional): [description]. Defaults to "fi".

    Returns:
        List[str]: First argument is an index, second is a translation or an empty list
    """
    return (
        [
            (kw["id"], kw.get("name", {language: ""})[language]) if kw else ""
            for kw in event_json["keywords"]
        ]
        if event_json["keywords"]
        else []
    )
