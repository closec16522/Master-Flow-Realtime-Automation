/**
 * Module 4: Engagement & Mini-Game Modules
 * - parade: รถแห่มหาสนุก (ตัวละครเกาะขบวนรถแห่)
 * - dance: นักเต้นแดนซ์ปาร์ตี้กลางเวที
 * - lantern: โคมลอย / กระทงอธิษฐานลอยขึ้นฟ้า
 * - top_spender: คิวโชว์ตัว Top Spender บนแท่นเกียรติยศ
 */

export class MiniGameEngine {
  constructor(initialMode = 'parade') {
    this.mode = initialMode;
    this.lanterns = [];
    this.topSpenders = new Map();
  }

  setMode(mode) {
    this.mode = mode;
  }

  onChatOrGift({ userId, nickname, comment, coins = 0 }) {
    if (coins > 0) {
      const prev = this.topSpenders.get(userId) || { userId, nickname, coins: 0 };
      prev.coins += coins;
      this.topSpenders.set(userId, prev);
    }

    if (this.mode === 'lantern' && (comment || coins > 0)) {
      this.lanterns.push({
        id: `${Date.now()}-${Math.random()}`,
        nickname,
        text: comment || 'อธิษฐานสมหวัง',
        x: 10 + Math.random() * 80,
        y: 95,
        speed: 0.35 + Math.random() * 0.25
      });
      if (this.lanterns.length > 18) this.lanterns.shift();
    }
  }

  getTopSpenders(limit = 5) {
    return Array.from(this.topSpenders.values())
      .sort((a, b) => b.coins - a.coins)
      .slice(0, limit);
  }

  step() {
    this.lanterns = this.lanterns
      .map((l) => ({ ...l, y: l.y - l.speed }))
      .filter((l) => l.y > -10);
    return {
      mode: this.mode,
      lanterns: this.lanterns,
      topSpenders: this.getTopSpenders()
    };
  }
}
