import sys

def print_words(filename):
  f = open(filename)
  for line in f:
    for word in line.split():
    	print word

def main():
  filename = sys.argv[0]
  print_words(filename)

if __name__ == '__main__':
  main()