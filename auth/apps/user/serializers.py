from djoser.serializers import UserCreateSerializer


from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'id',
            'stripe_customer_id',
            'stripe_account_id',
            'stripe_payment_id',
            'email',
            'username',
            'slug',
            'first_name',
            'last_name',
            'agreed',
            'is_active',
            'is_staff',
            'become_seller',
            'role',
            'verified',
        ]

class UserListSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'id',
            'stripe_customer_id',
            'stripe_account_id',
            'stripe_payment_id',
            'email',
            'username',
            'verified',
        ]