from rest_framework import permissions


class EventsPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'VO':
                if request.method in permissions.SAFE_METHODS:
                    return True
            if request.user.role == 'OR' or request.user.is_staff:
                return True
            else:
                return False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user is obj.organizer or request.user.is_staff:
                return True
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return False
        else:
            return False


class VotePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.role == 'VO' or request.user.is_staff:
                return True
            else:
                return False
        else:
            return False