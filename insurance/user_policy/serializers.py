from rest_framework import serializers
from .models import *
from insurance.utility import exception_detail
from insurance.config import *

class InsurancePolicyListSerializer(serializers.ModelSerializer):
    bodily_injury_liability = serializers.SerializerMethodField()
    personal_injury_protection = serializers.SerializerMethodField()
    property_damage_liability = serializers.SerializerMethodField()
    collision = serializers.SerializerMethodField()
    comprehensive = serializers.SerializerMethodField()
    fuel_id = serializers.CharField(source='fuel.id')
    fuel_name = serializers.CharField(source='fuel.name')
    vehicle_segment_id = serializers.CharField(source='vehicle_segment.id')
    vehicle_segment_name = serializers.CharField(source='vehicle_segment.name')
    gender = serializers.SerializerMethodField()
    income_group = serializers.CharField(source='customer.income_group')
    region_id = serializers.IntegerField(source='customer.region.id')
    region_name = serializers.CharField(source='customer.region.name')
    marital_status = serializers.SerializerMethodField()



    class Meta:
        model = InsurancePolicy
        fields = ('id', 'purchase_date', 'premium', 'bodily_injury_liability', 'personal_injury_protection',
                  'property_damage_liability', 'collision', 'comprehensive', 'fuel_id', 'fuel_name',
                  'vehicle_segment_id', 'vehicle_segment_name', 'customer_id', 'gender',
                  'income_group', 'region_id', 'region_name', 'marital_status')


    def get_bodily_injury_liability(self, obj):
        bodily_injury_liability = 'Yes'
        try:
            if obj.bodily_injury_liability == 0:
                bodily_injury_liability = 'No'
        except Exception as e:
            exception_detail()
        return bodily_injury_liability

    def get_personal_injury_protection(self, obj):
        personal_injury_protection = 'Yes'
        try:
            if obj.personal_injury_protection == 0:
                personal_injury_protection = 'No'
        except Exception as e:
            exception_detail()
        return personal_injury_protection

    def get_property_damage_liability(self, obj):
        property_damage_liability = 'Yes'
        try:
            if obj.property_damage_liability == 0:
                property_damage_liability = 'No'
        except Exception as e:
            exception_detail()
        return property_damage_liability

    def get_collision(self, obj):
        collision = 'Yes'
        try:
            if obj.collision == 0:
                collision = 'No'
        except Exception as e:
            exception_detail()
        return collision

    def get_comprehensive(self, obj):
        comprehensive = 'Yes'
        try:
            if obj.comprehensive == 0:
                comprehensive = 'No'
        except Exception as e:
            exception_detail()
        return comprehensive

    def get_gender(self, obj):
        gender = 'Male'
        try:
            if obj.customer.gender:
                gender = DEFAULT_GENDER_DICT_REVERSE.get(obj.customer.gender)
        except Exception as e:
            exception_detail()
        return gender


    def get_marital_status(self, obj):
        marital_status = 'Single'
        try:
            if obj.customer.marital_status:
                marital_status = DEFAULT_MARITAL_STATUS_REVERSE.get(obj.customer.marital_status)
        except Exception as e:
            exception_detail()
        return marital_status


class InsurancePolicySerializer(serializers.ModelSerializer):
    fuel_id = serializers.CharField(source='fuel.id')
    vehicle_segment_id = serializers.CharField(source='vehicle_segment.id')
    gender = serializers.IntegerField(source='customer.gender')
    income_group = serializers.CharField(source='customer.income_group')
    region_id = serializers.IntegerField(source='customer.region.id')
    marital_status = serializers.BooleanField(source='customer.marital_status')



    class Meta:
        model = InsurancePolicy
        fields = ('id', 'purchase_date', 'premium', 'bodily_injury_liability', 'personal_injury_protection',
                  'property_damage_liability', 'collision', 'comprehensive', 'fuel_id',
                  'vehicle_segment_id', 'customer_id', 'gender',
                  'income_group', 'region_id', 'marital_status')