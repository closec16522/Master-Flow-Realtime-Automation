/**
 * Module 2: Avatar & Identity System
 * - แปลงโปรไฟล์คนดูเป็นตัวละคร 2D/3D
 * - ขยายขนาด (Scale) ตามยอดเปย์สะสม
 * - จัดการ Chat Bubble เหนือศีรษะตัวละคร
 */

export class AvatarSystem {
  constructor(maxAvatars = 24) {
    this.avatars = new Map();
    this.maxAvatars = maxAvatars;
  }

  upsertViewer({ userId, nickname, avatarUrl, coins = 0, comment = '' }) {
    const existing = this.avatars.get(userId) || {
      userId,
      nickname,
      avatarUrl,
      totalCoins: 0,
      scale: 1.0,
      x: 15 + Math.random() * 70,
      y: 60 + Math.random() * 25,
      vx: (Math.random() - 0.5) * 0.4,
      bubbleText: '',
      bubbleExpiresAt: 0,
      lastActiveAt: Date.now()
    };

    existing.totalCoins += Number(coins || 0);
    // ขยายขนาดตัวละครตามยอดเปย์ (สูงสุด 2.4x)
    existing.scale = Math.min(2.4, 1.0 + Math.log10(1 + existing.totalCoins) * 0.45);
    existing.lastActiveAt = Date.now();

    if (comment) {
      existing.bubbleText = comment.slice(0, 48);
      existing.bubbleExpiresAt = Date.now() + 5500;
    }

    this.avatars.set(userId, existing);
    this._evictOldestIfNeeded();
    return existing;
  }

  stepPhysics() {
    const now = Date.now();
    for (const av of this.avatars.values()) {
      av.x += av.vx;
      if (av.x < 8 || av.x > 92) av.vx *= -1;
      if (av.bubbleExpiresAt && now > av.bubbleExpiresAt) {
        av.bubbleText = '';
      }
    }
    return Array.from(this.avatars.values());
  }

  _evictOldestIfNeeded() {
    if (this.avatars.size <= this.maxAvatars) return;
    let oldestKey = null;
    let oldestTime = Infinity;
    for (const [k, v] of this.avatars.entries()) {
      if (v.lastActiveAt < oldestTime) {
        oldestTime = v.lastActiveAt;
        oldestKey = k;
      }
    }
    if (oldestKey) this.avatars.delete(oldestKey);
  }
}
