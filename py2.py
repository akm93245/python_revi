import math

def calculate_cone_area(radius, slant_height):
    base_area = math.pi * radius ** 2
    lateral_area = math.pi * radius * slant_height
    total_area = base_area + lateral_area
    radius =  float(input("Enter radius of cone's base : "))
    slant_height =  float(input("Enter slant height of cone : "))
    
    cone_area =  calculate_cone_area(radius,slant_height)
    print("The area of cone is : ", cone_area)
    
    #clcoding.com