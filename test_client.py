import grpc
import os
from protos import schema_pb2, schema_pb2_grpc
import time

def run_test():
    # Configurar límites de tamaño de mensaje (100 MB)
    options = [
        ('grpc.max_send_message_length', 100 * 1024 * 1024),
        ('grpc.max_receive_message_length', 100 * 1024 * 1024)
    ]
    # Conectar al servidor con las opciones de tamaño
    host = os.environ.get("SERVER_HOST", "localhost")
    channel = grpc.insecure_channel(f'{host}:50051', options=options)
    stub = schema_pb2_grpc.DataServiceStub(channel)
    
    print(f"Enviando petición gRPC a {host}:50051...")
    start_time = time.time()
    
    try:
        # Enviar 0 para solicitar TODOS los usuarios disponibles (al igual que REST)
        response = stub.GetHeavyData(schema_pb2.DataRequest(count=0))
        
        elapsed = time.time() - start_time
        print(f"¡Éxito!")
        print(f"Usuarios recibidos: {len(response.users)}")
        print(f"Tiempo total (Red + Procesamiento): {elapsed*1000:.2f} ms")
        
        if len(response.users) > 0:
            print(f"Ejemplo del primer usuario: {response.users[0].username} ({response.users[0].email})")
            
    except grpc.RpcError as e:
        print(f"Error en la llamada gRPC: {e.code()} - {e.details()}")

if __name__ == "__main__":
    run_test()
