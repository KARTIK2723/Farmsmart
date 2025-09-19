document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("cropForm");
  const responseBox = document.getElementById("result");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const location = document.getElementById("location").value.trim();
    const rainfall = document.getElementById("rainfall").value;

    responseBox.style.display = "block";
    responseBox.innerHTML = "⏳ Fetching recommendation...";

    try {
      const res = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ location, rainfall }),
      });

      const data = await res.json();

      if (data.error) {
        responseBox.innerHTML = `⚠️ ${data.error}`;
      } else {
        responseBox.innerHTML = `
          <h3>🌾 Recommendation</h3>
          ✅ <b>${data.crop}</b><br>
          🌱 Soil Type: ${data.soil}<br>
          ☔ Rainfall: ${data.rainfall}
        `;
      }
    } catch (error) {
      console.error("Fetch error:", error);
      responseBox.innerHTML = "❌ Error connecting to server.";
    }
  });
});
