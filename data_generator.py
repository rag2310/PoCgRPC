import random
import uuid
import time
from protos import schema_pb2

def generate_mock_data(count=5000):
    users = []
    for i in range(count):
        user_id = str(uuid.uuid4())
        transactions = []
        for j in range(random.randint(5, 15)):
            transactions.append(schema_pb2.TransactionHistory(
                transaction_id=str(uuid.uuid4()),
                amount=random.uniform(10.0, 1000.0),
                currency="USD",
                timestamp=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                status=random.choice(["COMPLETED", "PENDING", "FAILED"]),
                description=f"Transaction {j} for user {i}",
                tags=["shopping", "electronics", "groceries", "services"][:random.randint(1, 4)]
            ))
        
        user = schema_pb2.UserProfile(
            id=user_id,
            username=f"user_{i}",
            email=f"user_{i}@example.com",
            first_name=f"FirstName_{i}",
            last_name=f"LastName_{i}",
            bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 5,
            address=schema_pb2.Address(
                street=f"{random.randint(100, 999)} Main St",
                city="Anytown",
                state="State",
                zip_code=f"{random.randint(10000, 99999)}",
                country="USA",
                location=schema_pb2.Location(
                    latitude=random.uniform(-90, 90),
                    longitude=random.uniform(-180, 180)
                )
            ),
            transactions=transactions,
            metadata={
                "registration_ip": f"192.168.1.{random.randint(1, 254)}",
                "last_login_device": random.choice(["Android", "iOS", "Web", "Desktop"]),
                "loyalty_program": random.choice(["Gold", "Silver", "Bronze", "None"])
            },
            is_active=random.choice([True, False]),
            reputation_score=random.uniform(0.0, 5.0),
            joined_at=int(time.time()) - random.randint(0, 10**7)
        )
        users.append(user)
    return users

# Pre-generate data to be shared between REST and gRPC
CACHED_USERS = generate_mock_data()
