/**
 * Module 6: Three.js Transparent 3D Scene Renderer + WebSocket Client
 */
import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { AvatarSystem } from './AvatarSystem';
import { MiniGameEngine } from './MiniGameEngine';

export default function SceneRenderer3D({ wsUrl = 'ws://127.0.0.1:3334' }) {
  const mountRef = useRef(null);
  const avatarSys = useRef(new AvatarSystem(24));
  const miniGame = useRef(new MiniGameEngine('parade'));

  const [avatars, setAvatars] = useState([]);
  const [giftBanner, setGiftBanner] = useState(null);
  const [godMilestone, setGodMilestone] = useState(null);
  const [config, setConfig] = useState({ transparentMode: true, minigameMode: 'parade' });

  // WebGL 3D Transparent Particles + Rotating Sacred/Neon Halo
  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 5;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x000000, 0); // Transparent background for OBS/TikTok Studio
    container.appendChild(renderer.domElement);

    const ringGeo = new THREE.TorusGeometry(1.4, 0.04, 16, 80);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0xfbbf24, transparent: true, opacity: 0.7 });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    scene.add(ring);

    let animId;
    const animate = () => {
      animId = requestAnimationFrame(animate);
      ring.rotation.z += 0.01;
      ring.rotation.x = Math.sin(Date.now() * 0.001) * 0.25;
      renderer.render(scene, camera);
      setAvatars([...avatarSys.current.stepPhysics()]);
    };
    animate();

    return () => {
      cancelAnimationFrame(animId);
      renderer.dispose();
      if (renderer.domElement.parentNode) container.removeChild(renderer.domElement);
    };
  }, []);

  // WebSocket Connection to Worker Service
  useEffect(() => {
    const ws = new WebSocket(wsUrl);
    ws.onmessage = (evt) => {
      const { type, payload } = JSON.parse(evt.data);
      if (type === 'INIT_STATE' || type === 'CONFIG_UPDATE') {
        const nextCfg = payload.config || payload;
        setConfig(nextCfg);
        if (nextCfg.minigameMode) miniGame.current.setMode(nextCfg.minigameMode);
      } else if (type === 'CHAT_BUBBLE') {
        avatarSys.current.upsertViewer(payload);
        miniGame.current.onChatOrGift(payload);
      } else if (type === 'GIFT_EFFECT') {
        avatarSys.current.upsertViewer(payload);
        miniGame.current.onChatOrGift(payload);
        setGiftBanner(payload);
        if (payload.speech && window.speechSynthesis) {
          const utter = new SpeechSynthesisUtterance(payload.speech);
          utter.lang = 'th-TH';
          window.speechSynthesis.speak(utter);
        }
        setTimeout(() => setGiftBanner(null), 3500);
      } else if (type === 'GOD_MILESTONE') {
        setGodMilestone(payload);
        setTimeout(() => setGodMilestone(null), 4500);
      }
    };
    return () => ws.close();
  }, [wsUrl]);

  return (
    <div style={{ position: 'relative', width: '100vw', height: '100vh', overflow: 'hidden', background: config.transparentMode ? 'transparent' : '#060814' }}>
      <div ref={mountRef} style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }} />

      {godMilestone && (
        <div style={{ position: 'absolute', top: '18%', left: '50%', transform: 'translateX(-50%)', background: 'linear-gradient(90deg, #f59e0b, #ef4444)', color: '#fff', padding: '12px 24px', borderRadius: 16, fontWeight: 900, boxShadow: '0 0 30px #f59e0b' }}>
          🐉 สัตว์เทพทะยานเข้าจอ! ขอบคุณคุณ {godMilestone.triggerUser}
        </div>
      )}

      {giftBanner && (
        <div style={{ position: 'absolute', top: '8%', left: '50%', transform: 'translateX(-50%)', background: 'rgba(15,23,42,0.9)', border: '2px solid #fbbf24', color: '#fde68a', padding: '10px 20px', borderRadius: 14, fontWeight: 800 }}>
          🎁 {giftBanner.nickname} {giftBanner.safeLabel}
        </div>
      )}

      {avatars.map((av) => (
        <div key={av.userId} style={{ position: 'absolute', left: `${av.x}%`, top: `${av.y}%`, transform: `translate(-50%, -50%) scale(${av.scale})`, textAlign: 'center', transition: 'transform 0.3s ease' }}>
          {av.bubbleText && (
            <div style={{ background: '#fff', color: '#0f172a', fontSize: 11, fontWeight: 700, padding: '4px 8px', borderRadius: 10, marginBottom: 4, maxWidth: 140 }}>
              {av.bubbleText}
            </div>
          )}
          <div style={{ width: 42, height: 42, borderRadius: '50%', border: '2px solid #fbbf24', background: '#1e293b', margin: '0 auto', overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontWeight: 800 }}>
            {av.avatarUrl ? <img src={av.avatarUrl} alt={av.nickname} style={{ width: '100%', height: '100%', objectFit: 'cover' }} /> : av.nickname?.slice(0, 2)}
          </div>
          <div style={{ fontSize: 10, color: '#fff', textShadow: '0 1px 3px #000', fontWeight: 700 }}>{av.nickname}</div>
        </div>
      ))}
    </div>
  );
}
