-- Crear la base de datos Examen2
CREATE DATABASE IF NOT EXISTS Examen2BD2;

-- Usar la base de datos Examen2
USE Examen2BD2;

-- Crear la tabla Inventario
CREATE TABLE IF NOT EXISTS Inventario (
    IdProducto INT AUTO_INCREMENT PRIMARY KEY,
    Cantidad INT NOT NULL,
    NombreProducto VARCHAR(255) NOT NULL,
    Precio DECIMAL(10, 2) NOT NULL
);

-- Crear la tabla OrdenCompra
CREATE TABLE IF NOT EXISTS OrdenCompra (
    IdOrden INT AUTO_INCREMENT PRIMARY KEY,
    IdProducto INT NOT NULL,
    Cantidad INT NOT NULL,
    NombreProducto VARCHAR(255) NOT NULL,
    Precio DECIMAL(10, 2) NOT NULL,
    NombreCliente VARCHAR(255) NOT NULL,
    DireccionCliente VARCHAR(255) NOT NULL,
    CedulaCliente VARCHAR(20) NOT NULL,
    TelefonoCliente VARCHAR(20) NOT NULL,
    FOREIGN KEY (IdProducto) REFERENCES Inventario(IdProducto)
);

-- Insertar algunos datos de ejemplo en la tabla Inventario
INSERT INTO Inventario (Cantidad, NombreProducto, Precio) VALUES
(100, 'Guantes de Box', 10.50),
(200, 'Straps', 15.75),
(150, 'Pesas', 20.00);

-- Insertar algunos datos de ejemplo en la tabla OrdenCompra
INSERT INTO OrdenCompra (IdProducto, Cantidad, NombreProducto, Precio, NombreCliente, DireccionCliente, CedulaCliente, TelefonoCliente) VALUES
(1, 2, 'Guantes de Box', 10.50, 'Juan Perez', 'Calle Falsa 123', '1234567890', '555-1234'),
(2, 1, 'Straps', 15.75, 'Maria Garcia', 'Avenida Siempre Viva 456', '0987654321', '555-5678'),
(3, 3, 'Pesas', 20.00, 'Carlos Ruiz', 'Boulevard Central 789', '1122334455', '555-7890');
