package calc

import (
	"errors"
	"math"
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

// Compute performs the requested operation and returns either a result or an error.
func Compute(req Request) (Response, error) {
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

