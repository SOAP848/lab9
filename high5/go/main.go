package main

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"
)

// sieveGo возвращает простые числа до limit (включительно) используя решето Эратосфена.
func sieveGo(limit int) []int {
	if limit < 2 {
		return []int{}
	}
	sieve := make([]bool, limit+1)
	for i := 2; i <= limit; i++ {
		sieve[i] = true
	}
	for i := 2; i*i <= limit; i++ {
		if sieve[i] {
			for j := i * i; j <= limit; j += i {
				sieve[j] = false
			}
		}
	}
	primes := []int{}
	for i, isPrime := range sieve {
		if isPrime {
			primes = append(primes, i)
		}
	}
	return primes
}

// handleSieve обрабатывает HTTP запрос с параметром limit.
func handleSieve(w http.ResponseWriter, r *http.Request) {
	limitStr := r.URL.Query().Get("limit")
	if limitStr == "" {
		http.Error(w, "Missing 'limit' query parameter", http.StatusBadRequest)
		return
	}
	limit, err := strconv.Atoi(limitStr)
	if err != nil || limit < 0 {
		http.Error(w, "Invalid 'limit': must be a non-negative integer", http.StatusBadRequest)
		return
	}
	primes := sieveGo(limit)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(primes)
}

func main() {
	http.HandleFunc("/sieve", handleSieve)
	port := "5000"
	log.Printf("Starting Go sieve server on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}