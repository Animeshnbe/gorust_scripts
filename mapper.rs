use std::io::{Write, BufReader, BufRead, ErrorKind};
use std::fs::File;
use std::path::Path;
use std::collections::HashMap;
use std::str::FromStr;
use std::cmp::Ordering;

fn main() {
    struct Customer {
        name: String,
        address: String,
        balance: f32,
    }

    let mut bob: Customer = Customer{
        name: String::from("Bob Smith"),
        address: String::from("123 Main Street"),
        balance: 100.0,
    }

    let mut heroes = HashMap::new();
    heroes.insert("Superman", "Clark Kent");
    heroes.insert("Batman", "Bruce Wayne");
    heroes.insert("Spiderman", "Peter Parker");
    heroes.insert("Iron Man", "Tony Stark");

    for (k, v) in heroes.iter() {
        println!("{} -> {}", k, v);
    }

    println!("Length: {}", heroes.len());

    if heroes.contains_key(&"Batman") {
        let batman = heroes.get(&"Batman");
        match batman {
            Some(v) => println!("Batman is {}", v),
            None => println!("Batman does not exist"),
        }
    }
}