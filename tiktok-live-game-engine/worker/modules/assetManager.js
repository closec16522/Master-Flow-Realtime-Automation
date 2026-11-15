/**
 * Module 8: Customization & Asset Manager
 * - รวม 19 ธีม (4 ธีมหลักเดิม + 15 ธีมใหม่)
 * - จัดการ Config พื้นฐาน, ฉากหลังที่อัปโหลดเอง และโหมดมินิเกม
 */

const THEMES_CATALOG = [
  // 4 Original Themes
  { id: 'naga', name: '🐉 วังบาดาลพญานาคราช & มณีนาคา', category: 'Sacred', accent: '#f59e0b', bg: '#0a1628', minigame: 'lantern' },
  { id: 'ganesha', name: '🐘 มหาเทวาลัยพระพิฆเนศปางประทานทรัพย์', category: 'Sacred', accent: '#fbbf24', bg: '#1e1024', minigame: 'lantern' },
  { id: 'caishen', name: '🪙 ตำหนักไฉ่ซิงเอี๊ย & ต้นไม้ทองคำพันปี', category: 'Sacred', accent: '#ef4444', bg: '#220b0b', minigame: 'top_spender' },
  { id: 'tarot', name: '🔮 สำนักไพ่ทาโรต์ & แมวมงคล AI', category: 'Oracle', accent: '#a855f7', bg: '#130b29', minigame: 'top_spender' },

  // +15 New Themes
  { id: 'parade_truck', name: '🚚 รถแห่มหาสนุก & ขบวนแดนซ์สายย่อ', category: 'MiniGame', accent: '#ec4899', bg: '#170926', minigame: 'parade' },
  { id: 'dance_arena', name: '🪩 เวทีคอนเสิร์ต & แดนซ์ปาร์ตี้ 3D Neon', category: 'MiniGame', accent: '#06b6d4', bg: '#070b1e', minigame: 'dance' },
  { id: 'floating_lantern', name: '🏮 โคมลอยยี่เป็ง & ลอยกระทงอธิษฐาน', category: 'Festival', accent: '#fb923c', bg: '#0c1229', minigame: 'lantern' },
  { id: 'cyber_samurai', name: '⚔️ ซามูไรไซเบอร์ & มังกรนีออน', category: 'Cyberpunk', accent: '#22d3ee', bg: '#060919', minigame: 'dance' },
  { id: 'kumanthong_rich', name: '🧸 กุมารทองมหาเศรษฐี & เรียกทรัพย์ 999', category: 'Sacred', accent: '#f43f5e', bg: '#210a12', minigame: 'top_spender' },
  { id: 'thao_wessuwan', name: '👹 ท้าวเวสสุวรรณโณ มหาเทพคุ้มครองทรัพย์', category: 'Sacred', accent: '#dc2626', bg: '#1a0608', minigame: 'lantern' },
  { id: 'dragon_palace', name: '🐲 ตำหนักมังกรทองจักรพรรดิ 9 มิติ', category: 'Fantasy', accent: '#eab308', bg: '#1a1204', minigame: 'top_spender' },
  { id: 'space_galaxy', name: '🚀 กาแล็กซีอวกาศ & ยานรบพิทักษ์จักรวาล', category: 'SciFi', accent: '#38bdf8', bg: '#030617', minigame: 'dance' },
  { id: 'underwater_mermaid', name: '🧜‍♀️ โลกใต้บาดาล & ฝูงปลาคราฟนำโชค', category: 'Fantasy', accent: '#2dd4bf', bg: '#041c24', minigame: 'lantern' },
  { id: 'muay_thai_arena', name: '🥊 สังเวียนมวยไทยไฟต์เดือด (Team Battle)', category: 'Battle', accent: '#f97316', bg: '#1c0c08', minigame: 'parade' },
  { id: 'cafe_cozy', name: '☕ คาเฟ่อบอุ่น Lo-Fi & น้องแมวบาริสต้า', category: 'Cozy', accent: '#d97706', bg: '#1c140d', minigame: 'top_spender' },
  { id: 'halloween_ghost', name: '👻 คฤหาสน์ภูตผี & ฟักทองเรืองแสง', category: 'Festival', accent: '#a855f7', bg: '#12081c', minigame: 'dance' },
  { id: 'sakura_shrine', name: '🌸 ศาลเจ้าซากุระ & จิ้งจอกเก้าหาง', category: 'Fantasy', accent: '#f472b6', bg: '#1f0d1b', minigame: 'lantern' },
  { id: 'football_stadium', name: '⚽ สนามฟุตบอลโลก & ยิงจุดโทษลุ้นโชค', category: 'Sports', accent: '#22c55e', bg: '#071d10', minigame: 'parade' },
  { id: 'lucky_wheel_casino', name: '🎡 วงล้อมหาโชค & ฝนดาวตกเพชร', category: 'Arcade', accent: '#facc15', bg: '#191305', minigame: 'top_spender' }
];

class AssetManager {
  constructor() {
    this.config = {
      activeTheme: 'naga',
      minigameMode: 'parade',
      transparentMode: true,
      complianceShield: true,
      ttsEnabled: true,
      customBackgroundUrl: ''
    };
  }

  getThemes() {
    return THEMES_CATALOG;
  }

  getConfig() {
    return { ...this.config };
  }

  updateConfig(patch) {
    Object.assign(this.config, patch);
    return this.getConfig();
  }
}

module.exports = { AssetManager, THEMES_CATALOG };
