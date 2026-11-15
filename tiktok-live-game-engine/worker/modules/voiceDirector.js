/**
 * Module 5: AI Voice Director / TTS System
 * - สุ่มแพทเทิร์นคำพูดขอบคุณภาษาไทย ไม่พูดซ้ำซาก
 * - มีระบบ Anti-Spam Cooldown ต่อผู้ใช้และภาพรวม
 */

const THANK_PATTERNS = [
  (user, gift) => `กราบขอบพระคุณคุณ ${user} สำหรับ ${gift} นะครับ ขอให้เฮงๆ รวยๆ ปังๆ ตลอดทั้งวัน`,
  (user, gift) => `ว้าว! คุณ ${user} ส่ง ${gift} มาให้กำลังใจแล้ว ขอบคุณมากๆ เลยครับผม`,
  (user, gift) => `สาธุ! คุณ ${user} ร่วมส่ง ${gift} เข้ามา ขอให้สมหวังดังปรารถนาทุกประการครับ`,
  (user, gift) => `สุดยอดเลยครับคุณ ${user} กับ ${gift} พลังบวกเต็มเปี่ยม ขอบคุณจากใจครับ`,
  (user, gift) => `โมทนาและขอบคุณคุณ ${user} ที่ส่ง ${gift} มาร่วมสนุกกันนะครับ ขอให้โชคดีมีชัย`
];

class VoiceDirector {
  constructor({ cooldownMs = 3500 } = {}) {
    this.cooldownMs = cooldownMs;
    this.lastSpokenAt = 0;
    this.lastPatternIdx = -1;
    this.userLastSpoken = new Map();
  }

  buildThankYouSpeech(userId, nickname, giftLabel) {
    const now = Date.now();
    if (now - this.lastSpokenAt < this.cooldownMs) {
      return null; // Global Anti-Spam
    }
    const prevUserTime = this.userLastSpoken.get(userId) || 0;
    if (now - prevUserTime < 8000) {
      return null; // Per-User Anti-Spam
    }

    let idx = Math.floor(Math.random() * THANK_PATTERNS.length);
    if (idx === this.lastPatternIdx) {
      idx = (idx + 1) % THANK_PATTERNS.length;
    }
    this.lastPatternIdx = idx;
    this.lastSpokenAt = now;
    this.userLastSpoken.set(userId, now);

    return THANK_PATTERNS[idx](nickname, giftLabel);
  }
}

module.exports = { VoiceDirector };
