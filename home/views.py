from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
from django.views.generic import View
from django import template
from django.contrib.auth import authenticate, login 
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import auth
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
import datetime
import hashlib
from random import randint
import random
from django.views.generic.edit import CreateView
from uuid import uuid4
from django.template.context_processors import csrf
from datetime import datetime,date,timedelta
from django.core import serializers
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import csv
from django.apps import apps
from .forms import MainForm,GymMainForm
from .serializers import *
from .models  import *
# from .PaytmChecksum import *
# from .Checksum import *
from django.db.models import Q
from yoggym.settings import EMAIL_HOST_USER
from django.urls import reverse
from django.http import JsonResponse
from django.core.files.base import ContentFile
from braces.views import CsrfExemptMixin
import json
import requests


def index(request):
	MasterGymData1 = ProfileMaster.objects.filter(userType="gym",userId__is_active=True).order_by('-id')[:4]
	MasterGymData2 = ProfileMaster.objects.filter(userType="gym",userId__is_active=True).order_by('-id')[4:8]
	MasterGymData3 = ProfileMaster.objects.filter(userType="gym",userId__is_active=True).order_by('-id')[8:12]
	GymData1 = {}
	GymData2 = {}
	GymData3 = {}
	for k in MasterGymData1:
		images = GymPictureForm.objects.filter(gymProfileId=k.gymData.id).order_by('-id')[:1]
		temp = {"data" : k,"images":images}
		GymData1[k.id]=temp	
	for k in MasterGymData2:
		images = GymPictureForm.objects.filter(gymProfileId=k.gymData.id).order_by('-id')[:1]
		temp = {"data" : k,"images":images}
		GymData2[k.id]=temp	
	for k in MasterGymData3:
		images = GymPictureForm.objects.filter(gymProfileId=k.gymData.id).order_by('-id')[:1]
		temp = {"data" : k,"images":images}
		GymData3[k.id]=temp	
	print(MasterGymData1)
	return render(request,'index.html',{'gymData1':GymData1,'gymData2':GymData2,'gymData3':GymData3})
def phoneOtp(request):
	return render(request,'sign_up_try.html')
def team(request):
	return render(request,'team.html')
def about(request):
	gyms = ProfileMaster.objects.filter(userType="gym")
	return render(request,'about.html',{'gyms':gyms})
def services(request):
	gyms = ProfileMaster.objects.filter(userType="gym")
	return render(request,'services.html',{'gyms':gyms})
def validateForm(request,inputData):
	user=User.objects.filter(username=inputData)
	if(user):
		return HttpResponse("no")
	user=User.objects.filter(email=inputData)
	if(user):
		return HttpResponse("no")
	return HttpResponse("okay")
#Signup API's
class SignupClient(APIView):
	def get(self, request):
		return render(request, 'signup-client.html')
	def post(self, request):
		serializer = MainFormSerializer(data=request.data)
		if serializer.is_valid():
			password=serializer.validated_data['password']
			serializer.validated_data['password']=make_password(password)
			serializer.save()
			form = authenticate(username=serializer.validated_data['username'], password=password)
			login(request, form)
			userData=User.objects.get(username=serializer.validated_data['username'])
			userData.is_active=False
			userData.save()
			# emailto = serializer.validated_data['email']
			# otp = str(random.randint(1000,9999))
			# send_mail(
			# 	'OTP from Yoggyms',
			# 	otp,
			# 	'info@yoggyms.com',
			# 	[emailto],
			# 	fail_silently=False
			# 	)
			# otp=(int(otp)*int(otp))*2
			ClientProfile = ClientProfileForm(userId=form)
			ClientProfile.save()
			referralId = str(serializer.data['id'])+str(random.randint(1000,9999))+"#$"+str(ClientProfile.id)
			referralData = ReferralIds(referralId=referralId,userId=userData,is_active=True)
			referralData.save()
			if('referralId' in request.POST and request.POST['referralId']!=""):
				try:
					referralData = ReferralIds.objects.get(referralId=request.POST['referralId'])
					refData = ReferralDetails(referralId=referralData,userId=form)
					refData.save()
				except:
					pass
			return render(request, 'client-profile-form.html',{'user':form})
		return render(request,'error.html', {'msg':"Wrong Input"})
def otpVerification(request):
	otpEntered = request.POST['otpEntered']
	otpRecieved = request.POST['otpRecieved']
	username = request.POST['username']
	password = request.POST['password']
	otpEntered = (int(otpEntered) * int(otpEntered)) * 2
	if(int(otpRecieved) != otpEntered):
		return render(request,'error.html',{'msg':'Wrong otp!'})
	userData = User.objects.get(username=username)
	userData.is_active = True
	userData.save()
	form = authenticate(username=username, password=password)
	login(request, form)
	return render(request, 'client-profile-form.html',{'user':form})
class SignupGym(APIView):
	def get(self, request):
		return render(request, 'signup-gym.html')
	def post(self, request):
		serializer = GymMainFormSerializer(data=request.data)
		if serializer.is_valid():
			user=User.objects.filter(username=serializer.validated_data['username'])
			if(user):
				return render(request,'error.html',{'msg':"Username Already Exist"})
			user = User.objects.filter(email=serializer.validated_data['email'])
			if(user):
				return render(request,'error.html',{'msg':'Email already Registered'})
			password=serializer.validated_data['password']
			serializer.validated_data['password']=make_password(password)
			serializer.save()
			form = authenticate(username=serializer.validated_data['username'], password=password)
			login(request, form)
			GymProfile = GymProfileForm(userId=form)
			GymProfile.save()
			return render(request, 'gym-profile-form.html',{'user':form})
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			# return render(request,'error.html', {'msg':"Wrong Input"})
class ForgotPassword(APIView):
	def get(self,request):
		return render(request,'forgot-password.html')
	def post(self,request):
		username=request.POST['username']
		password = request.POST['password']
		user=User.objects.filter(username=username)
		if(user):
			print(username)
			user=User.objects.get(username=username)
			print(user)
			enc_pass = make_password(password)
			user.password=enc_pass
			user.save()
			login(request, user)
			return redirect("http://127.0.0.1:8000/")
		else:
			return render(request,'error.html',{'msg':"Username Doesn't Exist"})

#Profile API's
class ClientProfileApi(APIView):
	def get(self,request):
		if(request.session._session):
			user=User.objects.get(id=request.session._session['_auth_user_id'])
			ProfileData = ClientProfileForm.objects.get(userId=user)
			try:
				referralData = ReferralIds.objects.get(userId=user)
				return render(request,'client-profile-form.html',{'profileData':ProfileData,'referralData':referralData})
			except:
				return render(request,'client-profile-form.html',{'profileData':ProfileData})
		else:
			return render(request,'error.html',{'msg':'Please Login First'})
	def post(self,request):
		serializer = ClientProfileFormSerializer(data=request.data)
		if serializer.is_valid():
			user=User.objects.get(id=request.session._session['_auth_user_id'])
			ProfileData = ClientProfileForm.objects.get(userId=user)
			ProfileData.city = serializer.validated_data['city']
			ProfileData.area = serializer.validated_data['area']
			ProfileData.pincode = serializer.validated_data['pincode']
			ProfileData.gender = serializer.validated_data['gender']
			ProfileData.height = serializer.validated_data['height']
			ProfileData.weight = serializer.validated_data['weight']
			ProfileData.dob = serializer.validated_data['dob']
			ProfileData.profilePic = serializer.validated_data['profilePic']
			ProfileData.save()
			ProfileData = ClientProfileForm.objects.get(userId=user)
			ProfileMasterData = ProfileMaster.objects.filter(userId=user,userType="client",clientData=ProfileData)
			if(ProfileMasterData):
				pass
			else:
				ProfileMasterData = ProfileMaster(userId=user,userType="client",clientData=ProfileData)
				ProfileMasterData.save()
			return render(request, 'index.html',{'user':user})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class GymProfileApi(APIView):
	def get(self,request):
		if(request.session._session):
			user=User.objects.get(id=request.session._session['_auth_user_id'])
			ProfileData = GymProfileForm.objects.get(userId=user)
			return render(request,'gym-profile-form.html',{'profileData':ProfileData})
		else:
			return render(request,'error.html',{'msg':'Please Login First'})
	def post(self,request):
		serializer = GymProfileFormSerializer(data=request.data)
		if serializer.is_valid():
			print("here1")
			user=User.objects.get(id=request.session._session['_auth_user_id'])
			ProfileData = GymProfileForm.objects.get(userId=user)
			ProfileData.houseNo = serializer.validated_data['houseNo']
			ProfileData.city = serializer.validated_data['city']
			ProfileData.state = serializer.validated_data['state']
			ProfileData.country = serializer.validated_data['country']
			ProfileData.pincode = serializer.validated_data['pincode']
			ProfileData.save()
			ProfileData = GymProfileForm.objects.get(userId=user)
			ProfileMasterData = ProfileMaster(userId=user,userType="gym",gymData=ProfileData)
			ProfileMasterData.save()
			auth.logout(request)
			user.is_active=False
			user.save()
			print("here2")
			return render(request, 'error.html',{'msg':'Our team will visit your gym soon and then u can login and continue on our site. We will notify the time and date by email.'})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Edit profile API's
