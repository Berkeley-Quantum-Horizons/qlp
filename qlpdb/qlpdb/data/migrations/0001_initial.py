# Generated by Django 3.0.3 on 2020-02-18 03:57

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('experiment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('measurement', models.PositiveIntegerField(help_text='Increasing integer field labeling measurement number')),
                ('spin_config', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(0)]), help_text='Spin configuration of solution, limited to 0, 1', size=None)),
                ('energy', models.FloatField(help_text='Energy corresponding to spin_config and QUBO')),
                ('experiment', models.ForeignKey(help_text='Foreign Key to `experiment`', on_delete=django.db.models.deletion.CASCADE, to='experiment.Experiment')),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Ananymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='data',
            constraint=models.UniqueConstraint(fields=('experiment', 'measurement'), name='unique_data'),
        ),
    ]