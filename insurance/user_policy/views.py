from rest_framework import viewsets
from .controllers import UserPolicyHomeController
from .models import InsurancePolicy
from .serializers import InsurancePolicySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from insurance.utility import get_response_object
from insurance.utility import exception_detail


class UserPolicyHomeViewSet(viewsets.ModelViewSet, UserPolicyHomeController):

    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicySerializer

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
        PERMISSION : ANYONE
        HEADER TO SEND : {
            Authorization : Bearer + <space> + <access token>
        }
        BODY TO SEND : {
            "id": <id>
        }
        RESPONSE (SUCCESS) : {
            "status": "success",
            "message": "Success in saving software version."
        }
        :param request:
        :return:
        URL: upload/activate_software_version/
        """
        try:
            success, msg, policy_data = self.get_policy_list(request)
            response_data = get_response_object(success, msg, policy_data)
        except Exception as e:
            exception_detail()
            response_data = get_response_object(False, 'Error in activating software version.')
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='list')
    def get_policy_edit_options_data(self, request):
        """
        METHOD : POST
        PERMISSION : ANYONE
        HEADER TO SEND : {
            Authorization : Bearer + <space> + <access token>
        }
        BODY TO SEND : {
            "id": <id>
        }
        RESPONSE (SUCCESS) : {
            "status": "success",
            "message": "Success in saving software version."
        }
        :param request:
        :return:
        URL: upload/activate_software_version/
        """
        try:
            success, msg, options_data = self.get_policy_edit_options(request)
            response_data = get_response_object(success, msg, options_data)
        except Exception as e:
            exception_detail()
            response_data = get_response_object(False, 'Error in activating software version.')
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='save_policy')
    def create_or_update_policy_data_api(self, request):
        """
        METHOD : POST
        BODY TO SEND: {
            "file": <file in memory object>
        }
        RESPONSE (SUCCESS) : {
            "message": "Success in uploading course sheet ."
        }
        RESPONSE (ERROR) : {
            "message": "Error in course data upload . Please try Again"
        }
        :param request: request data containing the file object
        :return:
        """
        try:
            success, msg = self.create_or_update_policy_data(request)
            response_data = get_response_object(success, msg)
        except Exception as e:
            exception_detail()
            response_data = get_response_object(False, 'Error in saving policy data . Please try Again')
        return Response(data=response_data, status=status.HTTP_200_OK)




