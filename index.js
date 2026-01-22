import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import fetch from "node-fetch";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("Backend running with Gemini Flash 🚀");
});

app.post("/generate-itinerary", async (req, res) => {
  try {
    const { location, budget, days, interests, groupSize } = req.body;

    const prompt = `
Create a ${days}-day student travel itinerary.
Location: ${location}
Budget: ${budget}
Group size: ${groupSize}
Interests: ${interests}

Include:
- Day-wise plan
- Budget food & stay
- Cost breakdown
`;

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [
            {
              role: "user",
              parts: [{ text: prompt }],
            },
          ],
        }),
      }
    );

    // ✅ CORRECT CHECK
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText);
    }

    // ✅ CORRECT JSON
    const data = await response.json();

    const text =
      data?.candidates?.[0]?.content?.parts?.[0]?.text;

    if (!text) {
      return res.status(500).json({
        error: "Empty Gemini response",
      });
    }

    res.json({ itinerary: text });

  } catch (err) {
    console.error("BACKEND ERROR:", err.message);
    res.status(500).json({
      error: err.message,
    });
  }
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`✅ Backend running on port ${PORT}`);
});
