from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("occurrences", "0044_add_group_name_to_studygroup_order_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="enrolment",
            name="is_part_of_cultural_route",
            field=models.BooleanField(
                default=False,
                help_text="Is enrolment part of a cultural route? True means yes, False means no, I don't know or unanswered.",
                verbose_name="is part of cultural route",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="eventqueueenrolment",
            name="is_part_of_cultural_route",
            field=models.BooleanField(
                default=False,
                help_text="Is enrolment part of a cultural route? True means yes, False means no, I don't know or unanswered.",
                verbose_name="is part of cultural route",
            ),
            preserve_default=False,
        ),
    ]
