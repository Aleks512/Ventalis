from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import viewsets, permissions, status, generics

class IsAuthenticatedAndConsultant(permissions.BasePermission):
    def has_permission(self, request, view):
        """Vérifie si l'utilisateur est authentifié et est un consultant"""
        return request.user.is_authenticated and request.user.is_employee

class IsAuthenticatedAndCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et est un client
        return request.user.is_authenticated and hasattr(request.user, 'customer')