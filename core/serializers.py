from rest_framework import serializers
from .models import CustomUser, File

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    def validate_file(self, value):
        valid_extensions = ['pptx', 'docx', 'xlsx']
        print(value)
        file_extension = value.name.split('.')[-1]
        if file_extension not in valid_extensions:
            raise serializers.ValidationError("Only pptx, docx, and xlsx files are allowed.")
        return value
    
    class Meta:
        model = File
        fields = '__all__'