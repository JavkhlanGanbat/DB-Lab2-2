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

  const query = `SELECT * FROM users WHERE username = ? AND password = ?`;

  db.query(query, [username, password], (err, results) => {
    if (err) {
      console.error("Database Error:", err.message);

      res.send(`
        <h1>Error</h1>
        <p>Please try again later.</p>
      `);
      return;
    }

    if (results.length > 0) {
      res.send(`
        <h1>Welcome</h1>
        <p>Welcome</p>
      `);
    } else {
      res.send(`
        <h1>Username or password wrong</h1>
      `);
    }
  });
});

// Start Server
app.listen(3000, () => {
  console.log("http://localhost:3000");
});
