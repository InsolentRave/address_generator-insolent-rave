# coding: utf-8

from copy import deepcopy
from http import HTTPStatus

from django.http import HttpResponseServerError, JsonResponse
from rest_framework import viewsets
from rest_framework.exceptions import ParseError

from .models import Address
from .serializers import AddressSerializer, CreateAddressRequestSerializer

from .errors import AddressPathError, NotSupportedCurrency, PrivateKeyError


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def create(self, request):
        data = CreateAddressRequestSerializer(request.data).data

        try:
            address = Address.create(**data)
        except PrivateKeyError as exc:
            return HttpResponseServerError(f"Invalid private key: {exc}")
        except NotSupportedCurrency as exc:
            raise ParseError(f"Non supported currency: {exc}")
        except AddressPathError as exc:
            raise ParseError(f"Invalid key path: {exc}")


        return JsonResponse(AddressSerializer(address).data, status=HTTPStatus.CREATED)
