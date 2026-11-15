/**
 * Module 3: Gift Trigger & Smart Queue Engine
 * - จัดคิวลำดับการแสดงผลของขวัญ (Priority Queue: ของขวัญใหญ่แทรกคิวได้)
 * - นับสะสม Milestone เพื่อเรียก "สัตว์เทพ / บอส" ทะยานเข้าจอ
 */

class SmartQueueEngine {
  constructor({ milestoneTarget = 500, onDispatch, onMilestone }) {
    this.queue = [];
    this.isProcessing = false;
    this.milestoneTarget = milestoneTarget;
    this.milestoneProgress = 0;
    this.onDispatch = onDispatch;
    this.onMilestone = onMilestone;
  }

  enqueueGift(giftEvent) {
    const priority = giftEvent.coins >= 99 ? 2 : giftEvent.coins >= 10 ? 1 : 0;
    const item = {
      ...giftEvent,
      priority,
      enqueuedAt: Date.now()
    };

    // High-value gifts jump ahead of standard gifts
    if (priority >= 2) {
      const idx = this.queue.findIndex((q) => q.priority < 2);
      if (idx === -1) this.queue.push(item);
      else this.queue.splice(idx, 0, item);
    } else {
      this.queue.push(item);
    }

    // Track God / Mythical Beast Milestone
    this.milestoneProgress += Number(giftEvent.coins || 1);
    if (this.milestoneProgress >= this.milestoneTarget) {
      const overflow = this.milestoneProgress % this.milestoneTarget;
      this.milestoneProgress = overflow;
      if (this.onMilestone) {
        this.onMilestone({
          triggerUser: giftEvent.nickname,
          avatarUrl: giftEvent.avatarUrl,
          target: this.milestoneTarget
        });
      }
    }

    this._processNext();
  }

  _processNext() {
    if (this.isProcessing || this.queue.length === 0) return;
    this.isProcessing = true;
    const nextItem = this.queue.shift();

    if (this.onDispatch) {
      this.onDispatch({
        ...nextItem,
        queueRemaining: this.queue.length,
        milestoneProgress: this.milestoneProgress,
        milestoneTarget: this.milestoneTarget
      });
    }

    const durationMs = nextItem.coins >= 99 ? 4200 : 2400;
    setTimeout(() => {
      this.isProcessing = false;
      this._processNext();
    }, durationMs);
  }
}

module.exports = { SmartQueueEngine };
