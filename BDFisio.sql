`fisiosalud-2`-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para fisiosalud-2
CREATE DATABASE IF NOT EXISTS `fisiosalud-2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `fisiosalud-2`;

-- Volcando estructura para tabla fisiosalud-2.acudiente
CREATE TABLE IF NOT EXISTS `acudiente` (
  `ID_acudiente` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_completo` varchar(255) NOT NULL,
  `telefono` varchar(255) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `ID_cita` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_acudiente`),
  KEY `ID_cita` (`ID_cita`),
  CONSTRAINT `acudiente_ibfk_4` FOREIGN KEY (`ID_cita`) REFERENCES `citas` (`cita_id`),
  CONSTRAINT `acudiente_ibfk_5` FOREIGN KEY (`ID_cita`) REFERENCES `citas` (`cita_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.acudiente: ~0 rows (aproximadamente)

-- Volcando estructura para tabla fisiosalud-2.administrador
CREATE TABLE IF NOT EXISTS `administrador` (
  `Codigo/ID` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `Contraseña` varchar(255) NOT NULL,
  `Correo_electronico` varchar(255) NOT NULL,
  PRIMARY KEY (`Codigo/ID`)
) ENGINE=InnoDB AUTO_INCREMENT=101235 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.administrador: ~0 rows (aproximadamente)
INSERT INTO `administrador` (`Codigo/ID`, `nombre`, `Contraseña`, `Correo_electronico`) VALUES
	(101234, 'Mario Corredor ', '1', 'mariocorredor_11@fisio.correo.gmail.com');

