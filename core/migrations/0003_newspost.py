from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_sponsor"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("slug", models.SlugField(blank=True, max_length=240, unique=True)),
                ("excerpt", models.CharField(blank=True, max_length=320)),
                ("content", models.TextField()),
                ("cover_image", models.ImageField(blank=True, upload_to="news/")),
                ("published", models.BooleanField(default=False)),
                ("published_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-published_at", "-created_at"],
            },
        ),
    ]
