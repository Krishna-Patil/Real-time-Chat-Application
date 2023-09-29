from django.db import models
from django.contrib.auth import get_user_model

class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='+')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='+')
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self) -> str:
        return self.text[:20]
    

class Channel(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name