const express = require("express");
const http = require("http");
const socketio = require("socket.io");
const axios = require("axios");

require("dotenv").config();
const { generateContent } = require("./ai/modelSelector");

const app = express();
const server = http.createServer(app);
const io = socketio(server);

app.use(express.static("public"));
app.use(express.json());

// ================= STEPS =================
const steps = [
  { name: "Prompt Input", status: "pending" },
  { name: "AI Generation", status: "pending" },
  { name: "Preview & Edit", status: "pending" },
  { name: "LinkedIn OAuth", status: "pending" },
  { name: "Access Token", status: "pending" },
  { name: "Profile Fetch", status: "pending" },
  { name: "Post to LinkedIn", status: "pending" }
];

// ================= STATE =================
let state = {
  prompt: "",
  content: "",
  edited: "",
  mediaUrl: "",
  asset: null,
  provider: "groq",
  code: null,
  token: null,
  userId: null
};
// ================= CLEAN PROMPT ==============
async function cleanPrompt(prompt) {
  return prompt
    .replace(/\[.*?\]/g, "")   // remove brackets
    .replace(/\n/g, " ")       // remove newlines
    .slice(0, 200);            // limit length
}
// ================= IMAGE GEN =================
async function generateImage(prompt) {
const updatedPrompt = await cleanPrompt(prompt);
return `https://image.pollinations.ai/prompt/${encodeURIComponent(updatedPrompt)}`;
}
// ===== formating ======
function fixJSONString(raw) {
  let inString = false;
  let escaped = false;
  let result = "";

  for (let i = 0; i < raw.length; i++) {
    const char = raw[i];

    if (char === '"' && !escaped) {
      inString = !inString;
    }

    if (inString) {
      if (char === '\n') {
        result += '\\n';
        continue;
      }
      if (char === '\r') continue;
    }

    if (char === '\\' && !escaped) {
      escaped = true;
    } else {
      escaped = false;
    }

    result += char;
  }

  return result;
}
// ================= CALLBACK =================
app.get("/callback", (req, res) => {
  state.code = req.query.code;
  steps[3].status = "approved";

  io.emit("state", { steps, state });
  res.send("Auth success. Close tab.");
});

// ================= SOCKET =================
io.on("connection", (socket) => {
  socket.emit("state", { steps, state });

  // PROMPT
  socket.on("set_prompt", (prompt) => {
    state.prompt = prompt;
    steps[0].status = "approved";
    io.emit("state", { steps, state });
  });

  // MODEL
  socket.on("set_provider", (provider) => {
    state.provider = provider;
  });

  // GENERATE
  socket.on("generate", async () => {
    try {
      steps[1].status = "processing";
      io.emit("state", { steps, state });

      const raw = await generateContent(state.prompt, state.provider);
      let parsed;

try {
  parsed = JSON.parse(raw);
} catch (e) {
  try {
    let cleaned = raw
      .trim()
      .replace(/^\uFEFF/, "")
      .replace(/```json/g, "")
      .replace(/```/g, "")
      .replace(/^[^{]*/, "")
      .replace(/[^}]*$/, "");

    cleaned = fixJSONString(cleaned);

    parsed = JSON.parse(cleaned);
  } catch (err) {
    console.error("❌ FINAL FAILED RAW:\n", raw);
    throw new Error("AI returned invalid JSON");
  }
}
      

      state.content = `
${parsed.hook}

${parsed.context}

${parsed.body}

💡 ${parsed.takeaway}

${parsed.cta}

${parsed.hashtags}
`;

      state.edited = state.content;

      // 🔥 IMAGE
      state.mediaUrl = await generateImage(parsed.mediaIdea);

      steps[1].status = "approved";
      steps[2].status = "ready";

      io.emit("state", { steps, state });

    } catch (err) {
      socket.emit("error", err.message);
    }
  });

  // EDIT
  socket.on("edit", (text) => {
    state.edited = text;
    steps[2].status = "approved";
    io.emit("state", { steps, state });
  });

  // OAUTH
  socket.on("oauth", () => {
    const url =
      `https://www.linkedin.com/oauth/v2/authorization?response_type=code` +
      `&client_id=${process.env.CLIENT_ID}` +
      `&redirect_uri=${encodeURIComponent(process.env.REDIRECT_URI)}` +
      `&scope=openid%20profile%20w_member_social`;

    socket.emit("oauth_url", url);
  });

  // TOKEN
  socket.on("token", async () => {
    const params = new URLSearchParams({
      grant_type: "authorization_code",
      code: state.code,
      redirect_uri: process.env.REDIRECT_URI,
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET
    });

    const res = await axios.post(
      "https://www.linkedin.com/oauth/v2/accessToken",
      params
    );

    state.token = res.data.access_token;
    steps[4].status = "approved";

    io.emit("state", { steps, state });
  });

  // PROFILE
  socket.on("profile", async () => {
    const res = await axios.get(
      "https://api.linkedin.com/v2/userinfo",
      {
        headers: { Authorization: `Bearer ${state.token}` }
      }
    );

    state.userId = res.data.sub;
    steps[5].status = "approved";

    io.emit("state", { steps, state });
  });

  // UPLOAD IMAGE
  async function uploadImage() {
    const register = await axios.post(
      "https://api.linkedin.com/v2/assets?action=registerUpload",
      {
        registerUploadRequest: {
          recipes: ["urn:li:digitalmediaRecipe:feedshare-image"],
          owner: `urn:li:person:${state.userId}`,
          serviceRelationships: [
            {
              relationshipType: "OWNER",
              identifier: "urn:li:userGeneratedContent"
            }
          ]
        }
      },
      {
        headers: { Authorization: `Bearer ${state.token}` }
      }
    );

    const uploadUrl =
      register.data.value.uploadMechanism[
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
      ].uploadUrl;

    state.asset = register.data.value.asset;

    const img = await axios.get(state.mediaUrl, {
      responseType: "arraybuffer"
    });

    await axios.put(uploadUrl, img.data, {
      headers: { "Content-Type": "image/jpeg" }
    });
  }

  // POST
  socket.on("post", async () => {
    try {
      await uploadImage();

      const body = {
        author: `urn:li:person:${state.userId}`,
        lifecycleState: "PUBLISHED",
        specificContent: {
          "com.linkedin.ugc.ShareContent": {
            shareCommentary: { text: state.edited },
            shareMediaCategory: "IMAGE",
            media: [
              {
                status: "READY",
                media: state.asset
              }
            ]
          }
        },
        visibility: {
          "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
      };

      await axios.post(
        "https://api.linkedin.com/v2/ugcPosts",
        body,
        {
          headers: {
            Authorization: `Bearer ${state.token}`,
            "X-Restli-Protocol-Version": "2.0.0"
          }
        }
      );

      steps[6].status = "approved";
      io.emit("state", { steps, state });

      socket.emit("posted");

    } catch (err) {
      socket.emit("error", err.message);
    }
  });
});

server.listen(54321, () => console.log("Server running"));