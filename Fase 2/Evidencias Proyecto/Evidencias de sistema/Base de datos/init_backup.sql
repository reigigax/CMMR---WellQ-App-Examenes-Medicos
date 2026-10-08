--
-- Tablas de la base de datos generada
--

-- public.region definition
-- Drop table
-- DROP TABLE public.region;
create table public.region (
	id int2 generated always as identity( increment by 1 minvalue 1 maxvalue 32767 start 1 cache 1 no cycle) not null,
	nombre varchar(50) storage MAIN not null,
	numero bpchar(4) storage MAIN not null,
	constraint region_pk primary key (id)
);

-- public.comuna definition
-- Drop table
-- DROP TABLE public.comuna;
create table public.comuna (
	id int2 generated always as identity( increment by 1 minvalue 1 maxvalue 32767 start 1 cache 1 no cycle) not null,
	nombre varchar(40) storage MAIN not null,
	region_fk int2 not null,
	constraint comuna_pk primary key (id),
	constraint region_fk foreign key (region_fk) references public.region(id)
);

-- public.direccion definition
-- Drop table
-- DROP TABLE public.direccion;
create table public.direccion (
	id int4 generated always as identity( increment by 1 minvalue 1 maxvalue 2147483647 start 1 cache 1 no cycle) not null,
	calle varchar(75) storage MAIN not null,
	numero int2 null,
	comuna_fk int2 not null,
	constraint direccion_pk primary key (id),
	constraint comuna_fk foreign key (comuna_fk) references public.comuna(id)
);

-- public.paciente definition
-- Drop table
-- DROP TABLE public.paciente;
create table public.paciente (
	id int2 generated always as identity( increment by 1 minvalue 1 maxvalue 32767 start 1 cache 1 no cycle) not null,
	rut varchar(9) storage MAIN not null,
	nombres varchar(200) storage MAIN not null,
	apellidos varchar(250) storage MAIN not null,
	correo varchar(250) storage MAIN not null,
	celular int2 null,
	direccion_fk int4 not null,
	constraint paciente_pk primary key (id),
	constraint paciente_unique unique (rut),
	constraint paciente_unique_1 unique (correo),
	constraint direccion_fk foreign key (direccion_fk) references public.direccion(id)
);

-- public.clinica definition
-- Drop table
-- DROP TABLE public.clinica;
create table public.clinica (
	id int2 generated always as identity( increment by 1 minvalue 1 maxvalue 32767 start 1 cache 1 no cycle) not null,
	nombre varchar(75) storage MAIN not null,
	direccion_fk int4 not null,
	constraint clinica_pk primary key (id),
	constraint direccion_fk foreign key (direccion_fk) references public.direccion(id)
);

-- public.clinico definition
-- Drop table
-- DROP TABLE public.clinico;
create table public.clinico (
	id int2 generated always as identity( increment by 1 minvalue 1 maxvalue 32767 start 1 cache 1 no cycle) not null,
	rut varchar(9) storage MAIN not null,
	nombres varchar(200) storage MAIN not null,
	apellidos varchar(200) storage MAIN not null,
	correo varchar(250) storage MAIN not null,
	celular int2 null,
	clinica_fk int2 not null,
	direccion_fk int4 not null,
	constraint clinico_pk primary key (id),
	constraint clinico_unique unique (correo),
	constraint clinica_fk foreign key (clinica_fk) references public.clinica(id),
	constraint direccion_fk foreign key (direccion_fk) references public.direccion(id)
);

-- public.examen definition
-- Drop table
-- DROP TABLE public.examen;
create table public.examen (
	id int2 generated always as identity( increment by 1 minvalue 1 maxvalue 32767 start 1 cache 1 no cycle) not null,
	titulo varchar(150) storage MAIN not null,
	sesion varchar(150) storage MAIN not null,
	nota_clinica varchar(500) storage MAIN null,
	fecha_subido date not null,
	version_archivo int2 not null,
	paciente_fk int2 not null,
	clinico_fk int2 not null,
	constraint examen_pk primary key (id),
	constraint clinico_fk foreign key (clinico_fk) references public.clinico(id),
	constraint paciente_fk foreign key (paciente_fk) references public.paciente(id)
);


