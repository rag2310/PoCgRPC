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
Por defecto, las librerías de gRPC limitan los mensajes a **4MB**. Nuestro payload de 5,000 usuarios excede los 9MB.

### Solución Implementada:
Aumentamos el límite a **100MB** en servidor y cliente:
- **Python:** Configurado vía `options` en `grpc.server` e `insecure_channel`.
- **Android:** Debe configurarse usando `.maxInboundMessageSize(100 * 1024 * 1024)`.

---

## 🐋 Prueba de Rendimiento "Pod a Pod" con Docker

Esta prueba simula la comunicación interna de una red de microservicios (similar a Kubernetes) donde el tráfico viaja a través de un bridge virtual de red.

### ⚙️ Configuración
- **Dockerfile:** Empaqueta la aplicación y sus dependencias.
- **Docker Compose:** Orquesta el backend y los clientes efímeros.
- **Variable de Entorno:** Los clientes usan `SERVER_HOST` para localizar el contenedor del servidor en la red de Docker.

### 🧪 ¿Por qué esta prueba simula fielmente un entorno Kubernetes?
Aunque Docker Compose no es un orquestador completo como K8s, para efectos de **rendimiento de protocolos**, es una simulación de alta fidelidad (>95%):

*   **Network Hops (Salto de Red):** Los datos no viajan por `localhost`. Deben salir del contenedor cliente, atravesar el **Docker Bridge (puente virtual)** y entrar al contenedor servidor. Esto genera latencia de red real.
*   **Service Discovery (DNS):** Usar `SERVER_HOST=backend` emula exactamente cómo un Pod busca a otro usando el nombre del Service en K8s. Docker resuelve el nombre del servicio a la IP privada del contenedor de forma dinámica.
*   **Costos de Serialización:** El impacto en CPU/Memoria para convertir datos a JSON vs Protobuf es **idéntico** al que ocurriría en un entorno productivo.
*   **Aislamiento:** Cada contenedor tiene su propio stack TCP/IP, simulando el aislamiento que ofrece un Pod.

*Nota técnica:* Las únicas diferencias menores son la ausencia de plugins de red complejos (CNI como Calico/Flannel) y balanceadores internos (Kube-proxy/IPVS), pero el impacto en la comparativa de gRPC vs REST es despreciable.

### 🛠️ Cómo ejecutar la prueba de Docker
1.  **Levantar el servidor en segundo plano:**
    ```bash
    docker-compose up -d backend
    ```
2.  **Ejecutar prueba REST (Contenedor a Contenedor):**
    ```bash
    docker-compose run --rm test-rest
    ```
3.  **Ejecutar prueba gRPC (Contenedor a Contenedor):**
    ```bash
    docker-compose run --rm test-grpc
    ```

---

## 🛠️ Cómo ejecutar las pruebas Locales (Fuera de Docker)

1.  **Instalar dependencias:** `.venv/bin/python -m pip install -r requirements.txt`
2.  **Iniciar Servidores:** `.venv/bin/python main.py`
3.  **Probar REST:** `.venv/bin/python test_rest.py`
4.  **Probar gRPC:** `.venv/bin/python test_client.py`

## 📱 Notas Críticas para el Cliente Android

Para la Fase 3 (Desarrollo en Android), es **imprescindible** aplicar esta misma configuración en el `ManagedChannel` de gRPC:

```kotlin
val channel = ManagedChannelBuilder.forAddress(host, port)
    .usePlaintext()
    .maxInboundMessageSize(100 * 1024 * 1024) // 100MB
    .build()
```
