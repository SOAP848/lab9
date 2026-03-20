package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
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
		writeResponseAndExit(calc.Response{Error: fmt.Sprintf("read stdin: %v", err)}, 1)
		return
	}

	var req calc.Request
	if err := json.Unmarshal(input, &req); err != nil {
		writeResponseAndExit(calc.Response{Error: fmt.Sprintf("invalid json: %v", err)}, 1)
		return
	}

	// Background processing: handle the request in a worker goroutine.
	jobs := make(chan job, 1)
	respCh := make(chan calc.Response, 1)

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		for j := range jobs {
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
	_ = json.NewEncoder(os.Stdout).Encode(res)
	if res.Error != "" {
		os.Exit(1)
	}
}

func writeResponseAndExit(res calc.Response, code int) {
	_ = json.NewEncoder(os.Stdout).Encode(res)
	os.Exit(code)
}

