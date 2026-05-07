from functions.write_file import write_file

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculaotr", "/tmp/temp.txt", "this should not be allowed"))
