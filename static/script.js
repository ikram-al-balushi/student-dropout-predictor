// =====================================================
// Muhammad Ikram — Student Dropout Predictor
// Frontend JS: sliders + fetch to Flask /predict API
// =====================================================

// Slider ke saath uska number live update karo
const sliders = ["attendance", "fee_delay_days", "marks_avg", "months_enrolled"];

sliders.forEach(function (id) {
  const slider = document.getElementById(id);
  const valueBox = document.getElementById(id + "_val");

  slider.addEventListener("input", function () {
    valueBox.textContent = slider.value;
  });
});

// Button dabne pe — 4 values Flask ko bhejo, jawab dikhao
document.getElementById("checkBtn").addEventListener("click", async function () {

  // 1. Charon sliders ki values lo
  const data = {
    attendance: document.getElementById("attendance").value,
    fee_delay_days: document.getElementById("fee_delay_days").value,
    marks_avg: document.getElementById("marks_avg").value,
    months_enrolled: document.getElementById("months_enrolled").value
  };

  // 2. Flask ke /predict route ko bhejo (POST + JSON)
  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await response.json();

  // 3. Result card dikhao
  document.getElementById("resultCard").classList.remove("hidden");

  // 4. Risk number, gauge, level, action bharo
  document.getElementById("riskValue").textContent = result.risk;
  document.getElementById("gaugeFill").style.width = result.risk + "%";
  document.getElementById("riskLevel").textContent = "RISK: " + result.level;
  document.getElementById("riskAction").textContent = result.action;
});