class EditClientProfileApi(APIView):
	def get(self,request):
		if(request.session._session):
			user=User.objects.get(id=request.session._session['_auth_user_id'])
			ProfileData = ClientProfileForm.objects.get(userId=user)
			return render(request,'edit-client-profile-form.html',{'profileData':ProfileData})
		else:
			return render(request,'error.html',{'msg':'Please Login First'})
	def post(self,request):
		if(request.session._session):
			serializer = EditClientProfileFormSerializer(data=request.data)
			if serializer.is_valid():
				user=User.objects.get(id=request.session._session['_auth_user_id'])
				ProfileData = ClientProfileForm.objects.get(userId=user)
				ProfileData.city = serializer.validated_data['city']
				ProfileData.area = serializer.validated_data['area']
				ProfileData.pincode = serializer.validated_data['pincode']
				ProfileData.gender = serializer.validated_data['gender']
				ProfileData.height = serializer.validated_data['height']
				ProfileData.weight = serializer.validated_data['weight']
				ProfileData.dob = serializer.validated_data['dob']
				ProfileData.save()
				return redirect("http://127.0.0.1:8000/dashboard")
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return render(request,'error.html',{'msg':'Please Login'})
#Login and logout
class LoginFormApi(APIView):
	def get(self, request):
		return render(request, 'sign-in.html')
	def post(self, request):
		email=request.POST['email']
		username = User.objects.filter(email=email)
		if(username):
			username = User.objects.get(email=email)
		else:
			return render(request,'error.html',{'msg':'Please SignUp First'})
		password=request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				print("User is valid, active and authenticated")
				login(request, user)
				if user.is_superuser:
					return redirect('http://127.0.0.1:8000/adminHome')
				else:
					return redirect('http://127.0.0.1:8000')
			else:
				print("The password is valid, but the account has been disabled!")
				return render(request,'error.html',{'msg':"The account has been disabled!"})
		else:
			print("The username and password were incorrect.")
			return render(request,'error.html',{'msg':"The Email and Password were incorrect!"})
def logout(request):
    auth.logout(request)
    return redirect('http://127.0.0.1:8000')

#Dashboards
def dashboardSwitch(request):
	if(request.session._session):
		ProfileMasterData=ProfileMaster.objects.get(userId=request.session._session['_auth_user_id'])
		if(ProfileMasterData.userType == "client"):
			return redirect("http://127.0.0.1:8000/UserDashboard")
		else:
			return redirect("http://127.0.0.1:8000/GymsDashboard")
	else:
		return redirect("http://127.0.0.1:8000/signin")
def GymsDashboard(request):
	if(request.session._session):
		gymId = GymProfileForm.objects.get(userId=request.session._session['_auth_user_id'])
		clientList = ClientSubscriptionForm.objects.filter(gymId=gymId.id)
		paymentList=PaymentForm.objects.filter(status="TXN_SUCCESS",gymId=gymId.id)
		amount=0
		for k in paymentList:
			amount+=float(k.txnAmount)
		return render(request,"gym-dashboard.html",{'clientList':clientList,'amount':amount})
	else:
		return redirect("http://127.0.0.1:8000/signin")
def ClientDashboard(request):
	if(request.session._session):
		data = ProfileMaster.objects.get(userId=request.session._session['_auth_user_id'])
		if(data.userType=="gym"):
			return redirect("http://127.0.0.1:8000/")
		user=User.objects.get(id=request.session._session['_auth_user_id'])
		ProfileData = ClientProfileForm.objects.get(userId=user)
		subData = ClientSubscriptionForm.objects.filter(userId=user,status=True)
		timelineData = timeline.objects.filter(userId=user,status=True).order_by('-id')
		gyms = ProfileMaster.objects.filter(userType="gym")
		timelineDataList={}
		i=0
		try:
			referralData = ReferralIds.objects.get(userId=user)
		except:
			referralData=""
		for k in timelineData:
			timelineDataList[i]=k.image
			i+=1
		if(subData):
			subData = ClientSubscriptionForm.objects.get(userId=user,status=True)
			if(subData.plan == "monthly"):
				endingDate = subData.startDate + timedelta(days=30)
			elif(subData.plan == "quarterly"):
				endingDate = subData.startDate + timedelta(days=120)
			elif(subData.plan == "yearly"):
				endingDate = subData.startDate + timedelta(days=365)
			else:
				endingDate = subData.startDate + timedelta(days=180)
		else:
			subData = None
			endingDate=""
		bmi=float(ProfileData.weight)/((float(ProfileData.height)/100)*(float(ProfileData.height)/100))
		bmi = round(bmi,2)
		return render(request,'client-profile-page.html',{'profileData':ProfileData,'referralData':referralData,'bmi':bmi,'subData':subData,'endingDate':endingDate,'timelineData':timelineDataList,'gyms':gyms})
	else:
		return redirect('http://127.0.0.1:8000/signin')
def GymDashboard(request,gymId):
	ProfileData = ProfileMaster.objects.get(gymData=gymId)
	Images = GymPictureForm.objects.filter(gymProfileId=ProfileData.gymData.id)
	if(request.session._session):
		user=User.objects.get(id=request.session._session['_auth_user_id'])
		subData = ClientSubscriptionForm.objects.filter(userId=user.id,status=True)
		if(subData):
			subData = ClientSubscriptionForm.objects.get(userId=user.id,status=True)
			return render(request,'gym-profile-page.html',{'profileData':ProfileData,'images':Images,'subData':subData})
		else:
			return render(request,'gym-profile-page.html',{'profileData':ProfileData,'images':Images})
	else:
		return redirect("http://127.0.0.1:8000/signin")
class gymZumbaDetails(APIView):
	def get(self,request,gymId):
		ProfileData = ProfileMaster.objects.get(id=int(gymId))
		zumbaImages = GymZumbaImages.objects.filter(zumbaId__gymFeatureId__id=ProfileData.gymData.featuresId.id)
		print(zumbaImages)
		zumbaData = GymZumba.objects.get(gymFeatureId__id=ProfileData.gymData.featuresId.id)
		if(request.session._session):
			user=User.objects.get(id=request.session._session['_auth_user_id'])
			subData = ClientSubscriptionForm.objects.filter(userId=user.id,status=True)
			if(subData):
				subData = ClientSubscriptionForm.objects.get(userId=user.id,status=True)
				return render(request,'gym-zumba-page.html',{'profileData':ProfileData,'zumbaData':zumbaData,'zumbaImages':zumbaImages,'subData':subData})
			else:
				return render(request,'gym-zumba-page.html',{'profileData':ProfileData,'zumbaData':zumbaData,'zumbaImages':zumbaImages})
		else:
			return redirect("http://127.0.0.1:8000/signin")
#Gym Catalog
class gymCatalog(APIView):
	def get(self,request):
		MasterGymData = ProfileMaster.objects.filter(userType="gym",userId__is_active=True)
		GymData = {}
		for k in MasterGymData:
			images = GymPictureForm.objects.filter(gymProfileId=k.gymData.id).order_by('-id')[:3]
			temp = {"data" : k,"images":images}
			GymData[k.id]=temp
		return render(request,'gym-catalog.html',{'gymData':GymData})
	def post(self,request):
		pass
