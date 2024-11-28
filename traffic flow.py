import os
import csv
from datetime import datetime

traffic_dict = {
    "total_vehicles": 0,
    "total_trucks": 0,
    "total_electric": 0,
    "total_two_wheeled": 0,
    "buses_north": 0,
    "no_turn": 0,
    "over_speed": 0,
    "elm_rabbit_total": 0,
    "scooters_at_elm_rabbit": 0,
    "hanley_westway_total": 0,
    "hours_of_rain": 0,
    "bicycles_hourly": {hour: 0 for hour in range(24)},
    "hanley_hourly": {hour: 0 for hour in range(24)},
}

def load_transactions(file_name="Results.txt"):
    """Load transaction data from a file."""
    global traffic_dict
    try:
        with open(file_name, 'r') as file:
            traffic_dict.clear()
            for line in file:
                key, value = line.strip().split(':', 1)
                traffic_dict[key] = int(value) if value.isdigit() else value
        print("Transactions loaded successfully.")
    except FileNotFoundError:
        print(f"No file found. Creating '{file_name}' and starting with an empty dataset.")
        with open(file_name, 'w') as file:
            file.write("")
    except Exception as e:
        print(f"Error loading transactions: {e}")

def validate_date_input():
    while True:
        # Get and validate the day
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if 1 <= day <= 31:
                break
            else:
                print("Out of range - values must be in the range 1 and 31.")
        except ValueError:
            print("Integer required")

    while True:
        # Get and validate the month
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if 1 <= month <= 12:
                break
            else:
                print("Out of range - values must be in the range 1 to 12.")
        except ValueError:
            print("Integer required")

    while True:
        # Get and validate the year
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if 2000 <= year <= 2024:
                break
            else:
                print("Out of range - values must range from 2000 and 2024.")
        except ValueError:
            print("Integer required")

    print(f"Survey date entered: {day:02d}-{month:02d}-{year}")



def get_csv_file_path(file_path):
    """Prompt user to select an existing file or create a new one."""
    while True:
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            print("File was not found.")
            break
    pass



def process_csv_data(file_path):
    """Process data from the specified CSV file."""
    global traffic_dict
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    vehicle_type = row.get('VehicleType', '').lower()
                    junction = row.get('Junction', '').lower()
                    direction = row.get('Direction', '').lower()
                    speed = int(row.get('Speed', '0') or '0')
                    speed_limit = int(row.get('SpeedLimit', '0') or '0')
                    time = datetime.strptime(row.get('Time', '00:00'), '%H:%M')
                    hour = time.hour
                    rain = row.get('Rain', 'No').lower() == 'yes'

                    traffic_dict["total_vehicles"] += 1
                    if vehicle_type == 'truck':
                        traffic_dict["total_trucks"] += 1
                    if vehicle_type == 'electric':
                        traffic_dict["total_electric"] += 1
                    if vehicle_type in {'bike', 'motorbike', 'scooter'}:
                        traffic_dict["total_two_wheeled"] += 1
                    if vehicle_type == 'bus' and junction == 'elm avenue/rabbit road' and direction == 'north':
                        traffic_dict["buses_north"] += 1
                    if direction == 'straight':
                        traffic_dict["no_turn"] += 1
                    if speed > speed_limit:
                        traffic_dict["over_speed"] += 1
                    if junction == 'elm avenue/rabbit road':
                        traffic_dict["elm_rabbit_total"] += 1
                        if vehicle_type == 'scooter':
                            traffic_dict["scooters_at_elm_rabbit"] += 1
                    if junction == 'hanley highway/westway':
                        traffic_dict["hanley_westway_total"] += 1

                    if vehicle_type == 'bicycle':
                        traffic_dict["bicycles_hourly"][hour] += 1
                    if junction == 'hanley highway/westway':
                        traffic_dict["hanley_hourly"][hour] += 1

                    if rain:
                        traffic_dict["hours_of_rain"] += 1
                except Exception as e:
                    print(f"Error processing row: {row} | Error: {e}")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error processing CSV: {e}")

def display_outcomes(stats, file_name):
    """Generate and display a report based on traffic statistics."""
    try:
        truck_percentage = round((stats["total_trucks"] / stats["total_vehicles"]) * 100) if stats["total_vehicles"] > 0 else 0
        scooter_percentage = round((stats["scooters_at_elm_rabbit"] / stats["elm_rabbit_total"]) * 100) if stats["elm_rabbit_total"] > 0 else 0
        total_bicycles = sum(stats["bicycles_hourly"].values())
        average_bicycles_hourly = round(total_bicycles / 24) if total_bicycles > 0 else 0
        peak_hour_count = max(stats["hanley_hourly"].values(), default=0)
        peak_hours = [
            f"Between {hour}:00 and {hour + 1}:00"
            for hour, count in stats["hanley_hourly"].items() if count == peak_hour_count
        ]

        report = [
            f"Selected CSV File: {file_name}",
            f"Total number of vehicles: {stats['total_vehicles']}",
            f"Total number of trucks: {stats['total_trucks']}",
            f"Total number of electric vehicles: {stats['total_electric']}",
            f"Total number of two-wheeled vehicles: {stats['total_two_wheeled']}",
            f"Total number of buses heading north at Elm Avenue/Rabbit Road: {stats['buses_north']}",
            f"Total number of vehicles passing without turning: {stats['no_turn']}",
            f"Percentage of trucks: {truck_percentage}%",
            f"Average number of bicycles per hour: {average_bicycles_hourly}",
            f"Total number of vehicles over speed limit: {stats['over_speed']}",
            f"Total vehicles through Elm Avenue/Rabbit Road: {stats['elm_rabbit_total']}",
            f"Total vehicles through Hanley Highway/Westway: {stats['hanley_westway_total']}",
            f"Percentage of scooters through Elm Avenue/Rabbit Road: {scooter_percentage}%",
            f"Number of vehicles in peak hour on Hanley Highway/Westway: {peak_hour_count}",
            f"Peak hour(s) on Hanley Highway/Westway: {', '.join(peak_hours)}",
            f"Total hours of rain: {stats['hours_of_rain']}",
        ]

        print("\n".join(report))
        return report
    except Exception as e:
        print(f"Error generating report: {e}")
        return []

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
            data = get_csv_file_path(file_path)
        elif choice == '2':
            if data != None:
                outcomes = process_csv_data(file_path, data)
                display_outcomes(outcomes)
            else:
                print("No data loaded. Please select a date first.")
        elif choice == '3':
            if outcomes != None:
                load_transactions(outcomes)
            else:
                print("No data loaded. Please select a date first.")
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
