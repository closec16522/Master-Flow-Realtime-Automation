/**
 * Module 7: TikTok Compliance & Anti-Restriction Shield
 * - Anti-Censor: กรองคำหยาบและคำต้องห้ามก่อนส่งขึ้นจอหรืออ่านออกเสียง
 * - Compliance Shield: ซ่อนราคาเหรียญ / คำขอของขวัญอัตโนมัติ ป้องกันโดนแบนจากกฎชุมชน TikTok
 */

const BANNED_WORDS = [
  'ควย', 'เหี้ย', 'สัส', 'เย็ด', 'มึง', 'กู', 'อีดอก', 'ระยำ', 'สถุน',
  'พนัน', 'เว็บพนัน', 'บาคาร่า', 'สล็อต', 'แทงบอล', 'ยาเสพติด', 'ฟอกเงิน',
  'fuck', 'shit', 'bitch', 'asshole', 'gamble', 'casino'
];

const GIFT_SOLICITATION_PATTERNS = [
  /ส่งของขวัญ/gi,
  /เปย์/gi,
  /โดเนท/gi,
  /\d+\s*เหรียญ/gi,
  /\d+\s*coins?/gi
];

class ComplianceShield {
  constructor(enabled = true) {
    this.enabled = enabled;
  }

  setEnabled(val) {
    this.enabled = Boolean(val);
  }

  /**
   * กรองคำหยาบและคำต้องห้าม (Anti-Censor)
   */
  sanitizeText(text = '') {
    let clean = String(text).trim();
    for (const word of BANNED_WORDS) {
      const regex = new RegExp(word, 'gi');
      clean = clean.replace(regex, '***');
    }
    if (this.enabled) {
      for (const pattern of GIFT_SOLICITATION_PATTERNS) {
        clean = clean.replace(pattern, '✨');
      }
    }
    return clean;
  }

  /**
   * ปรับข้อความของขวัญให้ปลอดภัยต่อกฎ TikTok Live Studio
   */
  formatSafeGiftLabel(giftName, coins) {
    if (this.enabled) {
      return `ส่งกำลังใจ "${giftName}"`;
    }
    return `ส่ง "${giftName}" (+${coins} เหรียญ)`;
  }
}

module.exports = { ComplianceShield };
