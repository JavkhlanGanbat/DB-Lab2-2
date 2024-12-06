const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql2");

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

const db = mysql.createConnection({
  host: process.env.MYSQL_HOST || 'localhost',
  port: process.env.MYSQL_PORT || 3000,
  user: process.env.MYSQL_USER || 'root',
  password: process.env.MYSQL_PASS,
  database: process.env.DBNAME
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

  // prepared statements
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
app.listen(process.env.PORT, () => {
  // console.log("http://localhost:3000");
  console.log(`Server running at http://localhost:${process.env.PORT}`);
});

