#python one.py

#__name__ # Built in variable, gets assigned a string

def func():
    print("FUNC() in ONE.PY")

print("TOP LEVEL in ONE.PY")

# Basically used more for code organization, usually don't see an else statement
if __name__ == "__main__":
    print('ONE.PY is being run directly!')
else:
    print('ONE.PY has been imported!')