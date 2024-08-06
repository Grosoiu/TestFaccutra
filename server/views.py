from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.authtoken.models import Token

from .serializers import *

#Custom function
from .utils import get_company_based_on_CUI

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response("Invalid credentials", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def company(request):
    user = request.user
    cui = request.data.get('cui')
    
    if cui:
        # If CUI is provided, fetch the company details from the external API
        try:
            company_info = get_company_based_on_CUI(cui)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        company_data = {
            'user': user.id,
            'company_registration_number': company_info.company_registration_number,
            'company_tin': company_info.company_tin,
            'company_name': company_info.company_name,
            'company_address_country_subentity': company_info.company_address_country_subentity,
            'company_address_country': company_info.company_address_country,
            'company_address_country_code': company_info.company_address_country_code,
            'company_address_country_subentity_code': company_info.company_address_country_subentity_code,
            'company_address_city': company_info.company_address_city,
            'company_address_street': company_info.company_address_street,
            'company_address_details': company_info.company_address_details,
            'company_vat_status': company_info.company_vat_status,
            'company_vat_number': company_info.company_vat_number,
        }
    else:
        # If CUI is not provided, expect all company details in the request data
        company_data = request.data.copy()
        company_data['user'] = user.id
    
    serializer = CompanySerializer(data=company_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_column(request, column_name):
    user = request.user
    value = request.data.get(column_name)
    
    if column_name not in ['email', 'name', 'phone_number']:
        return Response({"error": "Invalid column name"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not value:
        return Response({"error": f"{column_name} value is required"}, status=status.HTTP_400_BAD_REQUEST)

    if column_name == 'email':
        user.email = value
        user.status = 'pending'
    elif column_name == 'name':
        user.name = value
    elif column_name == 'phone_number':
        user.phone_number = value
        user.is_2fa_active = False
    
    user.save()
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_company_column(request, company_id, column_name):
    user = request.user  # Get the authenticated user
    value = request.data.get(column_name)
    
    if column_name not in ['company_name', 'company_address_city', 'company_address_street', 'company_address_details']:
        return Response({"error": "Invalid column name"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not value:
        return Response({"error": f"{column_name} value is required"}, status=status.HTTP_400_BAD_REQUEST)

    company = get_object_or_404(Company, user=user, id=company_id)  # Fetch the company by user and company_id
    
    setattr(company, column_name, value)
    company.save()
    
    serializer = CompanySerializer(company)
    return Response(serializer.data, status=status.HTTP_200_OK)
