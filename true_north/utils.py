def periodic_task_name(model_name: str, obj_pk: int) -> str:
    """
    e.g. "true_north-CoreValue-7"
    Stable, unique, never contains the user pk.
    """
    return f"true_north-{model_name}-{obj_pk}"