class TransferSubsciption(APIView):
	def get(self,request):
		if(request.session._session):
			user = User.objects.get(id=request.session._session['_auth_user_id'])
			subData = ClientSubscriptionForm.objects.filter(userId=user.id,status=True)
			if(subData):
				subData = ClientSubscriptionForm.objects.get(userId=user.id,status=True)
				paymentData = PaymentForm.objects.get(userId=user.id)
				gymData = GymProfileForm.objects.filter(Q(monthlyPrice=float(paymentData.txnAmount)) | Q(quarterlyPrice=float(paymentData.txnAmount)) | Q(yearlyPrice=float(paymentData.txnAmount)) | Q(halfyearlyPrice=float(paymentData.txnAmount)))
				GymData = {}
				for k in gymData:
					images = GymPictureForm.objects.filter(gymProfileId=k.id).order_by('-id')[:2]
					temp = {"data" : k,"images":images}
					GymData[k.id]=temp
				return render(request,'transfer-gym-catalog.html',{'gymData':GymData,'subData':subData})
			else:
				return render(request,'error.html',{'msg':'First Buy Subscription of any Gym Please.'})
		else:
			return redirect('http://127.0.0.1:8000/signin')
	def post(self,request):
		if(request.session._session):
			reqData = TranferRequestForm.objects.filter(userId=request.POST['userId'],status=False)
			if(reqData):
				return render(request,"error.html",{'msg':'You have already submitted one request. Please wait for it to be accepted or declined.'})
			else:
				serializer = TranferRequestFormSerializer(data=request.data)
				if serializer.is_valid():
					serializer.save()
					return render(request,"success.html",{'msg':'Request Successfully Submitted. You will be notified by Email when your request will be accepted by our team.'})
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return redirect("http://127.0.0.1:8000/signin")
#Client Subscription and Payment
class BookOrder(APIView):
	def post(self, request):
		if(request.session._session):
			subData = ClientSubscriptionForm.objects.filter(userId=request.session._session['_auth_user_id'],status=True)
			if subData:
				return render(request,'error.html',{'msg':'Already Joined a gym. Please use transfer subscription service.'})
			else:
				serializer = ClientSubscriptionFormSerializer(data=request.data)
				if serializer.is_valid():
					subData = serializer.save()
					url="http://127.0.0.1:8000/payment/"+str(subData.id)
					return redirect(url)
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return redirect("http://127.0.0.1:8000/signin")
def paytmStart(request,orderId):
	if(request.session._session):
		subData = ClientSubscriptionForm.objects.get(id=orderId)
		if(subData.plan == "monthly"):
			amount = subData.gymId.monthlyPrice
		elif(subData.plan == "quarterly"):
			amount = subData.gymId.quarterlyPrice
		elif(subData.plan == "yearly"):
			amount = subData.gymId.yearlyPrice
		else:
			amount = subData.gymId.halfyearlyPrice
		paytmParams = {
		"MID" : "xPqEzW24269949974387",
		"WEBSITE" : "WEBSTAGING",
		"INDUSTRY_TYPE_ID" : "Retail",
		"CHANNEL_ID" : "WEB",
		"ORDER_ID" : str(subData.id)+"-"+str( date.today()),
		"CUST_ID" : str(subData.userId.id),
		"MOBILE_NO" : subData.userId.username,
		"EMAIL" : subData.userId.email,
		"TXN_AMOUNT" : str(amount),
		"CALLBACK_URL" : "http://127.0.0.1:8000/success",
		}
		checksum = generateSignature(paytmParams, "Avn8R2W8FL4wX3Ut")
		print("generateSignature Returns:" + str(checksum))
		url = "https://securegw-stage.paytm.in/order/process"
		return render(request,'gym-confirm-sub.html',{'paytmParams':paytmParams,'url':url,'checksum':checksum,'subData':subData})
	else:
		return render(request,'error.html',{'msg':'Login First'})
@csrf_protect
@csrf_exempt
def success(request):
	received_data = request.POST
	print(received_data)
	paytmChecksum = ""
	paytmParams = {}
	for key, value in received_data.items(): 
		if key == 'CHECKSUMHASH':
			paytmChecksum = value
		else:
			paytmParams[key] = value
	isValidChecksum = verify_checksum(paytmParams, "Avn8R2W8FL4wX3Ut", paytmChecksum)
	orderId = paytmParams['ORDERID'].split('-')
	print(orderId[0])
	SubData = ClientSubscriptionForm.objects.get(id=int(orderId[0]))
	Payment = PaymentForm(userId=SubData.userId,gymId=SubData.gymId,currency=received_data['CURRENCY'],gatewayName=received_data['GATEWAYNAME'],responseMsg=received_data['RESPMSG'],bankName=received_data['BANKNAME'],paymentMode=received_data['PAYMENTMODE'],mid=received_data['MID'],responseCode=received_data['RESPCODE'],txnId=received_data['TXNID'],txnAmount=received_data['TXNAMOUNT'],status=received_data['STATUS'],bankTxnId=received_data['BANKTXNID'],txnDate=received_data['TXNDATE'],checksumHash=received_data['CHECKSUMHASH'])
	Payment.save()
	if isValidChecksum:
		if(received_data['RESPCODE']=='01'):
			SubData.paymentId = Payment
			SubData.status = True
			SubData.save()
			return render(request,"success.html",{'msg':'Registration Successfull. Visit the Gym on joining date to start.'})
		else:
			return render(request,'error.html',{'msg':received_data['RESPMSG']})
	else:
		print("Checksum Mismatched")
		return render(request,'error.html',{'msg':'Some Error Occured! Please Try agian Later!'})
def ClientDietChart(request):
	if(request.session._session):
		client = User.objects.get(id=request.session._session['_auth_user_id'])
		masterData = ProfileMaster.objects.get(userId=client.id)
		bmi=float(masterData.clientData.weight)/((float(masterData.clientData.height)/100)*(float(masterData.clientData.height)/100))
		bi = round(bmi,2)
		if bmi < 18.5:
			dietData = DietChartForm.objects.filter(dietCategory="underweight")
			return render(request,'client-diet-chart.html',{'dietData':dietData})
		elif bmi >= 18.5 and bmi <= 24.9:
			dietData = DietChartForm.objects.filter(dietCategory="normalWeight")
			return render(request,'client-diet-chart.html',{'dietData':dietData})
		elif bmi > 24.9 and bmi <= 29.9:
			dietData = DietChartForm.objects.filter(dietCategory="overweight")
			return render(request,'client-diet-chart.html',{'dietData':dietData})
		else:
			dietData = DietChartForm.objects.filter(dietCategory="obese")
			return render(request,'client-diet-chart.html',{'dietData':dietData})
	else:
		return redirect("http://127.0.0.1:8000/signin")
def ClientWorkoutChart(request):
	if(request.session._session):
		client = User.objects.get(id=request.session._session['_auth_user_id'])
		masterData = ProfileMaster.objects.get(userId=client.id)
		bmi=float(masterData.clientData.weight)/((float(masterData.clientData.height)/100)*(float(masterData.clientData.height)/100))
		bi = round(bmi,2)
		if bmi < 18.5:
			workoutData = WorkoutChartForm.objects.filter(workoutCategory="underweight")
			return render(request,'client-workout-chart.html',{'workoutData':workoutData})
		elif bmi >= 18.5 and bmi <= 24.9:
			workoutData = WorkoutChartForm.objects.filter(workoutCategory="normalWeight")
			return render(request,'client-workout-chart.html',{'workoutData':workoutData})
		elif bmi > 24.9 and bmi <= 29.9:
			workoutData = WorkoutChartForm.objects.filter(workoutCategory="overweight")
			return render(request,'client-workout-chart.html',{'workoutData':workoutData})
		else:
			workoutData = WorkoutChartForm.objects.filter(workoutCategory="obese")
			return render(request,'client-workout-chart.html',{'workoutData':workoutData})
	else:
		return redirect("http://127.0.0.1:8000/signin")
