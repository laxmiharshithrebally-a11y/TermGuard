"use client";

import React, { useState, useEffect } from "react";
import { ShieldCheck, Lock, Activity, Sparkles } from "lucide-react";

interface SplashIntroProps {
  onComplete?: () => void;
}

export default function SplashIntro({ onComplete }: SplashIntroProps) {
  const [visible, setVisible] = useState(true);
  const [fading, setFading] = useState(false);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Fill progress bar over 1.6s
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 5;
      });
    }, 75);

    // Trigger fade-out at 1.7s
    const fadeTimer = setTimeout(() => {
      setFading(true);
    }, 1700);

    // Completely unmount at 2.2s
    const completeTimer = setTimeout(() => {
      setVisible(false);
      if (onComplete) onComplete();
    }, 2200);

    return () => {
      clearInterval(progressInterval);
      clearTimeout(fadeTimer);
      clearTimeout(completeTimer);
    };
  }, [onComplete]);

  if (!visible) return null;

  return (
    <div
      className={`fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#090d16] text-white transition-opacity duration-500 ${
        fading ? "opacity-0 pointer-events-none" : "opacity-100"
      }`}
    >
      {/* Background Radial Glow */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-indigo-950/60 via-[#090d16] to-[#04060a] pointer-events-none" />

      {/* Decorative Grid Lines */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b15_1px,transparent_1px),linear-gradient(to_bottom,#1e293b15_1px,transparent_1px)] bg-[size:4rem_4rem] pointer-events-none" />

      {/* Center Animated Emblem */}
      <div className="relative z-10 flex flex-col items-center text-center space-y-6 max-w-md px-6">
        {/* Shield Icon with Rotating Glow Rings */}
        <div className="relative flex items-center justify-center">
          {/* Pulsing Outer Ring */}
          <div className="absolute w-28 h-28 rounded-full border border-indigo-500/30 animate-ping pointer-events-none" />
          <div className="absolute w-24 h-24 rounded-full border border-indigo-500/50 animate-pulse pointer-events-none" />

          {/* Core Shield */}
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-indigo-600 via-indigo-700 to-slate-900 border border-indigo-400/40 flex items-center justify-center shadow-2xl shadow-indigo-500/50">
            <ShieldCheck className="w-10 h-10 text-white animate-bounce" />
          </div>
        </div>

        {/* Brand Name with Glow */}
        <div className="space-y-1.5">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-950/80 border border-indigo-700/60 text-indigo-300 text-[11px] font-bold uppercase tracking-widest">
            <Sparkles className="w-3 h-3 text-indigo-400" />
            <span>Autonomous Contract Defense</span>
          </div>

          <h1 className="text-4xl sm:text-5xl font-black tracking-tight text-white drop-shadow-md">
            Term<span className="bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">Guard</span>
          </h1>

          <p className="text-xs sm:text-sm text-slate-400 font-medium">
            Guarding notice cutoffs, liability forfeiture & deadline execution
          </p>
        </div>

        {/* Progress Bar & Status */}
        <div className="w-64 space-y-2 pt-2">
          <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden border border-slate-700/50">
            <div
              className="h-full bg-gradient-to-r from-indigo-500 via-cyan-400 to-emerald-400 transition-all duration-100 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
          <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono">
            <span>RADAR INITIALIZATION</span>
            <span className="text-indigo-400 font-bold">{progress}%</span>
          </div>
        </div>
      </div>

      {/* Skip button in corner */}
      <button
        onClick={() => setVisible(false)}
        className="absolute bottom-6 right-6 text-xs text-slate-500 hover:text-white px-3 py-1.5 rounded-lg bg-slate-800/60 border border-slate-700/60 transition-colors"
      >
        Skip Intro →
      </button>
    </div>
  );
}
