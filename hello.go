package main

import "fmt"

func main() {
	fmt.Println("Ticket booking app")
	var num_tickets = 47 //:= as syntactic sugar
	num_tickets++
	var cust_name string

	var name_arr [10]string
	bookings := []string{} //dynamic size

	name_arr[0] = "Test"
	bookings = append(bookings, "Test1")

	fmt.Scan(&cust_name)
	fmt.Println(num_tickets, "available for", cust_name)
	fmt.Printf("Booked yesterday %v", name_arr)

	for _, val := range bookings {
		//infini
		fmt.Println("Some ", val)
	}
}
