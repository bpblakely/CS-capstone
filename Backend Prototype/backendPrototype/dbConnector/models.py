from django.db import models


class researchint(models.Model):
    name = models.CharField(max_length=200, default="default")
    interest = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    class Meta:
        unique_together = ["name", "interest", "department","email"]
    def __str__(self):
        return self.name + " " + self.interest + " " + self.department + " " + self.email

class publications(models.Model):
    name = models.CharField(max_length=200, default="default")
    publication = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    class Meta:
        unique_together = ["name", "publication", "department", "email"]
    def __str__(self):
        return self.name + " " + self.publication + " " + self.department + " " + self.email

class grants(models.Model):
    name = models.CharField(max_length=200, default="default")
    grant = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    class Meta:
        unique_together = ["name", "grant", "department","email"]
    def __str__(self):
        return self.name + " " + self.grant + " " + self.department + " " + self.email
