import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from django.test import RequestFactory, override_settings
from rest_framework.test import APITestCase

from wellq.urls import servir_media

from .models import Clinica, Clinico, Examen, Paciente

MEDIA_TEMPORAL = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class ExamenesPorClinicaTests(APITestCase):
    """
    Los datos de init.sql (10 clínicas y 10 clínicos) los carga la migración 0003,
    por lo que también existen en la base de datos de pruebas.
    """

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)

    def registrar_paciente(self, rut, correo, clinica_id=1):
        respuesta = self.client.post('/api/v1/auth/register/paciente/', {
            'rut': rut, 'nombres': 'Paciente', 'apellidos': rut,
            'correo': correo, 'celular': 912345678, 'password': 'Paciente01.',
            'clinica': clinica_id,
        }, format='json')
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        return Paciente.objects.get(rut=rut)

    def crear_clinico(self, clinica):
        clinico = Clinico.objects.filter(clinica=clinica).first()
        clinico.user = User.objects.create_user(username=clinico.rut, password='Clinico123!')
        clinico.save()
        return clinico

    def autenticar(self, rut, password):
        respuesta = self.client.post('/api/v1/auth/login/', {'rut': rut, 'password': password}, format='json')
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {respuesta.data['access']}")

    def subir_examen(self, titulo, paciente_id=None, estado_esperado=201):
        archivo = SimpleUploadedFile(f'{titulo}.pdf', b'%PDF-1.4 prueba', content_type='application/pdf')
        datos = {'titulo': titulo, 'sesion': 'Prueba', 'archivo': archivo}
        if paciente_id:
            datos['paciente'] = paciente_id
        respuesta = self.client.post('/api/v1/examenes/', datos, format='multipart')
        self.assertEqual(respuesta.status_code, estado_esperado, respuesta.content)
        return respuesta.data.get('id')

    def registrar_en_misma_clinica(self, paciente_base, rut, correo):
        return self.registrar_paciente(rut, correo, clinica_id=paciente_base.clinica_id)

    def archivo_accesible(self, ruta_media):
        # Los tests corren con DEBUG=False (sin ruta /media/), por eso se llama a la vista directo
        try:
            servir_media(RequestFactory().get('/media/' + ruta_media), ruta_media)
            return True
        except Http404:
            return False

    def titulos_visibles(self):
        respuesta = self.client.get('/api/v1/examenes/')
        self.assertEqual(respuesta.status_code, 200)
        return {examen['titulo'] for examen in respuesta.data}

    def test_registro_guarda_la_clinica_elegida(self):
        clinica = Clinica.objects.order_by('-id').first()
        paciente = self.registrar_paciente('100000001', 'a@test.cl', clinica_id=clinica.id)
        self.assertEqual(paciente.clinica_id, clinica.id)

    def test_registro_exige_una_clinica_valida(self):
        base = {'nombres': 'P', 'apellidos': 'X', 'celular': 912345678, 'password': 'Paciente01.'}
        url = '/api/v1/auth/register/paciente/'

        sin_clinica = self.client.post(url, {**base, 'rut': '100000001', 'correo': 'a@test.cl'}, format='json')
        self.assertEqual(sin_clinica.status_code, 400)
        self.assertIn('clinica', sin_clinica.data)

        inexistente = self.client.post(url, {**base, 'rut': '100000002', 'correo': 'b@test.cl', 'clinica': 9999}, format='json')
        self.assertEqual(inexistente.status_code, 400)
        self.assertIn('clinica', inexistente.data)
        self.assertFalse(Paciente.objects.filter(rut__in=['100000001', '100000002']).exists())

    def test_clinico_solo_ve_examenes_de_su_clinica(self):
        paciente_a = self.registrar_paciente('100000001', 'a@test.cl')
        paciente_b = self.registrar_paciente('100000002', 'b@test.cl', clinica_id=2)
        self.assertNotEqual(paciente_a.clinica_id, paciente_b.clinica_id)

        self.autenticar(paciente_a.rut, 'Paciente01.')
        examen_a = self.subir_examen('examen_a')
        self.autenticar(paciente_b.rut, 'Paciente01.')
        self.subir_examen('examen_b')

        clinico_a = self.crear_clinico(paciente_a.clinica)
        clinico_b = self.crear_clinico(paciente_b.clinica)

        self.autenticar(clinico_a.rut, 'Clinico123!')
        self.assertEqual(self.titulos_visibles(), {'examen_a'})

        self.autenticar(clinico_b.rut, 'Clinico123!')
        self.assertEqual(self.titulos_visibles(), {'examen_b'})
        # Tampoco puede abrir ni eliminar el examen de otra clínica
        self.assertEqual(self.client.get(f'/api/v1/examenes/{examen_a}/').status_code, 404)
        self.assertEqual(self.client.delete(f'/api/v1/examenes/{examen_a}/').status_code, 404)
        self.assertTrue(Examen.objects.filter(id=examen_a).exists())

    def test_login_devuelve_nombre_de_la_clinica(self):
        paciente = self.registrar_paciente('100000001', 'a@test.cl')
        respuesta = self.client.post('/api/v1/auth/login/', {
            'rut': paciente.rut, 'password': 'Paciente01.'}, format='json')
        self.assertEqual(respuesta.data['clinica'], paciente.clinica.nombre)

        clinico = self.crear_clinico(paciente.clinica)
        respuesta = self.client.post('/api/v1/auth/login/', {
            'rut': clinico.rut, 'password': 'Clinico123!'}, format='json')
        self.assertEqual(respuesta.data['clinica'], clinico.clinica.nombre)

    def test_clinico_deshabilita_examen_sin_eliminarlo(self):
        paciente = self.registrar_paciente('100000001', 'a@test.cl')
        self.autenticar(paciente.rut, 'Paciente01.')
        examen_id = self.subir_examen('examen_a')
        url_archivo = self.client.get(f'/api/v1/examenes/{examen_id}/').data['archivo']
        ruta_media = url_archivo.split('/media/', 1)[1]
        self.assertTrue(self.archivo_accesible(ruta_media))

        # El paciente no puede deshabilitar ni eliminar
        self.assertEqual(self.client.post(f'/api/v1/examenes/{examen_id}/deshabilitar/').status_code, 403)
        self.assertEqual(self.client.delete(f'/api/v1/examenes/{examen_id}/').status_code, 403)

        clinico = self.crear_clinico(paciente.clinica)
        self.autenticar(clinico.rut, 'Clinico123!')
        respuesta = self.client.post(f'/api/v1/examenes/{examen_id}/deshabilitar/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(respuesta.data['habilitado'])
        self.assertIsNone(respuesta.data['archivo'])

        # El registro y el archivo siguen existiendo, pero el archivo no se puede ver
        examen = Examen.objects.get(id=examen_id)
        self.assertFalse(examen.habilitado)
        self.assertTrue(examen.archivo.storage.exists(examen.archivo.name))
        self.assertFalse(self.archivo_accesible(ruta_media))

        # El clínico lo sigue viendo en su lista (como deshabilitado)
        self.assertEqual(self.titulos_visibles(), {'examen_a'})

        # DELETE tampoco elimina: solo deshabilita
        self.assertEqual(self.client.delete(f'/api/v1/examenes/{examen_id}/').status_code, 200)
        self.assertTrue(Examen.objects.filter(id=examen_id).exists())

        # El paciente ya no ve el examen deshabilitado, ni en la lista ni por id
        self.autenticar(paciente.rut, 'Paciente01.')
        self.assertEqual(self.titulos_visibles(), set())
        self.assertEqual(self.client.get(f'/api/v1/examenes/{examen_id}/').status_code, 404)

        # El clínico puede volver a habilitarlo y el paciente lo vuelve a ver
        self.autenticar(clinico.rut, 'Clinico123!')
        respuesta = self.client.post(f'/api/v1/examenes/{examen_id}/habilitar/')
        self.assertTrue(respuesta.data['habilitado'])
        self.assertTrue(self.archivo_accesible(ruta_media))
        self.autenticar(paciente.rut, 'Paciente01.')
        self.assertEqual(self.titulos_visibles(), {'examen_a'})

    def test_paciente_solo_ve_sus_propios_examenes(self):
        paciente_a = self.registrar_paciente('100000001', 'a@test.cl')
        paciente_b = self.registrar_paciente('100000002', 'b@test.cl')

        self.autenticar(paciente_a.rut, 'Paciente01.')
        self.subir_examen('examen_a')
        self.autenticar(paciente_b.rut, 'Paciente01.')
        self.subir_examen('examen_b')

        self.assertEqual(self.titulos_visibles(), {'examen_b'})

    def test_pacientes_de_la_misma_clinica_no_ven_documentos_entre_si(self):
        paciente_1 = self.registrar_paciente('100000001', 'a@test.cl')
        paciente_2 = self.registrar_en_misma_clinica(paciente_1, '100000002', 'b@test.cl')
        self.assertEqual(paciente_1.clinica_id, paciente_2.clinica_id)

        self.autenticar(paciente_1.rut, 'Paciente01.')
        examen_1 = self.subir_examen('examen_paciente_1')
        self.assertEqual(self.titulos_visibles(), {'examen_paciente_1'})

        self.autenticar(paciente_2.rut, 'Paciente01.')
        self.assertEqual(self.titulos_visibles(), set())
        self.assertEqual(self.client.get(f'/api/v1/examenes/{examen_1}/').status_code, 404)

        # El paciente 2 tampoco puede "adueñarse" de un documento suyo hacia otro paciente
        examen_2 = self.subir_examen('examen_paciente_2', paciente_id=paciente_1.id)
        self.assertEqual(Examen.objects.get(id=examen_2).paciente_id, paciente_2.id)
        self.client.patch(f'/api/v1/examenes/{examen_2}/', {'paciente': paciente_1.id}, format='multipart')
        self.assertEqual(Examen.objects.get(id=examen_2).paciente_id, paciente_2.id)

        # El clínico de esa clínica ve los documentos de ambos
        clinico = self.crear_clinico(paciente_1.clinica)
        self.autenticar(clinico.rut, 'Clinico123!')
        self.assertEqual(self.titulos_visibles(), {'examen_paciente_1', 'examen_paciente_2'})

    def test_clinico_asigna_documento_a_un_paciente_de_su_clinica(self):
        paciente_1 = self.registrar_paciente('100000001', 'a@test.cl')
        paciente_2 = self.registrar_en_misma_clinica(paciente_1, '100000002', 'b@test.cl')
        paciente_otra = self.registrar_paciente('100000003', 'c@test.cl', clinica_id=2)
        self.assertNotEqual(paciente_otra.clinica_id, paciente_1.clinica_id)

        # Un paciente no puede listar pacientes asignables
        self.autenticar(paciente_1.rut, 'Paciente01.')
        self.assertEqual(self.client.get('/api/v1/examenes/pacientes-asignables/').status_code, 403)

        clinico = self.crear_clinico(paciente_1.clinica)
        self.autenticar(clinico.rut, 'Clinico123!')

        # Solo aparecen los pacientes de su clínica
        respuesta = self.client.get('/api/v1/examenes/pacientes-asignables/')
        self.assertEqual({p['id'] for p in respuesta.data}, {paciente_1.id, paciente_2.id})

        # Asigna un documento al paciente 1
        examen_id = self.subir_examen('resultado_para_paciente_1', paciente_id=paciente_1.id)
        examen = Examen.objects.get(id=examen_id)
        self.assertEqual((examen.paciente_id, examen.clinico_id), (paciente_1.id, clinico.id))

        # No puede asignar a un paciente de otra clínica
        self.subir_examen('no_permitido', paciente_id=paciente_otra.id, estado_esperado=400)
        self.assertFalse(Examen.objects.filter(titulo='no_permitido').exists())

        # Solo el paciente 1 lo ve; el paciente 2 (misma clínica) no
        self.autenticar(paciente_1.rut, 'Paciente01.')
        self.assertEqual(self.titulos_visibles(), {'resultado_para_paciente_1'})
        self.autenticar(paciente_2.rut, 'Paciente01.')
        self.assertEqual(self.titulos_visibles(), set())