class ClientTimeline(APIView):
	def get(self,request):
		if(request.session._session):
			# user = User.objects.get(id=request.session._session['_auth_user_id'])
			imageData = timeline.objects.filter(userId=request.session._session['_auth_user_id'])
			return render(request,'client-timeline-page.html',{'imageData':imageData})
		else:
			return redirect("http://127.0.0.1:8000/signin")
	def post(self,request):
		serializer = timelineSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			url="http://127.0.0.1:8000/Timeline"
			return redirect(url)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def viewTimeline(request):
	TimelineData = timeline.objects.filter(status=True).order_by('-id')
	Data={}
	for k in TimelineData:
		if k.likes.filter(id=request.user.id).exists():
			Data[k.id] = {'data':k,'liked':True}
		else:
			Data[k.id] = {'data':k,'liked':False}
	return render(request,'timeline.html',{'Data':Data})
class applyForm(APIView):
	def post(self,request):
		serializer = ApplyFormSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			url="http://127.0.0.1:8000/about"
			return redirect(url)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Editor Section
def editorHome(request):
	if(request.session._session):
		editor = User.objects.get(id=request.session._session['_auth_user_id'])
		if editor.is_staff is True:
			return render(request,'site-editors/editor-index.html')
	else:
		return redirect('http://127.0.0.1:8000/signin')
def viewApps(request):
	if(request.session._session):
		editor = User.objects.get(id=request.session._session['_auth_user_id'])
		if editor.is_staff is True:
			appData = ApplyForm.objects.all()
			print(appData)
			return render(request,'site-editors/view-apps.html',{'appData':appData})
	else:
		return redirect('http://127.0.0.1:8000/signin')
class GymRequestApi(APIView):
	def get(self,request):
		GymList = ProfileMaster.objects.filter(userType="gym")
		return render(request,'site-editors/view-gym-requests.html',{'gymList':GymList})
	def post(self,request):
		GymId = request.POST['id']
		GymData = ProfileMaster.objects.get(id=GymId)
		GymUserData = User.objects.get(id=GymData.userId.id)
		GymUserData.is_active=False
		GymUserData.save()
		return redirect('http://127.0.0.1:8000/gymRequests')
class gymAddDetailsForm(APIView):
	def get(self,request,gymId):
		return render(request,'site-editors/gym-add-details.html',{'gymId':gymId})
	def post(self,request):
		files=request.FILES.getlist('pics')
		zumbaFile=request.FILES.getlist('image')
		gymFeatures = GymFeatures(facility=request.POST['facility'],genders=request.POST['genders'],speciality=request.POST['speciality'],ac=request.POST['ac'],changingRoom=request.POST['changingRoom'],personalTrainer=request.POST['personalTrainer'],sauna=request.POST['sauna'],locker=request.POST['locker'])	
		if(request.POST['days']):
			gymFeatures.zumba = True
		gymFeatures.save()
		if(request.POST['days']):
			zumbaDetails = GymZumba(gymFeatureId=gymFeatures,days=request.POST['days'],time=request.POST['time'],trainer=request.POST['trainer'],about=request.POST['about'],fee=request.POST['fee'])
			zumbaDetails.save()
			for x in range(0,len(zumbaFile)):
				zumbaPics = GymZumbaImages(file=zumbaFile[x],zumbaId=zumbaDetails)
				zumbaPics.save()
		MasterData = ProfileMaster.objects.get(id=request.POST['gymId'])
		GymData = GymProfileForm.objects.get(id=MasterData.gymData.id)
		GymData.about = request.POST['about']
		GymData.additionalInfo = request.POST['additionalInfo']
		GymData.testimonial = request.POST['testimonial']
		GymData.accountNo = request.POST['accountNo']
		GymData.bankName = request.POST['bankName']
		GymData.IFSCcode = request.POST['IFSCcode']
		GymData.bankBranch = request.POST['bankBranch']
		GymData.openingTime = request.POST['openingTime']
		GymData.closingTime = request.POST['closingTime']
		GymData.closedOn = request.POST['closedOn']
		GymData.monthlyPrice = request.POST['monthlyPrice']
		GymData.monthlyAbout = request.POST['monthlyAbout']
		GymData.quarterlyPrice = request.POST['quarterlyPrice']
		GymData.quarterlyAbout = request.POST['quarterlyAbout']
		GymData.halfyearlyPrice = request.POST['halfyearlyPrice']
		GymData.halfyearlyAbout = request.POST['halfyearlyAbout']
		GymData.yearlyPrice = request.POST['yearlyPrice']
		GymData.yearlyAbout = request.POST['yearlyAbout']
		GymData.monthlyOriginal = request.POST['monthlyOriginal']
		GymData.quarterlyOriginal = request.POST['quarterlyOriginal']
		GymData.halfyearlyOriginal = request.POST['halfyearlyOriginal']
		GymData.yearlyOriginal = request.POST['yearlyOriginal']
		GymData.ytlink = request.POST['ytlink']
		GymData.featuresId = gymFeatures
		GymData.save()
		for k in files:
			GymImages = GymPictureForm(gymProfileId=GymData,pic=k)
			GymImages.save()	
		GymUserData = User.objects.get(id=MasterData.userId.id)
		GymUserData.is_active = True
		GymUserData.save()
		return redirect("http://127.0.0.1:8000/")
def EditGymRequest(request):
	if(request.session._session):
		user = User.objects.get(id=request.session._session['_auth_user_id'])
		if user.is_staff:
			GymList = ProfileMaster.objects.filter(userType="gym")
			return render(request,'site-editors/edit-gyms.html',{'gymList':GymList})
		else:
			return render(request,'error.html',{'msg':'Please Login with Editor Account'})
	else:
		return redirect("http://127.0.0.1:8000/signin")
class EditGym(APIView):
	def get(self,request,gymId):
		if(request.session._session):
			user = User.objects.get(id=request.session._session['_auth_user_id'])
			if user.is_staff:
				gymData = ProfileMaster.objects.get(id=gymId)
				return render(request,'site-editors/gym-edit-details.html',{'gymData':gymData})
			else:
				return render(request,'error.html',{'msg':'Please Login with Editor Account'})
		else:
			return redirect("http://127.0.0.1:8000/signin")
	def post(self,request):
		files=request.FILES.getlist('pics')
		features = GymFeatures.objects.get(id=request.POST['featuresId'])
		features.facility=request.POST['facility']
		features.genders=request.POST['genders']
		features.speciality=request.POST['speciality']
		features.ac=request.POST['ac']
		features.changingRoom=request.POST['changingRoom']
		features.personalTrainer=request.POST['personalTrainer']
		features.sauna=request.POST['sauna']
		features.locker=request.POST['locker']	
		features.save()
		MasterData = ProfileMaster.objects.get(id=request.POST['gymId'])
		GymData = GymProfileForm.objects.get(id=MasterData.gymData.id)
		GymData.about = request.POST['about']
		GymData.additionalInfo = request.POST['additionalInfo']
		GymData.testimonial = request.POST['testimonial']
		GymData.accountNo = request.POST['accountNo']
		GymData.bankName = request.POST['bankName']
		GymData.IFSCcode = request.POST['IFSCcode']
		GymData.bankBranch = request.POST['bankBranch']
		GymData.openingTime = request.POST['openingTime']
		GymData.closingTime = request.POST['closingTime']
		GymData.closedOn = request.POST['closedOn']
		GymData.monthlyPrice = request.POST['monthlyPrice']
		GymData.monthlyAbout = request.POST['monthlyAbout']
		GymData.quarterlyPrice = request.POST['quarterlyPrice']
		GymData.quarterlyAbout = request.POST['quarterlyAbout']
		GymData.halfyearlyPrice = request.POST['halfyearlyPrice']
		GymData.halfyearlyAbout = request.POST['halfyearlyAbout']
		GymData.yearlyPrice = request.POST['yearlyPrice']
		GymData.yearlyAbout = request.POST['yearlyAbout']
		GymData.monthlyOriginal = request.POST['monthlyOriginal']
		GymData.quarterlyOriginal = request.POST['quarterlyOriginal']
		GymData.halfyearlyOriginal = request.POST['halfyearlyOriginal']
		GymData.yearlyOriginal = request.POST['yearlyOriginal']
		GymData.ytlink = request.POST['ytlink']
		GymData.featuresId = features
		GymData.save()
		return redirect("http://127.0.0.1:8000/")
