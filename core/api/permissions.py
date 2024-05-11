from rest_framework.permissions import BasePermission, IsAdminUser


class IsSuperUser(IsAdminUser):
    allowed_groups = ["SuperUser"]
    message = f"Only users belonging to groups: {allowed_groups} are allowed here"

    def has_permission(self, request, view):
        return (
            True
            if "SuperUser" in [group.name for group in request.user.groups.all()]
            or bool(request.user and request.user.is_superuser)
            else False
        )


class IsICTModerator(BasePermission):
    allowed_groups = ["ICTModerators", "SuperUser"]
    message = f"Only users belonging to groups: {allowed_groups} are allowed here"

    def has_permission(self, request, view):
        # return True if 'ICTModerators' in [group.name for group in request.user.groups.all()] else False
        check = any(
            i in self.allowed_groups
            for i in [group.name for group in request.user.groups.all()]
        )
        return check


class IsRegionalManager(BasePermission):
    allowed_groups = ["RegionalManagers", "ICTModerators", "SuperUser"]
    message = f"Only users belonging to groups: {allowed_groups} are allowed here"

    def has_permission(self, request, view):
        check = any(
            i in self.allowed_groups
            for i in [group.name for group in request.user.groups.all()]
        )
        return check


class IsCSPSupervisor(BasePermission):
    allowed_groups = [
        "CspSupervisors",
        "RegionalManagers",
        "ICTModerators",
        "SuperUser",
    ]
    message = f"Only users belonging to groups: {allowed_groups} are allowed here"

    def has_permission(self, request, view):
        check = any(
            i in self.allowed_groups
            for i in [group.name for group in request.user.groups.all()]
        )
        return check


class HasActiveStaffProfileAPI(BasePermission):
    
    message = f"Only users with active Staff Profile are allowed here"

    def has_permission(self, request, view):        
        try:
            profile = request.user.profile
            check = bool(profile and profile.active)
        except Exception as exp:
            print(exp)
            check =  False
        finally:
            return check

class HasActiveCustomerProfileAPI(BasePermission):
    
    message = f"Only users with Active Customer Profile are allowed here"

    def has_permission(self, request, view):        
        try:
            profile = request.user.customer
            check = bool(profile and profile.active)
        except Exception as exp:
            print(exp)
            check =  False
        finally:
            return check

class HasActiveVendorProfileAPI(BasePermission):
    
    message = f"Only users with active Vendor Profile are allowed here"

    def has_permission(self, request, view):        
        try:
            profile = request.user.vendor
            check = bool(profile and profile.active)
        except Exception as exp:
            print(exp)
            check =  False
        finally:
            return check

class HasActiveContractorProfileAPI(BasePermission):
    
    message = f"Only users with active Contractor Profile are allowed here"

    def has_permission(self, request, view):        
        try:
            profile = request.user.contractor
            check = bool(profile and profile.active)
        except Exception as exp:
            check =  False
        finally:
            return check
