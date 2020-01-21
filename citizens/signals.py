from .models import *
from django.db.models.signals import post_save
from django.dispatch import reciever

# Connect to GOOGLE API

# Create a contact
@reciever(post_save, sender=Citizen, content="Welcome New Users")
def create_contact_reciever(sender,instance, created,**kwargs):
    if created:
        Messages.objects.create(user=instance, content=kwargs['content'],issue="CO")

@reciever(post_save, sender=Citizen)
def save_message(sender, instance, **kwargs):
    instance.messages.save()

# Updating a contact
def update_contact_reciever(sender, **kwargs):
    pass

# Create a group
@reciever(post_save, sender=Group, weak=False, dispatch_uuid=None)
def create_group_reciever(sender,instance, created,**kwargs):
    if created:
        print("Successfully added a user")

# Updating a group
def update_group_reciever(sender,**kwargs):
    pass
