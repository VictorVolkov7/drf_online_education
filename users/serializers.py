from rest_framework import serializers

from materials.srializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(source='payments_set', many=True)

    class Meta:
        model = User
        fields = '__all__'
