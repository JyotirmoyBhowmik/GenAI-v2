"""
GenAI Platform - Sample Data Generator
Creates realistic sample data for all divisions
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger


class SampleDataGenerator:
    """Generates sample datasets for different divisions."""
    
    def __init__(self, output_dir: str = "./data/divisions"):
        """
        Initialize sample data generator.
        
        Args:
            output_dir: Directory to save generated data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"SampleDataGenerator initialized (output: {self.output_dir})")
    
    def generate_fmcg_sales_data(self):
        """Generate FMCG sales Excel data."""
        logger.info("Generating FMCG sales data...")
        
        # Generate sample sales data
        dates = [datetime.now() - timedelta(days=x) for x in range(90)]
        products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
        regions = ['North', 'South', 'East', 'West', 'Central']
        
        data = []
        for _ in range(500):
            data.append({
                'Date': random.choice(dates).strftime('%Y-%m-%d'),
                'Product': random.choice(products),
                'Region': random.choice(regions),
                'Quantity': random.randint(10, 500),
                'Unit_Price': round(random.uniform(50, 500), 2),
                'Revenue': None  # Will calculate
            })
        
        df = pd.DataFrame(data)
        df['Revenue'] = df['Quantity'] * df['Unit_Price']
        
        output_path = self.output_dir / 'fmcg' / 'sales_data.xlsx'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, index=False)
        
        logger.info(f"Generated FMCG sales data: {output_path}")
        return output_path
    
    def generate_manufacturing_production_data(self):
        """Generate manufacturing production logs."""
        logger.info("Generating manufacturing production data...")
        
        dates = [datetime.now() - timedelta(days=x) for x in range(60)]
        machines = ['Machine-001', 'Machine-002', 'Machine-003', 'Machine-004']
        products = ['Widget-A', 'Widget-B', 'Widget-C']
        shifts = ['Morning', 'Evening', 'Night']
        
        data = []
        for _ in range(300):
            data.append({
                'Date': random.choice(dates).strftime('%Y-%m-%d'),
                'Machine_ID': random.choice(machines),
                'Product': random.choice(products),
                'Shift': random.choice(shifts),
                'Units_Produced': random.randint(50, 500),
                'Defects': random.randint(0, 20),
                'Downtime_Hours': round(random.uniform(0, 2), 1),
                'Operator': f"OP-{random.randint(1, 10):03d}"
            })
        
        df = pd.DataFrame(data)
        df['Quality_Rate'] = ((df['Units_Produced'] - df['Defects']) / df['Units_Produced'] * 100).round(2)
        
        output_path = self.output_dir / 'manufacturing' / 'production_logs.xlsx'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, index=False)
        
        logger.info(f"Generated manufacturing data: {output_path}")
        return output_path
    
    def generate_hotel_booking_data(self):
        """Generate hotel booking data."""
        logger.info("Generating hotel booking data...")
        
        dates = [datetime.now() - timedelta(days=x) for x in range(120)]
        room_types = ['Single', 'Double', 'Suite', 'Deluxe']
        booking_sources = ['Online', 'Phone', 'Walk-in', 'Travel Agent']
        
        data = []
        for i in range(400):
            checkin = random.choice(dates)
            nights = random.randint(1, 7)
            checkout = checkin + timedelta(days=nights)
            
            data.append({
                'Booking_ID': f"BK-{i+1:05d}",
                'Guest_Name': f"Guest-{random.randint(1, 200)}",
                'Check_In': checkin.strftime('%Y-%m-%d'),
                'Check_Out': checkout.strftime('%Y-%m-%d'),
                'Nights': nights,
                'Room_Type': random.choice(room_types),
                'Rate_Per_Night': random.randint(2000, 10000),
                'Total_Amount': None,  # Will calculate
                'Booking_Source': random.choice(booking_sources),
                'Status': random.choice(['Confirmed', 'Checked-In', 'Checked-Out', 'Cancelled'])
            })
        
        df = pd.DataFrame(data)
        df['Total_Amount'] = df['Nights'] * df['Rate_Per_Night']
        
        output_path = self.output_dir / 'hotel' / 'bookings.xlsx'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, index=False)
        
        logger.info(f"Generated hotel booking data: {output_path}")
        return output_path
    
    def generate_stationery_catalog(self):
        """Generate stationery catalog."""
        logger.info("Generating stationery catalog...")
        
        categories = ['Pens', 'Notebooks', 'Files', 'Staplers', 'Paper']
        
        data = []
        for i in range(100):
            data.append({
                'SKU': f"ST-{i+1:04d}",
                'Product_Name': f"{random.choice(categories)} - {random.choice(['Premium', 'Standard', 'Economy'])}",
                'Category': random.choice(categories),
                'Price': round(random.uniform(5, 500), 2),
                'Stock': random.randint(0, 1000),
                'Supplier': f"Supplier-{random.choice(['A', 'B', 'C', 'D'])}",
                'Reorder_Level': random.randint(10, 100)
            })
        
        df = pd.DataFrame(data)
        
        output_path = self.output_dir / 'stationery' / 'catalog.xlsx'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, index=False)
        
        logger.info(f"Generated stationery catalog: {output_path}")
        return output_path
    
    def generate_hr_data(self):
        """Generate HR employee dataset."""
        logger.info("Generating HR employee data...")
        
        departments = ['HR', 'Finance', 'Sales', 'Marketing', 'IT', 'Operations']
        designations = ['Manager', 'Senior Executive', 'Executive', 'Assistant']
        
        data = []
        for i in range(150):
            data.append({
                'Employee_ID': f"EMP-{i+1:05d}",
                'Name': f"Employee {i+1}",
                'Department': random.choice(departments),
                'Designation': random.choice(designations),
                'Join_Date': (datetime.now() - timedelta(days=random.randint(30, 1825))).strftime('%Y-%m-%d'),
                'Salary': random.randint(30000, 150000),
                'Location': random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune']),
                'Experience_Years': random.randint(0, 20)
            })
        
        df = pd.DataFrame(data)
        
        output_path = self.output_dir / 'shared' / 'hr_employees.xlsx'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, index=False)
        
        logger.info(f"Generated HR data: {output_path}")
        return output_path
    
    def generate_all(self):
        """Generate all sample datasets."""
        logger.info("Generating all sample datasets...")
        
        results = {
            'fmcg_sales': self.generate_fmcg_sales_data(),
            'manufacturing_production': self.generate_manufacturing_production_data(),
            'hotel_bookings': self.generate_hotel_booking_data(),
            'stationery_catalog': self.generate_stationery_catalog(),
            'hr_employees': self.generate_hr_data()
        }
        
        logger.info(f"Generated {len(results)} sample datasets successfully!")
        return results


def main():
    """Generate all sample data."""
    generator = SampleDataGenerator()
    results = generator.generate_all()
    
    print("\n" + "="*60)
    print("Sample Data Generation Complete!")
    print("="*60)
    for name, path in results.items():
        print(f"  {name}: {path}")
    print("="*60)


if __name__ == "__main__":
    main()
