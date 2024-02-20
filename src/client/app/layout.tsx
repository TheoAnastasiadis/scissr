/* eslint-disable @next/next/no-page-custom-font */
import type { Metadata } from "next";
import "./globals.css";

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
    <html lang="en">
      <head>
        <style>
          <link rel="preconnect" href="https://fonts.googleapis.com" />
          <link
            rel="preconnect"
            href="https://fonts.gstatic.com"
            crossOrigin={"anonymous"}
          />
          <link
            href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Flow+Circular&family=Protest+Guerrilla&family=Shadows+Into+Light&display=swap"
            rel="stylesheet"
          />
        </style>
      </head>
      <body>{children}</body>
    </html>
  );
}
