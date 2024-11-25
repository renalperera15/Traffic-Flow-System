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
        date = input("Enter the date (YYYY-MM-DD): ")
        if len(date) == 10 and date[4] == '-' and date[7] == '-':
            year_str, month_str, day_str = date.split('-')
            if year_str.isdigit() and month_str.isdigit() and day_str.isdigit():
                year, month, day = int(year_str), int(month_str), int(day_str)
                if 2000 <= year <= 2024:  
                    if 1 <= month <= 12:
                        if (
                            (month in [1, 3, 5, 7, 8, 10, 12] and 1 <= day <= 31) or
                            (month in [4, 6, 9, 11] and 1 <= day <= 30) or
                            (month == 2 and 1 <= day <= (29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28))
                        ):
                            print(f"You entered a valid date: Year={year}, Month={month}, Day={day}")
                            return date  
                        else:
                            print("Invalid day for the given month.")
                    else:
                        print("Invalid month. Month must be between 1 and 12.")
                else:
                    print("Invalid year. Year must be between 2000 and 2024.")  
            else:
                print("Invalid date components. Ensure year, month, and day are numeric.")
        else:
            print("Invalid format. Please use the format YYYY-MM-DD.")

def get_csv_file_path():
    """Prompt user to select an existing file or create a new one."""
    while True:
        choice = input("Do you want to (1) use an existing file or (2) create a new file? Enter 1 or 2: ").strip()
        if choice == '1':
            date = validate_date_input()
            csv_filename = f"{date}.csv"
            file_path = os.path.join("path_to_csv_files", csv_filename)
            if os.path.exists(file_path):
                print(f"File found: {csv_filename}")
                return file_path
            else:
                print(f"Error: {csv_filename} not found.")
        elif choice == '2':
            date = validate_date_input()
            csv_filename = f"{date}.csv"
            file_path = os.path.join("path_to_csv_files", csv_filename)
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["VehicleType", "Junction", "Direction", "Speed", "SpeedLimit", "Time", "Rain"])
            print(f"New file created: {csv_filename}")
            return file_path
        else:
            print("Invalid choice. Please enter 1 or 2.")

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
    """Main function to drive the program."""
    load_transactions()
    file_path = get_csv_file_path()
    if file_path:
        process_csv_data(file_path)
        report = display_outcomes(traffic_dict, file_path)
        with open("Results.txt", "w") as result_file:
            result_file.write("\n".join(report))
    else:
        print("Exiting program as no valid file was provided.")

if __name__ == "__main__":
    main()
