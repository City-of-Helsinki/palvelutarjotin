from django.db import migrations
from django.utils import translation

from occurrences.consts import StudyGroupStudyLevels
from occurrences.models import StudyLevel


def update_study_levels(apps, schema_editor):
    """
    Update all current possible study_levels to a new StudyLevel table based on the
    value of StudyGroupStudyLevels.STUDY_LEVELS)
    """

    translation.activate("en")
    for level in range(len(StudyGroupStudyLevels.STUDY_LEVELS)):
        # Using index of the constant to assign the order of study levels list
        id, en_label = StudyGroupStudyLevels.STUDY_LEVELS[level]
        try:
            study_level = StudyLevel.objects.get(id=id)
            study_level.level = level
        except StudyLevel.DoesNotExist:
            study_level = StudyLevel.objects.create(id=id, level=level)
        study_level.label = en_label
        study_level.save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("occurrences", "0029_add_more_occurrence_languages"),
    ]

    operations = [
        migrations.RunPython(
            update_study_levels, reverse_code=migrations.RunPython.noop
        ),
    ]
