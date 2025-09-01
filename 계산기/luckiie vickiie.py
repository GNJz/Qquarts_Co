<!-- index.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Casio 계산기 시뮬레이터</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="skin-selector">
    <label for="skin">스킨 선택:</label>
    <select id="skin" onchange="changeSkin(this.value)">
      <option value="fx991es.png">Casio fx-991ES</option>
      <!-- 추가 스킨은 여기 옵션에 계속 넣으면 돼 -->
    </select>
  </div>

  <div class="calculator">
    <img id="calculator-image" src="skins/fx991es.png" alt="계산기 스킨" />
    
    <!-- 버튼 예시: sin, cos, = -->
    <button class="btn" style="top: 170px; left: 135px;" onclick="onButtonPress('sin')">sin</button>
    <button class="btn" style="top: 170px; left: 185px;" onclick="onButtonPress('cos')">cos</button>
    <button class="btn" style="top: 500px; left: 220px;" onclick="onButtonPress('=')">=</button>
  </div>

  <script src="script.js"></script>
</body>
</html>