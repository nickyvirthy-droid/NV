def build_runtime_context(
    session,
):

    return {
        "session_id": (
            session.session_id
        ),

        "workspace": (
            session.workspace
        ),

        "provider": (
            session.provider
        ),

        "admin_mode": (
            session.admin_mode
        ),
    }
