import math

def calculate_angle_of_view(sensor_width, focal_length, crop_factor):
    sensor_diagonal = math.sqrt(sensor_width**2 + (sensor_width/crop_factor)**2)
    angle_of_view = 2 * math.atan(sensor_diagonal / (2 * focal_length))
    return math.degrees(angle_of_view)

# Example usage
sensor_width = 24  # mm
focal_length = 50  # mm
crop_factor = 1.5
angle_of_view = calculate_angle_of_view(sensor_width, focal_length, crop_factor)
print(f"Angle of view: {angle_of_view:.2f} degrees")