def EditGymImages(request,gymId):
	if(request.session._session):
		user = User.objects.get(id=request.session._session['_auth_user_id'])
		if user.is_staff is True:
			images = GymPictureForm.objects.filter(gymProfileId=gymId)
			return render(request,'site-editors/gym-edit-images.html',{'images':images,'gymId':gymId})
		else:
			return render(request,'error.html',{'msg':'You are not an Editor!'})
	else:
		return redirect("http://127.0.0.1:8000/signin")
def deleteGymImage(request,imageId):
	if(request.session._session):
		user = User.objects.get(id=request.session._session['_auth_user_id'])
		if user.is_staff is True:
			image = GymPictureForm.objects.get(id=imageId)
			images = GymPictureForm.objects.filter(gymProfileId=image.gymProfileId)
			image.delete()
			return render(request,'site-editors/gym-edit-images.html',{'images':images})
		else:
			return render(request,'error.html',{'msg':'You are not an Editor!'})
	else:
		return redirect("http://127.0.0.1:8000/signin")
def addGymImages(request):
	if(request.session._session):
		user = User.objects.get(id=request.session._session['_auth_user_id'])
		if user.is_staff is True:
			files=request.FILES.getlist('pics')
			gymId = GymProfileForm.objects.get(id=request.POST['gymId'])
			for k in files:
				GymImages = GymPictureForm(gymProfileId=gymId,pic=k)
				GymImages.save()
			images = GymPictureForm.objects.filter(gymProfileId=gymId)
			return render(request,'site-editors/gym-edit-images.html',{'images':images})
		else:
			return render(request,'error.html',{'msg':'You are not an Editor!'})
	else:
		return redirect("http://127.0.0.1:8000/signin")
class ViewTransferRequests(APIView):
	def get(self,request):
		if(request.session._session):
			user = User.objects.get(id=request.session._session['_auth_user_id'])
			if user.is_staff is True:
				reqData = TranferRequestForm.objects.filter(status=False)
				return render(request,'site-editors/view-transfer-request.html',{'reqData':reqData})
			else:
				return render(request,'error.html',{'msg':'You are not an Editor!'})
		else:
			return redirect("http://127.0.0.1:8000/signin")
	def post(self,request):
		pass
def transferReqApprove(request,reqId):
	if(request.session._session):
		user = User.objects.get(id=request.session._session['_auth_user_id'])
		if user.is_staff is True:
			reqData = TranferRequestForm.objects.get(id=reqId)
			subData = ClientSubscriptionForm.objects.get(id=reqData.subId.id)
			subData.gymId = reqData.newGymId
			if(float(reqData.newGymId.monthlyPrice) == float(subData.paymentId.txnAmount)):
				plan = "monthly"
			elif(float(reqData.newGymId.quarterlyPrice) == float(subData.paymentId.txnAmount)):
				plan = "quarterly"
			elif(float(reqData.newGymId.yearlyPrice) == float(subData.paymentId.txnAmount)):
				plan = "yearly"
			else:
				plan = "halfyearly"
			subData.plan = plan
			subData.startDate = reqData.joiningDate
			subData.save()
			reqData.status=True
			reqData.save()
			return render(request,'success.html',{'msg':'YAYAY'})
		else:
			return render(request,'error.html',{'msg':'You are not an Editor!'})
	else:
		return redirect("http://127.0.0.1:8000/signin")
def transferReqDecline(request,reqId):
	if(request.session._session):
		user = User.objects.get(id=request.session._session['_auth_user_id'])
		if user.is_staff is True:
			reqData = TranferRequestForm.objects.get(id=reqId)
			reqData.delete()
			return redirect("http://127.0.0.1:8000/ViewTransferRequests")
		else:
			return render(request,'error.html',{'msg':'You are not an Editor!'})
	else:
		return redirect("http://127.0.0.1:8000/signin")
def clientList(request):
	if(request.session._session):
		user = User.objects.get(id=request.session._session['_auth_user_id'])
		if user.is_staff is True:
			clientData = ProfileMaster.objects.filter(userType="client")
			return render(request,"site-editors/client-list-diet.html",{'clientData':clientData})
		else:
			return render(request,'error.html',{'msg':'You are not an Editor!'})
	else:
		return redirect("http://127.0.0.1:8000/signin")
class addDietChart(APIView):
	def get(self,request):
		if(request.session._session):
			user = User.objects.get(id=request.session._session['_auth_user_id'])
			if user.is_staff is True:
				return render(request,"site-editors/add-diet-chart.html")
			else:
				return render(request,'error.html',{'msg':'You are not an Editor!'})
		else:
			return redirect("http://127.0.0.1:8000/signin")
	def post(self,request):
		dietData = DietChartForm.objects.filter(dietCategory=request.POST['dietCategory'])
		if(dietData):
			dietData = DietChartForm.objects.get(dietCategory=request.POST['dietCategory'])
			dietData.image = request.FILES['image']
			dietData.save()
		else:
			dietData = DietChartForm(dietCategory=request.POST['dietCategory'],image=request.FILES['image'])
			dietData.save()
		url="http://127.0.0.1:8000/editorHome"
		return redirect(url)
def clientWorkoutList(request):
	if(request.session._session):
		user = User.objects.get(id=request.session._session['_auth_user_id'])
		if user.is_staff is True:
			clientData = ProfileMaster.objects.filter(userType="client")
			return render(request,"site-editors/client-list-workout.html",{'clientData':clientData})
		else:
			return render(request,'error.html',{'msg':'You are not an Editor!'})
	else:
		return redirect("http://127.0.0.1:8000/signin")
class addWorkoutChart(APIView):
	def get(self,request):
		if(request.session._session):
			user = User.objects.get(id=request.session._session['_auth_user_id'])
			if user.is_staff is True:
				return render(request,"site-editors/add-workout-chart.html")
			else:
				return render(request,'error.html',{'msg':'You are not an Editor!'})
		else:
			return redirect("http://127.0.0.1:8000/signin")
	def post(self,request):
		workoutData = WorkoutChartForm.objects.filter(workoutCategory=request.POST['workoutCategory'])
		if(workoutData):
			workoutData = WorkoutChartForm.objects.get(workoutCategory=request.POST['workoutCategory'])
			workoutData.image = request.FILES['image']
			workoutData.save()
		else:
			workoutData = WorkoutChartForm(workoutCategory=request.POST['workoutCategory'],image=request.FILES['image'])
			workoutData.save()
		url="http://127.0.0.1:8000/editorHome"
		return redirect(url)
class ApproveTimeline(APIView):
	def get(self,request):
		if(request.session._session):
			user = User.objects.get(id=request.session._session['_auth_user_id'])
			if user.is_staff is True:
				data = timeline.objects.filter(status=False)
				return render(request,"site-editors/approve-timeline.html",{'data':data})
			else:
				return render(request,'error.html',{'msg':'You are not an Editor!'})
		else:
			return redirect("http://127.0.0.1:8000/signin")
def timelineApprove(request,imageId):
	if(request.session._session):
		user = User.objects.get(id=request.session._session['_auth_user_id'])
		if user.is_staff is True:
			data = timeline.objects.get(id=imageId)
			data.status = True
			data.save()
			data = timeline.objects.filter(status=False)
			return render(request,"site-editors/approve-timeline.html",{'data':data})
		else:
			return render(request,'error.html',{'msg':'You are not an Editor!'})
	else:
		return redirect("http://127.0.0.1:8000/signin")
def timelineDecline(request,imageId):
	if(request.session._session):
		user = User.objects.get(id=request.session._session['_auth_user_id'])
		if user.is_staff is True:
			data = timeline.objects.get(id=imageId)
			data.delete()
			data = timeline.objects.filter(status=False)
			return render(request,"site-editors/approve-timeline.html",{'data':data})
		else:
			return render(request,'error.html',{'msg':'You are not an Editor!'})
	else:
		return redirect("http://127.0.0.1:8000/signin")
