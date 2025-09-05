from . import *
from .books import Library, Book, Member

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='events')
    books = models.ManyToManyField(Book, related_name='events')

    def __str__(self):
        return f"{self.title} by {self.library}"


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='event_participations')
    registration_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.event} by {self.member}"