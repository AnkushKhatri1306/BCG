from rest_framework import viewsets
from .controllers import UserPolicyHomeController
from .models import InsurancePolicy
from .serializers import InsurancePolicyListSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from insurance.utility import get_response_object
from insurance.utility import exception_detail


class UserPolicyHomeViewSet(viewsets.ModelViewSet, UserPolicyHomeController):

    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicyListSerializer

    @action(detail=False, methods=['POST'], url_path='data_upload')
    def policy_data_upload_api(self, request):
        """
        METHOD : POST
        BODY TO SEND: {
            "file": <file in memory object>
        }
        RESPONSE (SUCCESS) : {
            "message": "Success in uploading policy data."
        }
        RESPONSE (ERROR) : {
            "message": "Error in policy data upload . Please try Again"
        }
        URL : '/home/data_upload/'
        :param request: request data containing the file object
        :return:
        """
        try:
            success, msg = self.policy_data_upload(request)
            response_data = get_response_object(success, msg)
        except Exception as e:
            exception_detail()
            response_data = get_response_object(False, 'Error in policy data upload . Please try Again')
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='list')
    def get_policy_list_data(self, request):
        """
        METHOD : GET
        PARAMS TO SEND : {
            "page_size": <page_size>,
            "page_number": <page_number>,
            "search_id": <search_id>
        }
        RESPONSE (SUCCESS) : {
            "status": "success",
            "message": "Success in getting policy list."
        }
        :param request:
        :return:
        URL : '/home/list/'
        """
        try:
            success, msg, policy_data = self.get_policy_list(request)
            response_data = get_response_object(success, msg, policy_data)
        except Exception as e:
            exception_detail()
            response_data = get_response_object(False, 'Error in getting policy list.')
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='options')
    def get_policy_edit_options_data(self, request):
        """
        METHOD : GET
        RESPONSE (SUCCESS) : {
            "status": "success",
            "message": "Success in getting policy options."
        }
        :param request:
        :return:
        URL: /home/options/
        """
        try:
            success, msg, options_data = self.get_policy_edit_options(request)
            response_data = get_response_object(success, msg, options_data)
        except Exception as e:
            exception_detail()
            response_data = get_response_object(False, 'Error in getting policy options.')
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='save_policy')
    def create_or_update_policy_data_api(self, request):
        """
        METHOD : POST
        BODY TO SEND: {
            "bodily_injury_liability": false
            "collision": true
            "comprehensive": true
            "customer_id": 400
            "fuel_id": "13"
            "gender": 0
            "id": 1206
            "income_group": "0- $25K"
            "marital_status": false
            "personal_injury_protection": false
            "premium": 958
            "property_damage_liability": false
            "purchase_date": "2018-01-16"
            "region_id": 17
            "vehicle_segment_id": "13"
        }
        RESPONSE (SUCCESS) : {
            "message": "Success in saving policy data ."
        }
        :param request:
        :return:
        URL: /home/save_policy/
        """
        try:
            success, msg = self.create_or_update_policy_data(request)
            response_data = get_response_object(success, msg)
        except Exception as e:
            exception_detail()
            response_data = get_response_object(False, 'Error in saving policy data . Please try Again')
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='get_policy')
    def get_insurance_policy_data(self, request):
        """
        METHOD : GET
        PARAMS TO SEND : {
            "policy_id": <id>
        }
        RESPONSE (SUCCESS) : {
            "status": "success",
            "message": "Success in getting policy data."
        }
        :param request:
        :return:
        URL: /home/get_policy/
        """
        try:
            success, msg, options_data = self.get_insurance_policy(request)
            response_data = get_response_object(success, msg, options_data)
        except Exception as e:
            exception_detail()
            response_data = get_response_object(False, 'Error in getting policy data')
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='get_policy_graph')
    def get_insurance_policy_graph_details(self, request):
        """
        METHOD : GET
        PARAMS TO SEND : {
            "year": <year>
        }
        RESPONSE (SUCCESS) : {
            "status": "success",
            "message": "Success in getting policy graph data."
        }
        :param request:
        :return:
        URL: /home/get_policy_graph/
        """
        try:
            success, msg, options_data = self.get_insurance_policy_graph_data(request)
            response_data = get_response_object(success, msg, options_data)
        except Exception as e:
            exception_detail()
            response_data = get_response_object(False, 'Error in getting policy graph data.')
        return Response(data=response_data, status=status.HTTP_200_OK)




