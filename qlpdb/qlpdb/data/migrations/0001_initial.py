# Generated by Django 3.1.2 on 2020-10-23 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(help_text='Primary key for Base class.', primary_key=True, serialize=False)),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='Date the class was last modified')),
                ('tag', models.CharField(blank=True, help_text='User defined tag for easy searches', max_length=200, null=True)),
                ('measurement', models.PositiveIntegerField(help_text='Increasing integer field labeling measurement number')),
                ('spin_config', models.JSONField(help_text='Spin configuration of solution, limited to 0, 1')),
                ('chain_break_fraction', models.FloatField(help_text='Chain break fraction')),
                ('energy', models.FloatField(help_text='Energy corresponding to spin_config and QUBO')),
                ('constraint_satisfaction', models.BooleanField(help_text='Are the inequality constraints satisfied by the slacks?')),
                ('experiment', models.ForeignKey(help_text='Foreign Key to `experiment`', on_delete=django.db.models.deletion.CASCADE, to='experiment.experiment')),
                ('user', models.ForeignKey(blank=True, help_text='User who updated this object. Set on save by connection to database. Anonymous if not found.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='data',
            constraint=models.UniqueConstraint(fields=('experiment', 'measurement'), name='unique_data'),
        ),
    ]
