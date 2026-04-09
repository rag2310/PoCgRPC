import grpc
import time
from concurrent import futures
from protos import schema_pb2, schema_pb2_grpc
from data_generator import CACHED_USERS

class DataServiceServicer(schema_pb2_grpc.DataServiceServicer):
    def GetHeavyData(self, request, context):
        start_time = time.time()
        # Slice based on request if necessary, or just return all
        count = request.count if request.count > 0 else len(CACHED_USERS)
        
        response = schema_pb2.DataResponse(users=CACHED_USERS[:count])
        
        # Calculate byte size
        payload_size_bytes = response.ByteSize()
        process_time = time.time() - start_time
        
        print(f"gRPC GetHeavyData -> Elements: {count} | Size: {payload_size_bytes / 1024 / 1024:.2f} MB | Time: {process_time*1000:.2f} ms")
        
        return response

def serve():
    # Configurar límites de tamaño de mensaje (100 MB)
    options = [
        ('grpc.max_send_message_length', 100 * 1024 * 1024),
        ('grpc.max_receive_message_length', 100 * 1024 * 1024)
    ]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
    schema_pb2_grpc.add_DataServiceServicer_to_server(DataServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
