from django.db import models

# Create your models here.
class AppM3(models.Model):
    appID = models.CharField(max_length=100, primary_key=True, unique=True)
    title = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=10, decimal_places=9)
    appType = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    downloads = models.CharField(max_length=50)
    appIcon = models.CharField(max_length=200)
    overallScore = models.IntegerField()

    thirdPartySharingScore = models.IntegerField()
    shareLawEnforcement = models.BooleanField()

    dataEncryptionScore = models.IntegerField()

    sensitiveDataScore = models.IntegerField()
    
    transparencyScore = models.IntegerField()

    class Meta:
      db_table = "apps"

    def __str__(self):
        return self.title