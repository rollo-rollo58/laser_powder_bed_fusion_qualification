import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        shell: "#090e16",
        panel: "#152233",
        stroke: "#314354",
        aqua: "#67e8d6",
        thermal: "#ff956c",
      },
      fontFamily: { sans: ["Inter", "Arial", "sans-serif"] },
    },
  },
  plugins: [],
};

export default config;
