from django.db.utils import IntegrityError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from accounts.models import CustomerProfile, PasswordResetTokens, UserProfile, UserType, VendorProfile, ContractorProfile
from core.api.permissions import IsSuperUser
from .serializers import (
    UserProfileSerializer, UserProfileListSerializer,
    CustomerProfileDetailsSerializer, CustomerProfileListSerializer,
    VendorProfileDetailsSerializer, VendorProfileListSerializer,
    ContractorProfileDetailsSerializer, ContractorProfileListSerializer,
)


from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.core.validators import validate_email

User = get_user_model()


def check_username(username) -> bool:
    # check = False
    forbidden_chars = ["`", "?", "/", "!", "~", "&", "^", "%", "$", "#", "(", ")", "{", "}", "[", "]", "\\", "|", "<", ">", "+" ]
    check = bool (len(username)<5 or any(map(username.__contains__, forbidden_chars)) )
    return check


class StaffLoginObtainAuthToken(ObtainAuthToken):
    """API View to allow login and return Token and Profile Data for Staff

    Args:
        ObtainAuthToken
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        try:
            if not user.is_active:
                return JsonResponse({"detail": "User is not active"})
            elif user.is_active and token:
                profile = user.profile
                if not profile.active:
                    return JsonResponse({"detail": "User is not active"})
                profile_serializer = UserProfileSerializer(
                    profile, context={'request': request}
                )
                data = {
                    "token": token.key,
                    "profile": profile_serializer.data,
                }
                status_code = status.HTTP_200_OK
            else:
                data = {"detail": "Invalid User!!!"}
                status_code = status.HTTP_403_FORBIDDEN
        except Exception as exp:
            data = {"detail": f"Client Error: {exp}", "code": 400}
            status_code = status.HTTP_400_BAD_REQUEST
        finally:
            return Response(data=data, status=status_code)


class CustomerLoginObtainAuthToken(ObtainAuthToken):
    """API View to allow login and return Token and Profile Data for Customer

    Args:
        ObtainAuthToken
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        try:
            if not user.is_active:
                return JsonResponse({"detail": "User is not active"})
            elif user.is_active and token:
                profile = user.customer
                if not profile.active:
                    return JsonResponse({"detail": "User is not active"})
                profile_serializer = CustomerProfileDetailsSerializer(
                    profile, context={'request': request}
                )
                data = {
                    "token": token.key,
                    "profile": profile_serializer.data,
                }
                status_code = status.HTTP_200_OK
            else:
                data = {"detail": "Invalid User!!!"}
                status_code = status.HTTP_403_FORBIDDEN
        except Exception as exp:
            data = {"detail": f"Client Error: {exp}", "code": 400}
            status_code = status.HTTP_400_BAD_REQUEST
        finally:
            return Response(data=data, status=status_code)


class VendorLoginObtainAuthToken(ObtainAuthToken):
    """API View to allow login and return Token and Profile Data for Vendor
    Args:
        ObtainAuthToken
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        try:
            if not user.is_active:
                return JsonResponse({"detail": "User is not active"})
            elif user.is_active and token:
                profile = user.vendor
                if not profile.active:
                    return JsonResponse({"detail": "User is not active"})
                profile_serializer = VendorProfileDetailsSerializer(
                    profile, context={'request': request}
                )
                data = {
                    "token": token.key,
                    "profile": profile_serializer.data,
                }
                status_code = status.HTTP_200_OK
            else:
                data = {"detail": "Invalid User!!!"}
                status_code = status.HTTP_403_FORBIDDEN
        except Exception as exp:
            data = {"detail": f"Client Error: {exp}", "code": 400}
            status_code = status.HTTP_400_BAD_REQUEST
        finally:
            return Response(data=data, status=status_code)


class ContractorLoginObtainAuthToken(ObtainAuthToken):
    """API View to allow login and return Token and Profile Data for Contractor
    Args:
        ObtainAuthToken
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        try:
            if not user.is_active:
                return JsonResponse({"detail": "User is not active"})
            elif user.is_active and token:
                profile = user.contractor
                if not profile.active:
                    data = {"detail": "User is not active"}
                    status_code = status.HTTP_403_FORBIDDEN
                    return Response(data=data, status=status_code)
                profile_serializer = ContractorProfileDetailsSerializer(
                    profile, context={'request': request}
                )
                data = {
                    "token": token.key,
                    "profile": profile_serializer.data,
                }
                status_code = status.HTTP_200_OK
                return Response(data=data, status=status_code)
            else:
                data = {"detail": "Invalid User!!!"}
                status_code = status.HTTP_403_FORBIDDEN
                return Response(data=data, status=status_code)
        except Exception as exp:
            data = {
                "detail": "Client Error", 
                "error": f"{exp}",
                "code": 400
            }
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(data=data, status=status_code)
        # finally:
        #     return Response(data=data, status=status_code)


