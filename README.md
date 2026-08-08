<!-- KOVΛ - code. create. evolve. -->

<p align="center">
  <img src="logo.png" alt="KOVΛ Logo" width="280">
</p>

<h1 align="center">KOVΛ</h1>

<p align="center">
  <strong>code. create. evolve.</strong>
</p>

<p align="center">
  <code>&lt;/&gt;</code>
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#examples">Examples</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#language-spec">Language Spec</a> •
  <a href="#contributing">Contributing</a>
</p>

---

## About

**KOVΛ** is a brand-new programming language built entirely from scratch by **phonmasverical**.

Every keyword is original — KOVΛ doesn't borrow syntax from any existing language.

- 🧠 **Clarity** — Clean, readable syntax that makes intent obvious
- ⚡ **Performance** — Fast compilation, smooth execution
- 🔧 **Versatile** — General purpose: web, apps, games, AI
- 🌍 **Open** — Open source, community driven

## Features

| Feature | Description |
|---|---|
| 🎯 Original Syntax | Completely new keywords — `grab`, `forge`, `spin`, `morph` |
| 🔄 Interpreter | Python-based interpreter |
| 📦 Auto Import | AI assistant for automatic library imports |
| 🧩 Data Types | Numbers, strings, booleans (`yes`/`no`), arrays, maps, `void` |
| 🎨 Variables | `grab` (mutable) / `lock` (immutable) |
| 🔨 Functions | `forge` to define, `yield` to return, lambda support |
| 🔁 Loops | `spin` (for) / `orbit` (while) / `snap` & `skip` |
| 🔀 Conditionals | `test` / `also` / `rival` |
| 🧬 OOP | `shape` (class) / `evolve` (inherit) |
| 🎭 Pattern Match | `morph` with guards and destructuring |
| 🛡️ Error Handling | `attempt` / `rescue` / `eject` |
| 📦 Modules | `pull` (import) / `expose` (export) |
| 🔗 Pipe Operator | `value |> func1 |> func2` |
| ⏳ Defer | `defer { ... }` — cleanup at scope exit |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/phonmasverical/KOVA.git
cd KOVA

# Run a KOVΛ program
python kova.py hello.kv
```

## Examples

### Hello World
```
emit("Hello, World!")
```

### Variables & Constants
```
grab name = "KOVΛ"
grab age = 1
lock VERSION = "1.0.0"

emit("Welcome to {name} v{VERSION}")
```

### Functions
```
forge greet(name) {
  yield "Hello, " + name + "!"
}

grab message = greet("bro")
emit(message)
```

### Conditionals
```
grab score = 85

test score >= 90 {
  emit("Excellent!")
} also score >= 70 {
  emit("Good job!")
} rival {
  emit("Keep trying!")
}
```

### Loops
```
-- Counted loop
spin i from 1 to 10 {
  emit(i)
}

-- Collection loop
grab colors = ["red", "green", "blue"]
spin color in colors {
  emit(color)
}

-- While loop
grab x = 0
orbit x < 100 {
  grab x = x + 1
}
```

### OOP
```
shape Animal {
  forge init(name, sound) {
    self.name = name
    self.sound = sound
  }

  forge speak() {
    emit(self.name + " says " + self.sound)
  }
}

evolve Dog from Animal {
  forge init(name) {
    parent.init(name, "Woof!")
  }

  forge fetch(item) {
    emit(self.name + " fetches the " + item)
  }
}

grab dog = Dog("Rex")
dog.speak()
dog.fetch("ball")
```

### Pattern Matching
```
grab status = 404

morph status {
  200 => emit("OK")
  404 => emit("Not Found")
  500 => emit("Server Error")
  _ => emit("Unknown: {status}")
}
```

### Pipe Operator
```
grab result = [1, 2, 3, 4, 5]
  |> arr.map(|x| => x * 2)
  |> arr.sift(|x| => x > 4)
  |> arr.fold(0, |acc, x| => acc + x)

emit(result)
```

### Error Handling
```
attempt {
  grab data = read("config.kv")
  emit(data)
} rescue err {
  emit("Error: {err}")
}
```

## Language Spec

📖 Full language specification: **[language-spec.md](language-spec.md)**

The spec covers all 37 unique KOVΛ keywords, data types, operators, control flow, OOP, modules, built-in functions, and more.

## Roadmap

- [x] Design language syntax & keywords
- [x] Create GitHub repository
- [x] Write Language Specification v1.0
- [ ] Build lexer (tokenizer)
- [ ] Build parser (AST generator)
- [ ] Build interpreter
- [ ] Standard library
- [ ] REPL (interactive mode)
- [ ] Package manager
- [ ] Documentation website
- [ ] VS Code extension

## Contributing

KOVΛ is open source. All contributions are welcome!

1. Fork the repo
2. Create a new branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## Author

**phonmasverical** — Creator & Lead Developer

## License

MIT License © 2026 phonmasverical

---

<p align="center">
  <sub>Built with ❤️ by phonmasverical</sub>
</p>
