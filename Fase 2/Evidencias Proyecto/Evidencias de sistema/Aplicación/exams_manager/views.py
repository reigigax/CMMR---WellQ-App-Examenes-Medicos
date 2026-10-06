from django.shortcuts import render

# Pagina base (el acceso definido aqui es solo para pruebas)
def base(request):
    return render(request, 'base.html')



# Pagina de Login
def login(request):
    return render(request, 'exams_manager/login.html')

# Pagina de Registro
def sign_up(request):
    return render(request, 'exams_manager/sign_up.html')

# Pagina de Subida de Examenes Medicos
def upload(request):
    return render(request, 'exams_manager/upload.html')

# Pagina de Colsulta y Visualizacion de Examenes Medicos
def home(request):
    return render(request, 'exams_manager/home.html')