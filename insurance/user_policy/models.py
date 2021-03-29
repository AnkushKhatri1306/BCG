from django.db import models


class Fuel(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'tbl_fuel'


class VehicleSegment(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'tbl_vehicle_seg'


class Region(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        db_table = 'tbl_region'


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    gender = models.SmallIntegerField(default=0)  # 0 = Male and 1 = Female
    income_group = models.CharField(max_length=20)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    marital_status = models.BooleanField(default=0)  # 0 = Single , 1 = Married

    class Meta:
        db_table = 'tbl_customer'


class InsurancePolicy(models.Model):
    purchase_date = models.DateField()
    premium = models.BigIntegerField()
    bodily_injury_liability = models.BooleanField(default=0)
    personal_injury_protection = models.BooleanField(default=0)
    property_damage_liability = models.BooleanField(default=0)
    collision = models.BooleanField(default=0)
    comprehensive = models.BooleanField(default=0)
    fuel = models.ForeignKey(Fuel, on_delete=models.DO_NOTHING)
    vehicle_segment = models.ForeignKey(VehicleSegment, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'tbl_insurance_policy'