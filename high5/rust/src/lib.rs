use std::ffi::c_uint;

/// Реализация решета Эратосфена на Rust.
/// Возвращает указатель на массив простых чисел, за которым следует 0.
/// Вызывающая сторона должна освободить память с помощью free_sieve_result.
#[no_mangle]
pub extern "C" fn sieve_rust(limit: c_uint) -> *mut c_uint {
    if limit < 2 {
        // Возвращаем массив из одного элемента 0
        let mut result = vec![0u32].into_boxed_slice();
        let ptr = result.as_mut_ptr();
        std::mem::forget(result);
        ptr
    } else {
        let limit_usize = limit as usize;
        let mut sieve = vec![true; limit_usize + 1];
        sieve[0] = false;
        sieve[1] = false;
        let sqrt_limit = (limit_usize as f64).sqrt() as usize;
        for i in 2..=sqrt_limit {
            if sieve[i] {
                let mut j = i * i;
                while j <= limit_usize {
                    sieve[j] = false;
                    j += i;
                }
            }
        }
        let mut primes: Vec<u32> = sieve
            .iter()
            .enumerate()
            .filter_map(|(i, &is_prime)| if is_prime { Some(i as u32) } else { None })
            .collect();
        // Добавляем 0 в конец как маркер
        primes.push(0);
        let mut boxed = primes.into_boxed_slice();
        let ptr = boxed.as_mut_ptr();
        std::mem::forget(boxed);
        ptr
    }
}

/// Освобождает память, выделенную sieve_rust.
/// Принимает указатель, возвращённый sieve_rust.
#[no_mangle]
pub extern "C" fn free_sieve_result(ptr: *mut c_uint) {
    if !ptr.is_null() {
        unsafe {
            // Находим длину, подсчитывая элементы до нуля
            let mut len = 0;
            while *ptr.add(len) != 0 {
                len += 1;
            }
            // Восстанавливаем Box с правильной длиной (len + 1 для нуля)
            let _ = Box::from_raw(std::slice::from_raw_parts_mut(ptr, len + 1));
        }
    }
}