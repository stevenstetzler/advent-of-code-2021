package main

import (
	"fmt"
	"os"
	"log"
	"bufio"
	"strings"
	"strconv"
)

func main() {
	file, err := os.Open("input")
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	horizontal_position := 0
	aim := 0
	depth := 0
	for scanner.Scan() {
		text := scanner.Text()
		line := strings.Split(text, " ")
		direction := line[0]
		_movement, err := strconv.ParseInt(line[1], 10, 0)
		if err != nil {
			log.Fatal(err)
		}
		movement := int(_movement)
		if direction == "forward" {
			horizontal_position += movement
			depth += movement * aim
		} else if direction == "up" {
			aim -= movement
		} else if direction == "down" {
			aim += movement
		} else {
			log.Fatal("bad direction")
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	fmt.Printf("%d %d %d\n", depth, horizontal_position, horizontal_position * depth)
}
