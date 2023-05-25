// test program
fn main() {
    let mut i=1;
    loop {
        if i==5 {
            break;
        }
        println!("Iter {:?}",i);
        i=i+1;
    }
    println!("Hello, world!");
}
