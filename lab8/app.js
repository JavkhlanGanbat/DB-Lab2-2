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
  database: process.env.DBNAME,
});

db.connect((err) => {
  if (err) {
    console.error("Database connection error:", err.message);
    process.exit(1);
  }

  console.log("Connected to database");
  console.log(`
    host: ${process.env.MYSQL_HOST}
    port: ${process.env.MYSQL_PORT}
    user: ${process.env.MYSQL_USER}
    schema: ${process.env.MYSQL_DBNAME}`);
})

/*
app.get('/data', (req, res) => {
  db.query('SELECT * FROM book.Authors', (err, results) => {
    if (err) {
      console.error('Error querying the database:', err.message);
      res.status(500).send('Database query error');
    } else {
      res.json(results);
    }
  });
});

*/

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

  const query = `SELECT * FROM book.Users WHERE username = '${username}' AND password = '${password}'`;
  // const querySimple = `SELECT * FROM book.Users`;

  console.log(`Executing query: ${query}`);
  // console.log(`Executing query: ${querySimple}`);

  db.query(query, (err, results) => {
    if (err) {
      console.error("SQL Error:", err.message);
      res.send(`<h1>Database Error: ${err.message}</h1>`);
      return;
    }

    if (results.length > 0) {
      res.send(`<h1>Welcome, ${username}</h1>`);
    } else {
      res.send("<h1>Invalid credentials.</h1>");
    }
  });
});

app.get('/home', (req, res) => {
  res.send('Hello, world!');
});

app.listen(process.env.PORT, () => {
  // console.log("http://localhost:3000");
  console.log(`Server running at http://localhost:${process.env.PORT}`);
});
