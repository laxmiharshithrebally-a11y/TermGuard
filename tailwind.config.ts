import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "#090D16",
        surface: "#111827",
        "surface-border": "rgba(255, 255, 255, 0.08)",
        cyan: {
          400: "#22d3ee",
          500: "#06b6d4",
          600: "#0891b2",
        },
      },
      fontFamily: {
        mono: ["var(--font-jetbrains-mono)", "monospace"],
        sans: ["var(--font-jakarta)", "sans-serif"],
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "glow-fade": "glowFade 2s ease-in-out infinite alternate",
      },
      keyframes: {
        glowFade: {
          "0%": { boxShadow: "0 0 10px rgba(6, 182, 212, 0.3)" },
          "100%": { boxShadow: "0 0 25px rgba(6, 182, 212, 0.7)" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
