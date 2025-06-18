-- Tabla principal de hoteles
-- Contiene la información básica de cada hotel.
CREATE OR REPLACE TABLE hoteles(
    hotel_id INT PRIMARY KEY,                    -- Identificador único del hotel
    ciudad VARCHAR(40),                          -- Ciudad donde se ubica el hotel
    tipo VARCHAR(10),                            -- Tipo de alojamiento (hotel, hostal, etc.)
    nombre VARCHAR(80),                          -- Nombre del hotel
    estrellas INT(1)                             -- Número de estrellas oficiales
);

-- Tabla de precios por fecha
-- Relaciona cada hotel con sus precios diarios.
CREATE OR REPLACE TABLE precios(
    hotel_id INT,                                -- Referencia al hotel
    fecha DATE,                                  -- Fecha del precio
    precio FLOAT,                                -- Precio para esa fecha
    FOREIGN KEY (hotel_id) REFERENCES hoteles(hotel_id)
);

-- Tabla de camas por habitación
-- Guarda las opciones de camas para cada habitación de cada hotel.
CREATE OR REPLACE TABLE camas(
    hotel_id INT,                                -- Referencia al hotel
    opcion_habitacion INT,                       -- Número de la opción de habitación
    camas VARCHAR(100),                          -- Descripción de las camas
    FOREIGN KEY (hotel_id) REFERENCES hoteles(hotel_id)
);

-- Tabla de categorías y notas
-- Guarda las valoraciones por categoría (limpieza, ubicación, etc.) de cada hotel.
CREATE OR REPLACE TABLE categorias_notas(
    hotel_id INT,                                -- Referencia al hotel
    categoria VARCHAR(40),                       -- Nombre de la categoría valorada
    nota FLOAT,                                  -- Nota obtenida en esa categoría
    FOREIGN KEY (hotel_id) REFERENCES hoteles(hotel_id)
);

-- Tabla de puntos de interés (POIs)
-- Relaciona cada hotel con los puntos de interés cercanos.
CREATE OR REPLACE TABLE pois(
    hotel_id INT,                                -- Referencia al hotel
    seccion VARCHAR(40),                         -- Tipo de POI (restaurantes, atracciones, etc.)
    poi VARCHAR(100),                            -- Nombre del punto de interés
    FOREIGN KEY (hotel_id) REFERENCES hoteles(hotel_id)
);

-- Tabla de comentarios
-- Guarda los comentarios de usuarios sobre cada hotel.
CREATE OR REPLACE TABLE comentarios(
    hotel_id INT,                                -- Referencia al hotel
    comentario VARCHAR(500),                     -- Texto del comentario
    FOREIGN KEY (hotel_id) REFERENCES hoteles(hotel_id)
);

-- Tabla de cuentas de anfitrión
-- Guarda los datos de los usuarios que pueden publicar alojamientos.
CREATE OR REPLACE TABLE cuenta_anfitrion (
    anfitrion_id INT PRIMARY KEY AUTO_INCREMENT, -- Identificador único autoincremental
    hotel_id INT,                                -- Referencia al hotel
    email VARCHAR(100) UNIQUE NOT NULL,          -- Correo electrónico único y obligatorio
    telefono VARCHAR(20),                        -- Teléfono de contacto
    nombre VARCHAR(40),                          -- Nombre del anfitrión
    apellidos VARCHAR(80),                       -- Apellidos del anfitrión
    edad INT,                                    -- Edad del anfitrión
    genero VARCHAR(20),                          -- Género (opcional, texto libre)
    password VARCHAR(255) NOT NULL,              -- Contraseña (debe almacenarse cifrada)
    FOREIGN KEY (hotel_id) REFERENCES hoteles(hotel_id)
);

-- Tabla de cuentas de huésped
-- Guarda los datos de los usuarios que pueden reservar alojamientos.
CREATE OR REPLACE TABLE cuenta_huesped (
    huesped_id INT PRIMARY KEY AUTO_INCREMENT,   -- Identificador único autoincremental
    email VARCHAR(100) UNIQUE NOT NULL,          -- Correo electrónico único y obligatorio
    telefono VARCHAR(20),                        -- Teléfono de contacto
    nombre VARCHAR(40),                          -- Nombre del huésped
    apellidos VARCHAR(80),                       -- Apellidos del huésped
    edad INT,                                    -- Edad del huésped
    genero VARCHAR(20),                          -- Género (opcional, texto libre)
    password VARCHAR(255) NOT NULL               -- Contraseña (debe almacenarse cifrada)
);