from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"


class Job(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} — {self.employer.company_name}"


class JobApplication(models.Model):
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=200)
    applicant_email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')   # correct
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant_name} applied for {self.job.title}"


# Create your models here.


