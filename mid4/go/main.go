package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math"
	"os"
)

type Request struct {
	Task string  `json:"task"`
	A    float64 `json:"a"`
	B    float64 `json:"b"`
}

type Response struct {
	Result float64 `json:"result,omitempty"`
	Error  string  `json:"error,omitempty"`
}

func main() {
	input, err := io.ReadAll(os.Stdin)
	if err != nil {
		writeErrorAndExit(fmt.Errorf("read stdin: %w", err), 1)
		return
	}

	var req Request
	if err := json.Unmarshal(input, &req); err != nil {
		writeErrorAndExit(fmt.Errorf("invalid json: %w", err), 1)
		return
	}

	res, err := handle(req)
	if err != nil {
		_ = json.NewEncoder(os.Stdout).Encode(Response{Error: err.Error()})
		os.Exit(1)
		return
	}

	_ = json.NewEncoder(os.Stdout).Encode(res)
}

func handle(req Request) (Response, error) {
	switch req.Task {
	case "add":
		return Response{Result: req.A + req.B}, nil
	case "mul":
		return Response{Result: req.A * req.B}, nil
	case "pow":
		return Response{Result: math.Pow(req.A, req.B)}, nil
	default:
		return Response{}, errors.New("unknown task: " + req.Task)
	}
}

func writeErrorAndExit(err error, code int) {
	_ = json.NewEncoder(os.Stdout).Encode(Response{Error: err.Error()})
	os.Exit(code)
}

