import { nextui } from "@nextui-org/react";
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        protest: ["var(--font-protest)"],
        metrophobic: ["var(--font-metrophobic)"],
        inter: ["var(--font-inter-tight)"],
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      animation: {
        spotlight: "spotlight 2s ease .75s 1 forwards",
      },
      keyframes: {
        spotlight: {
          "0%": {
            opacity: "0%",
            transform: "translate(-72%, -62%) scale(0.5)",
          },
          "100%": {
            opacity: "100%",
            transform: "translate(-50%,-40%) scale(1)",
          },
        },
      },
    },
  },
  darkMode: "class",
  plugins: [nextui()],
};
export default config;
