from django.db import models

# Create your models here.

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True, max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category_id}: {self.category_name}"
    

class CategoryValue(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="values")
    category_value = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("category_id", "category_value")

    def __str__(self):
        return f"{self.category_id} : {self.category_value}"
