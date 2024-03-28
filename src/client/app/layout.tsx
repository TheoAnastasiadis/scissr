import type { Metadata } from "next";
import localFont from "next/font/local";
import { Inter_Tight } from "next/font/google";

import "./globals.css";

// Font Awesome
import { config } from "@fortawesome/fontawesome-svg-core";
import "@fortawesome/fontawesome-svg-core/styles.css";
config.autoAddCss = false;

// Local Fonts
const ProtestGuerrilla = localFont({
  src: "../public/fonts/ProtestGuerrilla-Regular.ttf",
  variable: "--font-protest",
  display: "swap",
});

const MetrophobicRegular = localFont({
  src: "../public/fonts/Metrophobic-Regular.ttf",
  variable: "--font-metrophobic",
  display: "swap",
});

// Google Fonts
const InterTight = Inter_Tight({
  subsets: ["greek", "latin"],
  variable: "--font-inter-tight",
});

// UI
import { Providers } from "./providers";

// Meta
export const metadata: Metadata = {
  title: "SCISSR",
  description: "Dating made fun",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`dark ${ProtestGuerrilla.variable} ${MetrophobicRegular.variable} ${InterTight.variable}`}
    >
      <body className="font-metrophobic">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
