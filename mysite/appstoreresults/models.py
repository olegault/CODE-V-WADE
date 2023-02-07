from django.db import models
import uuid

# Create your models here.
class AppMetrics(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField()
    appID = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=10, decimal_places=9)
    appType = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    downloads = models.CharField(max_length=50)
    appIcon = models.CharField(max_length=200)
    overallScore = models.IntegerField()

    thirdPartySharingScore = models.IntegerField()
    shareAdvertisers = models.BooleanField()
    shareLawEnforcement = models.BooleanField()
    shareDataBrokers = models.BooleanField()
    shareHealthCareProvider = models.BooleanField()

    dataEncryptionScore = models.IntegerField()
    encryptedTransit = models.BooleanField()
    encryptedOnDevice = models.BooleanField()
    encryptedMetadata = models.BooleanField()

    sensitiveDataScore = models.IntegerField()
    collectPII = models.BooleanField()
    collectHealthInfo = models.BooleanField()
    collectReproductiveInfo = models.BooleanField()

    transparencyScore = models.IntegerField()
    requestData = models.BooleanField()
    requestDeletion = models.BooleanField()
    controlData = models.BooleanField()
    controlSharing = models.BooleanField()

    class Meta:
      db_table = "appsMetrics"

    def __str__(self):
        return self.title