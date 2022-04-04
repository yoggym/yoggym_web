"""yoggym URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from home import views as mv
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('phone',mv.phoneOtp,name="phone"),
    path('',mv.index,name="index"),
    path('team',mv.team,name="team"),
    path('about',mv.about,name="about"),
    path('signupClient',mv.SignupClient.as_view(),name="signupClient"),
    path('validateForm/<inputData>',mv.validateForm,name="validateForm"),
    path('ForgotPassword',mv.ForgotPassword.as_view(),name="ForgotPassword"),
    path('otpVerification',mv.otpVerification,name="otpVerification"),
    path('logout',mv.logout,name="logout"),
    path('signin',mv.LoginFormApi.as_view(),name="signin"),
    path('ClientProfile',mv.ClientProfileApi.as_view(),name="ClientProfile"),
    path('EditClientProfile',mv.EditClientProfileApi.as_view(),name="EditClientProfile"),
    path('dashboard',mv.dashboardSwitch,name="dashboard"),
    path('UserDashboard',mv.ClientDashboard,name="UserDashboard"),
    path('GymsDashboard',mv.GymsDashboard,name="GymsDashboard"),
    path('gymCatalog',mv.gymCatalog.as_view(),name="gymCatalog"),
    path('BookOrder',mv.BookOrder.as_view(),name="BookOrder"),
    path('payment/<orderId>',mv.paytmStart,name='payment'),
    path('success',mv.success,name="success"),
    path('TransferSubsciption',mv.TransferSubsciption.as_view(),name="TransferSubsciption"),
    path('DietChart',mv.ClientDietChart,name="DietChart"),
    path('WorkoutChart',mv.ClientWorkoutChart,name="WorkoutChart"),
    path('Timeline',mv.ClientTimeline.as_view(),name="Timeline"),
    path('timeline',mv.viewTimeline,name="timeline"),
    path('applyForm',mv.applyForm.as_view(),name="applyForm"),
    path('services',mv.services,name="services"),
    path('gymZumbaDetails/<gymId>',mv.gymZumbaDetails.as_view(),name="gymZumbaDetails"),
    #Gym URLs
    path('signupGym',mv.SignupGym.as_view(),name="signupGym"),
    path('GymProfile',mv.GymProfileApi.as_view(),name="GymProfile"),
    path('GymDashboard/<gymId>',mv.GymDashboard,name="GymDashboard"),
    #Editor URLs
    path('editorHome',mv.editorHome,name="editorHome"),
    path('gymRequests',mv.GymRequestApi.as_view(),name="gymRequests"),
    path('gymAddDetailsForm/<gymId>',mv.gymAddDetailsForm.as_view(),name="gymAddDetailsForm"),
    path('gymAddDetailsForm',mv.gymAddDetailsForm.as_view(),name="gymAddDetailsForm"),
    path('ViewTransferRequests',mv.ViewTransferRequests.as_view(),name="ViewTransferRequests"),
    path('transferReqDecline/<reqId>',mv.transferReqDecline,name="transferReqDecline"),
    path('transferReqApprove/<reqId>',mv.transferReqApprove,name="transferReqApprove"),
    path('clientList',mv.clientList,name="clientList"),
    path('addDietChart',mv.addDietChart.as_view(),name="addDietChart"),
    path('ApproveTimeline',mv.ApproveTimeline.as_view(),name="ApproveTimeline"),
    path('timelineApprove/<imageId>',mv.timelineApprove,name="timelineApprove"),
    path('timelineDecline/<imageId>',mv.timelineDecline,name="timelineDecline"),
    path('clientWList',mv.clientWorkoutList,name="clientWList"),
    path('addWorkoutChart',mv.addWorkoutChart.as_view(),name="addWorkoutChart"),
    path('ViewDeleteClients',mv.ViewDeleteClients.as_view(),name="ViewDeleteClients"),
    path('ViewDeleteGyms',mv.ViewDeleteGyms.as_view(),name="ViewDeleteGyms"),
    path('viewApps',mv.viewApps,name="viewApps"),
    path('EditGymRequest',mv.EditGymRequest,name='EditGymRequest'),
    path('EditGym/<gymId>',mv.EditGym.as_view(),name="EditGym"),
    path('EditGym',mv.EditGym.as_view(),name='EditGym'),
    path('EditGymImages/<gymId>',mv.EditGymImages,name='EditGymImages'),
    path('deleteGymImage/<imageId>',mv.deleteGymImage,name='deleteGymImage'),
    path('addGymImages',mv.addGymImages,name='addGymImages'),
    #Admin URLs
    path('adminHome',mv.adminHome,name="adminHome"),
    path('UploadAndroidBanner',mv.UploadAndroidBanner.as_view(),name="UploadAndroidBanner"),
    path('AddEditor',mv.AddEditor.as_view(),name="AddEditor"),
    path('ajaxlike',mv.ajaxlike,name="ajaxlike"),
    path('like/<postId>',mv.like.as_view(),name="like"),
    path('unlike/<postId>',mv.unlike.as_view(),name="unlike"),
    path('deleteEditor/<userId>',mv.deleteEditor,name="deleteEditor"),
    path('viewPayment',mv.viewPayment,name="viewPayment"),
    #Android APi'
    path('LoginFormApiAndroid',csrf_exempt(mv.LoginFormApiAndroid.as_view()),name="LoginFormApiAndroid"),
    path('SignupClientAndroid',csrf_exempt(mv.SignupClientAndroid.as_view()),name="SignupClientAndroid"),
    path('ClientProfileApiAndroid',csrf_exempt(mv.ClientProfileApiAndroid.as_view()),name="ClientProfileApiAndroid"),
    path('FetchBannerAndroid',csrf_exempt(mv.FetchBannerAndroid.as_view()),name="FetchBannerAndroid"),
    path('GymListAndroid',csrf_exempt(mv.GymListAndroid.as_view()),name="GymListAndroid"),
    path('OurServicesList',csrf_exempt(mv.OurServicesList.as_view()),name="OurServicesList"),
    path('SingleGymImageFetch',csrf_exempt(mv.SingleGymImageFetch.as_view()),name="SingleGymImageFetch"),
    path('SingleGymData',csrf_exempt(mv.SingleGymData.as_view()),name="SingleGymData"),
    path('FetchTimelineAndroid',csrf_exempt(mv.FetchTimelineAndroid.as_view()),name="FetchTimelineAndroid"),
    path('TimelineClientPhotoFetchAndroid',csrf_exempt(mv.TimelineClientPhotoFetchAndroid.as_view()),name="TimelineClientPhotoFetchAndroid"),
   path('FetchProfileData',csrf_exempt(mv.FetchProfileData.as_view()),name="FetchProfileData"),
   path('FetchSubData',csrf_exempt(mv.FetchSubData.as_view()),name="FetchSubData"),
   path('PaytmStartAndroid',csrf_exempt(mv.PaytmStartAndroid.as_view()),name="PaytmStartAndroid"),
   path('AndroidSuccess',csrf_exempt(mv.AndroidSuccess),name="AndroidSuccess"),
   path('UploadtoTimelineAndroid',csrf_exempt(mv.UploadtoTimelineAndroid.as_view()),name="UploadtoTimelineAndroid"),
   path('TimelineLikeImageAndroid',csrf_exempt(mv.TimelineLikeImageAndroid.as_view()),name="TimelineLikeImageAndroid"),
    path('TimelineUnLikeImageAndroid',csrf_exempt(mv.TimelineUnLikeImageAndroid.as_view()),name="TimelineUnLikeImageAndroid"),
    path('GymListAndroidLowToHign',csrf_exempt(mv.GymListAndroidLowToHign.as_view()),name="GymListAndroidLowToHign"),
    path('GymListAndroidDiscount',csrf_exempt(mv.GymListAndroidDiscount.as_view()),name="GymListAndroidDiscount"),

   ]
if(settings.DEBUG):
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)