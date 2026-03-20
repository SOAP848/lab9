package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"

	"mid4/calc"
)

func main() {
	input, err := io.ReadAll(os.Stdin)
	if err != nil {
		writeErrorAndExit(fmt.Errorf("read stdin: %w", err), 1)
		return
	}

	var req calc.Request
	if err := json.Unmarshal(input, &req); err != nil {
		writeErrorAndExit(fmt.Errorf("invalid json: %w", err), 1)
		return
	}

	res, err := calc.Compute(req)
	if err != nil {
		_ = json.NewEncoder(os.Stdout).Encode(calc.Response{Error: err.Error()})
		os.Exit(1)
		return
	}

	_ = json.NewEncoder(os.Stdout).Encode(res)
}

func writeErrorAndExit(err error, code int) {
	_ = json.NewEncoder(os.Stdout).Encode(calc.Response{Error: err.Error()})
	os.Exit(code)
}

