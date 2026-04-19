from django.db import models
from django.contrib.auth.models import User

class Party(models.Model):
    name = models.CharField(max_length=100)
    bengali_name = models.CharField(max_length=100)
    symbol = models.ImageField(
        upload_to='party_symbols/', 
        blank=True, 
        null=True,
        verbose_name="Party Symbol (Image)"
    )
    color = models.CharField(max_length=7, default='#333333')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def vote_count(self):
        return self.votes.count()

class Vote(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vote')
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.party.name}"
