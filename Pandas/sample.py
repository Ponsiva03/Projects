# Create a new file and write data to it
with open('new_file.txt', 'w') as file:
    file.write('This is a new file.\n')
    file.write('Hello, World!\n')

# Read from the file
with open('new_file.txt', 'r') as file:
    content = file.read()
    print('Content read from the file:')
    print(content)

# Append more data to the file
with open('new_file.txt', 'a') as file:
    file.write('Appending more data to the file.\n')

# Read and print the file line by line
with open('new_file.txt', 'r') as file:
    print('\nContent read line by line:')
    for line in file:
        print(line.strip())  # Use strip to remove the newline character
  # Use strip to remove the newline character

