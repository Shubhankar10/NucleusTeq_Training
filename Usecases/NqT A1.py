#Usecase 1
# Consider a scenario where you're developing a system to manage training sessions for a software development company. The JSON snippet provided represents one such training session named 'Python Training.' In this scenario, you have multiple training sessions with different instructors, dates, and participants. For this you need to handle booleans, integers, strings, floats a lists and dictionaries.

#Simple Json parsing


import json

json_data = '''
{
  "name": "Python Training",
  "date": "April 19, 2024",
  "completed": true,
  "instructor": {
    "name": "XYZ",
    "website": "http://pqr.com/"
  },
  "participants": [
    {
      "name": "Participant 1",
      "email": "email1@example.com"
    },
    {
      "name": "Participant 2",
      "email": "email2@example.com"
    }
  ]
}
'''

#Understands string to json format
training_session = json.loads(json_data)

print("Training Name:", training_session["name"])
print("Date:", training_session["date"])
print("Completed:", training_session["completed"])

print("Instructor Name:", training_session["instructor"]["name"])
print("Instructor Website:", training_session["instructor"]["website"])

print("Participants:")
for participant in training_session["participants"]:
    print("- Name:", participant["name"])
    print("  Email:", participant["email"])
