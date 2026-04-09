# Plan Backend (Python): PoC gRPC vs API REST

## 1. Contexto y Objetivos
El objetivo es proveer el backend para una Prueba de Concepto que compara el rendimiento entre un API REST tradicional (basado en JSON) y gRPC (basado en Protobuf). Se requiere servir una lista gigante de objetos complejos (haciendo el payload "lo más pesado posible") a través de ambos protocolos, devolviendo exactamente la misma data lógica.

## 2. Arquitectura y Tecnologías
*   Lenguaje: Python 3.
*   REST Framework: FastAPI (Uvicorn).
*   gRPC Framework: `grpcio`, `grpcio-tools`.
*   Generador de Datos: Script para instanciar en memoria una gran cantidad de objetos anidados y complejos.

## 3. Plan de Implementación (Backend)

### Fase 1: Definición del Esquema (Protobuf)
1.  Crear el directorio `protos/` en la raíz del proyecto.
2.  Crear el archivo `schema.proto` dentro de `protos/`.
3.  Definir los mensajes (e.g., `UserProfile`, `Address`, `TransactionHistory`) con múltiples atributos anidados y listas.
4.  Definir el servicio gRPC `DataService` con el método `GetHeavyData`.

### Fase 2: Lógica de Negocio y Servidores
1.  **Dependencias:** Asegurar que `fastapi`, `uvicorn`, `grpcio` y `grpcio-tools` estén instalados en el `.venv`.
2.  **Generación de código gRPC:** Ejecutar el compilador `protoc` (usando `grpc_tools.protoc`) para generar los archivos `_pb2.py` y `_pb2_grpc.py`.
3.  **Generador de Mock Data:** Crear un módulo que construya la lista de miles de `UserProfile` y la mantenga en memoria.
4.  **Servidor gRPC:** Implementar el `DataServiceServicer` que use la mock data generada y levante el servidor en el puerto 50051.
5.  **Servidor REST (FastAPI):** Implementar un endpoint `GET /heavy-data` que devuelva la misma mock data (FastAPI se encarga de serializar a JSON) y levantar el servidor en el puerto 8000.
6.  **Script de Entrada:** Crear un script `main.py` que permita correr ambos servidores de manera concurrente (o proveer instrucciones para correrlos en terminales separadas).

## 4. Verificación
*   Levantar ambos servidores.
*   Probar el endpoint REST localmente usando `curl` o el navegador en `http://localhost:8000/heavy-data`.
*   (Opcional) Usar herramientas como `grpcurl` para verificar que el endpoint gRPC en el puerto 50051 responde correctamente con la estructura esperada.
