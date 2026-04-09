import time
import json
from fastapi import FastAPI
from google.protobuf.json_format import MessageToDict
from data_generator import CACHED_USERS
import uvicorn

app = FastAPI()

@app.get("/heavy-data")
async def get_heavy_data(count: int = 0):
    start_time = time.time()
    limit = count if count > 0 else len(CACHED_USERS)
    
    # Convert Proto objects to dicts for JSON serialization
    users_list = [MessageToDict(u, preserving_proto_field_name=True) for u in CACHED_USERS[:limit]]
    payload = {"users": users_list}
    
    # Calculate byte size (approximation for logging)
    payload_size_bytes = len(json.dumps(payload).encode('utf-8'))
    process_time = time.time() - start_time
    
    print(f"REST /heavy-data -> Elements: {limit} | Size: {payload_size_bytes / 1024 / 1024:.2f} MB | Time: {process_time*1000:.2f} ms")
    
    return payload

def serve():
    print("REST server starting on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    serve()
