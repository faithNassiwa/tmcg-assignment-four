from django.test import TestCase
from sync.models import Group, Run, Step, Value
from django.utils import timezone


class TestGroup(TestCase):
    def test_add_groups(self):
        group_count = Group.objects.count()
        added_groups = Group.add_groups()
        self.assertEquals(Group.objects.count(), group_count + added_groups)

    def test_group_exists(self):
        class G(object):
            def __init__(self, name=None, uuid=None, query=None, count=None):
                self.name = name
                self.uuid = uuid
                self.query = query
                self.count = count

        rapidpro_mock_group = G(name='Test Group', uuid='random number', query=None, count=4)
        self.assertEquals(Group.group_exists(rapidpro_mock_group), False)
        Group.objects.create(name='Test Group', uuid='random number', query=None, count=4)
        self.assertEquals(Group.group_exists(rapidpro_mock_group), True)


class TestRun(TestCase):
    def test_add_runs(self):
        run_count = Run.objects.count()
        added_runs = Run.add_runs()
        self.assertEquals(Run.objects.count(), run_count + added_runs)

    def test_run_exists(self):
        class T(object):
            def __init__(self, id=None, run_id=None, responded=None, created_on=None, modified_on=None, exit_type=None):
                self.id = run_id
                self.run_id = run_id
                self.responded = responded
                self.created_on = created_on
                self.modified_on = modified_on
                self.exit_type = exit_type

        rapidpro_mock_run = T(run_id=6, responded=False, created_on=timezone.now(), modified_on=timezone.now(),
                              exit_type='completed')
        self.assertEquals(Run.run_exists(rapidpro_mock_run), False)
        Run.objects.create(run_id=6, responded=False, created_on=timezone.now(), modified_on=timezone.now(),
                           exit_type='completed')
        self.assertEquals(Run.run_exists(rapidpro_mock_run), True)

    def test_completed_runs(self):
        mock_run = Run.objects.create(run_id=6, responded=False, created_on=timezone.now(), modified_on=timezone.now()
                                      , exit_type='completed')

        self.assertEquals(mock_run.completed_runs, mock_run)


class TestStep(TestCase):
    def setUp(self):
        r = Run.objects.create(run_id=6, responded=False, created_on=timezone.now(), modified_on=timezone.now(),
                               exit_type='completed')
        s = Step.objects.create(node='788ghh', time=timezone.now(), run_id=r)

    def test_add_steps(self):
        run_object = Run.objects.first()
        steps = Step.objects.all()
        step_count = Step.objects.count()
        added_steps = Step.add_steps(run_object, steps)
        self.assertEquals(Step.objects.count(), step_count + added_steps)


class TestValue(TestCase):
    def setUp(self):
        r = Run.objects.create(run_id=6, responded=False, created_on=timezone.now(), modified_on=timezone.now(),
                               exit_type='Completed')
        v = Value.objects.create(value='testing', run_id=r)

    def test_add_values(self):
        run_object = Run.objects.first()
        values = Value.objects.all()
        value_count = Value.objects.count()
        added_values = Value.add_values(run_object, values)
        self.assertEquals(Value.objects.count(), value_count + added_values)