#Admin Section
class UploadAndroidBanner(APIView):
	def get(self,request):
		if(request.session._session):
			admin = User.objects.get(id=request.session._session['_auth_user_id'])
			if admin.is_superuser is True:
				return render(request,'site-admin/upload-app-banner.html')
			else:
				return render(request,'error.html',{'msg':'Please Login with Admin Account'})
		else:
			return redirect('http://127.0.0.1:8000/signin')
	def post(self,request):
		if(request.session._session):
			admin = User.objects.get(id=request.session._session['_auth_user_id'])
			if admin.is_superuser is True:
				serializer = bannerAndroidSerializer(data=request.data)
				print("here")
				if serializer.is_valid():
					print("ausud")
					serializer.save()
					return render(request,'site-admin/upload-app-banner.html')
				else:
					return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
					# return render(request,'error.html',{'msg':"OOPs Not upload"})
			else:
				return render(request,'error.html',{'msg':'Please Login with Admin Account'})
		else:
			return redirect('http://127.0.0.1:8000/signin')
def adminHome(request):
	if(request.session._session):
		admin = User.objects.get(id=request.session._session['_auth_user_id'])
		if admin.is_superuser is True:
			return render(request,'site-admin/admin-index.html')
		else:
			return render(request,'error.html',{'msg':'Please Login with Admin Account'})
	else:
		return redirect('http://127.0.0.1:8000/signin')
class AddEditor(APIView):
	def get(self, request):
		if(request.session._session):
			admin = User.objects.get(id=request.session._session['_auth_user_id'])
			if admin.is_superuser is True:
				editorList=User.objects.filter(is_staff=True,is_active=True)
				return render(request, 'site-admin/view-add-editors.html',{'editorList':editorList})
			else:
				return render(request,'error.html',{'msg':'Please Login with Admin Account'})
		else:
			return redirect('http://127.0.0.1:8000/signin')
	def post(self, request):
		if(request.session._session):
			admin = User.objects.get(id=request.session._session['_auth_user_id'])
			if admin.is_superuser is True:
				serializer = MainFormSerializer(data=request.data)
				if serializer.is_valid():
					user=User.objects.filter(username=serializer.validated_data['username'])
					if(user):
						return render(request,'signin.html',{'msg':"Username Already Exist"})
					user = User.objects.filter(email=serializer.validated_data['email'])
					if(user):
						return render(request,'error.html',{'msg':'Email already Registered'})
					password=serializer.validated_data['password']
					serializer.validated_data['password']=make_password(password)
					serializer.save()
					user=User.objects.get(username=serializer.validated_data['username'])
					user.is_staff = True
					user.save()
					return render(request, 'site-admin/view-add-editors.html')
				return render(request,'error.html', {'msg':"Wrong Input"})
			else:
				return render(request,'error.html',{'msg':'Please Login with Admin Account'})
		else:
			return redirect('http://127.0.0.1:8000/signin')
class ViewDeleteGyms(APIView):
	def get(self,request):
		if(request.session._session):
			admin = User.objects.get(id=request.session._session['_auth_user_id'])
			if admin.is_superuser is True:
				gymList = ProfileMaster.objects.filter(userType="gym")
				return render(request,'site-admin/view-delete-gyms.html',{'gymData':gymList})
		else:
			return redirect('http://127.0.0.1:8000/signin')
	def post(self,request):
		gymId = request.POST['id']
		gymList = ProfileMaster.objects.get(id=gymId)
		gymData = User.objects.get(id=gymList.userId.id)
		gymData.is_active=False
		gymData.save()
		gymList.delete()
		gymList = ProfileMaster.objects.filter(userType="gym")
		return render(request,'site-admin/view-delete-clients.html',{'gymData':gymList})
def deleteEditor(request,userId):
	if(request.session._session):
		admin = User.objects.get(id=request.session._session['_auth_user_id'])
		if admin.is_superuser is True:
			editorData = User.objects.get(id=userId)
			editorData.is_active=False
			editorData.save() 
			editorList=User.objects.filter(is_staff=True,is_active=True)
			return render(request,'site-admin/view-add-editors.html',{'editorList':editorList} )
		else:
			return render(request,'error.html',{'msg':'Please Login with Admin Account'})
	else:
		return redirect('http://127.0.0.1:8000/signin')
class ViewDeleteClients(APIView):
	def get(self,request):
		if(request.session._session):
			admin = User.objects.get(id=request.session._session['_auth_user_id'])
			if admin.is_superuser is True:
				clientList = ProfileMaster.objects.filter(userType="client")
				return render(request,'site-admin/view-delete-clients.html',{'clientData':clientList})
		else:
			return redirect('http://127.0.0.1:8000/signin')
	def post(self,request):
		clientId = request.POST['id']
		clientList = ProfileMaster.objects.get(id=clientId)
		clientData = User.objects.get(id=clientList.userId.id)
		clientData.is_active=False
		clientData.save()
		clientList.delete()
		clientList = ProfileMaster.objects.filter(userType="client")
		return render(request,'site-admin/view-delete-clients.html',{'clientData':clientList})
def viewPayment(request):
	if(request.session._session):
		admin = User.objects.get(id=request.session._session['_auth_user_id'])
		if admin.is_superuser is True:
			paymentData = PaymentForm.objects.all()
			return render(request,'site-admin/view-payments.html',{'paymentData':paymentData})
		else:
			return render(request,'error.html',{'msg':'Please Login with Admin Account'})
	else:
		return redirect('http://127.0.0.1:8000/signin')
def ajaxlike(request):
	TimelineData = timeline.objects.filter(status=True)
	Data={}
	for k in TimelineData:
		if k.likes.filter(id=request.user.id).exists():
			Data[k.id] = {'data':k,'liked':True}
		else:
			Data[k.id] = {'data':k,'liked':False}
	print(Data)
	return render(request,'ajax-like.html',{'Data':Data})
class like(APIView):
	def get(self,request,postId):
		post = timeline.objects.get(id=postId)
		post.likes.add(request.user)
		print(post.likes.count())
		data = {'id':post.id,'like':post.likes.count()}
		return JsonResponse(data)
class unlike(APIView):
	def get(self,request,postId):
		post = timeline.objects.get(id=postId)
		post.likes.remove(request.user)
		data = {'id':post.id,'like':post.likes.count()}
		return JsonResponse(data)
######################Android API's################################33
class LoginFormApiAndroid(APIView):
	def get(self, request):
		return render(request, 'sign-in.html')
	def post(self, request):
		print(request.data)
		email=request.POST['email']
		username = User.objects.filter(email=email)
		if(username):
			username = User.objects.get(email=email)
		else:
			return HttpResponse("Email not found! Please Signup First")
		password=request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				serializer = MainFormSerializer(user)
				return Response(serializer.data)
			else:
				return HttpResponse("Your Account has been disabled")
		else:
			return HttpResponse("Incorrect Username or password")
class SignupClientAndroid(APIView):
	def get(self, request):
		return render(request, 'signup-client.html')
	def post(self, request):
		password=request.POST['password']
		enc_pass=make_password(password)
		user = User.objects.filter(email=request.POST['email'])
		if(user):
			return HttpResponse('Already Exist')
		user = User.objects.filter(username=request.POST['phone'])
		if(user):
			return HttpResponse('Already Exist')	
		user = User(first_name=request.POST['name'],email=request.POST['email'],password=enc_pass,username=request.POST['phone'],is_active=False)
		user.save()
		# profilePic = request.POST['profilePic']
		# profilePic= ContentFile(base64.b64decode(profilePic), name=str(user.id)+'.' + "jpg")
		ClientProfile = ClientProfileForm(userId=user,city=request.POST['city'],area=request.POST['area'],pincode=request.POST['pincode'],gender=request.POST['gender'],height=request.POST['height'],weight=request.POST['weight'],dob=request.POST['dob'])
		ClientProfile.save()
		referralId = str(user.id)+str(random.randint(1000,9999))+"#$"+str(ClientProfile.id)
		referralData = ReferralIds(referralId=referralId,userId=user,is_active=True)
		referralData.save()
		ProfileData = ClientProfileForm.objects.get(userId=user)
		ProfileMasterData = ProfileMaster.objects.filter(userId=user,userType="client",clientData=ProfileData)
		if(ProfileMasterData):
			pass
		else:
			ProfileMasterData = ProfileMaster(userId=user,userType="client",clientData=ProfileData)
			ProfileMasterData.save()
		if('referralId' in request.POST and request.POST['referralId']!=""):
			print("here")
			try:
				referralData = ReferralIds.objects.get(referralId=request.POST['referralId'])
				refData = ReferralDetails(referralId=referralData,userId=user)
				refData.save()
			except Exception as e:
				print(e)
		response={'status':'success'}
		user.is_active = True
		user.save()
		return HttpResponse("Registered Successfully")
		# return Response(serializer.data)
