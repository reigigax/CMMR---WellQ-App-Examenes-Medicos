"""Ejecutar desde la carpeta Aplicacion o desde exams_manager. Conserva formularios y JS."""
from pathlib import Path
import re, shutil

here=Path.cwd()
root=here if (here/'templates'/'exams_manager').exists() else here/'exams_manager'
if not (root/'templates'/'exams_manager').exists():
    raise SystemExit('ERROR: ejecuta desde la carpeta Aplicacion (donde esta exams_manager) o desde exams_manager.')
source=Path(__file__).resolve().parent/'static'/'css'/'wellq-fotos.css'
dest=root/'static'/'css'/'wellq-fotos.css'
dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copyfile(source,dest)
t=root/'templates'/'exams_manager'
css='\n<link rel="stylesheet" href="{% static \'css/wellq-fotos.css\' %}?v=20261104-2">\n'

banners={
'paciente.html':('paciente','Tus exámenes, siempre disponibles','Consulta y administra tu información médica desde un solo lugar.'),
'clinico.html':('clinico','Gestión de pacientes','Consulta y administra los documentos médicos de tus pacientes.'),
'upload.html':('upload','Tu información médica, organizada','Organiza tus exámenes médicos de forma simple y segura.'),
}
for name in ['login.html','sign_up.html','paciente.html','clinico.html','upload.html']:
    f=t/name
    if not f.exists():
        print('OMITIDO (no existe):',f);continue
    s=f.read_text(encoding='utf-8-sig')
    backup=f.with_suffix('.html.bak-wellq')
    if not backup.exists():backup.write_text(s,encoding='utf-8')
    # Quitar banners que se insertaron antes del layout, o banners antiguos creados por esta entrega.
    s=re.sub(r'<div\s+class="wellq-photo-banner[^\"]*"[^>]*>.*?</div>\s*</div>','',s,flags=re.S)
    if name in banners:
        # Eliminar banners ajenos SOLO si usan las clases especificas del intento anterior.
        s=re.sub(r'<div\s+class="wellq-banner(?:\s+wellq-banner--[^\"]+)?"[^>]*>.*?</div>\s*</div>','',s,flags=re.S)
        typ,title,desc=banners[name]
        banner=(f'\n<div class="wellq-photo-banner wellq-photo-banner--{typ}">\n'
                f'  <div class="wellq-photo-banner__text">\n'
                f'    <h2>{title}</h2>\n    <p>{desc}</p>\n'
                f'  </div>\n</div>\n')
        pattern=r'(<section\s+class="content-card[^\"]*"[^>]*>)'
        s,count=re.subn(pattern,lambda m:m.group(1)+banner,s,count=1)
        if not count:print('AVISO: no encontre content-card en',name)
    if 'wellq-fotos.css' not in s:
        # Cargar despues de los CSS existentes, para que tenga prioridad.
        matches=list(re.finditer(r'<link[^>]+rel="stylesheet"[^>]*>',s))
        if matches:
            pos=matches[-1].end();s=s[:pos]+css+s[pos:]
        else:
            s=s.replace('{% block content %}','{% block content %}'+css,1)
    f.write_text(s,encoding='utf-8')
    print('ACTUALIZADO:',f)
print('\nListo. Confirma que los 5 archivos .webp esten en',root/'static'/'img')
