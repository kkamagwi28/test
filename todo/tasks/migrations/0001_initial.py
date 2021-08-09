# Generated by Django 3.2.6 on 2021-08-08 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('is_finished', models.BooleanField(default=False)),
                ('estimated_finish_time', models.DateTimeField()),
            ],
        ),
    ]