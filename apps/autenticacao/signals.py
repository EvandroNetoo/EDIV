from django.db.models.signals import post_save
from django.dispatch import receiver

from .active_account import ActiveAccount
from .models import User


@receiver(post_save, sender=User)
def active_account_mail(sender: User, instance: User, created: bool, **kwargs) -> None:
    if created and not instance.is_active:
        active_account = ActiveAccount(instance)
        active_account.active_account_send_email()