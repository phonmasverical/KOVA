# KOVA Usage Guide

> **KOVA -- Forged for clarity. Built for speed.**
>
> Version 1.0.0 | File extension: `.kva` | Command: `kovarun`

---

## Table of Contents

- [1. Getting Started](#1-getting-started)
- [2. Basic Syntax](#2-basic-syntax)
- [3. Variables & Constants](#3-variables--constants)
- [4. Data Types](#4-data-types)
- [5. Operators](#5-operators)
- [6. Control Flow](#6-control-flow)
  - [6.1 Conditionals](#61-conditionals)
  - [6.2 Loops](#62-loops)
  - [6.3 Pattern Matching](#63-pattern-matching)
- [7. Functions](#7-functions)
- [8. Object-Oriented Programming](#8-object-oriented-programming)
  - [8.1 Shapes (Classes)](#81-shapes-classes)
  - [8.2 Inheritance](#82-inheritance)
- [9. Error Handling](#9-error-handling)
- [10. Modules](#10-modules)
- [11. Defer](#11-defer)
- [12. Built-in Functions Reference](#12-built-in-functions-reference)
  - [12.1 I/O Functions](#121-io-functions)
  - [12.2 Type Functions](#122-type-functions)
  - [12.3 Math Functions](#123-math-functions)
  - [12.4 String Functions](#124-string-functions)
  - [12.5 Array Functions](#125-array-functions)
  - [12.6 Map Functions](#126-map-functions)
  - [12.7 File I/O](#127-file-io)
  - [12.8 System Functions](#128-system-functions)
- [13. String Methods (dot notation)](#13-string-methods-dot-notation)
- [14. Array Methods (dot notation)](#14-array-methods-dot-notation)
- [15. REPL Commands](#15-repl-commands)
- [16. Security Features](#16-security-features)
- [17. Complete Example Programs](#17-complete-example-programs)
- [18. Keyword Quick Reference](#18-keyword-quick-reference)

---

## 1. Getting Started

### Installation

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/user/KOVA.git
cd KOVA
```

No additional dependencies are required -- KOVA runs on Python 3.8+.

### Running Programs

Execute a KOVA source file with the `kovarun` command:

```bash
kovarun hello.kva
```

### Interactive REPL

Launch the interactive REPL by running `kovarun` with no arguments:

```bash
kovarun
```

The REPL displays the KOVA banner and a prompt where you can type expressions and statements interactively. Results are printed automatically. This is a great way to experiment with the language.

```
  KOVA Programming Language v1.0.0
  Type .help for help, .exit to quit

kova> grab name = "World"
kova> emit("Hello, {name}!")
Hello, World!
```

### CLI Options

| Command                  | Description                  |
|--------------------------|------------------------------|
| `kovarun filename.kva`   | Run a KOVA source file       |
| `kovarun`                | Launch the interactive REPL  |
| `kovarun --version`      | Print version and exit       |
| `kovarun -v`             | Print version and exit       |
| `kovarun --help`         | Show help message            |
| `kovarun -h`             | Show help message            |

### File Extension

All KOVA source files use the `.kva` extension.

### Creating Your First File

Use any text editor to create a KOVA source file:

```bash
nano hello.kva
```

Write a simple program:

```
-- hello.kva -- Your first KOVA program
emit("Hello, KOVA!")
```

Run it:

```bash
kovarun hello.kva
```

Output:

```
Hello, KOVA!
```

---

## 2. Basic Syntax

### Comments

**Single-line comments** begin with `--` and continue to the end of the line:

```
-- This is a single-line comment
grab x = 10  -- inline comment after code
```

**Multi-line comments** are enclosed in `{-- ... --}` and may be nested:

```
{--
  This is a multi-line comment.
  It can span as many lines as needed.

  {-- Nested comments are allowed. --}
--}
```

### Statements

KOVA uses one statement per line. Semicolons are not required and are not part of the language syntax.

```
grab x = 10
grab y = 20
emit(x + y)
```

### Code Blocks

All block constructs use curly braces `{ }` to delimit their bodies:

```
test x > 0 {
  emit("positive")
}
```

### String Interpolation

Embed expressions inside strings using `{expression}`:

```
grab name = "KOVA"
grab version = 1
emit("Welcome to {name}, version {version}.0")
-- Output: Welcome to KOVA, version 1.0
```

To include a literal brace in a string, escape it with `\{`:

```
emit("Use \{expression} for interpolation")
-- Output: Use {expression} for interpolation
```

---

## 3. Variables & Constants

### Mutable Variables: `grab`

The `grab` keyword declares a mutable variable that can be reassigned at any time:

```
grab count = 0
count = count + 1
emit(count)  -- 1

grab name = "Alice"
name = "Bob"
emit(name)  -- Bob
```

### Immutable Constants: `lock`

The `lock` keyword declares an immutable binding. Any attempt to reassign a locked constant produces a runtime error:

```
lock PI = 3.14159
lock MAX_SIZE = 1024
lock APP_NAME = "MyApp"

emit(PI)        -- 3.14159
emit(MAX_SIZE)  -- 1024

PI = 3.0  -- ERROR: Cannot reassign a locked constant
```

### Naming Rules

- Identifiers begin with a letter or underscore
- They may contain letters, digits, and underscores
- Identifiers are case-sensitive
- Unicode characters are supported in identifiers
- Reserved keywords cannot be used as identifiers

```
grab _count = 0        -- valid: starts with underscore
grab item2 = "second"  -- valid: contains digit
grab myVar = 42        -- valid: camelCase
grab total_sum = 100   -- valid: snake_case
```

### Destructuring

Both `grab` and `lock` support destructuring for arrays and maps:

```
-- Array destructuring
grab [first, second, ...rest] = [1, 2, 3, 4, 5]
emit(first)   -- 1
emit(second)  -- 2
emit(rest)    -- [3, 4, 5]

-- Map destructuring
grab {name, age} = {name: "Bob", age: 25, role: "dev"}
emit(name)  -- Bob
emit(age)   -- 25
```

---

## 4. Data Types

KOVA is dynamically typed. Every value belongs to one of the following types. Use the built-in `kind(value)` function to check a value's type at runtime.

### Numbers

Numbers are double-precision floating point values. There is no separate integer type; integer-valued numbers are a subset of the number type.

```
grab age = 42           -- integer
grab pi = 3.14159       -- decimal
grab negative = -7      -- negative
grab scientific = 2.5e10  -- scientific notation
grab hex = 0xFF         -- hexadecimal (255)

emit(kind(42))     -- "number"
emit(kind(3.14))   -- "number"
```

### Strings

Strings are delimited by double quotes `"` and support escape sequences and inline interpolation:

```
grab greeting = "Hello, world!"
grab name = "KOVA"
grab message = "Welcome to {name}!"
-- Output: "Welcome to KOVA!"
```

**Escape sequences:**

| Sequence | Meaning            |
|----------|--------------------|
| `\n`     | Newline            |
| `\t`     | Tab                |
| `\\`     | Literal backslash  |
| `\"`     | Literal quote      |
| `\{`     | Literal brace      |

**Multi-line strings** use triple double quotes:

```
grab poem = """
  Roses are red,
  Violets are blue,
  KOVA is forged,
  Especially for you.
"""
```

### Booleans

Boolean values are written as `yes` and `no` (not `true`/`false`):

```
grab active = yes
grab deleted = no

emit(kind(yes))  -- "boolean"
emit(active)     -- yes
```

### Void

The absence of a value is represented by `void` (equivalent to `null` or `nil` in other languages):

```
grab result = void

test result == void {
  emit("No result yet.")
}

emit(kind(void))  -- "void"
```

### Arrays

Arrays are ordered, zero-indexed collections that may contain mixed types:

```
grab numbers = [1, 2, 3, 4, 5]
grab mixed = ["hello", 42, yes, void]
grab nested = [[1, 2], [3, 4]]
grab empty = []

emit(numbers[0])   -- 1
emit(numbers[2])   -- 3
emit(numbers[-1])  -- 5 (negative indexing from end)
emit(nested[0][1]) -- 2

emit(kind([1, 2]))  -- "array"
```

### Maps

Maps are collections of key-value pairs. Keys are strings (quotes are optional when used as literals in map notation):

```
grab user = {
  name: "Alice",
  age: 30,
  active: yes
}

emit(user.name)       -- Alice
emit(user["age"])     -- 30

-- Dynamic keys require bracket notation
grab field = "name"
emit(user[field])     -- Alice

-- Map with quoted keys
grab config = {"host": "localhost", "port": 8080}
emit(config["host"])  -- localhost

emit(kind(user))  -- "map"
```

### Type Checking with `kind()`

The `kind()` function returns a string indicating the type of any value:

```
emit(kind(42))           -- "number"
emit(kind("hello"))      -- "string"
emit(kind(yes))          -- "boolean"
emit(kind(void))         -- "void"
emit(kind([1, 2, 3]))   -- "array"
emit(kind({a: 1}))      -- "map"
emit(kind(emit))         -- "function"
```

---

## 5. Operators

### Arithmetic Operators

| Operator | Description     | Example            | Result  |
|----------|-----------------|--------------------|---------|
| `+`      | Addition        | `5 + 3`            | `8`     |
| `-`      | Subtraction     | `5 - 3`            | `2`     |
| `*`      | Multiplication  | `5 * 3`            | `15`    |
| `/`      | Division        | `10 / 3`           | `3.333` |
| `%`      | Modulus         | `10 % 3`           | `1`     |
| `**`     | Exponentiation  | `2 ** 10`          | `1024`  |

```
grab result = (2 + 3) * 4 - 1
emit(result)  -- 19

emit(2 ** 8)   -- 256
emit(17 % 5)   -- 2
emit(10 / 3)   -- 3.3333333333333335
```

### Comparison Operators

All comparisons return `yes` or `no`.

| Operator | Description              | Example     | Result |
|----------|--------------------------|-------------|--------|
| `==`     | Equal to                 | `5 == 5`    | `yes`  |
| `!=`     | Not equal to             | `5 != 3`    | `yes`  |
| `>`      | Greater than             | `5 > 3`     | `yes`  |
| `<`      | Less than                | `3 < 5`     | `yes`  |
| `>=`     | Greater than or equal to | `5 >= 5`    | `yes`  |
| `<=`     | Less than or equal to    | `3 <= 5`    | `yes`  |

```
grab age = 25
test age >= 18 {
  emit("You are an adult")
}
```

### Logical Operators

Short-circuit evaluation applies: `and` stops at the first `no`; `or` stops at the first `yes`.

| Operator | Description | Example            | Result |
|----------|-------------|--------------------|--------|
| `and`    | Logical AND | `yes and no`       | `no`   |
| `or`     | Logical OR  | `yes or no`        | `yes`  |
| `not`    | Logical NOT | `not yes`          | `no`   |

```
grab logged_in = yes
grab is_admin = no

test logged_in and is_admin {
  emit("Admin access granted")
}

test logged_in or is_admin {
  emit("Some access granted")
}

test not is_admin {
  emit("Not an admin")
}
```

### Assignment Operators

| Operator | Equivalent       | Example             |
|----------|------------------|---------------------|
| `=`      | Assignment       | `x = 10`            |
| `+=`     | `x = x + rhs`   | `x += 5`            |
| `-=`     | `x = x - rhs`   | `x -= 3`            |
| `*=`     | `x = x * rhs`   | `x *= 2`            |
| `/=`     | `x = x / rhs`   | `x /= 4`            |
| `%=`     | `x = x % rhs`   | `x %= 3`            |

```
grab score = 0
score += 10
score += 5
score -= 3
emit(score)  -- 12
```

### String Concatenation

The `+` operator concatenates strings. If one operand is a string and the other is not, the non-string operand is automatically converted:

```
grab result = "Hello, " + "world!"
emit(result)  -- Hello, world!

grab label = "Count: " + 42
emit(label)  -- Count: 42
```

### Range Operator: `..`

The `..` operator creates an inclusive range, useful in loops and for generating arrays:

```
grab r = 1..10         -- range from 1 to 10, inclusive
grab nums = [1..5]     -- [1, 2, 3, 4, 5]

spin i in 1..5 {
  emit(i)
}
-- Output: 1 2 3 4 5
```

### Pipe Operator: `|>`

The pipe operator passes the result of the left expression as the first argument to the function on the right. It enables a readable left-to-right data flow:

```
grab result = "  Hello, World!  "
  |> trim
  |> crush
  |> split(", ")

-- Equivalent to: split(crush(trim("  Hello, World!  ")), ", ")
-- Result: ["hello", "world!"]
```

Pipes chain naturally with lambdas:

```
grab doubled = [1, 2, 3, 4, 5]
  |> filter(|x| => x % 2 == 0)
  |> map(|x| => x * 2)

-- Result: [4, 8]
```

---

## 6. Control Flow

### 6.1 Conditionals

KOVA uses `test`, `also`, and `rival` for conditional branching (equivalent to if / else if / else).

**Simple conditional (`test`):**

```
grab temperature = 35

test temperature > 30 {
  emit("It's hot outside!")
}
```

**Two-way conditional (`test` / `rival`):**

```
grab age = 16

test age >= 18 {
  emit("You can vote.")
} rival {
  emit("You are too young to vote.")
}
```

**Chained conditional (`test` / `also` / `rival`):**

```
grab score = 85

test score >= 90 {
  emit("Grade: A")
} also score >= 80 {
  emit("Grade: B")
} also score >= 70 {
  emit("Grade: C")
} also score >= 60 {
  emit("Grade: D")
} rival {
  emit("Grade: F")
}
-- Output: Grade: B
```

**Nested conditionals:**

```
grab user_role = "editor"
grab is_active = yes

test is_active {
  test user_role == "admin" {
    emit("Full access")
  } also user_role == "editor" {
    emit("Edit access")
  } rival {
    emit("Read-only access")
  }
} rival {
  emit("Account disabled")
}
-- Output: Edit access
```

**Inline conditional (ternary-style):**

`test` can be used as an expression:

```
grab age = 25
grab label = test age >= 18 { "adult" } rival { "minor" }
emit(label)  -- adult
```

### 6.2 Loops

#### `spin` -- For Range Loop

The `spin` keyword creates a counted loop. It iterates a variable `from` a start value `to` an end value (inclusive):

```
spin i from 1 to 5 {
  emit(i)
}
-- Output: 1 2 3 4 5
```

**With step (`by`):**

An optional `by` clause sets the step size:

```
spin i from 0 to 20 by 5 {
  emit(i)
}
-- Output: 0 5 10 15 20
```

```
spin i from 10 to 0 by -2 {
  emit(i)
}
-- Output: 10 8 6 4 2 0
```

#### `spin` -- For-Each Loop

When used with the `in` keyword, `spin` iterates over each element of an array, string, or map:

```
grab fruits = ["apple", "banana", "cherry"]

spin fruit in fruits {
  emit(fruit)
}
-- Output:
-- apple
-- banana
-- cherry
```

**Iterating over a map yields key-value pairs:**

```
grab config = {host: "localhost", port: 8080, debug: yes}

spin key, value in config {
  emit("{key} = {value}")
}
-- Output:
-- host = localhost
-- port = 8080
-- debug = yes
```

**Iterating over a string:**

```
spin char in "KOVA" {
  emit(char)
}
-- Output: K O V A
```

#### `orbit` -- While Loop

The `orbit` keyword creates a conditional loop that repeats as long as its condition evaluates to `yes`:

```
grab n = 1

orbit n <= 100 {
  n = n * 2
}

emit(n)  -- 128
```

**Infinite loop (use `snap` to exit):**

```
orbit yes {
  grab input = absorb("Enter 'quit' to exit: ")
  test input == "quit" {
    snap
  }
  emit("You typed: {input}")
}
```

#### Loop Control: `snap` and `skip`

- `snap` -- immediately exits the innermost loop (equivalent to `break`)
- `skip` -- skips the rest of the current iteration and advances to the next (equivalent to `continue`)

```
-- snap example: stop at 5
spin i from 1 to 10 {
  test i == 5 {
    snap
  }
  emit(i)
}
-- Output: 1 2 3 4
```

```
-- skip example: skip even numbers
spin i from 1 to 10 {
  test i % 2 == 0 {
    skip
  }
  emit(i)
}
-- Output: 1 3 5 7 9
```

```
-- Combined example
spin i from 1 to 10 {
  test i == 8 {
    snap
  }
  test i % 2 == 0 {
    skip
  }
  emit(i)
}
-- Output: 1 3 5 7
```

### 6.3 Pattern Matching

The `morph` keyword enables pattern matching. It evaluates a value against a series of patterns and executes the block of the first match. Use `_` as the default/wildcard pattern.

**Basic pattern matching:**

```
grab status = 404

morph status {
  200 => emit("OK")
  301 => emit("Moved Permanently")
  404 => emit("Not Found")
  500 => emit("Internal Server Error")
  _ => emit("Unknown status: {status}")
}
-- Output: Not Found
```

**Matching with string values:**

```
grab command = "start"

morph command {
  "start" => emit("Starting the engine...")
  "stop" => emit("Stopping the engine...")
  "restart" => {
    emit("Stopping...")
    emit("Starting...")
  }
  _ => emit("Unknown command: {command}")
}
-- Output: Starting the engine...
```

**Multiple patterns and complex expressions:**

```
grab day = "Saturday"

morph day {
  "Monday" => emit("Start of work week")
  "Friday" => emit("TGIF!")
  "Saturday" => emit("Weekend!")
  "Sunday" => emit("Weekend!")
  _ => emit("Midweek grind")
}
-- Output: Weekend!
```

**Destructuring in patterns:**

```
grab point = {x: 3, y: 0}

morph point {
  {x: 0, y: 0} => emit("Origin")
  {x, y: 0} => emit("On the X axis at {x}")
  {x: 0, y} => emit("On the Y axis at {y}")
  {x, y} => emit("Point at ({x}, {y})")
}
-- Output: On the X axis at 3
```

---

## 7. Functions

### Defining Functions: `forge`

Functions are declared with the `forge` keyword, followed by the function name and a parenthesized parameter list:

```
forge greet(name) {
  emit("Hello, {name}!")
}

greet("KOVA")   -- Hello, KOVA!
greet("Alice")  -- Hello, Alice!
```

### Returning Values: `yield`

The `yield` keyword returns a value from a function. If no `yield` is encountered, the function implicitly returns `void`:

```
forge square(n) {
  yield n ** 2
}

grab result = square(5)
emit(result)  -- 25
```

```
forge divide(a, b) {
  test b == 0 {
    yield void
  }
  yield a / b
}

emit(divide(10, 3))  -- 3.3333333333333335
emit(divide(10, 0))  -- void
```

### Calling Functions

Functions are called by name with arguments in parentheses:

```
forge add(a, b) {
  yield a + b
}

grab sum = add(3, 7)
emit(sum)  -- 10
```

### Default Parameters

Parameters may have default values. Default parameters must come after required parameters:

```
forge greet(name, greeting = "Hello") {
  emit("{greeting}, {name}!")
}

greet("Alice")                -- Hello, Alice!
greet("Bob", "Good morning")  -- Good morning, Bob!
```

```
forge create_user(name, role = "viewer", active = yes) {
  emit("Created {name} as {role} (active: {active})")
}

create_user("Alice")                    -- Created Alice as viewer (active: yes)
create_user("Bob", "admin")             -- Created Bob as admin (active: yes)
create_user("Charlie", "editor", no)    -- Created Charlie as editor (active: no)
```

### Lambdas (Anonymous Functions)

Anonymous functions use the `|params| => expression` syntax:

```
-- Single expression lambda
grab double = |x| => x * 2
emit(double(5))  -- 10

-- Multiple parameters
grab add = |a, b| => a + b
emit(add(3, 4))  -- 7

-- No parameters
grab say_hi = || => emit("Hi!")
say_hi()  -- Hi!

-- Multi-line lambda body
grab process = |x| => {
  grab temp = x * 2
  yield temp + 1
}
emit(process(5))  -- 11
```

### Closures

Lambdas are closures and capture their enclosing scope by reference:

```
forge make_counter() {
  grab count = 0
  yield || => {
    count += 1
    yield count
  }
}

grab counter = make_counter()
emit(counter())  -- 1
emit(counter())  -- 2
emit(counter())  -- 3
```

```
forge make_adder(n) {
  yield |x| => x + n
}

grab add5 = make_adder(5)
grab add10 = make_adder(10)
emit(add5(3))   -- 8
emit(add10(3))  -- 13
```

### Recursion

Functions can call themselves recursively:

```
-- Factorial
forge factorial(n) {
  test n <= 1 {
    yield 1
  }
  yield n * factorial(n - 1)
}

emit(factorial(5))   -- 120
emit(factorial(10))  -- 3628800
```

```
-- Fibonacci
forge fibonacci(n) {
  test n <= 0 {
    yield 0
  }
  test n == 1 {
    yield 1
  }
  yield fibonacci(n - 1) + fibonacci(n - 2)
}

emit(fibonacci(10))  -- 55
```

### Variadic Parameters

A rest parameter collects remaining arguments into an array:

```
forge sum(...nums) {
  grab total = 0
  spin n in nums {
    total += n
  }
  yield total
}

emit(sum(1, 2, 3, 4, 5))  -- 15
emit(sum(10, 20))          -- 30
```

---

## 8. Object-Oriented Programming

### 8.1 Shapes (Classes)

The `shape` keyword defines a class-like construct. A shape encapsulates data and behavior.

**Defining a shape:**

```
shape Circle {
  forge init(radius) {
    self.radius = radius
  }

  forge area() {
    yield 3.14159 * self.radius ** 2
  }

  forge circumference() {
    yield 2 * 3.14159 * self.radius
  }

  forge describe() {
    emit("Circle with radius {self.radius}")
  }
}

grab c = Circle(5)
c.describe()           -- Circle with radius 5
emit(c.area())         -- 78.53975
emit(c.circumference())  -- 31.4159
```

**Constructor: `forge init()`**

The constructor is a method named `init`, declared with `forge`. It is called automatically when a new instance is created. There is no `new` keyword; calling the shape name as a function constructs an instance.

```
shape Point {
  forge init(x, y) {
    self.x = x
    self.y = y
  }

  forge distance_to(other) {
    grab dx = self.x - other.x
    grab dy = self.y - other.y
    yield sqrt(dx ** 2 + dy ** 2)
  }
}

grab p1 = Point(3, 4)
grab p2 = Point(0, 0)
emit(p1.x)                  -- 3
emit(p1.distance_to(p2))    -- 5
```

**The `self` keyword:**

Inside any shape method, `self` refers to the current instance. It must be used explicitly to access instance properties and methods:

```
shape Timer {
  forge init() {
    self.start_time = tick()
  }

  forge elapsed() {
    yield tick() - self.start_time
  }
}

grab t = Timer()
sleep(100)
emit(t.elapsed())  -- approximately 100
```

### 8.2 Inheritance

The `evolve` keyword declares a shape that inherits from a parent shape. The child gains all methods and properties of the parent. Use `parent` to call parent methods.

**Basic inheritance:**

```
shape Animal {
  forge init(name, sound) {
    self.name = name
    self.sound = sound
  }

  forge speak() {
    emit("{self.name} says {self.sound}!")
  }
}

evolve Dog from Animal {
  forge init(name) {
    parent.init(name, "Woof")
    self.tricks = []
  }

  forge learn(trick) {
    self.tricks.push(trick)
  }

  forge show_tricks() {
    emit("{self.name} knows:")
    spin trick in self.tricks {
      emit("  - {trick}")
    }
  }
}

grab rex = Dog("Rex")
rex.speak()            -- Rex says Woof!
rex.learn("sit")
rex.learn("shake")
rex.show_tricks()
-- Output:
-- Rex knows:
--   - sit
--   - shake
```

**Method overriding:**

```
shape Vehicle {
  forge init(make, model) {
    self.make = make
    self.model = model
    self.speed = 0
  }

  forge describe() {
    yield "{self.make} {self.model}"
  }

  forge accelerate(amount) {
    self.speed += amount
  }
}

evolve ElectricCar from Vehicle {
  forge init(make, model, battery) {
    parent.init(make, model)
    self.battery = battery
  }

  -- Override parent method
  forge describe() {
    yield "{self.make} {self.model} (EV, {self.battery} kWh)"
  }

  forge charge() {
    emit("Charging {self.describe()}...")
  }
}

grab car = ElectricCar("Tesla", "Model 3", 75)
emit(car.describe())  -- Tesla Model 3 (EV, 75 kWh)
car.accelerate(60)
emit(car.speed)       -- 60
car.charge()          -- Charging Tesla Model 3 (EV, 75 kWh)...
```

---

## 9. Error Handling

### `attempt` / `rescue` (try/catch)

The `attempt` block executes code that may fail. If an error occurs, control passes to the `rescue` block, which receives the error value:

```
attempt {
  grab data = read("config.txt")
  emit(data)
} rescue err {
  emit("Failed to read config: {err}")
}
```

### `eject` (throw)

The `eject` keyword raises an error. It accepts a string message or any value:

```
forge divide(a, b) {
  test b == 0 {
    eject "Division by zero"
  }
  yield a / b
}

attempt {
  grab result = divide(10, 0)
} rescue err {
  emit("Error: {err}")
}
-- Output: Error: Division by zero
```

### Custom Error Shapes

You can define custom error types using shapes:

```
shape ValidationError {
  forge init(field, message) {
    self.field = field
    self.message = message
  }
}

forge validate_age(age) {
  test age < 0 or age > 150 {
    eject ValidationError("age", "Age must be between 0 and 150")
  }
  yield age
}

attempt {
  validate_age(-5)
} rescue err {
  emit("Validation failed on '{err.field}': {err.message}")
}
-- Output: Validation failed on 'age': Age must be between 0 and 150
```

### Nested Error Handling

`attempt` / `rescue` blocks can be nested for fine-grained control:

```
attempt {
  grab config = read("config.txt")

  attempt {
    grab data = read("data.txt")
    emit("Both files loaded")
  } rescue err {
    emit("Data file error: {err}")
    emit("Using default data")
  }

} rescue err {
  emit("Config file error: {err}")
}
```

---

## 10. Modules

### Importing: `pull`

The `pull` keyword imports functionality from another module. Modules are referenced by file path (without the `.kva` extension):

```
-- Import an entire module
pull "math_utils"

-- Import specific names
pull {sqrt, abs} from "math"

-- Import with alias
pull "networking" as net
```

### Exporting: `expose`

The `expose` keyword makes a declaration available to other modules:

```
-- utils.kva
expose forge clamp(value, low, high) {
  test value < low { yield low }
  test value > high { yield high }
  yield value
}

expose lock VERSION = "1.0.0"
```

```
-- main.kva
pull {clamp, VERSION} from "utils"

emit(clamp(15, 0, 10))  -- 10
emit(VERSION)            -- 1.0.0
```

### Circular Import Protection

KOVA automatically detects and prevents circular imports. If module A imports module B and module B imports module A, a runtime error is raised to protect against infinite loops.

### Module Example

```
-- geometry.kva
expose lock PI = 3.14159

expose forge circle_area(radius) {
  yield PI * radius ** 2
}

expose forge rect_area(width, height) {
  yield width * height
}
```

```
-- app.kva
pull {PI, circle_area, rect_area} from "geometry"

emit("PI = {PI}")
emit("Circle area (r=5): {circle_area(5)}")
emit("Rectangle area (3x4): {rect_area(3, 4)}")
```

---

## 11. Defer

### `defer` Blocks

A `defer` block schedules code to run when the enclosing scope exits, regardless of whether the exit is normal or caused by an error. This is ideal for cleanup operations. Multiple defers execute in last-in-first-out (LIFO) order.

**Basic defer:**

```
forge process_file(path) {
  emit("Opening {path}")
  defer {
    emit("Closing {path}")
  }

  grab content = read(path)
  emit("Processing...")
  yield content
}

process_file("data.txt")
-- Output:
-- Opening data.txt
-- Processing...
-- Closing data.txt
```

**LIFO execution order:**

```
forge example() {
  defer { emit("Third (deferred first)") }
  defer { emit("Second (deferred second)") }
  defer { emit("First (deferred third)") }
  emit("Main body")
}

example()
-- Output:
-- Main body
-- First (deferred third)
-- Second (deferred second)
-- Third (deferred first)
```

**Cleanup on error:**

```
forge risky_operation() {
  grab resource = "allocated"
  defer {
    emit("Cleanup: releasing resource")
  }

  eject "Something went wrong!"
}

attempt {
  risky_operation()
} rescue err {
  emit("Caught: {err}")
}
-- Output:
-- Cleanup: releasing resource
-- Caught: Something went wrong!
```

---

## 12. Built-in Functions Reference

All built-in functions are available globally without any `pull` statement.

### 12.1 I/O Functions

| Function | Description | Example |
|---|---|---|
| `emit(value)` | Print a value to standard output followed by a newline | `emit("Hello, world!")` |
| `absorb(prompt)` | Display an optional prompt and read a line of user input as a string | `grab name = absorb("Name: ")` |

```
-- Print various types
emit("Hello!")        -- Hello!
emit(42)              -- 42
emit([1, 2, 3])       -- [1, 2, 3]
emit(yes)             -- yes

-- Read input with type conversion
grab name = absorb("Enter your name: ")
grab age = cast(absorb("Enter your age: "), "number")
emit("Hello, {name}! You are {age} years old.")
```

### 12.2 Type Functions

| Function | Description | Example |
|---|---|---|
| `cast(value, type)` | Convert a value to the target type (`"number"`, `"string"`, or `"boolean"`) | `cast("42", "number")` -> `42` |
| `kind(value)` | Return the type name of a value as a string | `kind(42)` -> `"number"` |

```
-- cast examples
emit(cast("42", "number"))      -- 42
emit(cast("3.14", "number"))    -- 3.14
emit(cast(42, "string"))        -- "42"
emit(cast(1, "boolean"))        -- yes
emit(cast("", "boolean"))       -- no
emit(cast(0, "boolean"))        -- no

-- kind examples
emit(kind(42))            -- number
emit(kind("hello"))       -- string
emit(kind(yes))           -- boolean
emit(kind(void))          -- void
emit(kind([1, 2]))        -- array
emit(kind({a: 1}))        -- map
emit(kind(emit))          -- function
```

### 12.3 Math Functions

| Function | Description | Example |
|---|---|---|
| `abs(n)` | Absolute value | `abs(-5)` -> `5` |
| `sqrt(n)` | Square root (error if negative) | `sqrt(16)` -> `4` |
| `floor(n)` | Round down to nearest integer | `floor(3.7)` -> `3` |
| `ceil(n)` | Round up to nearest integer | `ceil(3.2)` -> `4` |
| `round(n)` | Round to nearest integer | `round(3.5)` -> `4` |
| `max(a, b)` | Return the larger of two values | `max(3, 7)` -> `7` |
| `min(a, b)` | Return the smaller of two values | `min(3, 7)` -> `3` |
| `rand(min, max)` | Return a random integer in [min, max] | `rand(1, 100)` |

```
emit(abs(-42))       -- 42
emit(sqrt(144))      -- 12.0
emit(floor(3.9))     -- 3
emit(ceil(3.1))      -- 4
emit(round(3.5))     -- 4
emit(round(3.4))     -- 3
emit(max(10, 20))    -- 20
emit(min(10, 20))    -- 10

grab die = rand(1, 6)
emit("You rolled: {die}")
```

### 12.4 String Functions

| Function | Description | Example |
|---|---|---|
| `crush(str)` | Convert a string to lowercase | `crush("HELLO")` -> `"hello"` |
| `rise(str)` | Convert a string to uppercase | `rise("hello")` -> `"HELLO"` |
| `split(str, delim)` | Split a string into an array by delimiter | `split("a,b,c", ",")` -> `["a","b","c"]` |
| `bond(arr, delim)` | Join array elements into a string with delimiter | `bond(["a","b"], ",")` -> `"a,b"` |

```
emit(crush("Hello World"))          -- hello world
emit(rise("hello"))                 -- HELLO
emit(split("one,two,three", ","))   -- [one, two, three]
emit(bond(["x", "y", "z"], "-"))    -- x-y-z

-- Combining functions
grab words = split("Hello World", " ")
grab upper_words = map(words, |w| => rise(w))
emit(bond(upper_words, " "))  -- HELLO WORLD
```

### 12.5 Array Functions

| Function | Description | Example |
|---|---|---|
| `span(arr)` | Return the length of an array, string, or map | `span([1,2,3])` -> `3` |
| `push(arr, val)` | Append a value to the end of an array (mutates) | `push(arr, 4)` |
| `pop(arr)` | Remove and return the last element of an array | `pop(arr)` |
| `sort(arr)` | Return a sorted copy of the array | `sort([3,1,2])` -> `[1,2,3]` |
| `reverse(arr)` | Return a reversed copy of the array | `reverse([1,2,3])` -> `[3,2,1]` |
| `fuse(a, b)` | Concatenate two arrays into a new array | `fuse([1,2], [3,4])` -> `[1,2,3,4]` |
| `slice(arr, start, end)` | Return a sub-array from start to end (exclusive) | `slice([1,2,3,4], 1, 3)` -> `[2,3]` |
| `seek(arr, val)` | Return the index of a value, or -1 if not found | `seek([1,2,3], 2)` -> `1` |
| `range(start, end)` | Create an array of integers from start to end (inclusive) | `range(1, 5)` -> `[1,2,3,4,5]` |
| `map(arr, fn)` | Apply a function to each element, return new array | `map([1,2,3], \|x\| => x*2)` -> `[2,4,6]` |
| `filter(arr, fn)` | Return elements for which the function returns `yes` | `filter([1,2,3,4], \|x\| => x > 2)` -> `[3,4]` |
| `reduce(arr, init, fn)` | Reduce an array to a single value with accumulator | `reduce([1,2,3], 0, \|a,x\| => a+x)` -> `6` |

```
grab nums = [5, 3, 8, 1, 9, 2]

emit(span(nums))                    -- 6
emit(sort(nums))                    -- [1, 2, 3, 5, 8, 9]
emit(reverse(nums))                 -- [2, 9, 1, 8, 3, 5]
emit(seek(nums, 8))                 -- 2
emit(slice(nums, 1, 4))             -- [3, 8, 1]
emit(fuse([1, 2], [3, 4]))          -- [1, 2, 3, 4]
emit(range(1, 5))                   -- [1, 2, 3, 4, 5]

-- Functional operations
grab doubled = map([1, 2, 3], |x| => x * 2)
emit(doubled)  -- [2, 4, 6]

grab evens = filter([1, 2, 3, 4, 5, 6], |x| => x % 2 == 0)
emit(evens)  -- [2, 4, 6]

grab total = reduce([1, 2, 3, 4, 5], 0, |acc, x| => acc + x)
emit(total)  -- 15
```

### 12.6 Map Functions

| Function | Description | Example |
|---|---|---|
| `keys(map)` | Return an array of all keys in the map | `keys({"a": 1})` -> `["a"]` |
| `vals(map)` | Return an array of all values in the map | `vals({"a": 1})` -> `[1]` |

```
grab user = {name: "Alice", age: 30, role: "admin"}

emit(keys(user))  -- [name, age, role]
emit(vals(user))  -- [Alice, 30, admin]

-- Iterate over a map's keys
spin key in keys(user) {
  emit("{key}: {user[key]}")
}
```

### 12.7 File I/O

| Function | Description | Example |
|---|---|---|
| `read(file)` | Read entire file contents as a string | `grab txt = read("data.txt")` |
| `write(file, content)` | Write a string to a file (overwrites if exists) | `write("out.txt", "Hello")` |
| `append(file, content)` | Append a string to the end of a file | `append("log.txt", "entry\n")` |

```
-- Write a file
write("output.txt", "Hello, KOVA!\n")

-- Append to a file
append("output.txt", "Second line.\n")

-- Read a file
grab content = read("output.txt")
emit(content)
-- Output:
-- Hello, KOVA!
-- Second line.

-- Safe file reading with error handling
attempt {
  grab data = read("missing.txt")
} rescue err {
  emit("Could not read file: {err}")
}
```

### 12.8 System Functions

| Function | Description | Example |
|---|---|---|
| `tick()` | Return the current Unix timestamp in milliseconds | `grab t = tick()` |
| `time()` | Return the current date/time as a formatted string (YYYY-MM-DD HH:MM:SS) | `emit(time())` |
| `sleep(ms)` | Pause execution for the given number of milliseconds | `sleep(1000)` |
| `exit(code)` | Exit the program with the given exit code (default 0) | `exit(0)` |
| `clone(val)` | Create a deep copy of a value (arrays, maps, etc.) | `grab b = clone(a)` |

```
-- Timing example
grab start = tick()
sleep(500)
grab elapsed = tick() - start
emit("Elapsed: {elapsed}ms")  -- approximately 500ms

-- Current time
emit(time())  -- e.g., "2026-08-08 14:30:00"

-- Deep copy
grab original = [1, [2, 3], 4]
grab copy = clone(original)
copy[1].push(99)
emit(original)  -- [1, [2, 3], 4]     (unchanged)
emit(copy)      -- [1, [2, 3, 99], 4] (modified copy only)

-- Exit
test some_fatal_error {
  emit("Fatal error, shutting down")
  exit(1)
}
```

---

## 13. String Methods (dot notation)

Strings support the following methods via dot notation. These methods return new values and do not mutate the original string.

| Method | Description | Example |
|---|---|---|
| `.crush()` | Return a lowercase copy | `"HELLO".crush()` -> `"hello"` |
| `.rise()` | Return an uppercase copy | `"hello".rise()` -> `"HELLO"` |
| `.trim()` | Remove leading and trailing whitespace | `" hi ".trim()` -> `"hi"` |
| `.split(delim)` | Split into an array on delimiter | `"a,b".split(",")` -> `["a","b"]` |
| `.has(sub)` | Check if a substring exists | `"hello".has("ell")` -> `yes` |
| `.swap(old, new)` | Replace all occurrences of old with new | `"hi".swap("hi","hello")` -> `"hello"` |
| `.span()` | Return the string length | `"hello".span()` -> `5` |
| `.starts(prefix)` | Check if string starts with prefix | `"hello".starts("he")` -> `yes` |
| `.ends(suffix)` | Check if string ends with suffix | `"hello".ends("lo")` -> `yes` |
| `.slice(start, end)` | Extract a substring from start to end (exclusive) | `"hello".slice(0, 3)` -> `"hel"` |

```
grab raw = "  Hello, World!  "
grab cleaned = raw.trim().crush()
emit(cleaned)                        -- hello, world!
emit(cleaned.has("world"))           -- yes
emit(cleaned.swap("world", "KOVA"))  -- hello, KOVA!

grab filename = "photo_2026.jpg"
test filename.ends(".jpg") or filename.ends(".png") {
  emit("This is an image file")
}

grab url = "https://example.com/path"
test url.starts("https://") {
  emit("Secure connection")
}

grab email = "user@example.com"
grab parts = email.split("@")
emit(parts[0])  -- user
emit(parts[1])  -- example.com

emit("Hello".span())         -- 5
emit("Hello".slice(1, 4))    -- ell
```

**Method chaining:**

String methods can be chained because each method returns a new string:

```
grab result = "  Hello, WORLD!  ".trim().crush().swap("world", "kova")
emit(result)  -- hello, kova!
```

---

## 14. Array Methods (dot notation)

Arrays support the following methods via dot notation. Some methods mutate the array in place (noted below), while others return new arrays.

| Method | Description | Mutates? | Example |
|---|---|---|---|
| `.push(val)` | Add a value to the end | Yes | `arr.push(4)` |
| `.pop()` | Remove and return the last element | Yes | `arr.pop()` |
| `.shift()` | Remove and return the first element | Yes | `arr.shift()` |
| `.span()` | Return the array length | No | `arr.span()` -> `3` |
| `.seek(val)` | Find the index of a value (-1 if not found) | No | `arr.seek(2)` -> `1` |
| `.has(val)` | Check if the array contains a value | No | `arr.has(2)` -> `yes` |
| `.each(fn)` | Execute a function for each element | No | `arr.each(\|x\| => emit(x))` |
| `.map(fn)` | Return a new array with transformed elements | No | `arr.map(\|x\| => x * 2)` |
| `.sift(fn)` | Return a new array with elements matching predicate | No | `arr.sift(\|x\| => x > 2)` |
| `.fold(init, fn)` | Reduce to a single value using accumulator | No | `arr.fold(0, \|a,x\| => a+x)` |
| `.sort()` | Return a sorted copy | No | `arr.sort()` |
| `.flip()` | Return a reversed copy | No | `arr.flip()` |
| `.fuse(other)` | Return a new array concatenated with another | No | `arr.fuse([4,5])` |
| `.slice(start, end)` | Return a sub-array from start to end (exclusive) | No | `arr.slice(1, 3)` |
| `.bond(delim)` | Join elements into a string with delimiter | No | `arr.bond(", ")` |

```
grab scores = [85, 92, 78, 95, 88]

-- Filtering and sorting
grab high_scores = scores.sift(|s| => s >= 90).sort().flip()
emit(high_scores)  -- [95, 92]

-- Reducing
grab total = scores.fold(0, |sum, s| => sum + s)
grab average = total / scores.span()
emit("Average: {average}")  -- Average: 87.6

-- Mapping
grab doubled = [1, 2, 3].map(|x| => x * 2)
emit(doubled)  -- [2, 4, 6]

-- Checking contents
grab fruits = ["apple", "banana", "cherry"]
emit(fruits.has("banana"))   -- yes
emit(fruits.seek("cherry"))  -- 2

-- Each
[1, 2, 3].each(|x| => emit("Item: {x}"))
-- Output:
-- Item: 1
-- Item: 2
-- Item: 3

-- Joining
grab csv = ["Alice", "Bob", "Charlie"].bond(", ")
emit(csv)  -- Alice, Bob, Charlie

-- Mutating operations
grab stack = [1, 2, 3]
stack.push(4)
emit(stack)       -- [1, 2, 3, 4]
grab last = stack.pop()
emit(last)        -- 4
grab first = stack.shift()
emit(first)       -- 1
emit(stack)       -- [2, 3]

-- Chaining
grab result = [5, 3, 8, 1, 9, 2]
  .sift(|x| => x > 3)
  .sort()
  .map(|x| => x * 10)
emit(result)  -- [50, 80, 90]
```

---

## 15. REPL Commands

When running the interactive REPL (`kovarun` with no arguments), the following dot commands are available:

| Command    | Description                           |
|------------|---------------------------------------|
| `.help`    | Show help message and quick reference |
| `.clear`   | Clear the terminal screen             |
| `.exit`    | Exit the REPL session                 |
| `.version` | Show the KOVA version                 |

```
kova> .help
  KOVA REPL Commands:
    .help     -- Show this help message
    .clear    -- Clear the screen
    .exit     -- Exit the REPL
    .version  -- Show version info

  Language Quick Reference:
    grab x = 10             -- Declare mutable variable
    lock PI = 3.14          -- Declare constant
    forge f(x) { }          -- Define function
    emit("hello")           -- Print output
    test x > 0 { }          -- If statement
    spin i from 1 to 5 { }  -- For loop

kova> .version
KOVA v1.0.0

kova> .exit
```

---

## 16. Security Features

KOVA includes several built-in safety limits to prevent runaway programs and protect the host system:

| Feature | Limit | Description |
|---|---|---|
| **Recursion depth** | 1,000 calls | Prevents stack overflow from deeply recursive functions |
| **Loop iteration limit** | 1,000,000 iterations | Prevents infinite loops from consuming resources |
| **Import depth limit** | 16 levels | Prevents circular or deeply nested module imports |
| **Sandboxed file I/O** | Working directory | File operations are restricted to allowed directories |

```
-- This will trigger the recursion limit
forge infinite() {
  infinite()
}

attempt {
  infinite()
} rescue err {
  emit("Caught: {err}")
  -- Output: Caught: Maximum recursion depth exceeded
}
```

```
-- This will trigger the loop limit
grab i = 0
attempt {
  orbit yes {
    i += 1
  }
} rescue err {
  emit("Loop stopped after {i} iterations")
}
```

---

## 17. Complete Example Programs

### Mini Todo App

A simple command-line TODO manager demonstrating shapes, arrays, maps, loops, and conditionals:

```
-- todo.kva -- Simple TODO manager

grab todos = []

forge add_todo(task) {
  todos.push({"task": task, "done": no})
  emit("Added: " + task)
}

forge complete_todo(index) {
  test index >= 0 and index < todos.span() {
    todos[index]["done"] = yes
    emit("Completed: " + todos[index]["task"])
  } rival {
    emit("Invalid index!")
  }
}

forge show_todos() {
  emit("--- TODO List ---")
  test todos.span() == 0 {
    emit("  (no tasks)")
    yield void
  }
  spin i from 0 to todos.span() - 1 {
    grab status = "[ ]"
    test todos[i]["done"] == yes {
      grab status = "[x]"
    }
    emit(cast(i, "string") + ". " + status + " " + todos[i]["task"])
  }
  emit("-----------------")
}

add_todo("Learn KOVA")
add_todo("Build a project")
add_todo("Share with friends")
complete_todo(0)
show_todos()
```

**Expected output:**

```
Added: Learn KOVA
Added: Build a project
Added: Share with friends
Completed: Learn KOVA
--- TODO List ---
0. [x] Learn KOVA
1. [ ] Build a project
2. [ ] Share with friends
-----------------
```

### FizzBuzz

The classic FizzBuzz problem, demonstrating `spin`, `test`/`also`/`rival`, modulus, and type casting:

```
-- fizzbuzz.kva
spin i from 1 to 100 {
  test i % 15 == 0 {
    emit("FizzBuzz")
  } also i % 3 == 0 {
    emit("Fizz")
  } also i % 5 == 0 {
    emit("Buzz")
  } rival {
    emit(cast(i, "string"))
  }
}
```

**Expected output (first 20 lines):**

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz
```

### Number Guessing Game

An interactive game demonstrating `orbit`, `absorb`, `rand`, `cast`, `snap`, and conditionals:

```
-- guess.kva -- Number Guessing Game
grab secret = rand(1, 100)
grab attempts = 0

emit("=== Number Guessing Game ===")
emit("I'm thinking of a number between 1 and 100")

orbit yes {
  grab guess = cast(absorb("Your guess: "), "number")
  attempts += 1

  test guess == secret {
    emit("Correct! You got it in " + cast(attempts, "string") + " attempts!")
    snap
  } also guess < secret {
    emit("Too low! Try again.")
  } rival {
    emit("Too high! Try again.")
  }
}

emit("Thanks for playing!")
```

### Simple Calculator with OOP

A calculator using shapes, methods, pattern matching, and error handling:

```
-- calculator.kva -- OOP Calculator

shape Calculator {
  forge init() {
    self.history = []
  }

  forge calculate(a, op, b) {
    grab result = void

    morph op {
      "+" => grab result = a + b
      "-" => grab result = a - b
      "*" => grab result = a * b
      "/" => {
        test b == 0 {
          eject "Division by zero"
        }
        grab result = a / b
      }
      "**" => grab result = a ** b
      "%" => grab result = a % b
      _ => eject "Unknown operator: {op}"
    }

    grab entry = "{a} {op} {b} = {result}"
    self.history.push(entry)
    yield result
  }

  forge show_history() {
    emit("--- Calculation History ---")
    test self.history.span() == 0 {
      emit("  (no history)")
      yield void
    }
    spin i from 0 to self.history.span() - 1 {
      emit("  {i + 1}. {self.history[i]}")
    }
    emit("---------------------------")
  }
}

-- Usage
grab calc = Calculator()

attempt {
  emit(calc.calculate(10, "+", 5))    -- 15
  emit(calc.calculate(10, "-", 3))    -- 7
  emit(calc.calculate(4, "**", 3))    -- 64
  emit(calc.calculate(17, "%", 5))    -- 2
  emit(calc.calculate(10, "/", 0))    -- Error!
} rescue err {
  emit("Error: {err}")
}

calc.show_history()
```

**Expected output:**

```
15
7
64
2
Error: Division by zero
--- Calculation History ---
  1. 10 + 5 = 15
  2. 10 - 3 = 7
  3. 4 ** 3 = 64
  4. 17 % 5 = 2
---------------------------
```

---

## 18. Keyword Quick Reference

A compact reference table of all KOVA keywords with their purpose and traditional equivalents.

| # | KOVA Keyword | Purpose | Traditional Equivalent |
|---|---|---|---|
| 1 | `grab` | Declare a mutable variable | `let` / `var` |
| 2 | `lock` | Declare an immutable constant | `const` / `final` |
| 3 | `forge` | Define a function or method | `function` / `def` |
| 4 | `yield` | Return a value from a function | `return` |
| 5 | `emit` | Print to standard output | `print` / `console.log` |
| 6 | `absorb` | Read user input | `input` / `readline` |
| 7 | `test` | Conditional branch (if) | `if` |
| 8 | `also` | Additional condition (else if) | `else if` / `elif` |
| 9 | `rival` | Fallback branch (else) | `else` |
| 10 | `spin` | Counted or collection loop | `for` |
| 11 | `from` | Start of range in `spin` loop | (part of for syntax) |
| 12 | `to` | End of range in `spin` loop | (part of for syntax) |
| 13 | `in` | Iterate over a collection | `in` |
| 14 | `by` | Step size in `spin` loop | `step` |
| 15 | `orbit` | Conditional loop (while) | `while` |
| 16 | `snap` | Exit loop immediately | `break` |
| 17 | `skip` | Skip to next iteration | `continue` |
| 18 | `shape` | Define a class / type | `class` / `struct` |
| 19 | `evolve` | Inherit from a parent shape | `extends` / `inherits` |
| 20 | `self` | Reference to current instance | `this` / `self` |
| 21 | `parent` | Reference to parent shape | `super` |
| 22 | `attempt` | Begin error-handled block | `try` |
| 23 | `rescue` | Handle error from `attempt` | `catch` / `except` |
| 24 | `eject` | Raise / throw an error | `throw` / `raise` |
| 25 | `pull` | Import a module | `import` / `require` |
| 26 | `expose` | Export a declaration | `export` |
| 27 | `defer` | Schedule cleanup at scope exit | Go's `defer` |
| 28 | `morph` | Pattern match on a value | `match` / `switch` |
| 29 | `and` | Logical AND | `&&` |
| 30 | `or` | Logical OR | `\|\|` |
| 31 | `not` | Logical NOT | `!` |
| 32 | `yes` | Boolean true | `true` |
| 33 | `no` | Boolean false | `false` |
| 34 | `void` | Null / absence of value | `null` / `nil` / `None` |
| 35 | `pipe` | Reserved for pipe operations | (reserved) |
| 36 | `\|>` | Pipe operator | Elixir's `\|>` |
| 37 | `..` | Range operator | Ruby's `..` |

---

*KOVA Usage Guide v1.0.0 -- End of Document*
