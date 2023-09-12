from .models import User, CartItem
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from menu.models import Menu
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8, write_only=True)
    id = serializers.UUIDField(read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access
        }
        return data

    class Meta:
        managed = True
        model = User
        fields = ['id', 'username', 'email',
                  'phone_number', 'password', 'tokens']

    def validate(self, attrs):
        if username_exists := User.objects.filter(
            username=attrs['username']
        ).exists():
            raise serializers.ValidationError(
                detail="User with this username exists!")

        if email_exists := User.objects.filter(
            username=attrs['email']
        ).exists():
            raise serializers.ValidationError(
                detail="User with this email exists!")

        if phone_number_exists := User.objects.filter(
            username=attrs['phone_number']
        ).exists():
            raise serializers.ValidationError(
                detail="User with this phone number exists!")
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'title', 'price', 'image']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    sub_total_price = serializers.SerializerMethodField()

    def get_sub_total_price(self, cart_item: CartItem):
        return cart_item.quantity*cart_item.product.price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'sub_total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    cart_price = serializers.SerializerMethodField()

    def get_cart_price(self, cart):
        return sum(item.quantity*item.product.price for item in cart.items.all())

    class Meta:
        model = User
        fields = ['items', 'cart_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