class ClientProfileApiAndroid(APIView):
	def get(self,request):
		pass
	def post(self,request):
		print(request.data)
		profilePic = request.POST['profilePic']
		# _format, imgstr = profilePic.split(';base64,')
		# ext = format.split('/')[-1]
		profilePic= ContentFile(base64.b64decode(profilePic), name=request.POST['userId']+'.' + "jpg")
		# serializer = ClientProfileFormSerializer(data=request.data)
		# if serializer.is_valid():
		user=User.objects.get(id=int(request.POST['userId']))
		user.is_active=True
		user.save()
		ProfileData = ClientProfileForm.objects.get(userId=user)
		ProfileData.city = request.POST['city']
		ProfileData.area = request.POST['area']
		ProfileData.pincode = request.POST['pincode']
		ProfileData.gender = request.POST['gender']
		ProfileData.height = request.POST['height']
		ProfileData.weight = request.POST['weight']
		ProfileData.dob = request.POST['dob']
		ProfileData.profilePic = profilePic
		print(ProfileData)
		ProfileData.save()
		ProfileData = ClientProfileForm.objects.get(userId=user)
		ProfileMasterData = ProfileMaster.objects.filter(userId=user,userType="client",clientData=ProfileData)
		if(ProfileMasterData):
			pass
		else:
			ProfileMasterData = ProfileMaster(userId=user,userType="client",clientData=ProfileData)
			ProfileMasterData.save()
		response={'status':'success'}
		return HttpResponse("Registered Successfully")
		# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class FetchBannerAndroid(APIView):
	def post(self,request):
		images = bannerAndroid.objects.all()
		pic_urls=[]
		for k in images:
			pic_urls.append("http://10.0.2.2:8000"+k.pic.url)
		return Response(pic_urls, status=status.HTTP_201_CREATED)
class GymListAndroid(APIView):
	def post(self,request):
		gymList=GymProfileForm.objects.all()
		data=[]
		for k in gymList:
			if(k.about):
				discount = ((int(k.monthlyOriginal) - k.monthlyPrice) / int(k.monthlyOriginal))*100
				discount = round(discount,2)
				pic = GymPictureForm.objects.filter(gymProfileId=k.id).order_by('-id')[:1]
				for x in pic:
					url = "http://10.0.2.2:8000"+x.pic.url
				temp={
				'gymName' : k.userId.first_name,
				'gymCity' : k.city,
				'gymPrice' : k.monthlyPrice,
				'gymOriginalPrice' : k.monthlyOriginal,
				'discount' : str(discount),
				'gymImage' : url,
				'gymId' : k.id,
				'gymDescription' : k.about[:50]
				}
				data.append(temp)
		print(data)
		return Response(data,status=status.HTTP_201_CREATED)
class GymListAndroidLowToHign(APIView):
	def post(self,request):
		gymList=GymProfileForm.objects.all().order_by('monthlyPrice')
		data=[]
		for k in gymList:
			if(k.about):
				discount = ((int(k.monthlyOriginal) - k.monthlyPrice) / int(k.monthlyOriginal))*100
				discount = round(discount,2)
				pic = GymPictureForm.objects.filter(gymProfileId=k.id).order_by('-id')[:1]
				for x in pic:
					url = "http://10.0.2.2:8000"+x.pic.url
				temp={
				'gymName' : k.userId.first_name,
				'gymCity' : k.city,
				'gymPrice' : k.monthlyPrice,
				'gymOriginalPrice' : k.monthlyOriginal,
				'discount' : str(discount),
				'gymImage' : url,
				'gymId' : k.id,
				'gymDescription' : k.about[:50]
				}
				data.append(temp)
		return Response(data,status=status.HTTP_201_CREATED)
class GymListAndroidDiscount(APIView):
	def post(self,request):
		gymList=GymProfileForm.objects.extra(select={'discount': 'monthlyOriginal - monthlyPrice'}).order_by('discount')
		data=[]
		for k in gymList:
			if(k.about):
				discount = ((int(k.monthlyOriginal) - k.monthlyPrice) / int(k.monthlyOriginal))*100
				discount = round(discount,2)
				pic = GymPictureForm.objects.filter(gymProfileId=k.id).order_by('-id')[:1]
				for x in pic:
					url = "http://10.0.2.2:8000"+x.pic.url
				temp={
				'gymName' : k.userId.first_name,
				'gymCity' : k.city,
				'gymPrice' : k.monthlyPrice,
				'gymOriginalPrice' : k.monthlyOriginal,
				'discount' : str(discount),
				'gymImage' : url,
				'gymId' : k.id,
				'gymDescription' : k.about[:50]
				}
				data.append(temp)
		return Response(data,status=status.HTTP_201_CREATED)
class OurServicesList(APIView):
	def post(self,request):
		serviceList = OurServicesImagesAndroid.objects.all()
		data=[]
		for k in serviceList:
			url = "http://10.0.2.2:8000"+k.pic.url
			temp={
			'serviceName' : k.serviceName,
			'serviceImage' : url
			}
			data.append(temp)
		print(data)
		return Response(data,status=status.HTTP_201_CREATED)
class SingleGymImageFetch(APIView):
	def post(self,request):
		gymId=request.POST['gymId']
		images = GymPictureForm.objects.filter(gymProfileId=gymId)
		pic_urls=[]
		for k in images:
			pic_urls.append("http://10.0.2.2:8000"+k.pic.url)
		return Response(pic_urls, status=status.HTTP_201_CREATED)
class SingleGymData(APIView):
	def post(self,request):
		gymId = request.POST['gymId']
		data = GymProfileForm.objects.get(id=gymId)
		features = []
		if data.featuresId.ac is True:
			features.append("AC")
		if data.featuresId.changingRoom is True:
			features.append("Changing Room")
		if data.featuresId.personalTrainer is True:
			features.append("Personal Trainer")
		if data.featuresId.sauna is True:
			features.append("Sauna")
		if data.featuresId.locker is True:
			features.append("Locker")
		if data.featuresId.zumba is True:
			features.append("Zumba")
		featuresResult=""
		for x in features:
			featuresResult=featuresResult+", "+x
		GymData=[]
		temp = {
		'gymName' : data.userId.first_name,
		'gymAddress' : data.houseNo + ", " + data.city,
		'gymTiming' : data.openingTime + "-" + data.closingTime,
		'closedOn' : data.closedOn,
		'genders' : data.featuresId.genders,
		'facilities' : featuresResult[1:],
		'about' : data.about,
		'monthlyOriginal' : data.monthlyOriginal,
		'monthlyPrice' : data.monthlyPrice,
		'monthlyAbout' : data.monthlyAbout,
		'halfyearlyOriginal' : data.halfyearlyOriginal,
		'halfyearlyPrice' : data.halfyearlyPrice,
		'halfyearlyAbout' : data.halfyearlyAbout,
		'quarterlyOriginal' : data.quarterlyOriginal,
		'quarterlyPrice' : data.quarterlyPrice,
		'quarterlyAbout' : data.quarterlyAbout,
		'yearlyOriginal' : data.yearlyOriginal,
		'yearlyPrice' : data.yearlyPrice,
		'yearlyAbout' : data.yearlyAbout
		}
		GymData.append(temp)
		print(GymData)
		return Response(GymData,status=status.HTTP_201_CREATED)
