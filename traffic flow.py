import csv
import os
from datetime import datetime

def load_csv_file(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def validate_date_input():
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if 1 <= day <= 31:
                break
            else:
                print("Out of range - values must be in the range 1 and 31.")
        except ValueError:
            print("Integer required")

    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if 1 <= month <= 12:
                break
            else:
                print("Out of range - values must be in the range 1 to 12.")
        except ValueError:
            print("Integer required")

    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if 2000 <= year <= 2024:
                break
            else:
                print("Out of range - values must range from 2000 to 2024.")
        except ValueError:
            print("Integer required")

    print(f"Survey date entered: {day:02d}-{month:02d}-{year}")
    file_path = f"traffic_data{day:02d}{month:02d}{year}.csv"
    print(f"Generated file path: {file_path}")

    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found. Please check the file name or directory.")
        return None
    return file_path


def process_csv_data(file_path, data):
    print(f"\tData file selected: {file_path}")

    vehicle_count = len(data)
    truck_count = sum(1 for item in data if item.get('VehicleType') == 'Truck')
    electric_vehicle_count = sum(1 for item in data if item ['elctricHybrid'] == 'TRUE')
    two_wheeled_vehicle_count = sum(1 for item in data if item.get('VehicleType') in ['Bicycle', 'Motorcycle', 'Scooter'])
    bus_north_count = sum(1 for item in data if item.get('VehicleType') == 'Buss' and item.get('travel_Direction_out') == 'N')
    count_not_turning = sum(1 for item in data if item.get('travel_Direction_in') == item.get('travel_Direction_out'))
    truck_percentage = round((truck_count / vehicle_count) * 100) if vehicle_count > 0 else 0
    bicycle_count = sum(1 for item in data if item.get('VehicleType') == 'Bicycle')
    bicycle_per_hour = round(bicycle_count / 24) if vehicle_count > 0 else 0
    over_speed_limit_count = sum(1 for item in data if int(item.get('VehicleSpeed', 0)) > int(item.get('JunctionSpeedLimit', 0)))
    elm_avenue_vehicle_count = sum(1 for item in data if item.get('JunctionName') == 'Elm Avenue/Rabbit Road')
    hanley_highway_vehicle_count = sum(1 for item in data if item.get('JunctionName') == 'Hanley Highway/Westway')
    scooter_count_elm = sum(1 for item in data if item.get('JunctionName') == 'Elm Avenue/Rabbit Road' and item.get('VehicleType') == 'Scooter')
    scooter_percentage_elm = round((scooter_count_elm / elm_avenue_vehicle_count) * 100) if elm_avenue_vehicle_count > 0 else 0

    hourly_data = {}
    for item in data:
        if item.get('JunctionName') == 'Hanley Highway/Westway' and 'Timestamp' in item:
            try:
                hour = item['Timestamp'].split(":")[0]
                hour = str(int(hour))  # Ensure valid hour
                hourly_data[hour] = hourly_data.get(hour, 0) + 1
            except ValueError:
                continue  
    if hourly_data:
        peak_hour_count = max(hourly_data.values())
        peak_hours = [
            f"Between {hour}:00 and {int(hour) + 1}:00"
            for hour, count in hourly_data.items()
            if count == peak_hour_count
        ]
    else:
        peak_hour_count = 0
        peak_hours = []
        
    rain_hours = sum(1 for item in data if item.get('Rain') == 'True')

    outcomes = {
        "data file selected is ": file_path,
        "The total number of vehicles recorded for this date is": vehicle_count,
        "The total number of trucks recorded for this date is": truck_count,
        "The total number of electric vehicles recorded for this date is": electric_vehicle_count,
        "he total number of two-wheeled vehicles for this date is": two_wheeled_vehicle_count,
        "The total number of Busses leaving Elm Avenue/Rabbit Road heading North is": bus_north_count,
        "The total number of Vehicles through both junctions not turning left or right is": count_not_turning,
        "The percentage of total vehicles recorded that are trucks for this date is": f"{truck_percentage}%",
        "The average number of Bicycles per hour for this date is": bicycle_per_hour,
        "The total number of Vehicles recorded as over the speed limit for this date is": over_speed_limit_count,
        "The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is": elm_avenue_vehicle_count,
        "The total number of vehicles recorded through Hanley Highway/Westway junction is": hanley_highway_vehicle_count,
        f"{scooter_percentage_elm}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters."
        "The highest number of vehicles in an hour on Hanley Highway/Westway": peak_hour_count,
        "The most vehicles through Hanley Highway/Westway weree recorded between": ", ".join(peak_hours),
        "The number of hours of rain for this date is ": rain_hours
    }

    return outcomes


def display_outcomes(outcomes):
    for key, value in outcomes.items():
        print(f"{key}: {value}")


def save_to_file(outcomes, file_name="results.txt"):
    try:
        with open(file_name, "w") as file:
            for key, value in outcomes.items():
                file.write(f"{key}: {value}\n")
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error saving data: {e}")


def main():
    data = None
    outcomes = None
    while True:
        print("\nMenu:")
        print("1. Add date.")
        print("2. Process data.")
        print("3. Save data to file")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            file_path = validate_date_input()
            if file_path:
                data = load_csv_file(file_path)

        elif choice == '2':
            if data:
                outcomes = process_csv_data(file_path, data)
                display_outcomes(outcomes)
            else:
                print("No data loaded. Please select a date first.")
        elif choice == '3':
            if outcomes:
                save_to_file(outcomes)
            else:
                print("No data to save. Process data first.")
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
