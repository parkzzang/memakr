from django.contrib.auth.models import User
from django.db import models

class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template_slug = models.CharField(max_length=50)  # 'bling', 'dragon' 같은 슬러그 저장
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'template_slug')
