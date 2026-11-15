/**
 * Worker Service Entrypoint (Backend / WebSocket / Event Streamer)
 * Port HTTP: 3334 | WebSocket: ws://127.0.0.1:3334
 */

const http = require('http');
const express = require('express');
const cors = require('cors');
const { WebSocketServer } = require('ws');

const { TikTokIngestionLayer } = require('./modules/ingestion');
const { ComplianceShield } = require('./modules/antiCensor');
const { SmartQueueEngine } = require('./modules/smartQueue');
const { VoiceDirector } = require('./modules/voiceDirector');
const { AssetManager } = require('./modules/assetManager');

const app = express();
app.use(cors());
app.use(express.json());

const server = http.createServer(app);
const wss = new WebSocketServer({ server });

const shield = new ComplianceShield(true);
const voiceDirector = new VoiceDirector({ cooldownMs: 3500 });
const assetManager = new AssetManager();

function broadcast(type, payload) {
  const packet = JSON.stringify({ type, payload, ts: Date.now() });
  for (const client of wss.clients) {
    if (client.readyState === 1) {
      client.send(packet);
    }
  }
}

const smartQueue = new SmartQueueEngine({
  milestoneTarget: 500,
  onDispatch: (gift) => {
    const safeLabel = shield.formatSafeGiftLabel(gift.giftName, gift.coins);
    const speech = assetManager.getConfig().ttsEnabled
      ? voiceDirector.buildThankYouSpeech(gift.userId, gift.nickname, gift.giftName)
      : null;
    broadcast('GIFT_EFFECT', { ...gift, safeLabel, speech });
  },
  onMilestone: (milestone) => {
    broadcast('GOD_MILESTONE', milestone);
  }
});

const ingestion = new TikTokIngestionLayer({
  onChat: (chat) => {
    const cleanComment = shield.sanitizeText(chat.comment);
    broadcast('CHAT_BUBBLE', { ...chat, comment: cleanComment });
  },
  onGift: (gift) => smartQueue.enqueueGift(gift),
  onLike: (like) => broadcast('LIKE_BURST', like),
  onFollow: (follow) => broadcast('NEW_FOLLOWER', follow),
  onStatus: (status) => broadcast('STREAM_STATUS', status)
});

wss.on('connection', (ws) => {
  ws.send(JSON.stringify({
    type: 'INIT_STATE',
    payload: {
      config: assetManager.getConfig(),
      themes: assetManager.getThemes(),
      connected: ingestion.isConnected,
      username: ingestion.username
    }
  }));
});

app.get('/api/health', (_req, res) => {
  res.json({
    ok: true,
    connected: ingestion.isConnected,
    username: ingestion.username,
    clients: wss.clients.size
  });
});

app.post('/api/connect', async (req, res) => {
  try {
    const state = await ingestion.connect(req.body.username);
    res.json({ ok: true, roomId: state.roomId });
  } catch (err) {
    res.status(500).json({ ok: false, error: err.message });
  }
});

app.post('/api/config', (req, res) => {
  const updated = assetManager.updateConfig(req.body || {});
  if (typeof req.body?.complianceShield === 'boolean') {
    shield.setEnabled(req.body.complianceShield);
  }
  broadcast('CONFIG_UPDATE', updated);
  res.json({ ok: true, config: updated });
});

app.post('/api/simulate', (req, res) => {
  const { kind = 'gift', nickname = 'ผู้ศรัทธา 99', comment = 'ขอพรให้ร่ำรวย', giftName = 'มณีนาคราช', coins = 99 } = req.body || {};
  if (kind === 'chat') {
    broadcast('CHAT_BUBBLE', { userId: nickname, nickname, avatarUrl: '', comment: shield.sanitizeText(comment) });
  } else if (kind === 'gift') {
    smartQueue.enqueueGift({ userId: nickname, nickname, avatarUrl: '', giftName, count: 1, coins: Number(coins) });
  } else if (kind === 'like') {
    broadcast('LIKE_BURST', { userId: nickname, nickname, likeCount: 15 });
  }
  res.json({ ok: true });
});

const PORT = process.env.WORKER_PORT || 3334;
server.listen(PORT, '127.0.0.1', () => {
  console.log(`[TikTok-Live-Worker] WebSocket & REST running at http://127.0.0.1:${PORT}`);
});
