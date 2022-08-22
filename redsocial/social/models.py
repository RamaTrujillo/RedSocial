from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='nadie.png')

	def __str__(self):
		return f'Perfil de {self.user.username}'

	def following(self):
		user_ids = Relationship.objects.filter(from_user=self.user)\
								.values_list('to_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)

	def followers(self):
		user_ids = Relationship.objects.filter(to_user=self.user)\
								.values_list('from_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)

class Post(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created=models.DateTimeField(default=timezone.now)
    content=models.TextField(max_length=300)

    class Meta:
        verbose_name='post'
        ordering=['-created'] #ordena por tiempo en forma decreciente

    def __str__(self):
        return f'{self.user.username}: {self.content}'

class Relationship(models.Model):
	from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.from_user} to {self.to_user}'

	class Meta:
		indexes = [
		models.Index(fields=['from_user', 'to_user',]),
		]







# Create your models here.
