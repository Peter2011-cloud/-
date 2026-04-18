<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>第3题动态演示</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
      background: #f3f6fb;
      color: #1f2937;
    }
    .wrap {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
      display: grid;
      grid-template-columns: 1.35fr 0.85fr;
      gap: 20px;
    }
    .card {
      background: #fff;
      border-radius: 20px;
      box-shadow: 0 12px 36px rgba(15, 23, 42, 0.08);
      overflow: hidden;
    }
    .left {
      padding: 16px;
    }
    canvas {
      width: 100%;
      height: 660px;
      display: block;
      background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
      border-radius: 16px;
    }
    .right {
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    h1 {
      margin: 0;
      font-size: 24px;
      line-height: 1.35;
    }
    .desc {
      font-size: 14px;
      line-height: 1.8;
      color: #475569;
    }
    .row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }
    button {
      border: 0;
      border-radius: 12px;
      padding: 10px 16px;
      font-size: 14px;
      cursor: pointer;
      background: #111827;
      color: #fff;
    }
    button.secondary {
      background: #e5e7eb;
      color: #111827;
    }
    input[type="range"] {
      width: 100%;
    }
    .stats {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }
    .stat {
      border: 1px solid #e5e7eb;
      background: #f8fafc;
      border-radius: 16px;
      padding: 14px;
    }
    .k {
      font-size: 13px;
      color: #64748b;
      margin-bottom: 8px;
    }
    .v {
      font-size: 28px;
      font-weight: 700;
      color: #0f172a;
    }
    .tip, .legend, .note {
      border: 1px solid #e5e7eb;
      background: #f8fafc;
      border-radius: 16px;
      padding: 14px 16px;
      font-size: 14px;
      line-height: 1.8;
      color: #334155;
    }
    .legend-line {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
    }
    .legend-line:last-child { margin-bottom: 0; }
    .swatch {
      width: 16px;
      height: 4px;
      border-radius: 999px;
      display: inline-block;
      flex: 0 0 auto;
    }
    .small {
      font-size: 13px;
      color: #64748b;
    }
    @media (max-width: 980px) {
      .wrap { grid-template-columns: 1fr; }
      canvas { height: 520px; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card left">
      <canvas id="stage" width="860" height="660"></canvas>
    </div>

    <div class="card right">
      <div>
        <h1>第3题动态过程演示</h1>
        <div class="desc">
          在等边 △ABC 中，AD ⟂ BC 于点 D，AC = 6，F 是线段 AD 上的动点。连接 BF，以 BF 为边作等边 △BFE，再连接 DE。<br>
          下面直接演示点 F 运动时，图形如何变化，以及线段 DE 的长度如何变化。
        </div>
      </div>

      <div class="row">
        <button id="playBtn">暂停</button>
        <button id="resetBtn" class="secondary">回到起点</button>
      </div>

      <div>
        <div class="small">拖动点 F 的位置（D → A）</div>
        <input id="slider" type="range" min="0" max="1000" value="0" />
      </div>

      <div class="stats">
        <div class="stat">
          <div class="k">当前 DE 长度</div>
          <div class="v" id="deNow">0</div>
        </div>
        <div class="stat">
          <div class="k">最小值</div>
          <div class="v" id="deMin">3/2</div>
        </div>
      </div>

      <div class="tip" id="tipBox"></div>

      <div class="legend">
        <div class="legend-line"><span class="swatch" style="background:#2563eb"></span> 蓝色：等边三角形 BFE</div>
        <div class="legend-line"><span class="swatch" style="background:#ef4444"></span> 红色：当前线段 DE</div>
        <div class="legend-line"><span class="swatch" style="background:#16a34a"></span> 绿色虚线：DE 最短时的位置</div>
        <div class="legend-line"><span class="swatch" style="background:#cbd5e1"></span> 灰色虚线：点 E 的轨迹</div>
      </div>

      <div class="note">
        这一版我改成了更稳的 <b>Canvas 绘图</b>，避免之前 SVG 显示异常。<br>
        同时只保留题目真正需要的那一侧，不再切换两侧，避免画面和学生理解都被干扰。<br>
        从动画中你会看到：当 <b>F</b> 走到 <b>AD 的中点</b> 时，<b>DE</b> 取得最小值 <b>3/2</b>。
      </div>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('stage');
    const ctx = canvas.getContext('2d');
    const slider = document.getElementById('slider');
    const playBtn = document.getElementById('playBtn');
    const resetBtn = document.getElementById('resetBtn');
    const deNowEl = document.getElementById('deNow');
    const tipBox = document.getElementById('tipBox');

    const SQRT3 = Math.sqrt(3);
    const side = 6;
    const height = 3 * SQRT3;

    const geom = {
      A: { x: 0, y: height },
      B: { x: -3, y: 0 },
      C: { x: 3, y: 0 },
      D: { x: 0, y: 0 }
    };

    const view = {
      left: -5.3,
      right: 6.8,
      bottom: -1.8,
      top: 6.8
    };

    let playing = true;
    let value = 0;
    let direction = 1;

    function mapX(x) {
      return (x - view.left) / (view.right - view.left) * canvas.width;
    }

    function mapY(y) {
      return canvas.height - (y - view.bottom) / (view.top - view.bottom) * canvas.height;
    }

    function toScreen(p) {
      return { x: mapX(p.x), y: mapY(p.y) };
    }

    function dist(P, Q) {
      return Math.hypot(P.x - Q.x, P.y - Q.y);
    }

    function rotate(vx, vy, angle) {
      const c = Math.cos(angle);
      const s = Math.sin(angle);
      return {
        x: vx * c - vy * s,
        y: vx * s + vy * c
      };
    }

    function formatNum(n) {
      const r = Math.round(n * 1000) / 1000;
      return Number.isInteger(r) ? String(r) : r.toFixed(3).replace(/0+$/, '').replace(/\.$/, '');
    }

    function stateFromU(u) {
      const t = u * height;
      const F = { x: 0, y: t };
      const BF = { x: F.x - geom.B.x, y: F.y - geom.B.y };

      // 取题目常见解答对应的一侧：E 在 BC 下方附近，最小值为 3/2
      const r = rotate(BF.x, BF.y, -Math.PI / 3);
      const E = { x: geom.B.x + r.x, y: geom.B.y + r.y };

      const Fmin = { x: 0, y: height / 2 };
      const BFmin = { x: Fmin.x - geom.B.x, y: Fmin.y - geom.B.y };
      const rmin = rotate(BFmin.x, BFmin.y, -Math.PI / 3);
      const Emin = { x: geom.B.x + rmin.x, y: geom.B.y + rmin.y };

      return {
        F,
        E,
        Fmin,
        Emin,
        DE: dist(geom.D, E)
      };
    }

    function drawPoint(p, label, color = '#111827', dx = 10, dy = -10, r = 7) {
      const s = toScreen(p);
      ctx.beginPath();
      ctx.arc(s.x, s.y, r, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
      ctx.fillStyle = color;
      ctx.font = '700 22px Microsoft YaHei, sans-serif';
      ctx.fillText(label, s.x + dx, s.y + dy);
    }

    function drawLine(P, Q, options = {}) {
      const a = toScreen(P);
      const b = toScreen(Q);
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.lineWidth = options.lineWidth || 3;
      ctx.strokeStyle = options.strokeStyle || '#111827';
      if (options.dash) ctx.setLineDash(options.dash);
      ctx.stroke();
      ctx.restore();
    }

    function drawPolygon(points, options = {}) {
      if (!points.length) return;
      ctx.save();
      const first = toScreen(points[0]);
      ctx.beginPath();
      ctx.moveTo(first.x, first.y);
      for (let i = 1; i < points.length; i++) {
        const s = toScreen(points[i]);
        ctx.lineTo(s.x, s.y);
      }
      ctx.closePath();
      if (options.fillStyle) {
        ctx.fillStyle = options.fillStyle;
        ctx.fill();
      }
      ctx.lineWidth = options.lineWidth || 3;
      ctx.strokeStyle = options.strokeStyle || '#111827';
      ctx.stroke();
      ctx.restore();
    }

    function drawTrail() {
      ctx.save();
      ctx.beginPath();
      for (let i = 0; i <= 120; i++) {
        const u = i / 120;
        const E = stateFromU(u).E;
        const s = toScreen(E);
        if (i === 0) ctx.moveTo(s.x, s.y);
        else ctx.lineTo(s.x, s.y);
      }
      ctx.setLineDash([7, 6]);
      ctx.lineWidth = 2.5;
      ctx.strokeStyle = '#cbd5e1';
      ctx.stroke();
      ctx.restore();
    }

    function drawArrow() {
      const p1 = toScreen({ x: 0.55, y: height * 0.18 });
      const p2 = toScreen({ x: 0.75, y: height * 0.85 });
      ctx.save();
      ctx.strokeStyle = '#94a3b8';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);
      ctx.stroke();

      const ang = Math.atan2(p2.y - p1.y, p2.x - p1.x);
      const len = 12;
      ctx.beginPath();
      ctx.moveTo(p2.x, p2.y);
      ctx.lineTo(p2.x - len * Math.cos(ang - Math.PI / 6), p2.y - len * Math.sin(ang - Math.PI / 6));
      ctx.lineTo(p2.x - len * Math.cos(ang + Math.PI / 6), p2.y - len * Math.sin(ang + Math.PI / 6));
      ctx.closePath();
      ctx.fillStyle = '#94a3b8';
      ctx.fill();
      ctx.restore();
    }

    function render() {
      const u = value / 1000;
      const s = stateFromU(u);
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      drawTrail();
      drawLine(geom.A, geom.D, { strokeStyle: '#cbd5e1', lineWidth: 7 });
      drawPolygon([geom.A, geom.B, geom.C], {
        fillStyle: 'rgba(148,163,184,0.08)',
        strokeStyle: '#111827',
        lineWidth: 3
      });
      drawPolygon([geom.B, s.F, s.E], {
        fillStyle: 'rgba(59,130,246,0.08)',
        strokeStyle: '#2563eb',
        lineWidth: 3
      });
      drawLine(geom.B, s.F, { strokeStyle: '#2563eb', lineWidth: 3.5 });
      drawLine(geom.D, s.E, { strokeStyle: '#ef4444', lineWidth: 4 });
      drawLine(geom.D, s.Emin, { strokeStyle: '#16a34a', lineWidth: 3, dash: [10, 7] });
      drawArrow();

      drawPoint(geom.A, 'A', '#111827', 10, -12, 7);
      drawPoint(geom.B, 'B', '#111827', -30, 28, 7);
      drawPoint(geom.C, 'C', '#111827', 10, 28, 7);
      drawPoint(geom.D, 'D', '#111827', 10, 28, 7);
      drawPoint(s.F, 'F', '#f59e0b', 10, -12, 8.5);
      drawPoint(s.E, 'E', '#ef4444', 10, -12, 8.5);
      drawPoint(s.Fmin, 'F*', '#16a34a', 10, 24, 6.5);
      drawPoint(s.Emin, 'E*', '#16a34a', 10, 24, 6.5);

      deNowEl.textContent = formatNum(s.DE);
      const close = Math.abs(s.DE - 1.5) < 0.02;
      tipBox.innerHTML = `设 <b>DF = t</b>，则这一侧对应的几何关系可化为：<br>
      <b>DE² = t² - 3√3t + 9</b>。<br>
      因此当 <b>t = 3√3 / 2</b> 时，<b>DE</b> 最小，也就是当 <b>F 恰好在 AD 的中点</b> 时，<b>DE 最小值 = 3/2</b>。${close ? '<br><b>现在已经到达最短位置。</b>' : ''}`;
    }

    function animate() {
      if (playing) {
        value += 4 * direction;
        if (value >= 1000) {
          value = 1000;
          direction = -1;
        }
        if (value <= 0) {
          value = 0;
          direction = 1;
        }
        slider.value = value;
        render();
      }
      requestAnimationFrame(animate);
    }

    playBtn.addEventListener('click', () => {
      playing = !playing;
      playBtn.textContent = playing ? '暂停' : '继续播放';
    });

    resetBtn.addEventListener('click', () => {
      value = 0;
      direction = 1;
      slider.value = value;
      render();
    });

    slider.addEventListener('input', (e) => {
      value = Number(e.target.value);
      render();
    });

    render();
    requestAnimationFrame(animate);
  </script>
</body>
</html>