class ComboLoginObtainAuthToken(ObtainAuthToken):
    """API View to allow login and return Token and Profile Data for all Available Profiles
    Args:
        ObtainAuthToken
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        try:
            if not user.is_active:
                return JsonResponse({"detail": "User is not active"})
            elif user.is_active and token:
                try:
                    staff_profile = user.profile
                    staff_serializer = UserProfileSerializer(
                        staff_profile, context={'request': request}
                    )
                    staff_check = staff_profile.active
                except Exception as staff_exp:
                    staff_profile = None
                    staff_serializer = None
                    staff_check = False
                try:
                    customer_profile = user.customer
                    customer_serializer = CustomerProfileDetailsSerializer(
                        customer_profile, context={'request': request}
                    )
                    customer_check = customer_profile.active
                except Exception as customer_exp:
                    customer_profile = None
                    customer_serializer = None
                    customer_check = False
                try:
                    vendor_profile = user.vendor
                    vendor_serializer = VendorProfileDetailsSerializer(
                        vendor_profile, context={'request': request}
                    )
                    vendor_check = vendor_profile.active
                except Exception as vendor_exp:
                    vendor_profile = None
                    vendor_serializer = None
                    vendor_check = False
                try:
                    contractor_profile = user.contractor
                    contractor_serializer = ContractorProfileDetailsSerializer(
                        contractor_profile, context={'request': request}
                    )
                    contractor_check = contractor_profile.active
                except Exception as contractor_exp:
                    contractor_profile = None
                    contractor_serializer = None
                    contractor_check = False

                all_check = bool(
                    staff_check or
                    customer_check or
                    vendor_check or
                    contractor_check
                )
                if not bool(staff_profile.active and customer_profile.active and vendor_profile.active and contractor_profile.active):
                    return JsonResponse({"detail": "User is not active"})
                
                data = {
                    "detail": "At least on Profile Found Active" if all_check else "User is not active",
                    "token": token.key if all_check else None,
                    "staff_profile": staff_serializer.data if staff_check else None,
                    "customer_profile": customer_serializer.data if customer_check else None,
                    "vendor_profile": vendor_serializer.data if vendor_check else None,
                    "contractor_profile": contractor_serializer.data if contractor_check else None,
                }
                status_code = status.HTTP_200_OK
            else:
                data = {"detail": "Invalid User!!!"}
                status_code = status.HTTP_403_FORBIDDEN
        except Exception as exp:
            data = {
                "detail": "Client Error", 
                "error": f"{exp}",
                "code": 400
                }
            status_code = status.HTTP_400_BAD_REQUEST
        finally:
            return Response(data=data, status=status_code)



class CreateStaffAccountAPIView(APIView):
    """Allow Creation of a Staff User Account with Profile
    """
    def post(self, request, format=None):
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        # user_profile
        phone_number = request.POST.get("phone_number")
        staff_id = request.POST.get("staff_id")
        user_type = request.POST.get("user_type")
        region = request.POST.get("region")
        csp = request.POST.get("csp")
        error_list = []
        required_info = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "staff_id": staff_id,
            "user_type": user_type,
            "region": region,
            # "csp": csp,
        }
        for entry in required_info.keys():
            if not required_info.get(entry):
                error_list.append(f"Invalid Entry of: {entry}")
        if error_list:
            dta = {
                "detail": "Fail to Create user, Some Required fileds are missing.",
                "errors": error_list,
            }
            status_code = 406
            raise ValidationError(dta, status_code)
        # domain validate
        domain = email.split('@')[1]
        domain_list = ["kedco.ng", ]
        #if domain not in domain_list:
        if email and not email.endswith("kedco.ng"):
            status_code = 406
            raise ValidationError({"detail": "You must use your kedco email",}, status_code)
        else:
            try:
                # create user
                if username.count(' ') > 0 or len(username) > 30:
                    return Response(
                        data={
                            "detail": "Username Cannot contain space and must be lessthan 30 characters"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif check_username(username=username):
                    return Response(
                        data={
                            "detail": "Username Contains Forbidden characters"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    user = User.objects.create(username=username)
            except IntegrityError as exp:
                raise ValidationError(
                    {"detail": f"{username} Already Exist Error: {exp}"})

            #  check for duplicate email
            user_with_email = User.objects.filter(email=email)
            if user_with_email.count() > 0:
                user.delete()
                raise ValidationError(
                    {"detail": f"User with email: {email} Already Exist!"})
            #  check for duplicate staff_id
            user_with_staff_id = UserProfile.objects.filter(staff_id=staff_id)
            if user_with_staff_id.count() > 0:
                user.delete()
                raise ValidationError(
                    {"detail": f"User with Staff ID: {staff_id} Already Exist!"})
            # check len of staff id
            if len(staff_id) != 9:
                user.delete()
                raise ValidationError(
                    {"detail": f"Invalid Staff ID: {staff_id}. Staff ID must be 9 Digits"})

            user.set_password(password)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # valid designation and branch

            try:
                egg = {
                    "user": user,
                    "phone_number": phone_number,
                    # "email": email,
                    # "DOB": dob,
                    "staff_id": staff_id,
                    "region_id": region,
                    "csp_id": csp,
                }
                profile = UserProfile(**egg)
                profile.save()
            except Exception as exp:
                # Delete The Created User
                user.delete()
                msg = f"Error while creating profile for the user: {username}"
                raise ValidationError(
                    {"detail": f"Validation Error while creating profile: {exp}",
                        "message": msg}
                )
            else:
                token, created = Token.objects.get_or_create(user=user)
                profile = user.profile
                profile_serializer = UserProfileSerializer(
                    profile, context={'request': request})
                dta = {
                    "message": "User Created Successfully.",
                    "token": f"{token}",
                    "profile": profile_serializer.data,
                }
                status_code = 201
        return Response(dta, status=status_code)


class CreateCustomerAccountAPIView(APIView):
    """Allow Creation of a Customer User Account with Profile
    """

    def post(self, request, format=None):
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        # user_profile
        phone_number = request.POST.get("phone_number")
        region = request.POST.get("region")
        address = request.POST.get("address")
        error_list = []
        required_info = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            # "region": region,
            "address": address,
        }
        for entry in required_info.keys():
            if not required_info.get(entry):
                error_list.append(f"Invalid Entry of: {entry}")
        if error_list:
            dta = {
                "detail": "Fail to Create user, Some Required fileds are missing.",
                "errors": error_list,
            }
            status_code = 406
            raise ValidationError(dta, status_code)
        else:
            try:
                # create user
                if username.count(' ') > 0 or len(username) > 15:
                    return Response(
                        data={
                            "detail": "Username Cannot contain space and must be lessthan 15 characters"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif check_username(username=username):
                    return Response(
                        data={
                            "detail": "Username Contains Forbidden characters"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    user = User.objects.create(username=username)
            except IntegrityError as exp:
                raise ValidationError(
                    {"detail": f"{username} Already Exist Error: {exp}"})

            #  check for duplicate email
            if email:
                user_with_email = User.objects.filter(email=email)
                if user_with_email.exists():
                    user.delete()
                    raise ValidationError(
                        {"detail": f"User with email: {email} Already Exist!"})
                user.email = email
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # valid designation and branch

            try:
                egg = {
                    "user": user,
                    "phone_number": phone_number,
                    # "email": email,
                    # "region_id": region,
                    "address": address,
                }
                profile = CustomerProfile(**egg)
                profile.save()
            except Exception as exp:
                # Delete The Created User
                user.delete()
                msg = f"Error while creating Customer Profile for the user: {username}"
                raise ValidationError(
                    {"detail": f"Validation Error while creating Profile: {exp}",
                        "message": msg}
                )
            else:
                token, created = Token.objects.get_or_create(user=user)
                profile = user.customer
                profile_serializer = CustomerProfileDetailsSerializer(
                    profile, context={'request': request}
                )
                dta = {
                    "message": "User Created Successfully.",
                    "token": f"{token}",
                    "profile": profile_serializer.data,
                }
                status_code = 201
        return Response(dta, status=status_code)


class CreateVendorAccountAPIView(APIView):
    """Allow Creation of a Vendor User Account with Profile
    """

    def post(self, request, format=None):
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        # user_profile
        phone_number = request.POST.get("phone_number")
        vendor = request.POST.get("vendor")
        # address = request.POST.get("address")
        error_list = []
        required_info = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "vendor": vendor,
            # "address": address,
        }
        for entry in required_info.keys():
            if not required_info.get(entry):
                error_list.append(f"Invalid Entry of: {entry}")
        if error_list:
            dta = {
                "detail": "Fail to Create user, Some Required fileds are missing.",
                "errors": error_list,
            }
            status_code = 406
            raise ValidationError(dta, status_code)
        else:
            try:
                # create user
                if username.count(' ') > 0 or len(username) > 15:
                    return Response(
                        data={
                            "detail": "Username Cannot contain space and must be lessthan 15 characters"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif check_username(username=username):
                    return Response(
                        data={
                            "detail": "Username Contains Forbidden characters"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    user = User.objects.create(username=username)
            except IntegrityError as exp:
                raise ValidationError(
                    {"detail": f"{username} Already Exist Error: {exp}"})

            #  check for duplicate email
            if email:
                user_with_email = User.objects.filter(email=email)
                if user_with_email.exists():
                    user.delete()
                    raise ValidationError(
                        {"detail": f"User with email: {email} Already Exist!"})
                user.email = email
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            try:
                egg = {
                    "user": user,
                    "phone_number": phone_number,
                    # "email": email,
                    "vendor_id": vendor,
                    # "address": address,
                }
                profile = VendorProfile(**egg)
                profile.save()
            except Exception as exp:
                # Delete The Created User
                user.delete()
                msg = f"Error while creating Vendor Profile for the user: {username}"
                raise ValidationError(
                    {"detail": f"Validation Error while creating Profile: {exp}",
                        "message": msg}
                )
            else:
                token, created = Token.objects.get_or_create(user=user)
                profile = user.vendor
                profile_serializer = VendorProfileDetailsSerializer(
                    profile, context={'request': request}
                )
                dta = {
                    "message": "User Created Successfully.",
                    "token": f"{token}",
                    "profile": profile_serializer.data,
                }
                status_code = 201
        return Response(dta, status=status_code)


class CreateContractorProfileAccountAPIView(APIView):
    """Allow Creation of a Contractor User Account with Profile
    """

    def post(self, request, format=None):
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        # user_profile
        phone_number = request.POST.get("phone_number")
        company_name = request.POST.get("company_name")
        nemsa_licence = request.POST.get("nemsa_licence")
        licence_expire_date = request.POST.get("licence_expire_date")
        address = request.POST.get("address")
        error_list = []
        required_info = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "company_name": company_name,
            "nemsa_licence": nemsa_licence,
            "licence_expire_date": licence_expire_date,
            "address": address,
        }
        for entry in required_info.keys():
            if not required_info.get(entry):
                error_list.append(f"Invalid Entry of: {entry}")
        if error_list:
            dta = {
                "detail": "Fail to Create user, Some Required fileds are missing.",
                "errors": error_list,
            }
            status_code = 406
            return Response(
                data=dta,
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        else:
            try:
                # create user
                if username.count(' ') > 0 or len(username) > 15:
                    return Response(
                        data={"detail": "Username Cannot contain space and must be lessthan 15 characters"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif check_username(username=username):
                    return Response(
                        data={
                            "detail": "Username Contains Forbidden characters"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    user = User.objects.create(username=username)
            except IntegrityError as exp:
                raise ValidationError(
                    {
                        "detail": f"{username} Already Exist",
                        "error": f"{exp}"
                    }
                )

            #  check for duplicate email
            if email:
                user_with_email = User.objects.filter(email=email)
                if user_with_email.exists():
                    user.delete()
                    raise ValidationError(
                        {"detail": f"User with email: {email} Already Exist!"})
                user.email = email
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            try:
                egg = {
                    "user": user,
                    "phone_number": phone_number,
                    # "email": email,
                    "company_name": company_name,
                    "nemsa_licence": nemsa_licence,
                    "licence_expire_date":licence_expire_date,
                    "address": address,
                }
                profile = ContractorProfile(**egg)
                profile.save()
            except Exception as exp:
                # Delete The Created User
                user.delete()
                msg = f"Error while creating Contractor Profile for the user: {username}"
                raise ValidationError(
                    {
                        "detail": msg,
                        "erro": f"{exp}"
                    }
                )
            else:
                token, created = Token.objects.get_or_create(user=user)
                profile = user.contractor
                profile_serializer = ContractorProfileDetailsSerializer(
                    profile, context={'request': request}
                )
                dta = {
                    "message": "User Created Successfully.",
                    "token": f"{token}",
                    "profile": profile_serializer.data,
                }
                status_code = 201
        return Response(dta, status=status_code)


class ChangePassword(APIView):
    """Allow a User to reset their Login Password

    Args:
        username: auth_username(char)
        oldpassword: old password
        newpassword: new password

    Returns:
        [success]: [Password changed]
        [error]: [Description of error]
    """
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        username = request.POST.get("username")
        oldpassword = request.POST.get("oldpassword")
        newpassword = request.POST.get("newpassword")
        # print(oldpassword, newpassword)
        if (
            not username
            or not oldpassword
            or not newpassword
        ):
            response = {
                "detail": "Please Provide : username, oldpassword and newpassword", "code": 400}
        try:
            # authenticate the user
            user = authenticate(username=username, password=oldpassword)
            if user:
                user.set_password(newpassword)
                user.save()
                response = {"detail": "Password changed", "code": 200}
            else:
                response = {
                    "detail": "Cannot Authenticate User, perhaps Old Password is wrong?",
                    "code": 401,
                }
        except Exception as exp:
            response = {"detail": f"Client Error: {exp}", "code": 400}
        finally:
            return JsonResponse(response)



class ResetPassword(APIView):
    """Allow a User to reset their Login Password
    """
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        token = request.POST.get("token")
        new_password_1 = request.POST.get("new_password_1")
        new_password_2 = request.POST.get("new_password_2")
        reset = None
        if (
            not token
            or not new_password_1
            or not new_password_2
        ):
            dta = {
                "detail": "Please Provide : token, new_password_1 and new_password_2", "code": 400
            }
            raise ValidationError(dta)
        try:
            reset = PasswordResetTokens.objects.get(token=token, active=True)
            if reset and reset.active:
                user = reset.user
                user.set_password(new_password_1)
                user.save()
                dta = {"detail": "Password changed Successfully"}
                status_code = 200
                reset.active = False
                reset.save()
            else:
                dta = {
                    "detail": "Password cannot be changed. Expired Token!!!",
                }
                status_code = 400
        except PasswordResetTokens.DoesNotExist as exp:
            raise ValidationError(
                {
                    "details": "Invalid Token!!!"
                }
            )
        except Exception as exp:
            print("here")
            dta = {"detail": f"Client Error: {exp}"}
            status_code = 400
        finally:
            return Response(data=dta, status=status_code)

    def get(self, request, format="json"):
        username = request.GET.get("username")
        email = request.GET.get("email")
        if ( not username and not email):
            dta = {
                "detail": "Please Provide one of : username or email",
            }
            raise ValidationError(dta)
        dta_success = {"detail": "An OTP Code was sent to your registered Email"}
        dta_error = {"detail": "An Error Occured"}
        user = None
        status_code = 200
        
        try:
            user = User.objects.get(username=username)
            reset, created = PasswordResetTokens.objects.get_or_create(user=user,active=True)
            dta = dta_success
            # if not created:
            reset.email_user()
        except User.DoesNotExist as exp:
            print(exp)
            try:
                user = User.objects.get(email=email)
                reset, created = PasswordResetTokens.objects.get_or_create(
                    user=user, active=True
                )
                dta = dta_success
                # if not created:
                reset.email_user()
            except User.DoesNotExist as exp:
                print(exp)
                dta = {"detail": f"Client Error: {exp}"}
                status_code = 400
        except Exception as exp:
            dta = {"detail": f"Client Error: {exp}"}
            status_code = 400
        finally:
            if user and not user.email:
                print("No email")
                raise ValidationError(
                    {
                        "details": f"User: {user} has no email Address"
                    }
                )
            return Response(data=dta, status=status_code)





class StaffUserProfileListAPIView(generics.ListAPIView):
    """Return list of Users based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of User Profile]
    """
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            qs = UserProfile.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class StaffUserProfileDetailsAPIView(generics.RetrieveAPIView):
    """Return Details information of the User with the given PK

    Args:
        generics ([int]): [pk of the User]
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfile.objects.all()

