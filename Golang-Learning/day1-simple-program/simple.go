package main

import "fmt"

func searchArray(incomingArray [10]int, searchNum int) int {
	var searchedIndex int = -1;
	for index := range incomingArray{
		if incomingArray[index] == searchNum{
			searchedIndex = index
			break
		}
	}
	return searchedIndex
}

func printArray(incomingArray [10]int){
	for index := range len(incomingArray){
		fmt.Println(incomingArray[index])
	}
}

func main() {
	var newArray[10]int
	for index := range 10 {
		newArray[index] = index * 3
	}
	printArray(newArray)

	var foundIndex int = searchArray(newArray, 6)
	fmt.Println("Found index at: ", foundIndex)
}
