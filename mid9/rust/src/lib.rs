
pub fn sieve_of_eratosthenes(n: usize) -> Vec<bool> {
    if n < 2 {
        return vec![false; n + 1];
    }
    let mut is_prime = vec![true; n + 1];
    is_prime[0] = false;
    is_prime[1] = false;
    let limit = (n as f64).sqrt() as usize;
    for i in 2..=limit {
        if is_prime[i] {
            let mut j = i * i;
            while j <= n {
                is_prime[j] = false;
                j += i;
            }
        }
    }
    is_prime
}

pub fn primes_upto(n: usize) -> Vec<usize> {
    let is_prime = sieve_of_eratosthenes(n);
    (2..=n).filter(|&i| is_prime[i]).collect()
}

pub fn count_primes(n: usize) -> usize {
    let is_prime = sieve_of_eratosthenes(n);
    is_prime.iter().skip(2).filter(|&&b| b).count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sieve_basic() {
        let primes = sieve_of_eratosthenes(10);
        assert_eq!(primes[2], true);
        assert_eq!(primes[3], true);
        assert_eq!(primes[4], false);
        assert_eq!(primes[5], true);
        assert_eq!(primes[9], false);
        assert_eq!(primes[10], false);
    }

    #[test]
    fn test_primes_upto() {
        let primes = primes_upto(20);
        assert_eq!(primes, vec![2, 3, 5, 7, 11, 13, 17, 19]);
    }

    #[test]
    fn test_count_primes() {
        assert_eq!(count_primes(10), 4);
        assert_eq!(count_primes(30), 10);
    }
}