package calc

import (
	"errors"
	"math"
)

type Request struct {
	Task string
	A    float64
	B    float64
}

type Response struct {
	Result float64
	Error  string
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