class FetchTimelineAndroid(APIView):
	def post(self,request):
		TimelineData = timeline.objects.filter(status=True).order_by('-id')
		print(request.POST['username'])
		user = User.objects.get(username=request.POST['username'])
		Data=[]
		for k in TimelineData:
			total_likes = k.likes.count()
			image_url = "http://10.0.2.2:8000"+k.image.url
			if k.likes.filter(id=user.id).exists():
				temp = {
				'id' : k.id,
				'title' : k.title,
				'image_url':image_url,
				'total_likes' : total_likes,
				'liked':"True"}
			else:
				temp = {'id' : k.id,
				'title' : k.title,
				'image_url':image_url,
				'total_likes' : total_likes,
				'liked':"False"}
			Data.append(temp)
		print(Data)
		return Response(Data,status=status.HTTP_201_CREATED)
class TimelineClientPhotoFetchAndroid(APIView):
	def post(self,request):
		print(request.data)
		user=User.objects.get(username=request.POST['userId'])
		images = timeline.objects.filter(userId=user.id,status=True)
		pic_urls=[]
		if(images):
			for k in images:
				pic_urls.append("http://10.0.2.2:8000"+k.image.url)
			return Response(pic_urls, status=status.HTTP_201_CREATED)
		else:
			return Response("False")
class FetchProfileData(APIView):
	def post(self,request):
		user=User.objects.get(username=request.POST['userId'])
		clientName=user.first_name
		clientData = ClientProfileForm.objects.get(userId=user.id)
		subData = ClientSubscriptionForm.objects.filter(userId=user.id,status=True)
		if(subData):
			subData = ClientSubscriptionForm.objects.get(userId=user.id,status=True)
			gymName = subData.gymId.userId.first_name
		else:
			gymName = "No Subscription Yet."
		if(subData):
			subData = ClientSubscriptionForm.objects.get(userId=user,status=True)
			if(subData.plan == "monthly"):
				endingDate = subData.startDate + timedelta(days=30)
			elif(subData.plan == "quarterly"):
				endingDate = subData.startDate + timedelta(days=120)
			elif(subData.plan == "yearly"):
				endingDate = subData.startDate + timedelta(days=365)
			else:
				endingDate = subData.startDate + timedelta(days=180)
			endingDate = "You have subsciption in gym which is ending on "+str(endingDate)+". Please renew the subscription before expiry date. Use our tranfer subscription service for switching gyms without worrying about payments."
		else:
			subData = None
			endingDate="Please Subscribe to get access to our 24x7 services."
		bmi=float(clientData.weight)/((float(clientData.height)/100)*(float(clientData.height)/100))
		bmi = round(bmi,2)
		if bmi < 18.5:
			bmiStatus="underweight"
		elif bmi >= 18.5 and bmi <= 24.9:
			bmiStatus = "normalWeight"
		elif bmi > 24.9 and bmi <= 29.9:
			bmiStatus="overweight"
		else:
			bmiStatus="obese"
		data=[]
		temp={
		'clientName':clientName,
		'bmi' : bmi,
		'bmiStatus' : bmiStatus,
		'gymName' : gymName,
		'endingDate' : endingDate
		}
		data.append(temp)
		return Response(data)
class FetchSubData(APIView):
	def post(self,request):
		userData = User.objects.get(username=request.POST['userId'])
		subData = ClientSubscriptionForm.objects.filter(userId=userData.id,status=True)
		if subData:
			data=[]
			temp={'msg':'False'}
			data.append(temp)
			print("here")
			return Response(data)
		else:
			data=[]
			gymData = GymProfileForm.objects.get(id=request.POST['gymId'])
			temp={
			'msg' : 'True',
			'email' : userData.email,
			'username' : userData.username,
			'gymName' : gymData.userId.first_name,
			}
			data.append(temp)
			return Response(data)
#Client Subscription and Payment
class PaytmStartAndroid(APIView):
	def post(self,request):
		user=User.objects.get(username=request.POST['userId'])
		gym=GymProfileForm.objects.get(id=request.POST['gymId'])
		subData = ClientSubscriptionForm(userId=user,gymId=gym,startDate=request.POST['startDate'],plan=request.POST['plan'].lower())
		subData.save()
		if(subData.plan == "monthly"):
			amount = subData.gymId.monthlyPrice
		elif(subData.plan == "quarterly"):
			amount = subData.gymId.quarterlyPrice
		elif(subData.plan == "yearly"):
			amount = subData.gymId.yearlyPrice
		else:
			amount = subData.gymId.halfyearlyPrice
		paytmParams = dict()
		paytmParams["body"] = {
		    "requestType"   : "Payment",
		    "mid"           : "UiAFna89875961510395",
		    "websiteName"   : "WEBSTAGING",
		    "orderId"       :  str(subData.id)+"-"+str( date.today()),
		    "callbackUrl"   : "http://10.0.2.2:8000/AndroidSuccess",
		    "txnAmount"     : {
		        "value"     : str(amount)+".00",
		        "currency"  : "INR",
		    },
		    "userInfo"      : {
		        "custId"    : str(subData.userId.id),
		    },
		}
		checksum = generateSignature(json.dumps(paytmParams["body"]), "MPwxfi7vMCXV98FC")
		paytmParams["head"] = {
		    "signature"    : checksum
		}
		post_data = json.dumps(paytmParams)
		url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=UiAFna89875961510395&orderId="+str(subData.id)+"-"+str( date.today())
		response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
		response['clientData'] ={
		'orderId': str(subData.id)+"-"+str( date.today()),
		'amount' : str(amount)+".00"
		}
		print(response)
		return Response(response)
def AndroidSuccess(request):
	received_data = request.POST
	paytmChecksum = ""
	paytmParams = {}
	for key, value in received_data.items(): 
		if key == 'CHECKSUMHASH':
			paytmChecksum = value
		else:
			paytmParams[key] = value
	isValidChecksum = verify_checksum(paytmParams, "MPwxfi7vMCXV98FC", paytmChecksum)
	orderId = paytmParams['ORDERID'].split('-')
	print(orderId[0])
	SubData = ClientSubscriptionForm.objects.get(id=int(orderId[0]))
	Payment = PaymentForm(userId=SubData.userId,gymId=SubData.gymId,currency=received_data['CURRENCY'],gatewayName=received_data['GATEWAYNAME'],responseMsg=received_data['RESPMSG'],bankName=received_data['BANKNAME'],paymentMode=received_data['PAYMENTMODE'],mid=received_data['MID'],responseCode=received_data['RESPCODE'],txnId=received_data['TXNID'],txnAmount=received_data['TXNAMOUNT'],status=received_data['STATUS'],bankTxnId=received_data['BANKTXNID'],txnDate=received_data['TXNDATE'],checksumHash=received_data['CHECKSUMHASH'])
	Payment.save()
	if isValidChecksum:
		if(received_data['RESPCODE']=='01'):
			SubData.paymentId = Payment
			SubData.status = True
			SubData.save()
			return render(request,'success.html',{'msg':'Payment Success'})
		else:
			return render(request,'error.html',{'msg':'Payment Failed'})
		print("Checksum Mismatched")
		return render(request,'error.html',{'msg':'Payment Failed'})
class UploadtoTimelineAndroid(APIView):
	def post(self,request):
		username=request.POST['userId']
		user = User.objects.get(username=username)
		print(request.data)
		timeline_image = request.POST['timeline_image']
		timeline_image= ContentFile(base64.b64decode(timeline_image), name=request.POST['userId']+'.' + "jpg")
		timelineData = timeline(userId=user,image=timeline_image,title=request.POST['caption'])
		# timelineData.likes.add(user.id)
		timelineData.save()
		return Response({'msg':'success'})
class TimelineLikeImageAndroid(APIView):
	def post(self,request):
		username=request.POST['username']
		user = User.objects.get(username=username)
		imageId = request.POST['photoid']
		post = timeline.objects.get(id=imageId)
		post.likes.add(user)
		data = {
		'likes' : post.likes.count()
		}
		print("like")
		print(data)
		return Response(data)
class TimelineUnLikeImageAndroid(APIView):
	def post(self,request):
		username=request.POST['username']
		user = User.objects.get(username=username)
		imageId = request.POST['photoid']
		post = timeline.objects.get(id=imageId)
		post.likes.remove(user)
		data = {
		'likes' : post.likes.count()
		}
		print("like")
		print(data)
		return Response(data)