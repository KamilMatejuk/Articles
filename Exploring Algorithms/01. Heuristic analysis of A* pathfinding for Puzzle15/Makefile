CC=g++
PARAMS=-std=c++17

all: main

main: main.o puzzle.o solver.o utils.o heuristic.o settings.o
	$(CC) $(PARAMS) -o main main.o puzzle.o solver.o utils.o heuristic.o settings.o

%.o: %.cpp %.h
	$(CC) -c -o $@ $<

run:
	./main

start: clean main run

push: clean
	git status
	git add ..
	git status
	git commit -m "commit"
	git push

.PHONY: clean
clean:
	rm -f main *.o *~