-- Volcando estructura para tabla fisiosalud-2.autorizaciones_medicas
CREATE TABLE IF NOT EXISTS `autorizaciones_medicas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo_autorizacion` varchar(50) DEFAULT NULL,
  `id_paciente` int(11) DEFAULT NULL,
  `nombre_paciente` varchar(100) DEFAULT NULL,
  `correo_paciente` varchar(100) DEFAULT NULL,
  `telefono_paciente` varchar(20) DEFAULT NULL,
  `servicio_solicitado` varchar(100) DEFAULT NULL,
  `tratamiento_especifico` varchar(200) DEFAULT NULL,
  `diagnostico` text DEFAULT NULL,
  `notas_adicionales` text DEFAULT NULL,
  `pdf_original_url` varchar(500) DEFAULT NULL,
  `pdf_fusionado_url` varchar(500) DEFAULT NULL,
  `estado` enum('pendiente','revisando','aprobado','rechazado','expirado') DEFAULT 'pendiente',
  `codigo_temporal` varchar(50) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_aprobacion` datetime DEFAULT NULL,
  `fecha_expiracion` datetime DEFAULT NULL,
  `id_admin_revisor` int(11) DEFAULT NULL,
  `notas_revisor` text DEFAULT NULL,
  `utilizado` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo_autorizacion` (`codigo_autorizacion`),
  UNIQUE KEY `codigo_temporal` (`codigo_temporal`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.autorizaciones_medicas: ~0 rows (aproximadamente)

-- Volcando estructura para tabla fisiosalud-2.cancelaciones_citas
CREATE TABLE IF NOT EXISTS `cancelaciones_citas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cita_id` varchar(50) NOT NULL,
  `terapeuta` varchar(100) NOT NULL,
  `paciente` varchar(100) NOT NULL,
  `servicio` varchar(100) NOT NULL,
  `fecha_programada` date NOT NULL,
  `hora_programada` time NOT NULL,
  `motivo_cancelacion` enum('solapamiento','razon_peso','finalizacion_terapia') NOT NULL,
  `detalles_adicionales` text DEFAULT NULL,
  `fecha_cancelacion` datetime DEFAULT current_timestamp(),
  `email_enviado` tinyint(1) DEFAULT 0,
  `paciente_id_relacionado` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_cita_id` (`cita_id`),
  KEY `idx_fecha_cancelacion` (`fecha_cancelacion`),
  KEY `idx_motivo` (`motivo_cancelacion`),
  KEY `idx_paciente_id` (`paciente_id_relacionado`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.cancelaciones_citas: ~0 rows (aproximadamente)
INSERT INTO `cancelaciones_citas` (`id`, `cita_id`, `terapeuta`, `paciente`, `servicio`, `fecha_programada`, `hora_programada`, `motivo_cancelacion`, `detalles_adicionales`, `fecha_cancelacion`, `email_enviado`, `paciente_id_relacionado`) VALUES
	(3, 'FS-0001', 'Laura Fernández', 'Miguel Gutierrez', 'Masaje Relajante', '2025-12-18', '17:00:00', 'finalizacion_terapia', '', '2025-12-05 05:17:33', 0, NULL),
	(4, 'FS-0001', 'Laura Fernández', 'Miguel Angel Gutierrez Lopez', 'Masaje Relajante', '2025-12-12', '09:30:00', 'finalizacion_terapia', '', '2025-12-05 05:27:41', 0, NULL),
	(5, 'FS-0002', 'Laura Fernández', 'Paula Garcia Perez', 'Masaje Relajante', '2025-12-24', '12:00:00', 'solapamiento', '', '2025-12-05 05:40:37', 0, NULL),
	(6, 'FS-0001', 'Laura Fernández', 'Pepe Garcia', 'Masaje Relajante', '2025-12-19', '15:00:00', 'razon_peso', 'Me mori', '2025-12-05 05:40:59', 0, NULL);

-- Volcando estructura para tabla fisiosalud-2.carrito
CREATE TABLE IF NOT EXISTS `carrito` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `producto_id` varchar(50) NOT NULL,
  `producto_tipo` enum('nutricion','implemento') NOT NULL,
  `cantidad` int(11) NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_usuario_producto_tipo` (`usuario_id`,`producto_id`,`producto_tipo`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.carrito: ~0 rows (aproximadamente)

-- Volcando estructura para tabla fisiosalud-2.cita
CREATE TABLE IF NOT EXISTS `cita` (
  `cita_id` varchar(50) NOT NULL,
  `nombre_paciente` varchar(255) NOT NULL,
  `servicio` varchar(255) NOT NULL,
  `terapeuta_designado` varchar(255) NOT NULL,
  `telefono` varchar(255) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `fecha_cita` date NOT NULL,
  `hora_cita` time NOT NULL,
  `notas_adicionales` text DEFAULT NULL,
  `tipo_pago` varchar(255) NOT NULL,
  `estado` varchar(255) NOT NULL,
  PRIMARY KEY (`cita_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.cita: ~0 rows (aproximadamente)

-- Volcando estructura para tabla fisiosalud-2.compras_confirmadas
CREATE TABLE IF NOT EXISTS `compras_confirmadas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `orden_id` varchar(255) NOT NULL,
  `fecha_compra` datetime NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` enum('pendiente','confirmada','enviada','entregada') DEFAULT 'confirmada',
  `direccion_envio` text NOT NULL,
  `ciudad` varchar(255) NOT NULL,
  `codigo_postal` varchar(20) NOT NULL,
  `metodo_pago` varchar(255) NOT NULL,
  `producto_id` varchar(50) NOT NULL,
  `producto_tipo` enum('nutricion','implemento') NOT NULL,
  `producto_nombre` varchar(255) NOT NULL,
  `cantidad_total` int(11) NOT NULL,
  `items_detalle` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`items_detalle`)),
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `orden_id` (`orden_id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `fecha_compra` (`fecha_compra`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.compras_confirmadas: ~2 rows (aproximadamente)
INSERT INTO `compras_confirmadas` (`id`, `usuario_id`, `orden_id`, `fecha_compra`, `total`, `estado`, `direccion_envio`, `ciudad`, `codigo_postal`, `metodo_pago`, `producto_id`, `producto_tipo`, `producto_nombre`, `cantidad_total`, `items_detalle`, `creado_en`) VALUES
	(1, 1112390178, 'ORD9DE3FFB7E653', '2025-12-03 22:22:27', 205000.00, 'confirmada', 'calle 45 #2130, buga, CP: 123', 'buga', '123', 'debit', 'BD1245', 'nutricion', 'Multivitamínico Completo', 3, '[{"producto_id": "BD1245", "producto_tipo": "nutricion", "nombre": "Multivitam\\u00ednico Completo", "descripcion": "Complejo vitam\\u00ednico y mineral de origen org\\u00e1nico para fortalecer el sistema inmunol\\u00f3gico y optimizar funciones metab\\u00f3licas.", "precio_unitario": 45000.0, "cantidad": 1, "subtotal": 45000.0}, {"producto_id": "AC3311", "producto_tipo": "nutricion", "nombre": "Prote\\u00edna en Polvo", "descripcion": "Prote\\u00edna de suero de leche de alta calidad para recuperaci\\u00f3n muscular y desarrollo de masa magra con m\\u00e1xima biodisponibilidad.", "precio_unitario": 85000.0, "cantidad": 1, "subtotal": 85000.0}, {"producto_id": "BIN8824", "producto_tipo": "nutricion", "nombre": "Batido Nutricional Completo", "descripcion": "Reemplazo de comida completo con balance perfecto de macronutrientes para control de peso y nutrici\\u00f3n optimizada.", "precio_unitario": 75000.0, "cantidad": 1, "subtotal": 75000.0}]', '2025-12-04 03:22:27'),
	(2, 1112148132, 'ORDCA25756E3E21', '2025-12-04 03:11:48', 75000.00, 'confirmada', 'Calle 15 #4-14, Buga, CP: 123', 'Buga', '123', 'transfer', 'BP5572', 'nutricion', 'Barritas Proteicas', 4, '[{"producto_id": "BP5572", "producto_tipo": "nutricion", "nombre": "Barritas Proteicas", "descripcion": "Snack saludable alto en prote\\u00edna y fibra, perfecto para entre comidas, post-entreno o como complemento nutricional.", "precio_unitario": 25000.0, "cantidad": 3, "subtotal": 75000.0}, {"producto_id": "5903LK", "producto_tipo": "", "nombre": null, "descripcion": null, "precio_unitario": 0, "cantidad": 1, "subtotal": 0}]', '2025-12-04 08:11:48');

-- Volcando estructura para tabla fisiosalud-2.ejercicios
CREATE TABLE IF NOT EXISTS `ejercicios` (
  `codigo_ejercicio` int(11) NOT NULL,
  `nombre_ejercicio` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `duracion (minutos)` int(11) DEFAULT NULL,
  `intensidad` varchar(255) DEFAULT NULL,
  `equipamento` varchar(255) DEFAULT NULL,
  `instrucciones_detalladas` text DEFAULT NULL,
  `precauciones` text DEFAULT NULL,
  `beneficios` text DEFAULT NULL,
  `contraindicaciones` text DEFAULT NULL,
  `repeticiones` int(11) DEFAULT NULL,
  `series` int(11) DEFAULT NULL,
  `frecuencia_semanal` int(11) DEFAULT NULL,
  `nivel_dificultad` varchar(255) DEFAULT NULL,
  `zona_corporal` varchar(255) DEFAULT NULL,
  `tipo_ejercicio` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`codigo_ejercicio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.ejercicios: ~30 rows (aproximadamente)
INSERT INTO `ejercicios` (`codigo_ejercicio`, `nombre_ejercicio`, `descripcion`, `duracion (minutos)`, `intensidad`, `equipamento`, `instrucciones_detalladas`, `precauciones`, `beneficios`, `contraindicaciones`, `repeticiones`, `series`, `frecuencia_semanal`, `nivel_dificultad`, `zona_corporal`, `tipo_ejercicio`, `created_at`, `updated_at`) VALUES
	(1001, 'Deslizamientos Superficiales', 'Técnica de masaje con movimientos largos y fluidos para calentar el tejido muscular y promover la circulación sanguínea.', 15, 'Baja', 'Aceites esenciales, camilla de masaje', '1. Aplicar aceite en manos 2. Realizar movimientos largos desde extremidades hacia el corazón 3. Mantener presión constante y suave 4. Repetir en todas las zonas del cuerpo', 'Evitar áreas con heridas o inflamación. No aplicar presión excesiva.', 'Mejora circulación sanguínea, Relajación muscular, Reducción de estrés', 'Fiebre, enfermedades de piel, trombosis', 10, 3, 2, 'Básico', 'Todo el cuerpo', 'Técnica de masaje', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1002, 'Amasamiento Circular', 'Técnica de masaje que consiste en presiones circulares para liberar tensión muscular superficial.', 10, 'Baja', 'Aceites esenciales, camilla de masaje', '1. Colocar palmas sobre músculo 2. Realizar movimientos circulares con presión moderada 3. Trabajar cada grupo muscular por 2-3 minutos 4. Combinar con respiraciones profundas', 'No aplicar sobre huesos o articulaciones. Detener si hay dolor agudo.', 'Liberación de tensión, Mejora de flexibilidad, Promueve relajación profunda', 'Lesiones recientes, osteoporosis severa', 15, 2, 2, 'Básico', 'Espalda, cuello, hombros', 'Técnica de masaje', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1003, 'Estiramiento de Cadena Posterior', 'Estiramiento completo de la cadena muscular posterior para mejorar flexibilidad y postura.', 8, 'Moderada', 'Colchoneta, banda elástica (opcional)', '1. Sentado con piernas extendidas 2. Flexionar tronco hacia adelante 3. Mantener espalda recta 4. Sostener 30 segundos 5. Repetir 3 veces', 'No rebotar. Detener si hay dolor agudo en espalda.', 'Mejora flexibilidad, Alivia tensión lumbar, Corrige postura', 'Hernia discal aguda, ciática severa', 3, 3, 3, 'Básico', 'Espalda baja, isquiotibiales, gemelos', 'Estiramiento estático', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1004, 'Rotaciones de Hombros', 'Ejercicio para movilidad articular y liberación de tensión en hombros y cuello.', 5, 'Baja', 'Ninguno', '1. Sentado o de pie con espalda recta 2. Elevar hombros hacia orejas 3. Rotar hombros hacia atrás en círculo 4. Realizar 10 repeticiones lentas 5. Cambiar dirección', 'Movimientos lentos y controlados. Evitar si hay lesión de hombro.', 'Mejora movilidad articular, Alivia tensión cervical, Prevención de lesiones', 'Luxación reciente de hombro', 10, 3, 5, 'Básico', 'Hombros, cuello, trapecio', 'Movilidad articular', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1005, 'Estiramiento de Pectoral en Puerta', 'Estiramiento para abrir pecho y corregir postura cifótica por sedentarismo.', 6, 'Moderada', 'Marco de puerta', '1. Parado en marco de puerta 2. Colocar antebrazos en jambas 3. Dar un paso adelante suavemente 4. Sentir estiramiento en pecho 5. Mantener 30 segundos', 'No forzar más allá de tensión moderada. Mantener espalda neutral.', 'Corrección postural, Alivia tensión pectoral, Mejora respiración', 'Dolor agudo en hombros', 3, 3, 4, 'Básico', 'Pectorales, hombros anteriores', 'Estiramiento estático', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1006, 'Sentadilla con Peso Corporal', 'Ejercicio fundamental para fortalecimiento de piernas y reeducación de movimiento tras lesión.', 10, 'Moderada', 'Ninguno o silla para apoyo', '1. Pies al ancho de hombros 2. Flexionar rodillas como si fuera a sentarse 3. Bajar hasta paralelo 4. Mantener espalda recta 5. Subir lentamente', 'No dejar que rodillas pasen puntas de pies. Comenzar sin peso.', 'Fortalecimiento cuadriceps, Mejora estabilidad, Prevención lesiones', 'Lesión de rodilla reciente, dolor agudo', 12, 3, 3, 'Intermedio', 'Piernas, glúteos, core', 'Fortalecimiento', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1007, 'Puente de Glúteos', 'Ejercicio para fortalecimiento de glúteos y estabilización de cadera post-lesión.', 8, 'Moderada', 'Colchoneta', '1. Acostado boca arriba con rodillas flexionadas 2. Elevar cadera hasta alineación hombros-rodillas 3. Contraer glúteos en posición alta 4. Bajar lentamente', 'Evitar arquear espalda baja excesivamente. Movimiento controlado.', 'Fortalecimiento glúteos, Estabilidad de cadera, Alivia dolor lumbar', 'Dolor agudo en espalda baja', 15, 3, 4, 'Intermedio', 'Glúteos, isquiotibiales, espalda baja', 'Fortalecimiento', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1008, 'Ejercicio de Propiocepción con Bosu', 'Ejercicio para mejorar equilibrio y propiocepción tras esguince de tobillo.', 12, 'Moderada', 'Bosu o superficie inestable', '1. Pararse sobre bosu con apoyo inicial 2. Mantener equilibrio 30 segundos 3. Progresar a ojos cerrados 4. Realizar movimientos suaves de cadera', 'Usar apoyo inicial si es necesario. Progresar gradualmente.', 'Mejora equilibrio, Recuperación esguinces, Prevención recaídas', 'Esguince grado III sin inmovilización adecuada', 3, 3, 5, 'Intermedio', 'Tobillos, piernas, core', 'Propiocepción', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1009, 'Caminata con Técnica Correcta', 'Reeducación de la marcha para corregir patrones de movimiento post-lesión.', 15, 'Baja', 'Pasillo despejado, espejo (opcional)', '1. Caminar lentamente 2. Prestar atención a: talón-punta, balanceo de brazos 3. Mantener postura erguida 4. Incrementar velocidad gradualmente', 'Comenzar distancias cortas. Detener si aparece cojera.', 'Reeducación de marcha, Mejora patrones movimiento, Prevención compensaciones', 'Fractura sin consolidación completa', 1, 5, 5, 'Intermedio', 'Todo el cuerpo', 'Reeducación motora', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1010, 'Movilizaciones Pasivas Asistidas', 'Ejercicios asistidos para recuperar rango de movimiento tras cirugía ortopédica.', 20, 'Baja', 'Asistencia de terapeuta, tablero de movilidad', '1. Terapeuta moviliza articulación pasivamente 2. Llevar hasta límite sin dolor 3. Mantener posición 10 segundos 4. Repetir en todos planos de movimiento', 'Solo con supervisión profesional. No forzar más allá de dolor tolerable.', 'Mantiene rango articular, Previene rigidez, Mejora circulación post-quirúrgica', 'Infección activa en zona quirúrgica, sangrado activo', 10, 3, 7, 'Avanzado', 'Área quirúrgica específica', 'Movilización pasiva', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1011, 'Ejercicios Isométricos Tempranos', 'Contracciones musculares sin movimiento articular para activación post-quirúrgica.', 15, 'Baja', 'Ninguno', '1. Contraer músculo objetivo sin mover articulación 2. Mantener contracción 5-10 segundos 3. Relajar completamente 4. Repetir secuencia', 'No realizar si hay dolor agudo. Comenzar con intensidad muy baja.', 'Activa circulación, Mantiene tono muscular, Reduce atrofia post-quirúrgica', 'Trombosis venosa profunda', 10, 3, 6, 'Avanzado', 'Grupo muscular cercano a cirugía', 'Isométrico', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1012, 'Ejercicios de Escalera de Movilidad', 'Progresión sistemática para recuperar rango completo de movimiento articular.', 25, 'Moderada', 'Tablero de medición, marcadores', '1. Medir rango inicial 2. Establecer meta de sesión 3. Trabajar hasta meta sin dolor 4. Registrar progreso 5. Incrementar meta gradualmente', 'Progresión lenta y constante. No avanzar si hay inflamación.', 'Recuperación rango articular, Medición objetiva progreso, Motivación paciente', 'Inestabilidad articular post-quirúrgica', 5, 4, 7, 'Avanzado', 'Articulación operada', 'Movilidad progresiva', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1013, 'Estiramientos Post-Punción', 'Estiramientos específicos para potenciar efectos de punción seca y prevenir recurrencia.', 10, 'Baja', 'Ninguno', '1. Después de punción seca 2. Realizar estiramiento suave del músculo tratado 3. Mantener 30-60 segundos 4. Repetir 2-3 veces 5. Combinar con respiraciones', 'Esperar 1 hora post-procedimiento. Estirar suavemente sin dolor.', 'Potencia efecto punción, Previene re-activación puntos gatillo, Mantiene longitud muscular', 'Sangrado o hematoma en zona punción', 3, 3, 3, 'Intermedio', 'Músculo tratado con punción', 'Estiramiento terapéutico', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1014, 'Ejercicios con Vendaje Activo', 'Movimientos específicos para potenciar efecto del vendaje neuromuscular.', 12, 'Baja', 'Vendaje neuromuscular aplicado', '1. Con vendaje aplicado 2. Realizar movimientos que el vendaje facilita 3. Enfocarse en rango completo 4. Mantener conciencia de postura 5. No exceder límites del dolor', 'No forzar movimiento más allá de lo natural. Respetar tiempo de uso del vendaje.', 'Potencia efecto vendaje, Mejora patrones movimiento, Educa al paciente', 'Reacción alérgica al adhesivo', 15, 3, 4, 'Intermedio', 'Zona vendada', 'Movimiento asistido', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1015, 'Activación Muscular con Feedback Táctil', 'Uso del vendaje como feedback para activación muscular correcta.', 8, 'Baja', 'Vendaje neuromuscular', '1. Vendaje aplicado con técnica de facilitación 2. Concentrarse en sensación del vendaje 3. Activar músculo suavemente 4. Sentir "tirón" del vendaje 5. Relajar y repetir', 'No activar bruscamente. Enfocarse en calidad del movimiento.', 'Mejora conexión mente-músculo, Corrige activación muscular, Potencia rehabilitación', 'Dolor cutáneo por vendaje', 10, 3, 5, 'Intermedio', 'Músculo con vendaje de facilitación', 'Activación neuromuscular', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1016, 'Auto-Liberación con Rodillo', 'Técnica de auto-liberación miofascial usando rodillo de espuma.', 15, 'Moderada', 'Rodillo de espuma', '1. Posicionar rodillo bajo área tensa 2. Usar peso corporal para presión 3. Rodar lentamente 4. Detener en puntos sensibles 5. Mantener 30-60 segundos en puntos gatillo', 'No rodar sobre huesos o articulaciones. Evitar columna lumbar.', 'Libera adherencias, Reduce dolor, Mejora movilidad', 'Hernia discal aguda, osteoporosis severa', 5, 2, 4, 'Intermedio', 'Músculos con restricción fascial', 'Auto-liberación', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1017, 'Liberación con Pelota de Tenis', 'Técnica específica para puntos gatillo profundos usando pelota de tenis.', 12, 'Moderada', 'Pelota de tenis o lacrosse', '1. Colocar pelota en punto gatillo 2. Aplicar presión gradual 3. Realizar movimientos pequeños 4. Respirar profundamente 5. Mantener hasta liberación', 'No aplicar sobre nervios superficiales. Detener si hay dolor irradiado.', 'Desactiva puntos gatillo, Alivia dolor referido, Restaura función muscular', 'Problemas circulatorios en área', 8, 2, 3, 'Intermedio', 'Puntos gatillo específicos', 'Liberación puntual', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1018, 'Estiramiento Fascial Dinámico', 'Combinación de liberación y estiramiento para sistema fascial.', 10, 'Moderada', 'Rodillo de espuma', '1. Liberar con rodillo 2. Seguir inmediatamente con estiramiento estático 3. Mantener estiramiento 30 segundos 4. Repetir secuencia 2-3 veces', 'No estirar bruscamente después de liberación. Progresar gradualmente.', 'Mejora elasticidad fascial, Potencia efectos liberación, Mantiene resultados', 'Lesión aguda sin evaluación', 3, 3, 4, 'Intermedio', 'Cadenas fasciales completas', 'Liberación-estiramiento', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1019, 'Compresión Isquémica', 'Técnica para desactivar puntos gatillo mediante presión sostenida.', 8, 'Moderada', 'Dedos pulgares, herramientas de presión', '1. Localizar punto gatillo 2. Aplicar presión gradual 3. Mantener hasta disminución sensibilidad 4. Incrementar presión progresivamente', 'No aplicar sobre nervios. Detener si hay adormecimiento o hormigueo.', 'Desactiva puntos gatillo, Reduce dolor local, Restaura función muscular', 'Problemas de coagulación, área inflamada', 5, 3, 2, 'Intermedio', 'Puntos gatillo musculares', 'Técnica de presión', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1020, 'Fricción Transversa Profunda', 'Técnica para liberar adherencias en tendones y ligamentos.', 10, 'Moderada', 'Dedos, herramienta de fricción', '1. Identificar área de adhesión 2. Aplicar fricción perpendicular a fibras 3. Movimiento corto y profundo 4. Continuar 5-10 minutos', 'No aplicar sobre heridas. Usar lubricante para evitar fricción cutánea.', 'Rompe adherencias, Mejora cicatrización, Restaura deslizamiento tisular', 'Infección local, herida abierta', 1, 3, 2, 'Intermedio', 'Tendones, ligamentos', 'Técnica de fricción', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1021, 'Masaje con Movilización Articular', 'Combinación de masaje y movilización para contracturas articulares.', 15, 'Moderada', 'Mesa de masaje', '1. Aplicar técnicas de masaje 2. Mientras relaja tejido, movilizar articulación 3. Trabajar rango completo de movimiento 4. Repetir secuencia', 'No movilizar más allá de límites articulares. Respetar dolor del paciente.', 'Libera contracturas, Mejora movilidad articular, Tratamiento integral', 'Inestabilidad articular, fractura reciente', 10, 3, 2, 'Intermedio', 'Articulaciones con restricción', 'Masaje-movilización', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1022, 'Balanceo del Sacro', 'Técnica suave para liberar restricciones en sistema craneosacral.', 12, 'Muy baja', 'Mesa de terapia', '1. Manos en sacro del paciente 2. Seguir movimiento natural 3. Asistir suavemente balanceo 4. Mantener hasta sentir liberación', 'Presión mínima. Paciente debe estar completamente relajado.', 'Equilibra sistema craneosacral, Alivia dolor lumbar, Relajación profunda', 'Trauma craneal reciente, presión intracraneal elevada', 1, 1, 2, 'Avanzado', 'Sacro, pelvis', 'Técnica manual suave', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1023, 'Descompresión de Sutura Craneal', 'Técnica para liberar restricciones en suturas craneales.', 10, 'Muy baja', 'Mesa de terapia', '1. Manos a los lados de cabeza 2. Contacto suave en suturas 3. Seguir movimiento de huesos craneales 4. Asistir descompresión natural', 'Presión casi imperceptible. Paciente debe estar cómodo.', 'Alivia cefaleas tensionales, Mejora circulación craneal, Equilibra presión intracraneal', 'Fractura craneal, cirugía craneal reciente', 1, 1, 2, 'Avanzado', 'Cráneo, suturas craneales', 'Técnica craneal', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1024, 'Bombeo de Ganglios', 'Técnica para estimular ganglios linfáticos y facilitar drenaje.', 8, 'Muy baja', 'Mesa de terapia, aceite ligero', '1. Localizar grupo ganglionar 2. Movimientos circulares muy suaves 3. Presión mínima 4. Dirección hacia centro del cuerpo', 'Presión extremadamente suave. No masajear ganglios inflamados.', 'Estimula sistema linfático, Reduce edema, Fortalece inmunidad', 'Infección activa, cáncer activo en área', 10, 2, 3, 'Intermedio', 'Ganglios linfáticos', 'Técnica de drenaje', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1025, 'Movimientos de Reabsorción', 'Técnica para mover líquido desde tejidos hacia vasos linfáticos.', 10, 'Muy baja', 'Mesa de terapia', '1. Manos planas sobre área edematosa 2. Movimientos suaves en dirección de drenaje 3. Presión mínima constante 4. Ritmo lento y rítmico', 'No causar enrojecimiento de piel. Movimientos muy lentos.', 'Reduce edema, Mejora circulación linfática, Elimina toxinas', 'Trombosis venosa profunda', 15, 2, 3, 'Intermedio', 'Áreas con edema', 'Técnica de drenaje', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1026, 'Ejercicio con EMS', 'Ejercicio de activación muscular asistida por electroterapia.', 15, 'Moderada', 'Equipo TENS/EMS, electrodos', '1. Colocar electrodos según protocolo 2. Iniciar estimulación suave 3. Realizar contracción voluntaria simultánea 4. Progresar intensidad gradualmente', 'No exceder intensidad tolerada. Seguir protocolo específico.', 'Re-educación muscular, Previene atrofia, Potencia recuperación', 'Marcapasos, embarazo, epilepsia', 10, 3, 4, 'Intermedio', 'Músculos específicos según protocolo', 'Electro-estimulación', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1027, 'Movilización con TENS', 'Movilización articular con apoyo de TENS para manejo del dolor.', 12, 'Baja', 'Equipo TENS, electrodos', '1. Aplicar TENS en área dolorosa 2. Iniciar movilización suave 3. Ajustar parámetros según tolerancia 4. Combinar con ejercicios de rango', 'No movilizar articulación inflamada agudamente. Supervisión profesional.', 'Permite movilización con menos dolor, Acelera rehabilitación, Control de dolor durante terapia', 'Área con herida abierta, infección local', 8, 3, 4, 'Intermedio', 'Articulaciones dolorosas', 'Electro-movilización', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1028, 'Saltos en Caja Controlados', 'Ejercicio pliométrico controlado para recuperación de potencia tras lesión.', 10, 'Alta', 'Caja pliométrica (altura baja)', '1. Comenzar con altura mínima 2. Salto controlado sobre caja 3. Aterrizaje silencioso y suave 4. Descenso controlado 5. Progresar altura gradualmente', 'No realizar en fase aguda. Aterrizaje perfecto es esencial.', 'Recupera potencia muscular, Mejora control neuromuscular, Prepara para deporte', 'Lesión aguda de rodilla/tobillo, dolor durante salto', 8, 3, 3, 'Avanzado', 'Piernas, glúteos, core', 'Pliometría controlada', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1029, 'Ejercicios en Cadena Cinética Cerrada', 'Ejercicios seguros post-quirúrgicos que involucran múltiples articulaciones.', 20, 'Moderada', 'Silla, pared para apoyo', '1. Comenzar con apoyo total 2. Realizar sentadillas parciales 3. Progresar a lunges estáticos 4. Mantener alineación correcta', 'No avanzar sin aprobación profesional. Priorizar calidad sobre cantidad.', 'Reintegra funcionalidad, Trabaja múltiples articulaciones, Simula actividades diarias', 'Inestabilidad articular post-quirúrgica', 12, 3, 4, 'Avanzado', 'Extremidad inferior o superior', 'Funcional', '2025-12-01 17:15:01', '2025-12-01 17:15:01'),
	(1030, 'Liberación con Herramienta de Ganzúa', 'Técnica específica con herramienta para liberaciones profundas.', 15, 'Moderada-Alta', 'Herramienta de liberación (ganzúa)', '1. Identificar banda tensa 2. Aplicar herramienta perpendicularmente 3. Deslizar a lo largo de banda 4. Repetir hasta sentir liberación', 'No usar sobre venas varicosas. Evitar áreas con poca grasa subcutánea.', 'Liberación profunda, Efectivo en tejido denso, Ahorra esfuerzo terapeuta', 'Piel delgada o frágil, moretones frecuentes', 5, 2, 2, 'Intermedio', 'Fascia profunda', 'Liberación instrumental', '2025-12-01 17:15:01', '2025-12-01 17:15:01');

-- Volcando estructura para tabla fisiosalud-2.ejercicios_completados
CREATE TABLE IF NOT EXISTS `ejercicios_completados` (
  `id` int(11) NOT NULL,
  `ID_usuario` int(11) NOT NULL,
  `codigo_ejercicio` int(11) NOT NULL,
  `fecha_completado` date DEFAULT NULL,
  `feedback` text DEFAULT NULL,
  `nivel_dificultad` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_ejercicio_usuario` (`ID_usuario`,`codigo_ejercicio`),
  KEY `codigo_ejercicio` (`codigo_ejercicio`),
  CONSTRAINT `codigo_ejercicio` FOREIGN KEY (`codigo_ejercicio`) REFERENCES `ejercicios` (`codigo_ejercicio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.ejercicios_completados: ~0 rows (aproximadamente)
INSERT INTO `ejercicios_completados` (`id`, `ID_usuario`, `codigo_ejercicio`, `fecha_completado`, `feedback`, `nivel_dificultad`, `created_at`) VALUES
	(0, 1112390178, 1002, '2025-12-02', 'Lol', 'facil', NULL);

-- Volcando estructura para tabla fisiosalud-2.logs_solicitudes
CREATE TABLE IF NOT EXISTS `logs_solicitudes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_solicitud` int(11) DEFAULT NULL,
  `id_admin` int(11) DEFAULT NULL,
  `accion` varchar(50) DEFAULT NULL,
  `mensaje` text DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `id_solicitud` (`id_solicitud`),
  KEY `id_admin` (`id_admin`),
  CONSTRAINT `logs_solicitudes_ibfk_1` FOREIGN KEY (`id_solicitud`) REFERENCES `autorizaciones_medicas` (`id`),
  CONSTRAINT `logs_solicitudes_ibfk_2` FOREIGN KEY (`id_admin`) REFERENCES `administrador` (`Codigo/ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.logs_solicitudes: ~0 rows (aproximadamente)

-- Volcando estructura para tabla fisiosalud-2.paciente
CREATE TABLE IF NOT EXISTS `paciente` (
  `ID_paciente` int(11) NOT NULL AUTO_INCREMENT,
  `codigo_cita` varchar(50) NOT NULL,
  `ID_usuario` int(11) NOT NULL,
  `nombre_completo` varchar(255) NOT NULL,
  `ID_acudiente` int(11) DEFAULT NULL,
  `historial_medico` text DEFAULT NULL,
  `terapeuta_asignado` varchar(255) DEFAULT NULL,
  `ejercicios_registrados` text DEFAULT NULL,
  `estado_cita` varchar(255) DEFAULT NULL,
  `reporte` longblob DEFAULT NULL,
  `fecha_creacion_reporte` date DEFAULT NULL,
  `tipo_plan` varchar(255) DEFAULT NULL,
  `precio_plan` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`ID_paciente`),
  UNIQUE KEY `idx_codigo_cita` (`codigo_cita`),
  KEY `FK_paciente_acudiente` (`ID_acudiente`),
  KEY `FK_paciente_usuario` (`ID_usuario`),
  CONSTRAINT `FK_paciente_acudiente` FOREIGN KEY (`ID_acudiente`) REFERENCES `acudiente` (`ID_acudiente`),
  CONSTRAINT `FK_paciente_usuario` FOREIGN KEY (`ID_usuario`) REFERENCES `usuario` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.paciente: ~0 rows (aproximadamente)

-- Volcando estructura para tabla fisiosalud-2.password_reset_tokens
CREATE TABLE IF NOT EXISTS `password_reset_tokens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `expiracion` datetime NOT NULL,
  `usado` tinyint(1) DEFAULT 0,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_token` (`token`),
  KEY `idx_usuario_expiracion` (`usuario_id`,`expiracion`),
  CONSTRAINT `password_reset_tokens_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.password_reset_tokens: ~5 rows (aproximadamente)

-- Volcando estructura para tabla fisiosalud-2.servicio_implementos
CREATE TABLE IF NOT EXISTS `servicio_implementos` (
  `codigo` varchar(50) NOT NULL DEFAULT 'AUTO_INCREMENT',
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `rango/peso` varchar(255) DEFAULT NULL,
  `ejercicios_posibles` text DEFAULT NULL,
  `dimensiones` varchar(255) DEFAULT NULL,
  `material` varchar(255) DEFAULT NULL,
  `peso_total_set` decimal(10,2) DEFAULT NULL,
  `beneficios` text DEFAULT NULL,
  `dificultad` int(11) DEFAULT NULL,
  `grupo_muscular` varchar(255) DEFAULT NULL,
  `frecuencia` varchar(255) DEFAULT NULL,
  `duracion` varchar(255) DEFAULT NULL,
  `contenido_set` text DEFAULT NULL,
  `uso_recomendado` text DEFAULT NULL,
  `contras` text DEFAULT NULL,
  `mantenimiento` text DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `peso` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.servicio_implementos: ~12 rows (aproximadamente)
INSERT INTO `servicio_implementos` (`codigo`, `nombre`, `descripcion`, `rango/peso`, `ejercicios_posibles`, `dimensiones`, `material`, `peso_total_set`, `beneficios`, `dificultad`, `grupo_muscular`, `frecuencia`, `duracion`, `contenido_set`, `uso_recomendado`, `contras`, `mantenimiento`, `precio`, `peso`) VALUES
	('1172RX', 'Kettlebell Ajustable', 'Kettlebell de peso ajustable para entrenamiento funcional y ejercicios de fuerza completa. Ideal para rehabilitación y acondicionamiento físico.', '4-20 kg', 'Swing, Clean, Press, Snatch, Turkish Get-up, Windmill', '25x15x15 cm', 'Material compuesto de alta durabilidad', 3.50, 'Entrenamiento funcional completo, Ahorro de espacio, Progresión gradual, Seguridad en el uso', 3, 'Full body: hombros, espalda, piernas, core', '2-4 veces por semana', '20-45 minutos por sesión', '1 kettlebell base, 4 placas de peso, manual de instrucciones', 'Ajustar peso según capacidad. Calentar antes de usar. Mantener postura correcta.', 'No exceder el peso máximo. Evitar golpes en superficies duras.', 'Limpiar con paño húmedo. Revisar ajustes regularmente. Almacenar en lugar seco.', 85000.00, 3.50),
	('2489HT', 'Rodillo de Espuma de Alta Densidad', 'Rodillo de liberación miofascial para aliviar tensiones musculares y mejorar la flexibilidad de forma profesional.', 'N/A', 'Liberación miofascial, estiramientos, masaje muscular, movilidad articular', '33x15 cm', 'EVA de alta densidad', 0.80, 'Alivio de tensiones musculares, Mejora de flexibilidad, Recuperación acelerada, Terapia profunda', 0, 'Grupo muscular específico según área trabajada', 'Diario o post-entrenamiento', '5-15 minutos por área', '1 rodillo de espuma, guía de uso especializada', 'Usar sobre músculos, no sobre huesos o articulaciones. Rodar lentamente.', 'No usar sobre lesiones agudas. Evitar presión excesiva en espalda baja.', 'Limpiar con solución suave. Evitar humedad excesiva. Almacenar plano.', 35000.00, 0.80),
	('3316FD', 'Set de Mancuernas Ajustables Pro', 'Set completo de mancuernas con peso ajustable para ejercicios de fortalecimiento progresivo y rehabilitación muscular.', '2.5-20 kg por mancuerna', 'Press, curl, extensiones, elevaciones, sentadillas con peso', '35x15x15 cm (cada mancuerna)', 'Acero recubierto, agarre antideslizante', 15.00, 'Fortalecimiento progresivo, Versatilidad de ejercicios, Ahorro de espacio, Ideal para rehabilitación', 3, 'Todos los grupos musculares', '2-5 veces por semana', '30-60 minutos por sesión', '2 mancuernas base, 16 placas de peso, rack de almacenamiento', 'Ajustar peso según ejercicio. Mantener técnica adecuada. Calentar antes.', 'No soltar pesas desde altura. Verificar ajustes antes de usar.', 'Limpiar con paño seco. Revisar tuercas regularmente. Almacenar en rack.', 120000.00, 15.00),
	('5634KJ', 'Bandas de Resistencia Profesionales', 'Set de bandas elásticas de diferentes niveles de resistencia para ejercicios terapéuticos y mejora de movilidad.', 'Ligera, Media, Pesada, Extra Pesada, Ultra Pesada', 'Pull-apart, face pull, rotaciones, extensiones, sentadillas con banda', 'Longitud: 120 cm (cada banda)', 'Látex natural de alta calidad', 0.50, 'Mejora de movilidad, Resistencia progresiva, Portabilidad, Versatilidad terapéutica', 4, 'Hombros, espalda, glúteos, piernas', '3-6 veces por semana', '15-30 minutos por sesión', '5 bandas de resistencia, manual de ejercicios, bolsa de almacenamiento', 'Inspeccionar bandas antes de usar. Evitar estiramiento excesivo.', 'No usar si hay signos de desgaste. Evitar contacto con objetos afilados.', 'Limpiar con paño húmedo. Almacenar lejos de luz solar directa.', 45000.00, 0.50),
	('5903LK', 'Almohadilla Térmica de Infrarrojo', 'Almohadilla de calor infrarrojo para alivio del dolor muscular y articular con tecnología avanzada y segura.', 'N/A', 'Terapia de calor, relajación muscular, alivio de dolor', '40x30 cm', 'Tela hipoalergénica, elementos calefactores de infrarrojo', 1.50, 'Alivio del dolor muscular, Relajación profunda, Mejora de circulación, Penetración profunda', 0, 'Área específica de aplicación', '1-2 veces al día según necesidad', '15-30 minutos por sesión', 'Almohadilla térmica, controlador, cable de alimentación', 'No usar sobre piel dañada. No dormir con la almohadilla encendida.', 'No usar sobre heridas abiertas. Personas con sensibilidad al calor.', 'Limpiar funda según instrucciones. Guardar enrollada sin doblar.', 95000.00, 1.50),
	('6308BP', 'Masajeador Percusivo Profesional', 'Dispositivo de terapia de percusión para aliviar tensiones musculares profundas y mejorar la recuperación.', '5 velocidades ajustables', 'Masaje de percusión, liberación muscular, terapia de puntos gatillo', '25x8x8 cm', 'Plástico ABS, motor de percusión', 1.10, 'Alivio de tensiones profundas, Recuperación acelerada, Movilidad mejorada, Terapia profesional', 5, 'Todos los grupos musculares grandes', 'Diario o post-entrenamiento', '10-20 minutos por área', 'Dispositivo principal, 4 cabezales, cargador USB, manual', 'Empezar con velocidad baja. No usar sobre huesos o articulaciones.', 'No usar sobre lesiones agudas. Personas con marcapasos consultar médico.', 'Limpiar cabezales regularmente. Cargar completamente antes de primer uso.', 150000.00, 1.10),
	('8741QM', 'Pelota de Estabilidad Profesional', 'Pelota de ejercicio de alta resistencia para mejorar equilibrio, core y rehabilitación postural de forma segura.', '55-75 cm (según tamaño)', 'Planchas, abdominales, sentadillas, ejercicios de equilibrio, rehabilitación postural', 'Diámetro según tamaño (55-75 cm)', 'Material anti-reventón PVC', 1.00, 'Mejora del equilibrio, Fortalecimiento de core, Rehabilitación postural, Versatilidad de ejercicios', 0, 'Core, espalda, piernas', '2-4 veces por semana', '15-30 minutos por sesión', '1 pelota de estabilidad, bomba de aire, tapón de seguridad', 'Inflar según recomendaciones de tamaño. Usar sobre superficie antideslizante.', 'No exponer a calor extremo. No usar con objetos afilados.', 'Limpiar con solución suave. Revisar presión regularmente.', 40000.00, 1.00),
	('90346G', 'Equipo de Electroterapia TENS/EMS', 'Dispositivo profesional para estimulación eléctrica nerviosa y muscular con fines terapéuticos y manejo del dolor.', '20 niveles de intensidad', 'Estimulación muscular (EMS), manejo del dolor (TENS), rehabilitación', '15x10x3 cm', 'Plástico médico, electrodos adhesivos', 1.20, 'Manejo del dolor, Estimulación muscular, Rehabilitación, Terapia profesional', 4, 'Área específica según colocación de electrodos', 'Según prescripción (1-3 veces al día)', '15-30 minutos por sesión', 'Dispositivo TENS/EMS, 4 electrodos, cables, cargador, manual', 'Seguir prescripción profesional. Colocar electrodos correctamente.', 'No usar sobre corazón, cabeza, o si tiene marcapasos. Embarazo.', 'Limpiar electrodos según indicaciones. Almacenar en lugar seco.', 180000.00, 1.20),
	('A93F7G', 'Compresa de Gel Reutilizable', 'Compresa de gel multifuncional para terapia de frío y calor. Ideal para lesiones agudas y manejo del dolor.', 'N/A', 'Terapia de frío, terapia de calor, reducción de inflamación', '25x15 cm', 'Gel terapéutico, funda de tela lavable', 0.30, 'Versatilidad frío/calor, Alivio inmediato, Reutilizable, Fácil de usar', 0, 'Área específica de aplicación', 'Según necesidad (cada 2-4 horas)', '15-20 minutos por aplicación', '1 compresa de gel, funda lavable', 'Para frío: congelar 2+ horas. Para calor: calentar en microondas 30-60 seg.', 'No aplicar directamente sobre piel. No calentar en microondas sin funda.', 'Lavar funda regularmente. Verificar integridad del gel periódicamente.', 25000.00, 0.30),
	('PH63RT', 'Pelotas de Ejercicio para Manos', 'Set de pelotas de diferentes resistencias para ejercicios de rehabilitación de manos, muñecas y antebrazos.', 'Suave, Media, Firme', 'Apretar, rodar, ejercicios de pinza, movilidad de dedos', 'Diámetro: 6 cm (cada pelota)', 'Goma antideslizante', 0.20, 'Rehabilitación de manos, Fortalecimiento de agarre, Alivio de artritis, Movilidad mejorada', 0, 'Manos, muñecas, antebrazos', 'Diario o según prescripción', '5-15 minutos por sesión', '3 pelotas de diferentes resistencias, guía de ejercicios', 'Empezar con resistencia suave. Realizar ejercicios lentamente.', 'No usar si tiene cortes en las manos. Evitar morder las pelotas.', 'Limpiar con paño húmedo. Almacenar en lugar fresco.', 18000.00, 0.20),
	('UT92LM', 'Ultrasonido Terapéutico Portátil', 'Dispositivo de ultrasonido portátil para terapia de tejidos profundos y tratamiento de lesiones musculoesqueléticas.', '1-3 MHz frecuencia ajustable', 'Terapia de tejidos profundos, reducción de inflamación, cicatrización', '18x10x5 cm', 'Plástico médico, transductor de ultrasonido', 0.90, 'Terapia profunda, Reducción de inflamación, Aceleración de cicatrización, Portabilidad profesional', 5, 'Área específica según diagnóstico', 'Según prescripción profesional', '5-15 minutos por área', 'Dispositivo de ultrasonido, transductor, gel conductor, cargador', 'Usar gel conductor. Mover el transductor constantemente.', 'No usar sobre ojos, corazón, o áreas con cáncer. Embarazo.', 'Limpiar transductor después de cada uso. Cargar completamente.', 220000.00, 0.90),
	('YB47KQ', 'Set de Bloques de Yoga Terapéutico', 'Bloques de espuma de alta densidad para facilitar posturas de yoga y ejercicios de estiramiento terapéutico.', 'N/A', 'Posturas de yoga, estiramientos terapéuticos, soporte en ejercicios', '23x15x7.5 cm y 15x15x7.5 cm', 'Espuma EVA ecológica', 0.60, 'Facilita posturas, Mejora alineación, Soporte terapéutico, Material ecológico', 0, 'Full body, especialmente espalda y extremidades', 'Diario o según rutina', 'Variable según uso', '2 bloques de diferentes alturas', 'Usar para apoyo en posturas difíciles. Mantener alineación correcta.', 'No pararse sobre los bloques. No usar para carga pesada.', 'Limpiar con paño húmedo. Almacenar en lugar seco y plano.', 32000.00, 0.60);

-- Volcando estructura para tabla fisiosalud-2.servicio_nutricion
CREATE TABLE IF NOT EXISTS `servicio_nutricion` (
  `codigo` varchar(50) NOT NULL DEFAULT 'AUTO_INCREMENT',
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `tiempo/resultado` varchar(255) DEFAULT NULL,
  `proteina/porcion` decimal(10,2) DEFAULT NULL,
  `valor_energetico` decimal(10,2) DEFAULT NULL,
  `proteinas` decimal(10,2) DEFAULT NULL,
  `carbohidratos` decimal(10,2) DEFAULT NULL,
  `grasas` decimal(10,2) DEFAULT NULL,
  `beneficios` text DEFAULT NULL,
  `dosis_recomendada` varchar(255) DEFAULT NULL,
  `preparacion` text DEFAULT NULL,
  `momento_ideal_post_tratamiento` varchar(255) DEFAULT NULL,
  `contraindicaciones` text DEFAULT NULL,
  `forma_almacenar` varchar(255) DEFAULT NULL,
  `sabores` varchar(255) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `porciones` int(11) DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.servicio_nutricion: ~12 rows (aproximadamente)
INSERT INTO `servicio_nutricion` (`codigo`, `nombre`, `descripcion`, `tiempo/resultado`, `proteina/porcion`, `valor_energetico`, `proteinas`, `carbohidratos`, `grasas`, `beneficios`, `dosis_recomendada`, `preparacion`, `momento_ideal_post_tratamiento`, `contraindicaciones`, `forma_almacenar`, `sabores`, `precio`, `porciones`) VALUES
	('AC3311', 'Proteína en Polvo', 'Proteína de suero de leche de alta calidad para recuperación muscular y desarrollo de masa magra con máxima biodisponibilidad.', 'Resultados en 2-4 semanas con uso constante', 25.00, 120.00, 25.00, 5.00, 1.50, 'Recuperación muscular rápida, Desarrollo de masa magra, Fácil digestión, Máxima biodisponibilidad', '1-2 porciones diarias (pre/post entrenamiento)', 'Mezclar 1 scoop (30g) con 250ml de agua o leche. Agitar vigorosamente o usar licuadora.', 'Ideal 30 minutos después del entrenamiento', 'Personas con alergia a proteína de leche. Consultar si tiene problemas renales.', 'Lugar fresco y seco. Evitar humedad.', 'Vainilla, Chocolate, Fresa', 85000.00, 30),
	('BD1245', 'Multivitamínico Completo', 'Complejo vitamínico y mineral de origen orgánico para fortalecer el sistema inmunológico y optimizar funciones metabólicas.', 'Efectos notables en 2-3 meses', 0.00, 5.00, 0.00, 1.00, 0.00, 'Fortalece sistema inmunológico, Optimiza funciones metabólicas, Energía sostenida, Certificación orgánica', '1 tableta diaria con el desayuno', 'Tomar con un vaso de agua. Puede tomarse con o sin alimentos.', 'No específico - tomar por la mañana', 'Consultar si está tomando anticoagulantes', 'Ambiente seco a temperatura ambiente', 'No aplica - tableta', 45000.00, 60),
	('BIN8824', 'Batido Nutricional Completo', 'Reemplazo de comida completo con balance perfecto de macronutrientes para control de peso y nutrición optimizada.', 'Control de peso en 2-4 semanas, energía inmediata', 20.00, 200.00, 20.00, 25.00, 5.00, 'Control de peso, Nutrición completa, Energía sostenida, Digestión saludable', '1-2 porciones al día como reemplazo de comida', 'Mezclar 2 scoops (50g) con 300ml de líquido. Agitar bien.', 'Ideal como desayuno o cena para control de peso', 'Consultar si tiene problemas renales severos', 'Ambiente seco en envase hermético', 'Vainilla, Chocolate, Frutos del Bosque', 75000.00, 9),
	('BP5572', 'Barritas Proteicas', 'Snack saludable alto en proteína y fibra, perfecto para entre comidas, post-entreno o como complemento nutricional.', 'Satisfacción inmediata, control de peso a largo plazo', 15.00, 210.00, 15.00, 22.00, 8.00, 'Control del apetito, Energía sostenida, Conveniencia, Sin gluten', '1-2 barritas al día como snack', 'Listo para consumir. No requiere preparación.', 'Ideal como snack post-entrenamiento o entre comidas', 'Contiene nueces. Verificar alergias.', 'Lugar fresco. Evitar calor directo.', 'Chocolate, Vainilla-Nuez, Coco', 25000.00, 6),
	('CH6741', 'Colágeno Hidrolizado', 'Suplemento para salud articular, ósea y de la piel con colágeno tipo I y III para mejorar flexibilidad y reducir dolor articular.', 'Mejora visible en piel y articulaciones en 4-8 semanas', 10.00, 40.00, 10.00, 0.00, 0.00, 'Salud articular mejorada, Piel más firme, Huesos fortalecidos, Cabello y uñas fuertes', '10g diarios (1 scoop)', 'Mezclar con agua, jugo, café o batidos. Se disuelve fácilmente.', 'En ayunas o antes de dormir para mejor absorción', 'Consultar si tiene fenilcetonuria', 'Lugar fresco y seco en envase cerrado', 'Natural (sin sabor), Vainilla', 55000.00, 30),
	('CQ5128', 'Coenzima Q10', 'Antioxidante poderoso para salud cardiovascular, energía celular y protección contra el estrés oxidativo.', 'Energía mejorada en 2-4 semanas, beneficios cardíacos en 3-6 meses', 0.00, 5.00, 0.00, 0.50, 0.50, 'Energía celular, Protección cardiovascular, Antioxidante potente, Compatibilidad con medicamentos cardíacos', '1-2 cápsulas diarias con alimentos grasos', 'Tomar con alimentos que contengan grasas para mejor absorción.', 'Con la comida principal que contenga grasas', 'Consultar si está embarazada o amamantando', 'Refrigerar para mayor estabilidad', 'No aplica - cápsula', 52000.00, 60),
	('CV3952', 'Calcio + Vitamina D3', 'Combinación esencial para la salud ósea, dental y muscular con máxima absorción y biodisponibilidad.', 'Prevención de osteoporosis a largo plazo, efectos en 6-12 meses', 0.00, 5.00, 0.00, 1.00, 0.00, 'Huesos fuertes, Prevención de osteoporosis, Salud dental, Función muscular adecuada', '1 tableta diaria con comida', 'Tomar con alimentos para mejor absorción, especialmente con alimentos grasos para la vitamina D.', 'Con la comida principal del día', 'Hipercalcemia, problemas renales severos', 'Ambiente seco, evitar humedad', 'No aplica - tableta', 38000.00, 90),
	('FS8435', 'Fibra Soluble Premium', 'Mezcla de fibras solubles para salud digestiva, control de azúcar en sangre y sensación de saciedad prolongada.', 'Mejora digestiva en 3-7 días, control de peso en 2-4 semanas', 0.00, 25.00, 0.00, 5.00, 0.00, 'Salud digestiva mejorada, Control de azúcar en sangre, Saciedad prolongada, Microbiota intestinal saludable', '1-2 cucharadas diarias', 'Mezclar con al menos 250ml de agua o jugo. Beber inmediatamente y tomar agua adicional.', 'Antes de las comidas principales para control de apetito', 'Tomar con suficiente agua para evitar obstrucción', 'Envase hermético en lugar seco', 'Natural (sin sabor)', 28000.00, 40),
	('JA7294', 'Jugo de Aloe Vera Orgánico', 'Jugo puro de aloe vera para salud digestiva, desintoxicación y bienestar general con certificación orgánica.', 'Alivio digestivo en 1-2 semanas, desintoxicación en 1 mes', 0.50, 10.00, 0.50, 2.00, 0.00, 'Salud digestiva, Desintoxicación, Apoyo inmunológico, Piel saludable', '60-120ml diarios (2-4 onzas)', 'Agitar antes de usar. Tomar solo o mezclar con jugo.', 'En ayunas para mejor absorción y desintoxicación', 'Consultar si está embarazada o tiene problemas renales', 'Refrigerar después de abierto. Consumir en 30 días.', 'Natural de Aloe Vera', 35000.00, 16),
	('NH4316', 'Omega 3 Premium', 'Ácidos grasos esenciales de alta pureza para salud cardiovascular, cognitiva y antiinflamatoria con certificación de calidad.', 'Beneficios cardiovasculares en 3-6 meses', 0.00, 10.00, 0.00, 0.00, 1.00, 'Salud cardiovascular, Función cognitiva, Propiedades antiinflamatorias, Certificado IFOS de pureza', '2 cápsulas diarias con alimentos', 'Tomar con las comidas principales para mejor absorción.', 'Con cualquier comida principal', 'Personas con alergia a pescado. Consultar si toma anticoagulantes.', 'Refrigerar después de abierto', 'No aplica - cápsula', 65000.00, 60),
	('PE2346', 'Pre-Entreno Energético', 'Fórmula avanzada para maximizar rendimiento deportivo, enfoque mental y resistencia durante el entrenamiento.', 'Energía inmediata, mejor rendimiento en 1-2 semanas', 5.00, 25.00, 5.00, 10.00, 0.00, 'Mayor rendimiento deportivo, Enfoque mental mejorado, Resistencia aumentada, Sin bajones de energía', '1 scoop 30 minutos antes del entrenamiento', 'Mezclar con 250-300ml de agua. Consumir dentro de los 30 minutos posteriores.', '30 minutos antes del entrenamiento', 'Sensibilidad a cafeína, problemas cardíacos, hipertensión', 'Ambiente seco en envase hermético', 'Frutas Cítricas, Frutos del Bosque, Tropical', 48000.00, 20),
	('QN1199', 'Quemador Natural', 'Termogénico natural para acelerar metabolismo, aumentar quema de grasa y suprimir apetito de forma segura.', 'Energía aumentada en horas, pérdida de grasa notable en 4-8 semanas', 0.00, 5.00, 0.00, 1.00, 0.00, 'Metabolismo acelerado, Quema de grasa aumentada, Apetito suprimido, Energía sin nerviosismo', '1 cápsula 2 veces al día (mañana y tarde)', 'Tomar con un vaso de agua. La segunda dosis antes de las 4pm.', '30 minutos antes del desayuno y almuerzo', 'Sensibilidad a cafeína, problemas cardíacos, embarazo', 'Lugar fresco y seco', 'No aplica - cápsula', 42000.00, 90);

-- Volcando estructura para tabla fisiosalud-2.servicio_terapia
CREATE TABLE IF NOT EXISTS `servicio_terapia` (
  `codigo` varchar(50) NOT NULL DEFAULT 'AUTO_INCREMENT',
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `terapeuta_disponible` varchar(255) DEFAULT NULL,
  `inicio_jornada` time DEFAULT NULL,
  `final_jornada` time DEFAULT NULL,
  `duracion` int(11) DEFAULT NULL,
  `intensidad` varchar(255) DEFAULT NULL,
  `equipamento` varchar(255) DEFAULT NULL,
  `modalidad` varchar(255) DEFAULT NULL,
  `condiciones_tratar` text DEFAULT NULL,
  `requisitos` text DEFAULT NULL,
  `beneficios` text DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `consideraciones` text DEFAULT NULL,
  `promedio_sesiones` int(11) DEFAULT NULL,
  `recomendacion_precita` varchar(3000) DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.servicio_terapia: ~12 rows (aproximadamente)
INSERT INTO `servicio_terapia` (`codigo`, `nombre`, `descripcion`, `terapeuta_disponible`, `inicio_jornada`, `final_jornada`, `duracion`, `intensidad`, `equipamento`, `modalidad`, `condiciones_tratar`, `requisitos`, `beneficios`, `precio`, `consideraciones`, `promedio_sesiones`, `recomendacion_precita`) VALUES
	('12AB34', 'Masaje Relajante', 'Masaje suave diseñado para reducir el estrés, promover la relajación y mejorar la circulación sanguínea.', 'Laura Fernández | Carlos Ríos | Mariana Soto', '08:00:00', '18:00:00', 45, 'Baja', 'Camilla de masaje, aceites esenciales', 'Presencial', 'Estrés, ansiedad, tensión muscular leve, mala circulación', 'Ninguno específico', 'Reducción del estrés y ansiedad, Mejora de la circulación, Alivio de tensiones leves, Promueve el bienestar general', 35000.00, 'Ideal para personas con altos niveles de estrés laboral', 1, 'Traer identificación personal, ropa cómoda, evitar comer 2 horas antes. Informar al terapeuta sobre alergias a aceites esenciales si las tiene.'),
	('23WE45', 'Terapia de Estiramientos', 'Sesiones guiadas de estiramiento para mejorar flexibilidad, prevenir lesiones y aliviar tensiones.', 'Andrés Gómez | Camila Rojas | Felipe Duarte', '08:00:00', '18:00:00', 50, 'Moderada', 'Colchonetas, bandas elásticas, rodillos de espuma', 'Presencial', 'Rigidez muscular, mala postura, riesgo de lesiones, sedentarismo', 'Ropa cómoda para ejercicio', 'Aumento de la flexibilidad muscular, Mejora de la postura corporal, Prevención de lesiones, Alivio de dolores por sedentarismo', 40000.00, 'Recomendado para personas con trabajos de oficina', 4, 'Presentar documento de identidad, traer ropa deportiva cómoda, hidratarse bien antes de la sesión. Informar sobre cualquier limitación de movimiento o lesiones previas.'),
	('56DF12', 'Rehabilitación Deportiva', 'Programa personalizado para recuperación de lesiones deportivas y mejora del rendimiento físico.', 'Daniela Pérez | Ricardo Ruiz | Sofía Torres', '09:00:00', '19:00:00', 75, 'Moderada-Alta', 'Equipo de fisioterapia, pesas terapéuticas, bosu', 'Presencial', 'Esguinces, lesiones deportivas, recuperación post-lesional', 'Evaluación inicial obligatoria', 'Recuperación de esguinces, Fortalecimiento muscular, Reeducación de la marcha, Prevención de nuevas lesiones', 65000.00, 'Programa personalizado según deporte y lesión', 8, 'Traer identificación, exámenes diagnósticos de la lesión (radiografías, resonancias si las tiene), ropa deportiva adecuada, informe médico inicial. Preferiblemente venir con 1 hora de anticipación para evaluación preliminar.'),
	('65AF31', 'Rehabilitación Post-Quirúrgica', 'Programa intensivo de recuperación después de cirugías ortopédicas o procedimientos invasivos.', 'Manuel Quintero | Paula Vargas | Diego López', '09:00:00', '17:00:00', 120, 'Alta', 'Equipo especializado, máquinas de rehabilitación', 'Presencial', 'Post-cirugía ortopédica, reemplazos articulares, reconstrucciones', 'Historial médico completo, coordinación con equipo quirúrgico', 'Seguimiento post-operatorio, Recuperación de movilidad, Manejo del dolor post-quirúrgico, Prevención de complicaciones', 120000.00, 'Requiere supervisión médica constante', 12, 'Traer documento de identidad, historial médico completo, informe quirúrgico detallado, recetas médicas actuales. Coordinar previamente con el cirujano tratante. Informar sobre medicamentos en uso y alergias. Llevar ropa que facilite el acceso a la zona intervenida.'),
	('67HH34', 'Punción Seca', 'Técnica especializada donde se insertan agujas finas en puntos gatillo para desactivar contracturas profundas.', 'Lucía Moreno | Santiago Peña', '10:00:00', '17:00:00', 45, 'Alta', 'Agujas estériles, equipo de punción, camilla especial', 'Presencial', 'Puntos gatillo, contracturas profundas, dolor miofascial crónico', 'Evaluación médica previa obligatoria', 'Desactivación de puntos gatillo, Alivio de dolor miofascial, Mejora de movilidad muscular, Resultados inmediatos', 75000.00, 'Técnica invasiva que requiere certificación especial', 3, 'Documento de identidad, exámenes de diagnóstico previos si los tiene, informe médico. Informar sobre condiciones hemorrágicas, uso de anticoagulantes o marcapasos. No aplicar cremas o lociones en la zona a tratar. Puede presentar molestias posteriores durante 24-48 horas.'),
	('67RE23', 'Vendaje Neuromuscular', 'Aplicación de vendas elásticas especiales para facilitar la función muscular y reducir el dolor.', 'Adriana Castro | Julián Rincón', '08:00:00', '18:00:00', 30, 'Baja-Moderada', 'Vendas kinesiológicas, tijeras especiales', 'Presencial', 'Dolor muscular, edema, problemas posturales, apoyo deportivo', 'Evaluación de zona a tratar', 'Alivio del dolor muscular, Mejora de la circulación linfática, Corrección de problemas posturales, Soporte durante la actividad física', 45000.00, 'Las vendas pueden permanecer varios días', 1, 'Traer documento de identificación, ropa cómoda que permita acceso a la zona a tratar. Informar sobre alergias al adhesivo (si se conoce), condiciones de piel sensible. Las vendas deben mantenerse secas por 2 horas después de la aplicación y pueden durar 3-5 días.'),
	('75KE23', 'Terapia Miofascial', 'Técnicas manuales para liberar las restricciones del tejido conectivo y aliviar el dolor crónico.', 'Valeria Martínez | Andrés López', '09:00:00', '19:00:00', 60, 'Moderada', 'Instrumentos de liberación miofascial, rodillos', 'Presencial', 'Adherencias fasciales, dolor crónico, limitación de movilidad', 'Diagnóstico previo recomendado', 'Liberación de adherencias fasciales, Mejora de la movilidad articular, Reducción del dolor crónico, Mejora de la postura', 60000.00, 'Puede causar molestias temporales durante la terapia', 4, 'Presentar documento de identidad, traer ropa cómoda, informar sobre diagnósticos previos relacionados. La terapia puede generar sensibilidad temporal en las zonas tratadas. Hidratarse bien antes y después de la sesión. Evitar comidas pesadas 2 horas antes.'),
	('765Q64', 'Terapia Craneosacral', 'Técnica manual suave para evaluar y mejorar el funcionamiento del sistema craneosacral.', 'Luis Castillo | Daniela Cruz', '10:00:00', '16:00:00', 60, 'Baja', 'Camilla especial, ambiente tranquilo', 'Presencial', 'Cefaleas, migrañas, estrés, trastornos del sueño, desequilibrios nerviosos', 'Evaluación previa obligatoria', 'Alivio de cefaleas y migrañas, Reducción del estrés y ansiedad, Mejora de trastornos del sueño, Equilibrio del sistema nervioso', 70000.00, 'Técnica muy suave pero requiere precisión', 6, 'Traer documento de identificación, historial médico relacionado con síntomas neurológicos. Informar sobre medicamentos para migrañas o ansiedad. Usar ropa cómoda, preferiblemente de algodón. Evitar consumo de cafeína 4 horas antes. La sesión puede generar relajación profunda; planificar no conducir inmediatamente después.'),
	('76BG11', 'Masaje Terapéutico', 'Técnicas manuales específicas para aliviar contracturas musculares y dolores localizados.', 'Marcos Rivera | Natalia Ochoa', '08:00:00', '18:00:00', 60, 'Moderada', 'Camilla especializada, aceites terapéuticos', 'Presencial', 'Contracturas musculares, puntos gatillo, dolor localizado', 'Evaluación de zonas problemáticas', 'Alivio de contracturas musculares, Liberación de puntos gatillo, Mejora de movilidad articular, Reducción de dolor localizado', 55000.00, 'Enfoque en zonas específicas de dolor', 2, 'Documento de identidad, informe sobre zonas específicas de dolor, evaluaciones previas si las tiene. Informar sobre alergias a productos tópicos. Puede experimentar dolor temporal durante la manipulación de contracturas. Usar ropa que permita acceso a las zonas afectadas.'),
	('865F14', 'Drenaje Linfático Manual', 'Técnica manual suave para estimular el sistema linfático y eliminar toxinas del organismo.', 'Patricia Gil | Carlos Navarro', '09:00:00', '17:00:00', 50, 'Baja', 'Camilla, aceites especiales, ambiente controlado', 'Presencial', 'Edemas, linfoedemas, problemas circulatorios, post-cirugía', 'Historial médico para casos post-quirúrgicos', 'Reducción de edemas y linfoedemas, Mejora del sistema inmunológico, Eliminación de toxinas, Alivio de piernas cansadas', 65000.00, 'Recomendado especialmente para pacientes post-quirúrgicos', 5, 'Documento de identidad, informe médico o quirúrgico si aplica, exámenes relacionados con problemas circulatorios. Informar sobre insuficiencia cardíaca, trombosis o infecciones activas. Traer ropa cómoda. Beber agua abundante antes y después para facilitar eliminación de toxinas. No aplicar cremas antes de la sesión.'),
	('87FT88', 'Electroterapia Avanzada', 'Uso de corrientes eléctricas terapéuticas para manejo del dolor y estimulación muscular.', 'Esteban Vargas | Valentina Muñoz', '10:00:00', '17:00:00', 50, 'Moderada', 'Equipo de electroterapia, electrodos, gel conductor', 'Presencial', 'Dolor crónico, atrofia muscular, inflamación, recuperación tisular', 'Diagnóstico médico previo obligatorio', 'Alivio de dolor crónico, Estimulación muscular, Reducción de inflamación, Aceleración de recuperación', 70000.00, 'Protocolo personalizado según diagnóstico', 6, 'Presentar documento de identidad, diagnóstico médico completo, exámenes de imagen si los tiene. Informar sobre marcapasos, implantes metálicos, embarazo o epilepsia. No usar cremas o lociones antes. Zona a tratar debe estar limpia y seca. Traer ropa que permita acceso a la zona afectada.'),
	('90AS12', 'Terapia Neural', 'Tratamiento del sistema neurovegetativo para condiciones crónicas y alteraciones del sistema nervioso.', 'Sebastián Cano | María Pardo | Pablo Herrera | Ana Gutiérrez', '11:00:00', '16:00:00', 90, 'Alta', 'Equipo especializado, materiales estériles', 'Presencial', 'Neuralgias, alteraciones neurovegetativas, dolores crónicos complejos', 'Evaluación completa con especialista certificado', 'Tratamiento de neuralgias, Alteraciones neurovegetativas, Dolores crónicos complejos, Enfoque holístico integral', 95000.00, 'Disponible solo con especialistas certificados', 8, 'Traer documento de identidad, historial médico completo, exámenes neurológicos previos, lista de medicamentos actuales. Informar sobre alergias a anestésicos locales si las tiene. Prohibido el consumo de alcohol 48 horas antes. Coordinar con otros tratamientos médicos en curso. Requiere evaluación previa obligatoria con el especialista.');

-- Volcando estructura para tabla fisiosalud-2.terapeuta
CREATE TABLE IF NOT EXISTS `terapeuta` (
  `Codigo_trabajador` varchar(50) NOT NULL,
  `nombre_completo` varchar(255) NOT NULL,
  `fisio_correo` varchar(255) NOT NULL,
  `telefono` varchar(255) NOT NULL,
  `especializacion` varchar(255) DEFAULT NULL,
  `franja_horaria_dias` varchar(255) DEFAULT NULL,
  `franja_horaria_horas` varchar(255) DEFAULT NULL,
  `estado` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Codigo_trabajador`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.terapeuta: ~30 rows (aproximadamente)
INSERT INTO `terapeuta` (`Codigo_trabajador`, `nombre_completo`, `fisio_correo`, `telefono`, `especializacion`, `franja_horaria_dias`, `franja_horaria_horas`, `estado`) VALUES
	('T001', 'Laura Fernández', 'laura.fernandez@fisio.correo.gmail.com', '3104567890', 'Masaje Relajante', 'Lunes a Viernes', '8:00 - 17:00', 'Activo'),
	('T002', 'Carlos Ríos', 'carlos.rios@fisio.correo.gmail.com', '3129876543', 'Masaje Relajante', 'Lunes a Viernes', '8:00 - 17:00', 'Activo'),
	('T003', 'Mariana Soto', 'mariana.soto@fisio.correo.gmail.com', '3152345678', 'Masaje Relajante', 'Lunes a Viernes', '8:00 - 17:00', 'Activo'),
	('T004', 'Andrés Gómez', 'andres.gomez@fisio.correo.gmail.com', '3187654321', 'Terapia de Estiramientos', 'Lunes a Viernes', '8:00 - 17:00', 'Activo'),
	('T005', 'Camila Rojas', 'camila.rojas@fisio.correo.gmail.com', '3119871234', 'Terapia de Estiramientos', 'Lunes a Viernes', '8:00 - 17:00', 'Activo'),
	('T006', 'Felipe Duarte', 'felipe.duarte@fisio.correo.gmail.com', '3204563214', 'Terapia de Estiramientos', 'Lunes a Viernes', '8:00 - 17:00', 'Activo'),
	('T007', 'Daniela Pérez', 'daniela.perez@fisio.correo.gmail.com', '3146547891', 'Rehabilitación Deportiva', 'Lunes a Viernes', '8:00 - 17:00', 'Activo'),
	('T008', 'Ricardo Ruiz', 'ricardo.ruiz@fisio.correo.gmail.com', '3198745632', 'Rehabilitación Deportiva', 'Lunes a Viernes', '8:00 - 17:00', 'Activo'),
	('T009', 'Sofía Torres', 'sofia.torres@fisio.correo.gmail.com', '3117563421', 'Rehabilitación Deportiva', 'Lunes a Viernes', '8:00 - 17:00', 'Activo'),
	('T010', 'Manuel Quintero', 'manuel.quintero@fisio.correo.gmail.com', '3209874123', 'Rehabilitación Post-Quirúrgica', 'Lunes a Viernes', '8:00 - 17:00', 'Activo'),
	('T011', 'Paula Vargas', 'paula.vargas@fisio.correo.gmail.com', '3127419630', 'Rehabilitación Post-Quirúrgica', 'Lunes a Sábado', '9:00 - 18:00', 'Activo'),
	('T012', 'Diego López', 'diego.lopez@fisio.correo.gmail.com', '3147532986', 'Rehabilitación Post-Quirúrgica', 'Lunes a Sábado', '9:00 - 18:00', 'Activo'),
	('T013', 'Lucía Moreno', 'lucia.moreno@fisio.correo.gmail.com', '3157539512', 'Punción Seca', 'Lunes a Sábado', '9:00 - 18:00', 'Activo'),
	('T014', 'Santiago Peña', 'santiago.pena@fisio.correo.gmail.com', '3169513579', 'Punción Seca', 'Lunes a Sábado', '9:00 - 18:00', 'Activo'),
	('T015', 'Adriana Castro', 'adriana.castro@fisio.correo.gmail.com', '3109517534', 'Vendaje Neuromuscular', 'Lunes a Sábado', '9:00 - 18:00', 'Inactivo'),
	('T016', 'Julián Rincón', 'julian.rincon@fisio.correo.gmail.com', '3189517531', 'Vendaje Neuromuscular', 'Lunes a Sábado', '9:00 - 18:00', 'Activo'),
	('T017', 'Mario Rios Escobar', 'marioriosescobar@fisio.correo.gmail.com', '3106416355', 'Neurológica', 'Martes a Viernes', '10:00 - 19:00', 'Activo'),
	('T018', 'Andrés López', 'andres.lopez@fisio.correo.gmail.com', '3108471593', 'Terapia Miofascial', 'Martes a Viernes', '10:00 - 19:00', 'Activo'),
	('T019', 'Marcos Rivera', 'marcos.rivera@fisio.correo.gmail.com', '3113692584', 'Masaje Terapéutico', 'Martes a Viernes', '10:00 - 19:00', 'Activo'),
	('T020', 'Natalia Ochoa', 'natalia.ochoa@fisio.correo.gmail.com', '3209517532', 'Masaje Terapéutico', 'Martes a Viernes', '10:00 - 19:00', 'Activo'),
	('T021', 'Luis Castillo', 'luis.castillo@fisio.correo.gmail.com', '3176547890', 'Terapia Craneosacral', 'Lunes, Miércoles, Viernes', '7:00 - 16:00', 'Activo'),
	('T022', 'Daniela Cruz', 'daniela.cruz@fisio.correo.gmail.com', '3163214789', 'Terapia Craneosacral', 'Lunes, Miércoles, Viernes', '7:00 - 16:00', 'Activo'),
	('T023', 'Patricia Gil', 'patricia.gil@fisio.correo.gmail.com', '3137896541', 'Drenaje Linfático Manual', 'Lunes, Miércoles, Viernes', '7:00 - 16:00', 'Activo'),
	('T024', 'Carlos Navarro', 'carlos.navarro@fisio.correo.gmail.com', '3196541237', 'Drenaje Linfático Manual', 'Lunes, Miércoles, Viernes', '7:00 - 16:00', 'Activo'),
	('T025', 'Esteban Vargas', 'esteban.vargas@fisio.correo.gmail.com', '3111478523', 'Electroterapia Avanzada', 'Lunes a Jueves', '6:00 - 15:00', 'Activo'),
	('T026', 'Valentina Muñoz', 'valentina.munoz@fisio.correo.gmail.com', '3152589631', 'Electroterapia Avanzada', 'Lunes a Jueves', '6:00 - 15:00', 'Activo'),
	('T027', 'Sebastián Cano', 'sebastian.cano@fisio.correo.gmail.com', '3129631478', 'Terapia Neural', 'Lunes a Jueves', '6:00 - 15:00', 'Activo'),
	('T028', 'María Pardo', 'maria.pardo@fisio.correo.gmail.com', '3104569512', 'Terapia Neural', 'Lunes a Jueves', '6:00 - 15:00', 'Activo'),
	('T029', 'Pablo Herrera', 'pablo.herrera@fisio.correo.gmail.com', '3192581473', 'Terapia Neural', 'Miércoles a Domingo', '11:00 - 20:00', 'Activo'),
	('T030', 'Ana Gutiérrez', 'ana.gutierrez@fisio.correo.gmail.com', '3142589634', 'Terapia Neural', 'Miércoles a Domingo', '11:00 - 20:00', 'Activo');

-- Volcando estructura para tabla fisiosalud-2.usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `genero` varchar(255) DEFAULT NULL,
  `correo` varchar(255) NOT NULL,
  `telefono` varchar(255) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `contraseña_confirmada` varchar(255) NOT NULL,
  `historial_medico` text DEFAULT NULL,
  `estado` varchar(255) DEFAULT 'Activo',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1113147124 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fisiosalud-2.usuario: ~2 rows (aproximadamente)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