class StaffUserProfileUpdateAPIView(generics.UpdateAPIView):
    """Update Profile information of the User with the given PK

    Args:
        generics ([int]): [pk of the User]
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserProfile.objects.all()


class StaffUserProfileSearchAPIView(generics.ListAPIView):
    """Return list of Users based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]
        staff_id: [the staff id of the user]
        username: [the username of the user]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of User Profile]
    """
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            search_query = self.request.GET.get("search_query")
            qs = UserProfile.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
            if search_query:
                qs = qs
            # if username:
            #     qs = qs.filter(user__username=username)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class StaffUserProfileDeleteAPIView(generics.DestroyAPIView):
    """Delete UserProfile by Deleting the Django Auth User

    Args:
        generics ([pk]): [int: pk of the intended userprofile]

    Returns:
        [dict]: [{"detail": "Delete Success"}]
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]
    queryset = UserProfile.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            title = f"{self.instance}"
            user = instance.user
            self.perform_destroy(instance)
            user.delete()
            dta = {"detail": f"Staff: {title} Delete Success"}
            return Response(dta, status=status.HTTP_200_OK)
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp



## Customer

class CustomerProfileListAPIView(generics.ListAPIView):
    """Return list of Users based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of User Profile]
    """
    serializer_class = CustomerProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            qs =  CustomerProfile.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class CustomerProfileSearchAPIView(generics.ListAPIView):
    """Return list of Users based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]
        staff_id: [the staff id of the user]
        username: [the username of the user]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of User Profile]
    """
    serializer_class = CustomerProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            search_query = self.request.GET.get("search_query")
            qs = CustomerProfile.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
            if search_query:
                qs = qs
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class CustomerProfileDetailsAPIView(generics.RetrieveAPIView):
    """Return Details information of the User with the given PK

    Args:
        generics ([int]): [pk of the User]
    """
    serializer_class = CustomerProfileDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomerProfile.objects.all()


