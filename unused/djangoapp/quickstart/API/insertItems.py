from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quickstart.serializers import IntblItemsSerializer
from quickstart.models import IntblItems


class IntblItemsAPI(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer=IntblItemsSerializer(data=data["RequisitionDetailsList"],many=True)
        if serializer.is_valid():
            for item in data["RequisitionDetailsList"]:
                if item["ExpDate"]=="":
                    IntblItems.objects.create(rate=item["Rate"],taxable=item["Taxable"],status=item["Status"],groupname=item["GroupName"],department=item["Department"],stocktype=item["StockType"],uom=item["UOM"],code=item["Code"],brandname=item["BrandName"],name=item["Name"],ItemID=item["ItemID"])
                else:
                    IntblItems.objects.create(rate=item["Rate"],taxable=item["Taxable"],status=item["Status"],expdate=item["ExpDate"],groupname=item["GroupName"],department=item["Department"],stocktype=item["StockType"],uom=item["UOM"],code=item["Code"],brandname=item["BrandName"],name=item["Name"],ItemID=item["ItemID"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
