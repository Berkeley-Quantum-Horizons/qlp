"""Models of experiment
"""
from typing import List, Dict

from django.db import models
from espressodb.base.models import Base
from django.db.models import JSONField

from django.db.models import Count, Avg


class Experiment(Base):
    """Experiment base class."""

    tag = None


class DWaveExperiment(Experiment):
    """Specialization to DWave experiments."""

    graph = models.ForeignKey(
        "graph.Graph", on_delete=models.CASCADE, help_text=r"Foreign Key to `graph`"
    )
    machine = models.TextField(
        null=False, blank=False, help_text="Hardware name (e.g. DW_2000Q_5)"
    )
    settings = JSONField(help_text="Store DWave machine parameters")
    settings_hash = models.TextField(
        null=False,
        blank=False,
        help_text="md5 hash of key sorted normalized machine, settings, p, dictionary",
    )
    p = models.DecimalField(
        null=False,
        max_digits=6,
        decimal_places=2,
        help_text="Coefficient of penalty term, 0 to 9999.99",
    )
    chain_strength = models.FloatField(
        null=False, help_text="Set chain strength before auto_scaling"
    )
    tag = models.TextField(
        null=False,
        blank=False,
        help_text="Tag describing the anneal schedule. (Easier to just unique with tag.)",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "graph",
                    "machine",
                    "settings_hash",
                    "p",
                    "chain_strength",
                    "tag",
                ],
                name="unique_experiment",
            )
        ]

    @property
    def n_data(self) -> int:
        """Returns the number of present data entries
        """
        return self.data_set.count()

    def get_summary(self, n_entries: int = 5) -> List[Dict[str, float]]:
        """Returns a summary of solutions which fulfill the constraints.

        The returned list is sorted according to energy (ascending) and contains the
        energy and number of occurances.

        Arguments:
            n_entries: Number of different energies to be returned.
        """
        exp_data = self.data_set.all()
        satisfied_data = (
            exp_data.filter(
                constraint_satisfaction=True,
                experiment_ptr__dwaveexperiment__isnull=False,
            )
            .values("energy")
            .annotate(
                occurances=Count("energy"),
                chain_break_fraction=Avg("chain_break_fraction"),
            )
        )
        return sorted(list(satisfied_data[:n_entries]), key=lambda el: el["energy"])


class HMCExperiment(Experiment):
    """Class for associating HMC runs with graphs."""

    graph = models.ForeignKey(
        "graph.Graph", on_delete=models.CASCADE, help_text=r"Foreign Key to `graph`"
    )
    beta = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=6,
        help_text="Inverse temperature, 0 to 9999.999999",
    )
    thermalization_steps = models.PositiveIntegerField(
        null=False,
        help_text="Number of thermalization steps before measuring trajectories.",
    )
    evolution_steps = models.PositiveIntegerField(
        null=False, help_text="Number of evolution steps when used in measurement.",
    )
    shift_c = models.DecimalField(
        null=False, max_digits=10, decimal_places=6, help_text="???, 0 to 9999.999999",
    )
    trajectory_length = models.DecimalField(
        null=False, max_digits=10, decimal_places=6, help_text="???, 0 to 9999.999999",
    )
    md_steps = models.PositiveIntegerField(
        null=False, help_text="Number of molecular dynamics steps.",
    )

    misc = JSONField(help_text="Dump field for future data. Should be a python dict.")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "graph",
                    "beta",
                    "thermalization_steps",
                    "evolution_steps",
                    "shift_c",
                    "trajectory_length",
                    "md_steps",
                ],
                name="unique_hmc_run",
            )
        ]
