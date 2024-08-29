import json
import os

from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete, post_delete
from root import settings
from root.settings import BASE_DIR
from texnomart.models import Category, Product
from django.dispatch import receiver
from django.core.cache import cache
from .models import Comment


def send_notification_email(subject, body):
    sender_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [settings.TEACHER_EMAIL]

    try:
        send_mail(subject, body, sender_email, recipient_list)
        print(f'Notification email sent to {settings.TEACHER_EMAIL}')
    except Exception as error:
        print(error)
        raise Exception(f'Failed to send email notification: {str(error)}')


def save_deletion_backup(instance, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(BASE_DIR / directory, filename)

    data = {
        'id': instance.id,
        'title': getattr(instance, 'title', None),
        'name': getattr(instance, 'name', None),
        'slug': getattr(instance, 'slug', None),
        'price': getattr(instance, 'price', None),
    }

    with open(file_path, mode='a') as file_json:
        json.dump(data, file_json, indent=4)

    print(f'{instance.__class__.__name__} "{instance}" has been deleted and archived.')


@receiver(post_save, sender=Category)
def notify_teacher_on_category_change(sender, instance, created, **kwargs):
    email_subject = f'Notification: Category {"Created" if created else "Updated"} by Akbarshoh'
    email_body = f'The category "{instance.title}" has been {"successfully added" if created else "updated"}. We appreciate your attention!'

    send_notification_email(email_subject, email_body)


@receiver(pre_delete, sender=Category)
def course_delete(sender, instance, **kwargs):
    directory = 'category/signal_deleted/'
    filename = f'category_{instance.title}.json'

    save_deletion_backup(instance, directory, filename)


@receiver(post_save, sender=Product)
def notify_teacher_on_product_change(sender, instance, created, **kwargs):
    email_subject = f'Notification: Product {"Created" if created else "Updated"} by Akbarshoh'
    email_body = f'The product "{instance.name}" has been {"successfully added" if created else "modified"}. Thank you for your attention!'

    send_notification_email(email_subject, email_body)


@receiver(pre_delete, sender=Product)
def handle_product_deletion(sender, instance, **kwargs):
    backup_directory = 'archived_products/deleted/'
    filename = f'deleted_product_{instance.name}.json'

    save_deletion_backup(instance, backup_directory, filename)


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    cache.delete(f'product_{instance.id}_discounted_price')
    cache.delete(f'product_{instance.id}_average_rating')

@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def clear_comment_cache(sender, instance, **kwargs):
    cache.delete(f'product_{instance.product.id}_average_rating')