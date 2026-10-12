from  dbutils import get_connection

def createBanksTable():
    print("Create the Bank Tables if not exists")
    query = """
    IF NOT EXISTS ( Select * from sys.tables where name = 'Banks')
    BEGIN 
	    CREATE Table banks(
	        bank_id INT IDENTITY(1,1) PRIMARY KEY,
	        bank_name VARCHAR(20) Not Null,

            CONSTRAINT UNIQUER UNIQUE (bank_name)
	    )
    END
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
        conn.commit()
    print("Bank Table is verified existence and created if not")


def insertBankTable(*banknames):
    print(f"insert{banknames} in the banks table")
    bank_list = []
    createBanksTable()
    if len(banknames) == 1 and isinstance(banknames[0], (list, tuple)):
        bank_list = banknames[0]
    else:
        bank_list = list(banknames)  # It's already multiple positional arguments (tuple)
    insert_query = """
    Insert into banks(bank_name)
    values(?)
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            for bank in bank_list:
                checkQuery = f"select 1 from banks where bank_name=?"
                result = cursor.execute(checkQuery,(bank,))
                row = result.fetchone()
                if row is None:
                    cursor.execute( insert_query, (bank,))
                    print(f"Successfully inserted: {bank}")
                else:
                    print(f"Skipped (already exists): {bank}")
        conn.commit()
    print("BankName is inserted into Banks Table")


def getBanksDetails():
    """Retrieves bank records and auto-seeds default banks if the table is nearly empty."""
    print("Retrieve Bank Records")
    query = """
    SELECT bank_id, bank_name FROM banks;
    """
    attributes = []
    
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Auto-seed if there is 1 or fewer records
            if len(rows) <= 1:
                insertBankTable('HDFC', 'IDB')
                # Re-run query to fetch the newly seeded records
                cursor.execute(query)
                rows = cursor.fetchall()
                
            for row in rows:
                attributes.append({
                    "bank_id": row.bank_id,    
                    "bank_name": row.bank_name
                })
                
    # Don't forget to return your collected data!
    return attributes 

def fetchBankEmployeesSchema():
    print("Fetch the Employees table schema")
    query ="""
    SELECT 
        COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'bank_employees'
    """
    attributes = []
    with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    for row in rows:
                         attributes.append({
                              "column_name":row.COLUMN_NAME,
                              "data_type":row.DATA_TYPE,
                              "character_max_length":row.CHARACTER_MAXIMUM_LENGTH,
                              "is_nullable":row.IS_NULLABLE
                         })
                conn.commit()
    return attributes


def createBankEmployeesTable():
    print("Create the BankEmployee Tables if not exists")
    query = """
    IF NOT Exists( Select * from sys.tables where name = 'bank_employees')
    BEGIN
        CREATE TABLE bank_employees (
            employee_id INT IDENTITY(1,1),
            fullname VARCHAR(100) NOT NULL,
            email_id VARCHAR(100) UNIQUE NOT NULL,
            salary DECIMAL(18, 2),
            age INT CHECK (age >= 18),
            bank_id INT NOT NULL,
            branch VARCHAR(50),
            address VARCHAR(255),           -- Corrected spelling from 'adress'
            indian BIT default 1,                     -- BIT acts as a boolean (0 or 1 / True or False)
            mobile_number VARCHAR(20),
    
            -- Explicitly named constraints
            CONSTRAINT PK_BankEmployees PRIMARY KEY (employee_id),
            CONSTRAINT FK_BankEmployees_Banks FOREIGN KEY (bank_id) REFERENCES banks(bank_id)
        );
    END
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
        conn.commit()


