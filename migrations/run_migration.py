"""Script untuk menjalankan database migration.

Contoh penggunaan:
    python migrations/run_migration.py --database postgresql --host localhost --port 5432 --user postgres --db market_data
    python migrations/run_migration.py --database mysql --host localhost --port 3306 --user root --db market_data
"""

import argparse
import os
from pathlib import Path


def run_postgres_migration(host, port, user, password, database):
    """Jalankan migration untuk PostgreSQL."""
    try:
        import psycopg2
    except ImportError:
        print("Error: psycopg2-binary belum terinstall")
        print("Install dengan: pip install psycopg2-binary")
        return False

    try:
        # Connect to database
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Read migration file
        migration_file = Path(__file__).parent / "001_create_market_data_table.sql"
        with open(migration_file, "r") as f:
            migration_sql = f.read()

        # Execute migration
        cursor.execute(migration_sql)
        print("✓ Migration berhasil dijalankan untuk PostgreSQL")
        print(f"  Database: {database}")
        print(f"  Host: {host}:{port}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"✗ Error menjalankan migration: {e}")
        return False


def run_mysql_migration(host, port, user, password, database):
    """Jalankan migration untuk MySQL/MariaDB."""
    try:
        import mysql.connector
    except ImportError:
        print("Error: mysql-connector-python belum terinstall")
        print("Install dengan: pip install mysql-connector-python")
        return False

    try:
        # Connect to database
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        # Read migration file
        migration_file = Path(__file__).parent / "001_create_market_data_table_mysql.sql"
        with open(migration_file, "r") as f:
            migration_sql = f.read()

        # Split and execute migration by statements
        statements = [s.strip() for s in migration_sql.split(';') if s.strip()]
        for statement in statements:
            if statement:
                cursor.execute(statement)

        conn.commit()
        print("✓ Migration berhasil dijalankan untuk MySQL")
        print(f"  Database: {database}")
        print(f"  Host: {host}:{port}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"✗ Error menjalankan migration: {e}")
        return False


def rollback_postgres_migration(host, port, user, password, database):
    """Rollback migration untuk PostgreSQL."""
    try:
        import psycopg2
    except ImportError:
        print("Error: psycopg2-binary belum terinstall")
        return False

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()

        rollback_file = Path(__file__).parent / "001_rollback_market_data_table.sql"
        with open(rollback_file, "r") as f:
            rollback_sql = f.read()

        cursor.execute(rollback_sql)
        print("✓ Rollback migration berhasil dijalankan untuk PostgreSQL")
        print(f"  Database: {database}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"✗ Error menjalankan rollback: {e}")
        return False


def rollback_mysql_migration(host, port, user, password, database):
    """Rollback migration untuk MySQL/MariaDB."""
    try:
        import mysql.connector
    except ImportError:
        print("Error: mysql-connector-python belum terinstall")
        return False

    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        rollback_file = Path(__file__).parent / "001_rollback_market_data_table_mysql.sql"
        with open(rollback_file, "r") as f:
            rollback_sql = f.read()

        # Split and execute migration by statements
        statements = [s.strip() for s in rollback_sql.split(';') if s.strip()]
        for statement in statements:
            if statement:
                cursor.execute(statement)

        conn.commit()
        print("✓ Rollback migration berhasil dijalankan untuk MySQL")
        print(f"  Database: {database}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"✗ Error menjalankan rollback: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Jalankan database migration")
    parser.add_argument(
        "--database",
        choices=["postgresql", "mysql"],
        required=True,
        help="Tipe database"
    )
    parser.add_argument("--host", default="localhost", help="Database host")
    parser.add_argument("--port", type=int, help="Database port (default: 5432 for postgres, 3306 for mysql)")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", help="Database password (default: dari env var DB_PASSWORD)")
    parser.add_argument("--db", required=True, help="Database name")
    parser.add_argument("--rollback", action="store_true", help="Jalankan rollback migration")

    args = parser.parse_args()

    # Get password from argument or environment
    password = args.password or os.environ.get("DB_PASSWORD")
    if not password:
        print("Error: Password tidak ditemukan. Gunakan --password atau set env var DB_PASSWORD")
        return

    # Set default port based on database type
    if args.port is None:
        args.port = 5432 if args.database == "postgresql" else 3306

    # Run migration
    if args.database == "postgresql":
        if args.rollback:
            rollback_postgres_migration(args.host, args.port, args.user, password, args.db)
        else:
            run_postgres_migration(args.host, args.port, args.user, password, args.db)
    else:  # mysql
        if args.rollback:
            rollback_mysql_migration(args.host, args.port, args.user, password, args.db)
        else:
            run_mysql_migration(args.host, args.port, args.user, password, args.db)


if __name__ == "__main__":
    main()
