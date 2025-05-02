from graphql_jwt.decorators import user_passes_test

event_staff_member_required = user_passes_test(
    lambda u: getattr(u, "is_event_staff", False)
)