class CustomerUserProfileUpdateAPIView(generics.UpdateAPIView):
    """Update Customer Profile information of the User with the given PK

    Args:
        generics ([int]): [pk of the User]
    """
    serializer_class = CustomerProfileDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomerProfile.objects.all()


class CustomerProfileDeleteAPIView(generics.DestroyAPIView):
    """Delete Customer Profile by Deleting the Django Auth User

    Args:
        generics ([pk]): [int: pk of the intended customerprofile]

    Returns:
        [dict]: [{"detail": "Delete Success"}]
    """
    serializer_class = CustomerProfileDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]
    queryset = CustomerProfile.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = instance.user
            self.perform_destroy(instance)
            user.delete()
            dta = {"detail": "Delete Success"}
            return Response(dta, status=status.HTTP_200_OK)
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp


## Vendor
class VendorProfileListAPIView(generics.ListAPIView):
    """Return list of Users based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of User Profile]
    """
    serializer_class = VendorProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            vendor = self.request.GET.get("vendor")
            qs = VendorProfile.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
            if vendor:
                qs = qs.filter(vendor=vendor)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class VendorProfileDetailsAPIView(generics.RetrieveAPIView):
    """Return Details information of the User with the given PK

    Args:
        generics ([int]): [pk of the User]
    """
    serializer_class = VendorProfileDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = VendorProfile.objects.all()


