import multiprocessing
import grpc_server
import rest_server

def run_grpc():
    grpc_server.serve()

def run_rest():
    rest_server.serve()

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_grpc)
    p2 = multiprocessing.Process(target=run_rest)
    
    p1.start()
    p2.start()
    
    print("Servers are running. Press Ctrl+C to stop.")
    try:
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()
        print("Servers stopped.")
