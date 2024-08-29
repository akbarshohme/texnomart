from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer

from texnomart.models import Category, Product, ProductAttribute, Key, Value


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    category_name = serializers.CharField(source="category.title")
    is_liked = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and user in obj.is_liked.all()

    def get_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            image_url = primary_image.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url) if request else image_url

    class Meta:
        model = Product
        fields = '__all__'


class ProductModelSerializer(ModelSerializer):
    category_name = serializers.CharField(source="category.title")
    is_liked = serializers.SerializerMethodField()
    count_is_liked = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    comment_info = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, instance):
        return [{attr.key.name: attr.value.name} for attr in instance.attributes.all()]

    def get_comment_info(self, obj):
        comment_count = obj.comments.count()
        comments = obj.comments.all().values('comment', 'rating', 'user__username')
        return {'comment_count': comment_count, 'comments': comments}

    def get_all_images(self, instance):
        request = self.context.get('request')
        images = instance.images.all().order_by('-is_primary', '-id')
        return [request.build_absolute_uri(img.image.url) for img in images] if request else [img.image.url for img in images]

    def get_avg_rating(self, obj):
        avg_rating = obj.comments.all().aggregate(avg_rating=Round(Avg('rating')))
        return avg_rating['avg_rating']

    def get_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            image_url = primary_image.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url) if request else image_url

    def get_count_is_liked(self, instance):
        return instance.is_liked.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and user in obj.is_liked.all()

    class Meta:
        model = Product
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, product):
        attributes = ProductAttribute.objects.filter(product=product)
        return {attribute.key.name: attribute.value.name for attribute in attributes}

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'attributes']


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = '__all__'


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3, max_length=150, required=True)
    first_name = serializers.CharField(min_length=3, max_length=150, required=False)
    last_name = serializers.CharField(min_length=3, max_length=150, required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists.')
        return username

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match.')
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
