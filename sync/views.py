from django.shortcuts import render
from sync.models import Group, Step, Value


def index(request):
    groups = Group.objects.all()
    return render(request, 'index.html', {'groups': groups})


def run(request):
    steps = Step.objects.all()
    val = Value.objects.all()
    return render(request, 'run.html', {'steps': steps, 'val': val})