class VendorProfileUpdateAPIView(generics.UpdateAPIView):
    """Update Profile information of the User with the given PK

    Args:
        generics ([int]): [pk of the User]
    """
    serializer_class = VendorProfileDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = VendorProfile.objects.all()


class VendorProfileSearchAPIView(generics.ListAPIView):
    """Return list of Users based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]
        staff_id: [the staff id of the user]
        username: [the username of the user]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of User Profile]
    """
    serializer_class = VendorProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            search_query = self.request.GET.get("search_query")
            qs = VendorProfile.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
            if search_query:
                qs = qs
            # if username:
            #     qs = qs.filter(user__username=username)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class VendorProfileDeleteAPIView(generics.DestroyAPIView):
    """Delete VendorProfile by Deleting the Django Auth User

    Args:
        generics ([pk]): [int: pk of the intended profile]

    Returns:
        [dict]: [{"detail": "Delete Success"}]
    """
    serializer_class = VendorProfileDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]
    queryset = VendorProfile.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            title = f"{self.instance}"
            user = instance.user
            self.perform_destroy(instance)
            user.delete()
            dta = {"detail": f"Vendor Staff: {title} Delete Success"}
            return Response(dta, status=status.HTTP_200_OK)
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp


## ContractorProfile


class ContractorProfileListAPIView(generics.ListAPIView):
    """Return list of Users based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of User Profile]
    """
    serializer_class = ContractorProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            qs = ContractorProfile.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class ContractorProfileSearchAPIView(generics.ListAPIView):
    """Return list of Contractors based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]
        search_query: [the search value to lookup]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of Contractor Profile]
    """
    serializer_class = ContractorProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            search_query = self.request.GET.get("search_query")
            qs = ContractorProfile.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
            if search_query:
                phone_number_qs = qs.filter(phone_number__icontains=search_query)
                nemsa_licence_qs = qs.filter(
                    nemsa_licence__icontains=search_query)
                qs = phone_number_qs | nemsa_licence_qs
            else:
                qs = None
            # if username:
            #     qs = qs.filter(user__username=username)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class ContractorProfileDetailsAPIView(generics.RetrieveAPIView):
    """Return Details information of the User with the given PK

    Args:
        generics ([int]): [pk of the User]
    """
    serializer_class = ContractorProfileDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ContractorProfile.objects.all()


