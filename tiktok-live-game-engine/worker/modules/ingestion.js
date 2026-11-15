/**
 * Module 1: TikTok Live Data Ingestion Layer
 * - เชื่อมต่อ TikTok Live API (tiktok-live-connector)
 * - ดักจับ Chat, Gift, Like, Follow แบบ Real-time
 */

const { WebcastPushConnection } = require('tiktok-live-connector');

class TikTokIngestionLayer {
  constructor({ onChat, onGift, onLike, onFollow, onStatus }) {
    this.connection = null;
    this.username = '';
    this.isConnected = false;
    this.callbacks = { onChat, onGift, onLike, onFollow, onStatus };
  }

  async connect(uniqueId) {
    const cleanId = String(uniqueId || '').replace(/^@/, '').trim();
    if (!cleanId) throw new Error('TikTok username is required');

    if (this.connection) {
      try { this.connection.disconnect(); } catch (_) {}
    }

    this.username = cleanId;
    this.connection = new WebcastPushConnection(cleanId, {
      processInitialData: false,
      enableExtendedGiftInfo: true
    });

    this.connection.on('chat', (data) => {
      this.callbacks.onChat?.({
        userId: data.uniqueId || data.userId,
        nickname: data.nickname || data.uniqueId,
        avatarUrl: data.profilePictureUrl || '',
        comment: data.comment || ''
      });
    });

    this.connection.on('gift', (data) => {
      // Only trigger on gift streak end (or non-streakable gifts)
      if (data.giftType === 1 && !data.repeatEnd) return;
      const count = data.repeatCount || 1;
      const coins = (data.diamondCount || 1) * count;
      this.callbacks.onGift?.({
        userId: data.uniqueId || data.userId,
        nickname: data.nickname || data.uniqueId,
        avatarUrl: data.profilePictureUrl || '',
        giftName: data.giftName || 'Gift',
        count,
        coins
      });
    });

    this.connection.on('like', (data) => {
      this.callbacks.onLike?.({
        userId: data.uniqueId || data.userId,
        nickname: data.nickname || data.uniqueId,
        avatarUrl: data.profilePictureUrl || '',
        likeCount: data.likeCount || 1
      });
    });

    this.connection.on('follow', (data) => {
      this.callbacks.onFollow?.({
        userId: data.uniqueId || data.userId,
        nickname: data.nickname || data.uniqueId,
        avatarUrl: data.profilePictureUrl || ''
      });
    });

    this.connection.on('disconnected', () => {
      this.isConnected = false;
      this.callbacks.onStatus?.({ connected: false, username: this.username });
    });

    const state = await this.connection.connect();
    this.isConnected = true;
    this.callbacks.onStatus?.({
      connected: true,
      username: this.username,
      roomId: state.roomId
    });
    return state;
  }
}

module.exports = { TikTokIngestionLayer };
