from django.conf import settings
from django.db import models
from temba_client.v2 import TembaClient


class Group(models.Model):
    uuid = models.CharField(max_length=50, blank=False)
    name = models.CharField(max_length=50, blank=False)
    count = models.IntegerField(blank=False)
    query = models.CharField(max_length=50, null=True, blank=True)

    @classmethod
    def add_groups(cls):
        client = TembaClient(settings.HOST, settings.KEY)
        groups = client.get_groups().all()
        added = 0
        for group in groups:
            if not cls.group_exists(group):
                cls.objects.create(uuid=group.uuid, name=group.name, query=group.query, count=group.count)
                added += 1

        return added

    @classmethod
    def group_exists(cls, group):
        return cls.objects.filter(uuid=group.uuid).exists()

    def __unicode__(self):
        return self.id


class Run(models.Model):
    run_id = models.IntegerField()
    responded = models.BooleanField()
    created_on = models.DateTimeField()
    modified_on = models.DateTimeField()

    @classmethod
    def add_runs(cls):
        client = TembaClient(settings.HOST, settings.KEY)
        runs = client.get_runs().all()
        added = 0
        for run in runs:
            if not cls.run_exists(run):
                cls.objects.create(run_id=run.id, responded=run.responded, created_on=run.created_on,
                                   modified_on=run.modified_on)
                r = Run.objects.get(run_id=run.id)
                Step.add_steps(run=r, steps=run.path)
                Value.add_values(run=r, values=run.values)
                added += 1

        return added

    @classmethod
    def run_exists(cls, run):
        return cls.objects.filter(run_id=run.id).exists()

    def __unicode__(self):
        return str(self.run_id)


class Step(models.Model):
    node = models.CharField(max_length=100)
    time = models.DateTimeField()
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE)

    @classmethod
    def add_steps(cls, run, steps):
        added = 0
        for step in steps:
            cls.objects.create(node=step.node, time=step.time, run_id=run)
            added += 1
        return added

    def __unicode__(self):
        return self.node


class Value(models.Model):
    value = models.CharField(max_length=100, blank=False)
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE)

    @classmethod
    def add_values(cls, run, values):
        added = 0
        for val in values:
            cls.objects.create(value=val, run_id=run)
            added += 1
        return added

    def __unicode__(self):
        return self.value
