from PIL import Image
ans = ""

while ans != "no":
    ans = input("Enter path name: ")
    image = Image.open(ans)
    image = image.resize((100,100))
    image.save(ans)
    