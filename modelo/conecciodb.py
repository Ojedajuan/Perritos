import sqlite3
import os

class ConeccioDB:
    def __init__(self, db_path=None):
        # If no path is provided, use a default path
        if db_path is None:
            # Determine the base directory of your project
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, 'data', 'dogs_database.db.sql')
        
        # Print the full path to verify
        print(f"Attempting to connect to database at: {db_path}")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        try:
            # Connect to the database (will create if not exists)
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            print(f"Database connection established successfully to {db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            self.conn = None
            self.cursor = None
    
    def commit(self):
        if self.conn:
            self.conn.commit()

    def cerrar_con(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    # Alias to ensure compatibility
    close = cerrar_con

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cerrar_con()