class ContractorProfileUpdateAPIView(generics.UpdateAPIView):
    """Update Profile information of the User with the given PK

    Args:
        generics ([int]): [pk of the User]
    """
    serializer_class = ContractorProfileDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ContractorProfile.objects.all()


class ContractorProfileDeleteAPIView(generics.DestroyAPIView):
    """Delete ContractorProfile by Deleting the Django Auth User

    Args:
        generics ([pk]): [int: pk of the intended profile]

    Returns:
        [dict]: [{"detail": "Delete Success"}]
    """
    serializer_class = ContractorProfileDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]
    queryset = ContractorProfile.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            title = f"{self.instance}"
            user = instance.user
            self.perform_destroy(instance)
            user.delete()
            dta = {"detail": f"ContractorProfile Staff: {title} Delete Success"}
            return Response(dta, status=status.HTTP_200_OK)
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp


# class NMMPKYCCreateAPIView(generics.CreateAPIView):
#     """
#        Allows creation of NMMPKYC
#     """

#     serializer_class = NMMPKYCDetailsSerializer
#     permission_classes = [
#         permissions.IsAuthenticated,
#         HasActiveStaffProfileAPI
#     ]

#     def create(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             dta = {
#                 "detail": "KYC Information Submitted Successfully",
#                 "data": serializer.data
#             }
#             return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
#         except Exception as exp:
#             raise ValidationError({"detail": f"Client Error: {exp}"})

