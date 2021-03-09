import pandas as pd
from datetime import date
import os
import json

def calc_year_month(dob):
    
    today = date.today()
    try:
        dob_list = dob.split('/')
    except Exception:
        dob_list = today.strftime("%m/%d/%Y").split('/') 
    
    year = today.year-int(dob_list[2])   
    month = today.month-int(dob_list[0])
    if month < 0:
        month = -month
    
    Years = ' Years'
    Months = ' Months'
    
    if year == 1:
        Years = ' Year'
    if month == 1:
        Months =' Month'
    return str(year) + Years + " " + str(month) + Months

def to_json(df, json_path, category):
    data = df.to_dict('records')
    data = {category + "RecordCount": len(df), "data": data}
    if not os.path.exists(json_path):
        os.mkdir(json_path)
    filename = category + ".json"
    file = open(os.path.join(json_path, filename), "w")
    file.write(json.dumps(data, indent=4))
    file.close()

def csv_json(json_path):
    csv_path = "D:\ADMIN\Desktop\CSV2JSON-Inheritence\csv\input.csv"
    df = pd.read_csv(csv_path) 
    
    df['fullName'] = df['firstname'] + " " + df['lastname']
    df['age'] = df['dob'].apply(calc_year_month)

    df.loc[df['total_marks']*0.1 >= 90.0, "grade"] = "A+"
    df.loc[(df['total_marks']*0.1 >= 80.0) & (df['total_marks']*0.1 <= 89.0), "grade"] = "A"
    df.loc[(df['total_marks']*0.1 >= 70.0) & (df['total_marks']*0.1 <= 79.0), "grade"] = "B+"
    df.loc[(df['total_marks']*0.1 >= 60.0) & (df['total_marks']*0.1 <= 69.0), "grade"] = "B"
    df.loc[(df['total_marks']*0.1 >= 50.0) & (df['total_marks']*0.1 <= 59.0), "grade"] = "C"
    df.loc[(df['total_marks']*0.1 >= 0.0) & (df['total_marks']*0.1 <= 49.0), "grade"] = "D"

    df['servicePeriod'] = df['doj'].notnull().apply(calc_year_month)

    df.loc[df["gender"] == "m", "gender"] = "Male"
    df.loc[df["gender"] == "f", "gender"] = "Female"

    df['salary'] = df['salary'].apply(lambda x: "{:,.0f}".format(x))


    df.rename(columns = {'previous_school': 'previousSchool', 'total_marks': 'totalMarks', 'class_teacher_of': 'classTeacher', 
                   'emp_no': 'empNo', 'aadhar_number': 'aadhar', 'contact_number': 'contactNumber', 'roll_no': 'rollNo',
                   'class': 'className', 'sec_percent': 'secPercent', 'hs_stream': 'hsStream'}, inplace=True )
    
    
    teacher_df = df.loc[df['category'] == "teacher"]
    student_df = df.loc[df['category'] == "student"]
    

    teacher_df = teacher_df[['id', 'fullName', 'gender', 'dob', 'age', 'aadhar', 'city', 'contactNumber',
               'empNo', 'classTeacher', 'doj', 'servicePeriod', 'previousSchool', 'post', 'salary']]
    
    student_df = student_df[['id', 'fullName', 'gender', 'dob', 'age', 'aadhar', 'city', 'contactNumber',
             'rollNo', 'className', 'totalMarks', 'grade', 'secPercent', 'hsStream']]
    
    to_json(teacher_df, json_path, "teacher")
    to_json(student_df, json_path, "student")

json_path = input('Enter Your json Path:')

csv_json(json_path)
