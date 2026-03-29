function extractValue(text) {
  text = text.toLowerCase();

  if (text.includes("heavy") || text.includes("slow") || text.includes("congestion"))
    return "Heavy";
  else if (text.includes("moderate"))
    return "Moderate";
  else
    return "Low";
}

function resolve() {
  let input = document.getElementById("input").value.split("\n");

  let mapping = {"Low":1, "Moderate":2, "Heavy":3};
  let scores = {};
  let analysisHTML = "";
  let values = [];

  input.forEach((line, i) => {
    let value = extractValue(line);
    values.push(value);

    let trust = 0.9 - (i * 0.2);
    let score = mapping[value] * trust;

    scores[value] = (scores[value] || 0) + score;

    analysisHTML += `<p>${value} → Score: ${score.toFixed(2)}</p>`;
  });

  let result = Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b);

  let total = Object.values(scores).reduce((a,b)=>a+b,0);
  let confidence = (scores[result] / total) * 100;

  let unique = new Set(values);
  let conflict = "";
  if(unique.size == 1) conflict = "No Conflict";
  else if(unique.size == 2) conflict = "Moderate Conflict";
  else conflict = "High Conflict";

  document.getElementById("analysis").innerHTML =
    "<h3>Analysis</h3>" + analysisHTML;

  document.getElementById("result").innerHTML = `
    <h2>Final Decision: ${result} Traffic</h2>
    <h3>Confidence: ${confidence.toFixed(2)}%</h3>
    <h3>Conflict Level: ${conflict}</h3>
  `;
}