from rest_framework import serializers
from .models import Citizen, Messages, Group

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'


class CitizenSerializers(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, required=False)
    class Meta:
        model = Citizen
        fields = ["id_number","surname","first_name","last_name","location","email","gender","phone_number","dob","is_active","is_admin","messages"]

class GroupSerializer(serializers.ModelSerializer):
    members = CitizenSerializers(many=True, required=False)
    class Meta:
        model = Group
        fields = ['name', 'members']