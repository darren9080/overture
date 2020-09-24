import json

data = '''
    "name" = "chuck",
    "phone" = {
        "type" :"intl",
        "number" : "+1 123 121 1231"
    },
    "email" = {
        "hide" = "yes"
    }'''

info = json.loads(data)
print("Name: ", info["name"] )
print("Hide: ", infor["email"]["hide"])
