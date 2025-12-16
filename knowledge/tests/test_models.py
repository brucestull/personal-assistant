# knowledge/tests/test_models.py

from django.contrib.contenttypes.fields import GenericForeignKey

from knowledge.models import NoteEntry


def test_note_entry_has_generic_fk_and_ordering():
    # ordering is defined in Meta :contentReference[oaicite:14]{index=14}
    assert NoteEntry._meta.ordering == ["-created"]

    # the model exposes a GenericForeignKey attribute
    assert hasattr(NoteEntry, "content_object")
    assert isinstance(NoteEntry.content_object, GenericForeignKey)
