from django.db import models
from django.contrib.auth.models import User

''''
By default we consider user as StoreManager and 
'''


class StoreManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class DeliveryPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Task(models.Model):

    class Status:
        LOW = 'low'
        MEDIUM = 'medium'
        HIGH = 'high'

    class State:
        NEW = 'new'
        ACCEPTED = 'accepted'
        COMPLETED = 'completed'
        DECLINED = 'declined'
        CANCELLED = 'cancelled'
        PENDING = 'pending'

    status_choices = (
        (0,Status.LOW),
        (1,Status.MEDIUM),
        (2,Status.HIGH)
    )

    state_choices = (
        (State.NEW, State.NEW),
        (State.ACCEPTED, State.ACCEPTED),
        (State.COMPLETED, State.COMPLETED),
        (State.DECLINED, State.DECLINED),
        (State.CANCELLED, State.CANCELLED),
        (State.PENDING, State.PENDING),
    )

    title = models.CharField(max_length=200)
    priority = models.IntegerField(max_length=200, choices=status_choices)
    created = models.DateTimeField()
    created_by = models.ForeignKey(StoreManager, on_delete=models.CASCADE)
    last_state = models.CharField(max_length=200, choices=state_choices)
    delivered_by = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE, null=True, related_name='delivery',blank=True)

    class Meta:
        ordering = ('-priority',)


    def __str__(self):
        return self.title

class TaskState(models.Model):

    class State:
        NEW = 'new'
        ACCEPTED = 'accepted'
        COMPLETED = 'completed'
        DECLINED = 'declined'
        CANCELLED = 'cancelled'
        PENDING = 'pending'

    state_choices = (
        (State.NEW, State.NEW),
        (State.ACCEPTED, State.ACCEPTED),
        (State.COMPLETED, State.COMPLETED),
        (State.DECLINED, State.DECLINED),
        (State.CANCELLED, State.CANCELLED),
        (State.PENDING, State.PENDING),
    )

    state = models.CharField(max_length=200, choices=state_choices)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,  related_name='task_back')
    created = models.DateTimeField()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.state