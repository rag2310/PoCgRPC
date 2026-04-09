# PoC gRPC vs API REST - Backend

Este proyecto provee dos servicios (REST y gRPC) para comparar su rendimiento en la transferencia de grandes volúmenes de datos.

## Estructura del Proyecto

- `protos/`: Definición de mensajes y servicios mediante Protocol Buffers.
- `data_generator.py`: Genera datos mock complejos en memoria.
- `grpc_server.py`: Servidor gRPC en el puerto 50051.
- `rest_server.py`: Servidor REST (FastAPI) en el puerto 8000.
- `main.py`: Script para ejecutar ambos servidores simultáneamente.

## Instalación y Ejecución

1. Asegúrate de tener Python 3.x y un entorno virtual configurado.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta los servidores:
   ```bash
   python main.py
   ```

## Endpoints

- **REST:** `GET http://localhost:8000/heavy-data?count=1000`
- **gRPC:** Puerto `50051`, servicio `poc_grpc.DataService`, método `GetHeavyData`.

## Notas para el Cliente Android

- El archivo `protos/schema.proto` debe ser copiado al proyecto Android para generar los stubs correspondientes.
- Asegúrate de que el dispositivo móvil tenga acceso a la IP local del servidor.
