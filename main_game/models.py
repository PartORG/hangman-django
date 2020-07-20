from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	word = models.CharField(max_length=25, default='')
	word_letters_count = models.IntegerField(default=0)
	used_letters = models.CharField(max_length=50, default='')
	lives = models.IntegerField(default=6)
	status = models.CharField(max_length=10, default='ongoing')
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.word