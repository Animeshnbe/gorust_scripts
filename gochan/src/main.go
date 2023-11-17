package main

import (
	"fmt"
	// "sync"
	// "io"
	// "net"
	// "os"
	"time"
)

func fib(max int, ch chan int){
	f := make([]int, max)
	f[0] = 1
	f[1] = 1
	ch <- f[0]
	ch <- f[1]
	for i := 2; i<max; i++ {
		f[i] = f[i-1] + f[i-2]
		ch <- f[i]
	}
	close(ch)
}
func countDown(n int){
	for n>=0 {
		fmt.Println(n)
		n--
		time.Sleep(time.Millisecond * 500)
	}
}
func main(){
	// listener, err := net.Listen("tcp", "localhost:9000")

	// if (err != nil){
	// 	fmt.Println(err)
	// 	os.Exit(1)
	// }

	// for {
	// 	conn, err := listener.Accept()
	// 	if err != nil {
	// 		fmt.Println(err)
	// 		continue
	// 	}

	// 	go func ()  {
	// 		for {
	// 			_, err := io.WriteString(conn, time.Now().Format("15:05:05\n"))
	// 			if err != nil {
	// 				return
	// 			}
	// 			time.Sleep(time.Second)
	// 		}
	// 	}()
	// }

	// var wg sync.WaitGroup

	// wg.Add(1)
	// go func(){
	// 	countDown(10)
	// 	wg.Done()
	// }()
	// wg.Add(1)
	// go func(){
	// 	countDown(5)
	// 	wg.Done()
	// }()

	// wg.Wait()

	ch := make(chan int)
	go fib(10, ch)
	for msg := range ch{
		// fmt.Println("%d\n", <- ch)
		fmt.Println(msg)
	}
}