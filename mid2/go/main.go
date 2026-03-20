package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	"sync"

	"mid2/calc"
)

type job struct {
	req  calc.Request
	resp chan calc.Response
}

func main() {
	input, err := io.ReadAll(os.Stdin)
	if err != nil {
		fmt.Fprintln(os.Stdout, "ERROR read stdin:", err)
		os.Exit(1)
		return
	}

	fields := strings.Fields(string(input))
	if len(fields) < 3 {
		fmt.Fprintln(os.Stdout, "ERROR expected: <task> <a> <b>")
		os.Exit(1)
	}

	req := calc.Request{Task: fields[0]}
	a, err := strconv.ParseFloat(fields[1], 64)
	if err != nil {
		fmt.Fprintln(os.Stdout, "ERROR invalid a:", err)
		os.Exit(1)
		return
	}
	b, err := strconv.ParseFloat(fields[2], 64)
	if err != nil {
		fmt.Fprintln(os.Stdout, "ERROR invalid b:", err)
		os.Exit(1)
		return
	}
	req.A = a
	req.B = b

	// Background processing: handle the request in a worker goroutine.
	jobs := make(chan job, 1)
	respCh := make(chan calc.Response, 1)

	var wg sync.WaitGroup
	wg.Add(1)
	fmt.Fprintln(os.Stderr, "[main goroutine] dispatching job")
	go func() {
		defer wg.Done()
		fmt.Fprintln(os.Stderr, "[worker goroutine] started")
		for j := range jobs {
			fmt.Fprintln(os.Stderr, "[worker goroutine] processing task:", j.req.Task)
			res, computeErr := calc.Compute(j.req)
			if computeErr != nil {
				j.resp <- calc.Response{Error: computeErr.Error()}
				continue
			}
			j.resp <- res
		}
	}()

	jobs <- job{req: req, resp: respCh}
	close(jobs)
	wg.Wait()

	res := <-respCh
	if res.Error != "" {
		fmt.Fprintln(os.Stdout, "ERROR", res.Error)
		os.Exit(1)
		return
	}

	// Plain text output: easier to consume from Python without JSON.
	fmt.Fprintf(os.Stdout, "%g\n", res.Result)
}

