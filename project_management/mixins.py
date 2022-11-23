from django.contrib.auth.mixins import AccessMixin


class TeacherRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    @staticmethod
    def is_student(user) -> bool:
        print('is student')
        try:
            user = user.teacher
            return True
        except (Exception,) as e:
            return False

    def dispatch(self, request, *args, **kwargs):
        print('i am inside')
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.is_student(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class SuperUserMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    @staticmethod
    def superuser(user) -> bool:
        return user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        print('i am inside')
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.superuser(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