--
-- Insersion de datos a las tablas creadas -- (Solo actualmente a Comuna y Region) --
--

-- Datos de Tabla Region
INSERT INTO public.region (nombre,numero) VALUES
	 ('Arica y Parinacota','XV  '),
	 ('Tarapacá','I   '),
	 ('Antofagasta','II  '),
	 ('Atacama','III '),
	 ('Coquimbo','IV  '),
	 ('Valparaiso','V   '),
	 ('Region Metropolitana','RM  '),
	 ('Libertador General Bernardo OHiggins','VI  '),
	 ('Maule','VII '),
	 ('Ñuble','XVI ');
INSERT INTO public.region (nombre,numero) VALUES
	 ('BioBío','VIII'),
	 ('La Araucanía','IX  '),
	 ('Los Ríos','XIV '),
	 ('Los Lagos','X   '),
	 ('Aysén del General Carlos Ibáñez del Campo','XI  '),
	 ('Magallanes y Antartica Chilena','XII ');

-- Datos de tabla Comuna
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Calama',3),
	 ('María Elena',3),
	 ('Mejillones',3),
	 ('Ollagüe',3),
	 ('San Pedro de Atacama',3),
	 ('Sierra Gorda',3),
	 ('Taltal',3),
	 ('Tocopilla',3),
	 ('Antofagasta',3),
	 ('Camarones',1);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('General Lagos',1),
	 ('Putre',1),
	 ('Arica',1),
	 ('Alto del Carmen',4),
	 ('Caldera',4),
	 ('Chañaral',4),
	 ('Copiapó',4),
	 ('Diego de Almagro',4),
	 ('Freirina',4),
	 ('Huasco',4);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Tierra Amarilla',4),
	 ('Vallenar',4),
	 ('Aysén',15),
	 ('Chile Chico',15),
	 ('Cisnes',15),
	 ('Cochrane',15),
	 ('Coyhaique',15),
	 ('Guaitecas',15),
	 ('Lago Verde',15),
	 ('OHiggins',15);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Río Ibáñez',15),
	 ('Tortel',15),
	 ('Alto BioBío',11),
	 ('Antuco',11),
	 ('Arauco',11),
	 ('Cabrero',11),
	 ('Cañete',11),
	 ('Chiguayante',11),
	 ('Concepción',11),
	 ('Contulmo',11);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Coronel',11),
	 ('Curanilahue',11),
	 ('Florida',11),
	 ('Hualpén',11),
	 ('Hualqui',11),
	 ('Laja',11),
	 ('Lebu',11),
	 ('Los Álamos',11),
	 ('Los Ángeles',11),
	 ('Lota',11);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Mulchén',11),
	 ('Nacimiento',11),
	 ('Negrete',11),
	 ('Penco',11),
	 ('Quilaco',11),
	 ('Quilleco',11),
	 ('San Pedro de la Paz',11),
	 ('San Rosendo',11),
	 ('Santa Bárbara',11),
	 ('Santa Juana',11);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Talcahuano',11),
	 ('Tirúa',11),
	 ('Tomé',11),
	 ('Tucapel',11),
	 ('Yumbel',11),
	 ('Andacollo',5),
	 ('Canela',5),
	 ('Combarbalá',5),
	 ('Coquimbo',5),
	 ('Illapel',5);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('La Higuera',5),
	 ('La Serena',5),
	 ('Los Vilos',5),
	 ('Monte Patria',5),
	 ('Ovalle',5),
	 ('Paihuano',5),
	 ('Punitaqui',5),
	 ('Río Hurtado',5),
	 ('Salamanca',5),
	 ('Vicuña',5);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Angol',12),
	 ('Carahue',12),
	 ('Cholchol',12),
	 ('Collipulli',12),
	 ('Cunco',12),
	 ('Curacautín',12),
	 ('Curarrehue',12),
	 ('Ercilla',12),
	 ('Freire',12),
	 ('Galvarino',12);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Gorbea',12),
	 ('Lautaro',12),
	 ('Loncoche',12),
	 ('Lonquimay',12),
	 ('Los Sauces',12),
	 ('Lumaco',12),
	 ('Melipueco',12),
	 ('Nueva Imperial',12),
	 ('Padre Las Casas',12),
	 ('Perquenco',12);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Pitrufquén',12),
	 ('Pucón',12),
	 ('Purén',12),
	 ('Renaico',12),
	 ('Saavedra',12),
	 ('Temuco',12),
	 ('Teodoro Schmidt',12),
	 ('Toltén',12),
	 ('Traiguén',12),
	 ('Victoria',12);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Vilcún',12),
	 ('Villarica',12),
	 ('Chépica',8),
	 ('Chimbarongo',8),
	 ('Codehua',8),
	 ('Coinco',8),
	 ('Coltauco',8),
	 ('Doñihue',8),
	 ('Graneros',8),
	 ('La Estrella',8);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Las Cabras',8),
	 ('Litueche',8),
	 ('Lolol',8),
	 ('Machaí',8),
	 ('Malloa',8),
	 ('Marchigüe',8),
	 ('Mostazal',8),
	 ('Nancagua',8),
	 ('Navidad',8),
	 ('Olivar',8);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Palmilla',8),
	 ('Paredones',8),
	 ('Peralillo',8),
	 ('Peumo',8),
	 ('Pichidegua',8),
	 ('Pichilemu',8),
	 ('Placilla',8),
	 ('Pumanque',8),
	 ('Quinta de Tilcoco',8),
	 ('Rancagua',8);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Rengo',8),
	 ('Requinoa',8),
	 ('San Fernando',8),
	 ('San Vicente',8),
	 ('Santa Cruz',8),
	 ('Ancud',14),
	 ('Calbuco',14),
	 ('Castro',14),
	 ('Chaitén',14),
	 ('Chonchi',14);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Cochamó',14),
	 ('Curaco de Vélez',14),
	 ('Dalcahue',14),
	 ('Fresia',14),
	 ('Frutillar',14),
	 ('Futaleufú',14),
	 ('Hualaihué',14),
	 ('Llanquihue',14),
	 ('Los Muermos',14),
	 ('Maullín',14);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Osorno',14),
	 ('Palena',14),
	 ('Puerto Montt',14),
	 ('Puerto Octay',14),
	 ('Puerto Varas',14),
	 ('Puqueldón',14),
	 ('Purranque',14),
	 ('Puyehue',14),
	 ('Queilén',14),
	 ('Quellón',14);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Quemchi',14),
	 ('Quinchao',14),
	 ('Río Negro',14),
	 ('San Juan de la Costa',14),
	 ('San Pablo',14),
	 ('Corral',13),
	 ('Futrono',13),
	 ('La Unión',13),
	 ('Lago Ranco',13),
	 ('Lanco',13);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Los Lagos',13),
	 ('Máfil',13),
	 ('Mariquina',13),
	 ('Paillaco',13),
	 ('Panguipulli',13),
	 ('Río Bueno',13),
	 ('Valdivia',13),
	 ('Antártica',16),
	 ('Cabo de Hornos',16),
	 ('Laguna Blanca',16);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Natales',16),
	 ('Porvenir',16),
	 ('Primavera',16),
	 ('Punta Arenas',16),
	 ('Río Verde',16),
	 ('San Gregorio',16),
	 ('Timaukel',16),
	 ('Torres del Paine',16),
	 ('Cauquenes',9),
	 ('Chanco',9);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Colbún',9),
	 ('Constitución',9),
	 ('Curepto',9),
	 ('Curicó',9),
	 ('Empedrado',9),
	 ('Hualañé',9),
	 ('Licantén',9),
	 ('Linares',9),
	 ('Longaví',9),
	 ('Maule',9);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Molina',9),
	 ('Parral',9),
	 ('Pelarco',9),
	 ('Pelluhue',9),
	 ('Pencahue',9),
	 ('Rauco',9),
	 ('Retiro',9),
	 ('Río Claro',9),
	 ('Romeral',9),
	 ('Sagrada Familia',9);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('San Clemente',9),
	 ('San Javier',9),
	 ('San Rafael',9),
	 ('Talca',9),
	 ('Teno',9),
	 ('Vichuquén',9),
	 ('Villa Alegre ',9),
	 ('Yerbas Buenas',9),
	 ('Alhué',7),
	 ('Buin',7);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Calera de Tango',7),
	 ('Cerrillos',7),
	 ('Cerro Navia',7),
	 ('Colina',7),
	 ('Conchalí',7),
	 ('Curacaví',7),
	 ('El Bosque',7),
	 ('El Monte',7),
	 ('Estacion Central',7),
	 ('Huechuraba',7);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Independencia',7),
	 ('Isla de Maipo',7),
	 ('La Cisterna',7),
	 ('La Florida',7),
	 ('La Granja',7),
	 ('La Pintana',7),
	 ('La Reina',7),
	 ('Lampa',7),
	 ('Las Condes',7),
	 ('Lo Barnechea',7);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Lo Espejo',7),
	 ('Lo Prado',7),
	 ('Macul',7),
	 ('Maipú',7),
	 ('María Pinto',7),
	 ('Melipilla',7),
	 ('Ñuñoa',7),
	 ('Padre Hurtado',7),
	 ('Paine',7),
	 ('Pedro Aguirre Cerda',7);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Peñaflor',7),
	 ('Peñalolén',7),
	 ('Pirque',7),
	 ('Providencia',7),
	 ('Pudahuel',7),
	 ('Puente Alto',7),
	 ('Quilicura',7),
	 ('Quinta Normal',7),
	 ('Recoleta',7),
	 ('Renca',7);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('San Bernardo',7),
	 ('San Joaquín',7),
	 ('San José de Maipo',7),
	 ('San Miguel',7),
	 ('San Pedro',7),
	 ('San Ramón',7),
	 ('Santiago',7),
	 ('Talagante',7),
	 ('Til Til',7),
	 ('Vitacura',7);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Bulnes',10),
	 ('Chillán',10),
	 ('Chillán Viejo',10),
	 ('Cobquecura',10),
	 ('Coelemu',10),
	 ('Coihueco',10),
	 ('El Carmen',10),
	 ('Ñiquén',10),
	 ('Ninhue',10),
	 ('Pemuco',10);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Pinto',10),
	 ('Portezuelo',10),
	 ('Quillón',10),
	 ('Quirihue',10),
	 ('Ránquil',10),
	 ('San Carlos',10),
	 ('San Fabián',10),
	 ('San Ignacio',10),
	 ('San Nicolás',10),
	 ('Treguaco',10);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Yungay',10),
	 ('Alto Hospicio',2),
	 ('Camiña',2),
	 ('Colchane',2),
	 ('Huara',2),
	 ('Iquique',2),
	 ('Pica',2),
	 ('Pozo Almonte',2),
	 ('Algarrobo',6),
	 ('Cabildo',6);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Calle Larga',6),
	 ('Cartagena',6),
	 ('Casablanca',6),
	 ('Catemu',6),
	 ('Concón',6),
	 ('El Quisco',6),
	 ('El Tabo',6),
	 ('Hijuelas',6),
	 ('Isla de Pascua',6),
	 ('Juan Fernández',6);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('La Calera',6),
	 ('La Cruz',6),
	 ('La Ligua',6),
	 ('Limache',6),
	 ('Llay-Llay',6),
	 ('Los Andes',6),
	 ('Nogales',6),
	 ('Olmué',6),
	 ('Panquehue',6),
	 ('Papudo',6);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Petorca',6),
	 ('Puchancaví',6),
	 ('Putaendo',6),
	 ('Quillota',6),
	 ('Quilpué',6),
	 ('Quintero',6),
	 ('Rinconada',6),
	 ('San Antonio',6),
	 ('San Esteban',6),
	 ('San Felipe',6);
INSERT INTO public.comuna (nombre,region_fk) VALUES
	 ('Santa María',6),
	 ('Santo Domingo',6),
	 ('Valparaíso',6),
	 ('Villa Alemana',6),
	 ('Viña del Mar',6),
	 ('Zapallar',6);
