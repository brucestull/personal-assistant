# Registration Accepted Mixin Fix

- [Check CBVs Mixins - Private](https://chatgpt.com/c/681ccb80-5e1c-8002-8749-44f2f6bafe5e)
- [Check CBVs Mixins - Shared](https://chatgpt.com/share/681cd018-5d8c-8002-881c-77da40dcddcd)

- Need to ensure all appropriate views use the `RegistrationAcceptedMixin` to ensure that the user has their registration accepted.
    - `base/mixins.py`

- There is also a `@registration_accepted_required` decorator that can be used to enforce this requirement.
    - `base/decorators.py`