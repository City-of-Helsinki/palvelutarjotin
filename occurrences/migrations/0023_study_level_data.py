# Generated by Django 2.2.13 on 2021-01-15 10:28

from django.db import migrations

from occurrences.consts import StudyGroupStudyLevels
from django.utils import translation

from occurrences.models import StudyLevel as NewStudyLevel, StudyGroup as NewStudyGroup


def init_study_levels(apps, schema_editor):
    """
    Initialize all current possible study_levels to a new StudyLevel table.

    All existing study_level values were listed in the model's constant,
    which is now moved to occurrences.consts.StudyGroupStudyLevels.
    """

    translation.activate("en")
    for level in range(len(StudyGroupStudyLevels.STUDY_LEVELS)):
        id, en_label = StudyGroupStudyLevels.STUDY_LEVELS[level]
        # Multiply by 10, so it's easier to add new levels between existing ones.
        study_level = NewStudyLevel(id=id, level=level * 10,)
        study_level.label = en_label
        study_level.save()


def clear_study_levels(apps, schema_editor):
    """
    Reverse for init_study_levels: Clears the StudyLevel table.
    """

    StudyLevel = apps.get_model("occurrences", "StudyLevel")
    StudyLevel.objects.all().delete()


def link_study_levels(apps, schema_editor):
    """
    Make a m2m-link from a StudyGroup instance to a StudyLevel instance.
    The old field and value still exists in isntance.study_level.
    It now needs to be converted to a link to StudyLevel -table.
    """

    translation.activate("en")

    # The StudyGroup model cannot be imported directly as it has been changed.
    # The historical version must be used instead.
    StudyGroup = apps.get_model("occurrences", "StudyGroup")
    ThroughModel = NewStudyGroup.study_levels.through

    new_objects = [
        ThroughModel(studygroup_id=studygroup_id, studylevel_id=studylevel_id)
        for studygroup_id, studylevel_id in StudyGroup.objects.exclude(
            study_level__isnull=True
        )
        .exclude(study_level__exact="")
        .values_list("id", "study_level")
    ]

    ThroughModel.objects.bulk_create(new_objects)


def reverse_link_study_levels(apps, schema_editor):
    """
    Reverse function for link_study_levels: Reads all links between
    StudyGroups and StudyLevels and populates a study_level field.
    """

    StudyLevel = apps.get_model("occurrences", "StudyLevel")
    for study_level in StudyLevel.objects.all():
        study_level.study_groups.all().update(study_level=study_level.id)


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("occurrences", "0022_study_level"),
    ]

    operations = [
        # Run study_levels initialization when all the structure is created.
        migrations.RunPython(init_study_levels, reverse_code=clear_study_levels),
        # Run the linking between study groups and study levels when
        # all the study levels has been created
        migrations.RunPython(link_study_levels, reverse_code=reverse_link_study_levels),
    ]
