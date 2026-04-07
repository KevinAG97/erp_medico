from rest_framework import serializers
from .models import Paciente


def validar_cpf(cpf: str) -> bool:
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i, peso in enumerate(range(10, 1, -1)):
        soma = sum(int(cpf[j]) * (peso - j) for j in range(i + 1))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i + 1]):
            return False

    return True


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

    def validate_cpf(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('O CPF deve conter apenas números.')
        if len(value) != 11:
            raise serializers.ValidationError('O CPF deve conter exatamente 11 dígitos.')
        if not validar_cpf(value):
            raise serializers.ValidationError('CPF inválido.')
        return value
