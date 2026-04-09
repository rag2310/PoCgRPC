import urllib.request
import json
import time

def run_test():
    url = "http://localhost:8000/heavy-data"
    
    print(f"Enviando petición REST a {url}...")
    start_time = time.time()
    
    try:
        # Realizar la petición GET
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            users = data.get("users", [])
            
            elapsed = time.time() - start_time
            print(f"¡Éxito!")
            print(f"Usuarios recibidos: {len(users)}")
            print(f"Tiempo total (Red + Procesamiento): {elapsed*1000:.2f} ms")
            
            if len(users) > 0:
                first_user = users[0]
                print(f"Ejemplo del primer usuario: {first_user.get('username')} ({first_user.get('email')})")
                
    except Exception as e:
        print(f"Error en la llamada REST: {e}")

if __name__ == "__main__":
    run_test()
