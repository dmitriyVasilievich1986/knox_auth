from rest_framework import serializers
from django.contrib.auth.models import User


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if user is None:
            return value
        raise serializers.ValidationError("this email already exists")

    def create(self, validated_data, *args, **kwargs):
        user = User(
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            username=validated_data.get("username"),
            email=validated_data.get("email", ""),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user
