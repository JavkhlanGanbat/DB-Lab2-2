const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql");

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "root",
  database: "test",
});

db.connect((err) => {
  if (err) {
    console.error("Database connection error:", err.message);
    process.exit(1);
  }
  console.log("Connected to database.");
});

app.get("/", (req, res) => {
  res.send(`
    <h1>Login</h1>
    <form method="POST" action="/login">
      <label>Username:</label><br>
      <input type="text" name="username" /><br><br>
      <label>Password:</label><br>
      <input type="password" name="password" /><br><br>
      <button type="submit">Login</button>
    </form>
  `);
});

app.post("/login", (req, res) => {
  const { username, password } = req.body;

  console.log("Received username:", username);
  console.log("Received password:", password);

  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;

  console.log(`Executing query: ${query}`);

  db.query(query, (err, results) => {
    if (err) {
      console.error("SQL Error:", err.message);
      res.send(`<h1>Database Error: ${err.message}</h1>`);
      return;
    }

    if (results.length > 0) {
      res.send(`<h1>Welcome</h1>`);
    } else {
      res.send("<h1>Invalid credentials.</h1>");
    }
  });
});

app.listen(3000, () => {
  console.log("http://localhost:3000");
});
