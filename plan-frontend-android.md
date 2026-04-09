# Plan Frontend (Android): PoC gRPC vs API REST

## 1. Contexto y Objetivos
El objetivo de este plan es construir la aplicación móvil (cliente) para una Prueba de Concepto que compara el rendimiento entre un API REST (JSON) y gRPC (Protobuf).
La aplicación móvil se conectará a un backend existente que provee una lista gigante de objetos complejos a través de ambos protocolos. El objetivo es consumir esta data y medir la latencia total y el tamaño del payload de cada protocolo.

## 2. Arquitectura y Tecnologías
*   Plataforma: Android Nativo.
*   Lenguaje: Kotlin.
*   UI: Jetpack Compose.
*   REST Client: Retrofit, OkHttp.
*   gRPC Client: `grpc-kotlin-stub`, `grpc-okhttp`, `protobuf-kotlin`.
*   Contrato: Se debe copiar el archivo `schema.proto` generado en el backend para generar las clases en Android.

## 3. Plan de Implementación (Android)

### Fase 1: Configuración del Proyecto y Dependencias
1.  Inicializar un proyecto Android vacío con Jetpack Compose.
2.  Agregar dependencias de Retrofit, OkHttp y logging interceptor.
3.  Configurar el plugin de Protobuf en el `build.gradle` del proyecto (App) para compilar el código gRPC/Kotlin.
4.  Copiar el archivo `schema.proto` del backend dentro de la carpeta `src/main/proto/` del proyecto Android.

### Fase 2: Capa de Red (Network Layer)
1.  **REST:**
    *   Crear la interfaz de Retrofit para consumir el endpoint `GET /heavy-data`.
    *   Crear los data classes en Kotlin equivalentes para la respuesta JSON (o usar GSON/Moshi).
    *   Configurar un `Interceptor` en OkHttp para registrar la longitud del body (Content-Length o conteo de bytes descargados) para estimar el tamaño del payload REST.
2.  **gRPC:**
    *   Crear el canal de comunicación (`ManagedChannelBuilder.forAddress()`) apuntando a la IP del servidor.
    *   Usar el stub asíncrono (Coroutines) generado a partir de `schema.proto`.

### Fase 3: Interfaz de Usuario (UI) y Medición
1.  Crear una pantalla principal con Compose con la siguiente estructura:
    *   Input para configurar la IP del servidor.
    *   Botón: "Test REST API".
    *   Botón: "Test gRPC".
    *   Texto de Resultados que muestre para la última petición:
        *   **Tiempo Total (Latencia):** medido en ms.
        *   **Tamaño (Size):** medido en KB o MB.
        *   **Items:** Número de objetos recibidos para validar que son iguales en ambos casos.
2.  Implementar la lógica en un ViewModel que ejecute las llamadas en el hilo de IO (`Dispatchers.IO`), mida el tiempo con `System.currentTimeMillis()` antes y después de la llamada, y actualice los estados de la UI.

## 4. Verificación
*   Asegurar que el dispositivo móvil (físico o emulador) esté en la misma red que el backend (usando la IP local, no localhost/10.0.2.2 si es un dispositivo físico).
*   Realizar pruebas con REST y luego con gRPC repetidas veces.
*   Comparar los resultados visuales en pantalla, observando diferencias en latencia y estimación de tamaño de datos transferidos.
