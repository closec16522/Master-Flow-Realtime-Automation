import React from 'react';
import SceneRenderer3D from './engine/SceneRenderer3D';

export default function App() {
  return <SceneRenderer3D wsUrl="ws://127.0.0.1:3334" />;
}
