from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_student(self, email, password, **extra_fields):
        #extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)

        if extra_fields.get("is_staff") is True:
            raise ValueError(_("is_staff must have is_staff=False."))
        if extra_fields.get("is_superuser") is not False:
            raise ValueError(_("Superuser must have is_superuser=False."))
        return self.create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", False)

        if extra_fields.get("is_staff") is True:
            raise ValueError(_("is_staff must have is_staff=False."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)