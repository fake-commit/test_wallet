# Wallet API

A Django REST Framework API for managing wallets and transactions, following the JSON:API specification.

## Features

- Wallet management (create, read, update, delete)
- Transaction management (create, read, update, delete)
- Automatic balance calculation based on transactions
- Prevention of negative balances
- Unique transaction IDs
- JSON:API compliant responses
- Swagger/OpenAPI documentation
- PostgreSQL database
- Docker support

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)

## Quick Start with Docker Compose

1. Clone the repository:
```bash
git clone <repository-url>
cd test_wallet
```

2. Start the application using Docker Compose:
```bash
docker-compose up --build
```

3. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

4. Create a superuser (optional):
```bash
docker-compose exec web python manage.py createsuperuser
```

The API will be available at:
- API endpoints: http://localhost:8000/api/
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Development with Docker Compose

### Running Tests
```bash
docker-compose exec web pytest
```

### Code Quality
```bash
# Format code
docker-compose exec web black .
docker-compose exec web isort .

# Run linter
docker-compose exec web flake8
```

### Database Management
```bash
# Access PostgreSQL shell
docker-compose exec db psql -U postgres -d wallet_db

# Reset database (if needed)
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

## API Documentation

### Wallets

#### List Wallets
```
GET /api/wallets/
```

Query Parameters:
- `filter[min_balance]`: Filter wallets with balance >= value
- `filter[max_balance]`: Filter wallets with balance <= value
- `filter[label]`: Search wallets by label
- `sort`: Order by fields (e.g., `-balance`, `label`)

#### Create Wallet
```
POST /api/wallets/
```

Request Body:
```json
{
  "data": {
    "type": "wallets",
    "attributes": {
      "label": "My Wallet"
    }
  }
}
```

#### Get Wallet
```
GET /api/wallets/{id}/
```

#### Update Wallet
```
PATCH /api/wallets/{id}/
```

Request Body:
```json
{
  "data": {
    "type": "wallets",
    "id": "{id}",
    "attributes": {
      "label": "Updated Label"
    }
  }
}
```

#### Delete Wallet
```
DELETE /api/wallets/{id}/
```

### Transactions

#### List Transactions
```
GET /api/transactions/
```

Query Parameters:
- `filter[min_amount]`: Filter transactions with amount >= value
- `filter[max_amount]`: Filter transactions with amount <= value
- `filter[wallet]`: Filter transactions by wallet ID
- `filter[txid]`: Search transactions by transaction ID
- `sort`: Order by fields (e.g., `-amount`, `created_at`)

#### Create Transaction
```
POST /api/transactions/
```

Request Body:
```json
{
  "data": {
    "type": "transactions",
    "attributes": {
      "wallet": 1,
      "txid": "unique-transaction-id",
      "amount": "10.00"
    }
  }
}
```

#### Get Transaction
```
GET /api/transactions/{id}/
```

#### Update Transaction
```
PATCH /api/transactions/{id}/
```

Request Body:
```json
{
  "data": {
    "type": "transactions",
    "id": "{id}",
    "attributes": {
      "amount": "20.00"
    }
  }
}
```

#### Delete Transaction
```
DELETE /api/transactions/{id}/
```

## Database Schema

### Wallet
- id: UUID (Primary Key)
- label: String
- balance: Decimal(18,18)

### Transaction
- id: UUID (Primary Key)
- wallet_id: UUID (Foreign Key to Wallet)
- txid: String (Unique)
- amount: Decimal(18,18)

## Constraints
- Transaction txid must be unique
- Wallet balance cannot be negative
- Transaction amount can be negative