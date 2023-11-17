from rest_framework import serializers

from materials.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(source='payments_set', many=True)

    class Meta:
        model = User
        fields = '__all__'


class LimitedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'last_name',)
