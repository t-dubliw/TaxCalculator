# Tax Rules Engine

This tax calculation engine is designed for the following scenario: annual tax calculation based on income.

### Requirements

1. The program should be able to receive and store tax rules
2. Users should be able to input income details
3. The program should return the calculated tax amount, including the applicable tax rule version
4. The system should provide a way to query past tax rule versions

## Architecture Overview

### The application follows Clean Architecture pattern. 

### Key Design Decisions

1. **Extendability**: The program should be able to support multiple types of tax rules (e.g., income tax, tax on goods, property tax, etc.), and within each type, multiple versions of the tax rules.
2. **Modularity**: The tax calculation and tax rule loading are designed as separate modules. Further tax calculations can be extended based on the tax types.

## Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 12+ (or SQLite for development)
- Docker & Docker Compose (optional)

### Local Development Setup

**Option 1 - using Docker: Rocommended**

Prerequisites: Make sure to have docker installed.

1. Create a docker network
```
docker network create taxcalc-net
```
2. Go to the root folder (parent of src folder), and execute the following commands:
```
docker build -t taxcalc:dev -f deployments/docker/Dockerfile --target development .

docker run -d --name taxcalc-postgres --network taxcalc-net -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypasswor -e POSTGRES_DB=tax_residency_db -p 6543:5432 -v postgres_data:/var/lib/postgresql/data postgres:15

docker run -d --name taxcalc-fastapi --network taxcalc-net -p 8000:8000 -e DB_TYPE=postgresql -e DB_HOST=taxcalc-postgres -e DB_PORT=5432 -e DB_NAME=tax_residency_db -e DB_USER=myuser -e DB_PASSWORD=mypasswor taxcalc:dev
```
3. To view Swagger docs, check this url on a browser
```http://127.0.0.1:8000/docs#```


**Option 2 - using the source code**
1. Go to the src directory using terminal
2. Install dependencies (Requirements.txt)
3. Run PostgreSQL (either existing or docker)
```
docker run -d --name tax_residency_db_container -e POSTGRES_DB=tax_residency_db -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -p 6543:5432 postgres:15
```
4. Setup DB variables in ```\config\environments``` 

```DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=6543
DB_NAME=tax_residency_db
DB_USER=myuser
DB_PASSWORD=mypassword
```

5. Run command 
```uvicorn src.main:app --reload --host 0.0.0.0 --port 8000```

6. To view Swagger docs
```http://127.0.0.1:8000/docs#```


**Built using FastAPI, SQLAlchemy, and PostgreSQL**

## Current Implementation

1. Tax rule types: Income tax (code: income_tax), property tax (code: property_tax). Currently, the calculation is implemented only for ***income_tax***. 
2. There will be only one active tax rule per tax type.

### Tax Calculation APIs

### 1. Create Tax Rule
Insert a new tax rule into the system.

**Endpoint**: `POST /api/v1/tax-rules`

#### Request Headers
```http
Authorization: Bearer your-api-key-here
[In this implementation, we do not validate the key, but this shouldn't be empty]
```

#### Request Body Schema (json)
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `rule_type` | string | Yes | Type of tax rule to apply (supported types: "income_tax") |
| `version` | string | Yes | Rule version |
| `tax_date` | string | Yes | Date when this rule becomes effective |
| `tax_rule` | json object | Yes | The tax calculation rules |
| `is_active` | boolean | Yes | Is this rule active |

#### Sample Request Body
```json
{
  "rule_type": "income_tax",
  "version": "2024.1",
  "tax_date": "2025-08-15T14:03:06.968Z",
  "tax_rule": {
    "calculation_type": "brackets",
    "brackets": [
      {"min_amount": 0, "max_amount": 500, "rate": 10},
      {"min_amount": 501, "max_amount": 700, "rate": 12},
      {"min_amount": 701, "max_amount": 900, "rate": 15},
      {"min_amount": 901, "max_amount": null, "rate": 18}
      ]
    },
    "is_active": true
}
```

#### Response Schema: TaxRuleResponse
```json
{
  "id": number,
  "rule_type": string,
  "version": string,
  "is_active": boolean,
  "tax_rule": json object
}
```

### 2. Calculate Tax
Calculate tax amount based on income and tax type using the latest active tax rule.

**Endpoint**: `GET /api/v1/tax-rules/calculate/{rule_type}/{amount}`

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `amount` | number | Yes | Income amount to calculate tax for |
| `rule_type` | string | Yes | Type of tax rule to apply (supported types: "income_tax", "sales_tax") |

#### Request Example
```http
GET /api/v1/tax-rules/calculate/income_tax/600
```

#### Response Schema (for income tax)
```json
{
  "income": number,
  "tax_amount": number,
  "rule_version": string,
  "breakdown": [
    {
      "bracket": string,
      "rate": string,
      "taxable_amount": number,
      "tax": number
    }
  ]
}
```

### 3. Get all tax rules
Get all tax rules stored in the system.

**Endpoint**: `GET /api/v1/tax-rules`

#### Query Parameters: None

#### Request Example
```http
GET  /api/v1/tax-rules
```

#### Response Schema: TaxRuleListResponse
```json
{
  "success": boolean,
  "message": string,
  "timestamp": string,
  "rules": [TaxRuleResponse],
}
```

---
