import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      colors: {
        black: {
          500: "#130720",
          900: "#021002",
        },
        primary: {
          1000: "#5e10a8",
          900: "#6e28b1",
          800: "#7e40b9",
          700: "#8e58c2",
          600: "#9e70cb",
          500: "#af88d4",
          400: "#bf9fdc",
          300: "#cfb7e5",
          200: "#dfcfee",
          100: "#efe7f6",
        },
        sucess: {
          1000: "#237429",
          900: "#39823e",
          800: "#4f9054",
          700: "#659e69",
          600: "#7bac7f",
          500: "#91ba94",
          400: "#a7c7a9",
          300: "#bdd5bf",
          200: "#d3e3d4",
          100: "#e9f1ea",
        },
        info: {
          1000: "#ffe3f1",
          900: "#e6ccd9",
          800: "#ccb6c1",
          700: "#b39fa9",
          600: "#998891",
          500: "#807279",
          400: "#665b60",
          300: "#4c4448",
          200: "#332d30",
          100: "#191718",
        },
        error: {
          1000: "#ae455d",
          900: "#9d3e54",
          800: "#8b374a",
          700: "#7a3041",
          600: "#682938",
          500: "#57232f",
          400: "#461c25",
          300: "#34151c",
          200: "#230e13",
          100: "#110709",
        },
      },
      fontFamily: {
        "flow-circular": ['"Flow Circular"', "system-ui"],
        archivo: ['"Archivo Black"', "sans-serif"],
        shadows: ['"Shadows Into Light"', "cursive"],
        protest: ['"Protest Guerrilla"', "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
