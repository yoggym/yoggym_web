from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
from django import forms


class ClientProfileForm(models.Model):
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	city = models.CharField(max_length=50,blank=True)
	area = models.CharField(max_length=100,blank=True)
	pincode = models.CharField(max_length=50,blank=True)
	gender = models.CharField(max_length=10,blank=True)
	height = models.CharField(max_length=100,blank=True,default=0)
	weight = models.CharField(max_length=100,blank=True,default=0)
	dob = models.CharField(max_length=50,blank=True)
	profilePic = models.FileField(blank=True)
class ReferralIds(models.Model):
	referralId = models.CharField(max_length=100)
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
class ReferralDetails(models.Model):
	referralId = models.ForeignKey(ReferralIds,on_delete=models.CASCADE)
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
# class Wallet(models.Model):
# 	userId = models.ForeignKey(User,on_delete=models.CASCADE)
# 	referralId = models.ForeignKey(ReferralIds,on_delete=models.CASCADE)
# 	amount = models.CharField(max_length=100,default=None,blank=True,null=True)
# 	withdrawAmount = models.CharField(max_length=100,default=None,blank=True,null=True)
# 	lastWithdraw = models.DateTimeField(auto_now_add=True)
class GymFeatures(models.Model):
	facility = models.CharField(max_length=10000,blank=True)
	genders = models.CharField(max_length=100,blank=True)
	speciality = models.CharField(max_length=100,blank=True)
	ac = models.BooleanField(blank=True)
	changingRoom = models.BooleanField(blank=True)
	personalTrainer = models.BooleanField(blank=True)
	sauna = models.BooleanField(blank=True)
	locker = models.BooleanField(blank=True)
	zumba = models.BooleanField(blank=True)
class GymProfileForm(models.Model):
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	featuresId = models.ForeignKey(GymFeatures,on_delete=models.CASCADE,null=True)
	houseNo = models.CharField(max_length=50,blank=True)
	city = models.CharField(max_length=50,blank=True)
	state = models.CharField(max_length=50,blank=True)
	country = models.CharField(max_length=50,blank=True)
	pincode = models.CharField(max_length=50,blank=True)
	about = models.CharField(max_length=1000,blank=True)
	additionalInfo = models.CharField(max_length=1000,blank=True)
	testimonial = models.CharField(max_length=10000,blank=True)
	accountNo = models.CharField(max_length=100,blank=True)
	bankName = models.CharField(max_length=100,blank=True)
	IFSCcode = models.CharField(max_length=100,blank=True)
	bankBranch = models.CharField(max_length=100,blank=True)
	openingTime = models.CharField(max_length=100,blank=True)
	closingTime = models.CharField(max_length=100,blank=True)
	closedOn = models.CharField(max_length=100,blank=True)
	monthlyPrice = models.IntegerField(blank=True,null=True)
	monthlyAbout = models.CharField(max_length=200,blank=True)
	quarterlyPrice = models.IntegerField(blank=True,null=True)
	quarterlyAbout = models.CharField(max_length=200,blank=True)
	halfyearlyPrice = models.IntegerField(blank=True,null=True)
	halfyearlyAbout = models.CharField(max_length=200,blank=True)
	yearlyPrice = models.IntegerField(blank=True,null=True)
	yearlyAbout = models.CharField(max_length=200,blank=True)
	ytlink = models.CharField(max_length=1000,blank=True)
	monthlyOriginal = models.IntegerField(blank=True)
	quarterlyOriginal = models.IntegerField(blank=True)
	halfyearlyOriginal = models.IntegerField(blank=True)
	yearlyOriginal = models.IntegerField(blank=True)
class GymZumba(models.Model):
	gymFeatureId = models.ForeignKey(GymFeatures,on_delete=models.CASCADE)
	days = models.CharField(max_length=100)
	time = models.CharField(max_length=100)
	trainer = models.CharField(max_length=100)
	about = models.CharField(max_length=5000)
	fee = models.CharField(max_length=1000)
class GymZumbaImages(models.Model):
	file = models.FileField()
	zumbaId = models.ForeignKey(GymZumba,on_delete=models.CASCADE)
class GymPictureForm(models.Model):
	gymProfileId = models.ForeignKey(GymProfileForm,on_delete=models.CASCADE)
	pic = models.FileField(blank=True)
class ProfileMaster(models.Model):
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	userType = models.CharField(max_length=10)
	clientData = models.ForeignKey(ClientProfileForm,on_delete=models.CASCADE,blank=True,null=True)
	gymData = models.ForeignKey(GymProfileForm,on_delete=models.CASCADE,blank=True,null=True)
class PaymentForm(models.Model):
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	gymId = models.ForeignKey(GymProfileForm,on_delete=models.CASCADE)
	currency = models.CharField(max_length=1000)
	gatewayName = models.CharField(max_length=1000)
	responseMsg = models.CharField(max_length=1000)
	bankName = models.CharField(max_length=1000)
	paymentMode = models.CharField(max_length=1000)
	mid = models.CharField(max_length=1000)
	responseCode = models.CharField(max_length=1000)
	txnId = models.CharField(max_length=1000)
	txnAmount = models.CharField(max_length=1000)
	status = models.CharField(max_length=1000)
	bankTxnId = models.CharField(max_length=1000)
	txnDate = models.CharField(max_length=1000)
	checksumHash = models.CharField(max_length=1000)
class ClientSubscriptionForm(models.Model):
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	gymId = models.ForeignKey(GymProfileForm,on_delete=models.CASCADE)
	startDate = models.DateField()
	dateCreated = models.DateTimeField(auto_now_add=True)
	plan = models.CharField(max_length=100)
	status = models.BooleanField(default=False)
	paymentId = models.ForeignKey(PaymentForm,on_delete=models.CASCADE,null=True,default=None)
class TranferRequestForm(models.Model):
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	oldGymId = models.ForeignKey(GymProfileForm,on_delete=models.CASCADE,related_name='oldGym')
	newGymId = models.ForeignKey(GymProfileForm,on_delete=models.CASCADE,related_name='newGym')
	joiningDate = models.DateField()
	requestDate = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=False)
	subId = models.ForeignKey(ClientSubscriptionForm,on_delete=models.CASCADE)
class DietChartForm(models.Model):
	dietCategory = models.CharField(max_length=1000)
	image = models.FileField()
class WorkoutChartForm(models.Model):
	workoutCategory = models.CharField(max_length=1000)
	image = models.FileField()
class timeline(models.Model):
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	image = models.FileField()
	title = models.CharField(max_length=100)
	status = models.BooleanField(default=False)
	likes = models.ManyToManyField(User,related_name="likes")
	dateCreated = models.DateTimeField(auto_now_add=True)
	def save(self, *args, **kwargs):
		imageTemproary = Image.open(self.image)
		if imageTemproary.mode != 'RGB':
			imageTemproary = imageTemproary.convert('RGB')
		outputIoStream = BytesIO()
		imageTemproaryResized = imageTemproary.resize( (2550,1700) )
		imageTemproaryResized.save(outputIoStream , format='JPEG', quality=85)
		outputIoStream.seek(0)
		self.image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
		super(timeline, self).save(*args, **kwargs)
class ApplyForm(models.Model):
	name = models.CharField(max_length=1000)
	email = models.CharField(max_length=1000)
	phone = models.CharField(max_length=1000)
	post = models.CharField(max_length=1000)
class bannerAndroid(models.Model):
	pic = models.FileField()
class OurServicesImagesAndroid(models.Model):
	serviceName = models.CharField(max_length=1000)
	pic = models.FileField()


	


	