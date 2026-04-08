from rest_framework import serializers
from .models import Paciente





class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

    def validate_cpf(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('O CPF deve conter apenas números.')
        if len(value) != 11:
            raise serializers.ValidationError('O CPF deve conter exatamente 11 dígitos.')
        
