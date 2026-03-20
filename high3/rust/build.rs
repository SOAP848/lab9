fn main() {
    // Tell cargo to rerun this script if the wrapper changes
    println!("cargo:rerun-if-changed=src/lib.rs");
    // No cbindgen for simplicity
}