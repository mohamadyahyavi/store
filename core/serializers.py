
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from store.models import Customer

class UserCreateSerializer(BaseUserCreateSerializer):


      class Meta(BaseUserCreateSerializer.Meta):
            
           fields=['id','username','password','email','first_name','last_name'] 