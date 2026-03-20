use std::env;
use std::time::Instant;
use sieve::{sieve_of_eratosthenes, count_primes};

fn main() {
    let args: Vec<String> = env::args().collect();
    let n = if args.len() > 1 {
        args[1].parse::<usize>().expect("Ожидается целое число")
    } else {
        1_000_000
    };
    let iterations = if args.len() > 2 {
        args[2].parse::<usize>().expect("Ожидается целое число")
    } else {
        10
    };

    println!("Бенчмарк Rust решета Эратосфена до n = {}", n);
    println!("Итераций: {}", iterations);

    let mut times = Vec::with_capacity(iterations);
    for _ in 0..iterations {
        let start = Instant::now();
        let _ = sieve_of_eratosthenes(n);
        let duration = start.elapsed();
        times.push(duration.as_secs_f64());
    }

    let total: f64 = times.iter().sum();
    let mean = total / iterations as f64;
    let min = times.iter().fold(f64::INFINITY, |a, &b| a.min(b));
    let max = times.iter().fold(0.0f64, |a, &b| a.max(b));
    let std_dev = if iterations > 1 {
        let variance = times.iter().map(|&t| (t - mean).powi(2)).sum::<f64>() / (iterations - 1) as f64;
        variance.sqrt()
    } else {
        0.0
    };

    println!("Результаты:");
    println!("  Среднее время: {:.6} сек", mean);
    println!("  Минимум: {:.6} сек", min);
    println!("  Максимум: {:.6} сек", max);
    println!("  Стандартное отклонение: {:.6} сек", std_dev);

    // Также выведем количество простых чисел для проверки
    let count = count_primes(n);
    println!("  Количество простых до {}: {}", n, count);
}