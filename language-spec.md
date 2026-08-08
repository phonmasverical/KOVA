# KOVA Language Specification

**Version 1.0 -- August 2026**
**File Extension: `.kv`**

---

> *KOVA -- Forged for clarity. Built for speed.*

---

## Table of Contents

1. [Overview](#1-overview)
2. [Lexical Structure](#2-lexical-structure)
   - 2.1 [Comments](#21-comments)
   - 2.2 [Identifiers](#22-identifiers)
   - 2.3 [Reserved Keywords](#23-reserved-keywords)
3. [Data Types](#3-data-types)
   - 3.1 [Numbers](#31-numbers)
   - 3.2 [Strings](#32-strings)
   - 3.3 [Booleans](#33-booleans)
   - 3.4 [Void (Null)](#34-void-null)
   - 3.5 [Arrays](#35-arrays)
   - 3.6 [Maps](#36-maps)
4. [Variables and Constants](#4-variables-and-constants)
5. [Operators](#5-operators)
   - 5.1 [Arithmetic Operators](#51-arithmetic-operators)
   - 5.2 [Comparison Operators](#52-comparison-operators)
   - 5.3 [Logical Operators](#53-logical-operators)
   - 5.4 [String Concatenation](#54-string-concatenation)
   - 5.5 [Range Operator](#55-range-operator)
   - 5.6 [Pipe Operator](#56-pipe-operator)
   - 5.7 [Assignment Operators](#57-assignment-operators)
6. [Control Flow](#6-control-flow)
   - 6.1 [Conditionals: test / also / rival](#61-conditionals-test--also--rival)
   - 6.2 [Loops: spin (for)](#62-loops-spin-for)
   - 6.3 [Loops: orbit (while)](#63-loops-orbit-while)
   - 6.4 [Loop Control: snap and skip](#64-loop-control-snap-and-skip)
   - 6.5 [Pattern Matching: morph](#65-pattern-matching-morph)
7. [Functions](#7-functions)
   - 7.1 [Defining Functions: forge](#71-defining-functions-forge)
   - 7.2 [Returning Values: yield](#72-returning-values-yield)
   - 7.3 [Lambda / Anonymous Functions](#73-lambda--anonymous-functions)
   - 7.4 [Default Parameters](#74-default-parameters)
   - 7.5 [Variadic Parameters](#75-variadic-parameters)
8. [Object-Oriented Programming](#8-object-oriented-programming)
   - 8.1 [Shapes (Classes)](#81-shapes-classes)
   - 8.2 [Constructors: forge init()](#82-constructors-forge-init)
   - 8.3 [Inheritance: evolve ... from](#83-inheritance-evolve--from)
   - 8.4 [The self Keyword](#84-the-self-keyword)
9. [Error Handling](#9-error-handling)
   - 9.1 [attempt / rescue](#91-attempt--rescue)
   - 9.2 [Ejecting Errors: eject](#92-ejecting-errors-eject)
10. [Modules](#10-modules)
    - 10.1 [Importing: pull](#101-importing-pull)
    - 10.2 [Exporting: expose](#102-exporting-expose)
11. [Input and Output](#11-input-and-output)
    - 11.1 [emit -- Print to Screen](#111-emit----print-to-screen)
    - 11.2 [absorb -- Read Input](#112-absorb----read-input)
12. [Scope and Deferred Execution](#12-scope-and-deferred-execution)
    - 12.1 [Block Scoping](#121-block-scoping)
    - 12.2 [defer Blocks](#122-defer-blocks)
13. [Built-in Functions](#13-built-in-functions)
14. [String Methods](#14-string-methods)
15. [Array Methods](#15-array-methods)
16. [File I/O](#16-file-io)
17. [Complete Example Program](#17-complete-example-program)
18. [Keyword Reference Table](#18-keyword-reference-table)

---

## 1. Overview

KOVA is a general-purpose, dynamically typed programming language designed for readability, expressiveness, and modern development workflows. It uses curly-brace delimited blocks, a fully original keyword set, and a clean syntax that favors explicit intent over implicit convention.

KOVA source files use the `.kv` extension.

### Design Principles

- **Clarity over brevity.** Every keyword communicates its purpose in plain English, but no keyword is borrowed from an existing language.
- **Modern defaults.** Pipelines, pattern matching, deferred execution, and string interpolation are first-class features.
- **Low ceremony.** No semicolons required. No mandatory type annotations. Minimal boilerplate.
- **Consistent structure.** All block constructs use `{ }`. All declarations begin with a distinct keyword.

---

## 2. Lexical Structure

### 2.1 Comments

**Single-line comments** begin with `--` and continue to the end of the line.

```
-- This is a single-line comment
grab x = 10  -- inline comment
```

**Multi-line comments** are enclosed in `{-- ... --}`. They may be nested.

```
{--
  This is a multi-line comment.
  It can span as many lines as needed.

  {-- Nested comments are allowed. --}
--}
```

### 2.2 Identifiers

Identifiers begin with a letter or underscore and may contain letters, digits, and underscores. They are case-sensitive.

```
grab name = "KOVA"
grab _count = 0
grab item2 = "second"
```

### 2.3 Reserved Keywords

The following words are reserved and cannot be used as identifiers:

```
grab    lock    forge   yield   emit    absorb
test    also    rival   spin    from    to
orbit   snap    skip    shape   evolve  self
attempt rescue  eject   pull    expose  defer
morph   and     or      not     yes     no
void    pipe
```

---

## 3. Data Types

KOVA is dynamically typed. Every value belongs to one of the following types.

### 3.1 Numbers

Numbers are IEEE 754 double-precision floating point values. There is no separate integer type; integer-valued numbers are a subset of the number type.

```
grab age = 42
grab pi = 3.14159
grab negative = -7
grab scientific = 2.5e10
grab hex = 0xFF
```

### 3.2 Strings

Strings are delimited by double quotes. They support escape sequences and inline interpolation with `{expression}`.

```
grab greeting = "Hello, world!"
grab name = "KOVA"
grab message = "Welcome to {name}, version {1 + 0}.0"
-- Result: "Welcome to KOVA, version 1.0"
```

**Escape sequences:**

| Sequence | Meaning          |
|----------|------------------|
| `\n`     | Newline          |
| `\t`     | Tab              |
| `\\`     | Literal backslash|
| `\"`     | Literal quote    |
| `\{`     | Literal brace    |

**Multi-line strings** use triple double quotes:

```
grab poem = """
  Roses are red,
  Violets are blue,
  KOVA is forged,
  Especially for you.
"""
```

### 3.3 Booleans

Boolean values are written as `yes` and `no`.

```
grab active = yes
grab deleted = no
```

### 3.4 Void (Null)

The absence of a value is represented by `void`.

```
grab result = void

test result == void {
  emit("No result yet.")
}
```

### 3.5 Arrays

Arrays are ordered, zero-indexed collections of values. They may contain mixed types.

```
grab numbers = [1, 2, 3, 4, 5]
grab mixed = ["hello", 42, yes, void]
grab nested = [[1, 2], [3, 4]]

emit(numbers[0])   -- 1
emit(numbers[-1])  -- 5 (negative indexing from end)
```

### 3.6 Maps

Maps are unordered collections of key-value pairs. Keys are strings (quotes optional when used as literals in map notation).

```
grab user = {
  name: "Alice",
  age: 30,
  active: yes
}

emit(user.name)       -- "Alice"
emit(user["age"])     -- 30

-- Dynamic keys require bracket notation
grab field = "name"
emit(user[field])     -- "Alice"
```

---

## 4. Variables and Constants

### Mutable Variables: `grab`

The `grab` keyword declares a mutable variable. It may be reassigned at any time.

```
grab count = 0
count = count + 1
emit(count)  -- 1
```

### Immutable Constants: `lock`

The `lock` keyword declares an immutable binding. Any attempt to reassign a locked variable produces a runtime error.

```
lock PI = 3.14159
lock MAX_SIZE = 1024

PI = 3.0  -- ERROR: Cannot reassign a locked constant
```

### Destructuring

Both `grab` and `lock` support destructuring for arrays and maps.

```
grab [first, second, ...rest] = [1, 2, 3, 4, 5]
-- first = 1, second = 2, rest = [3, 4, 5]

grab {name, age} = {name: "Bob", age: 25, role: "dev"}
-- name = "Bob", age = 25
```

---

## 5. Operators

### 5.1 Arithmetic Operators

| Operator | Description     | Example        |
|----------|-----------------|----------------|
| `+`      | Addition        | `5 + 3` = `8`  |
| `-`      | Subtraction     | `5 - 3` = `2`  |
| `*`      | Multiplication  | `5 * 3` = `15` |
| `/`      | Division        | `10 / 3` = `3.333...` |
| `%`      | Modulus         | `10 % 3` = `1` |
| `**`     | Exponentiation  | `2 ** 10` = `1024` |

### 5.2 Comparison Operators

| Operator | Description              |
|----------|--------------------------|
| `==`     | Equal to                 |
| `!=`     | Not equal to             |
| `>`      | Greater than             |
| `<`      | Less than                |
| `>=`     | Greater than or equal to |
| `<=`     | Less than or equal to    |

All comparisons yield `yes` or `no`.

### 5.3 Logical Operators

| Operator | Description   | Example                |
|----------|---------------|------------------------|
| `and`    | Logical AND   | `yes and no` = `no`    |
| `or`     | Logical OR    | `yes or no` = `yes`    |
| `not`    | Logical NOT   | `not yes` = `no`       |

Short-circuit evaluation applies: `and` stops at the first `no`; `or` stops at the first `yes`.

### 5.4 String Concatenation

The `+` operator concatenates strings. If one operand is a string and the other is not, the non-string operand is automatically converted.

```
grab result = "Hello, " + "world!"    -- "Hello, world!"
grab label = "Count: " + 42           -- "Count: 42"
```

### 5.5 Range Operator

The `..` operator creates an inclusive range. Ranges are lazy and can be used in `spin` loops or converted to arrays.

```
grab r = 1..10         -- range from 1 to 10, inclusive
grab nums = [1..5]     -- [1, 2, 3, 4, 5]
```

### 5.6 Pipe Operator

The pipe operator `|>` passes the result of the left expression as the first argument to the function on the right. It enables a readable left-to-right data flow.

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
  |> sift(|x| => x % 2 == 0)
  |> map(|x| => x * 2)

-- Result: [4, 8]
```

### 5.7 Assignment Operators

| Operator | Equivalent        |
|----------|-------------------|
| `=`      | Assignment        |
| `+=`     | `x = x + rhs`    |
| `-=`     | `x = x - rhs`    |
| `*=`     | `x = x * rhs`    |
| `/=`     | `x = x / rhs`    |
| `%=`     | `x = x % rhs`    |

---

## 6. Control Flow

### 6.1 Conditionals: `test` / `also` / `rival`

The `test` keyword begins a conditional branch. `also` introduces additional conditions (like "else if"). `rival` is the final fallback (like "else").

**Simple conditional:**

```
grab score = 85

test score >= 90 {
  emit("Excellent")
} rival {
  emit("Good effort")
}
```

**Chained conditional:**

```
grab score = 85

test score >= 90 {
  emit("Grade: A")
} also score >= 80 {
  emit("Grade: B")
} also score >= 70 {
  emit("Grade: C")
} rival {
  emit("Grade: F")
}
```

**Inline conditional (ternary-style):**

`test` can also be used as an expression:

```
grab label = test age >= 18 { "adult" } rival { "minor" }
```

### 6.2 Loops: `spin` (for)

The `spin` keyword creates a counted loop. It iterates a variable `from` a start value `to` an end value (inclusive).

```
spin i from 1 to 5 {
  emit(i)
}
-- Output: 1 2 3 4 5
```

**Stepping:**

An optional `by` clause sets the step size.

```
spin i from 0 to 20 by 5 {
  emit(i)
}
-- Output: 0 5 10 15 20
```

**Iterating over collections:**

When used with the `in` keyword, `spin` iterates over each element of an array, string, or map.

```
grab fruits = ["apple", "banana", "cherry"]

spin fruit in fruits {
  emit(fruit)
}
```

Iterating over a map yields key-value pairs:

```
grab config = {host: "localhost", port: 8080}

spin key, value in config {
  emit("{key} = {value}")
}
```

### 6.3 Loops: `orbit` (while)

The `orbit` keyword creates a conditional loop that repeats as long as its condition evaluates to `yes`.

```
grab n = 1

orbit n <= 100 {
  n = n * 2
}

emit(n)  -- 128
```

**Infinite loop:**

Omitting the condition creates an infinite loop (must be exited with `snap`).

```
orbit {
  grab input = absorb("Enter 'quit' to exit: ")
  test input == "quit" {
    snap
  }
}
```

### 6.4 Loop Control: `snap` and `skip`

- `snap` -- immediately exits the innermost loop (equivalent to "break").
- `skip` -- skips the rest of the current iteration and advances to the next (equivalent to "continue").

```
spin i from 1 to 10 {
  test i == 5 {
    snap  -- stop the loop entirely at 5
  }
  test i % 2 == 0 {
    skip  -- skip even numbers
  }
  emit(i)
}
-- Output: 1 3
```

### 6.5 Pattern Matching: `morph`

The `morph` keyword enables pattern matching. It evaluates a value against a series of patterns and executes the block of the first match.

```
grab status = 404

morph status {
  200 => emit("OK")
  301 => emit("Moved")
  404 => emit("Not Found")
  500 => emit("Server Error")
  _ => emit("Unknown status: {status}")
}
```

**Matching with guards:**

```
grab age = 25

morph age {
  0..12 => emit("Child")
  13..17 => emit("Teenager")
  n test n >= 18 and n < 65 => emit("Adult")
  _ => emit("Senior")
}
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
-- Output: "On the X axis at 3"
```

---

## 7. Functions

### 7.1 Defining Functions: `forge`

Functions are declared with the `forge` keyword, followed by the function name and a parenthesized parameter list.

```
forge greet(name) {
  emit("Hello, {name}!")
}

greet("KOVA")  -- Hello, KOVA!
```

### 7.2 Returning Values: `yield`

The `yield` keyword returns a value from a function. If no `yield` is encountered, the function implicitly yields `void`.

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
```

### 7.3 Lambda / Anonymous Functions

Anonymous functions (lambdas) use the `|params| => expression` syntax. For multi-line bodies, use a block.

```
-- Single expression
grab double = |x| => x * 2
emit(double(5))  -- 10

-- Multiple parameters
grab add = |a, b| => a + b
emit(add(3, 4))  -- 7

-- Multi-line lambda body
grab process = |x| => {
  grab temp = x * 2
  yield temp + 1
}
```

Lambdas are closures and capture their enclosing scope by reference.

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
```

### 7.4 Default Parameters

Parameters may have default values.

```
forge greet(name, greeting = "Hello") {
  emit("{greeting}, {name}!")
}

greet("Alice")              -- Hello, Alice!
greet("Bob", "Good morning") -- Good morning, Bob!
```

### 7.5 Variadic Parameters

A rest parameter collects remaining arguments into an array.

```
forge sum(...nums) {
  grab total = 0
  spin n in nums {
    total += n
  }
  yield total
}

emit(sum(1, 2, 3, 4, 5))  -- 15
```

---

## 8. Object-Oriented Programming

### 8.1 Shapes (Classes)

The `shape` keyword defines a class-like construct. A shape encapsulates data and behavior.

```
shape Circle {
  forge init(radius) {
    self.radius = radius
  }

  forge area() {
    yield 3.14159 * self.radius ** 2
  }

  forge describe() {
    emit("Circle with radius {self.radius}")
  }
}

grab c = Circle(5)
c.describe()       -- Circle with radius 5
emit(c.area())     -- 78.53975
```

### 8.2 Constructors: `forge init()`

The constructor is a method named `init`, declared with `forge`. It is called automatically when a new instance is created. There is no `new` keyword; calling the shape name as a function constructs an instance.

```
shape Point {
  forge init(x, y) {
    self.x = x
    self.y = y
  }
}

grab p = Point(3, 4)
emit(p.x)  -- 3
```

### 8.3 Inheritance: `evolve ... from`

The `evolve` keyword declares a shape that inherits from a parent shape. The child shape gains all methods and properties of the parent.

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
rex.speak()           -- Rex says Woof!
rex.learn("sit")
rex.learn("shake")
rex.show_tricks()
-- Rex knows:
--   - sit
--   - shake
```

The `parent` keyword accesses the parent shape's methods, allowing the child to extend rather than replace behavior.

### 8.4 The `self` Keyword

Inside any shape method, `self` refers to the current instance. It must be used explicitly to access instance properties and methods.

```
shape Timer {
  forge init() {
    self.start = tick()
  }

  forge elapsed() {
    yield tick() - self.start
  }
}
```

---

## 9. Error Handling

### 9.1 `attempt` / `rescue`

The `attempt` block executes code that may fail. If an error occurs, control passes to the `rescue` block, which receives the error value.

```
attempt {
  grab data = read("config.txt")
  emit(data)
} rescue err {
  emit("Failed to read config: {err}")
}
```

An optional `finally`-style cleanup can be achieved with `defer` (see Section 12.2).

### 9.2 Ejecting Errors: `eject`

The `eject` keyword raises an error. It accepts a string message or any value.

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
  emit("Error: {err}")  -- Error: Division by zero
}
```

Custom error shapes can be used for structured errors:

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
}

attempt {
  validate_age(-5)
} rescue err {
  emit("Validation failed on '{err.field}': {err.message}")
}
```

---

## 10. Modules

### 10.1 Importing: `pull`

The `pull` keyword imports functionality from another module. Modules are referenced by file path (without the `.kv` extension) or by standard library name.

```
-- Import an entire module
pull "math"

-- Import specific names
pull {sqrt, abs} from "math"

-- Import with alias
pull "networking" as net
```

### 10.2 Exporting: `expose`

The `expose` keyword makes a declaration available to other modules.

```
-- utils.kv
expose forge clamp(value, low, high) {
  test value < low { yield low }
  test value > high { yield high }
  yield value
}

expose lock VERSION = "1.0.0"
```

```
-- main.kv
pull {clamp, VERSION} from "utils"

emit(clamp(15, 0, 10))  -- 10
emit(VERSION)            -- 1.0.0
```

---

## 11. Input and Output

### 11.1 `emit` -- Print to Screen

`emit` outputs one or more values to standard output, followed by a newline.

```
emit("Hello, world!")
emit(42)
emit("Name:", name, "Age:", age)
```

### 11.2 `absorb` -- Read Input

`absorb` displays an optional prompt and reads a line from standard input, returning it as a string.

```
grab name = absorb("What is your name? ")
grab age = cast(absorb("How old are you? "), "number")

emit("Hello, {name}! You are {age} years old.")
```

---

## 12. Scope and Deferred Execution

### 12.1 Block Scoping

Variables declared with `grab` or `lock` are scoped to the nearest enclosing `{ }` block. Inner blocks can read and modify variables from outer scopes.

```
grab x = 10

test yes {
  grab y = 20
  emit(x)     -- 10 (accessible from outer scope)
  emit(y)     -- 20
}

emit(x)       -- 10
-- emit(y)    -- ERROR: y is not defined in this scope
```

### 12.2 `defer` Blocks

A `defer` block schedules code to run when the enclosing scope exits, regardless of whether the exit is normal or caused by an error. Multiple defers execute in last-in-first-out (LIFO) order.

```
forge process_file(path) {
  grab handle = open(path)
  defer {
    close(handle)
    emit("File closed.")
  }

  -- Work with the file...
  grab content = read(handle)
  yield content
}
-- The defer block runs after the function returns
```

```
forge example() {
  defer { emit("Third") }
  defer { emit("Second") }
  defer { emit("First") }
}

example()
-- Output:
-- First
-- Second
-- Third
```

---

## 13. Built-in Functions

The KOVA standard library provides the following built-in functions. They are available globally without any `pull` statement.

| Function                    | Description                          | Example                                |
|-----------------------------|--------------------------------------|----------------------------------------|
| `emit(value)`               | Print value to stdout                | `emit("hello")`                        |
| `absorb(prompt)`            | Read line from stdin                 | `grab s = absorb(">")`                 |
| `cast(value, type)`         | Convert value to given type          | `cast("42", "number")` = `42`          |
| `span(collection)`          | Return length of array, string, map  | `span([1,2,3])` = `3`                  |
| `fuse(a, b)`                | Concatenate two arrays               | `fuse([1],[2])` = `[1,2]`              |
| `slice(arr, start, end)`    | Return sub-array from start to end   | `slice([1,2,3,4], 1, 3)` = `[2,3]`    |
| `seek(arr, value)`          | Return index of value, or -1         | `seek([5,10,15], 10)` = `1`            |
| `crush(string)`             | Convert string to lowercase          | `crush("HI")` = `"hi"`                |
| `rise(string)`              | Convert string to uppercase          | `rise("hi")` = `"HI"`                 |
| `split(string, delim)`      | Split string into array              | `split("a,b", ",")` = `["a","b"]`     |
| `bond(array, delim)`        | Join array elements into string      | `bond(["a","b"], "-")` = `"a-b"`      |
| `clone(value)`              | Deep copy a value                    | `grab b = clone(a)`                    |
| `kind(value)`               | Return type name as string           | `kind(42)` = `"number"`               |
| `halt(ms)`                  | Pause execution for ms milliseconds  | `halt(1000)`                           |
| `tick()`                    | Current Unix timestamp (ms)          | `grab now = tick()`                    |
| `rand(min, max)`            | Random number in [min, max]          | `rand(1, 100)`                         |
| `keys(map)`                 | Return array of map keys             | `keys({a:1})` = `["a"]`               |
| `vals(map)`                 | Return array of map values           | `vals({a:1})` = `[1]`                  |

---

## 14. String Methods

Strings support the following methods via dot notation.

| Method              | Description                      | Example                                    |
|---------------------|----------------------------------|--------------------------------------------|
| `str.crush()`       | Return lowercase copy            | `"HI".crush()` = `"hi"`                   |
| `str.rise()`        | Return uppercase copy            | `"hi".rise()` = `"HI"`                    |
| `str.trim()`        | Remove leading/trailing spaces   | `"  hi  ".trim()` = `"hi"`               |
| `str.split(delim)`  | Split into array on delimiter    | `"a,b,c".split(",")` = `["a","b","c"]`   |
| `str.has(sub)`      | Check if substring exists        | `"hello".has("ell")` = `yes`              |
| `str.swap(old,new)` | Replace occurrences              | `"aabb".swap("aa","cc")` = `"ccbb"`      |
| `str.span()`        | Return length                    | `"hello".span()` = `5`                    |

```
grab raw = "  Hello, World!  "
grab cleaned = raw.trim().crush()
emit(cleaned)                      -- "hello, world!"
emit(cleaned.has("world"))         -- yes
emit(cleaned.swap("world", "KOVA")) -- "hello, KOVA!"
```

---

## 15. Array Methods

Arrays support the following methods via dot notation.

| Method                              | Description                        | Example                                  |
|-------------------------------------|------------------------------------|------------------------------------------|
| `arr.push(val)`                     | Append value to end (mutates)      | `[1,2].push(3)` = `[1,2,3]`            |
| `arr.pop()`                         | Remove and return last element     | `[1,2,3].pop()` = `3`                   |
| `arr.shift()`                       | Remove and return first element    | `[1,2,3].shift()` = `1`                 |
| `arr.span()`                        | Return length                      | `[1,2,3].span()` = `3`                  |
| `arr.seek(val)`                     | Return index of value, or -1      | `[5,10,15].seek(10)` = `1`              |
| `arr.each(\|item\| => ...)`        | Execute function for each element  | `[1,2].each(\|x\| => emit(x))`         |
| `arr.map(\|item\| => ...)`         | Return new mapped array            | `[1,2].map(\|x\| => x*2)` = `[2,4]`   |
| `arr.sift(\|item\| => ...)`        | Return new filtered array          | `[1,2,3].sift(\|x\| => x>1)` = `[2,3]`|
| `arr.fold(init, \|acc,item\| => ...)`| Reduce to single value           | `[1,2,3].fold(0, \|a,x\| => a+x)` = `6`|
| `arr.sort()`                        | Return sorted copy                | `[3,1,2].sort()` = `[1,2,3]`           |
| `arr.flip()`                        | Return reversed copy              | `[1,2,3].flip()` = `[3,2,1]`           |

```
grab scores = [85, 92, 78, 95, 88]

grab high_scores = scores
  .sift(|s| => s >= 90)
  .sort()
  .flip()

emit(high_scores)  -- [95, 92]

grab total = scores.fold(0, |sum, s| => sum + s)
grab average = total / scores.span()
emit("Average: {average}")  -- Average: 87.6
```

---

## 16. File I/O

KOVA provides built-in functions for file operations.

| Function                       | Description              |
|--------------------------------|--------------------------|
| `read(path)`                   | Read entire file as string |
| `write(path, content)`         | Write string to file (overwrite) |
| `append(path, content)`        | Append string to file    |

```
-- Write a file
write("output.txt", "Hello, KOVA!\n")

-- Append to a file
append("output.txt", "Second line.\n")

-- Read a file
grab content = read("output.txt")
emit(content)
-- Hello, KOVA!
-- Second line.
```

File operations that fail (e.g., file not found) will raise errors that can be caught with `attempt` / `rescue`.

```
attempt {
  grab data = read("missing.txt")
} rescue err {
  emit("Could not read file: {err}")
}
```

---

## 17. Complete Example Program

The following program demonstrates most of KOVA's features in a single, cohesive example: a simple task manager.

```
-- ============================================================
-- KOVA Task Manager
-- A complete example demonstrating the KOVA language.
-- File: task_manager.kv
-- ============================================================

pull {tick} from "std"

{-- 
  Shape: Task
  Represents a single task with a title, priority, and status.
--}
shape Task {
  forge init(title, priority = "normal") {
    self.title = title
    self.priority = priority
    self.done = no
    self.created_at = tick()
  }

  forge complete() {
    self.done = yes
  }

  forge describe() {
    grab status = test self.done { "done" } rival { "pending" }
    grab marker = test self.done { "[x]" } rival { "[ ]" }
    yield "{marker} {self.title} ({self.priority}) - {status}"
  }
}

{--
  Shape: TaskManager
  Manages a collection of tasks with add, complete, and report features.
--}
shape TaskManager {
  forge init() {
    self.tasks = []
  }

  forge add(title, priority = "normal") {
    grab task = Task(title, priority)
    self.tasks.push(task)
    emit("Added: {title}")
    yield task
  }

  forge complete(index) {
    test index < 0 or index >= self.tasks.span() {
      eject "Invalid task index: {index}"
    }
    self.tasks[index].complete()
    emit("Completed: {self.tasks[index].title}")
  }

  forge pending() {
    yield self.tasks.sift(|t| => not t.done)
  }

  forge report() {
    emit("\n--- Task Report ---")
    test self.tasks.span() == 0 {
      emit("No tasks yet.")
      yield void
    }

    spin i from 0 to self.tasks.span() - 1 {
      emit("  {i}. {self.tasks[i].describe()}")
    }

    grab total = self.tasks.span()
    grab done_count = self.tasks.sift(|t| => t.done).span()
    grab pending_count = total - done_count

    emit("\nTotal: {total} | Done: {done_count} | Pending: {pending_count}")
    emit("-------------------\n")
  }
}

-- Priority ranking helper using morph
forge priority_rank(priority) {
  morph priority {
    "critical" => yield 4
    "high"     => yield 3
    "normal"   => yield 2
    "low"      => yield 1
    _          => yield 0
  }
}

-- Sort tasks by priority (highest first) using pipe
forge sort_by_priority(tasks) {
  -- Simple bubble sort for demonstration
  grab sorted = clone(tasks)
  grab n = sorted.span()

  spin i from 0 to n - 2 {
    spin j from 0 to n - 2 - i {
      grab rank_a = priority_rank(sorted[j].priority)
      grab rank_b = priority_rank(sorted[j + 1].priority)
      test rank_a < rank_b {
        grab temp = sorted[j]
        sorted[j] = sorted[j + 1]
        sorted[j + 1] = temp
      }
    }
  }

  yield sorted
}

-- ========== Main Program ==========

grab manager = TaskManager()

-- Add some tasks
manager.add("Write KOVA specification", "critical")
manager.add("Build parser", "high")
manager.add("Design logo", "low")
manager.add("Write unit tests", "normal")
manager.add("Set up CI pipeline", "high")

-- Complete a couple
attempt {
  manager.complete(0)
  manager.complete(3)
} rescue err {
  emit("Error: {err}")
}

-- Generate report
manager.report()

-- Show only pending tasks, sorted by priority
grab pending = manager.pending()
grab sorted = sort_by_priority(pending)

emit("Pending tasks by priority:")
sorted.each(|task| => {
  emit("  - [{task.priority}] {task.title}")
})

-- Demonstrate defer and file output
forge save_report(manager, path) {
  defer {
    emit("Report save operation finished.")
  }

  grab lines = manager.tasks.map(|t| => t.describe())
  grab content = bond(lines, "\n")

  attempt {
    write(path, content)
    emit("Report saved to {path}")
  } rescue err {
    emit("Failed to save report: {err}")
  }
}

save_report(manager, "tasks_report.txt")

-- Interactive mode example (commented out for non-interactive run)
{--
orbit {
  emit("\nCommands: add, done, list, quit")
  grab cmd = absorb("> ")

  morph cmd {
    "add" => {
      grab title = absorb("Task title: ")
      grab prio = absorb("Priority (low/normal/high/critical): ")
      manager.add(title, prio)
    }
    "done" => {
      grab idx = cast(absorb("Task index: "), "number")
      attempt {
        manager.complete(idx)
      } rescue err {
        emit("Error: {err}")
      }
    }
    "list" => manager.report()
    "quit" => snap
    _ => emit("Unknown command: {cmd}")
  }
}

emit("Goodbye!")
--}
```

**Expected output:**

```
Added: Write KOVA specification
Added: Build parser
Added: Design logo
Added: Write unit tests
Added: Set up CI pipeline
Completed: Write KOVA specification
Completed: Write unit tests

--- Task Report ---
  0. [x] Write KOVA specification (critical) - done
  1. [ ] Build parser (high) - pending
  2. [ ] Design logo (low) - pending
  3. [x] Write unit tests (normal) - done
  4. [ ] Set up CI pipeline (high) - pending

Total: 5 | Done: 2 | Pending: 3
-------------------

Pending tasks by priority:
  - [high] Build parser
  - [high] Set up CI pipeline
  - [low] Design logo
Report saved to tasks_report.txt
Report save operation finished.
```

---

## 18. Keyword Reference Table

A complete summary of every KOVA keyword and its purpose.

| KOVA Keyword | Purpose                         | Traditional Equivalent |
|--------------|----------------------------------|------------------------|
| `grab`       | Declare mutable variable         | `let` / `var`          |
| `lock`       | Declare immutable constant       | `const` / `final`      |
| `forge`      | Define a function or method      | `function` / `def`     |
| `yield`      | Return a value from a function   | `return`               |
| `emit`       | Print to standard output         | `print` / `console.log`|
| `absorb`     | Read input from user             | `input` / `readline`   |
| `test`       | Conditional branch (if)          | `if`                   |
| `also`       | Additional condition (else if)   | `else if` / `elif`     |
| `rival`      | Fallback branch (else)           | `else`                 |
| `spin`       | Counted / collection loop        | `for`                  |
| `from`       | Start of range in spin loop      | (part of for syntax)   |
| `to`         | End of range in spin loop        | (part of for syntax)   |
| `in`         | Iterate over collection          | `in`                   |
| `by`         | Step size in spin loop           | `step`                 |
| `orbit`      | Conditional loop (while)         | `while`                |
| `snap`       | Exit loop immediately            | `break`                |
| `skip`       | Skip to next iteration           | `continue`             |
| `shape`      | Define a class / type            | `class` / `struct`     |
| `evolve`     | Inherit from a parent shape      | `extends` / `inherits` |
| `self`       | Reference to current instance    | `this` / `self`        |
| `parent`     | Reference to parent shape        | `super`                |
| `attempt`    | Begin error-handled block        | `try`                  |
| `rescue`     | Handle error from attempt        | `catch` / `except`     |
| `eject`      | Raise / throw an error           | `throw` / `raise`      |
| `pull`       | Import a module                  | `import` / `require`   |
| `expose`     | Export a declaration             | `export` / `module.exports`|
| `defer`      | Schedule cleanup at scope exit   | (Go's `defer`)         |
| `morph`      | Pattern match on a value         | `match` / `switch`     |
| `and`        | Logical AND                      | `&&` / `and`           |
| `or`         | Logical OR                       | `\|\|` / `or`          |
| `not`        | Logical NOT                      | `!` / `not`            |
| `yes`        | Boolean true                     | `true` / `True`        |
| `no`         | Boolean false                    | `false` / `False`      |
| `void`       | Null / absence of value          | `null` / `nil` / `None`|
| `\|>`        | Pipe operator                    | (Elixir's `\|>`)       |
| `..`         | Range operator                   | (Ruby's `..`)          |

---

*KOVA Language Specification v1.0 -- End of Document*
