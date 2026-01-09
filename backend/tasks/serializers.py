from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, Contact, Deal, Task, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    email = serializers.EmailField(source='user.email', required=False, allow_blank=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'phone', 'job_title', 'department', 'company', 'profile_picture', 'bio'
        ]
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """Ensure user fields are properly included in response"""
        ret = super().to_representation(instance)
        ret['first_name'] = instance.user.first_name
        ret['last_name'] = instance.user.last_name
        ret['email'] = instance.user.email
        ret['username'] = instance.user.username
        return ret

    def update(self, instance, validated_data):
        # Extract nested user dict (DRF groups dotted-source fields here)
        user_data = validated_data.pop('user', {})
        
        # Update User model fields
        user = instance.user
        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()
        
        # Update UserProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance





class CompanySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    contacts_count = serializers.SerializerMethodField()
    deals_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'industry', 'website', 'phone', 'email', 'address',
                  'notes', 'created_at', 'updated_at', 'created_by', 'created_by_name',
                  'contacts_count', 'deals_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def get_contacts_count(self, obj):
        return obj.contacts.count()

    def get_deals_count(self, obj):
        return obj.deals.count()


class ContactSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    company_name = serializers.CharField(source='company.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
                  'position', 'company', 'company_name', 'notes', 'created_at',
                  'updated_at', 'created_by', 'created_by_name']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'full_name']


class DealSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    contact_name = serializers.CharField(source='contact.full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Deal
        fields = ['id', 'title', 'amount', 'stage', 'probability', 'expected_close_date',
                  'company', 'company_name', 'contact', 'contact_name', 'notes',
                  'created_at', 'updated_at', 'created_by', 'created_by_name']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class TaskSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='contact.full_name', read_only=True)
    deal_title = serializers.CharField(source='deal.title', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date',
                  'contact', 'contact_name', 'deal', 'deal_title', 'assigned_to',
                  'assigned_to_name', 'created_at', 'updated_at', 'created_by',
                  'created_by_name']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
