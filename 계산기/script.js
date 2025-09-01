<script>
let display = document.getElementById("display");
let current = "";

function press(val) {
  if (display.innerText === "0") display.innerText = val;
  else display.innerText += val;
}

function calculate() {
  try {
    display.innerText = eval(display.innerText);
  } catch {
    display.innerText = "Error";
  }
}

function changeSkin(skinFile) {
  document.getElementById("calculator-image").src = `skins/${skinFile}`;
}
</script>
</body>
</html>
