from .models import *
from .serializers import *
from insurance.utility import exception_detail
from django.db.models import Q
from django.db import transaction
from insurance.config import *
import csv
from django.core.paginator import Paginator


class UserPolicyHomeController():

    def policy_data_upload(self, request):
        """
        function to save the data which is uploaded through the sheet into the database.
        1. Getting the file object from request object
        2. iterating over the records and then making a dict for all distinct elements inside it.
        3. calling the function for saving the value which is distinct into the database according to relevant tables.
        4. calling the function for saving the data for insurance table .
        5. If not success then raising a manual error
        :param request: request data
        :return: success or error status with message
        """
        success = False
        msg = 'Error in policy data upload . Please try Again'
        try:
            with transaction.atomic():
                file_obj = request.FILES.get('file')
                file_obj = file_obj.read().decode('utf-8').splitlines()
                csv_reader = csv.DictReader(file_obj)
                distinct_fuel_dict = {}
                distinct_vehicle_segment_dict = {}
                distinct_region_dict = {}
                distinct_customer_id_dict = {}
                for row in csv_reader:
                    distinct_fuel_dict[row.get('Fuel')] = True
                    distinct_vehicle_segment_dict[row.get('VEHICLE_SEGMENT')] = True
                    distinct_region_dict[row.get('Customer_Region')] = True
                    distinct_customer_id_dict[row.get('Customer_id')] = {
                        'gender': row.get('Customer_Gender'),
                        'income_group': row.get('Customer_Income group'),
                        'region': row.get('Customer_Region'),
                        'marital_status': row.get('Customer_Marital_status')
                    }
                fuel_name_id_dict = self.save_and_get_fuel_vehicle_region_id_dict(distinct_fuel_dict, Fuel)
                vehicle_segment_name_id_dict = self.save_and_get_fuel_vehicle_region_id_dict(distinct_vehicle_segment_dict,
                                                                                             VehicleSegment)
                region_name_id_dict = self.save_and_get_fuel_vehicle_region_id_dict(distinct_region_dict, Region)
                customer_id_dict = self.save_and_get_customer_id_dict(distinct_customer_id_dict, region_name_id_dict)
                success = self.save_insurance_policy_data(fuel_name_id_dict, vehicle_segment_name_id_dict,
                                                     customer_id_dict, csv.DictReader(file_obj))

                if not success:
                    raise Exception('Error in policy data upload . Please try Again')
                msg = 'Success in uploading policy data.'
        except Exception as e:
            exception_detail()
        return success, msg


    def save_insurance_policy_data(self, fuel_name_id_dict, vehicle_segment_name_id_dict, customer_id_dict, csv_reader):
        """
        function to save the data into insurance table .
        1. Iterator over the data in csv reader
        2. making objects according to data present
        3. appending into create list to in single time able to save all data.
        :param fuel_name_id_dict: fuel name corresponding id list
        :param vehicle_segment_name_id_dict: vehicle segment name corresponding id list
        :param customer_id_dict: customer id corresponding id list
        :param csv_reader: csv reader with the csv data
        :return:
        """
        success = False
        try:
            create_list = []
            for row in csv_reader:
                policy_obj = InsurancePolicy()
                policy_obj.purchase_date = row.get('Date of Purchase')
                policy_obj.premium = row.get('Premium')
                policy_obj.bodily_injury_liability = row.get('bodily injury liability')
                policy_obj.personal_injury_protection = row.get(' personal injury protection')
                policy_obj.property_damage_liability = row.get(' property damage liability')
                policy_obj.collision = row.get(' collision')
                policy_obj.comprehensive = row.get(' comprehensive')
                policy_obj.fuel_id = fuel_name_id_dict.get(row.get('Fuel'))
                policy_obj.vehicle_segment_id = vehicle_segment_name_id_dict.get(row.get('VEHICLE_SEGMENT'))
                policy_obj.customer_id =  customer_id_dict.get(row.get('Customer_id'))
                create_list.append(policy_obj)
            if create_list:
                InsurancePolicy.objects.bulk_create(create_list)
            success = True
        except Exception as e:
            exception_detail()
        return success

    def save_and_get_fuel_vehicle_region_id_dict(self, distinct_dict, Model):
        """
        function to save the data for fuel , vehicle and region data into thd database
        1. getting the data related to the model and then making a dict with name and id
        2. checking the length is same means all data is there no need to save
        3. using for loop saving all the data into the database
        :param distinct_dict:
        :param Model:
        :return:
        """
        name_id_dict = {}
        try:
            objs = Model.objects.filter(name__in=distinct_dict).values('id', 'name')
            name_id_dict = {obj.get('name'): obj.get('id') for obj in objs}
            if not len(distinct_dict.keys()) == len(name_id_dict.keys()):
                for name, flag in distinct_dict.items():
                    if not name_id_dict.get(name):
                        obj = Model()
                        obj.name = name
                        obj.save()
                        name_id_dict[name] = obj.id
        except Exception as e:
            exception_detail()
        return name_id_dict
    
    
    def save_and_get_customer_id_dict(self, distinct_customer_id_dict, region_name_id_dict):
        """
        function to save customer data and then get the dict of that
        1. first getting the customer objects and then checking the length for comparision
        2. making a customer object and saving into the database , and making a dictionary
        :param distinct_customer_id_dict:
        :param region_name_id_dict:
        :return:
        """
        customer_id_dict = {}
        try:
            objs = Customer.objects.filter(customer_id__in=distinct_customer_id_dict).values('customer_id')
            customer_id_dict = {obj.get('customer_id'): obj.get('customer_id') for obj in objs}
            if not len(distinct_customer_id_dict.keys()) == len(region_name_id_dict.keys()):
                for customer_id, customer_data in distinct_customer_id_dict.items():
                    if not customer_id_dict.get(customer_id):
                        obj = Customer()
                        obj.customer_id = customer_id
                        obj.gender = DEFAULT_GENDER_DICT.get(customer_data.get('gender'))
                        obj.income_group = customer_data.get('income_group')
                        obj.region_id = region_name_id_dict.get(customer_data.get('region'))
                        obj.marital_status = customer_data.get('marital_status')
                        obj.save()
                        customer_id_dict[customer_id] = obj.customer_id
        except Exception as e:
            exception_detail()
        return customer_id_dict

    def get_policy_list(self, request):
        """
        function to get the policy list data
        1. getting the required data from request data
        2. then making a search filter for applying into InsurancePolicy object
        3. making a paginator object and according to the page number getting the object
        4. serializing it according to the need and then sending it.
        :param request:
        :return:
        """
        success = False
        msg = 'Error in getting the Policy data.'
        policy_data = {}
        try:
            page_size = request.GET.get('page_size', 10)
            page_number = request.GET.get('page_number', 1)
            search_id = request.GET.get('search_id')
            search_filter = Q()
            if search_id:
                if not search_id.isdigit():
                    return False, 'Search is not correct . Please give number as input', policy_data
                search_filter = Q(id=search_id) | Q(customer_id=search_id)
            policy_objs = InsurancePolicy.objects.filter(search_filter).order_by('id')
            paginator_obj = Paginator(policy_objs, page_size)
            page_obj = paginator_obj.page(page_number)
            policy_page_obj = page_obj.object_list
            policy_serailizer = InsurancePolicyListSerializer(policy_page_obj, many=True)
            policy_data['policy_data'] = policy_serailizer.data
            policy_data['total_page'] = paginator_obj.num_pages
            policy_data['has_next'] = page_obj.has_next()
            policy_data['has_previous'] = page_obj.has_previous()
            policy_data['start_index'] = page_obj.start_index()
            policy_data['end_index'] = page_obj.end_index()
            policy_data['count'] = paginator_obj.count
            success = True
            msg = 'Success in getting the Policy data.'
        except Exception as e:
            exception_detail()
        return success, msg, policy_data


    def get_policy_edit_options(self, request):
        """
        function to get the options list need to be there in edit option of policy data
        1. getting the data for fuel , vechile_segment and region
        :param request:
        :return:
        """
        success = False
        msg = 'Error in getting the Policy edit options data.'
        options_data = {}
        try:
            options_data['fuel_list'] = Fuel.objects.filter().values('id', 'name')
            options_data['vehicle_segment_list'] = VehicleSegment.objects.filter().values('id', 'name')
            options_data['region_list'] = Region.objects.filter().values('id', 'name')
            success = True
            msg = 'Success in getting the Policy edit options data.'
        except Exception as e:
            exception_detail()
        return success, msg, options_data


    def create_or_update_policy_data(self, request):
        """
        fucntion to create or update the data of insurance policy into the database
        1. if id is there then getting the object of insurance and if not then making new object
        2. binding the data which is came in request
        3. saving it to database
        :param request:
        :return:
        """
        success = False
        msg = 'Error in saving policy data . Please try Again.'
        try:
            post_data = request.data
            if post_data:
                if post_data.get('id'):
                    insurance_obj = InsurancePolicy.objects.get(id=post_data.get('id'))
                else:
                    insurance_obj = InsurancePolicy()
                insurance_obj.premium = post_data.get('premium')
                insurance_obj.bodily_injury_liability = post_data.get('bodily_injury_liability')
                insurance_obj.personal_injury_protection = post_data.get('personal_injury_protection')
                insurance_obj.property_damage_liability = post_data.get('property_damage_liability')
                insurance_obj.collision = post_data.get('collision')
                insurance_obj.comprehensive = post_data.get('comprehensive')
                insurance_obj.fuel_id = post_data.get('fuel_id')
                insurance_obj.vehicle_segment_id = post_data.get('vehicle_segment_id')
                insurance_obj.save()
                customer_obj = Customer.objects.get(customer_id=post_data.get('customer_id'))
                customer_obj.gender = post_data.get('gender')
                customer_obj.income_group = post_data.get('income_group')
                customer_obj.region_id = post_data.get('region_id')
                customer_obj.marital_status = post_data.get('marital_status')
                customer_obj.save()
                success = True
                msg = 'Success in saving policy data . Please try Again.'
        except Exception as e:
            exception_detail()
        return success, msg


    def get_insurance_policy(self, request):
        """
        function to get the options list need to be there in edit option of policy data
        1. getting the data for fuel , vechile_segment and region
        :param request:
        :return:
        """
        success = False
        msg = 'Error in getting the Policy edit options data.'
        policy_data = {}
        try:
            policy_id = request.GET.get('policy_id')
            if policy_id:
                policy_obj = InsurancePolicy.objects.get(id=policy_id)
                policy_serializer = InsurancePolicySerializer(policy_obj)
                policy_data = policy_serializer.data
            success = True
            msg = 'Success in getting the Policy edit options data.'
        except Exception as e:
            exception_detail()
        return success, msg, policy_data

