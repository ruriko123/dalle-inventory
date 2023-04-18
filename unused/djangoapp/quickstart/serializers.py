from quickstart.models import IntblItems,Intblstorereqdetails,Intblstorerequisition
from rest_framework import serializers



class IntblItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntblItems
        fields  = '__all__'



class IntblstorereqdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intblstorereqdetails
        fields  = '__all__'


class IntblstorerequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intblstorerequisition
        fields  = '__all__'