from graphics import *
import csv

class MultiCSVProcessor:
    def __init__(self):
        self.current_data = []

    def validate_date_input(self):
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

        try:
            with open(file_path, 'r') as _:
                return file_path
        except FileNotFoundError:
            print(f"File '{file_path}' not found. Please check the file name or directory.")
            return None

    def load_csv_file(self, file_path):
        data = []
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
            print(f"Successfully loaded {len(data)} rows from '{file_path}'.")
        except Exception as e:
            print(f"Error loading CSV file: {e}")
        return data

    def clear_previous_data(self):
        self.current_data = []

    def draw_histogram(self, data_elm, data_hanley, date):
        win = GraphWin("Histogram", 900, 600)
        win.setBackground("lightgray")

        # Title
        title = Text(Point(400, 40), f"Histogram of Vehicle Frequency per Hour ({date})")
        title.setSize(14)
        title.setStyle("bold")
        title.draw(win)

        # Axes
        x_axis = Line(Point(50, 500), Point(750, 500))  # x-axis horizontal line
        x_axis.draw(win)
        y_axis = Line(Point(40, 500), Point(40, 100))  # y-axis vertical line
        y_axis.draw(win)

        # Horizontal line for the X-axis (completing the bottom axis line)
        x_axis_line = Line(Point(40, 502), Point(750, 502))  # Drawing the X-axis line
        x_axis_line.setWidth(2)  # You can adjust the width if needed
        x_axis_line.draw(win)

        # Labels for x-axis (hours)
        for i in range(24):
            x = 50 + i * 30
            hour_label = Text(Point(x, 520), f"{i:02}")
            hour_label.setSize(10)
            hour_label.draw(win)

        # Labels for y-axis (frequency)
        for i in range(0, 0, ):
            y = 500 - i * 8
            freq_label = Text(Point(30, y), str(i))
            freq_label.setSize(10)
            freq_label.draw(win)
            grid_line = Line(Point(50, y), Point(750, y))
            grid_line.setFill("lightblue")
            grid_line.draw(win)

        # Bars
        for i in range(24):
            x_base = 50 + i * 30
            elm_height = data_elm.get(str(i), 0) * 4
            hanley_height = data_hanley.get(str(i), 0) * 4

            # Elm Avenue bar (green)
            elm_bar = Rectangle(Point(x_base - 10, 500), Point(x_base, 500 - elm_height))
            elm_bar.setFill("green")
            elm_bar.draw(win)

            # Hanley Highway bar (red)
            hanley_bar = Rectangle(Point(x_base, 500), Point(x_base + 10, 500 - hanley_height))
            hanley_bar.setFill("red")
            hanley_bar.draw(win)

            # Values on top of bars
            elm_value = Text(Point(x_base - 5, 495 - elm_height), str(data_elm.get(str(i), 0)))
            elm_value.setSize(8)
            elm_value.draw(win)

            hanley_value = Text(Point(x_base + 5, 495 - hanley_height), str(data_hanley.get(str(i), 0)))
            hanley_value.setSize(8)
            hanley_value.draw(win)

        # Legend
        legend_elm = Rectangle(Point(560, 120), Point(535, 140))
        legend_elm.setFill("green")
        legend_elm.draw(win)
        legend_text_elm = Text(Point(680, 130), "Elm Avenue/Rabbit Road")
        legend_text_elm.setSize(10)
        legend_text_elm.draw(win)

        legend_hanley = Rectangle(Point(560, 150), Point(535, 170))
        legend_hanley.setFill("red")
        legend_hanley.draw(win)
        legend_text_hanley = Text(Point(680, 160), "Hanley Highway/Westway")
        legend_text_hanley.setSize(10)
        legend_text_hanley.draw(win)

        # Wait for click to close
        win.getMouse()
        win.close()

    def process_csv_data(self, file_path, data):
        print(f"\tData file selected: {file_path}")

        vehicle_count = len(data)
        truck_count = sum(1 for item in data if item.get('VehicleType') == 'Truck')
        electric_vehicle_count = sum(1 for item in data if item.get('elctricHybrid') == 'True')
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

        hourly_data_elm = {str(i): 0 for i in range(24)}
        hourly_data_hanley = {str(i): 0 for i in range(24)}

        for item in data:
            if 'timeOfDay' in item:
                hour = str(int(item['timeOfDay'].split(":")[0]))  # Ensure no leading zero
                if item.get('JunctionName') == 'Elm Avenue/Rabbit Road':
                    hourly_data_elm[hour] += 1
                elif item.get('JunctionName') == 'Hanley Highway/Westway':
                    hourly_data_hanley[hour] += 1


        if hourly_data_hanley:
            peak_hour_count = max(hourly_data_hanley.values())
            peak_hours = [
                f"Between {hour}:00 and {int(hour) + 1}:00"
                for hour, count in hourly_data_hanley.items()
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
            "The total number of two-wheeled vehicles for this date is": two_wheeled_vehicle_count,
            "The total number of Busses leaving Elm Avenue/Rabbit Road heading North is": bus_north_count,
            "The total number of Vehicles through both junctions not turning left or right is": count_not_turning,
            "The percentage of total vehicles recorded that are trucks for this date is": f"{truck_percentage}%",
            "The average number of Bicycles per hour for this date is": bicycle_per_hour,
            "The total number of Vehicles recorded as over the speed limit for this date is": over_speed_limit_count,
            "The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is": elm_avenue_vehicle_count,
            "The total number of vehicles recorded through Hanley Highway/Westway junction is": hanley_highway_vehicle_count,
            f"{scooter_percentage_elm}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.": "",
            "The highest number of vehicles in an hour on Hanley Highway/Westway": peak_hour_count,
            "The time or times of the peak (busiest) traffic hour (or hours) on Hanley Highway/Westway": ", ".join(peak_hours),
            "The number of hours of rain for this date is ": rain_hours
        }

        self.display_outcomes(outcomes)
        self.draw_histogram(hourly_data_elm, hourly_data_hanley, file_path)

        self.save_to_file(outcomes)

    def display_outcomes(self, outcomes):
        for key, value in outcomes.items():
            print(f"{key}: {value}")

    def save_to_file(self, outcomes, file_name="results.txt"):
        try:
            with open(file_name, "a") as file:
                file.write("\n*******************\n")
                for key, value in outcomes.items():
                    file.write(f"{key}: {value}\n")
            print(f"Data appended to {file_name}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def handle_user_interaction(self):
        while True:
            print("\nMenu:")
            print("1. Load a CSV file")
            print("2. Process current data")
            print("3. Clear data")
            print("4. Quit")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                file_path = self.validate_date_input()
                if file_path:
                    self.current_data = self.load_csv_file(file_path)

            elif choice == '2':
                if self.current_data:
                    self.process_csv_data(file_path, self.current_data)
                else:
                    print("No data loaded. Please load a CSV file first.")

            elif choice == '3':
                self.clear_previous_data()
                print("Previous data cleared.")

            elif choice == '4':
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.handle_user_interaction()
