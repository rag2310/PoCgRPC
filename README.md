# PoC gRPC vs API REST - Backend & Documentación

Este proyecto es una Prueba de Concepto (PoC) diseñada para comparar el rendimiento, la latencia y el tamaño del payload entre un API REST tradicional (JSON) y gRPC (Protobuf) en un escenario de alta carga de datos.

## 🚀 Resumen de Logros y Funcionalidad

1.  **Contrato Único:** Definición de un esquema complejo en `protos/schema.proto` que incluye objetos anidados, listas de transacciones y metadatos.
2.  **Generador de Datos Pesados:** Un motor en `data_generator.py` que crea 5,000 perfiles de usuario únicos en memoria para asegurar una carga "pesada" (aprox. 16MB en JSON y 9MB en gRPC).
3.  **Servidor Dual:** `main.py` levanta simultáneamente:
    *   **REST (FastAPI):** Puerto 8000, devuelve JSON.
    *   **gRPC:** Puerto 50051, devuelve Protobuf binario.
4.  **Medición de Rendimiento:** Ambos servidores calculan e imprimen en consola:
    *   **Payload Size:** El tamaño real en MB del mensaje generado.
    *   **Internal Latency:** El tiempo de procesamiento y serialización en el servidor (ms).
5.  **Clientes de Prueba:** Scripts individuales (`test_rest.py` y `test_client.py`) para validar la conexión y medir el tiempo total de ida y vuelta (Round-Trip Time).

## ⚠️ Solución al Error: `RESOURCE_EXHAUSTED`

Durante las pruebas, encontramos el error:
`StatusCode.RESOURCE_EXHAUSTED - CLIENT: Received message larger than max (9907346 vs. 4194304)`

### Causa:
Por defecto, las librerías de gRPC (tanto en servidor como en cliente) limitan el tamaño de los mensajes a **4MB** para prevenir ataques de denegación de servicio (DoS) por agotamiento de memoria. Nuestro payload de 5,000 usuarios excedía los 9MB.

### Solución Implementada:
Hemos aumentado el límite a **100MB** tanto en el servidor como en el cliente de prueba mediante la configuración de `grpc.max_send_message_length` y `grpc.max_receive_message_length`.

**En el Servidor (`grpc_server.py`):**
```python
options = [
    ('grpc.max_send_message_length', 100 * 1024 * 1024),
    ('grpc.max_receive_message_length', 100 * 1024 * 1024)
]
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
```

**En el Cliente (`test_client.py`):**
```python
options = [
    ('grpc.max_receive_message_length', 100 * 1024 * 1024)
]
channel = grpc.insecure_channel('localhost:50051', options=options)
```

## 📱 Notas Críticas para el Cliente Android

Para la Fase 3 (Desarrollo en Android), es **imprescindible** aplicar esta misma configuración en el `ManagedChannel` de gRPC:

```kotlin
val channel = ManagedChannelBuilder.forAddress(host, port)
    .usePlaintext()
    .maxInboundMessageSize(100 * 1024 * 1024) // 100MB
    .build()
```

## 🛠️ Cómo ejecutar las pruebas

1.  **Instalar dependencias:** `.venv/bin/python -m pip install -r requirements.txt`
2.  **Iniciar Servidores:** `.venv/bin/python main.py`
3.  **Probar REST:** `.venv/bin/python test_rest.py`
4.  **Probar gRPC:** `.venv/bin/python test_client.py`

Los resultados comparativos aparecerán en la consola del servidor.