#     def perform_create(self, serializer):
#         return serializer.save(kyc_by=self.request.user.profile)

##

class ProfileStatsDashboard(APIView):
    """
        Return All Profiles (Staff, Customer & Vendor) Stats
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        username = request.GET.get("username")
        today = timezone.localdate()
        try:
            all_staffs = UserProfile.objects.all()
            all_customers = CustomerProfile.objects.all()
            all_vendors = VendorProfile.objects.all()
            all_contractor = ContractorProfile.objects.all()
            dta = {
                "total_staffs": all_staffs.count(),
                "total_active_staffs": all_staffs.filter(active=True).count(),
                "total_staffs_today": all_staffs.filter(timestamp__date=today).count(),
                #
                "total_customers": all_customers.count(),
                "total_active_customers": all_customers.filter(active=True).count(),
                "total_customers_today": all_customers.filter(timestamp__date=today).count(),
                #
                "total_vendors": all_vendors.count(),
                "total_active_vendors": all_vendors.filter(active=True).count(),
                "total_vendors_today": all_vendors.filter(timestamp__date=today).count(),
                #
                "total_vendors": all_contractor.count(),
                "total_active_contractors": all_contractor.filter(active=True).count(),
                "total_contractors_today": all_contractor.filter(timestamp__date=today).count(),
                
            }
            status_code = 200
        except Exception as exp:
            status_code = 400
            dta = {"detail": f"Client Error: {exp}"}
        finally:
            return Response(data=dta, status=status_code)
