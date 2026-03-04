# Generated manually: set empty enrollment_number to NULL to avoid unique constraint

from django.db import migrations


def empty_enrollment_to_null(apps, schema_editor):
    StudentProfile = apps.get_model("student_portal", "StudentProfile")
    StudentProfile.objects.filter(enrollment_number="").update(enrollment_number=None)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("student_portal", "0005_fix_enrollment_number_default"),
    ]

    operations = [
        migrations.RunPython(empty_enrollment_to_null, noop),
    ]
