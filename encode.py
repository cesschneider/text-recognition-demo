import base64

with open("testocr.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    
print(encoded_string.decode())
with open('encoded.b64', "wb") as file: 
    file.write(encoded_string)