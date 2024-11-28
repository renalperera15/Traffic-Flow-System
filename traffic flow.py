import csv
def load_csv_file(file_path):
    while True:
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            print("File was not found.")
            break
    pass

#Task A
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
                print("Out of range - values must range from 2000 and 2024.")
        except ValueError:
            print("Integer required")

    print(f"Survey date entered: {day:02d}-{month:02d}-{year}")
    file_path = f"traffic_data{day:02d}{month:02d}{year}.csv"
    print(file_path)
    return file_path

def process_csv_data(file_path, data):
    print("\t"+f"data file selected is{file_path}")

    # Find Total number of vehicle count
    vehicle_count = len(data)

    # Find Truck count
    truck_count = 0
    for item in data:
        if item['VehicleType'] == 'Truck':
            truck_count += 1

    # Find electric vehicles
    electric_vehicle_count = 0
    for item in data:
        if item['elctricHybrid'] == 'True':
            # data set 'TRUE' is stored as 'True' in dictionary
            electric_vehicle_count += 1

    # Find two-wheeled vehicles
    two_wheeled_vehicle_count = 0
    for item in data:
        if item['VehicleType'] == 'Bicycle' or item['VehicleType'] == 'Motorcycle' or item['VehicleType'] == 'Scooter':
            two_wheeled_vehicle_count += 1

    # Find number of buss leaving north
    buss_north_count = 0
    for item in data:
        if item['VehicleType'] == 'Buss' and item['travel_Direction_out'] == 'N':
            buss_north_count += 1

    # Find number of vehicle not turning
    count_not_turning = 0
    for item in data:
        if item['travel_Direction_in'] == item['travel_Direction_out']:
            count_not_turning += 1

    # Find trucks percentage
    truck_percentage = (truck_count/vehicle_count)*100

    # Find the number of bicycles per hour
    bicycle_count = 0
    for item in data:
        if item['VehicleType'] == 'Bicycle':
            bicycle_count += 1
    bicycle_per_hour = bicycle_count/24

    # Find over limit vehicles
    over_limit_vehicle_count = 0
    for item in data:
        if item['JunctionSpeedLimit'] < item['VehicleSpeed']:
            over_limit_vehicle_count += 1

    elm_avenue_vehicle_count = 0
    for item in data:
        if item['JunctionName'] == 'Elm Avenue/Rabbit Road':
            elm_avenue_vehicle_count += 1

    hanley_highway_vehicle_count = 0
    for item in data:
        if item['JunctionName'] == 'Hanley Highway/Westway':
            hanley_highway_vehicle_count += 1

    scooter_count_elm = 0
    for item in data:
        if item['JunctionName'] == 'Elm Avenue/Rabbit Road' and item['VehicleType'] == 'Scooter':
            scooter_count_elm += 1
    percent_scooter_count_elm = (scooter_count_elm/elm_avenue_vehicle_count)*100

    outcomes = {'The total number of vehicles recorded for this date is': vehicle_count,
                'The total number of trucks recorded for this date is': truck_count,
                'The total number of electric vehicles recorded for this date is': electric_vehicle_count,
                'The total number of two-wheeled vehicles for this date is': two_wheeled_vehicle_count,
                'The total number of Busses leaving Elm Avenue/Rabbit Road heading North is': buss_north_count,
                'The total number of Vehicles through both junctions not turning left or right is': count_not_turning,
                'The percentage of total vehicles recorded that are trucks for this date is': truck_percentage,
                'The average number of Bicycles per hour for this date is': bicycle_per_hour,
                'The total number of Vehicles recorded as over the speed limit for this date is': over_limit_vehicle_count,
                'The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is': elm_avenue_vehicle_count,
                'The total number of vehicles recorded through Hanley Highway/Westway junction is': hanley_highway_vehicle_count,
                round(percent_scooter_count_elm, 2):'% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.'
                }

    return outcomes
    pass

def display_outcomes(outcomes):
    for key, value in outcomes.items():
        print(f"{key}: {value}")
    pass
def save_to_file(outcomes, file_name="results.txt"):
    try:
        with open(file_name, "w") as file:
            for key, value in outcomes.items():
                file.write(f"{key}: {value}\n")
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error saving data: {e}")
    pass

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
            data = load_csv_file(file_path)
        elif choice == '2':
            if data != None:
                outcomes = process_csv_data(file_path, data)
                display_outcomes(outcomes)
            else:
                print("No data loaded. Please select a date first.")
        elif choice == '3':
            if outcomes != None:
                save_to_file(outcomes)
            else:
                print("No data loaded. Please select a date first.")
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()

