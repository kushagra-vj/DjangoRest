from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # admin_permission = super().has_permission(request, view)
        # return admin_permission or self.request.method == 'GET'
        if request.method in permissions.SAFE_METHODS: # if request is GET request then allowing user to access the data
            return True
        else:
            # check is user is staff user or not
            return bool(request.user and request.user.is_staff)
    

class IsReviewUserOrReadOnly(permissions.BasePermission):
    # check if the user is allowed to update the review or not
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.review_user == request.user or request.user.is_staff