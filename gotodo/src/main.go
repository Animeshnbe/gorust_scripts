package main

import (
	"flag"
	"fmt"
	"os"
	"github.com/Animeshnbe/gotodo"
)

const (
	todoFile = ".todos.json"
)

func main() {
	add := flag.Bool("add", false, "add a new todo")
	complete := flag.Int("complete", 0, "complete a todo")
	del := flag.Int("delete", 0, "remove a todo")

	flag.Parse()

	todos := &todo.Todos{}
	if err := todos.Load(todoFile); err != nil {
		fmt.Fprintln(os.Stderr,err.Error())
		os.Exit(1)
	}
	switch {
	case *add: todos.Add("Sample todo")
		err := todos.Store(todoFile)
		if err != nil {
			fmt.Fprintln(os.Stderr,err.Error())
		}
	case *complete > 0:
		err := todos.Complete(*complete)
		if err != nil {
			fmt.Fprintln(os.Stderr,err.Error())
		}
		err = todos.Store(todoFile)
		if err != nil {
			fmt.Fprintln(os.Stderr,err.Error())
		}
	case *del > 0:
		err := todos.Remove(*del)
		if err != nil {
			fmt.Fprintln(os.Stderr,err.Error())
		}
		err = todos.Store(todoFile)
		if err != nil {
			fmt.Fprintln(os.Stderr,err.Error())
		}
	default: fmt.Fprintln(os.Stdout,"invalid command")
		os.Exit(1)
	}
}