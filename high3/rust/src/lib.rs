use std::os::raw::c_int;

/// Returns a vector of primes up to limit (inclusive) using Sieve of Eratosthenes.
fn sieve_of_eratosthenes(limit: usize) -> Vec<usize> {
    if limit < 2 {
        return Vec::new();
    }
    let mut is_prime = vec![true; limit + 1];
    is_prime[0] = false;
    is_prime[1] = false;
    let sqrt_limit = (limit as f64).sqrt() as usize;
    for i in 2..=sqrt_limit {
        if is_prime[i] {
            let mut j = i * i;
            while j <= limit {
                is_prime[j] = false;
                j += i;
            }
        }
    }
    is_prime
        .into_iter()
        .enumerate()
        .filter_map(|(i, prime)| if prime { Some(i) } else { None })
        .collect()
}

/// FFI‑compatible function that returns the number of primes up to limit.
/// The result is stored in a buffer provided by the caller.
///
/// # Safety
/// The caller must ensure `out` points to a buffer of size at least `limit + 1`
/// and that `out_len` is the actual length of that buffer.
#[no_mangle]
pub unsafe extern "C" fn sieve_primes(limit: c_int, out: *mut c_int, out_len: c_int) -> c_int {
    if limit < 0 || out.is_null() || out_len <= 0 {
        return -1;
    }
    let limit = limit as usize;
    let primes = sieve_of_eratosthenes(limit);
    let count = primes.len().min(out_len as usize);
    for (i, &p) in primes.iter().take(count).enumerate() {
        *out.add(i) = p as c_int;
    }
    count as c_int
}

/// FFI‑compatible function that returns the count of primes up to limit.
#[no_mangle]
pub extern "C" fn count_primes(limit: c_int) -> c_int {
    if limit < 0 {
        return -1;
    }
    let primes = sieve_of_eratosthenes(limit as usize);
    primes.len() as c_int
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sieve_basic() {
        let primes = sieve_of_eratosthenes(10);
        assert_eq!(primes, vec![2, 3, 5, 7]);
    }

    #[test]
    fn test_sieve_empty() {
        let primes = sieve_of_eratosthenes(1);
        assert!(primes.is_empty());
    }

    #[test]
    fn test_sieve_large() {
        let primes = sieve_of_eratosthenes(30);
        assert_eq!(primes, vec![2, 3, 5, 7, 11, 13, 17, 19, 23, 29]);
    }

    #[test]
    fn test_count_primes() {
        assert_eq!(count_primes(10), 4);
        assert_eq!(count_primes(0), 0);
        assert_eq!(count_primes(2), 1);
    }

    #[test]
    fn test_sieve_primes_ffi() {
        let limit = 20;
        let mut buffer = vec![0; 30];
        let count = unsafe {
            sieve_primes(
                limit,
                buffer.as_mut_ptr(),
                buffer.len() as c_int,
            )
        };
        assert_eq!(count, 8);
        let result: Vec<i32> = buffer.into_iter().take(count as usize).collect();
        assert_eq!(result, vec![2, 3, 5, 7, 11, 13, 17, 19]);
    }
}