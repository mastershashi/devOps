const axios = require("axios");
const { GoogleGenerativeAI } = require("@google/generative-ai");

function cleanJSON(text) {
  return text.replace(/```json|```/g, "").trim();
}

async function generateContent(prompt, provider) {
  const systemPrompt = `
  You are an expert LinkedIn content writer.
  
  Your job is to create high quality, engaging LinkedIn posts.
  Always follow this structure step by step:
  1. Strong hook 1 line
  2. Context 2 to 3 short lines
  3. Main insight short paragraphs or bullets
  4. Key takeaway
  5. Call to action
  
  Rules
  - Keep sentences short
  - Use clean spacing like LinkedIn posts
  - Max 1 to 2 emojis
  - No fluff no generic phrases
  - Sound human not AI
  
  MEDIA RULES :
  - mediaIdea must be a VISUAL description
  - Max 10 to 12 words
  - Use only concrete objects people, laptop, charts, office, AI, robot, etc.
  - DO NOT use abstract words like growth, success, convergence, ecosystem
  - DO NOT use instructions like "create", "include", "show"
  - Think like an image prompt, not a sentence
  
  HASHTAG RULES:
  - 4 to 6 relevant hashtags
  - lowercase
  - no spaces inside hashtags
  
  Return ONLY valid JSON:
  {
    "hook": "",
    "context": "",
    "body": "",
    "takeaway": "",
    "cta": "",
    "mediaIdea": "",
    "hashtags": ""
  }
  `;

  const userPrompt = `
Topic: ${prompt}
Write a high-quality LinkedIn post.
`;

  // -------- GROQ --------
  if (provider === "groq") {
    const res = await axios.post(
      "https://api.groq.com/openai/v1/chat/completions",
      {
        model: "llama-3.1-8b-instant",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userPrompt }
        ]
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.GROQ_API_KEY}`
        }
      }
    );

    return cleanJSON(res.data.choices[0].message.content);
  }

  // -------- OPENAI --------
  if (provider === "openai") {
    const res = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-4o-mini",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userPrompt }
        ]
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.OPENAI_API_KEY}`
        }
      }
    );

    return cleanJSON(res.data.choices[0].message.content);
  }

  // -------- GEMINI --------
  if (provider === "gemini") {
    const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

    const model = genAI.getGenerativeModel({
      model: "gemini-1.5-flash",
      systemInstruction: systemPrompt
    });

    const result = await model.generateContent({
      contents: [{ role: "user", parts: [{ text: userPrompt }] }]
    });

    return cleanJSON(result.response.text());
  }

  throw new Error("Invalid provider");
}

module.exports = { generateContent };