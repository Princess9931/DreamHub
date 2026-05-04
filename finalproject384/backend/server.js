// ================= IMPORTS =================
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bcrypt = require("bcryptjs");
const path = require("path");
require("dotenv").config();

const app = express();

// ================= MIDDLEWARE =================
app.use(express.json());
app.use(cors());
app.use(express.static(path.join(__dirname, "..")));

// ================= MONGODB CONNECTION =================
mongoose.connect(process.env.MONGO_URI)
.then(() => console.log("MongoDB Connected ✅"))
.catch((err) => console.log("Error ❌", err));

// ================= USER SCHEMA =================
const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    password: { type: String, required: true }
});

const User = mongoose.model("User", userSchema);

// ================= REGISTER API =================
app.post("/register", async (req, res) => {
    try {
        const { username, password } = req.body;

        const existingUser = await User.findOne({ username });
        if (existingUser) {
            return res.status(400).json({ msg: "User already exists ❌" });
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        const newUser = new User({ username, password: hashedPassword });
        await newUser.save();

        res.status(201).json({ msg: "Registered Successfully ✅" });

    } catch (err) {
        res.status(500).json({ msg: "Error ❌", error: err.message });
    }
});

// ================= LOGIN API =================
app.post("/login", async (req, res) => {
    try {
        const { username, password } = req.body;
        const user = await User.findOne({ username });

        if (!user) {
            return res.status(404).json({ msg: "User not found ❌" }); // FIXED: 'return' typo
        }
        
        const isMatch = await bcrypt.compare(password, user.password);
        
        if (isMatch) {
          res.json({ msg: "Login Success ✅" }); // FIXED: Emoji syntax
        } else {
            res.status(401).json({ msg: "Invalid Credentials ❌" });
        }

    } catch (err) {
        res.status(500).json({ msg: "Error ❌", error: err.message });
    }
});

// ================= TEST ROUTE =================
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "..", "index.html"));
});

// ================= START SERVER =================
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  // FIXED: Used backticks for template literal
  console.log(`Server running on port ${PORT} 🚀`); 
});