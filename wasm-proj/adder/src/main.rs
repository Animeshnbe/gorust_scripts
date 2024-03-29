use std::io::stdin;
fn sum_fn(arr: Vec<&str>) ->i32 {
    arr.into_iter()
        .map(|elem| elem.parse::<i32>().unwrap_or(0))
        .sum::<i32>()
}

fn main() {
    println!("Welcome to adder of space separated numbers!");
    loop {
        let mut buffer = String::new();
        stdin().read_line(&mut buffer).unwrap();
        let splits = buffer.split_whitespace().collect();
        
        println!("{:?}",splits);
        let sum = sum_fn(splits);
        println!("Sum = {}",sum);
    }
}
