from rest_framework import serializers
from django import forms
from .forms import MainForm,GymMainForm
from .models import *
from django.contrib.auth.models import User
class MainFormSerializer(serializers.ModelSerializer):
	first_name=serializers.CharField()
	email = serializers.EmailField()
	username = serializers.CharField()
	password = serializers.CharField()
	class Meta(object):
		model=User
		fields=('id','first_name','username','email','password')
class GymMainFormSerializer(serializers.ModelSerializer):
	first_name=serializers.CharField()
	last_name=serializers.CharField()
	email = serializers.EmailField()
	username = serializers.CharField()
	password = serializers.CharField()
	class Meta(object):
		model=User
		fields=('id','first_name','last_name','username','email','password')
class ClientProfileFormSerializer(serializers.ModelSerializer):
	class Meta:
		model=ClientProfileForm
		fields='__all__'
class EditClientProfileFormSerializer(serializers.ModelSerializer):
	class Meta:
		model=ClientProfileForm
		fields=('id','area','city','pincode','gender','height','weight','dob')
class GymProfileFormSerializer(serializers.ModelSerializer):
	class Meta:
		model=GymProfileForm
		fields='__all__'
class GymPictureFormSerializer(serializers.ModelSerializer):
	class Meta:
		model=GymPictureForm
		fields='__all__'
class ProfileMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model=ProfileMaster
		fields='__all__'
class ClientSubscriptionFormSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClientSubscriptionForm
		fields = '__all__'
class PaymentFormSerializer(serializers.ModelSerializer):
	class Meta:
		model = PaymentForm
		fields = '__all__'
class TranferRequestFormSerializer(serializers.ModelSerializer):
	class Meta:
		model = TranferRequestForm
		fields = '__all__'
class DietChartFormSerializer(serializers.ModelSerializer):
	class Meta:
		model = DietChartForm
		fields = '__all__'
class timelineSerializer(serializers.ModelSerializer):
	class Meta:
		model = timeline
		fields = '__all__'
class WorkoutChartFormSerializer(serializers.ModelSerializer):
	class Meta:
		model = WorkoutChartForm
		fields = '__all__'
class ApplyFormSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApplyForm
		fields = '__all__'
class GymFeaturesSerializer(serializers.ModelSerializer):
	class Meta:
		model = GymFeatures
		fields = '__all__'
class bannerAndroidSerializer(serializers.ModelSerializer):
	class Meta:
		model = bannerAndroid
		fields = '__all__'
class GymZumbaSerializer(serializers.ModelSerializer):
	class Meta:
		model = GymZumba
		fields = '__all__'
class ReferralIdsSerializer(serializers.ModelSerializer):
	class Meta:
		model = ReferralIds
		fields = '__all__'
class ReferralDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = ReferralDetails
		fields = '__all__'