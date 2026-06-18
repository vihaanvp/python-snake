// ════════════════════════════════════════════════════════════
//  Canvas snake animation
// ════════════════════════════════════════════════════════════
(function() {
  const canvas = document.getElementById('snake-canvas');
  const ctx = canvas.getContext('2d');
  let w, h;

  function resize() {
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    w = Math.round(rect.width * dpr);
    h = Math.round(rect.height * dpr);
    canvas.width = w;
    canvas.height = h;
  }
  resize();
  window.addEventListener('resize', resize);

  const segments = 22;
  let time = 0;

  function draw() {
    time += 0.025;
    ctx.clearRect(0, 0, w, h);

    const spacing = w / (segments + 1);
    const amp = h * 0.32;

    for (let i = segments - 1; i >= 0; i--) {
      const x = (i + 1) * spacing;
      const y = h / 2 + Math.sin((i * 0.35) + time * 2.5) * amp;

      const t = i / (segments - 1);
      const brightness = Math.max(60, 200 - i * 7);
      const alpha = 0.35 + 0.65 * (1 - t * 0.5);
      const radius = (i === 0) ? h * 0.22 : h * 0.18 * (1 - t * 0.3);
      const r = Math.max(2, radius);

      // outer glow
      const glow = ctx.createRadialGradient(x, y, 0, x, y, r * 3);
      glow.addColorStop(0, `rgba(0, ${brightness + 40}, 0, ${alpha * 0.25})`);
      glow.addColorStop(1, `rgba(0, 0, 0, 0)`);
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(x, y, r * 3, 0, Math.PI * 2);
      ctx.fill();

      // body segment
      ctx.fillStyle = `rgba(0, ${brightness}, 0, ${alpha})`;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();

      // head: eyes
      if (i === 0) {
        const angle = Math.cos(time * 2.5) * 0.6;
        const ex = Math.cos(angle) * r * 0.45;
        const ey = Math.sin(angle) * r * 0.45;
        ctx.fillStyle = '#0a0a0a';
        ctx.beginPath();
        ctx.arc(x + ex - r * 0.3, y + ey, r * 0.25, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(x + ex + r * 0.3, y + ey, r * 0.25, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    requestAnimationFrame(draw);
  }
  draw();
})();

// ════════════════════════════════════════════════════════════
//  Fetch latest version from GitHub API
// ════════════════════════════════════════════════════════════
(async function() {
  const badge = document.getElementById('version-badge');
  const dlVersion = document.getElementById('dl-version');
  const dlBtn = document.getElementById('dl-btn');

  try {
    const res = await fetch('https://api.github.com/repos/vihaanvp/python-snake/releases/latest');
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();
    const tag = data.tag_name || '';
    if (tag) {
      const label = tag.startsWith('v') ? tag : 'v' + tag;
      badge.textContent = label;
      dlVersion.textContent = label;
      // update download button href to point at this release's asset
      const asset = data.assets && data.assets.find(a => a.name === 'snake.exe');
      if (asset) {
        dlBtn.href = asset.browser_download_url;
      } else {
        // fallback: direct to releases page
        dlBtn.href = data.html_url;
      }
    }
  } catch (e) {
    // keep hardcoded v1.2.0 fallback
    console.log('Could not fetch latest release:', e.message);
  }
})();
