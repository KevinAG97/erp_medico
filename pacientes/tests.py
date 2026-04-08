from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Paciente


class PacienteModelTest(TestCase):
    """Testes unitários do model Paciente"""

    def setUp(self):
        self.paciente = Paciente.objects.create(
            nome='João Silva',
            cpf='12345678901',
            data_nascimento='1990-01-15',
            telefone='51999999999',
            email='joao@email.com',
        )

    def test_paciente_criado_com_sucesso(self):
        self.assertEqual(self.paciente.nome, 'João Silva')
        self.assertEqual(self.paciente.cpf, '12345678901')

    def test_str_retorna_nome(self):
        self.assertEqual(str(self.paciente), 'João Silva')

    def test_cpf_unico(self):
        with self.assertRaises(Exception):
            Paciente.objects.create(
                nome='Maria Silva',
                cpf='12345678901',
                data_nascimento='1995-05-10',
            )


class PacienteAPITest(TestCase):
    """Testes de integração da API de Pacientes"""

    def setUp(self):
        self.client = APIClient()
        self.paciente = Paciente.objects.create(
            nome='Ana Costa',
            cpf='98765432100',
            data_nascimento='1985-03-20',
            telefone='51988888888',
            email='ana@email.com',
        )

    def test_listar_pacientes(self):
        response = self.client.get('/api/pacientes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_criar_paciente(self):
        dados = {
            'nome': 'Carlos Souza',
            'cpf': '11122233344',
            'data_nascimento': '2000-07-10',
        }
        response = self.client.post('/api/pacientes/', dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Paciente.objects.count(), 2)

    def test_buscar_paciente_por_id(self):
        response = self.client.get(f'/api/pacientes/{self.paciente.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cpf'], '98765432100')

    def test_atualizar_paciente(self):
        dados = {
            'nome': 'Ana Costa Atualizada',
            'cpf': '98765432100',
            'data_nascimento': '1985-03-20',
        }
        response = self.client.put(
            f'/api/pacientes/{self.paciente.id}/', dados, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Ana Costa Atualizada')

    def test_deletar_paciente(self):
        response = self.client.delete(f'/api/pacientes/{self.paciente.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Paciente.objects.count(), 0)

    def test_criar_paciente_cpf_duplicado_retorna_erro(self):
        dados = {
            'nome': 'Outro Nome',
            'cpf': '98765432100',
            'data_nascimento': '1990-01-01',
        }
        response = self.client.post('/api/pacientes/', dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
