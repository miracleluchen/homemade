from django.db import models

# Create your models here.
class Image(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=256)
	pic = models.CharField(max_length=256)

	class Meta:
		db_table = 'image'


class User(models.Model):
	username = models.CharField(max_length=128)
	kitchen = models.CharField(max_length=128)
	email = models.CharField(max_length=128, unique=True)
	signature = models.CharField(max_length=512)
	mobile = models.CharField(max_length=20, unique=True)
	address = models.CharField(max_length=256)
	postcode = models.CharField(max_length=10)
	nationality = models.CharField(max_length=128)
	province = models.CharField(max_length=128)
	photo = models.CharField(max_length=128)
	gender = models.PositiveSmallIntegerField(default=0)
	birthday= models.DateField()
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'user'


class Food(models.Model):
	name = models.CharField(max_length=128)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	pic = models.CharField(max_length=256)
	user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
	description = models.CharField(max_length=256)
	create_time = models.DateTimeField(auto_now_add=True)
	score = models.PositiveSmallIntegerField()
	dilivery = models.BooleanField(default=0)
	like = models.PositiveIntegerField()

	class Meta:
		unique_together = ('name', 'user')
		db_table = 'food'


class Tag(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		db_table = 'tag'


class FoodTag(models.Model):
	food = models.ForeignKey(Food, on_delete=models.PROTECT, null=True)
	tag = models.ForeignKey(Tag, on_delete=models.PROTECT, null=True)

	class Meta:
		unique_together = ('food', 'tag')
		db_table = 'food_tag'	

class FoodImage(models.Model):
	food = models.ForeignKey(Food, on_delete=models.PROTECT, null=True)
	image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True)

	class Meta:
		unique_together = ('food', 'image')
		db_table = 'food_image'	


class Message(models.Model):
	pass

class Order(models.Model):pass

class OrderDetail(models.Model):pass

class Review(models.Model):pass
